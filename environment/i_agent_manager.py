from abc import ABC, abstractmethod

from data.board import Board
from environment.i_entity import IEntity
from agent.agent_message.agent_message import AgentMessage


class IAgentManager(ABC):

    """Базовый интерефейс менеджера агентов"""

    @abstractmethod
    async def create_chess_piece_agent(
        self,
        board: Board,
        piece_id: str,
        enabled: bool = True,
    ) -> None:
        pass

    @abstractmethod
    async def send_message(
        self,
        item: IEntity,
        message: AgentMessage,
    ) -> AgentMessage:
        pass

    @abstractmethod
    async def send_all(
        self,
        message: AgentMessage,
    ) -> list[AgentMessage]:
        pass

    @abstractmethod
    async def kill_all_agent(self) -> None:
        ...
