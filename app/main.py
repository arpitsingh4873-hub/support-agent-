from fastapi import FastAPI,UploadFile, File
import shutil
from dotenv import load_dotenv
from app.memory import get_history,add_to_history,format_history
from langchain_openai import ChatOpenAI
from app.ingest import ingest_document,search_documents
import os
load_dotenv()
app = FastAPI()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
@app.get("/")
def home():
    return {"message":"Support Agent is running"}

@app.get("/test-key")
def test_key():
    if GROQ_API_KEY:
        return {"status":"API key loaded"}
    return {"status":"API key missing"}

@app.get("/ingest-test")
def ingest_test():
    result = ingest_document("docs/sample.txt")
    return {"result": result}

@app.get("/test-llm")
def test_llm():
    llm = ChatOpenAI(
        api_key= GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
        model = "llama-3.1-8b-instant"
    )
    response = llm.invoke("Say hello in one sentence.")
    return {"response": response.content}

@app.get("/search")
def search(query:str):
    results = search_documents(query)
    return {"results":results}

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    file_path = f"docs/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    result = ingest_document(file_path)
    return {"message": f"File uploaded and ingested", "details": result}

@app.get("/chat")
def chat(question:str, session_id:str = "default"):
    context_chunks = search_documents(question)
    context = "\n".join(context_chunks)

    if not context.strip():
        return {
            "answer": "I don't have enough information to answer this. Escalating to a human agent.",
            "escalate": True,
            "session_id": session_id
        }

    history = format_history(session_id)

    prompt = f"""You are a customer support agent. You ONLY answer using the context below.
    If the answer is NOT found in the context, you MUST reply with exactly one word: ESCALATE

context:
{context}

Conversation so far:
{history}

Question: {question}
Answer:"""
    
    llm = ChatOpenAI(
        api_key= GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
        model = "llama-3.1-8b-instant"
    )
    response = llm.invoke(prompt)
    answer = response.content

    if "ESCALATE" in answer:
        return {
            "answer": "This requires human assistance. Connecting you to an agent.",
            "escalate": True,
            "session_id": session_id
        }
    
    add_to_history(session_id, question, answer)
    return {"answer": answer ,"escalate": False, "session_id": session_id}