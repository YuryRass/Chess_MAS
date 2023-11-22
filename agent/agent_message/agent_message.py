"""Пул сообщений, которыми может обмениваться агент с системой"""
from enum import IntEnum


class MessageType(IntEnum):
    """Типы сообщений агента"""
    INITIATE_AGENT = 1  # инициализация агента
    INITIATE_EPOCH = 2  # инициализация эпохи
    SUGGEST_MOVE = 3  # предложения по передвижнию фигур
    INACTIVITY = 4  # дезактивация агента
    ERROR = 5  # ошибка на стороне агента
    KILL = 6  # уничтожение процесса агента


class AgentMessage:
    """Сообщения агента"""
    def __init__(self, message_type: MessageType):
        self._message_type = message_type

    @property
    def message_type(self) -> MessageType:
        return self._message_type
