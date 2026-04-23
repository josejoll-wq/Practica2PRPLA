import random
import time
from threading import Thread
from puente import GestorDelPuente, lista_tipo
from analizar_trazas import analizar_trazas

class GuardarTrazas:
    def __init__(self, archivo : str ="trazas.txt"):
        self.archivo = archivo
        with open(self.archivo, "w") as f:
            f.write("")

    def guardar(self, mensaje : str) -> None:
        with open(self.archivo, "a") as f:
            f.write(mensaje + "\n")
        return  None

class Usuario(Thread):
    def __init__(self, gestor : GestorDelPuente, tipo : int, num_usuario : int):
        super().__init__()
        self.gestor = gestor
        self.tipo = tipo
        self.num_usuario = num_usuario

    def run(self)-> None:
        self.gestor.cruzar(self.tipo, self.num_usuario)
        return None



if __name__ == "__main__":
    guardador = GuardarTrazas()
    gestor = GestorDelPuente(guardador)

    usuarios : list[Usuario] = []
    num_usuarios = 15
    # Simulación:
    for i in range(num_usuarios):
        t = random.choice(lista_tipo)
        u = Usuario(gestor, t, i)
        usuarios.append(u)
        u.start()

        # Añadimos tiempo entre las llegadas de los coches/peatones
        time.sleep(random.uniform(0.05, 0.2))

    for u in usuarios:
        u.join()

    print("Simulación terminada. Trazas guardadas en trazas.txt")

    analizar_trazas( archivo= "trazas.txt",num_usuarios = num_usuarios)