import csv
import json
import os
import shutil
import sqlite3

MAP_FIELD_TYPES_TO_SQLITE_TYPES = {"boolean": "int", "integer": "int", "number": "real"}


class Builder:

    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.connection = None
        self.cursor = None
        self.information_out = None
        self.MAPPING_FOREIGN_KEY_NAMES_TO_LAYERS = {
            "Phase": "phases",
            "Physical infrastructure provider": "organisations",
            "Supplier": "organisations",
            "Start": "nodes",
            "End": "nodes",
        }
        self.MAPPING_MANY_TO_MANY_KEY_NAMES_TO_LAYERS = {
            "Network providers": "organisations",
            "Funders": "organisations",
            "Related phases": "phases",
        }

    def _load_codelist_items(
        self,
        open_codelist: bool,
        codelist_name: str,
        create_database_table_even_if_closed=False,
    ):
        # If we haven't already loaded the codelist contents, do so
        if (
            codelist_name
            not in self.information_out[
                ("open_codelists" if open_codelist else "closed_codelists")
            ].keys()
        ):
            with open(
                os.path.join(
                    self.root_directory,
                    "buildofdsqgisplugin",
                    "schema_0_3",
                    "codelists",
                    "open" if open_codelist else "closed",
                    codelist_name,
                )
            ) as csvfile:
                csvreader = csv.reader(csvfile)
                headers = next(csvreader)
                raw_values = []
                for line in csvreader:
                    raw_values.append(line)
                values = []
                for raw_value in raw_values:
                    desc = (
                        # Description always has the actual title of the codelist item
                        raw_value[1]
                        # If it's a very long codelist, we add the actual code so that people can see what the codelist is sorted by
                        + (" (" + raw_value[0] + ")" if len(raw_values) > 20 else "")
                        # And if it exists, we add the description of the codelist item
                        + (
                            ": " + raw_value[2]
                            if len(raw_value) > 2 and raw_value[2]
                            else ""
                        )
                    )
                    values.append((raw_value[0], desc))
            self.information_out[
                ("open_codelists" if open_codelist else "closed_codelists")
            ][codelist_name] = values
        if open_codelist or create_database_table_even_if_closed:
            table_name = (
                "codelist_"
                + ("open" if open_codelist else "closed")
                + "_"
                + codelist_name[:-4]
            )
            self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                [table_name],
            )
            if not self.cursor.fetchone():

                self.cursor.execute(
                    """
                    INSERT INTO gpkg_contents (table_name, data_type, identifier, srs_id)
                    VALUES (?, "attributes", ?, 4326);
                    """,
                    [
                        table_name,
                        table_name,
                    ],
                )

                self.cursor.execute(
                    """
                    CREATE TABLE {} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        code TEXT,
                        description TEXT
                    );
                """.format(
                        table_name,
                    )
                )

                for column_name, column_title, column_desc in [
                    ("code", "Code", "The code for this item"),
                    ("description", "Description", "The Description for this item."),
                ]:
                    self.cursor.execute(
                        """
                        INSERT INTO gpkg_data_columns (
                            table_name,
                            column_name,
                            name,
                            title,
                            description,
                            mime_type,
                            constraint_name
                        )
                        VALUES (?, ?, ?, ?, ?, NULL, NULL);
                        """,
                        [
                            table_name,
                            column_name,
                            column_title,
                            column_title,
                            column_title,
                        ],
                    )

                for code, desc in self.information_out[
                    ("open_codelists" if open_codelist else "closed_codelists")
                ][codelist_name]:
                    self.cursor.execute(
                        """
                        INSERT INTO {} (
                            code,
                            description
                        )
                        VALUES (?, ?);
                        """.format(
                            table_name
                        ),
                        [code, desc],
                    )

    def _create_table_from_json_schema(
        self,
        json_schema,
        table_name,
        has_network_id=False,
        parent_column=None,
        geographic_type=None,
        geographic_field=None,
    ):

        columns = self._for_create_table_get_columns_from_json_schema(
            json_schema, table_name, geographic_field
        )

        if has_network_id:
            columns.append(
                {
                    "name": "network_id",
                    "type": "foreign_key",
                    "sqlite_type": "integer",
                    "foreignkey_key": "id",
                    "foreignkey_value": "name",
                    "foreignkey_layer": "networks",
                    "title": "Network ID",
                    "description": "",
                }
            )

        if parent_column:
            columns.append(parent_column)

        for column in columns:
            constraint_name = None

            if column["type"] == "closed_codelist":
                constraint_name = "closed_codelist_" + column["codelist"]

            self.cursor.execute(
                """
                    INSERT INTO gpkg_data_columns (
                        table_name,
                        column_name,
                        name,
                        title,
                        description,
                        mime_type,
                        constraint_name
                    )
                    VALUES (?, ?, ?, ?, ?, NULL, ?);
                    """,
                [
                    table_name,
                    column["name"],
                    column["title"],
                    column["title"],
                    column["description"],
                    constraint_name,
                ],
            )

        fields_sql = [
            '"' + i["name"] + '" ' + i.get("sqlite_type", i["type"]) for i in columns
        ]
        fields_sql += [
            "FOREIGN KEY ({}) REFERENCES codelist_open_{}(id)".format(
                i["name"], i["codelist"][:-4]
            )
            for i in columns
            if i["type"] == "open_codelist"
        ]
        fields_sql += [
            "FOREIGN KEY ({}) REFERENCES {}(id)".format(
                i["name"], i["foreignkey_layer"]
            )
            for i in columns
            if i["type"] in ["foreign_key", "foreign_key_id_name_dict"]
        ]
        self.cursor.execute(
            """
            CREATE TABLE {} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {}
                {}
            );
        """.format(
                table_name,
                "geom BLOB NULL," if geographic_type else "",
                ",".join(fields_sql),
            )
        )

        self.cursor.execute(
            """
            INSERT INTO gpkg_contents (table_name, data_type, identifier, srs_id)
            VALUES ('{}', '{}', '{}', 4326);
        """.format(
                table_name,
                "features" if geographic_type else "attributes",
                table_name,
            )
        )

        if geographic_type:
            self.cursor.execute(
                """
                INSERT INTO gpkg_geometry_columns (
                    table_name, column_name, geometry_type_name, srs_id, z, m
                ) VALUES ('{}', 'geom', '{}', 4326, 0, 0);
            """.format(
                    table_name, geographic_type
                )
            )

        self.information_out["tables"][table_name] = {
            "columns": columns,
            "relations": [],
            "geographic_type": geographic_type,
            "geographic_field": geographic_field,
        }

    def _for_create_table_get_columns_from_json_schema(
        self,
        json_schema,
        table_name,
        geographic_field=None,
        name_prefix="",
        title_prefix="",
        description_prefix="",
    ):
        columns = []
        for property_key, property_value in json_schema["properties"].items():
            # Each column has some fields the same, so set them up here to avoid code reptition
            column = {
                "name": (
                    "ofds_id"
                    if property_key == "id" and not name_prefix
                    else name_prefix + property_key
                ),
                "title": (title_prefix + " " if title_prefix else "")
                + property_value.get("title"),
                "description": (description_prefix + " " if description_prefix else "")
                + property_value.get("description", property_value.get("title")),
            }

            # -------- Date
            if (
                property_value["type"] == "string"
                and property_value.get("format") == "date"
            ):
                column["type"] = "date"
                column["sqlite_type"] = "text"
                columns.append(column)

            # --------  codelist
            elif property_value["type"] == "string" and property_value.get("codelist"):
                # loaded the codelist contents
                self._load_codelist_items(
                    property_value.get("openCodelist"), property_value["codelist"]
                )
                # set up field
                column["type"] = (
                    "open_codelist"
                    if property_value.get("openCodelist")
                    else "closed_codelist"
                )
                column["sqlite_type"] = (
                    "integer" if property_value.get("openCodelist") else "text"
                )
                column["codelist"] = property_value["codelist"]
                columns.append(column)

            # --------  Foreign key (the special type that's a dict with an id and name field)
            elif (
                property_value["type"] == "object"
                and list(property_value["properties"].keys()) == ["id", "name"]
                and property_value["title"]
                in self.MAPPING_FOREIGN_KEY_NAMES_TO_LAYERS.keys()
            ):
                column["type"] = "foreign_key_id_name_dict"
                column["sqlite_type"] = "integer"
                column["foreignkey_key"] = "id"
                column["foreignkey_value"] = "name"
                column["foreignkey_layer"] = self.MAPPING_FOREIGN_KEY_NAMES_TO_LAYERS[
                    property_value["title"]
                ]
                columns.append(column)

            # -------- Foreign key (the normal type)
            elif (
                property_value["type"] == "string"
                and property_value["title"]
                in self.MAPPING_FOREIGN_KEY_NAMES_TO_LAYERS.keys()
            ):
                column["type"] = "foreign_key"
                column["sqlite_type"] = "integer"
                column["foreignkey_key"] = "id"
                column["foreignkey_value"] = "name"
                column["foreignkey_layer"] = self.MAPPING_FOREIGN_KEY_NAMES_TO_LAYERS[
                    property_value["title"]
                ]
                columns.append(column)

            # -------- String
            elif property_value["type"] == "string":
                column["type"] = "text"
                columns.append(column)

            # -------- Boolean
            elif property_value["type"] == "boolean":
                column["type"] = "boolean"
                column["sqlite_type"] = "text"
                columns.append(column)

            # -------- Number
            elif property_value["type"] == "number":
                column["type"] = "number"
                column["sqlite_type"] = "real"
                columns.append(column)

            # -------- Integer
            elif property_value["type"] == "integer":
                column["type"] = "integer"
                column["sqlite_type"] = "integer"
                columns.append(column)

            # -------- An object that we might call recursively
            elif property_value["type"] == "object":
                # First, check for any special cases we ignore because they are handled elsewhere
                if table_name == "networks" and property_key == "crs":
                    continue
                if geographic_field and geographic_field == property_key:
                    continue
                # Ok, we go
                columns.extend(
                    self._for_create_table_get_columns_from_json_schema(
                        property_value,
                        table_name,
                        name_prefix=name_prefix + property_key + "__",
                        description_prefix=(
                            description_prefix + " " if description_prefix else ""
                        )
                        + property_value.get(
                            "description", property_value.get("title")
                        ),
                        title_prefix=(title_prefix + " " if title_prefix else "")
                        + property_value.get("title"),
                    )
                )

        # We're done, return
        return columns

    def _create_relations_from_json_schema(
        self,
        json_schema,
        table_name,
    ):

        relations = self._for_create_relations_get_relations_from_json_schema(
            json_schema, table_name
        )

        for relation in relations:

            # Create mapping table per GeoPackage spec
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS {} (
                    base_id INTEGER NOT NULL,
                    related_id INTEGER NOT NULL,
                    PRIMARY KEY (base_id, related_id),
                    FOREIGN KEY (base_id) REFERENCES {}(id),
                    FOREIGN KEY (related_id) REFERENCES {}(id)
                );
                """.format(
                    relation["mapping_table"], table_name, relation["related_table"]
                )
            )

            # Add to contents
            self.cursor.execute(
                """
                INSERT INTO gpkg_contents (table_name, data_type, identifier, srs_id)
                VALUES ('{}', 'attributes', '{}', 4326);
                """.format(
                    relation["mapping_table"],
                    relation["mapping_table"],
                )
            )

            # Add mapping table to gpkg_extensions per GeoPackage spec
            self.cursor.execute(
                """
                INSERT OR IGNORE INTO gpkg_extensions (table_name, column_name, extension_name, definition, "scope")
                VALUES (?, null, 'gpkg_related_tables','http://docs.opengeospatial.org/is/18-000/18-000.html', 'read-write');
                """,
                [relation["mapping_table"]],
            )

            # Add the relationship to gpkgext_relations
            self.cursor.execute(
                """
                INSERT INTO gpkgext_relations (
                    base_table_name,
                    base_primary_column,
                    related_table_name,
                    related_primary_column,
                    relation_type,
                    mapping_table_name
                )
                VALUES  (
                    ?,
                    'id',
                    ?,
                    'id',
                    ?,
                    ?
                );
                """,
                [
                    table_name,
                    relation["related_table"],
                    relation["name"],
                    relation["mapping_table"],
                ],
            )

        self.information_out["tables"][table_name]["relations"] = relations

    def _write_codelists(self):
        for codelist_name, codelist_values in self.information_out[
            "closed_codelists"
        ].items():
            for codelist_value in codelist_values:
                self.cursor.execute(
                    """
                    INSERT OR IGNORE INTO gpkg_data_column_constraints (
                    constraint_name,
                    constraint_type,
                    value,
                    description
                    )
                    VALUES (
                    ?,
                    'enum',
                    ?,
                    ?
                    );
                """,
                    [
                        "closed_codelist_" + codelist_name,
                        codelist_value[0],
                        codelist_value[1],
                    ],
                )

    def _for_create_relations_get_relations_from_json_schema(
        self,
        json_schema,
        table_name,
    ):
        relations = []
        for property_key, property_value in json_schema["properties"].items():

            # --------  many to many
            if (
                property_value["type"] == "array"
                and property_value["items"]["type"] == "object"
                and property_value["title"]
                in self.MAPPING_MANY_TO_MANY_KEY_NAMES_TO_LAYERS.keys()
            ):

                relations.append(
                    {
                        "standard_field": property_key,
                        "name": table_name + "_" + property_key,
                        "related_table": self.MAPPING_MANY_TO_MANY_KEY_NAMES_TO_LAYERS[
                            property_value["title"]
                        ],
                        "mapping_table": "relation_" + table_name + "_" + property_key,
                        "title": property_value["title"],
                        "related_table_private": False,
                    }
                )

            # --------  multi codelist
            elif property_value["type"] == "array" and property_value.get("codelist"):
                # loaded the codelist contents
                self._load_codelist_items(
                    property_value.get("openCodelist"),
                    property_value["codelist"],
                    create_database_table_even_if_closed=True,
                )
                # set up field
                relations.append(
                    {
                        "standard_field": property_key,
                        "name": table_name + "_" + property_key,
                        "related_table": "codelist_"
                        + ("open" if property_value.get("openCodelist") else "closed")
                        + "_"
                        + property_value["codelist"][:-4],
                        "mapping_table": "relation_" + table_name + "_" + property_key,
                        "title": property_value["title"],
                        "related_table_private": not property_value.get("openCodelist"),
                        "codelist": True,
                    }
                )

        return relations

    def go(self):
        # Load JSON Schema
        jsonschema_filename = os.path.join(
            self.root_directory,
            "buildofdsqgisplugin",
            "schema_0_3",
            "schema.json",
        )
        with open(jsonschema_filename) as fp:
            jsonschema = json.load(fp)
        # Copy GeoPackage
        sqlite_filename = os.path.join(
            self.root_directory,
            "ofdsqgisplugin",
            "schema_0_3",
            "geopackage.gpkg",
        )
        shutil.copyfile(
            os.path.join(
                self.root_directory,
                "buildofdsqgisplugin",
                "empty.gpkg",
            ),
            sqlite_filename,
        )
        # Setup
        self.connection = sqlite3.connect(sqlite_filename)
        self.cursor = self.connection.cursor()
        self.information_out = {
            "tables": {},
            "open_codelists": {},
            "closed_codelists": {},
        }
        # Create extension tables
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS gpkgext_relations (
                id INTEGER PRIMARY KEY AUTOINCREMENT, base_table_name TEXT NOT NULL, base_primary_column TEXT NOT NULL, related_table_name TEXT NOT NULL, related_primary_column TEXT NOT NULL, relation_type TEXT NOT NULL, mapping_table_name TEXT UNIQUE
            );
        """
        )
        # Create gpkg_data_columns per https://www.geopackage.org/spec120/#gpkg_data_columns_sql
        # EXCEPT don't make the name column UNIQUE, this causes us clashes
        # https://www.geopackage.org/spec120/#gpkg_data_columns_cols says "A human-readable identifier (e.g. short name) for the column_name content" so why unique?
        # And indeed this is changed in the unreleased version https://www.geopackage.org/spec/#gpkg_data_columns_sql
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS gpkg_data_columns (
                table_name TEXT NOT NULL, column_name TEXT NOT NULL, name TEXT, title TEXT, description TEXT, mime_type TEXT, constraint_name TEXT,
                CONSTRAINT pk_gdc PRIMARY KEY (table_name, column_name),
                CONSTRAINT fk_gdc_tn FOREIGN KEY (table_name) REFERENCES gpkg_contents(table_name)
            );
        """
        )
        # Create gpkg_data_column_constraints per https://www.geopackage.org/spec120/#gpkg_data_column_constraints_sql
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS gpkg_data_column_constraints (
                constraint_name TEXT NOT NULL, constraint_type TEXT NOT NULL, value TEXT, min NUMERIC, min_is_inclusive BOOLEAN, max NUMERIC, max_is_inclusive BOOLEAN, description TEXT, CONSTRAINT gdcc_ntv UNIQUE (constraint_name, constraint_type, value)
            );
        """
        )
        # Register extensions
        self.cursor.execute(
            "INSERT OR IGNORE INTO gpkg_extensions (table_name, column_name, extension_name, definition, scope) VALUES ('gpkgext_relations', NULL, 'gpkg_related_tables','http://docs.opengeospatial.org/is/18-000/18-000.html', 'read-write');"
        )
        self.cursor.execute(
            "INSERT OR IGNORE INTO gpkg_extensions (table_name, column_name, extension_name, definition, scope) VALUES ('gpkg_data_columns', NULL, 'gpkg_schema','http://www.geopackage.org/spec120/#extension_schema', 'read-write');"
        )
        self.cursor.execute(
            "INSERT OR IGNORE INTO gpkg_extensions (table_name, column_name, extension_name, definition, scope) VALUES ('gpkg_data_column_constraints', NULL, 'gpkg_schema','http://www.geopackage.org/spec120/#extension_schema', 'read-write');"
        )
        # Create Tables
        self._create_table_from_json_schema(jsonschema, table_name="networks")
        self._create_table_from_json_schema(
            jsonschema["properties"]["nodes"]["items"],
            table_name="nodes",
            has_network_id=True,
            geographic_field="location",
            geographic_type="POINT",
        )
        self._create_table_from_json_schema(
            jsonschema["properties"]["spans"]["items"],
            table_name="spans",
            has_network_id=True,
            geographic_field="route",
            geographic_type="LINESTRING",
        )
        self._create_table_from_json_schema(
            jsonschema["properties"]["phases"]["items"],
            table_name="phases",
            has_network_id=True,
        )
        self._create_table_from_json_schema(
            jsonschema["properties"]["organisations"]["items"],
            table_name="organisations",
            has_network_id=True,
        )
        self._create_table_from_json_schema(
            jsonschema["properties"]["contracts"]["items"],
            table_name="contracts",
            has_network_id=True,
        )
        self._create_table_from_json_schema(
            jsonschema["properties"]["nodes"]["items"]["properties"][
                "internationalConnections"
            ]["items"],
            table_name="nodes_internationalConnections",
            has_network_id=True,
            parent_column={
                "name": "node_id",
                "type": "foreign_key",
                "sqlite_type": "integer",
                "foreignkey_key": "id",
                "foreignkey_value": "name",
                "foreignkey_layer": "nodes",
                "title": "Nodes ID",
                "description": "",
            },
        )
        self._create_table_from_json_schema(
            jsonschema["properties"]["contracts"]["items"]["properties"]["documents"][
                "items"
            ],
            table_name="contracts_documents",
            has_network_id=True,
            parent_column={
                "name": "contract_id",
                "type": "foreign_key",
                "sqlite_type": "integer",
                "foreignkey_key": "id",
                "foreignkey_value": "title",
                "foreignkey_layer": "contracts",
                "title": "Contract ID",
                "description": "",
            },
        )
        # Create relations
        self._create_relations_from_json_schema(
            jsonschema["properties"]["nodes"]["items"],
            table_name="nodes",
        )
        self._create_relations_from_json_schema(
            jsonschema["properties"]["spans"]["items"],
            table_name="spans",
        )
        self._create_relations_from_json_schema(
            jsonschema["properties"]["phases"]["items"],
            table_name="phases",
        )
        self._create_relations_from_json_schema(
            jsonschema["properties"]["contracts"]["items"],
            table_name="contracts",
        )
        self._create_relations_from_json_schema(
            jsonschema["properties"]["organisations"]["items"],
            table_name="organisations",
        )
        # Codelists
        self._write_codelists()
        # Wrapup
        self.connection.commit()
        schema_information_json_filename = os.path.join(
            self.root_directory,
            "ofdsqgisplugin",
            "schema_0_3",
            "schema_information.json",
        )
        with open(schema_information_json_filename, "w") as fp:
            json.dump(self.information_out, fp, indent=2)


if __name__ == "__main__":
    builder = Builder(
        root_directory=os.path.realpath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
        ),
    )
    builder.go()
