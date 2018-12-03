import os
import json
import logging
import sys
import signal

from include.parser_schema_class import ParserSchemaObject
from include.mult_proc_driver_class import MultProcess

logging.basicConfig(format=u'%(asctime)-8s %(levelname)-8s [%(module)s:%(lineno)d] %(message)-8s', level=logging.INFO)
logger = logging.getLogger("tester")


def signal_handler(current_signal, frame):
    """
    Удаляем все процессы в случаи завершения через сигнал используя функцию stopProcess
    :param current_signal:
    :param frame:
    :return:
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    logger.info("Received signal %s. Start aborting", current_signal)
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)


path_main = os.getcwd()
a = ParserSchemaObject(path_main + "/" + "jsonschema")
a.import_schema()
with open(path_main + "/" + "test_json.json", "r") as open_test:
    test_schema = json.loads(open_test.read())
commands = test_schema["startTest"]
print(commands)
print(a.valid_schema(commands))
