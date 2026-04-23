import random
import time
from threading import Thread
from puente import GestorDelPuente, lista_tipo


class GuardarTrazas:
    def __init__(self, archivo="trazas.txt"):
        self.archivo = archivo
        with open(self.archivo, "w") as f:
            f.write("")

    def guardar(self, mensaje):
        with open(self.archivo, "a") as f:
            f.write(mensaje + "\n")


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

    # Simulación:
    for i in range(10):
        t = random.choice(lista_tipo)
        u = Usuario(gestor, t, i)
        usuarios.append(u)
        u.start()

        # Añadimos tiempo entre las llegadas de los coches/peatones
        time.sleep(random.uniform(0.05, 0.2))

    for u in usuarios:
        u.join()

    print("Simulación terminada. Trazas guardadas en trazas.txt")
