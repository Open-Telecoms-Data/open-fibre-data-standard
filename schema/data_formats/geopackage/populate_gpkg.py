import sqlite3
import struct
import uuid

from shapely.geometry import shape

# Adapted from ofds-qgis-plugin's ofdsqgisplugin/python/import_from_json.py.
#
# Differences from the original ImportJSONToCallable:
#   - takes `schema_information` directly instead of loading schema_information.json from a
#     fixed path relative to the plugin, since this repository already generates an equivalent
#     dict in-memory via buildofdsgeopackage.Builder
#   - encodes geometry data as a GeoPackage geometry BLOB (see encode_geometry) instead of as a
#     JSON string, so that the result is a valid GeoPackage outside of QGIS


def encode_geometry(geom_data, srs_id=4326):
    """Encode a GeoJSON geometry dict as a GeoPackage StandardGeoPackageBinary blob."""
    wkb = shape(geom_data).wkb
    # magic (2 bytes), version (1 byte), flags (1 byte: little-endian, no envelope), srs_id (int32)
    header = b"GP" + struct.pack("<BBi", 0, 1, srs_id)
    return header + wkb


def populate_geopackage(gpkg_filename, schema_information, json_data):
    """
    Populate a GeoPackage produced by buildofdsgeopackage.Builder (an empty schema, with codelist
    tables pre-populated) with data from an OFDS JSON file.
    """
    connection = sqlite3.connect(gpkg_filename)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    def callable_write(table_name, data):
        cursor.execute(
            "INSERT INTO "
            + table_name  # nosec B608
            + " ("
            + ",".join([i[0] for i in data])
            + ") VALUES ("
            + ",".join(["?" for i in data])
            + ")",
            [i[1] for i in data],
        )
        cursor.execute("SELECT last_insert_rowid()")
        return cursor.fetchone()[0]

    def callable_read(table_name):
        cursor.execute("SELECT * FROM " + table_name)  # nosec B608
        return cursor.fetchall()

    importer = ImportJSONToCallable(
        json_data, schema_information, callable_write, callable_read
    )
    importer.go()

    connection.commit()
    connection.close()


class ImportJSONToCallable:

    def __init__(self, json_data_to_import, schema_information, callable_write, callable_read):
        self._json_data_to_import = json_data_to_import
        self._schema_information = schema_information
        self._callable_write = callable_write
        self._callable_read = callable_read
        self._open_codelists_codes_to_id_mappings = {}

    def _get_deep_key_from_data_for_import(self, data, key, column_info={}):
        key_bits = key.split("/")
        final_key = key_bits.pop(-1)
        for key_bit in key_bits:
            if key_bit in data and isinstance(data[key_bit], dict):
                data = data[key_bit]
            else:
                return None
        out = data.get(final_key)
        column_type = column_info.get("type")

        # ------------ Foreign key (id and name dict)
        if column_type == "foreign_key_id_name_dict" and isinstance(out, dict):
            return (
                self._standard_id_to_geopackage_id_mappings[
                    column_info["foreignkey_layer"]
                ][out.get("id")]
                if out.get("id")
                in self._standard_id_to_geopackage_id_mappings[
                    column_info["foreignkey_layer"]
                ]
                else None
            )

        # ------------ Foreign key (normal)
        elif column_type == "foreign_key":
            return (
                self._standard_id_to_geopackage_id_mappings[
                    column_info["foreignkey_layer"]
                ][out]
                if out
                in self._standard_id_to_geopackage_id_mappings[
                    column_info["foreignkey_layer"]
                ]
                else None
            )

        # ------------ Open codelist
        elif column_type == "open_codelist" and out:
            # Do we know about this value in our codelist table? If not, add it to our code list table
            if (
                not out
                in self._open_codelists_codes_to_id_mappings[column_info["codelist"]]
            ):
                new_id = self._callable_write(
                    "codelist_open_" + column_info["codelist"][:-4],
                    [("code", out), ("description", out)],
                )
                self._open_codelists_codes_to_id_mappings[column_info["codelist"]][
                    out
                ] = new_id
            # Now return
            return self._open_codelists_codes_to_id_mappings[column_info["codelist"]][
                out
            ]

        # ------------ Any other type
        else:
            return out

    def go(self):
        # Load Codelist data we may need later
        self._open_codelists_codes_to_id_mappings = {}
        for open_codelist_name in self._schema_information["open_codelists"].keys():
            self._open_codelists_codes_to_id_mappings[open_codelist_name] = {}
            for data in self._callable_read("codelist_open_" + open_codelist_name[:-4]):
                self._open_codelists_codes_to_id_mappings[open_codelist_name][
                    data["id"]
                ] = data["code"]
        # For each network ...
        networks = self._json_data_to_import.get("networks", [])
        if isinstance(networks, list):
            for network in networks:
                self._go_network(network)

    def _go_network(self, network):
        # Network table
        network_ofds_id = network["id"] or uuid.uuid4()
        data = []
        for column_info in self._schema_information["tables"]["networks"]["columns"]:
            if column_info["name"] == "ofds_id":
                data.append(("ofds_id", network_ofds_id))
            else:
                data.append(
                    (
                        column_info["name"],
                        self._get_deep_key_from_data_for_import(
                            network,
                            column_info["name"].replace("__", "/"),
                            column_info=column_info,
                        ),
                    )
                )
        network_table_id = self._callable_write("networks", data)
        # Now other tables
        self._standard_id_to_geopackage_id_mappings = {}
        list_idx_to_geopackage_id_mappings = {}
        # First pass, make main tables and store mappings
        # The order of these tables is carefully choosen, as some of them have foreign keys to each other.
        # We have to load the target tables first, so we have information about them before we load the tables that have the foreign keys on.
        for table_name in [
            "phases",
            "organisations",
            "nodes",
            "spans",
            "contracts",
            "wayleaves",
        ]:
            table_datas = network.get(table_name, [])
            self._standard_id_to_geopackage_id_mappings[table_name] = {}
            list_idx_to_geopackage_id_mappings[table_name] = {}
            if isinstance(table_datas, list):
                for idx, table_data in enumerate(table_datas):
                    thing_id = table_data.get("id") or uuid.uuid4()
                    data = [("network_id", network_table_id), ("ofds_id", thing_id)]
                    for column_info in self._schema_information["tables"][table_name][
                        "columns"
                    ]:
                        if column_info["name"] not in ["ofds_id", "network_id"]:
                            data.append(
                                (
                                    column_info["name"],
                                    self._get_deep_key_from_data_for_import(
                                        table_data,
                                        column_info["name"].replace("__", "/"),
                                        column_info=column_info,
                                    ),
                                )
                            )
                    if self._schema_information["tables"][table_name][
                        "geographic_field"
                    ]:
                        geom_data = table_data.get(
                            self._schema_information["tables"][table_name][
                                "geographic_field"
                            ]
                        )
                        if isinstance(geom_data, dict):
                            data.append(("geom", encode_geometry(geom_data)))
                    geopackage_id = self._callable_write(table_name, data)
                    self._standard_id_to_geopackage_id_mappings[table_name][
                        thing_id
                    ] = geopackage_id
                    list_idx_to_geopackage_id_mappings[table_name][idx] = geopackage_id
        # Second pass, some tables underneath the main tables
        for table_name, sub_table_and_field_name, parent_field_name in [
            ("nodes", "internationalConnections", "node_id"),
            ("contracts", "documents", "contract_id"),
        ]:
            table_datas = network.get(table_name, [])
            if isinstance(table_datas, list):
                for idx, table_data in enumerate(table_datas):
                    sub_table_datas = table_data.get(sub_table_and_field_name)
                    if isinstance(sub_table_datas, list):
                        for sub_table_data in sub_table_datas:
                            data = [
                                ("network_id", network_table_id),
                                (
                                    parent_field_name,
                                    list_idx_to_geopackage_id_mappings[table_name][idx],
                                ),
                            ]
                            for column_info in self._schema_information["tables"][
                                table_name + "_" + sub_table_and_field_name
                            ]["columns"]:
                                if column_info["name"] not in [
                                    parent_field_name,
                                    "network_id",
                                ]:
                                    data.append(
                                        (
                                            column_info["name"],
                                            self._get_deep_key_from_data_for_import(
                                                sub_table_data,
                                                column_info["name"].replace("__", "/"),
                                                column_info=column_info,
                                            ),
                                        )
                                    )
                            self._callable_write(
                                table_name + "_" + sub_table_and_field_name,
                                data,
                            )
        # Third pass, relations
        for table_name in [
            "nodes",
            "spans",
            "phases",
            "organisations",
            "contracts",
        ]:
            table_datas = network.get(table_name, [])
            if isinstance(table_datas, list):
                for relation in self._schema_information["tables"][table_name].get(
                    "relations", []
                ):
                    # First, for codelist, we may have to load the codelist contents to memory
                    if (
                        relation.get("codelist")
                        and relation["related_table"]
                        not in self._standard_id_to_geopackage_id_mappings
                    ):
                        self._standard_id_to_geopackage_id_mappings[
                            relation["related_table"]
                        ] = {}
                        for related_data in self._callable_read(
                            relation["related_table"]
                        ):
                            self._standard_id_to_geopackage_id_mappings[
                                relation["related_table"]
                            ][related_data["code"]] = related_data["id"]

                    # Now process
                    for idx, table_data in enumerate(table_datas):
                        relation_datas = table_data.get(relation["standard_field"])
                        if isinstance(relation_datas, list):
                            for relation_data in relation_datas:
                                relation_data_id = (
                                    relation_data
                                    if relation.get("codelist")
                                    or isinstance(relation_data, str)
                                    else relation_data.get("id")
                                )
                                if relation_data_id:
                                    # If an open code list, it may be a new value we have to insert
                                    if (
                                        relation.get("codelist")
                                        and not relation_data_id
                                        in self._standard_id_to_geopackage_id_mappings[
                                            relation["related_table"]
                                        ]
                                    ):
                                        self._standard_id_to_geopackage_id_mappings[
                                            relation["related_table"]
                                        ][relation_data_id] = self._callable_write(
                                            relation["related_table"],
                                            [
                                                ("code", relation_data_id),
                                                ("description", relation_data_id),
                                            ],
                                        )

                                    # Now insert to mapping table
                                    self._callable_write(
                                        relation["mapping_table"],
                                        [
                                            (
                                                "base_id",
                                                list_idx_to_geopackage_id_mappings[
                                                    table_name
                                                ][idx],
                                            ),
                                            (
                                                "related_id",
                                                self._standard_id_to_geopackage_id_mappings[
                                                    relation["related_table"]
                                                ][
                                                    relation_data_id
                                                ],
                                            ),
                                        ],
                                    )
