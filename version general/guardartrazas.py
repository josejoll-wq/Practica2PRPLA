class GuardarTrazas:
    def __init__(self, archivo : str ="trazas.txt"):
        self.archivo = archivo
        with open(self.archivo, "w") as f:
            f.write("")

    def guardar(self, mensaje : str) -> None:
        with open(self.archivo, "a") as f:
            f.write(mensaje + "\n")
        return  None
