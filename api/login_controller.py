from fastapi import APIRouter
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


class LoginRequest(BaseModel):
    code: str
    broker: str
    connection_key: str


@routerlogin.post("/login")
async def login(request: LoginRequest):
    # Switch control
    match request.broker:

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
    accesscode = f"{request.code}_{request.broker}"

    # Create execution engine
    engine = ExecutionEngine(broker)

    # Load previous holdings
    engine.holdings = SessionManager.load_holdings(accesscode)

    # Register session
    SessionManager.create_session(accesscode, engine)

    return {
        "message": f"{request.code} logged in successfully"
    }