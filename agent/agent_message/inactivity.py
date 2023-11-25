from agent.agent_message.agent_message import AgentMessage, MessageType


class InactivityAgentMessage(AgentMessage):
    """Сообщение о дезактивации агента"""
    def __init__(self, piece_id: str):
        super().__init__(MessageType.INACTIVITY)
        self._piece_id = piece_id

    @property
    def piece_id(self) -> str:
        return self._piece_id
