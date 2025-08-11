from langchain_openai import chat_models
from dotenv import load_dotenv

load_dotenv()

model = chat_models.ChatOpenAI(model='gpt-4', temperature=0.4, max_completion_tokens=10)

result =model.invoke('Hello, how are you?')
print(result.content)