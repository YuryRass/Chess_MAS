from environment.env_state.state_enum import EnvStateType


class EnvState:
    """Базовый класс состояний вирт. системы"""
    def __init__(self, state_type: EnvStateType):
        self._state_type = state_type

    @property
    def state_type(self) -> EnvStateType:
        return self._state_type
