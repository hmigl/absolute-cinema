import threading


class Barrier:
    """
    Implementação de uma barreira personalizada para controle de sincronização entre threads em um ambiente
    multithreading.

    Barreira utilizada para sincronizar um número fixo de threads, fazendo com que elas esperem até que todas
    tenham alcançado um determinado ponto de execução, antes de prosseguir.
    """

    def __init__(self, n):
        if n <= 0:
            raise ValueError("n should be a positive integer")
        self.__n = n
        self.__count = 0
        self.__cond = threading.Condition()
        self.__interrupt = threading.Event()

    def wait(self):
        """
        Faz a thread esperar até que todas as threads tenham alcançado a barreira.
        :return: None
        """
        with self.__cond:
            self.__count += 1
            if self.__count != self.__n:
                self.__cond.wait()
            else:
                self.__cond.notify_all()
                self.__count = 0

    def interrupt(self):
        """
        Interrompe a espera das threads na barreira.
        :return: None
        """
        with self.__cond:
            self.__interrupt.set()
            self.__cond.notify_all()
