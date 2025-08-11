from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

#chat template
chat_template = ChatPromptTemplate([
    ('system', 'You are a helpful customer support agent'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human', '{query}')
])

# with MessagePlaceholder langchain handles the merge automatically

chat_history = []

## load chat history (we can load it from database also)
with open('chat_history.txt') as f:
    chat_history.extend(f.readlines())
    
print(chat_history)

#create prompt
prompt = chat_template.invoke({'chat_history': chat_history, 'query': 'Where is my refund?'})

print(prompt)