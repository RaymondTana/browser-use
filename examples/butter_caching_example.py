import os, asyncio
from dotenv import load_dotenv
from browser_use import Agent, ChatOpenAI

load_dotenv()

async def main():
    llm = ChatOpenAI(
        base_url="https://proxy.butter.dev/v1",
        default_headers={"Butter-Auth": f"Bearer {os.getenv('BUTTER_API_KEY')}"},
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o"       
    )
    
    task = "Use Google Translate: What is the English word for mantequilla?"
    agent = Agent(task=task, llm=llm, use_vision=False)
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())