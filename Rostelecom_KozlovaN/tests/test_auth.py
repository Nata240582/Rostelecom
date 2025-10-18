import pytest
from config import Config


class TestAuthentication:
    """Тесты 1-4: Стандартная авторизация"""

    @pytest.mark.positive
    def test_1_successful_phone_auth(self, auth_page):
        """Тест-кейс 1: Успешная авторизация по номеру телефона"""
        # Проверка активного таба
        current_tab = auth_page.get_current_tab()
        assert current_tab == auth_page.PHONE_TAB, "По умолчанию активен не таб 'Номер'"

        # Ввод учетных данных
        auth_page.enter_credentials(Config.TEST_PHONE, Config.TEST_PASSWORD)
        auth_page.submit()

        # Проверка редиректа
        assert auth_page.is_redirected_to_lk(), "Не произошел переход в личный кабинет"

    def test_2_wrong_password_auth(self, auth_page):
        """Тест-кейс 2: Авторизация с неверным паролем по номеру телефона"""
        auth_page.enter_credentials(Config.TEST_PHONE, Config.INVALID_PASSWORD)
        auth_page.submit()

        error_message = auth_page.get_error_message()

        assert "Неверный логин или пароль" in error_message
        assert not auth_page.is_redirected_to_lk(), "Произошло перенаправление при неверном пароле"

    def test_3_auto_tab_switch(self, auth_page):
        """Тест-кейс 3: Проверка автоматического переключения табов"""
        # Ввод email при активном табе "Номер"
        auth_page.enter_credentials(Config.TEST_EMAIL, "")

        # Проверка автоматического переключения
        current_tab = auth_page.get_current_tab()
        assert current_tab == auth_page.EMAIL_TAB, "Таб не переключился автоматически на 'Почта'"

    @pytest.mark.positive
    def test_4_successful_ls_auth(self, auth_page):
        """Тест-кейс 4: Успешная авторизация по лицевому счету"""
        auth_page.select_tab("ls")
        auth_page.enter_credentials(Config.TEST_LOGIN, Config.TEST_PASSWORD)
        auth_page.submit()

        assert auth_page.is_redirected_to_lk(), "Не произошло перенаправление в личный кабинет"