from selenium.webdriver.common.by import By
from utils.helpers import Helpers
import time


class TempCodePage(Helpers):
    # Локаторы авторизации по временному коду
    PHONE_INPUT = (By.ID, "address")
    GET_CODE_BUTTON = (By.ID, "otp_get_code")
    CODE_INPUTS = [(By.ID, f"rt-code-{i}") for i in range(6)]

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def enter_phone(self, phone):
        """Ввод номера телефона"""
        self.wait_for_element(self.PHONE_INPUT).clear()
        self.driver.find_element(*self.PHONE_INPUT).send_keys(phone)

    def get_code(self):
        """Запрос кода"""
        self.wait_for_clickable(self.GET_CODE_BUTTON).click()
        time.sleep(2)

    def enter_code(self, code="123456"):
        """Ввод кода"""
        for i, locator in enumerate(self.CODE_INPUTS[:6]):
            try:
                element = self.wait_for_element(locator)
                element.clear()
                # Проверка маски ввода - пытаемся ввести не цифры
                test_chars = ["a", "B", "@", "!"]
                for char in test_chars:
                    element.send_keys(char)
                    value = element.get_attribute("value")
                    if char in value:
                        element.clear()  # Очищаем если что-то ввелось

                # Вводим цифру
                element.send_keys(code[i] if i < len(code) else "0")
            except:
                continue

    def is_code_input_numeric(self):
        """Проверка, что поля принимают только цифры"""
        test_locator = self.CODE_INPUTS[0]
        try:
            element = self.wait_for_element(test_locator)

            # Пытаемся ввести букву
            element.clear()
            element.send_keys("a")
            value = element.get_attribute("value")

            # Если значение пустое или не содержит букву - маска работает
            return "a" not in value and value == ""
        except:
            return False