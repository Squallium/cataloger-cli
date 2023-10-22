import logging
import time
from builtins import Exception

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumManager:
    DRIVER_CHROME = 'chrome'
    DRIVER_FIREFOX = 'firefox'

    def __init__(self, port=9224, driver=DRIVER_CHROME):
        super().__init__()

        self.__port = port
        self.__driver = driver

        self.__chrome_driver: webdriver = None
        self.__firefox_driver: webdriver = None
        self.__web_loaded = None

    def chrome_driver(self) -> webdriver:
        if not self.__chrome_driver:
            chrome_options = ChromeOptions()
            chrome_options.add_experimental_option("debuggerAddress", f'127.0.0.1:{self.__port}')

            self.__chrome_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                                    options=chrome_options)

        return self.__chrome_driver

    def firefox_driver(self, profile_path='') -> webdriver:
        if not self.__firefox_driver:
            firefox_options = FirefoxOptions()
            # firefox_options.add_argument(f'--remote-debugging-port={self.__port}')
            # firefox_options.add_argument('--marionette-port 50550')
            # firefox_options.add_argument('--connect-existing')
            firefox_options.add_argument(f'-profile')
            firefox_options.add_argument(profile_path)

            self.__firefox_driver = webdriver.Firefox(options=firefox_options)

        return self.__firefox_driver

    @property
    def driver(self) -> webdriver:
        if self.__driver == 'chrome':
            return self.chrome_driver()
        elif self.__driver == 'firefox':
            return self.firefox_driver()
        else:
            raise Exception

    def load_web(self, web_url, seconds=0, reload=False):
        if not self.__web_loaded or self.__web_loaded != web_url or reload:
            self.driver.get(web_url)
            if seconds > 0:
                logging.info(f'Waiting {seconds} loading seconds')
                time.sleep(seconds)
            self.__web_loaded = web_url

    def scroll_to_the_end(self, loop=True, sleep_time=1):
        script = 'window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;'
        len_of_page = self.chrome_driver.execute_script(script)
        match = False
        while not match:
            last_count = len_of_page
            time.sleep(sleep_time)
            len_of_page = self.chrome_driver.execute_script(script)
            if last_count == len_of_page or loop:
                match = True

    def close(self):
        self.driver.close()
