from agent.agent_message.agent_message import AgentMessage, MessageType


class ErrorAgentMessage(AgentMessage):
    def __init__(self, piece_id: str, error: str):
        super().__init__(MessageType.ERROR)
        self._error = error
        self._piece_id = piece_id

    @property
    def error(self) -> str:
        return self._error

    @property
    def piece_id(self) -> str:
        return self._piece_id
