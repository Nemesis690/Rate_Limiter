import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.last_refill = time.time()

    def allow_request(self):
        now = time.time()
        elapsed = now - self.last_refill
        refill = elapsed * self.refill_rate

        self.tokens = min(self.capacity, self.tokens + refill)
        self.last_refill = now

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
