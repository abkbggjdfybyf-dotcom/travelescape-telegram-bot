import pytest
import sys
import os

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from states import ApplicationStates


class TestBotFlow:
    def test_application_flow_states(self):
        """Тест последовательности состояний диалога"""
        from states import APPLICATION_FLOW

        # Проверяем что состояния идут в правильном порядке
        expected_flow = [
            ApplicationStates.DEPARTURE,
            ApplicationStates.DESTINATION,
            ApplicationStates.DATES,
            ApplicationStates.NIGHTS,
            ApplicationStates.TRAVELERS,
            ApplicationStates.HOTEL_CLASS,
            ApplicationStates.MEALS,
            ApplicationStates.WISHES
        ]

        assert APPLICATION_FLOW == expected_flow

    def test_states_values(self):
        """Тест значений состояний"""
        assert ApplicationStates.DEPARTURE == 1
        assert ApplicationStates.DESTINATION == 2
        assert ApplicationStates.DATES == 3
        assert ApplicationStates.NIGHTS == 4
        assert ApplicationStates.TRAVELERS == 5
        assert ApplicationStates.HOTEL_CLASS == 6
        assert ApplicationStates.MEALS == 7
        assert ApplicationStates.WISHES == 8