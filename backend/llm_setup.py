from fastapi import FastAPI
from pydantic import BaseModel
from api_setup import llm_call

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/get-vid")
async def get_vid(request: PromptRequest):
    await llm_call(request.prompt)
    
    return {"received": request.prompt}
