from fastapi import APIRouter
from models.trade_models import TradeRequest
from core.session_manager import SessionManager
from notifications.notifier import Notifier

routertrade = APIRouter()


@routertrade.post("/execute")
async def execute_trade(request: TradeRequest):

    # Get execution engine for this user
    engine = SessionManager.get_engine(request.code)

    if not engine:
        return {
            "error": f"User {request.code} is not logged in. Please call /login first."
        }

    # Execute portfolio trades
    results = await engine.execute_portfolio(request.orders)

    # Send notification
    notifier = Notifier()
    notifier.notify(results)

    return {
        "results": results
    }