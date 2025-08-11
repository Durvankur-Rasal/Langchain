from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')

messages = [
    SystemMessage(content="You are a helpful AI assistant."),
    HumanMessage(content="What's your favorite color?"),
]

result = model.invoke(messages)
messages.append(AIMessage(content=result.content))

print(messages)