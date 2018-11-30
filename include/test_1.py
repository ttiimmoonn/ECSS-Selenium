from browser_driver_class import ECSS_webdribe
import logging

logger = logging.getLogger("logger")

def browser_watcher(pathwebdriver, pathgooglechrome, display, ip_serv_ssw):
    a = ECSS_webdribe(pathwebdriver, pathgooglechrome, display, ip_serv_ssw)
    return work(a)

def work(a):
    try:
        if a.author({"login": "admin", "passw": "password"}):
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
            for b in ["Call-центр", "Домены", "Консоль", "Управление услугами", "Профили алиасов", "Кластеры RestFS", "Документация", "Календарь"]:
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
    except Exception as ex:
        logger.error("[ work ]  Exception:\n [%s]", ex)
