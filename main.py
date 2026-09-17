import asyncio
import os
import httpx

async def call_gemini(prompt: str) -> str:
    api_key = os.environ.get("GOOGLE_GEMINI_API_KEY")
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent"

    max_retries = 2
    async with httpx.AsyncClient() as client:
        for attempt in range(max_retries + 1):
            response = await client.post(
                url,
                params={"key": api_key},
                json={"contents": [{"parts": [{"text": prompt}]}]}
            )
            if response.status_code == 429 and attempt < max_retries:
                await asyncio.sleep(1)
                continue
            response.raise_for_status()
            data = response.json()
            print(data)
            return data["candidates"][0]["content"]["parts"][0]["text"]
from pydantic import BaseModel

class Record(BaseModel):
    title: str
    creator: str
    rating: int



from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/echo")
def echo(record: Record):
    return record

class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask")
async def ask(request: PromptRequest):
    answer = await call_gemini(request.prompt)
    return {"answer": answer}