import time
import random
from threading import Lock, Condition
from guardartrazas import GuardarTrazas
COCHE_NORTE = 0
COCHE_SUR = 1
PEATON = 2

lista_tipo = [COCHE_NORTE, COCHE_SUR, PEATON]


class GestorDelPuente:
    def __init__(self, guardador : GuardarTrazas):
        self.cerrojo = Lock()
        self.guardador = guardador

        self.cruzando = {COCHE_NORTE: 0, COCHE_SUR: 0, PEATON: 0}
        self.esperando = {COCHE_NORTE: 0, COCHE_SUR: 0, PEATON: 0}

        self.turno = COCHE_NORTE

        self.condiciones = {t: Condition(self.cerrojo) for t in lista_tipo}

        self.nombres = {
            COCHE_NORTE: "coche norte",
            COCHE_SUR: "coche sur",
            PEATON: "peaton"
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

            if otros_esperando > 0:
                siguiente = (tipo + 1) % 3
                alternativo = (tipo + 2) % 3

                if self.esperando[siguiente] > 0:
                    self.turno = siguiente
                elif self.esperando[alternativo] > 0:
                    self.turno = alternativo

            if self.cruzando[tipo] == 0:
                self.condiciones[self.turno].notify_all()

        return None

    def cruzar(self, tipo : int, num_usuario : int) -> None:
        self.quiero_cruzar(tipo, num_usuario)
        time.sleep(random.uniform(0.1, 0.3))
        self.he_cruzado(tipo, num_usuario)

        return None
