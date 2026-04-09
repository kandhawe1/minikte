from fastapi import FastAPI
from api.trade_controller import routertrade
from api.login_controller import routerlogin

import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Kalpi - MiniTradeExecution Engine Running"}

app.include_router(routertrade)
app.include_router(routerlogin)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)