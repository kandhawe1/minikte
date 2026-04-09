from fastapi import APIRouter
from fastapi import Request
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
async def execute_trade(request: Request, body: TradeRequest):

    # Get execution engine for this user
    accesscode = f"{body.code}_{body.broker}"

    engine = SessionManager.get_engine(accesscode)

    if not engine:
        return {
            "error": f"User {body.code} is not logged in with broker {body.broker}. Please call /login first."
        }

    # Execute portfolio trades
    results = await engine.execute_portfolio(body.orders)

    # Send notification
    notifier = Notifier()
    notifier.notify(results)

    return {
        "results": results
    }