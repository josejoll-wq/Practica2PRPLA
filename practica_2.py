import time
import random
from threading import Thread, Lock, Condition
import os


COCHE_NORTE = 0
COCHE_SUR = 1
PEATON = 2

lista_tipo = [COCHE_NORTE, COCHE_SUR, PEATON]

class GuardarTrazas:
    def __init__(self, archivo="trazas.txt"):
        self.archivo = archivo
        self.archivo_lock = Lock()
        
        ruta_absoluta = os.path.abspath(self.archivo)
        print(f"\nEl archivo de trazas se va a guardar aquí:")
        print(f"en {ruta_absoluta}\n")

        with open(self.archivo, "w") as f:
            f.write("")

    def guardar(self, mensaje):
        with self.archivo_lock: 
            with open(self.archivo, "a") as f:
                f.write(mensaje + "\n")

class GestorDelPuente:
    def __init__(self, guardador):
        self.cerrojo = Lock()
        
        self.guardador = guardador
        
        self.cruzando = {COCHE_NORTE: 0, COCHE_SUR: 0, PEATON: 0}
        self.esperando = {COCHE_NORTE: 0, COCHE_SUR: 0, PEATON: 0}
        
        self.turno = COCHE_NORTE
        
        self.condiciones = {t: Condition(self.cerrojo) for t in lista_tipo}
        
        self.nombres = {COCHE_NORTE: "coche norte", COCHE_SUR: "coche sur", PEATON: "peaton"}


    def pueden_cruzar(self, tipo):
            otros_cruzando = sum(self.cruzando[t] for t in lista_tipo if t != tipo)
            if otros_cruzando > 0: 
                return False
            
            otros_esperando = sum(self.esperando[t] for t in lista_tipo if t != tipo)
            if self.turno != tipo and otros_esperando > 0: 
                return False
                
            return True

    def quiero_cruzar(self, tipo, num_usuario):
        with self.cerrojo:
            self.guardador.guardar(f"{self.nombres[tipo]} {num_usuario} pide")
            self.esperando[tipo] += 1 
            
            while not self.pueden_cruzar(tipo):
                self.condiciones[tipo].wait()
                
            self.esperando[tipo] -= 1
            self.cruzando[tipo] += 1 
            self.guardador.guardar(f"{self.nombres[tipo]} {num_usuario} entra")

    def he_cruzado(self, tipo, num_usuario):
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

    def cruzar(self, tipo, num_usuario):
        self.quiero_cruzar(tipo, num_usuario)
        
        time.sleep(random.uniform(0.1, 0.3)) 
        
        self.he_cruzado(tipo, num_usuario)



class Usuario(Thread):
    def __init__(self, gestor, tipo, num_usuario):
        super().__init__()
        self.gestor = gestor
        self.tipo = tipo     
        self.num_usuario = num_usuario

    def run(self):
        self.gestor.cruzar(self.tipo, self.num_usuario)



if __name__ == "__main__":
    guardador = GuardarTrazas()
    gestor = GestorDelPuente(guardador)
    
    usuarios = []
    
    for i in range(10):
        t = random.choice(lista_tipo)
        u = Usuario(gestor, t, i)
        usuarios.append(u)
        
        u.start()
        
    for u in usuarios: 
        u.join()
        
    print("Simulación terminada. Trazas guardadas en trazas.txt")