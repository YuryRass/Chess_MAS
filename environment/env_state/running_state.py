from environment.env_state.env_state import EnvState
from environment.env_state.state_enum import EnvStateType
from data.board import Board


class RunningEnvState(EnvState):
    """Состояние заупска системы"""
    def __init__(self, board: Board):
        super().__init__(EnvStateType.RUNNING)
        self._board = board

    @property
    def board(self) -> Board:
        return self._board
