"""Реализация агента с привязкой его к шахматной доске"""

from agent.agent import Agent
from agent.agent_message.agent_message import AgentMessage, MessageType
from agent.agent_message.error import ErrorAgentMessage
from agent.agent_message.inactivity import InactivityAgentMessage
from agent.agent_message.initiate_agent import InitiateAgentMessage
from agent.agent_message.initiate_epoch import InitiateEpochAgentMessage
from agent.agent_message.suggest_move import SuggestMoveAgentMessage
from data.board import Board
from data.move_suggestions import MoveSuggestion
from data.position import Position


class ChessPieceAgent(Agent):
    """Шахматная фигура - агент"""

    def __init__(self, board: Board, piece_id: str) -> None:
        super().__init__()
        self._board = board
        self._piece_id = piece_id

    async def step(self, message: AgentMessage) -> AgentMessage:
        """Этапы работы: инициализация агента, инициализации эпохи"""
        match message.message_type:
            case MessageType.INITIATE_AGENT:
                return self.init_agent(message)
            case MessageType.INITIATE_EPOCH:
                return self.initiate_epoch(message)
            case _:
                return InactivityAgentMessage(piece_id=self._piece_id)

    def init_agent(self, message: InitiateAgentMessage) -> AgentMessage:
        """Инициализация агента

        Args:
            message (InitiateAgentMessage): сообщение для инициализации агента

        Returns:
            AgentMessage: сообщение агента
        """
        self._board = message.board
        self._piece_id = message.piece_id
        return InactivityAgentMessage(piece_id=self._piece_id)

    def initiate_epoch(
        self, message: InitiateEpochAgentMessage
    ) -> AgentMessage:

        """Инициализация эпохи. Определяет новые ходы фигуры,
        минимизируя конфликтные ситуации

        Args:
            message (InitiateEpochAgentMessage):  искомая эпоха

        Returns:
            AgentMessage: ErrorAgentMessage | SuggestMoveAgentMessage
        """
        self._board = message.board
        piece = self._board.find_piece_by_id(self._piece_id)

        if piece is None:
            return ErrorAgentMessage(
                piece_id=self._piece_id,
                error="Can not find chess piece with this id",
            )

        conflicts = self._board.get_conflicts()

        # список возможных перемещений фигуры
        possible_moves: list[MoveSuggestion] = []

        if len(conflicts) == 0:
            return SuggestMoveAgentMessage(move_suggestion=[])

        # список возможных ходов для фигуры piece
        movable_positions: list[Position] = \
            self._board.get_movable_positions(piece)

        for new_position in movable_positions:
            new_board = self._board.copy()
            new_piece = new_board.find_piece_by_id(self._piece_id)

            # меняем положение фигуры и определяем кол-во новых конфликтов
            new_board.move(new_piece, new_position)
            new_conflicts = new_board.get_conflicts()

            if len(new_conflicts) <= len(conflicts):
                possible_moves.append(
                    MoveSuggestion(
                        piece_id=self._piece_id,
                        new_position=new_position,
                        number_of_conflicts=len(new_conflicts),
                    )
                )
        return SuggestMoveAgentMessage(move_suggestion=possible_moves)
