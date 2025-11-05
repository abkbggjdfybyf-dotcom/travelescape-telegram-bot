import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    ConversationHandler, filters, ContextTypes
)

from config import Config
from keyboards import *
from states import ApplicationStates, APPLICATION_FLOW
from database import Database

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация базы данных
db = Database()

class TravelEscapeBot:
    def __init__(self, token):
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        # Обработчик диалога заявки
        conv_handler = ConversationHandler(
            entry_points=[MessageHandler(filters.Regex('^🎯 Подобрать тур$'), self.start_application)],
            states={
                ApplicationStates.DEPARTURE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_departure)
                ],
                ApplicationStates.DESTINATION: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_destination)
                ],
                ApplicationStates.DATES: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_dates)
                ],
                ApplicationStates.NIGHTS: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_nights)
                ],
                ApplicationStates.TRAVELERS: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_travelers)
                ],
                ApplicationStates.HOTEL_CLASS: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_hotel_class)
                ],
                ApplicationStates.MEALS: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_meals)
                ],
                ApplicationStates.WISHES: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_wishes)
                ],
            },
            fallbacks=[
                MessageHandler(filters.Regex('^🔙 Назад$'), self.back_handler),
                MessageHandler(filters.Regex('^🏠 В начало$'), self.cancel),
                CommandHandler('start', self.cancel),
                CommandHandler('cancel', self.cancel)
            ],
            allow_reentry=True
        )

        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(filters.Regex('^📞 Контакты$'), self.show_contacts))
        self.application.add_handler(MessageHandler(filters.Regex('^📍 Адрес$'), self.show_address))
        self.application.add_handler(MessageHandler(filters.Regex('^📞 Телефон$'), self.show_phone))
        self.application.add_handler(MessageHandler(filters.Regex('^📧 Email$'), self.show_email))
        self.application.add_handler(MessageHandler(filters.Regex('^🔙 Назад$'), self.back_to_main))
        self.application.add_handler(MessageHandler(filters.Regex('^🏠 В начало$'), self.start))
        self.application.add_handler(conv_handler)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Приветственное сообщение"""
        welcome_text = """
🌟 Добро пожаловать в TravelEscape! 🌟

Мы поможем вам найти идеальный тур для незабываемого отдыха!

Выберите опцию ниже:
        """
        await update.message.reply_text(
            welcome_text,
            reply_markup=get_main_menu()
        )
        return ConversationHandler.END

    async def show_contacts(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать меню контактов"""
        await update.message.reply_text(
            "📞 Контакты TravelEscape:\n\nВыберите что вас интересует:",
            reply_markup=get_contacts_menu()
        )

    async def show_address(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать адрес"""
        await update.message.reply_text(
            Config.CONTACTS['address'],
            reply_markup=get_contacts_menu()
        )

    async def show_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать телефон"""
        await update.message.reply_text(
            Config.CONTACTS['phone'],
            reply_markup=get_contacts_menu()
        )

    async def show_email(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать email"""
        await update.message.reply_text(
            Config.CONTACTS['email'],
            reply_markup=get_contacts_menu()
        )

    async def back_to_main(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Вернуться в главное меню"""
        return await self.start(update, context)

    # === ОБРАБОТЧИКИ ДЛЯ ЗАЯВКИ ===

    async def start_application(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало оформления заявки"""
        context.user_data['application'] = {}
        await update.message.reply_text(
            "🎯 Отлично! Давайте подберем для вас идеальный тур!\n\n"
            "Откуда планируете вылет? (город, страна):",
            reply_markup=get_back_button()
        )
        return ApplicationStates.DEPARTURE

    async def get_departure(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получить город вылета"""
        context.user_data['application']['departure_city'] = update.message.text
        await update.message.reply_text(
            "✈️ Куда хотите полететь? (страна, курорт, можно несколько направлений):",
            reply_markup=get_back_button()
        )
        return ApplicationStates.DESTINATION

    async def get_destination(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получить направление"""
        context.user_data['application']['destination'] = update.message.text
        await update.message.reply_text(
            "📅 Укажите желаемые даты вылета:",
            reply_markup=get_back_button()
        )
        return ApplicationStates.DATES

    async def get_dates(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получить даты"""
        context.user_data['application']['dates'] = update.message.text
        await update.message.reply_text(
            "🌙 На сколько ночей планируете поездку?",
            reply_markup=get_back_button()
        )
        return ApplicationStates.NIGHTS

    async def get_nights(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получить количество ночей"""
        context.user_data['application']['nights'] = update.message.text
        await update.message.reply_text(
            "👨‍👩‍👧‍👦 Сколько взрослых и детей? (если дети - укажите возраст):",
            reply_markup=get_back_button()
        )
        return ApplicationStates.TRAVELERS

    async def get_travelers(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получить информацию о путешественниках"""
        context.user_data['application']['travelers'] = update.message.text
        await update.message.reply_text(
            "⭐ Какой класс отеля предпочитаете? (количество звезд):",
            reply_markup=get_back_button()
        )
        return ApplicationStates.HOTEL_CLASS

    async def get_hotel_class(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получить класс отеля"""
        context.user_data['application']['hotel_class'] = update.message.text
        await update.message.reply_text(
            "🍽️ Какое питание предпочитаете? (завтрак, полупансион, все включено и т.д.):",
            reply_markup=get_back_button()
        )
        return ApplicationStates.MEALS

    async def get_meals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получить информацию о питании"""
        context.user_data['application']['meals'] = update.message.text
        await update.message.reply_text(
            "💫 Дополнительные пожелания (можно пропустить, отправив любое сообщение):",
            reply_markup=get_back_button()
        )
        return ApplicationStates.WISHES

    async def get_wishes(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получить дополнительные пожелания и завершить заявку"""
        context.user_data['application']['wishes'] = update.message.text
        context.user_data['application']['user_id'] = update.effective_user.id
        context.user_data['application']['username'] = update.effective_user.username or update.effective_user.first_name

        # Сохраняем заявку в базу данных
        db.save_application(context.user_data['application'])

        # Отправляем заявку менеджеру
        await self.send_application_to_manager(context.user_data['application'])

        await update.message.reply_text(
            "✅ Спасибо! Ваша заявка отправлена!\n\n"
            "Наш менеджер свяжется с вами в ближайшее время для уточнения деталей.",
            reply_markup=get_start_button()
        )
        
        # Очищаем данные
        context.user_data.clear()
        return ConversationHandler.END

    async def send_application_to_manager(self, application_data):
        """Отправка заявки менеджеру в Telegram"""
        application_text = f"""
🎯 НОВАЯ ЗАЯВКА НА ПОДБОР ТУРА

👤 Пользователь: @{application_data['username']} (ID: {application_data['user_id']})
✈️ Вылет из: {application_data['departure_city']}
🎯 Направление: {application_data['destination']}
📅 Даты: {application_data['dates']}
🌙 Ночей: {application_data['nights']}
👥 Путешественники: {application_data['travelers']}
⭐ Класс отеля: {application_data['hotel_class']}
🍽️ Питание: {application_data['meals']}
💫 Пожелания: {application_data.get('wishes', 'не указано')}
        """
        
        # Отправляем менеджеру
        if Config.MANAGER_CHAT_ID:
            await self.application.bot.send_message(
                chat_id=Config.MANAGER_CHAT_ID,
                text=application_text
            )

    async def back_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик кнопки Назад"""
        current_state = context.user_data.get('current_state')
        
        if not current_state:
            return await self.start(update, context)
            
        # Определяем предыдущее состояние
        if current_state in APPLICATION_FLOW:
            current_index = APPLICATION_FLOW.index(current_state)
            if current_index > 0:
                previous_state = APPLICATION_FLOW[current_index - 1]
                context.user_data['current_state'] = previous_state
                
                # Возвращаемся к предыдущему вопросу
                questions = {
                    ApplicationStates.DEPARTURE: "Откуда планируете вылет?",
                    ApplicationStates.DESTINATION: "Куда хотите полететь?",
                    ApplicationStates.DATES: "Укажите желаемые даты вылета:",
                    ApplicationStates.NIGHTS: "На сколько ночей планируете поездку?",
                    ApplicationStates.TRAVELERS: "Сколько взрослых и детей?",
                    ApplicationStates.HOTEL_CLASS: "Какой класс отеля предпочитаете?",
                    ApplicationStates.MEALS: "Какое питание предпочитаете?",
                    ApplicationStates.WISHES: "Дополнительные пожелания:"
                }
                
                await update.message.reply_text(
                    f"🔙 Возвращаемся к предыдущему вопросу:\n\n{questions[previous_state]}",
                    reply_markup=get_back_button()
                )
                return previous_state
        
        return await self.start(update, context)

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отмена диалога"""
        context.user_data.clear()
        await update.message.reply_text(
            "Диалог прерван.",
            reply_markup=get_main_menu()
        )
        return ConversationHandler.END

    def run(self):
        """Запуск бота"""
        Config.validate()
        logger.info("Бот TravelEscape запущен...")
        self.application.run_polling()

if __name__ == '__main__':
    bot = TravelEscapeBot(Config.TELEGRAM_BOT_TOKEN)
    bot.run()
