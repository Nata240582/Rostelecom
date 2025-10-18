from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import Helpers
import time


class CookiePopup(Helpers):
    """
    Page Object для работы с popup при отключенных cookie
    """

    # Локаторы основного popup
    MAIN_POPUP = (By.CSS_SELECTOR, "[data-testid='cookie-disabled-popup'], .cookie-popup, .rt-cookie-popup")
    POPUP_TITLE = (By.CSS_SELECTOR, "[data-testid='cookie-popup-title'], .cookie-popup__title, .rt-cookie-popup__title")
    POPUP_DESCRIPTION = (By.CSS_SELECTOR,
                         "[data-testid='cookie-popup-description'], .cookie-popup__description, .rt-cookie-popup__description")
    COOKIE_LINK = (By.CSS_SELECTOR, "[data-testid='cookie-info-link'], .cookie-popup__link, .rt-cookie-popup__link")
    RETRY_BUTTON = (By.CSS_SELECTOR,
                    "[data-testid='cookie-retry-button'], .cookie-popup__retry, .rt-cookie-popup__retry")

    # Локаторы вспомогательного popup
    HELPER_POPUP = (By.CSS_SELECTOR, "[data-testid='cookie-helper-popup'], .cookie-helper-popup, .rt-cookie-helper")
    HELPER_TEXT = (By.CSS_SELECTOR, "[data-testid='cookie-helper-text'], .cookie-helper__text, .rt-cookie-helper__text")
    CLOSE_HELPER_BUTTON = (By.CSS_SELECTOR,
                           "[data-testid='close-helper-popup'], .cookie-helper__close, .rt-cookie-helper__close")

    # Локаторы формы авторизации (для проверки блокировки)
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BUTTON = (By.ID, "kc-login")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def disable_cookies_and_reload(self):
        """
        Отключает cookies и перезагружает страницу
        В реальном проекте это делается через настройки браузера
        """
        # Эмуляция отключения cookies через JavaScript
        self.driver.execute_script("""
            // Блокируем все cookies
            Object.defineProperty(document, 'cookie', {
                get: function() { return ''; },
                set: function() { return ''; }
            });

            // Эмулируем событие отключенных cookies
            window.dispatchEvent(new CustomEvent('cookiesDisabled'));
        """)

        # Перезагружаем страницу
        self.driver.refresh()
        time.sleep(3)

    def enable_cookies(self):
        """
        Включает cookies (для cleanup)
        """
        self.driver.execute_script("""
            // Восстанавливаем нормальную работу cookies
            delete Object.getOwnPropertyDescriptor(document, 'cookie');
        """)

    def is_main_popup_visible(self):
        """Проверяет видимость основного popup"""
        try:
            element = self.wait_for_element(self.MAIN_POPUP, timeout=5)
            return element.is_displayed()
        except:
            return False

    def is_helper_popup_visible(self):
        """Проверяет видимость вспомогательного popup"""
        try:
            element = self.wait_for_element(self.HELPER_POPUP, timeout=5)
            return element.is_displayed()
        except:
            return False

    def get_popup_title(self):
        """Получает заголовок основного popup"""
        try:
            return self.wait_for_element(self.POPUP_TITLE).text
        except:
            return ""

    def get_popup_description(self):
        """Получает описание основного popup"""
        try:
            return self.wait_for_element(self.POPUP_DESCRIPTION).text
        except:
            return ""

    def get_helper_text(self):
        """Получает текст вспомогательного popup"""
        try:
            return self.wait_for_element(self.HELPER_TEXT).text
        except:
            return ""

    def click_cookie_link(self):
        """Кликает на ссылку 'cookie' в основном popup"""
        self.wait_for_clickable(self.COOKIE_LINK).click()
        time.sleep(1)

    def click_retry_button(self):
        """Кликает на кнопку 'Повторить попытку'"""
        current_url = self.driver.current_url
        self.wait_for_clickable(self.RETRY_BUTTON).click()

        # Ждем начала перезагрузки
        time.sleep(2)
        return current_url

    def close_helper_popup(self):
        """Закрывает вспомогательный popup"""
        self.wait_for_clickable(self.CLOSE_HELPER_BUTTON).click()
        time.sleep(1)

    def is_auth_form_available(self):
        """
        Проверяет, доступна ли форма авторизации для взаимодействия
        """
        try:
            username_field = self.driver.find_element(*self.USERNAME_INPUT)
            return username_field.is_enabled() and not username_field.get_attribute("readonly")
        except:
            return False

    def is_auth_form_blocked(self):
        """
        Проверяет, заблокирована ли форма авторизации
        """
        return not self.is_auth_form_available()

    def click_outside_popup(self):
        """
        Кликает вне области popup для проверки поведения
        """
        # Кликаем в верхний левый угол (вне popup)
        self.driver.execute_script("window.scrollTo(0, 0);")
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.click()
        time.sleep(1)

    def check_popup_styling(self):
        """
        Проверяет визуальное оформление popup
        """
        try:
            main_popup = self.wait_for_element(self.MAIN_POPUP)

            # Проверяем основные CSS свойства
            styles = {
                'display': main_popup.value_of_css_property('display'),
                'visibility': main_popup.value_of_css_property('visibility'),
                'opacity': main_popup.value_of_css_property('opacity'),
                'z-index': main_popup.value_of_css_property('z-index')
            }

            return styles
        except:
            return {}

    def clear_cookies_and_reload(self):
        """
        Очищает cookies и перезагружает страницу (для теста с разрешенными cookie)
        """
        self.driver.delete_all_cookies()
        self.driver.refresh()
        time.sleep(3)

    def check_text_grammar(self, text):
        """
        Базовая проверка грамматики текста
        """
        common_mistakes = [
            'cookie',  # должно быть cookies в английском, но в русском может быть "cookie"
            'отключеные',  # должно быть отключены
            'авторизаци',  # должно быть авторизации
        ]

        issues = []
        for mistake in common_mistakes:
            if mistake in text.lower():
                issues.append(mistake)

        return issues

    def wait_for_page_reload(self, previous_url, timeout=10):
        """
        Ожидает перезагрузки страницы
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            current_url = self.driver.current_url
            if current_url != previous_url:
                return True
            time.sleep(0.5)
        return False