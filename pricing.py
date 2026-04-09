def calculate_cost(tokens, model):
    # Simple pricing (you can upgrade later)
    price_per_1k_tokens = 0.0005

    cost = (tokens / 1000) * price_per_1k_tokens
    return round(cost, 6)