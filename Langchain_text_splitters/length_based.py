from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(
    separator = "",
    chunk_size = 10,
    chunk_overlap  = 5,
)

text = "This is a long string that needs to be split into smaller chunks of text."

splitter = text_splitter.split_text(text)

for chunk in splitter:
    print(chunk)
   