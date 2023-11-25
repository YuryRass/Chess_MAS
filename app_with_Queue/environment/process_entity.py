from agent.agent import Agent
from agent.agent_message.agent_message import AgentMessage, MessageType
import asyncio

from multiprocessing import Process, Queue
from agent.agent_message.initiate_agent import InitiateAgentMessage
from agent.chess_piece_agent import ChessPieceAgent

from environment.i_entity import IEntity


class MyProcess(Process):
    """Описание работы процесса"""

    def __init__(
        self,
        name: str,
        input_queue: Queue,
        output_queue: Queue,
    ):
        """
        Args:
            name (str): имя процесса
            input_queue (Queue): входная очередь сообщений
            output_queue (Queue): выходная очередь сообщений
        """
        super().__init__()
        self.name = name
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self):
        """Запуск процесса"""
        asyncio.run(self._run())

    async def _run(self):
        """Основная работа процесса"""

        agent: Agent | None = None
        # бесконечный цикл проверки очереди сообщений
        while True:
            if self.input_queue.empty():
                await asyncio.sleep(0.05)
                continue

            # как только входная очередь не пуста - вытаскиваем из нее данные
            data: AgentMessage = self.input_queue.get()

            # Инициализация шахматной фигуры - агента
            if data.message_type == MessageType.INITIATE_AGENT:
                if isinstance(data, InitiateAgentMessage):
                    agent: Agent | None = ChessPieceAgent(
                        data.board, data.piece_id
                    )

            if agent is None:
                raise NotImplementedError('No agent')

            output_data = await agent.step(data)
            self.output_queue.put(output_data)

            # выходим из цикла, убивая процесс
            if data.message_type == MessageType.KILL:
                break


class ProcessEntity(IEntity):

    """Сущность-процесс"""

    def __init__(
        self,
        entity_id: str,
        enabled: bool = True,
    ) -> None:
        super().__init__(entity_id, enabled)
        self.input_queue = Queue()
        self.output_queue = Queue()
        # !меняем местами очереди
        self.process = MyProcess(
            name=str(self._entity_id),
            input_queue=self.output_queue,
            output_queue=self.input_queue,
        )
        self.process.start()  # запуск процесса

    async def send_message(self, message: AgentMessage,) -> AgentMessage:
        """Отправка сообщения агенту через очередь"""

        self.output_queue.put(message)

        while self.input_queue.empty():
            await asyncio.sleep(0.05)

        return self.input_queue.get()
