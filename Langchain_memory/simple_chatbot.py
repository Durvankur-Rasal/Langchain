from langchain.chains import ConversationChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()



# Use Gemini 2.5 flash model
llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0.2)
memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

conversation.invoke({"input": "Hi, my name is Durv."})
conversation.invoke({"input": "What is my name?"})
