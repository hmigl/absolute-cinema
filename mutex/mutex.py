import threading
import time


class Mutex:
    """
    Mutex personalizado para controle de acesso à seções críticas em um ambiente multithreading.

    Esta implementação de Mutex utiliza uma variável booleana (`__flag`) para indicar se o mutex está
    atualmente bloqueado. O mutex é protegido por um `threading.Lock`, garantindo que as operações de
    aquisição e liberação sejam realizadas de maneira segura.

    Uso Típico:
        Este mutex é adequado para cenários onde o controle simples de acesso a uma seção crítica é necessário,
        e onde o bloqueio pode ser gerenciado manualmente.
    """

    def __init__(self):
        self.__lock = threading.Lock()
        self.__flag = False

    def acquire(self, timeout=None):
        """
        Tenta adquirir o mutex. Se o mutex estiver bloqueado, o método espera até que ele seja liberado ou até que o
        tempo limite seja atingido (se especificado).
        :param timeout: Tempo limite para esperar a aquisição do mutex (em segundos)
        :return: True se o mutex foi adquirido, False se o tempo limite foi atingido
        """
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
        """
        Libera o mutex, permitindo que outros threads possam adquiri-lo.
        :return: None
        """
        with self.__lock:
            self.__flag = False

    def __enter__(self):
        """
        Permite o uso do mutex em um bloco 'with'.
        """
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Libera o mutex automaticamente ao sair do bloco 'with'.
        """
        self.release()
