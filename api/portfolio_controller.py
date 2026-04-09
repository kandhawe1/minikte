from fastapi import APIRouter
from pydantic import BaseModel
from core.session_manager import SessionManager

routerportfolio = APIRouter()


class HoldingsRequest(BaseModel):
    code: str
    broker: str


@routerportfolio.post("/holdings")
async def get_holdings(request: HoldingsRequest):

    accesscode = f"{request.code}_{request.broker}"

    engine = SessionManager.get_engine(accesscode)

    if not engine:
        return {"error": "Session not found"}

    return {
        "code": request.code,
        "broker": request.broker,
        "holdings": engine.holdings
    }