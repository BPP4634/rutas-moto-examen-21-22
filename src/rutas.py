from collections import namedtuple, defaultdict
import csv
from parsers import *

Ruta = namedtuple('Ruta', 'ciudad_inicio, coordenada, fecha_ruta, km, gasolineras, dificultad, zona_descanso, vel_max, vel_min')
Coordenada = namedtuple('Coordenada', 'latitud, longitud')

def lee_rutas(archivo):
    result=[]
    with open(archivo,encoding='utf-8') as f:
        lector=csv.reader(f,delimiter=';')
        next(lector)
        for ciudad_inicio, coordenada, fecha_ruta, km, gasolineras, dificultad, zona_descanso, vel_max, vel_min in lector:
            ciudad_inicio = ciudad_inicio.strip()
            latitud,longitud = coordenada.split('/')
            coordenada = Coordenada(float(latitud),float(longitud))
            fecha_ruta = parsea_fecha(fecha_ruta)
            km = float(km)
            gasolineras = int(gasolineras)
            zona_descanso = zona_descanso == 'True'
            vel_max = int(vel_max)
            vel_min = int(vel_min)
            result.append(Ruta(ciudad_inicio, coordenada, fecha_ruta, km, gasolineras, dificultad, zona_descanso, vel_max, vel_min))
    return result

def acumular_kms_por_meses(rutas):
    d= agrupar_por_anyos(rutas)
    res = dict()
    for anyo, rutas_anyo in d.items():
        d_total_meses = acumular_por_meses(rutas_anyo)
        total_meses_anyo = [d_total_meses.get(mes, 0) for mes in range(1, 13)]
        res[anyo] = total_meses_anyo
    return res

def agrupar_por_anyos(rutas):
    res = defaultdict(list)
    for ruta in rutas:
        res[ruta.fecha_ruta.year].append(ruta)
    return res

def acumular_por_meses(rutas):
    res = defaultdict(float)
    for ruta in rutas:
       res[ruta.fecha_ruta.month] += ruta.km
    return res

def diferencias_kms_meses_anyo(rutas):
    result = defaultdict(list)
    años = acumular_kms_por_meses(rutas)
    for a in años:
        meses=años[a]
        aux=list(zip(meses[1:],meses))
        for mes1,mes2 in aux:
            result[a].append(mes1-mes2)
    return result

def top_rutas_lejanas(rutas,n,c,km_min=None):
    if km_min==None:
        km_min=0
    distancias=[]
    for r in rutas:
        if km_min<r.km:
            distancias.append(((distancia_Manhattan(c,r.coordenada)),r))
    distancias=(sorted(distancias,reverse=True))[:n]
    return [d[1] for d in distancias]

def distancia_Manhattan(coor1,coor2):
    return abs(coor1[0]-coor2[0])+abs(coor1[1]-coor2[1])

    # meses=defaultdict(float)
    # años=defaultdict(list)
    # result={}
    # for r in rutas:
    #     años[r.fecha_ruta.year]+=[r]
    # for a in años:
    #     for k in años[a]:
    #         meses[k.fecha_ruta.month]+=k.km
    #     aux = [meses.get(mes, 0) for mes in range(1, 13)]
    #     result[a]=aux
    #     meses.clear()
    # return result


    #     result[a]=list(meses.values())[:]
    #     meses.clear()
    # return result

    # def top_rutas_lejanas()

def ciudades_top_tiempo_dificultad(rutas,n=3):
    result={}
    dif=defaultdict(list)
    for r in rutas:
        if r.zona_descanso==True:
            t = r.km/r.vel_min
            dif[r.dificultad].append((t,r))
    for d in dif:
        rs=dif[d]
        result[d]=(sorted(rs,reverse=True))[:n]
        rr=result[d]
        result[d]=[r[1].ciudad_inicio for r in rr]
    return result
    # return {'alta':result[:n],'media':result[n:2*n],'baja':result[2*n:3*n]}
        


'''Dada una lista de tuplas de tipo Ruta y un valor entero n, obtener un diccionario que relacione
cada dificultad con las ciudades de inicio de las n rutas con zona de descanso que han tardado más
tiempo en hacerse, ordenadas de mayor a menor tiempo. Si suponemos que la velocidad de las rutas ha
sido siempre constante y con valor vel_min, podemos calcular el tiempo usando la fórmula t = km/vel_min.
El parámetro n tendrá un valor por defecto igual a 3.'''