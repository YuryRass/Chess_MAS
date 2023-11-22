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
        super().__init__()
        self.name = name
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self):
        asyncio.run(self._run())

    async def _run(self):
        agent: Agent | None = None
        while True:
            if self.input_queue.empty():
                await asyncio.sleep(0.05)
                continue

            data: AgentMessage = self.input_queue.get()
            if data.message_type == MessageType.INITIATE_AGENT:
                if isinstance(data, InitiateAgentMessage):
                    agent: Agent | None = ChessPieceAgent(
                        data.board, data.piece_id
                    )

            if agent is None:
                raise NotImplementedError('No agent')

            output_data = await agent.step(data)
            self.output_queue.put(output_data)

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
        self.process = MyProcess(
            name=str(self._entity_id),
            input_queue=self.output_queue,
            output_queue=self.input_queue,
        )
        self.process.start()

    async def send_message(self, message: AgentMessage,) -> AgentMessage:
        self.output_queue.put(message)

        while self.input_queue.empty():
            await asyncio.sleep(0.05)

        return self.input_queue.get()
