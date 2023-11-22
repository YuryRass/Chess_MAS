from environment.env_state.env_state import EnvState
from environment.env_state.state_enum import EnvStateType
from data.board import Board, BoardEvent


class ReadyEnvState(EnvState):
    """Сотсояние готовности системы"""
    def __init__(self, board: Board, new_events: list[BoardEvent],):
        """
        Args:
            board (Board): шахм. доска
            new_events (list[BoardEvent]): список из перемещений,
        которые происходили на доске.
        """
        super().__init__(EnvStateType.READY)
        self._board = board
        self._new_events = new_events

    @property
    def board(self) -> Board:
        return self._board

    @property
    def new_events(self) -> list[BoardEvent]:
        return self._new_events
