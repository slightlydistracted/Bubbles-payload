
import json
from value_decoder import decode_token_value
from mutation_engine import apply_mutation_strategies

def extract_alpha_signals(token_data, market_context, mutation_memory):
    """
    Analyze token data and market context to extract actionable alpha signals.
    """
    decoded_value = decode_token_value(token_data, market_context)
    mutation_recommendations = apply_mutation_strategies(token_data, mutation_memory)

    return {
        "decoded_value": decoded_value,
        "mutation_recommendations": mutation_recommendations
    }
