import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class Helpers:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def wait_for_element(self, locator, timeout=15):
        """Ожидание элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=15):
        """Ожидание кликабельности элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def element_exists(self, locator):
        """Проверка существования элемента"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def get_element_text(self, locator):
        """Получение текста элемента"""
        try:
            return self.driver.find_element(*locator).text
        except NoSuchElementException:
            return ""

    def take_screenshot(self, name):
        """Создание скриншота"""
        self.driver.save_screenshot(f"screenshots/{name}.png")