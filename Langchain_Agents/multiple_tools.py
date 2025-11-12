from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from dotenv import load_dotenv
from langchain.tools import tool


load_dotenv()

wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

@tool
def multiply(numbers: str)-> int:
    "multiply two numbers given as 'a,b'"
    a,b = map(int, numbers.split(","))
    return a*b

llm  = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0.2)

agent = initialize_agent(
    tools = [wiki,multiply],
    llm = llm,
    agent_type= AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True    
)

agent.invoke({"input": "Who is Elon Musk and what is 12 times 7?"})

