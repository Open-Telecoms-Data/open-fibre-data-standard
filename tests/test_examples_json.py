import os
import json

from .schema import CurrentVersionOFDSSchema
from libcoveofds.additionalfields import AdditionalFields
from libcoveofds.python_validate import PythonValidate
from libcoveofds.jsonschemavalidate import JSONSchemaValidator


class BaseTestExampleDataValid:
    """
    A helper class. Extend it and override get_data to use it.
    Tests data is actually valid.
    """

    def setup_class(self):
        self.schema = CurrentVersionOFDSSchema()

    def get_data(self):
        return {}

    def test_additional_fields(self):
        """Test there is no additional fields. Uses libcoveofds library."""
        worker = AdditionalFields(self.schema)
        results = worker.process(self.get_data())
        assert results == {}

    def test_jsonschema_validation(self):
        """Test there is no JSON Schema validation errors. Uses libcoveofds library."""
        worker = JSONSchemaValidator(self.schema)
        results = worker.validate(self.get_data())
        # We call .json() so that if there any any problems, the output error messages are usefull.
        results = [r.json() for r in results]
        assert results == []

    def test_python_validation(self):
        """Test there is no Python validation errors. Uses libcoveofds library."""
        worker = PythonValidate(self.schema)
        results = worker.validate(self.get_data())
        assert results == []


class TestNetworkPackage(BaseTestExampleDataValid):
    """
    Tests examples/json/network-package.json is valid.
    """

    def get_data(self):
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "examples", "json",
                                "network-package.json")
        with open(filename) as fp:
            return json.load(fp)


class TestMultipleNetworks(BaseTestExampleDataValid):
    """
    Tests examples/json/multiple-networks.json is valid.
    See
    """

    def get_data(self):
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "examples", "json",
                                "multiple-networks.json")
        with open(filename) as fp:
            return json.load(fp)
