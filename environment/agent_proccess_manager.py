import asyncio
from agent.agent_message.initiate_agent import InitiateAgentMessage
from agent.agent_message.kill_agent import KillAgentMessage
from environment.i_agent_manager import IAgentManager
from data.board import Board
from environment.i_entity import IEntity
from agent.agent_message.agent_message import AgentMessage
from environment.process_entity import ProcessEntity


class AgentProcessManager(IAgentManager):
    """Менеджер агентов"""

    def __init__(self) -> None:
        self.process_entities: list[IEntity] = []

    async def create_chess_piece_agent(
        self,
        board: Board,
        piece_id: str,
        enabled: bool = True,
    ) -> None:
        """Создание шахм. фигуры-агента

        Args:
            board (Board): доска
            piece_id (str): ID фигуры
            enabled (bool, optional): активность. Defaults to True.
        """
        entity: IEntity = ProcessEntity(piece_id, enabled)
        await entity.send_message(
            InitiateAgentMessage(board, piece_id),
        )
        self.process_entities.append(entity)

    async def send_message(
        self,
        item: IEntity,
        message: AgentMessage,
    ) -> AgentMessage:
        return await item.send_message(message)

    async def send_all(
        self,
        message: AgentMessage,
    ) -> list[AgentMessage]:
        return await asyncio.gather(
            *[
                item.send_message(message)
                for item in self.process_entities
            ]
        )

    async def kill_all_agent(self) -> None:
        await self.send_all(KillAgentMessage())
