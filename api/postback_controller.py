from fastapi import APIRouter, Request
import json

routerpostback = APIRouter()

@routerpostback.post("/postback")
async def broker_postback(request: Request):

    try:

        data = await request.json()

        print("Received Broker Postback:")
        print(json.dumps(data, indent=2))

        # Example fields (varies by broker)
        order_id = data.get("order_id")
        status = data.get("status")

        # Process update

        # update database

        # update session manager

        # notify strategy engine

        return {
            "status": "received"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }