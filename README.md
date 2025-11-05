# 🏝️ TravelEscape Telegram Bot

Telegram бот для турагентства с автоматизированной системой подбора туров и полным циклом тестирования.

## 🚀 Быстрый старт

```bash
git clone https://github.com/abkbggjdfybyf-dotcom/travelescape-telegram-bot.git
cd travelescape-telegram-bot
pip install -r requirements.txt
cp .env.example .env
# Добавьте TELEGRAM_BOT_TOKEN в .env
python bot.py

🔍Тестирование
pytest tests/ -v
Результат: 9 тестов ✅ PASSED

📁 Структура проекта
tests/              # 9 автотестов
.github/workflows/  # CI/CD
bot.py             # Основной код
config.py          # Конфигурация
database.py        # SQLite база
requirements.txt   # Зависимости

💡 Функциональность
8-шаговая форма заявки на тур
Сохранение в SQLite базу
Умная навигация (назад/в начало)
Уведомления менеджеру

🛠️ Технологии
Python
python-telegram-bot
SQLite
Pytest
GitHub Actions
