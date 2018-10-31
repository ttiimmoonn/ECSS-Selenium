import re
import time
from datetime import datetime
import logging
import random
import sys
import os

from multiprocessing import Process, Queue
import datetime
from selenium import webdriver
import selenium.webdriver.chrome.service as service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display

#logger = logging.getLogger("logger")

FORMAT = '%(asctime)-15s %(levelname)-8s %(message)s'
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename="{}/log/{}".format(os.getcwd(), datetime.datetime.now().strftime("%d-%b-%Y-%I_%M%p")), format=u'%(asctime)-8s %(levelname)-8s [%(module)s:%(lineno)d] %(message)-8s', filemode='w', level=logging.INFO)
class ECSS_webdribe():

    def __init__(self, path_web_driver, path_chrome, status_display, serv_url, timer = {"short":2,"average":4,"long":10}):
        #Блок Display определяет будет ли создан виртуальный display для теста
        self.display = {"Status": status_display}
        if self.display["Status"] == True:
            self.display["Display"] = Display(visible=0, size=(1024, 768)).start()

        # Блок создает экземпляр driver
        self.serv_url = serv_url
        self.path_web_driver = path_web_driver
        self.path_chrome = path_chrome
        self.web_driver = service.Service(path_web_driver)
        self.web_driver.start()
        self.driver = webdriver.Remote(self.web_driver.service_url, {'chrome.binary': path_chrome})
        self.driver.get(self.serv_url)

        self.namepr = str

        self.time_1 = timer["short"]
        self.time_2 = timer["average"]
        self.time_3 = timer["long"]

        self.start_testTime = datetime
        self.end_testTime = datetime

    def close(self):
        self.end_testTime = datetime.datetime.now()
        try:
            logger.info("The driver is terminating...")
            time.sleep(self.time_3)
            self.driver.quit()
            if self.display["Status"] == True:
                logger.debug("The hidden display ends...")
                self.display["Display"].stop()
            time.sleep(self.time_1)
            logger.info("The driver is complete.")
            logger.info("Test start: [%s]", a.start_testTime)
            logger.info("Test end: [%s]", a.end_testTime)
            return True
        except Exception as ex:
            logger.error("Error close process:\n [%s]", ex)
            return False

    def check_objectText(self, search_object, should_there_be):
        """
        Функция проверяет находится или нет заданный текс на странице
        :param search_object: список объектов для проверки
        :param should_there_be: true - объект должен быть найден/false - объекта быть не должно
        :return: true - если утверждение верно и false - если ошибочно
        """
        try:
            logger.info("Begins the search for text objects: %s.", search_object)
            time.sleep(self.time_2)
            for object in search_object:
                logger.debug("Work with object: [%s]", object)
                objectID = self.driver.find_elements_by_xpath("//*[contains(text(), '{}')]".format(object))
                logger.debug("Text found in object: \n [%s]", objectID)
                if not objectID:
                    logger.debug("Error while searching for object: [%s]", object)
                    if should_there_be:
                        logger.error("The required object was not found: [%s]", object)
                        return False
                if not should_there_be:
                    logger.error("Found an object which should not be: [%s]", object)
                    return False
            logger.info("Everything in its place.")
            return True
        except Exception as ex:
            logger.error("Error check object Text:\n [%s]", ex)
            return False

    def applicationLaunch(self, name_applicat):
        """
        Запускает приложение на SSW
        :param name_applicat: строчное значение одного приложения
        :return: True в случаи упешного открытия приложения и False в случаи неудачи
        """
        logger.info("Launch application: [%s]", name_applicat)
        try:
            time.sleep(self.time_2)
            applic = self.driver.find_element_by_xpath("//*[.='{}']".format(name_applicat))
            logger.debug("Serch object application: [%s]", applic)
            applic.click()
        except Exception as ex:
            logger.error("Error starting application:\n [%s]", ex)
            return False

        time.sleep(self.time_1)

        try:
            expandApplic = self.driver.find_elements_by_class_name("x-tool-maximize")
            logger.debug("Expand object application: [%s]", expandApplic)
        except Exception as ex:
            logger.error("Expand object application:\n [%s]", ex)
            return False
        if len(expandApplic) != 0:
            while True:
                try:
                    i = random.randint(0, len(expandApplic) - 1)
                    logger.debug("Click object:\n [%s]", expandApplic[i])
                    expandApplic[i].click()
                    logger.debug("Click object.")
                    return True
                except Exception as ex:
                    logger.debug("Exceptions when expand applications:\n [%s]", ex)
        else:
            return False

    def applicationClose(self):
        logger.info("Start close application...")
        """
        Закрывает все приложения
        :return:
        """
        time.sleep(self.time_1)
        self.driver.refresh()
        time.sleep(self.time_2)
        countCloseAppl = 0
        try:
            closeElemenAppl = self.driver.find_elements_by_xpath('//*[@data-qtip="Закрыть"]')
            countAppl = len(closeElemenAppl)
        except Exception as ex:
            logger.error("No open application:\n [%s]", ex)
            return False
        while True:
            time.sleep(self.time_1)
            try:
                a = random.randint(0, len(closeElemenAppl) - 1)
                if closeElemenAppl[a].is_displayed():
                    closeElemenAppl[a].click()
                    countCloseAppl += 1
                    logger.debug("Close the window:\n [%s]\nAll window:\n [%s]\nNumber of closed applications:\n [%s]\nNumber of applications:\n [%s]" % (closeElemenAppl[a], closeElemenAppl, countCloseAppl, countAppl))
                    self.driver.closeElemenAppl[a].clear()
                else:
                    logger.debug("The selected application is under another: [%s]", closeElemenAppl[a])
            except Exception as ex:
                logger.debug("Exceptions when closing applications:\n [%s]", ex)
            if countAppl == countCloseAppl:
                logger.info("Close all the window.")
                return True
            elif countAppl < countCloseAppl:
                logger.error("Error counting the number of windows.")
                return False

    def author(self, auth_couple):
        self.start_testTime = datetime.datetime.now()
        """
        Проводит авторизацию на сервера SSW
        auth_couple - {"login":"ожидается логин", "passw":"ожидается пароль"}
        :return:Успешная авторизация - True/При ошибке - False
        """
        time.sleep(self.time_2)
        try:
            auth_form = self.driver.find_element_by_xpath("//td[contains(text(),'Авторизация ECSS-10')]")
            login = self.driver.find_element_by_name("login")
            login.send_keys(auth_couple["login"])
            time.sleep(self.time_1)
            passwd = self.driver.find_element_by_name("password")
            passwd.send_keys(auth_couple["passw"])
            time.sleep(self.time_1)
            enter = self.driver.find_element_by_class_name("x-btn-inner")
            enter.click()
            logger.info("Login successful.")

            time.sleep(self.time_1)
            return True
        except Exception as ex:
            logger.error("Login failed. Exception:\n [%s]", ex)
            return False

    def enterAction(self, position):
        """
        Совершает клик по указанной позиции
        :param position: словарь из позиции {"x":"ширина","y":"высота"}
        :return:
        """
        try:
            actions = ActionChains(self.driver)
            actions.move_by_offset(position["x"], position["y"]).perform()
        except Exception as ex:
            logger.error("Enter. Exception:\n [%s]", ex)
            return False


def browser_watcher(pathwebdriver, pathgooglechrome, ip_serv_ssw, name):
    a = ECSS_webdribe(pathwebdriver, pathgooglechrome, True, ip_serv_ssw)
    work(a)

def work(a):
    if a.author({"login":"admin", "passw":"password"}):
        pass
    else:
        a.close()
        return False
    if a.applicationClose():
        pass
    else:
        a.close()
        return False

    while True:
        for b in ["Call-центр", "Домены", "Консоль", "Управление услугами", "Профили алиасов", "Кластеры RestFS", "Документация", "Календарь", "MSR медиа регистраторы"]:
            if a.applicationLaunch(str(b)):
                pass
            else:
                a.close()
                return False


            if a.check_objectText([str(b)], True):
                pass
            else:
                a.close()
                return False

            if a.applicationClose():
                pass
            else:
                a.close()
                return False


if __name__ == "__main__":
    set_sessions = {}
    pathwebdriver = "/home/ttiimmoonn/pythonscripts/eltex/web_test/pytest-selenium/webdriver/chromedriver"
    ip_serv_ssw = "http://192.168.116.131"
    pathgooglechrome = "/usr/bin/google-chrome-stable"
    count_procc = 4
    for i in list(range(count_procc)):
        name = "browser_watcher_" + str(i)
        proc_selen = Process(target=browser_watcher, name="browser_watcher_" + str(i),
                             args=(pathwebdriver, pathgooglechrome, ip_serv_ssw, name,))
        set_sessions["browser_watcher_" + str(i)] = proc_selen
        proc_selen.start()
    print(set_sessions)
    proc_selen.join()




