import threading, time

sleep_time = 0.2

# with no locks: all execute in 0.2 seconds
def print_num(i):
    # do something
    time.sleep(sleep_time)
st = time.time()
threads = [threading.Thread(target=print_num, args=(i,)) for i in range(20)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Time taken with no lock: {round(time.time()-st, 1)} seconds")

# with mutex: one-by-one execution in 0.2*20 seconds
lock = threading.Lock()
def print_num2(i):
    with lock:
        # do something
        time.sleep(sleep_time)
st = time.time()
threads = [threading.Thread(target=print_num2, args=(i,)) for i in range(20)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Time taken with Mutex lock: {round(time.time()-st, 1)} seconds")

# with semaphore lock: 20/5 batches of execution 0.2*4 seconds
sem_lock = threading.Semaphore(5)
def print_num3(i):
    with sem_lock:
        # do something
        time.sleep(sleep_time)
st = time.time()
threads = [threading.Thread(target=print_num3, args=(i,)) for i in range(20)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Time taken with Semaphore lock: {round(time.time()-st, 1)} seconds")
