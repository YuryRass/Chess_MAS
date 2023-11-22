from enum import Enum


class CommandEnum(Enum):
    """Консольные команды"""
    INIT = 0  # инициализация
    STEP = 1  # текущий шаг
    STOP = 2  # остановка работы приложения
    AUTO = 3  # автомоделирование с финальным результатом
    NONE = 4  # нет такой команды


_mapped_commands = {
    "step": CommandEnum.STEP,
    "stop": CommandEnum.STOP,
    "auto": CommandEnum.AUTO,
}


def get_command(input_data: str) -> CommandEnum:
    return _mapped_commands.get(
        input_data.lower(),
        CommandEnum.NONE,
    )
