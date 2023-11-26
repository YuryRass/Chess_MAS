from agent.agent_message.agent_message import AgentMessage, MessageType
from data.board import Board


class InitiateEpochAgentMessage(AgentMessage):
    """Сообщение об инициализации эпохи агента"""
    def __init__(self, board: Board):
        super().__init__(MessageType.INITIATE_EPOCH)
        self._board = board

    @property
    def board(self) -> Board:
        return self._board
