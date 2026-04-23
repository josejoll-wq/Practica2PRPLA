import random
import time
from threading import Thread
from puente import GestorDelPuente, GuardarTrazas, lista_tipo
from analizar_trazas import analizar_trazas


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

    # Simulación "normal":
    guardador = GuardarTrazas("trazas1.txt")
    gestor = GestorDelPuente(guardador)
    usuarios: list[Usuario] = []
    num_usuarios = 15

    for i in range(num_usuarios):
        t = random.choice(lista_tipo)
        u = Usuario(gestor, t, i)
        usuarios.append(u)
        u.start()

        # Añadimos tiempo entre las llegadas de los coches/peatones
        time.sleep(random.uniform(0.05, 0.2))

    for u in usuarios:
        u.join()

    print("Simulación 'normal' terminada. Trazas guardadas en trazas1.txt")
    analizar_trazas(archivo="trazas1.txt", num_usuarios=num_usuarios)

    # Simulación "solo coches":

    guardador = GuardarTrazas("trazas2.txt")
    gestor = GestorDelPuente(guardador)
    usuarios: list[Usuario] = []
    num_usuarios = 30

    for i in range(num_usuarios):
        t = random.choice([0,1])
        u = Usuario(gestor, t, i)
        usuarios.append(u)
        u.start()

        # Añadimos tiempo entre las llegadas de los coches/peatones
        time.sleep(random.uniform(0.05, 0.2))

    for u in usuarios:
        u.join()

    print("Simulación 'solo coches' terminada. Trazas guardadas en trazas2.txt")

    analizar_trazas(archivo="trazas2.txt", num_usuarios = num_usuarios)
