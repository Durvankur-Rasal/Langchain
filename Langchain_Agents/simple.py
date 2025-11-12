from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

@tool
def add(numbers: str)-> int:
    "Add two numbers given as 'a,b'"
    a,b = map(int, numbers.split(","))
    return a+b

llm  = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0.2)

agent = initialize_agent(
    tools=[add],
    llm = llm,
    agent_type= AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

agent.invoke({"input": "What is 34 plus 22?"})