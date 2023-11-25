from agent.agent_message.agent_message import AgentMessage, MessageType
from data.board import Board


class InitiateAgentMessage(AgentMessage):
    """Сообщение об инициализации агента"""

    def __init__(self, board: Board, piece_id: str):
        super().__init__(MessageType.INITIATE_AGENT)
        self._board = board
        self._piece_id = piece_id

    @property
    def board(self) -> Board:
        return self._board

    @property
    def piece_id(self) -> str:
        return self._piece_id
