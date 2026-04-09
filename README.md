# minikte - TradeExecutionEngine

##Setup and run instructions

docker build -t minikte

docker images - to check image has been created successfully ( minikte )

docker run -p 8000:8000 minikte


##Architecture
Used Adapter Pattern meet requirement for broker adaptability with minimal change.
Created separate adapters file to easily handle the specific area.

Scenerio Handled <br/>
- Multiple Users Logins <br/>
- Multiple Vendor Supported <br/>
- Single User/Multiple Vendor Supported <br/>
- No negative while placing "SELL" order <br/>
- "REBALANCE" will check buy or sell accordingly<br/>

RateLimiter
- Only 5 login requests per minute per IP
- Max 100 trade calls per minute
- #For clientcode limiter = Limiter(key_func=lambda request: request.headers.get("X-User-Code"))

##Third-party open-source trading libraries used.
slowapi - For RateLimiting


##
<b>Supported Brokers</b>:- <br/>
Zerodha = "zerodha"<br/>
Fyers	= "fyers"<br/>
Angelone= "angelone"<br/>
Groww	= "groww"<br/>
Upstox	= "upstox"<br/>

<b>Supported Actions</b>:- <br/>
"BUY"<br/>
"SELL"<br/>
"REBALANCE"<br/>


/login

{
  "code": "apple",
  "broker": "zerodha",
  "connection_key": "abcdef"
}


/execute ( Trade )

{
  "code": "apple",
  "broker": "zerodha",
  "orders": [
    {"symbol": "RELIANCE", "quantity": 1, "action": "BUY"},
    {"symbol": "INFY", "quantity": 1, "action": "BUY"}
  ]
}