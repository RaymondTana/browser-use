from browser_use import Agent, Browser, ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

browser = Browser(
    use_cloud=True,  # Automatically provisions a cloud browser
)


agent = Agent(
    task="Find the number of stars of the browser-use repo",
    llm=ChatOpenAI(model="gpt-4.1"),
    browser=Browser(use_cloud=True),  # Uses Browser-Use cloud for the browser
)
agent.run_sync()