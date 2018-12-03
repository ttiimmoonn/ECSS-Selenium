import re
import time
import logging
import random
import sys
import os
import signal

from datetime import datetime
from multiprocessing import Process, Queue, Manager

from test_1 import browser_watcher, work


def signal_handler(current_signal, frame):
    """
    Удаляем все процессы в случаи завершения через сигнал используя функцию stopProcess
    :param current_signal:
    :param frame:
    :return:
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    logger.info("Received signal %s. Start aborting", current_signal)
    if "test" in globals():
        test.stopProcess()
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


class MultProcess():
    def __init__(self, countDrive = 1, infintTest = False):
        """
        :param countDrive: количество запускаемых дисплеев
        :param infintTest: является ли тест бесконечным (запускает новые процессы в случаи завершения старых)
        :param activeProcesses: словарь из всех активных процессов
        :param manager
        """
        ProcessQueue = Queue()

        self.countDrive = countDrive
        self.infintTest = infintTest

        self.allProcesses = {}
        self.activeProcesses = {}

        self.QueEndProcess = ProcessQueue

    def managerProcess(self):
        """
        Запускает требуемое количество процессов и по требованию контролирует их количество
        self.countDrive: количество процессов которые будут запущены
        self.infintTest: будет ли автоматически поддерживаться count процессов
        self.activeProcesses: записываются созданные и удаленные существуюшие процессы
        self.allProcesses: словарь всех процессов используевых в тесте с временем создания и удаления
        :return:
        """
        try:
            for countDisplayDrive in list(range(self.countDrive)):
                logger.info("Start new process... ")
                self.startProcess()
            if self.infintTest:
                while True:
                    msg = self.QueEndProcess.get()
                    self.allProcesses[msg[0]]["timeEND"] = datetime.now()
                    self.allProcesses[msg[0]]["timeLONG"] = self.allProcesses[msg[0]]["timeSTART"] - self.allProcesses[msg[0]]["timeEND"]
                    self.allProcesses[msg[0]]["EndStatus"] = msg[1]
                    del(self.activeProcesses[msg[0]])
                    logger.info("ID %s process completed. Status completed %s.", msg[0], str(msg[1]))
                    self.startProcess()
                    logger.info("Start new process")
            else:
                while self.activeProcesses != {}:
                    msg = self.QueEndProcess.get()
                    self.allProcesses[msg[0]]["timeEND"] = datetime.now()
                    self.allProcesses[msg[0]]["timeLONG"] = self.allProcesses[msg[0]]["timeSTART"] - self.allProcesses[msg[0]]["timeEND"]
                    self.allProcesses[msg[0]]["EndStatus"] = msg[1]
                    del(self.activeProcesses[msg[0]])
                    logger.info("ID %s process completed. Status completed %s.", msg[0], str(msg[1]))
                    logger.info("Active processes: %s", self.activeProcesses)
        except Exception as ex:
            logger.error("Process manager crashed: %s", ex)

    def startProcess(self):
        ProcessId = generalID()
        proc_selen = Process(target=startDrive, args=(self.QueEndProcess, ProcessId, ))
        self.activeProcesses[ProcessId] = proc_selen
        self.allProcesses[ProcessId] = {"timeSTART": datetime.now(), "timeEND": "", "timeLONG": "", "EndStatus": ""}
        proc_selen.start()
        logger.info("Active processes: %s", self.activeProcesses)
        return True

    def stopProcess(self):
        for ID_procc in self.activeProcesses.keys():
            try:
                self.allProcesses[ID_procc]["timeEND"] = datetime.now()
                self.allProcesses[ID_procc]["timeLONG"] = self.allProcesses[ID_procc]["timeSTART"] - self.allProcesses[ID_procc]["timeEND"]
                self.activeProcesses[ID_procc].terminate()
                logger.info("Succ stop process: %s", self.allProcesses[ID_procc])
            except Exception as ex:
                logger.error("Process stop crashed: %s", ex)
        logger.info("All Processes test: \n%s\n", self.allProcesses)
        logger.info("Active Processes test: \n%s\n", self.activeProcesses)
"""    
        for ID_procc in self.allProcesses.keys():
            logger.info(self.allProcesses)
            try:
                #logger.info("ProccID: {}:\nTime_Start: {}\nTime_Stop: {}\n Long_Time: {}\n Test_Status: {}\n\n".format(ID_procc, self.allProcesses["timeSTART"].strftime("%Y_%m_%d_%H_%M_%S"), self.allProcesses["timeEND"].strftime("%Y_%m_%d_%H_%M_%S"), self.allProcesses["timeLONG"].strftime("%Y_%m_%d_%H_%M_%S"), self.allProcesses["EndStatus"]))
            except Exception as ex:
                logger.error("Process stop crashed: %s", ex)
"""


def startDrive(QueStatus, id):
    try:
        if browser_watcher("/home/ttiimmoonn/pythonscripts/eltex/web_test/pytest-selenium/webdriver/chromedriver",
                           "/usr/bin/google-chrome-stable", True, "http://192.168.116.130"):
            QueStatus.put([id, "Succ."])
        else:
            QueStatus.put([id, "Fail."])
            return False
    except Exception as ex:
        logger.error("Process startDrive crashed: %s", ex)
        QueStatus.put(id)
        return False


def generalID():
    ls = list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
    random.shuffle(ls)
    ID = ''.join([random.choice(ls) for x in range(12)])
    return ID


log_path = "{}/log/{}".format(os.getcwd(), datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
os.makedirs(log_path)
log_file = log_path + "/log.log"
log = open("{}/log.log".format(log_path), "w+")
log.close()
logging.basicConfig(filename=log_file,
                    format=u'%(asctime)-8s %(levelname)-8s [%(module)s:%(lineno)d] %(message)-8s',
                    filemode='w', level=logging.INFO)

logger = logging.getLogger("tester")


test = MultProcess(2, True)
test.managerProcess()
test.stopProcess()