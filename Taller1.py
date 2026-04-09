def leer_instancia_scp(ruta_archivo):
    with open(ruta_archivo, 'r') as file:
        data = file.read().split()

    if not data:
        return None

    num_elementos = int(data[0])
    num_subconjuntos = int(data[1])

    costos = []
    idx = 2
    for _ in range(num_subconjuntos):
        costos.append(float(data[idx]))
        idx += 1

    cobertura_por_elemento = {}
    for i in range(1, num_elementos + 1):
        cantidad_subconjuntos = int(data[idx])
        idx += 1
        subconjuntos = []
        for _ in range(cantidad_subconjuntos):
            subconjuntos.append(int(data[idx]))
            idx += 1
        cobertura_por_elemento[i] = subconjuntos

    instancia = {
        'num_elementos': num_elementos,
        'num_subconjuntos': num_subconjuntos,
        'costos': costos,
        'cobertura': cobertura_por_elemento
    }
    return instancia

def visualizar_instancia_scp(instancia):
    if not instancia:
        print("Error: Instancia vacía o nula.")
        return

    n = instancia['num_elementos']
    m = instancia['num_subconjuntos']
    costos = instancia['costos']
    cobertura = instancia['cobertura']

    costo_min = min(costos)
    costo_max = max(costos)
    costo_promedio = sum(costos) / m

    cobertura_promedio = sum(len(sub) for sub in cobertura.values()) / n

    print("="*40)
    print("ANÁLISIS DE INSTANCIA SCP")
    print("="*40)
    print(f"Total de Elementos (n):      {n}")
    print(f"Total de Subconjuntos (m):   {m}")
    print(f"Espacio Teórico (Fuerza B.): 2^{m}")
    print("-" * 40)
    print("MÉTRICAS DE COSTOS")
    print(f"Costo Mínimo:                {costo_min:.2f}")
    print(f"Costo Máximo:                {costo_max:.2f}")
    print(f"Costo Promedio:              {costo_promedio:.2f}")
    print("-" * 40)
    print("MÉTRICAS DE COBERTURA")
    print(f"Promedio de subconjuntos que")
    print(f"cubren cada elemento:        {cobertura_promedio:.2f}")
    print("="*40)

    
facil = '/content/01_facil.txt'
print("Iniciando la ejecución del análisis de instancia SCP...")
print(f"Buscando el archivo: '{facil}'")
instancia_cargada = leer_instancia_scp(facil)
visualizar_instancia_scp(instancia_cargada)

medio = '/content/02_medio.txt'
print("Iniciando la ejecución del análisis de instancia SCP...")
print(f"Buscando el archivo: '{medio}'")
instancia_cargada = leer_instancia_scp(medio)
visualizar_instancia_scp(instancia_cargada)

dificil = '/content/03_dificil.txt'
print("Iniciando la ejecución del análisis de instancia SCP...")
print(f"Buscando el archivo: '{dificil}'")
instancia_cargada = leer_instancia_scp(dificil)
visualizar_instancia_scp(instancia_cargada)
