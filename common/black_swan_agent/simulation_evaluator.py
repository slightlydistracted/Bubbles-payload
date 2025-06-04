import json

def evaluate_simulation(results):
    '''
    Evaluate a set of simulation results and score performance.
    :param results: List of dictionaries containing performance metrics.
    :return: Summary dictionary with evaluation metrics.
    '''
    if not results:
        return {"error": "No simulation results provided."}

    total_return = sum(r.get("net_gain", 0) for r in results)
    total_trades = sum(r.get("trades", 0) for r in results)
    win_trades = sum(1 for r in results if r.get("net_gain", 0) > 0)
    loss_trades = sum(1 for r in results if r.get("net_gain", 0) <= 0)

    evaluation = {
        "total_simulations": len(results),
        "total_return": total_return,
        "average_return": total_return / len(results),
        "total_trades": total_trades,
        "win_rate": win_trades / len(results) if results else 0,
        "loss_rate": loss_trades / len(results) if results else 0,
        "win_loss_ratio": (win_trades / loss_trades) if loss_trades > 0 else float('inf'),
    }

    return evaluation
