from include.parser_schema_class import ParserSchemaObject
import os

path_schema = os.getcwd()
print(path_schema)
a = ParserSchemaObject(path_schema + "/" + "jsonschema")
a.import_schema()

print(a.list_schema)