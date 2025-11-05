from telegram import ReplyKeyboardMarkup

# Главное меню
def get_main_menu():
    return ReplyKeyboardMarkup([
        ['🎯 Подобрать тур', '📞 Контакты']
    ], resize_keyboard=True)

# Меню контактов
def get_contacts_menu():
    return ReplyKeyboardMarkup([
        ['📍 Адрес', '📞 Телефон'],
        ['📧 Email', '🔙 Назад']
    ], resize_keyboard=True)

# Кнопка назад
def get_back_button():
    return ReplyKeyboardMarkup([['🔙 Назад']], resize_keyboard=True)

# Кнопка в начало
def get_start_button():
    return ReplyKeyboardMarkup([['🏠 В начало']], resize_keyboard=True)
