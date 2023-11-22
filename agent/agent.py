"""Базовый класс агента"""
from abc import ABC, abstractmethod

from agent.agent_message.agent_message import AgentMessage


class Agent(ABC):
    @abstractmethod
    async def step(self, message: AgentMessage) -> AgentMessage:
        pass
