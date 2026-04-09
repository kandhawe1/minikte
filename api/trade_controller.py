from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from models.trade_models import TradeRequest
from core.session_manager import SessionManager
from notifications.notifier import Notifier

routertrade = APIRouter()
limiter = Limiter(key_func=get_remote_address)
#limiter = Limiter(key_func=lambda request: request.headers.get("X-User-Code"))


@routertrade.post("/execute")
@limiter.limit("100/minute")
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