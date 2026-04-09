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


