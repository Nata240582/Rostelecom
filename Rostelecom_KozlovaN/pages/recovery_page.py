from selenium.webdriver.common.by import By
from utils.helpers import Helpers
import time


class RecoveryPage(Helpers):
    # Локаторы формы восстановления
    USERNAME_INPUT = (By.ID, "username")
    CAPTCHA_INPUT = (By.ID, "captcha")
    CONTINUE_BUTTON = (By.ID, "reset")

    # Способы восстановления
    SMS_OPTION = (By.ID, "rt-code-0")
    EMAIL_OPTION = (By.ID, "rt-code-1")
    CONTINUE_RECOVERY_BUTTON = (By.ID, "reset-form-submit")

    # Форма ввода кода
    CODE_INPUTS = [(By.ID, f"rt-code-{i}") for i in range(6)]

    # Форма нового пароля
    NEW_PASSWORD_INPUT = (By.ID, "new-password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "confirm-password")
    SAVE_PASSWORD_BUTTON = (By.ID, "t-btn-reset-pass")

    # Ошибки
    PASSWORD_ERROR = (By.CSS_SELECTOR, "[data-error='new-password']")
    CONFIRM_PASSWORD_ERROR = (By.CSS_SELECTOR, "[data-error='confirm-password']")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def enter_username(self, username):
        """Ввод username для восстановления"""
        self.wait_for_element(self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)

    def enter_captcha(self, captcha_text="00000"):
        """Ввод капчи"""
        self.wait_for_element(self.CAPTCHA_INPUT).clear()
        self.driver.find_element(*self.CAPTCHA_INPUT).send_keys(captcha_text)

    def continue_recovery(self):
        """Продолжение восстановления"""
        self.wait_for_clickable(self.CONTINUE_BUTTON).click()
        time.sleep(2)

    def select_sms_recovery(self):
        """Выбор восстановления по SMS"""
        self.wait_for_clickable(self.SMS_OPTION).click()

    def enter_recovery_code(self, code="123456"):
        """Ввод кода восстановления"""
        for i, locator in enumerate(self.CODE_INPUTS[:6]):
            try:
                element = self.wait_for_element(locator)
                element.clear()
                element.send_keys(code[i] if i < len(code) else "0")
            except:
                continue

    def enter_new_password(self, password, confirm_password=None):
        """Ввод нового пароля"""
        if confirm_password is None:
            confirm_password = password

        self.wait_for_element(self.NEW_PASSWORD_INPUT).clear()
        self.driver.find_element(*self.NEW_PASSWORD_INPUT).send_keys(password)

        self.wait_for_element(self.CONFIRM_PASSWORD_INPUT).clear()
        self.driver.find_element(*self.CONFIRM_PASSWORD_INPUT).send_keys(confirm_password)

    def save_new_password(self):
        """Сохранение нового пароля"""
        self.wait_for_clickable(self.SAVE_PASSWORD_BUTTON).click()
        time.sleep(2)

    def get_password_error(self):
        """Получение ошибки пароля"""
        try:
            return self.wait_for_element(self.PASSWORD_ERROR).text
        except:
            return ""