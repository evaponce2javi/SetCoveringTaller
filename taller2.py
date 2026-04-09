from Taller1 import leer_instancia_scp

def crear_solucion(vector_binario, instancia):
    """
    Construye la estructura de datos que representa una solucion candidata
    al SCP a partir de un vector de decision binario.

    Parameters
    ----------
    vector_binario : list of int
        Lista de longitud m con valores en {0, 1}.
    instancia : dict
        Diccionario retornado por leer_instancia_scp.

    Returns
    -------
    dict
        Diccionario con claves: 'vector', 'subconjuntos_seleccionados',
        'num_seleccionados', 'costo_total', 'es_valida',
        'elementos_no_cubiertos'.

    Raises
    ------
    ValueError
        Si la longitud del vector no coincide con m, o si contiene
        valores fuera de {0, 1}.
    """
    m      = instancia['num_subconjuntos']
    costos = instancia['costos']

    # Validamos la dimension del vector antes de proceder
    if len(vector_binario) != m:
        raise ValueError(
            f"Dimension incorrecta: el vector tiene {len(vector_binario)} "
            f"elementos, pero la instancia requiere m = {m}."
        )

    # Validamos que todos los valores sean binarios
    if any(xi not in (0, 1) for xi in vector_binario):
        raise ValueError(
            "El vector contiene valores fuera del dominio {0, 1}."
        )

    # Identificamos los subconjuntos activos (indice base 1)
    subconjuntos_seleccionados = [
        i + 1 for i, xi in enumerate(vector_binario) if xi == 1
    ]

    # Calculamos el costo total de la seleccion
    costo_total = sum(
        costos[i] for i, xi in enumerate(vector_binario) if xi == 1
    )

    solucion = {
        'vector'                    : list(vector_binario),
        'subconjuntos_seleccionados': subconjuntos_seleccionados,
        'num_seleccionados'         : len(subconjuntos_seleccionados),
        'costo_total'               : costo_total,
        'es_valida'                 : None,   # se determina en verificar_solucion
        'elementos_no_cubiertos'    : [],     # se rellena en verificar_solucion
    }
    return solucion

def verificar_solucion(solucion, instancia):
    """
    Verifica si la solucion cumple la restriccion de cobertura del SCP.

    Para cada elemento j en {1,...,n} comprueba que al menos uno de los
    subconjuntos que lo cubren este incluido en la seleccion actual.
    Modifica y retorna el diccionario de solucion con los campos
    'es_valida' y 'elementos_no_cubiertos' actualizados.

    Parameters
    ----------
    solucion : dict
        Diccionario creado por crear_solucion.
    instancia : dict
        Diccionario retornado por leer_instancia_scp.

    Returns
    -------
    dict
        Diccionario de solucion con campos de validez actualizados.
    """
    cobertura = instancia['cobertura']
    n         = instancia['num_elementos']

    # Convertimos a conjunto para busqueda O(1) por elemento
    seleccionados = set(solucion['subconjuntos_seleccionados'])

    elementos_no_cubiertos = []

    # Recorremos cada elemento del universo y verificamos cobertura
    for j in range(1, n + 1):
        subconjuntos_que_cubren_j = set(cobertura[j])

        # El elemento j esta cubierto si la interseccion no es vacia
        if subconjuntos_que_cubren_j.isdisjoint(seleccionados):
            elementos_no_cubiertos.append(j)

    # Actualizamos la solucion con los resultados de la verificacion
    solucion['es_valida']              = (len(elementos_no_cubiertos) == 0)
    solucion['elementos_no_cubiertos'] = elementos_no_cubiertos

    return solucion

def leer_solucion(ruta_archivo, instancia):
    """
    Lee una solucion desde un archivo de texto, construye su estructura
    interna y verifica su factibilidad.

    Formato del archivo (.sol):
        Una unica linea con los indices (base 1) de los subconjuntos
        seleccionados, separados por espacios o saltos de linea.
        Ejemplo de contenido:   3 7 12 45 101

    Parameters
    ----------
    ruta_archivo : str
        Ruta al archivo de solucion.
    instancia : dict
        Diccionario retornado por leer_instancia_scp.

    Returns
    -------
    dict
        Diccionario de solucion completamente verificado.

    Raises
    ------
    ValueError
        Si algun indice esta fuera del rango [1, m].
    """
    m = instancia['num_subconjuntos']

    with open(ruta_archivo, 'r') as archivo:
        contenido = archivo.read().split()

    # Construimos el vector binario a partir de los indices leidos
    vector_binario = [0] * m

    for token in contenido:
        indice = int(token)
        if not (1 <= indice <= m):
            raise ValueError(
                f"Indice {indice} fuera de rango: los subconjuntos van "
                f"de 1 a {m}."
            )
        vector_binario[indice - 1] = 1    # conversion a indice base 0

    # Creamos la estructura y verificamos la factibilidad
    solucion = crear_solucion(vector_binario, instancia)
    solucion = verificar_solucion(solucion, instancia)

    return solucion

def visualizar_solucion(solucion, instancia):
    """
    Imprime un reporte detallado del estado de la solucion.

    Parameters
    ----------
    solucion : dict
        Diccionario creado por crear_solucion y procesado por
        verificar_solucion.
    instancia : dict
        Diccionario retornado por leer_instancia_scp.
    """
    if solucion['es_valida'] is None:
        print("Advertencia: la solucion no ha sido verificada aun.")

    m   = instancia['num_subconjuntos']
    n   = instancia['num_elementos']
    vec = solucion['vector']
    sel = solucion['subconjuntos_seleccionados']
    nc  = solucion['elementos_no_cubiertos']

    print()
    print("=" * 50)
    print("          REPORTE DE SOLUCION SCP")
    print("=" * 50)
    print(f"  Subconjuntos totales (m) : {m}")
    print(f"  Elementos del universo (n): {n}")
    print("-" * 50)

    # Mostramos el vector en bloques de 25 para legibilidad
    print("  VECTOR DE DECISION  (x_1 ... x_m)")
    BLOQUE = 25
    for inicio in range(0, m, BLOQUE):
        fin  = min(inicio + BLOQUE, m)
        fila = ''.join(str(xi) for xi in vec[inicio:fin])
        print(f"  [{inicio+1:>5} - {fin:>5}]  {fila}")

    print("-" * 50)
    print("  SUBCONJUNTOS SELECCIONADOS")
    print(f"  Cantidad : {solucion['num_seleccionados']} de {m}")

    # Mostramos los indices en grupos de 15 por linea
    GRUPO = 15
    for k in range(0, len(sel), GRUPO):
        grupo_str = '  '.join(f"{idx:>4}" for idx in sel[k:k+GRUPO])
        print(f"  {grupo_str}")

    print("-" * 50)
    print(f"  Costo Total : {solucion['costo_total']:.2f}")
    print("-" * 50)

    if solucion['es_valida']:
        print("  Estado : [OK]  SOLUCION VALIDA")
        print("           Todos los elementos estan cubiertos.")
    else:
        print("  Estado : [X]   SOLUCION INVALIDA")
        print(f"           Elementos no cubiertos : {len(nc)} de {n}")
        muestra = nc[:20]
        sufijo  = " ..." if len(nc) > 20 else ""
        print(f"           Indices : {muestra}{sufijo}")

    print("=" * 50)
    print()

def ejecutar_pruebas():
    """
    Bateria de pruebas sobre la instancia de referencia en memoria.
    """
    instancia = {
        'num_elementos'    : 5,
        'num_subconjuntos' : 6,
        'costos'           : [3.0, 5.0, 2.0, 4.0, 6.0, 1.0],
        'cobertura'        : {
            1: [1, 5],       # elemento 1 cubierto por S1 y S5
            2: [1, 2, 6],    # elemento 2 cubierto por S1, S2 y S6
            3: [2, 3, 5],    # elemento 3 cubierto por S2, S3 y S5
            4: [3, 4, 6],    # elemento 4 cubierto por S3, S4 y S6
            5: [4, 5],       # elemento 5 cubierto por S4 y S5
        },
    }

    # Caso 1: solucion valida no optima --- {S1, S3, S4}, costo = 9
    sol1 = crear_solucion([1, 0, 1, 1, 0, 0], instancia)
    sol1 = verificar_solucion(sol1, instancia)
    assert sol1['es_valida']   == True
    assert sol1['costo_total'] == 9.0

    # Caso 2: solucion optima --- {S5, S6}, costo = 7
    sol2 = crear_solucion([0, 0, 0, 0, 1, 1], instancia)
    sol2 = verificar_solucion(sol2, instancia)
    assert sol2['es_valida']   == True
    assert sol2['costo_total'] == 7.0

    # Caso 3: solucion invalida --- {S2} no cubre elementos 1, 4 y 5
    sol3 = crear_solucion([0, 1, 0, 0, 0, 0], instancia)
    sol3 = verificar_solucion(sol3, instancia)
    assert sol3['es_valida']                  == False
    assert set(sol3['elementos_no_cubiertos']) == {1, 4, 5}

    # Caso 4: solucion vacia --- ningun subconjunto seleccionado
    sol4 = crear_solucion([0, 0, 0, 0, 0, 0], instancia)
    sol4 = verificar_solucion(sol4, instancia)
    assert sol4['es_valida']   == False
    assert sol4['costo_total'] == 0.0

    # Caso 5: seleccion total --- todos los subconjuntos, costo = 21
    sol5 = crear_solucion([1, 1, 1, 1, 1, 1], instancia)
    sol5 = verificar_solucion(sol5, instancia)
    assert sol5['es_valida']   == True
    assert sol5['costo_total'] == 21.0

    print("Todas las pruebas superadas exitosamente.")


if __name__ == '__main__':
    ejecutar_pruebas()
    instancia = leer_instancia_scp('/content/01_facil.txt')
    solucion  = leer_solucion('/content/01_facil.txt', instancia)
    visualizar_solucion(solucion, instancia)