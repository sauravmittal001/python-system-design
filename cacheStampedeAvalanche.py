import threading, time, random
from collections import Counter

class SecureCache:
    def __init__(self):
        self.cache = {}
        self.db_hits = 0
        self.lock = threading.Lock()

    def get_data(self):
        if "key" in self.cache:
            print("Hey")
            return self.cache["key"]

        with self.lock:
            if "key" not in self.cache:
                # print(time.time())
                self.db_hits += 1
                time.sleep(1)
                self.cache["key"] = "data"
            # print(time.time())
            return self.cache["key"]

def mock_db():
    time.sleep(0.1)

db_hits, cache = 0, {}
def get_data():
    global db_hits
    if "key" not in cache:
        mock_db()
        db_hits += 1
        cache["key"] = "data"

sc = SecureCache()

threads = [threading.Thread(target=sc.get_data) for _ in range(20)]
for t in threads: t.start()
for t in threads: t.join()

print(f"STAMPEDE on db by {sc.db_hits} hits")

def invalidate(jitter=False):
    values = [100 + random.randint(-10, 10) if jitter else 0 for _ in range(1000)]
    val = max(Counter(values).values())
    return val

print(f"AVALANCHE: Max keys expiring at once: {invalidate(False)}")
print(f"AVALANCHE: Max keys expiring at once: {invalidate(True)}")
