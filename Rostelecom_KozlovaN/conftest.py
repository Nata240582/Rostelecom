import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from config import Config


@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания драйвера"""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Явно указываем архитектуру
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def auth_page(driver):
    """Фикстура для страницы авторизации"""
    from pages.auth_page import AuthPage
    return AuthPage(driver).open()


@pytest.fixture
def registration_page(auth_page):
    """Фикстура для страницы регистрации"""
    return auth_page.go_to_registration()


@pytest.fixture
def recovery_page(auth_page):
    """Фикстура для страницы восстановления"""
    return auth_page.go_to_password_recovery()

@pytest.fixture
def cookie_popup(driver):
    """Фикстура для работы с cookie popup"""
    from pages.cookie_popup import CookiePopup
    page = CookiePopup(driver)
    driver.get(Config.BASE_URL)
    return page

@pytest.fixture
def cookie_popup_with_disabled_cookies(cookie_popup):
    """Фикстура с уже отключенными cookies"""
    cookie_popup.disable_cookies_and_reload()
    return cookie_popup

# Хуки для отчетности
def pytest_html_report_title(report):
    report.title = "Автотесты Ростелеком"


def pytest_configure(config):
    config._metadata = {
        "Проект": "Автотесты Ростелеком",
        "Тестировщик": "Automation QA"
    }