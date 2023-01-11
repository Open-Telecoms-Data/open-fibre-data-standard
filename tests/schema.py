import json
import os
import jsonref

from libcoveofds.schema import OFDSSchema


class CurrentVersionOFDSSchema(OFDSSchema):
    """
    A Schema object for libcoveofds that is used in these tests.
    The OFDSSchema object always fetches the latest schema from the web.
    This one uses the schema files that are on disk in schema/ directory,
    so any changes to the schema locally are used in the tests.
    """

    def __init__(self):
        filename_package = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "schema", "network-package-schema.json")
        filename_network = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "schema", "network-schema.json")
        with open(filename_package) as fp:
            self.schema = json.load(fp)
        with open(filename_network) as fp:
            self.data_schema = jsonref.load(fp)
        self.schema['properties']['networks']['items'] = self.data_schema

    def get_package_schema_dereferenced(self):
        return self.schema

    def get_package_schema(self):
        return self.schema
