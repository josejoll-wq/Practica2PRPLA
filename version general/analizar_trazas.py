def analizar_trazas(num_usuarios: int, archivo: str = "trazas.txt") -> None:
    cruzando = {}
    linea_num = 0
    total_salidas = 0
    errores = 0

    with open(archivo, "r") as f:
        for linea in f:
            linea_num += 1
            partes = linea.strip().split()
            if not partes: 
                continue
            
             # Construir tipo y acción
            accion = partes[-1]
            tipo = " ".join(partes[:-2])
            
            # Si el tipo no está en el diccionario, lo inicializamos a 0
            if tipo not in cruzando:
                cruzando[tipo] = 0
            
            # Actualizar estado
            if accion == "entra":
                cruzando[tipo] += 1
            elif accion == "sale":
                cruzando[tipo] -= 1
                total_salidas += 1
            
            
            # Buscamos en el diccionario cuales son los tipos que están cruzando actualmente el punete (cantidad > 0)
            tipos_activos = [t for t, cantidad in cruzando.items() if cantidad > 0]
            
            # Si hay más de 1 tipo diferente en el puente al mismo tiempo hay una colisión.
            if len(tipos_activos) > 1:
                nombres_chocando = ", ".join(tipos_activos)
                print(f"ERROR línea {linea_num} en el archivo {archivo}: Hay colisión entre {nombres_chocando}")
                errores += 1

        # Validación final
        if total_salidas == num_usuarios:
            print(f"El análisis de {archivo} ha finalizado. Han cruzado los {num_usuarios} usuarios correctamente.")
        else:
            print(f"El análisis de {archivo} ha finalizado. Se esperaban {num_usuarios} usuarios pero salieron {total_salidas}.")
            errores += 1

    # Contamos los errores encontrados durante el análisis
    if errores == 0:
        print(f"Análisis de {archivo} finalizado. La traza está bien.\n")
    else:
        print(f"Análisis de {archivo} finalizado con {errores} errores.\n")


if __name__ == "__main__":

    # Probamos las 3 simulaciones del main directamente
    analizar_trazas(30, "trazas1.txt")
    analizar_trazas(30, "trazas2.txt")
    analizar_trazas(101, "trazas3.txt")