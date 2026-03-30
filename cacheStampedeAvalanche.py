import threading, time, random
from collections import Counter

### START --- CACHE AVALANCHE --- START ###

"""
Demo shows that invalidating with a jitter is always better: it avoids too many DB 
hits at  same instant. Spreading out using jitter flattens the spikes
"""

def invalidate(jitter=False):
    # random.randint takes a range of numbers both inclusive and randomly returns within range
    values = [100 + random.randint(-10, 10) if jitter else 0 for _ in range(1000)]
    # Counter is a collection function which takes an array and creates a frequency map
    val = max(Counter(values).values())
    return val

print(f"AVALANCHE: Max keys expiring at once: {invalidate(False)}")
print(f"AVALANCHE: Max keys expiring at once: {invalidate(True)}")

### END --- CACHE AVALANCHE --- END ###

### START --- CACHE STAMPEDE WITHOUT LOCKS --- START ###

"""
All threads miss cache and hit db
By the time the cache is set, all threads have already stampede the db
"""
def mock_db():
    time.sleep(0.1)

db_hits, cache = 0, {}
def get_data():
    global db_hits
    if "key" not in cache:
        mock_db()
        db_hits += 1
        cache["key"] = "data"

# create 20 thread objects but do not execute them
threads = [threading.Thread(target=get_data) for _ in range(20)]
# start all threads
for t in threads: t.start()
# wait for each thread to finish one-by-one
for t in threads: t.join()

print(f"STAMPEDE on db by {db_hits} hits")

### END --- CACHE STAMPEDE WITHOUT LOCKS --- END ###


### START --- CACHE STAMPEDE WITH SECURE LOCKS --- START ###
"""
1. Secure locks stops thread until prev thread retrieves value
2 In this demo each thread is spawned almost at the same instant which is why all the threads wait at lock statement
3. In real life threads are spawned at different times, so not every thread would acquire a lock; it will 
exit function from cache itself
4. Uncomment time.time() to understand how each thread behaves
5. Uncomment time.sleep() to add jitter to thread spawn to simulate real-life requests (not all at same time)
"""

class SecureCache:
    def __init__(self):
        self.cache = {}
        self.db_hits = 0
        self.lock = threading.Lock()

    def get_data(self):
        if "key" in self.cache:
            # print(f"Cache hit: {time.time()} (request thread doesn't acquire lock)")
            return self.cache["key"]

        with self.lock:
            if "key" not in self.cache:
                # print(f"DB hit: {time.time()}")
                self.db_hits += 1
                time.sleep(2)
                self.cache["key"] = "data"
            # else:
            #     print(f"Cache hit: {time.time()} (request thread acquires lock)")
            return self.cache["key"]

sc = SecureCache()

threads = [threading.Thread(target=sc.get_data) for _ in range(20)]
for t in threads:
    t.start()
    # time.sleep(random.uniform(0, 0.5)) # simulates real-life incoming requests at random times
for t in threads: t.join()

print(f"STAMPEDE on db by {sc.db_hits} hits")

### START --- CACHE STAMPEDE WITHOUT SECURE LOCKS --- START ###
