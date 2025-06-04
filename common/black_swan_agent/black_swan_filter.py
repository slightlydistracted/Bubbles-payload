
def is_black_swan_event(token_data, volatility_threshold=0.65, volume_spike_threshold=5.0):
    price_change = abs(token_data.get("percentChange24h", 0))
    volume_ratio = token_data.get("volume24h", 1) / max(token_data.get("avgVolume7d", 1), 1)
    
    if price_change >= volatility_threshold * 100 and volume_ratio >= volume_spike_threshold:
        return True
    return False

def flag_black_swans(tokens):
    flagged = []
    for token in tokens:
        if is_black_swan_event(token):
            flagged.append(token["token_address"])
    return flagged
