from abc import ABC, abstractmethod

from agent.agent_message.agent_message import AgentMessage


class IEntity(ABC):
    """Интерефейс сущности-процесса"""

    def __init__(
            self,
            entity_id: str,
            enabled: bool = True,
    ) -> None:
        """
        Args:
            entity_id (str): ID сущости
            enabled (bool, optional): активация сущности. Defaults to True.
        """
        self._entity_id = entity_id
        self._enabled = enabled

    @property
    def entity_id(self) -> str:
        return self._entity_id

    @property
    def enabled(self) -> bool:
        return self._enabled

    @abstractmethod
    async def send_message(self, message: AgentMessage,) -> AgentMessage:
        pass
