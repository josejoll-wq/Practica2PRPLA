def analizar_trazas(archivo: str = "trazas1.txt", num_usuarios: int = 30) -> None:
    cruzando = {
        "coche norte": 0,
        "coche sur": 0,
        "ambulancia norte": 0,
        "ambulancia sur": 0,
        "peaton": 0,
        "ganado": 0
    }

    linea_num = 0
    total_salidas = 0

    with open(archivo, "r") as f:
        for linea in f:
            linea_num += 1
            partes = linea.strip().split()
            if not partes:
                continue

            # Construir tipo
            if partes[0] in ["coche", "ambulancia"]:
                tipo = partes[0] + " " + partes[1]
            else:
                tipo = partes[0]

            accion = partes[-1]

            # Actualizar estado
            if accion == "entra":
                cruzando[tipo] += 1
            elif accion == "sale":
                cruzando[tipo] -= 1
                total_salidas += 1

            # Variables cortas
            cn = cruzando["coche norte"]
            cs = cruzando["coche sur"]
            an = cruzando["ambulancia norte"]
            a_s = cruzando["ambulancia sur"]
            p = cruzando["peaton"]
            g = cruzando["ganado"]

            vehiculos_norte = cn + an
            vehiculos_sur = cs + a_s
            total_vehiculos = vehiculos_norte + vehiculos_sur

            # Colisiones frontales
            if vehiculos_norte > 0 and vehiculos_sur > 0:
                print(f"ERROR línea {linea_num}: colisión frontal entre vehículos")

            #  Atropellos peatones
            if p > 0 and total_vehiculos > 0:
                print(f"ERROR línea {linea_num}: peatón atropellado")

            #  Ganado con vehículos
            if g > 0 and total_vehiculos > 0:
                print(f"ERROR línea {linea_num}: ganado en peligro con vehículos")

            #  Peatón + ganado
            if g > 0 and p > 0:
                print(f"AVISO línea {linea_num}: peatones y ganado coinciden")

        # Validación final
        if total_salidas == num_usuarios:
            print(f"Han cruzado los {num_usuarios} usuarios correctamente.")
        else:
            print(f"Se esperaban {num_usuarios} usuarios pero salieron {total_salidas}.")

    print("Análisis finalizado.")

analizar_trazas()
