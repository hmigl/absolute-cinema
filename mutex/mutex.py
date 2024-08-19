import threading
import time


class Mutex:
    def __init__(self):
        self.__lock = threading.Lock()
        self.__flag = False

    def acquire(self, timeout=None):
        start_time = time.time()
        while True:
            with self.__lock:
                if not self.__flag:
                    self.__flag = True
                    return True
            if timeout and (time.time() - start_time) >= timeout:
                return False
            time.sleep(0.01)

    def release(self):
        with self.__lock:
            self.__flag = False

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
