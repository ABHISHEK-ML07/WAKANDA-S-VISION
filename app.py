from fastapi import FastAPI
from pydantic import BaseModel
from tokenizer import count_tokens
from pricing import calculate_cost

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"

@app.post("/analyze")
def analyze_prompt(data: PromptRequest):
    input_tokens = count_tokens(data.prompt, data.model)

    # temporary assumption (later replace with real API response)
    output_tokens = int(input_tokens * 0.5)

    total_tokens = input_tokens + output_tokens
    cost = calculate_cost(data.model, input_tokens, output_tokens)

    return {
        "model": data.model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cost_usd": cost
    }