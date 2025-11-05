import pytest
import sqlite3
import os
import sys
import os

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from database import Database


class TestDatabase:
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.db = Database('test_applications.db')

    def teardown_method(self):
        """Очистка после каждого теста"""
        if os.path.exists('test_applications.db'):
            os.remove('test_applications.db')

    def test_database_initialization(self):
        """Тест инициализации базы данных"""
        # Проверяем что таблица создалась
        conn = sqlite3.connect('test_applications.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='applications'")
        result = cursor.fetchone()

        assert result is not None
        assert result[0] == 'applications'
        conn.close()

    def test_save_application(self):
        """Тест сохранения заявки"""
        test_data = {
            'user_id': 12345,
            'username': 'test_user',
            'departure_city': 'Москва',
            'destination': 'Турция',
            'dates': '2024-08-15',
            'nights': '7',
            'travelers': '2 взрослых',
            'hotel_class': '5 звезд',
            'meals': 'Все включено',
            'wishes': 'Нет'
        }

        # Сохраняем заявку
        self.db.save_application(test_data)

        # Проверяем что заявка сохранилась
        applications = self.db.get_applications()
        assert len(applications) == 1
        assert applications[0][2] == 'test_user'  # username

    def test_application_count(self):
        """Тест подсчета заявок"""
        # Добавляем тестовую заявку
        test_data = {
            'user_id': 123,
            'username': 'test',
            'departure_city': 'test',
            'destination': 'test',
            'dates': 'test',
            'nights': 'test',
            'travelers': 'test',
            'hotel_class': 'test',
            'meals': 'test',
            'wishes': 'test'
        }
        self.db.save_application(test_data)

        # Проверяем количество через get_applications()
        applications = self.db.get_applications()
        assert len(applications) == 1