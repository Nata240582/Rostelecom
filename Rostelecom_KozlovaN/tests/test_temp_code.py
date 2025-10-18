import pytest
from config import Config


class TestTempCodeAuth:
    """Тесты 5-6: Авторизация по временному коду"""

    @pytest.mark.positive
    def test_5_successful_temp_code_auth(self, auth_page):
        """Тест-кейс 5: Успешная авторизация по временному коду"""
        from pages.temp_code_page import TempCodePage

        # Переход к авторизации по коду (нужно найти правильный элемент)
        temp_code_page = TempCodePage(auth_page.driver)

        # Ввод телефона и запрос кода
        temp_code_page.enter_phone(Config.TEST_PHONE)
        temp_code_page.get_code()

        # Ввод кода (в реальном тесте нужно получать из SMS)
        temp_code_page.enter_code("123456")

        # Проверка редиректа
        assert auth_page.is_redirected_to_lk(), "Пользователь не аутентифицирован"

    def test_6_code_input_mask(self, auth_page):
        """Тест-кейс 6: Проверка маски ввода для кода"""
        from pages.temp_code_page import TempCodePage

        temp_code_page = TempCodePage(auth_page.driver)

        # Проверка, что поля принимают только цифры
        assert temp_code_page.is_code_input_numeric(), "Поля кода принимают не только цифры"