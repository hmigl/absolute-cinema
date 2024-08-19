import threading
import time
from collections import deque


class Semaphore:
    """
    Implementação de um semáforo personalizado para controle de acesso à seções críticas em um ambiente multithreading.

    Este semáforo utiliza uma variável de contagem para controlar o número de threads que podem acessar uma seção crítica
    simultaneamente. É protegido por um `threading.Lock`, garantindo que as operações de aquisição e liberação
    sejam realizadas de maneira segura. Além disso, implementa uma fila de threads para garantir a (fairness)
    no acesso à seção crítica
    """

    def __init__(self, max_count):
        self.__max_count = max_count
        self.__current_count = max_count
        self.__lock = threading.Lock()
        self.__condition = threading.Condition(self.__lock)
        self.__queue = (
            deque()
        )  # Fila de threads, utilizada com o propósito de garantir 'fairness'

    def acquire(self, timeout=None):
        with self.__condition:
            start_time = time.time()

            self.__queue.append(threading.current_thread())

            while True:
                if timeout:
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= timeout:
                        self.__queue.remove(threading.current_thread())
                        return False

                if (
                    self.__queue[0] == threading.current_thread()
                    and self.__current_count > 0
                ):
                    self.__current_count -= 1
                    self.__queue.popleft()  # Remova a thread da fila
                    return True

                remaining_time = None if not timeout else timeout - elapsed_time
                self.__condition.wait(timeout=remaining_time)

    def release(self):
        with self.__condition:
            if self.__current_count >= self.__max_count:
                raise ValueError("Semaphore released too many times")
            self.__current_count += 1
            self.__condition.notify()  # Notifique a thread que está esperando

    def locked(self):
        with self.__lock:
            return self.__current_count == 0

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
