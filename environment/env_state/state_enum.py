from enum import IntEnum


class EnvStateType(IntEnum):
    """Типы состояний системы"""
    IDLE = 1  # состояние покоя
    READY = 2  # вирт. среда готова
    RUNNING = 3  # вирт. среда запущена
    FINISH = 4  # вирт. среда завершена
