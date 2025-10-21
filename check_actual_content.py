#!/usr/bin/env python3
"""Check what's actually stored in message history after a few steps."""
import asyncio
import json
import os
from dotenv import load_dotenv

from browser_use import Agent
from browser_use.llm.openai.chat import ChatOpenAI

load_dotenv()


async def check_stored_content():
	"""Check what's actually in the message history."""

	llm = ChatOpenAI(
		model="gpt-4o-mini",
		api_key=os.getenv("OPENAI_API_KEY"),
	)

	task = "Navigate to google.com"
	agent = Agent(
		task=task,
		llm=llm,
		use_vision=False,
	)

	# Run 2 steps
	await agent.step()
	await agent.step()

	messages = agent._message_manager.state.history.get_messages()

	print(f"\n📊 Checking message content after 2 steps:")
	print(f"Total messages: {len(messages)}\n")
	print("="*80)

	for i, msg in enumerate(messages):
		msg_type = type(msg).__name__
		print(f"\n[{i+1}] {msg_type}")
		print("-" * 80)

		if hasattr(msg, 'content'):
			content = msg.content

			# Check for the bad pattern
			if isinstance(content, str):
				if "completion=AgentOutput" in content:
					print("❌ FOUND BAD PATTERN: 'completion=AgentOutput' in content!")
					print(f"Content preview: {content[:300]}...")
				elif "AgentOutput(" in content:
					print("❌ FOUND BAD PATTERN: 'AgentOutput(' in content!")
					print(f"Content preview: {content[:300]}...")
				else:
					# Check if it's JSON
					try:
						parsed = json.loads(content)
						print(f"✅ Valid JSON content")
						print(f"Keys: {list(parsed.keys()) if isinstance(parsed, dict) else 'not a dict'}")

						# Check structure
						if isinstance(parsed, dict) and "thinking" in parsed:
							print(f"✅ Has 'thinking' field (raw JSON format)")
						if isinstance(parsed, dict) and "action" in parsed:
							print(f"✅ Has 'action' field (raw JSON format)")

					except json.JSONDecodeError:
						# Plain text
						preview = content[:200] if len(content) > 200 else content
						print(f"Plain text content: {preview}")
			else:
				# List content (multimodal)
				print(f"Multimodal content with {len(content)} parts")

	print("\n" + "="*80)
	print("\n🔍 Summary:")

	assistant_messages = [m for m in messages if type(m).__name__ == 'AssistantMessage']
	print(f"- Total AssistantMessages: {len(assistant_messages)}")

	bad_count = 0
	for msg in assistant_messages:
		if isinstance(msg.content, str):
			if "completion=AgentOutput" in msg.content or "AgentOutput(" in msg.content:
				bad_count += 1

	if bad_count > 0:
		print(f"❌ {bad_count} AssistantMessage(s) contain the bad pattern!")
	else:
		print(f"✅ All AssistantMessages contain raw JSON (no bad patterns)")


if __name__ == "__main__":
	asyncio.run(check_stored_content())
