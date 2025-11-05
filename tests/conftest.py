import pytest
import sys
import os

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

@pytest.fixture
def test_database():
    """Фикстура для тестовой базы данных"""
    from database import Database
    db = Database('test_applications.db')
    yield db
    # Очистка после тестов
    if os.path.exists('test_applications.db'):
        os.remove('test_applications.db')

@pytest.fixture
def sample_application_data():
    """Фикстура с тестовыми данными заявки"""
    return {
        'user_id': 12345,
        'username': 'test_user',
        'departure_city': 'Москва',
        'destination': 'Турция, Анталия',
        'dates': '15-25 августа 2024',
        'nights': '10 ночей',
        'travelers': '2 взрослых, 1 ребенок 5 лет',
        'hotel_class': '5 звезд',
        'meals': 'Все включено',
        'wishes': 'Номер с видом на море'
    }