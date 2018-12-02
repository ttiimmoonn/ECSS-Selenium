from jsonschema import validate
import json
import os
import logging
import re

logger = logging.getLogger("tester")


class ParserSchemaObject:
    """
    Класс для хранения сценариев
    """
    def __init__(self, path):
        self.list_schema = {}
        self.path_schema = path

    def import_schema(self):
        try:
            logger.info("Download schema for commands...")
            schemas = os.listdir(path=self.path_schema)
            for schema in schemas:
                with open(self.path_schema + "/" + schema, "r") as open_schema:
                    self.list_schema[schema] = json.loads(open_schema.read())
        except Exception as ex:
            logger.error("Error Json parsing files: %s", ex)

    def valid_schema(self):
        try:
            validate({"name": "Eggs", "price": "вфыв"}, self.list_schema)
        except Exception as ex:
            logger.error("Error valid commands: %s", ex)

