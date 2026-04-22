def analizar_trazas(archivo = "trazas.txt"):
    cruzando = {"coche norte": 0, "coche sur": 0, "peaton": 0}
    linea_num = 0
    
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
            
            cn, cs, p = cruzando["coche norte"], cruzando["coche sur"], cruzando["peaton"]
            
            if (cn > 0 and cs > 0):
                print(f"ERROR en Línea {linea_num}: ¡Colisión frontal de coches norte y sur!")
            if (p > 0 and (cn > 0 or cs > 0)):
                print(f"ERROR en Línea {linea_num}: ¡Peatones y coches coinciden, hay un atropello!")
                
    print("Análisis finalizado. Si no hay mensajes de ERROR, la traza es segura.")

analizar_trazas()