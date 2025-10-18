import pytest
from config import Config


class TestPasswordRecovery:
    """Тесты 7-9: Восстановление пароля"""

    @pytest.mark.positive
    def test_7_successful_password_recovery_sms(self, recovery_page):
        """Тест-кейс 7: Успешное восстановление пароля через SMS"""
        # Ввод данных для восстановления
        recovery_page.enter_username(Config.TEST_PHONE)
        recovery_page.enter_captcha("00000")
        recovery_page.continue_recovery()

        # Выбор способа восстановления
        recovery_page.select_sms_recovery()

        # Ввод кода (заглушка)
        recovery_page.enter_recovery_code("123456")

        # Ввод нового пароля
        recovery_page.enter_new_password(Config.NEW_PASSWORD)
        recovery_page.save_new_password()

        # Проверка редиректа на страницу авторизации
        assert "auth" in recovery_page.driver.current_url, "Пользователь не перенаправлен на страницу авторизации"

    def test_8_password_validation_recovery(self, recovery_page):
        """Тест-кейс 8: Проверка валидации нового пароля"""
        # Навигация до формы нового пароля (упрощенно)
        recovery_page.enter_new_password(Config.SHORT_PASSWORD)

        # Проверка ошибки
        error_text = recovery_page.get_password_error()
        assert "Длина пароля должна быть не менее 8 символов" in error_text

    def test_9_password_confirmation(self, recovery_page):
        """Тест-кейс 9: Проверка совпадения паролей"""
        recovery_page.enter_new_password(Config.NEW_PASSWORD, Config.INVALID_PASSWORD)
        recovery_page.save_new_password()

        error_text = recovery_page.get_password_error()
        assert "Пароли не совпадают" in error_text