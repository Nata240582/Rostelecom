import pytest
from config import Config


class TestRegistration:
    """Тесты 10-13: Регистрация нового пользователя"""

    @pytest.mark.positive
    def test_10_successful_registration_email(self, registration_page):
        """Тест-кейс 10: Успешная регистрация по email"""
        registration_page.enter_personal_data(Config.NEW_NAME, Config.NEW_LASTNAME)
        registration_page.enter_credentials(Config.NEW_EMAIL, Config.NEW_PASSWORD)
        registration_page.submit_registration()

        # Здесь должен быть ввод кода подтверждения
        # Проверка редиректа в ЛК
        assert registration_page.is_redirected_to_lk(), "Пользователь не зарегистрирован"

    def test_11_existing_email_registration(self, registration_page):
        """Тест-кейс 11: Регистрация с существующим email"""
        registration_page.enter_personal_data(Config.NEW_NAME, Config.NEW_LASTNAME)
        registration_page.enter_credentials(Config.TEST_EMAIL, Config.NEW_PASSWORD)
        registration_page.submit_registration()

        assert registration_page.is_existing_account_popup_visible(), "Не отображается попап существующей учетной записи"

    def test_12_name_validation(self, registration_page):
        """Тест-кейс 12: Проверка валидации поля 'Имя'"""
        registration_page.enter_personal_data("А", Config.NEW_LASTNAME)

        error_text = registration_page.get_first_name_error()
        assert "Необходимо заполнить поле кириллицей" in error_text
        assert "От 2 до 30 символов" in error_text

    def test_13_cyrillic_password_validation(self, registration_page):
        """Тест-кейс 13: Проверка валидации пароля с кириллицей"""
        registration_page.enter_credentials(Config.NEW_EMAIL, Config.CYRILLIC_PASSWORD)

        error_text = registration_page.get_password_error()
        assert "Пароль должен содержать только латинские буквы" in error_text