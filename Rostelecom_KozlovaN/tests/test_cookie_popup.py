import pytest
import time
from config import Config


class TestCookiePopup:
    """Тесты 15-20: Проверка popup при отключенных cookie"""

    def test_15_main_popup_display_with_disabled_cookies(self, cookie_popup_with_disabled_cookies):
        """
        Тест-кейс 15: Отображение основного popup при отключенных cookie
        """
        popup = cookie_popup_with_disabled_cookies

        # 1. Проверяем отображение основного popup
        assert popup.is_main_popup_visible(), "Основной popup не отображается"

        # 2. Проверяем заголовок popup
        title = popup.get_popup_title()
        assert "Cookie отключены" in title, f"Неверный заголовок: {title}"

        # 3. Проверяем описание popup
        description = popup.get_popup_description()
        assert "Для авторизации необходимо предоставить доступ к файлам cookie" in description, \
            f"Неверное описание: {description}"

        # 4. Проверяем наличие кликабельной ссылки "cookie"
        assert popup.element_exists(popup.COOKIE_LINK), "Ссылка 'cookie' не найдена"

        # 5. Проверяем наличие кнопки "Повторить попытку"
        assert popup.element_exists(popup.RETRY_BUTTON), "Кнопка 'Повторить попытку' не найдена"
        retry_button = popup.driver.find_element(*popup.RETRY_BUTTON)
        assert retry_button.is_enabled(), "Кнопка 'Повторить попытку' не активна"

        # 6. Проверяем, что форма авторизации заблокирована
        assert popup.is_auth_form_blocked(), "Форма авторизации не заблокирована"

    def test_16_cookie_link_functionality(self, cookie_popup_with_disabled_cookies):
        """
        Тест-кейс 16: Функциональность кнопки "cookie" во вспомогательном тексте
        """
        popup = cookie_popup_with_disabled_cookies

        # Убеждаемся, что основной popup отображается
        assert popup.is_main_popup_visible(), "Основной popup не отображается"

        # 1. Кликаем на ссылку "cookie"
        popup.click_cookie_link()

        # 2. Проверяем, что открылся вспомогательный popup
        assert popup.is_helper_popup_visible(), "Вспомогательный popup не открылся"

        # 3. Проверяем пояснительный текст
        helper_text = popup.get_helper_text()
        expected_phrases = [
            "Файлы cookie необходимы",
            "безопасной аутентификации",
            "хранения ваших данных",
            "личный кабинет невозможен"
        ]

        for phrase in expected_phrases:
            assert phrase in helper_text, f"Фраза '{phrase}' не найдена в тексте: {helper_text}"

        # 4. Проверяем наличие кнопки закрытия
        assert popup.element_exists(popup.CLOSE_HELPER_BUTTON), "Кнопка закрытия не найдена"
        close_button = popup.driver.find_element(*popup.CLOSE_HELPER_BUTTON)
        assert close_button.is_displayed(), "Кнопка закрытия не отображается"

    def test_17_close_helper_popup(self, cookie_popup_with_disabled_cookies):
        """
        Тест-кейс 17: Закрытие вспомогательного popup
        """
        popup = cookie_popup_with_disabled_cookies

        # Открываем вспомогательный popup
        popup.click_cookie_link()
        assert popup.is_helper_popup_visible(), "Вспомогательный popup не открылся"

        # 1. Закрываем вспомогательный popup
        popup.close_helper_popup()

        # 2. Проверяем, что вспомогательный popup закрылся
        assert not popup.is_helper_popup_visible(), "Вспомогательный popup не закрылся"

        # 3. Проверяем, что основной popup остался видимым
        assert popup.is_main_popup_visible(), "Основной popup не остался видимым"

        # 4. Проверяем, что ссылка "cookie" снова доступна
        cookie_link = popup.driver.find_element(*popup.COOKIE_LINK)
        assert cookie_link.is_enabled(), "Ссылка 'cookie' не доступна после закрытия вспомогательного popup"

    def test_18_retry_button_functionality(self, cookie_popup_with_disabled_cookies):
        """
        Тест-кейс 18: Функциональность кнопки "Повторить попытку"
        """
        popup = cookie_popup_with_disabled_cookies

        # Запоминаем текущий URL
        current_url = popup.driver.current_url

        # 1. Нажимаем кнопку "Повторить попытку"
        previous_url = popup.click_retry_button()

        # 2. Проверяем, что страница начала перезагружаться
        # (URL может временно измениться или остаться тем же при перезагрузке)
        time.sleep(3)  # Даем время на перезагрузку

        # 3. Проверяем, что адресная строка осталась на том же домене
        assert "rt.ru" in popup.driver.current_url, "Домен изменился после нажатия кнопки"

        # 4. Проверяем, что popup снова отображается (т.к. cookies все еще отключены)
        # Ждем немного для появления popup после перезагрузки
        time.sleep(2)
        assert popup.is_main_popup_visible(), "Popup не отображается после перезагрузки"

    def test_19_behavior_with_enabled_cookies(self, cookie_popup):
        """
        Тест-кейс 19: Проверка поведения при разрешенных cookie
        """
        # 1. Очищаем cookies и перезагружаем страницу
        popup.clear_cookies_and_reload()

        # 2. Проверяем, что popup НЕ отображается
        assert not popup.is_main_popup_visible(), "Popup отображается при разрешенных cookie"

        # 3. Проверяем, что форма авторизации доступна
        assert popup.is_auth_form_available(), "Форма авторизации недоступна"

        # 4. Проверяем основные элементы формы авторизации
        assert popup.element_exists(popup.USERNAME_INPUT), "Поле ввода логина не найдено"
        assert popup.element_exists(popup.PASSWORD_INPUT), "Поле ввода пароля не найдено"
        assert popup.element_exists(popup.SUBMIT_BUTTON), "Кнопка входа не найдена"

    def test_20_popup_visual_and_ux_validation(self, cookie_popup_with_disabled_cookies):
        """
        Тест-кейс 20: Проверка визуального оформления, орфографии и удобства использования
        """
        popup = cookie_popup_with_disabled_cookies

        # 1. Проверяем визуальное оформление
        styles = popup.check_popup_styling()
        assert styles.get('display') == 'block' or styles.get('display') == 'flex', \
            f"Popup имеет неверное display свойство: {styles.get('display')}"
        assert int(styles.get('z-index', 0)) > 1000, "Popup имеет низкий z-index"

        # 2. Проверяем орфографию и грамматику текстов
        title = popup.get_popup_title()
        description = popup.get_popup_description()

        # Проверяем основные тексты на очевидные ошибки
        title_issues = popup.check_text_grammar(title)
        description_issues = popup.check_text_grammar(description)

        assert len(title_issues) == 0, f"Ошибки в заголовке: {title_issues}"
        assert len(description_issues) == 0, f"Ошибки в описании: {description_issues}"

        # 3. Проверяем анимацию (косвенно через CSS свойства)
        main_popup = popup.driver.find_element(*popup.MAIN_POPUP)
        transition = main_popup.value_of_css_property('transition')
        assert 'opacity' in transition or 'all' in transition or transition != 'none', \
            "Отсутствует плавная анимация"

        # 4. Проверяем поведение при клике вне popup
        # Запоминаем состояние popup до клика
        popup_visible_before = popup.is_main_popup_visible()

        # Кликаем вне popup
        popup.click_outside_popup()

        # Проверяем, что popup не закрылся
        popup_visible_after = popup.is_main_popup_visible()
        assert popup_visible_after == popup_visible_before, \
            "Popup закрылся при клике вне его границ"

        # 5. Проверяем, что форма авторизации все еще заблокирована
        assert popup.is_auth_form_blocked(), "Форма авторизации разблокирована после клика вне popup"

    def test_cookie_popup_integration(self, cookie_popup):
        """
        Интеграционный тест: полный сценарий работы с cookie popup
        """
        # Часть 1: Проверяем поведение при отключенных cookies
        cookie_popup.disable_cookies_and_reload()
        assert cookie_popup.is_main_popup_visible(), "Popup не показан при отключенных cookies"

        # Часть 2: Работа со вспомогательным popup
        cookie_popup.click_cookie_link()
        assert cookie_popup.is_helper_popup_visible(), "Вспомогательный popup не открылся"

        cookie_popup.close_helper_popup()
        assert not cookie_popup.is_helper_popup_visible(), "Вспомогательный popup не закрылся"

        # Часть 3: Проверяем кнопку повтора
        previous_url = cookie_popup.driver.current_url
        cookie_popup.click_retry_button()
        time.sleep(3)

        # Popup должен остаться, т.к. cookies все еще отключены
        assert cookie_popup.is_main_popup_visible(), "Popup исчез после перезагрузки"

        # Часть 4: Включаем cookies и проверяем, что popup исчезает
        cookie_popup.enable_cookies()
        cookie_popup.driver.refresh()
        time.sleep(3)

        # При включенных cookies popup не должен показываться
        assert not cookie_popup.is_main_popup_visible(), "Popup показывается при включенных cookies"
        assert cookie_popup.is_auth_form_available(), "Форма авторизации недоступна"