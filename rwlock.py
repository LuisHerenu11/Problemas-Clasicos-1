""" rwlock.py
    Clase para implementar read-write locks sobre la libreria standard threading.
    rLock: Read Lock, permite multiples accesos concurrentes a operaciones de Lectura (Read)
    wLock: Write Lock, permite un unico acceso (exclusión mútuo) para Escritura (Write)
    Esto esta implementado con dos MUTEX (instancias threading.Lock) y una variable entera (num_r) que lleva
    la cuenta de la cantidad de Readers bloqueados. Un Lock (num_r_lock) protege el acceso a num_r y solo es
    utlizado por los Readers. El otro Lock (w_lock) es de acceso global y asegura la exclusión mutua de los
    writers. Esto requiere que un Lock adquirido por una thread pueda ser liberado por otra.

    Comenzar Lectura (adquirir Read Lock)
    1 obtener num_r_lock
    2 incrementar num_r
    3 Si num_r = 1, obtener w_lock
    4 liberar num_r_lock

    Fin de Lectura (Liberar Read Lock)
    1 obtener num_r_lock
    2 decrementar num_r
    3 Si num_r = 0, liberar w_lock
    4 liberar num_r_lock

    Comenzar Escritura
    1 obtener w_lock

    Fin de Escritura
    2 liberar w_lock

    Esta es una implementación de RW Locks con Preferencia de Lectura (Read-Preferring RW locks).
    Este tipo de RW lock permite la máxima concurrencia, pero pueden provocar falta de escritura (Write-Starvation)
    si la concurerncia es alta.
    Esto se debe a que los hilos writer no pueden adquirir el Lock mientras al menos un hilo reader lo tenga.
    Dado que varios hilos reader pueden tener el lock a la vez, un hilo writer puede quedarse esperando el lock
    mientras nuevos hilos reader pueden obtenerlo, incluso hasta el punto en que el writer tenga que esperar
    hasta que todos los readers que tienen el lock lo liberen.

    Nota: Hay otras implementaciones de RW Locks:

        Write-preferring RW Locks (resuelve el problema de writer-starvation)
        Unspecified-priority RW Locks

"""


# _______________________________________________________________________
# Imports

from threading  import Lock

# _______________________________________________________________________
# Class

class RWLock(object):
    """ Clase RWLock;  tiene como propósito permitir que un objeto sea leido por multiples hilos
        simultáneamente, pero solo puede ser escrito por un solo hilo a la vez.

        Uso:
            from rwlock import RWLock
            mi_RWLock = RWLock()

            # Al leer de mi_objeto
            mi_RWLock.r_acquire()
            try:
                # tareas de SOLO Lectura con mi_objeto
            finally:
                mi_RWLock.r_release()


            # Al escribir en my_obj:
            mi_RWLock.w_acquire()
            try:
                # tareas de escritura en mi_objeto
            finally:
                mi_RWLock.w_release()

    """
    # Constructor

    def __init__(self):

        self.w_lock = Lock() # write lock
        self.num_r_lock = Lock() # read lock
        self.num_r = 0 # contador locks 

    # ___________________________________________________________________
    # Metodos de Lectura (Reading).

    def r_acquire(self):
        self.num_r_lock.acquire() # acá un lector, les dice a otros lectores que esta leyendo.
        self.num_r += 1
        if self.num_r == 1:
            self.w_lock.acquire() # acá si alguien esta leyendo, impide que el escritor escriba.
        self.num_r_lock.release() # libera el lock de lectura.

    def r_release(self):
        assert self.num_r > 0 # si hay un lock de lectura bloqueado hacer tal.
        self.num_r_lock.acquire() # adquiere lock de lectura.
        self.num_r -= 1 #
        if self.num_r == 0:
            self.w_lock.release() # libera el write lock adquirido por otro hilo. VER LINEA 91.
        self.num_r_lock.release() # libera el lock de lectura adquirido en el mismo hilo.


    # ___________________________________________________________________
    # Métodos de Escritura (Writing).

    def w_acquire(self):
        self.w_lock.acquire()

    def w_release(self):
        self.w_lock.release()
