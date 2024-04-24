import pandas as pd  # Importa la librería pandas para el manejo de datos en forma de DataFrame
import numpy as np  # Importa la librería numpy para operaciones matemáticas avanzadas

def leer_excel(archivo):
    df = pd.read_excel(archivo)  # Lee el archivo Excel y lo guarda en un DataFrame
    return df  # Retorna el DataFrame leído

def construir_red(df):
    actividades = {}  # Inicializa un diccionario para almacenar información sobre las actividades
    nodo_inicial = None  # Inicializa el nodo inicial como vacío
    nodos_sin_sucesores = set()  # Inicializa un conjunto para almacenar nodos sin sucesores

    for i, fila in df.iterrows():  # Itera sobre las filas del DataFrame
        actividad = fila['Actividad']  # Obtiene el nombre de la actividad
        descripcion = fila['Descripción']  # Obtiene la descripción
        precedentes = fila['Precedentes']  # Obtiene los precedentes
        duracion = fila['Duración']  # Obtiene la duración de la actividad

        if pd.isna(precedentes) or precedentes == '-':  # Comprueba que no hay precedentes
            nodo_inicial = actividad  # Asigna la actividad como nodo inicial
            precedentes = []  # Establece una lista vacía de precedentes
        else:
            precedentes = [int(p) for p in str(precedentes).split(',') if p]  # Convierte los precedentes a una lista de números enteros

        actividades[actividad] = {'descripcion': descripcion,  # Almacena la información de la actividad en el diccionario
                                  'precedentes': precedentes,
                                  'duracion': duracion,
                                  'sucesores': []}

        nodos_sin_sucesores.add(actividad)  # Agrega la actividad al conjunto de nodos sin sucesores

        for p in precedentes:  # Itera sobre los precedentes
            if p in actividades:  # Comprueba si el precedente existe en las actividades
                actividades[p]['sucesores'].append(actividad)  # Agrega la actividad como sucesor del precedente
                nodos_sin_sucesores.discard(p)  # Elimina el precedente del conjunto de nodos sin sucesores
            else:
                print(f"Advertencia: La actividad {p} no existe y se omitirá como precedente de {actividad}.")  # Advierte si no existe un precedente

    if len(nodos_sin_sucesores) != 1:  # Comprueba si hay exactamente un nodo final sin sucesores
        raise ValueError("Debe haber exactamente un nodo final sin sucesores.")  # Indica un error si la condicioón no se cumple

    nodo_final = next(iter(nodos_sin_sucesores))  # Obtiene el nodo final del conjunto de nodos sin sucesores

    return actividades, nodo_inicial, nodo_final  # Retorna la información de las actividades, el nodo inicial y el nodo final

def calcular_fechas(actividades, nodo_inicial, nodo_final):
    fechas_mas_proximas = {}  # Inicializa un diccionario para almacenar las fechas más próximas
    fechas_mas_lejanas = {}  # Inicializa un diccionario para almacenar las fechas más lejanas

    def calcular_fechas_rec(nodo, tiempo_acumulado):
        if nodo not in fechas_mas_proximas:  # Comprueba si el nodo no tiene fecha más próxima
            fechas_mas_proximas[nodo] = tiempo_acumulado  # Asigna el tiempo acumulado como la fecha más próxima
        else:
            fechas_mas_proximas[nodo] = max(fechas_mas_proximas[nodo], tiempo_acumulado)  # Actualiza la fecha más próxima si es necesario

        tiempo_acumulado += actividades[nodo]['duracion']  # Incrementa el tiempo acumulado con la duración de la actividad

        if nodo not in fechas_mas_lejanas:  # Comprueba si el nodo no tiene fecha más lejana
            fechas_mas_lejanas[nodo] = tiempo_acumulado  # Asigna el tiempo acumulado como la fecha más lejana
        else:
            fechas_mas_lejanas[nodo] = max(fechas_mas_lejanas[nodo], tiempo_acumulado)  # Actualiza la fecha más lejana si es necesario

        for sucesor in actividades[nodo]['sucesores']:  # Itera sobre los sucesores del nodo
            calcular_fechas_rec(sucesor, tiempo_acumulado)  # Llama recursivamente a la función para calcular las fechas de los sucesores

    calcular_fechas_rec(nodo_inicial, 0)  # Llama a la función interna para calcular las fechas desde el nodo inicial

    return fechas_mas_proximas, fechas_mas_lejanas  # Retorna las fechas más próximas y más lejanas para cada actividad

def generar_reporte(actividades, nodo_inicial, nodo_final, fechas_mas_proximas, fechas_mas_lejanas):
    tiempo_minimo = fechas_mas_lejanas[nodo_final]  # Obtiene el tiempo mínimo necesario para el proyecto
    actividades_criticas = []  # Inicializa una lista para almacenar las actividades críticas

    for actividad, info in actividades.items():  # Itera sobre las actividades
        if fechas_mas_proximas[actividad] == fechas_mas_lejanas[actividad] - info['duracion']:  # Comprueba si la actividad es crítica
            actividades_criticas.append(f"{actividad}. {info['descripcion']}")  # Agrega la actividad a la lista de actividades críticas

    with open('reporte.txt', 'w', encoding='utf-8') as f:  # Abre el archivo de reporte en modo escritura
        f.write(f"El tiempo necesario para la elaboración del proyecto es de {tiempo_minimo} semanas.\n\n")  # Escribe la duración del proyecto en el reporte
        f.write("Las actividades críticas son:\n\n")  # Escribe un encabezado para las actividades críticas en el reporte
        for actividad in actividades_criticas:  # Itera sobre las actividades críticas
            f.write(f"{actividad},\n")  # Escribe cada actividad crítica en el reporte

def main():  # Define la función principal del programa
    archivo_excel = 'Creacion_de_la_carrera_de_mat_ap.xlsx'  # Especifica el nombre del archivo Excel
    df = leer_excel(archivo_excel)  # Lee el archivo Excel y carga los datos en un DataFrame
    actividades, nodo_inicial, nodo_final = construir_red(df)  # Construye la red de actividades a partir del DataFrame
    fechas_mas_proximas, fechas_mas_lejanas = calcular_fechas(actividades, nodo_inicial, nodo_final)  # Calcula las fechas de inicio y fin de las actividades
    generar_reporte(actividades, nodo_inicial, nodo_final, fechas_mas_proximas, fechas_mas_lejanas)  # Genera un reporte

if __name__ == '_main_':  # Verifica si el script se está ejecutando directamente
    main()  # Llama a la función principal
