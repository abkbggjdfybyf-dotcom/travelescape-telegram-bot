import pytest
import sys
import os

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from keyboards import get_main_menu, get_contacts_menu, get_back_button, get_start_button


class TestKeyboards:
    def test_main_menu_keyboard(self):
        """Тест главного меню"""
        keyboard = get_main_menu()

        # Проверяем структуру клавиатуры
        assert hasattr(keyboard, 'keyboard')
        assert len(keyboard.keyboard) >= 1
        # Проверяем что есть нужные кнопки
        button_texts = []
        for row in keyboard.keyboard:
            for button in row:
                button_texts.append(button.text)

        assert '🎯 Подобрать тур' in button_texts
        assert '📞 Контакты' in button_texts

    def test_contacts_menu_keyboard(self):
        """Тест меню контактов"""
        keyboard = get_contacts_menu()

        assert hasattr(keyboard, 'keyboard')
        button_texts = []
        for row in keyboard.keyboard:
            for button in row:
                button_texts.append(button.text)

        assert '📍 Адрес' in button_texts
        assert '📞 Телефон' in button_texts
        assert '📧 Email' in button_texts
        assert '🔙 Назад' in button_texts

    def test_back_button(self):
        """Тест кнопки назад"""
        keyboard = get_back_button()

        assert hasattr(keyboard, 'keyboard')
        assert len(keyboard.keyboard) == 1
        assert keyboard.keyboard[0][0].text == '🔙 Назад'

    def test_start_button(self):
        """Тест кнопки в начало"""
        keyboard = get_start_button()

        assert hasattr(keyboard, 'keyboard')
        assert len(keyboard.keyboard) == 1
        assert keyboard.keyboard[0][0].text == '🏠 В начало'