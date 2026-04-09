from fastapi import FastAPI
from pydantic import BaseModel

from tokenizer import get_token_importance, clean_tokens
from pricing import calculate_cost

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str
    model: str


def count_tokens(text):
    return len(clean_tokens(text))


@app.get("/")
def home():
    return {"message": "TokenScope API Running 🚀"}


@app.post("/analyze")
def analyze(req: PromptRequest):
    prompt = req.prompt

    input_tokens = count_tokens(prompt)
    output_tokens = 2
    total_tokens = input_tokens + output_tokens

    cost = calculate_cost(total_tokens, req.model)

    token_importance = get_token_importance(prompt)

    # 🔥 Filter LOW tokens
    filtered_tokens = {
        k: v for k, v in token_importance.items()
        if v["level"] != "LOW"
    }

    return {
        "model": req.model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cost_usd": cost,
        "token_importance": token_importance,
        "important_tokens_only": filtered_tokens
    }