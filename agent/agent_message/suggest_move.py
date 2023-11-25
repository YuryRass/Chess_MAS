from agent.agent_message.agent_message import AgentMessage, MessageType
from data.move_suggestions import MoveSuggestion


class SuggestMoveAgentMessage(AgentMessage):
    """Сообщение о предложениях по ходам агента"""
    def __init__(self, move_suggestion: list[MoveSuggestion]):
        super().__init__(MessageType.SUGGEST_MOVE)
        self._move_suggestion = move_suggestion

    @property
    def move_suggestion(self) -> list[MoveSuggestion]:
        return self._move_suggestion
