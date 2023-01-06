from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from cataloger_cli.managers.selenium_manager import SeleniumManager


class TestSeleniumManager:

    def test_01_basic_chrome_window(self):
        self.sm = SeleniumManager()
        self.sm.load_web('https://es.wikipedia.org/wiki/Web_scraping', seconds=2)
        page_title: WebElement = self.sm.chrome_driver.find_element(By.CLASS_NAME, 'mw-page-title-main')

        assert page_title
        assert page_title.text == 'Web scraping'

        self.sm.close()
