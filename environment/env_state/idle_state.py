from environment.env_state.env_state import EnvState
from environment.env_state.state_enum import EnvStateType


class IdleEnvState(EnvState):
    """Состояние покоя вирт. системы"""
    def __init__(self):
        super().__init__(EnvStateType.IDLE)
