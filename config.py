import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    MANAGER_CHAT_ID = os.getenv('MANAGER_CHAT_ID')  # ID менеджера для заявок
    
    # Контактная информация
    CONTACTS = {
        'address': '📍 Москва, ул. Путешественников, д. 42\n⏰ Режим работы: Пн-Пт с 9:00 до 19:00',
        'phone': '📞 +7 (495) 123-45-67\n⏰ Режим работы: Пн-Пт с 9:00 до 19:00',
        'email': '📧 info@travelescape.ru\n⏰ Режим работы: Пн-Пт с 9:00 до 19:00'
    }

    @classmethod
    def validate(cls):
        """Проверяет, что все необходимые переменные заданы."""
        required_vars = ['TELEGRAM_BOT_TOKEN']
        for var in required_vars:
            if not getattr(cls, var):
                raise ValueError(f"Не задана обязательная переменная окружения: {var}")
