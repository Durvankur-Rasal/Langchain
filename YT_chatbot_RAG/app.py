from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Allow CORS for all origins (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

class VideoRequest(BaseModel):
    video_id: str
    question: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process_video")
async def process_video(request: VideoRequest):

    try:
        ytt_api = YouTubeTranscriptApi()
        fetched = ytt_api.fetch(request.video_id, languages=["en","hi"])
        raw_transcript = fetched.to_raw_data()
        transcript = " ".join(entry["text"] for entry in raw_transcript)
    except TranscriptsDisabled:
        return {"answer": "No captions available for this video."}
    except NoTranscriptFound:
        return {"answer": "No transcript found in the requested language."}
    except VideoUnavailable:
        return {"answer": "The video is unavailable."}
    except Exception as e:
        return {"answer": f"An unexpected error occurred: {str(e)}"}

    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150)
    chunks = splitter.create_documents([transcript])

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_documents(chunks, embedding=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    retrieved_docs = retriever.invoke(request.question)
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

    prompt = PromptTemplate(
        template="""
        You are a helpful assistant.
        Answer ONLY from the provided transcript context.
        If the context is insufficient, just say you don't know.

        {context}
        Question: {question}
        """,
        input_variables=["context", "question"]
    )

    llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', temperature=0.2)
    final_prompt = prompt.invoke({"context": context_text, "question": request.question})
    answer = llm.invoke(final_prompt)

    return {"answer": answer.content}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
