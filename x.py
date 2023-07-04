import time
from multiprocessing import Process, Queue
import multiprocessing
import threading


def queueToGenerator(q: multiprocessing.Queue):
    while True:
        v = q.get()
        if v is None: return
        yield v

def processChan(gen, name):
    for v in gen:
        print(name, "receive", v)
    print(name, "close")

def main():
    a, b = Queue(), Queue()
    threading.Thread(target=processChan, args=(queueToGenerator(a), "a")).start()
    
    Process(target=processChan, args=(queueToGenerator(b), "b")).start()
    
    for i in range(5):
        print("send", i)
        a.put(i)
        b.put(i)
    a.put(None)
    b.put(None)
    # process_a.join()
    # process_b.join()
    print("finish")
    time.sleep(1)

if __name__ == "__main__":
    main()
