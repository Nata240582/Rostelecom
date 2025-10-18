import pytest


class TestUIStructure:
    """Тест 14: Проверка структуры формы авторизации"""

    def test_14_auth_form_structure(self, auth_page):
        """Тест-кейс 14: Проверка отображения базовой структуры"""
        structure = auth_page.check_page_structure()

        # Проверка всех элементов
        for element_name, exists in structure.items():
            assert exists, f"Элемент '{element_name}' не найден"

        # Проверка активного таба
        current_tab = auth_page.get_current_tab()
        assert current_tab == auth_page.PHONE_TAB, "По умолчанию активен не таб 'Номер'"

        # Проверка правого блока
        assert "Ростелеком" in auth_page.get_element_text(auth_page.SLOGAN), "Не найден продуктовый слоган"