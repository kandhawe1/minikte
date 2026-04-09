from fastapi import APIRouter
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from pydantic import BaseModel
from brokers.zerodha_adapter import ZerodhaAdapter
from brokers.fyers_adapter import FyersAdapter
from brokers.angelone_adapter import AngeloneAdapter
from brokers.groww_adapter import GrowwAdapter
from brokers.upstox_adapter import UpstoxAdapter
from brokers.fyers_adapter import FyersAdapter

from core.execution_engine import ExecutionEngine
from core.session_manager import SessionManager

routerlogin = APIRouter()

limiter = Limiter(key_func=get_remote_address)
# limiter = Limiter(key_func=lambda request: request.headers.get("X-User-Code"))

class LoginRequest(BaseModel):
    code: str
    broker: str
    connection_key: str


@routerlogin.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, body: LoginRequest):
    # Switch control
    match body.broker:

        case "zerodha":
            broker = ZerodhaAdapter()

        case "fyers":
            broker = FyersAdapter()

        case "angelone":
            broker = AngeloneAdapter()

        case "groww":
            broker = GrowwAdapter()

        case "upstox":
            broker = UpstoxAdapter()

        case _:
            return {"error": "Unsupported broker"}

    #broker = ZerodhaAdapter()
    accesscode = f"{body.code}_{body.broker}"

    # Create execution engine
    engine = ExecutionEngine(broker)

    # Load previous holdings
    engine.holdings = SessionManager.load_holdings(accesscode)

    # Register session
    SessionManager.create_session(accesscode, engine)

    return {
        "message": f"{body.code} logged in successfully"
    }