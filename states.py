from telegram.ext import ConversationHandler

# Состояния для заявки
class ApplicationStates:
    DEPARTURE = 1
    DESTINATION = 2
    DATES = 3
    NIGHTS = 4
    TRAVELERS = 5
    HOTEL_CLASS = 6
    MEALS = 7
    WISHES = 8

# Список всех состояний для удобства
APPLICATION_FLOW = [
    ApplicationStates.DEPARTURE,
    ApplicationStates.DESTINATION, 
    ApplicationStates.DATES,
    ApplicationStates.NIGHTS,
    ApplicationStates.TRAVELERS,
    ApplicationStates.HOTEL_CLASS,
    ApplicationStates.MEALS,
    ApplicationStates.WISHES
]
