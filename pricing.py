MODEL_PRICING = {
    "gpt-4o-mini": {
        "input": 0.15 / 1_000_000,
        "output": 0.60 / 1_000_000
    },
    "gpt-3.5-turbo": {
        "input": 0.50 / 1_000_000,
        "output": 1.50 / 1_000_000
    }
}

def calculate_cost(model, input_tokens, output_tokens):
    pricing = MODEL_PRICING.get(model)
    if not pricing:
        return 0

    cost = (input_tokens * pricing["input"]) + (output_tokens * pricing["output"])
    return round(cost, 6)