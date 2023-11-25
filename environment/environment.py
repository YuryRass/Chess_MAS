from typing import Callable
import asyncio
import random

from agent.agent_message.initiate_epoch import InitiateEpochAgentMessage
from agent.agent_message.suggest_move import SuggestMoveAgentMessage
from data.board import Board
from data.epoch_info import EpochInfo
from data.board_event import BoardEvent
from data.move_suggestions import MoveSuggestion
from environment.env_state.env_state import EnvState
from environment.env_state.running_state import RunningEnvState
from environment.env_state.ready_state import ReadyEnvState
from environment.env_state.finish_state import FinishEnvState
from environment.i_agent_manager import IAgentManager


class Environment:
    """Виртуальная среда"""

    def __init__(
        self,
        board: Board,
        console_callback: Callable[[EnvState], None],
        agent_manager: IAgentManager,
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
        await asyncio.gather(
            *[
                self._agent_manager.create_chess_piece_agent(
                    self._board,
                    piece_id.id,
                )
                for piece_id in self._board.pieces
            ]
        )
        self._console_callback(RunningEnvState(self._board))

    async def run(self) -> None:
        while self._steps_without_progress < 300:
            if not self._is_run:
                break

            await self._step()
            if self._current_epoch_info.number_of_conflicts == 0:
                await self.stop()
                return

            if self._current_epoch_info < self._previous_epoch_info:
                self._steps_without_progress = 0
            else:
                self._steps_without_progress += 1

            self._previous_epoch_info = self._current_epoch_info

        if self._is_run:
            await self.stop()

    async def stop(self) -> None:
        await self._agent_manager.kill_all_agent()
        self._is_run = False
        self._console_callback(
            FinishEnvState(self._board.copy(), self._epoch_number)
        )

    async def _step(self) -> BoardEvent:
        self._epoch_number += 1

        responses = await self._agent_manager.send_all(
            InitiateEpochAgentMessage(self._board),
        )

        suggested_moves_from_each_agent = [
            e for e in responses
            if isinstance(e, SuggestMoveAgentMessage)
        ]

        suggested_moves: list[MoveSuggestion] = []
        for agent_suggestion in suggested_moves_from_each_agent:
            suggested_moves.extend(agent_suggestion.move_suggestion)

        suggested_moves.sort(key=lambda x: x.number_of_conflicts)

        if suggested_moves:
            move = random.choice(suggested_moves)
            result = self._board.apply(move)
            conflicts = self._board.get_conflicts()
            self._current_epoch_info = EpochInfo(len(conflicts))
            return result

    async def step(self) -> None:
        result = await self._step()
        self._console_callback(ReadyEnvState(self._board.copy(), [result]))
