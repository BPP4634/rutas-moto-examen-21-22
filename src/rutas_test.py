from rutas import *
from datetime import date

def test_lee_rutas(rutas):
    print('Número de registros leídos:',len(rutas))
    print('Los cinco primeros son:',rutas[:5])
    print('El último es:',rutas[-1:])

def test_acumular_kms_por_meses(rutas):
    akpm=acumular_kms_por_meses(rutas)
    print('Los km acumulados por mes en cada año son:')
    for a,k in akpm.items():
        print(f'{a}: {k}')

def test_diferencias_kms_meses_anyo(rutas):
    dkma = diferencias_kms_meses_anyo(rutas)
    print('La diferencia de km acumulados entre los meses de cada año son:')
    for a,d in dkma.items():
        print(f'{a}: {d}')

def test_top_rutas_lejanas(rutas,n,c,km_min=None):
    trl = top_rutas_lejanas(rutas,n,c,km_min)
    print(f'Las {n} rutas más lejanas a las coordenadas {c} de km mínimo {km_min} son: {trl}')

def test_ciudades_top_tiempo_dificultad(rutas):
    cttd = ciudades_top_tiempo_dificultad(rutas)
    print('Las ciudades cuyas rutas tardan más tiempo en hacerse según la dificultad son:')
    for d,c in cttd.items():
        print(f'{d}: {c}')

def main():
    DATOS = lee_rutas("data/rutas_motos.csv")
    test_lee_rutas(DATOS)
    test_acumular_kms_por_meses(DATOS)
    test_diferencias_kms_meses_anyo(DATOS)
    test_top_rutas_lejanas(DATOS,2,(35.15, -8.76))
    test_ciudades_top_tiempo_dificultad(DATOS)

if '__main__' == __name__:
    main()