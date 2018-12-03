from jsonschema import validate
import json
import os
import logging

logger = logging.getLogger("tester")


class ParserSchemaObject:
    def __init__(self, path):
        """
        Класс для хранения сценариев
        :param dictionary_schema: словарь, который хранит schema сценарии json
        :param path_schema: путь до директории с сценариями
        """
        self.dictionary_schema = {}
        self.path_schema = path

    def import_schema(self):
        try:
            logger.info("Download schema for commands...")
            schemas = os.listdir(path=self.path_schema)
            for schema in schemas:
                logger.debug("Reading schema %s...", schema)
                with open(self.path_schema + "/" + schema, "r") as open_schema:
                    self.dictionary_schema[schema] = json.loads(open_schema.read())
                    logger.debug("Schema added to the list of scenarios: %s", self.dictionary_schema)
            return True
        except Exception as ex:
            logger.error("Error Json parsing files: %s", ex)
            return False

    def valid_schema(self, commands):
        error_schemas = []
        status_valid_schema = False
        logger.info("Begin script Command verification...")
        for command in list(commands):
            try:
                for schema in self.dictionary_schema.keys():
                    try:
                        validate(command, self.dictionary_schema[schema])
                        status_valid_schema = True
                        break
                    except Exception as ex:
                        logger.debug("Error valid commands: %s", ex)
                        status_valid_schema = False
                if status_valid_schema:
                    status_valid_schema = False
                else:
                    error_schemas.append(command)
            except Exception as ex:
                logger.error("Error getting list schema: %s", ex)
                return False
        if error_schemas:
            logger.error("Error schema:")
            for error_schema in error_schemas:
                logger.error("    Command: %s", error_schema)
            return False
        else:
            logger.debug("Command [%s] valid schemas.", command)
            return True
