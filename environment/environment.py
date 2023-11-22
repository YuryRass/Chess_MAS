from typing import Callable

from data.board import Board
from data.epoch_info import EpochInfo
from data.board_event import BoardEvent
from environment.env_state.env_state import EnvState


class Environment:
    """Виртуальная среда"""
    def __init__(
        self,
        board: Board,
        console_callback: Callable[[EnvState], None],
        agent_manager: None,
    ) -> None:
        self._board = board
        self._agent_manager = agent_manager
        self._console_callback = console_callback
        self._initial_board_state = board.copy()
        self._steps_without_progress = 0
        self._epoch_number = 0
        self._current_epoch_info: EpochInfo = EpochInfo(999)
        self._previous_epoch_info: EpochInfo = EpochInfo(999)
        self._is_run = True

    async def initialize(self) -> None:
        ...

    async def run(self) -> None:
        ...

    async def stop(self) -> None:
        ...

    async def _step(self) -> BoardEvent:
        ...

    async def step(self) -> None:
        ...
