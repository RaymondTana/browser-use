from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from browser_use.llm.messages import (
	BaseMessage,
)

if TYPE_CHECKING:
	pass


class MessageHistory(BaseModel):
	"""History of messages - simple append-only list"""
	messages: list[BaseMessage] = Field(default_factory=list)
	model_config = ConfigDict(arbitrary_types_allowed=True)

	def get_messages(self) -> list[BaseMessage]:
		"""Get all messages"""
		return self.messages

	def add_message(self, message: BaseMessage) -> None:
		"""Append a message to history"""
		self.messages.append(message)


class MessageManagerState(BaseModel):
	"""Holds the state for MessageManager"""

	history: MessageHistory = Field(default_factory=MessageHistory)
	tool_id: int = 1

	model_config = ConfigDict(arbitrary_types_allowed=True)
