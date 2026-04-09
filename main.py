from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from api.trade_controller import routertrade
from api.login_controller import routerlogin

import uvicorn

app = FastAPI()

# Create limiter
limiter = Limiter(key_func=get_remote_address)

# Attach to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SlowAPIMiddleware)

@app.get("/")
def home():
    return {"message": "Kalpi - MiniTradeExecution Engine Running"}

app.include_router(routertrade)
app.include_router(routerlogin)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)