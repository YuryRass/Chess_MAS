from agent.agent_message.agent_message import AgentMessage, MessageType


class KillAgentMessage(AgentMessage):
    """Сообщение об уничтожении процесса-агента"""
    def __init__(self):
        super().__init__(MessageType.KILL)
