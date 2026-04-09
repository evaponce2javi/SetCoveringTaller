from Taller1 import leer_instancia_scp
from taller2 import verificar_solucion, crear_solucion
from taller3 import generar_combinaciones, comparar_soluciones
import time

def busqueda_exhaustiva(instancia):
    """
    Resuelve una instancia del SCP mediante busqueda exhaustiva.

    Recorre la totalidad del espacio {0,1}^m, evalua cada vector binario
    como solucion candidata y retiene aquella factible de menor costo.
    Garantiza optimalidad global al precio de un tiempo de ejecucion
    exponencial en m.

    Parameters
    ----------
    instancia : dict
        Diccionario retornado por leer_instancia_scp.

    Returns
    -------
    dict
        Diccionario de resultados con las claves:
        - 'mejor_solucion'       : dict (solucion optima encontrada)
                                   o None si no existe solucion factible.
        - 'costo_optimo'         : float o None.
        - 'tiempo_segundos'      : float, tiempo de pared del recorrido.
        - 'soluciones_evaluadas' : int, total de vectores procesados
                                   (siempre igual a 2^m).
        - 'soluciones_factibles' : int, vectores que satisfacen todas
                                   las restricciones de cobertura.
    """
    m = instancia['num_subconjuntos']

    mejor_solucion       = None
    soluciones_evaluadas = 0
    soluciones_factibles = 0

    t_inicio = time.perf_counter()

    for vector in generar_combinaciones(m):
        soluciones_evaluadas += 1

        solucion = crear_solucion(vector, instancia)
        solucion = verificar_solucion(solucion, instancia)

        if solucion['es_valida']:
            soluciones_factibles += 1

            if (mejor_solucion is None or
                    comparar_soluciones(solucion, mejor_solucion) == -1):
                mejor_solucion = solucion

    t_fin = time.perf_counter()

    return {
        'mejor_solucion'        : mejor_solucion,
        'costo_optimo'          : (mejor_solucion['costo_total']
                                   if mejor_solucion else None),
        'tiempo_segundos'       : t_fin - t_inicio,
        'soluciones_evaluadas'  : soluciones_evaluadas,
        'soluciones_factibles'  : soluciones_factibles,
    }

def visualizar_resultado_exhaustiva(resultado, instancia):
    """
    Imprime un reporte completo de la busqueda exhaustiva.

    Parameters
    ----------
    resultado : dict
        Diccionario retornado por busqueda_exhaustiva.
    instancia : dict
        Diccionario retornado por leer_instancia_scp.
    """
    m   = instancia['num_subconjuntos']
    n   = instancia['num_elementos']
    ev  = resultado['soluciones_evaluadas']
    fac = resultado['soluciones_factibles']
    t   = resultado['tiempo_segundos']
    sol = resultado['mejor_solucion']

    densidad = fac / ev * 100 if ev > 0 else 0.0

    print()
    print('=' * 55)
    print('  RESULTADO: BUSQUEDA EXHAUSTIVA SCP')
    print('=' * 55)
    print(f"  Instancia           : n={n}, m={m}")
    print(f"  Espacio total       : 2^{m} = {2**m:,}")
    print('-' * 55)
    print(f"  Soluciones evaluadas: {ev:,}")
    print(f"  Soluciones factibles: {fac:,}  ({densidad:.2f}% del espacio)")
    print('-' * 55)
    print(f"  Tiempo de ejecucion : {t * 1000:.3f} ms")
    print(f"  Velocidad           : {ev / t:,.0f} sol/s")
    print('-' * 55)

    if sol is None:
        print('  Resultado : NO SE ENCONTRO SOLUCION FACTIBLE')
    else:
        sels  = sol['subconjuntos_seleccionados']
        costo = sol['costo_total']
        print(f"  Costo optimo        : {costo:.2f}")
        print(f"  Subconjuntos ({sol['num_seleccionados']:>3})  : "
              + ' '.join(f"S{i}" for i in sels))
    print('=' * 55)
    print()

def ejecutar_pruebas_taller4():
    """
    Bateria de pruebas del algoritmo de busqueda exhaustiva.

    Casos de prueba:
    ----------------
    1. Instancia de referencia (memoria): optimo {S5,S6}, costo = 7.
    2. SCP_simple1: optimo {S3,S4,S10}, costo = 6,
       1024 evaluadas, 820 factibles.
    3. SCP_simple2: optimo {S1,S7,S14}, costo = 3,
       1048576 evaluadas, 1005882 factibles.
    4. Reporte comparativo con factores de crecimiento.
    """
    # ----------------------------------------------------------
    # Caso 1: instancia de referencia en memoria
    # ----------------------------------------------------------
    instancia_ref = {
        'num_elementos'   : 5,
        'num_subconjuntos': 6,
        'costos'          : [3.0, 5.0, 2.0, 4.0, 6.0, 1.0],
        'cobertura'       : {
            1: [1, 5], 2: [1, 2, 6],
            3: [2, 3, 5], 4: [3, 4, 6], 5: [4, 5],
        },
    }
    res_ref = busqueda_exhaustiva(instancia_ref)
    assert res_ref['costo_optimo'] == 7.0
    assert res_ref['mejor_solucion']['es_valida'] == True
    assert set(res_ref['mejor_solucion']['subconjuntos_seleccionados']) \
        == {5, 6}
    assert res_ref['soluciones_evaluadas'] == 2**6    # 64

    # ----------------------------------------------------------
    # Caso 2: SCP_simple1
    # ----------------------------------------------------------
    inst_s1 = leer_instancia_scp('SCP_simple1.txt')
    res_s1  = busqueda_exhaustiva(inst_s1)
    assert res_s1['costo_optimo'] == 6.0
    assert res_s1['mejor_solucion']['es_valida'] == True
    assert set(res_s1['mejor_solucion']['subconjuntos_seleccionados']) \
        == {3, 4, 10}
    assert res_s1['soluciones_evaluadas'] == 2**10    # 1 024
    assert res_s1['soluciones_factibles'] == 820

    # ----------------------------------------------------------
    # Caso 3: SCP_simple2
    # ----------------------------------------------------------
    inst_s2 = leer_instancia_scp('SCP_simple2.txt')
    res_s2  = busqueda_exhaustiva(inst_s2)
    assert res_s2['costo_optimo'] == 3.0
    assert res_s2['mejor_solucion']['es_valida'] == True
    assert set(res_s2['mejor_solucion']['subconjuntos_seleccionados']) \
        == {1, 7, 14}
    assert res_s2['soluciones_evaluadas'] == 2**20    # 1 048 576
    assert res_s2['soluciones_factibles'] == 1_005_882

    # ----------------------------------------------------------
    # Reporte comparativo
    # ----------------------------------------------------------
    print("=== SCP_simple1 (n=20, m=10) ===")
    visualizar_resultado_exhaustiva(res_s1, inst_s1)

    print("=== SCP_simple2 (n=50, m=20) ===")
    visualizar_resultado_exhaustiva(res_s2, inst_s2)

    factor_espacio = res_s2['soluciones_evaluadas'] \
                   / res_s1['soluciones_evaluadas']
    factor_tiempo  = res_s2['tiempo_segundos'] \
                   / res_s1['tiempo_segundos']
    print(f"Factor crecimiento espacio : x{factor_espacio:,.0f}")
    print(f"Factor crecimiento tiempo  : x{factor_tiempo:,.0f}")

    print("\nTodas las pruebas del Taller 4 superadas exitosamente.")


if __name__ == '__main__':
    ejecutar_pruebas_taller4()