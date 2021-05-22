import threading
import random
import logging
import time
from typing import NamedTuple
from rwlock import RWLock

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

rwlock = RWLock()
partido = ["Gimnasia", 1, "Estudiantes", 0]

class Lector(threading.Thread):
    def __init__(self):
        super().__init__()
       

    def run(self):
        global partido
        while True:
            rwlock.r_acquire()
            try:
                logging.info(f'el resultado fue: {partido[0]} {partido[1]} - {partido[2]} {partido[3]} ')
            finally:
                rwlock.r_release()
                time.sleep(random.randint(1,2))

class Escritor(threading.Thread):
    def __init__(self):
        super().__init__()
        self.equipos = ["Boca", "River", "Racing", "Independiente", "San Lorenzo", "Huracán", "Gimnasia", "Estudiantes", "Velez", "Ferro", "Lanus", "Quilmes"]

    def run(self):
        global partido
        while True:
            rwlock.w_acquire()
            try:
                equipo1 = self.equipos[random.randint(0,len(self.equipos)-1)]
                equipo2 = self.equipos[random.randint(0,len(self.equipos)-1)]
                int_goles1 = random.randint(0,3)
                int_goles2 = random.randint(0,3)

                partido[0] = equipo1
                partido[1] = int_goles1
                partido[2] = equipo2
                partido[3] = int_goles2

                logging.info(f'Partido actualizado por: {self.name}')
                time.sleep(random.randint(1,2))
            finally:
                rwlock.w_release()


def main():
    hilos = []
    escritor = Escritor() 
    hilos.append(escritor)
    logging.info(f'Arrancando escritor {escritor.name}')
    escritor.start()

    for i in range(3):
        lector = Lector() 
        hilos.append(lector)
        logging.info(f'Arrancando lector {lector.name}')
        lector.start()

    for thr in hilos:
        thr.join()


if __name__ == '__main__':
    main()
