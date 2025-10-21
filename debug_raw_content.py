#!/usr/bin/env python3
"""Debug script to check what's in raw_content field."""
import asyncio
import json
import os
from dotenv import load_dotenv

from browser_use import Agent
from browser_use.llm.openai.chat import ChatOpenAI
from browser_use.agent.views import AgentOutput

load_dotenv()


async def debug_raw_content():
	"""Check what gets stored in raw_content."""

	llm = ChatOpenAI(
		model="gpt-4o-mini",
		api_key=os.getenv("OPENAI_API_KEY"),
	)

	# Make a simple LLM call with structured output
	from browser_use.llm.messages import UserMessage

	messages = [UserMessage(content="Say hello in JSON format")]

	response = await llm.ainvoke(messages, output_format=AgentOutput)

	print(f"Response type: {type(response)}")
	print(f"Has raw_content: {hasattr(response, 'raw_content')}")

	if hasattr(response, 'raw_content'):
		print(f"raw_content is None: {response.raw_content is None}")
		if response.raw_content:
			print(f"raw_content type: {type(response.raw_content)}")
			print(f"raw_content preview: {response.raw_content[:300] if len(response.raw_content) > 300 else response.raw_content}")

			# Try parsing it
			try:
				parsed = json.loads(response.raw_content)
				print(f"✅ raw_content is valid JSON")
				print(f"   Keys: {list(parsed.keys())}")
			except:
				print(f"❌ raw_content is NOT valid JSON")

	print(f"\nCompletion type: {type(response.completion)}")
	print(f"Completion str(): {str(response.completion)[:300]}")

	# Check if str(completion) produces the bad format
	completion_str = str(response.completion)
	if "completion=AgentOutput" in completion_str or "AgentOutput(" in completion_str:
		print(f"❌ ERROR: str(completion) produces the transformed format!")
	else:
		print(f"✅ str(completion) looks okay")


if __name__ == "__main__":
	asyncio.run(debug_raw_content())
