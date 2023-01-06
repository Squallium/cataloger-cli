import logging
import os
import sys
import time
from builtins import Exception

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


class SeleniumManager:
    DRIVER_CHROME = 'chrome'
    DRIVER_FIREFOX = 'firefox'

    def __init__(self, port=9224, driver=DRIVER_CHROME):
        super().__init__()

        self.__port = port
        self.__driver = driver

        self.__chrome_driver: WebDriver = None
        self.__firefox_driver: WebDriver = None
        self.__web_loaded = None

    @property
    def chrome_driver(self) -> WebDriver:
        if not self.__chrome_driver:
            # setup chrome driver
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", f'127.0.0.1:{self.__port}')
            if sys.platform == 'darwin':
                username = os.environ.get('USER', None)
                chrome_driver_path = f'/Users/{username}/Applications/ChromeDrive/chromedriver'
            elif sys.platform == 'linux':
                chrome_driver_path = "/snap/bin/chromium.chromedriver"
            else:
                logging.error('Platform not supported')
                sys.exit(1)

            if os.path.isfile(chrome_driver_path):
                self.__chrome_driver = webdriver.Chrome(chrome_driver_path, chrome_options=chrome_options)
            else:
                logging.error('chromedriver not found')
                sys.exit(1)

        return self.__chrome_driver

    @property
    def firefox_driver(self) -> WebDriver:
        raise NotImplementedError

    @property
    def driver(self) -> WebDriver:
        if self.__driver == 'chrome':
            return self.chrome_driver
        elif self.__driver == 'firefox':
            return self.firefox_driver
        else:
            raise Exception

    def load_web(self, web_url, seconds=0, reload=False):
        if not self.__web_loaded or self.__web_loaded != web_url or reload:
            self.driver.get(web_url)
            if seconds > 0:
                logging.info(f'Waiting {seconds} loading seconds')
                time.sleep(seconds)
            self.__web_loaded = web_url

    def close(self):
        self.driver.close()
