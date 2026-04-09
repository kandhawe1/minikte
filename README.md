# minikte - TradeExecutionEngine

##Setup and run instructions

docker build -t minikte

docker images - to check image has been created successfully ( minikte )

docker run -p 8000:8000 minikte


##Architecture
Used Adapter Pattern meet requirement for broker adaptability with minimal change.
Created separate adapters file to easily handle the specific area


##Third-party open-source trading libraries used.
slowapi - For RateLimiting


##
Supported Brokers:- <br/>
Zerodha = "zerodha"<br/>
Fyers	= "fyers"<br/>
Angelone= "angelone"<br/>
Groww	= "groww"<br/>
Upstox	= "upstox"<br/>



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