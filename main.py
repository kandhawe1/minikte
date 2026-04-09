from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler

from api.trade_controller import routertrade
from api.login_controller import routerlogin
from api.portfolio_controller import routerportfolio

import uvicorn

app = FastAPI()

# Create limiter
limiter = Limiter(key_func=get_remote_address)

# Attach to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Allow CORS
origins = ["*"]  # allow all origins for testing

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Kalpi - MiniTradeExecution Engine Running"}

app.include_router(routertrade)
app.include_router(routerlogin)
app.include_router(routerportfolio)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)