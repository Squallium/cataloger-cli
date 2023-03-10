import logging
import time
from builtins import Exception

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


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

            self.__chrome_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                                    options=chrome_options)

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
