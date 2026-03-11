from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

from LLM.prompts import EXPLANATION_PROMPT, DEBUG_PROMPT, ALGORITHM_PROMPT
from rag.retrieval_engine import RetrievalEngine
from rag.embeddings import embedding_function
from Utils.detect_language import detect_language

retrieval_engine = RetrievalEngine(
    persist_directory="./chroma_db",
    embedding_function=embedding_function
)
app = FastAPI(title="AI Coding Assistant Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi3"

retrieval_engine = RetrievalEngine(
    persist_directory="./chroma_db",
    embedding_function=embedding_function
)

class QueryRequest(BaseModel):
    question: str
    language: str | None = None
    code: str | None = None

class QueryResponse(BaseModel):
    language: str
    intent: str
    answer: str

def detect_intent(question: str) -> str:
    q = question.lower()
    if any(word in q for word in ["error", "exception", "bug", "not working", "fix"]):
        return "debug"
    if any(word in q for word in ["algorithm", "approach", "complexity", "optimize"]):
        return "algorithm"
    return "explanation"

async def call_ollama(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=response.text)
        return response.json().get("response", "")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):

    try:
        print("Received request:", request)

        if not request.question:
            raise HTTPException(status_code=400, detail="Question is required")

        language = request.language or detect_language(
            request.question,
            request.code
        )

        print("Detected language:", language)

        if language == "unknown":
            raise HTTPException(status_code=400, detail="Unable to detect language")

        intent = detect_intent(request.question)
        print("Detected intent:", intent)

        docs = retrieval_engine.retrieve(language, request.question)
        context = ""
        for i, doc in enumerate(docs):
            context += f"\n[Document {i+1}]\n{doc}\n"

        print("Retrieved context length:", len(context))

        if intent == "debug":
            prompt_template = DEBUG_PROMPT
        elif intent == "algorithm":
            prompt_template = ALGORITHM_PROMPT
        else:
            prompt_template = EXPLANATION_PROMPT

        prompt = prompt_template.format(
            language=language,
            query=request.question,
            context=context
        )

        print("Calling Ollama...")

        answer = await call_ollama(prompt)

        return QueryResponse(
            language=language,
            intent=intent,
            answer=answer
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))