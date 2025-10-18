from selenium.webdriver.common.by import By
from utils.helpers import Helpers
import time


class RegistrationPage(Helpers):
    # Локаторы формы регистрации
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    EMAIL_INPUT = (By.ID, "address")
    PASSWORD_INPUT = (By.ID, "password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "password-confirm")
    REGISTER_BUTTON = (By.NAME, "register")

    # Сообщения об ошибках
    FIRST_NAME_ERROR = (By.CSS_SELECTOR, "[data-error='firstName']")
    PASSWORD_ERROR = (By.CSS_SELECTOR, "[data-error='password']")
    CONFIRM_PASSWORD_ERROR = (By.CSS_SELECTOR, "[data-error='password-confirm']")

    # Попап существующей учетной записи
    EXISTING_ACCOUNT_POPUP = (By.CLASS_NAME, "card-modal__card")
    LOGIN_BUTTON_POPUP = (By.ID, "reg-err-reset-pass")
    RECOVER_BUTTON_POPUP = (By.ID, "reg-err-register")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def enter_personal_data(self, first_name, last_name):
        """Ввод персональных данных"""
        self.wait_for_element(self.FIRST_NAME_INPUT).clear()
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)

        self.wait_for_element(self.LAST_NAME_INPUT).clear()
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)

    def enter_credentials(self, email, password, confirm_password=None):
        """Ввод учетных данных"""
        if confirm_password is None:
            confirm_password = password

        self.wait_for_element(self.EMAIL_INPUT).clear()
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)

        self.wait_for_element(self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

        self.wait_for_element(self.CONFIRM_PASSWORD_INPUT).clear()
        self.driver.find_element(*self.CONFIRM_PASSWORD_INPUT).send_keys(confirm_password)

    def submit_registration(self):
        """Отправка формы регистрации"""
        self.wait_for_clickable(self.REGISTER_BUTTON).click()
        time.sleep(2)

    def get_first_name_error(self):
        """Получение ошибки имени"""
        try:
            return self.wait_for_element(self.FIRST_NAME_ERROR).text
        except:
            return ""

    def get_password_error(self):
        """Получение ошибки пароля"""
        try:
            return self.wait_for_element(self.PASSWORD_ERROR).text
        except:
            return ""

    def is_existing_account_popup_visible(self):
        """Проверка видимости попапа существующей учетной записи"""
        return self.element_exists(self.EXISTING_ACCOUNT_POPUP)