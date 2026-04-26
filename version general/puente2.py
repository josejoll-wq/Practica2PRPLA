import time
import random
from threading import Lock, Condition
from guardartrazas import GuardarTrazas


TIPOS_USUARIO = {
    0: "coche norte",
    1: "coche sur",
    2: "peaton",
    #Añadimos mas tipos al problema:
    3: "ganado",  #Similar a los peatones, no pueden coincidir con otros tipos
    4: "ambulancia norte", # Similar a los coches, pero con preferencia sobre todos los demás tipos
    5: "ambulancia sur",
    6: "bicicleta",
    7: "motocicleta"
    # Aquí se pueden añadir los tipos que se quieran,
    # se les asigna un número único y un nombre
}

lista_tipo = list(TIPOS_USUARIO.keys()) # La lista de tipos con los números 


class GestorDelPuente:
    def __init__(self, guardador : GuardarTrazas, tipos: dict = TIPOS_USUARIO):
        self.cerrojo = Lock()
        self.guardador = guardador
        
        self.lista_tipos = list(tipos.keys())
        self.num_tipos = len(self.lista_tipos)

        self.cruzando = {t: 0 for t in self.lista_tipos}
        self.esperando = {t: 0 for t in self.lista_tipos}

        self.turno = self.lista_tipos[0]  # El primer tipo en la lista empieza teniendo el turno

        self.condiciones = {t: Condition(self.cerrojo) for t in self.lista_tipos}


        self.nombres = tipos

        #Aquí añadimos los tipos prioritarios sobre todos los demás,
        # en este caso las ambulancias, pero se podrían añadir los tipos que se quieran
        # En esta lista se ordenan de más a menos prioridad,
        #con el tipo 5 (ambulancia sur) teniendo más prioridad sobre el tipo 4 (ambulancia norte) 
        # para evitar colisiones entre ellas.
        self.tipos_prioritarios = [5, 4]



    def pueden_cruzar(self, tipo : int) -> bool:
        otros_cruzando = sum(self.cruzando[t] for t in self.lista_tipos if t != tipo)
        if otros_cruzando > 0:
            return False

        otros_esperando = sum(self.esperando[t] for t in self.lista_tipos if t != tipo)
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

            otros_esperando = sum(self.esperando[t] for t in self.lista_tipos if t != tipo)

            # Se cambian los turnos de forma circular para garantizar que a todos les llegue el turno se hace una excepción al final con las ambulancias, pues tienen prioridad máxima
            # Al hacerlo de esta forma resulta más sencillo añadir más tipos.
            if otros_esperando > 0:
                indice_actual = self.lista_tipos.index(tipo)

                # Hacemos un bucle y buscamos el primer tipo más próximo que esté esperando para darle el turno
                for i in range(1, self.num_tipos):
                        indice_sig = (indice_actual + i) % self.num_tipos
                        tipo_sig = self.lista_tipos[indice_sig]
                        
                        if self.esperando[tipo_sig] > 0:
                            self.turno = tipo_sig
                            break

            # Si hay ambulancias esperando, le damos el turno inmediatamente siguiente. (la ambulancia del SUR tiene prioridad sobre la del NORTE para evitar colisiones)
                for t in self.tipos_prioritarios:
                    if t in self.esperando and self.esperando[t] > 0:
                        self.turno = t
                        break # Si encontramos al más prioritario, paramos de buscar

            if self.cruzando[tipo] == 0:
                self.condiciones[self.turno].notify_all()

        return None

    def cruzar(self, tipo : int, num_usuario : int) -> None:
        self.quiero_cruzar(tipo, num_usuario)
        time.sleep(random.uniform(0.05, 0.2))
        self.he_cruzado(tipo, num_usuario)

        return None
