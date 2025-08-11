from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import os

load_dotenv()

hf_api_key = os.getenv("HF_API_KEY")

llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation",
    api_key=hf_api_key
)

model = ChatHuggingFace(llm=llm)

# 1st prompt -> detailed report
template1 = PromptTemplate(
    template='Write a detailed report on {topic}',
    input_variables=['topic']
)


template2 = PromptTemplate(
    template='Write a  5 line summary of the following text: /n {text}',
    input_variables=['text']
)

prompt1 = template1.invoke({'topic': 'Black Hole'})

result1 = model.invoke(prompt1)

print(result1)

prompt2 = template2.invoke({'text': result1})

result2 = model.invoke(prompt2)

print(result2)
