from include.parser_schema_class import ParserSchemaObject
import os
import json
import logging

logging.basicConfig(format=u'%(asctime)-8s %(levelname)-8s [%(module)s:%(lineno)d] %(message)-8s', level=logging.INFO)
logger = logging.getLogger("tester")

path_main = os.getcwd()
a = ParserSchemaObject(path_main + "/" + "jsonschema")
a.import_schema()
with open(path_main + "/" + "test_json.json", "r") as open_test:
    test_schema = json.loads(open_test.read())
commands = test_schema["startTest"]
print(commands)
print(a.valid_schema(commands))
