from langchain_community.document_loaders import PDFLoader,DirectoryLoader

loader = DirectoryLoader(
    path = 'folder/',
    glob='*.pdf',
    loader_cls=PDFLoader
)

docs = loader.load() # loads all the pdfs 

docs = loader.lazy_load() # loads the pdfs one by one

for document in docs:
    print(document.metadata)
