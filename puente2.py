import time
import random
from threading import Lock, Condition
from guardatrazas import GuardarTrazas

COCHE_NORTE = 0
COCHE_SUR = 1
PEATON = 2

#Añadimos mas tipos al problema:
GANADO = 3 # Similar a los peatones, no pueden coincidir con otros tipos
AMBULANCIA_NORTE = 4 # Similar a los coches, pero con preferencia sobre todos los demás tipos
AMBULANCIA_SUR = 5

lista_tipo = [COCHE_NORTE, COCHE_SUR, PEATON, GANADO, AMBULANCIA_NORTE, AMBULANCIA_SUR]

class GestorDelPuente:
    def __init__(self, guardador : GuardarTrazas):
        self.cerrojo = Lock()
        self.guardador = guardador

        self.cruzando = {COCHE_NORTE: 0, COCHE_SUR: 0, PEATON: 0, GANADO: 0, AMBULANCIA_NORTE: 0, AMBULANCIA_SUR: 0}
        self.esperando = {COCHE_NORTE: 0, COCHE_SUR: 0, PEATON: 0, GANADO: 0, AMBULANCIA_NORTE: 0, AMBULANCIA_SUR: 0}

        self.turno = COCHE_NORTE

        self.condiciones = {t: Condition(self.cerrojo) for t in lista_tipo}

        self.nombres = {
            COCHE_NORTE: "coche norte",
            COCHE_SUR: "coche sur",
            PEATON: "peaton",
            GANADO: "ganado",
            AMBULANCIA_NORTE: "ambulancia_norte",
            AMBULANCIA_SUR: "ambulancia_sur"
        }

    def pueden_cruzar(self, tipo : int) -> bool:
        otros_cruzando = sum(self.cruzando[t] for t in lista_tipo if t != tipo)
        if otros_cruzando > 0:
            return False

        otros_esperando = sum(self.esperando[t] for t in lista_tipo if t != tipo)
        if self.turno != tipo and otros_esperando > 0:
            return False

        return True

    def quiero_cruzar(self, tipo : int, num_usuario : int) -> None:
        with self.cerrojo:
            self.guardador.guardar(f"{self.nombres[tipo]} {num_usuario} pide")
            self.esperando[tipo] += 1

            while not self.pueden_cruzar(tipo):
                self.condiciones[tipo].wait()

            self.esperando[tipo] -= 1
            self.cruzando[tipo] += 1
            self.guardador.guardar(f"{self.nombres[tipo]} {num_usuario} entra")

        return None

    def he_cruzado(self, tipo : int, num_usuario : int) -> None:
        with self.cerrojo:
            self.cruzando[tipo] -= 1
            self.guardador.guardar(f"{self.nombres[tipo]} {num_usuario} sale")

            otros_esperando = sum(self.esperando[t] for t in lista_tipo if t != tipo)

            # Se cambian los turnos de forma circular para garantizar que a todos les llegue el turno
            # Se hace una excepción al final con las ambulancias, pues deben tener prioridad máxima
            # Al hacerlo de esta forma resulta más sencillo añadir más tipos.
            if otros_esperando > 0:
                sig = (tipo + 1) % 6
                sig1 = (tipo + 2) % 6
                sig2 = (tipo + 3) % 6
                sig3 = (tipo + 4) % 6
                sig4 = (tipo + 5) % 6

                if self.esperando[sig] > 0:
                    self.turno = sig
                elif self.esperando[sig1] > 0:
                    self.turno = sig1
                elif self.esperando[sig2] > 0:
                    self.turno = sig2
                elif self.esperando[sig3] > 0:
                    self.turno = sig3
                elif self.esperando[sig4] > 0:
                    self.turno = sig4

            # Si hay ambulancias esperando se les concede el turno inmediatamente (la ambulancia del SUR tiene prioridad sobre la del NORTE para evitar colisiones)
            if self.esperando[AMBULANCIA_NORTE] > 0:
                self.turno = AMBULANCIA_NORTE

            if self.esperando[AMBULANCIA_SUR] > 0:
                self.turno = AMBULANCIA_SUR

            if self.cruzando[tipo] == 0:
                self.condiciones[self.turno].notify_all()

        return None

    def cruzar(self, tipo : int, num_usuario : int) -> None:
        self.quiero_cruzar(tipo, num_usuario)
        time.sleep(random.uniform(0.05, 0.2))
        self.he_cruzado(tipo, num_usuario)

        return None