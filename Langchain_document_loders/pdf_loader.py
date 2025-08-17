from langchain_community.document_loaders import PDFLoader

loader = PDFLoader('cricket.pdf')

docs = loader.load()

print(type(docs))
print(len(docs))
print(docs[0].page_content)