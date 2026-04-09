from Taller1 import leer_instancia_scp
from taller2 import verificar_solucion, crear_solucion

def calcular_funcion_objetivo(vector_binario, instancia):
    """
    Calcula el valor de la funcion objetivo z(x) para un vector binario dado.

    El calculo corresponde a la suma de los costos ci de todos los
    subconjuntos Si cuya variable de decision xi vale 1, sin verificar
    la factibilidad de la solucion.

    Parameters
    ----------
    vector_binario : list of int
        Lista de longitud m con valores en {0, 1}.
    instancia : dict
        Diccionario retornado por leer_instancia_scp.

    Returns
    -------
    float
        Valor de la funcion objetivo z(x) = sum_{i: xi=1} ci.
    """
    costos = instancia['costos']
    return sum(costos[i] for i, xi in enumerate(vector_binario) if xi == 1)

def comparar_soluciones(solucion_a, solucion_b):
    """
    Compara dos soluciones del SCP segun validez y funcion objetivo.

    Jerarquia de criterios:
      1. Solucion valida > solucion invalida.
      2. Entre validas: menor costo_total es mejor.
      3. Entre invalidas: menor numero de elementos_no_cubiertos es mejor.
      4. Empate si ambas dimensiones son iguales.

    Precondicion: ambas soluciones deben haber sido procesadas por
    verificar_solucion (campo 'es_valida' distinto de None).

    Parameters
    ----------
    solucion_a : dict
        Diccionario creado por crear_solucion y verificado por
        verificar_solucion.
    solucion_b : dict
        Idem para la segunda solucion.

    Returns
    -------
    int
        -1 si solucion_a es estrictamente mejor que solucion_b.
         0 si ambas soluciones son equivalentes segun los criterios.
        +1 si solucion_b es estrictamente mejor que solucion_a.
    """
    valida_a = solucion_a['es_valida']
    valida_b = solucion_b['es_valida']

    # Criterio 1: validez
    if valida_a and not valida_b:
        return -1
    if valida_b and not valida_a:
        return 1

    # Criterio 2: entre validas, menor costo es mejor
    if valida_a and valida_b:
        costo_a = solucion_a['costo_total']
        costo_b = solucion_b['costo_total']
        if costo_a < costo_b:
            return -1
        if costo_b < costo_a:
            return 1
        return 0  # empate

    # Criterio 3: entre invalidas, menos elementos descubiertos es mejor
    nc_a = len(solucion_a['elementos_no_cubiertos'])
    nc_b = len(solucion_b['elementos_no_cubiertos'])
    if nc_a < nc_b:
        return -1
    if nc_b < nc_a:
        return 1
    return 0  # empate

def generar_combinaciones(m):
    """
    Generador que produce todos los vectores binarios de longitud m
    en orden lexicografico creciente (de 0...0 a 1...1).

    La implementacion recorre los enteros k en [0, 2^m) y extrae los
    m bits menos significativos usando desplazamiento de bits, evitando
    la conversion a cadena y la asignacion de listas intermedias.

    Parameters
    ----------
    m : int
        Longitud del vector binario; equivale al numero de subconjuntos
        de la instancia.

    Yields
    ------
    list of int
        Vector binario de longitud m con valores en {0, 1}.

    Notes
    -----
    El espacio de soluciones tiene cardinalidad 2^m. Para m > 25 el
    recorrido exhaustivo se vuelve computacionalmente inviable; en tales
    casos este generador debe usarse solo como componente de referencia
    sobre instancias reducidas, no como algoritmo de produccion.
    """
    total = 1 << m  # equivale a 2^m
    for k in range(total):
        vector = [(k >> i) & 1 for i in range(m)]
        yield vector

def visualizar_comparacion(solucion_a, solucion_b, nombre_a='A', nombre_b='B'):
    """
    Imprime un reporte estructurado comparando dos soluciones del SCP.

    Parameters
    ----------
    solucion_a : dict
        Primera solucion, verificada por verificar_solucion.
    solucion_b : dict
        Segunda solucion, verificada por verificar_solucion.
    nombre_a : str, optional
        Etiqueta identificadora de la primera solucion (defecto: 'A').
    nombre_b : str, optional
        Etiqueta identificadora de la segunda solucion (defecto: 'B').
    """
    resultado = comparar_soluciones(solucion_a, solucion_b)

    def estado(sol):
        return 'VALIDA' if sol['es_valida'] else 'INVALIDA'

    print()
    print('=' * 55)
    print('  COMPARACION DE SOLUCIONES SCP')
    print('=' * 55)
    print(f"  {'Atributo':<28} {'Sol. ' + nombre_a:>10}  {'Sol. ' + nombre_b:>10}")
    print('-' * 55)
    print(f"  {'Estado':<28} {estado(solucion_a):>10}  {estado(solucion_b):>10}")
    print(f"  {'Costo total':<28} {solucion_a['costo_total']:>10.2f}  "
          f"{solucion_b['costo_total']:>10.2f}")
    print(f"  {'Subconjuntos seleccionados':<28} "
          f"{solucion_a['num_seleccionados']:>10}  "
          f"{solucion_b['num_seleccionados']:>10}")
    print(f"  {'Elementos no cubiertos':<28} "
          f"{len(solucion_a['elementos_no_cubiertos']):>10}  "
          f"{len(solucion_b['elementos_no_cubiertos']):>10}")
    print('-' * 55)
    if resultado == -1:
        print(f'  Veredicto: la solucion {nombre_a} es MEJOR que {nombre_b}.')
    elif resultado == 1:
        print(f'  Veredicto: la solucion {nombre_b} es MEJOR que {nombre_a}.')
    else:
        print(f'  Veredicto: ambas soluciones son EQUIVALENTES.')
    print('=' * 55)
    print()

def ejecutar_pruebas_taller3():
    """
    Bateria de pruebas sobre la instancia de referencia del Taller 2.

    Casos de prueba:
    ----------------
    1. Funcion objetivo: valor correcto sobre solucion conocida.
    2. Comparacion valida vs. invalida: la valida siempre gana.
    3. Comparacion entre validas: gana la de menor costo.
    4. Comparacion entre invalidas: gana la de menos elementos
       descubiertos.
    5. Empate: dos soluciones identicas en validez y costo.
    6. Generador: produce exactamente 2^m vectores sin repeticion.
    """
    instancia = {
        'num_elementos': 5,
        'num_subconjuntos': 6,
        'costos': [3.0, 5.0, 2.0, 4.0, 6.0, 1.0],
        'cobertura': {
            1: [1, 5],
            2: [1, 2, 6],
            3: [2, 3, 5],
            4: [3, 4, 6],
            5: [4, 5],
        },
    }

    # --- Caso 1: funcion objetivo ---
    fo = calcular_funcion_objetivo([1, 0, 1, 1, 0, 0], instancia)
    assert fo == 9.0, f"Esperado 9.0, obtenido {fo}"

    fo_optima = calcular_funcion_objetivo([0, 0, 0, 0, 1, 1], instancia)
    assert fo_optima == 7.0, f"Esperado 7.0, obtenido {fo_optima}"

    # --- Caso 2: valida vs. invalida ---
    sol_valida   = verificar_solucion(crear_solucion([1, 0, 1, 1, 0, 0], instancia), instancia)
    sol_invalida = verificar_solucion(crear_solucion([0, 1, 0, 0, 0, 0], instancia), instancia)
    assert comparar_soluciones(sol_valida, sol_invalida) == -1
    assert comparar_soluciones(sol_invalida, sol_valida) == 1

    # --- Caso 3: entre validas, menor costo gana ---
    sol_optima = verificar_solucion(crear_solucion([0, 0, 0, 0, 1, 1], instancia), instancia)
    # sol_valida tiene costo 9, sol_optima tiene costo 7
    assert comparar_soluciones(sol_optima, sol_valida) == -1
    assert comparar_soluciones(sol_valida, sol_optima) == 1

    # --- Caso 4: entre invalidas, menos descubiertos gana ---
    # sol_invalida = {S2}: descubre elementos 1, 4, 5  (3 no cubiertos)
    # sol_peor    = {}:    descubre todos los elementos (5 no cubiertos)
    sol_peor = verificar_solucion(crear_solucion([0, 0, 0, 0, 0, 0], instancia), instancia)
    assert comparar_soluciones(sol_invalida, sol_peor) == -1

    # --- Caso 5: empate entre validas de igual costo ---
    sol_igual = verificar_solucion(crear_solucion([1, 0, 1, 1, 0, 0], instancia), instancia)
    assert comparar_soluciones(sol_valida, sol_igual) == 0

    # --- Caso 6: generador produce exactamente 2^m vectores distintos ---
    m = instancia['num_subconjuntos']
    vectores = list(generar_combinaciones(m))
    assert len(vectores) == 2**m, \
        f"Esperados {2**m} vectores, generados {len(vectores)}"
    # Verifica que no haya repeticiones convirtiendo cada vector a tupla
    assert len(set(tuple(v) for v in vectores)) == 2**m, \
        "El generador produjo vectores duplicados"

    print("Todas las pruebas del Taller 3 superadas exitosamente.")


if __name__ == '__main__':
    ejecutar_pruebas_taller3()
    # Para explorar la instancia SCP_simple1:
    instancia = leer_instancia_scp('SCP_simple1.txt')
    for vector in generar_combinaciones(instancia['num_subconjuntos']):
         solucion = crear_solucion(vector, instancia)
         solucion = verificar_solucion(solucion, instancia)
         print(solucion) # ESTO LO PUSE PARA VER Q PASABA (desastre)
        