import pytest
import sys
import os

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import Config


class TestConfig:
    def test_config_contacts(self):
        """Тест контактной информации"""
        contacts = Config.CONTACTS

        assert 'address' in contacts
        assert 'phone' in contacts
        assert 'email' in contacts
        assert 'Москва' in contacts['address']
        assert '+7 (495)' in contacts['phone']
        assert 'travelescape.ru' in contacts['email']
        assert 'Режим работы' in contacts['address']

    def test_config_attributes(self):
        """Тест наличия атрибутов конфигурации"""
        # Проверяем что атрибуты существуют
        assert hasattr(Config, 'TELEGRAM_BOT_TOKEN')
        assert hasattr(Config, 'MANAGER_CHAT_ID')
        assert hasattr(Config, 'CONTACTS')