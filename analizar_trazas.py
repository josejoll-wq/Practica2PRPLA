num_usuarios = input("Introduce el número total de usuarios que quieren cruzar el puente")
def analizar_trazas(archivo: str = "trazas.txt", num_usuarios : int) -> None:
    cruzando = {"coche norte": 0, "coche sur": 0, "peaton": 0}
    linea_num = 0
    total_salidas = 0

    with open(archivo ,  "r") as f:
        for linea in f:
            linea_num += 1
            partes = linea.strip().split()
            if not partes: continue
            
            tipo = partes[0] + (" " + partes[1] if partes[1] in ["norte", "sur"] else "")
            accion = partes[-1]
            
            if accion == "entra":
                cruzando[tipo] += 1
            elif accion == "sale":
                cruzando[tipo] -= 1
                total_salidas += 1
            
            cn, cs, p = cruzando["coche norte"], cruzando["coche sur"], cruzando["peaton"]
            
            if (cn > 0 and cs > 0):
                print(f"ERROR en Línea {linea_num}: ¡Colisión frontal de coches norte y sur!")
            if (p > 0 and (cn > 0 or cs > 0)):
                print(f"ERROR en Línea {linea_num}: ¡Peatones y coches coinciden, hay un atropello!")

        if total_salidas == num_usuarios:
            print(f"Han cruzado los {num_usuarios} usuarios correctamente.")
        else:
            print(f"Se esperaban {num_usuarios} usuarios pero solo salieron {total_salidas}.")

    print("El análisis ha finalizado. Si no hay mensajes de ERROR, la traza es correcta.")
    return None

analizar_trazas()
