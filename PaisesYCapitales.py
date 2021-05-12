import threading
import random
import logging
import time

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class listaFinita(list):

    def __init__(self, max_elementos):
            self.max_elementos = max_elementos
            super().__init__()

    def pop(self, index):
        assert len(self) != 0, "lista vacia"
        return super().pop(index)

    def append(self, item):
        assert len(self) < self.max_elementos,"lista llena"
        super().append(item)

    def insert(self, index, item):
        assert index < self.max_elementos, "indice invalido"
        super().insert(index, item)

    def full(self):
        if len(self) == self.max_elementos:
            return True
        else:
            return False

    def empty(self):
        if len(self) == 0:
            return True
        else:
            return False    

class Productor(threading.Thread):
    def __init__(self, lista = listaFinita):
        super().__init__()
        self.lista = lista
        self.lock = threading.Lock()
        self.listaPaises = [ ("España","Madrid"), ("Francia","Paris"),("Italia","Roma"),("Inglaterra","Londres"),("Alemania","Berlin"),("Rusia","Moscu"),("Turquia","Istambul"),("China","Pekin"), ("Japon","Tokio"),("Emiratos Arabes","Dubai"),("Argentina","Buenos Aires"),("Brasil","Brasilia"),("Colombia","Bogota"),("Uruguay","Montevideo")]

    def run(self):
        while True:
            if not self.lista.full():
                self.lock.acquire()
            try:
                if self.lock.locked(): 
                    self.lista.append(self.listaPaises[random.randint(0,len(self.listaPaises)-1)])
                    logging.info(f'La capital de: {self.lista[-1][0]} es: {self.lista[-1][1]}')
                    time.sleep(random.randint(1,5))
            finally:
                if self.lock.locked():
                    self.lock.release()



class Consumidor(threading.Thread):
    def __init__(self, lista):
        super().__init__()
        self.lista = lista


    def run(self):
        while True:
            elemento = self.lista.pop(0)
            logging.info(f'consumio la capital de: {elemento[0]} es: {elemento[1]}')
            time.sleep(random.randint(1,5))

def main():
    lista = listaFinita(14)
    hilos = []
    
    for i in range(7):
        productor = Productor(lista)
        consumidor = Consumidor(lista)
        hilos.append(productor)
        hilos.append(consumidor)

        logging.info(f'Arrancando productor {productor.name}')
        productor.start()

        logging.info(f'Arrancando productor {consumidor.name}')
        consumidor.start()

    for h in hilos:
        h.join()


if __name__ == '__main__':
    main()
