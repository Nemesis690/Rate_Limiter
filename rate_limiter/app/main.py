from fastapi import FastAPI, HTTPException, Request
from app.limiter import TokenBucket

app = FastAPI()

# In-memory store: user_id → token bucket
buckets = {}

CAPACITY = 5
REFILL_RATE = 5 / 60  # 5 requests per minute

@app.post("/request")
def handle_request(request: Request):
    user_ip = request.client.host

    if user_ip not in buckets:
        buckets[user_ip] = TokenBucket(CAPACITY, REFILL_RATE)

    bucket = buckets[user_ip]

    if bucket.allow_request():
        return {"message": "Request allowed"}
    else:
        raise HTTPException(status_code=429, detail="Too many requests")
