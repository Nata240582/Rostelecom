from selenium.webdriver.common.by import By
from utils.helpers import Helpers
import time


class AuthPage(Helpers):
    # Локаторы формы авторизации
    PHONE_TAB = (By.ID, "t-btn-tab-phone")
    EMAIL_TAB = (By.ID, "t-btn-tab-mail")
    LOGIN_TAB = (By.ID, "t-btn-tab-login")
    LS_TAB = (By.ID, "t-btn-tab-ls")

    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BUTTON = (By.ID, "kc-login")

    ERROR_MESSAGE = (By.ID, "form-error-message")
    FORGOT_PASSWORD_LINK = (By.ID, "forgot_password")
    REGISTER_LINK = (By.ID, "kc-register")

    # Элементы правого блока
    RIGHT_BLOCK = (By.CLASS_NAME, "card-container__content")
    SLOGAN = (By.CLASS_NAME, "what-is__title")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def open(self):
        """Открытие страницы авторизации"""
        self.driver.get("https://b2c.passport.rt.ru")
        self.wait_for_element(self.USERNAME_INPUT)
        return self

    def select_tab(self, tab_name):
        """Выбор таба авторизации"""
        tabs = {
            "phone": self.PHONE_TAB,
            "email": self.EMAIL_TAB,
            "login": self.LOGIN_TAB,
            "ls": self.LS_TAB
        }
        self.wait_for_clickable(tabs[tab_name]).click()

    def enter_credentials(self, username, password):
        """Ввод учетных данных"""
        self.wait_for_element(self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)

        self.wait_for_element(self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def submit(self):
        """Нажатие кнопки входа"""
        self.wait_for_clickable(self.SUBMIT_BUTTON).click()
        time.sleep(2)

    def get_current_tab(self):
        """Получение активного таба"""
        tabs = [self.PHONE_TAB, self.EMAIL_TAB, self.LOGIN_TAB, self.LS_TAB]
        for tab in tabs:
            try:
                element = self.driver.find_element(*tab)
                if "active" in element.get_attribute("class"):
                    return tab
            except:
                continue
        return None

    def get_error_message(self):
        """Получение сообщения об ошибке"""
        try:
            return self.wait_for_element(self.ERROR_MESSAGE).text
        except:
            return ""

    def go_to_registration(self):
        """Переход к регистрации"""
        self.wait_for_clickable(self.REGISTER_LINK).click()
        from pages.registration_page import RegistrationPage
        return RegistrationPage(self.driver)

    def go_to_password_recovery(self):
        """Переход к восстановлению пароля"""
        self.wait_for_clickable(self.FORGOT_PASSWORD_LINK).click()
        from pages.recovery_page import RecoveryPage
        return RecoveryPage(self.driver)

    def is_redirected_to_lk(self):
        """Проверка редиректа в ЛК"""
        return "account" in self.driver.current_url or "lk" in self.driver.current_url

    def check_page_structure(self):
        """Проверка структуры страницы"""
        elements = {
            "Левый блок": self.USERNAME_INPUT,
            "Правый блок": self.RIGHT_BLOCK,
            "Слоган": self.SLOGAN,
            "Таб телефон": self.PHONE_TAB,
            "Таб почта": self.EMAIL_TAB,
            "Таб логин": self.LOGIN_TAB,
            "Таб лицевой счет": self.LS_TAB
        }

        results = {}
        for name, locator in elements.items():
            results[name] = self.element_exists(locator)

        return results