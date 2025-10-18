from selenium.webdriver.common.by import By
import time


class CookieUtils:
    """
    Утилиты для работы с cookies в браузере
    """

    def __init__(self, driver):
        self.driver = driver

    def block_all_cookies(self):
        """
        Блокирует все cookies через настройки браузера (эмуляция)
        """
        # В реальном проекте это делается через профиль браузера
        # Здесь эмулируем через JavaScript
        self.driver.execute_script("""
            // Эмуляция блокировки cookies
            window.cookiesBlocked = true;
            console.log('Cookies blocked for testing');
        """)

    def allow_all_cookies(self):
        """
        Разрешает все cookies
        """
        self.driver.execute_script("""
            // Эмуляция разрешения cookies
            window.cookiesBlocked = false;
            console.log('Cookies allowed for testing');
        """)

    def get_cookie_state(self):
        """
        Получает состояние cookies (для отладки)
        """
        return self.driver.execute_script("return window.cookiesBlocked || false;")

    def simulate_cookie_disabled_event(self):
        """
        Симулирует событие отключенных cookies
        """
        self.driver.execute_script("""
            // Создаем и dispatch событие отключенных cookies
            const event = new CustomEvent('cookiesDisabled', {
                detail: { reason: 'browser_settings' }
            });
            window.dispatchEvent(event);
        """)

    def check_cookie_popup_selectors(self):
        """
        Проверяет различные возможные селекторы для cookie popup
        """
        possible_selectors = [
            "[data-testid*='cookie']",
            "[class*='cookie']",
            ".cookie-popup",
            ".rt-cookie-popup",
            "#cookie-popup",
            "#cookieWarning",
            ".cookie-notification",
            ".cookie-banner"
        ]

        found_selectors = []
        for selector in possible_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    found_selectors.append(selector)
            except:
                continue

        return found_selectors