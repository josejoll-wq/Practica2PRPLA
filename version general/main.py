import random
import time
from threading import Thread
from puente2 import GestorDelPuente, TIPOS_USUARIO
from guardartrazas import GuardarTrazas

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
    gestor = GestorDelPuente(guardador, TIPOS_USUARIO)
    usuarios: list[Usuario] = []
    num_usuarios = 30

    for num_usuario in range(num_usuarios):
        t = random.choice(list(TIPOS_USUARIO.keys()))
        u = Usuario(gestor, t, num_usuario)
        usuarios.append(u)
        u.start()

        # Añadimos tiempo entre las llegadas de los coches/peatones
        time.sleep(random.uniform(0, 0.01))

    for u in usuarios:
        u.join()

    print("Simulación 'normal' terminada. Trazas guardadas en trazas1.txt")
  
    # Simulación "solo coches":
    guardador = GuardarTrazas("trazas2.txt")
    gestor = GestorDelPuente(guardador, TIPOS_USUARIO)
    usuarios: list[Usuario] = []
    num_usuarios = 30

    for num_usuario in range(num_usuarios):
        t = random.choice([0, 1])  # Solo coches norte y sur
        u = Usuario(gestor, t, num_usuario)
        usuarios.append(u)
        u.start()

        # Añadimos tiempo entre las llegadas de los coches/peatones
        time.sleep(random.uniform(0, 0.01))

    for u in usuarios:
        u.join()

    print("Simulación 'solo coches' terminada. Trazas guardadas en trazas2.txt")


     # Simulación "100 peatones y 1 coche":
    guardador = GuardarTrazas("trazas3.txt")
    gestor = GestorDelPuente(guardador, TIPOS_USUARIO)
    usuarios: list[Usuario] = []
    num_usuarios = 101
    tipos = [2] * 100 + [0]
    
    random.shuffle(tipos)  # Mezclamos el orden para que el coche no siempre sea el último en llegar
    
    for num_usuario, t in enumerate(tipos):
        u = Usuario(gestor, t, num_usuario)
        usuarios.append(u)
        u.start()

        # Añadimos tiempo entre las llegadas de los coches/peatones
        time.sleep(random.uniform(0, 0.01))

    for u in usuarios:
        u.join()

    print(f"Simulación '100 peatones y 1 coche' terminada. Trazas guardadas en trazas3.txt")
