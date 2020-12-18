import datetime
import os
from datetime import datetime
import pandas as pd
import xlrd
from unidecode import unidecode
import logging

def Archivo(Cliente):
    Dic=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q']

    print(f"Comenzó el reporte de {Cliente}")
    fecha = datetime.now()
    mes = fecha.strftime("%B").capitalize()
    anho = fecha.strftime("%Y")
    carpeta_resultados = f"../../Datos de clientes/Clientes {anho}/{mes}/"
    #carpeta_resultados = f"../../Datos de clientes/Clientes {anho}/noviembre/"

    clientes = os.listdir(carpeta_resultados)
    booleanos = [Cliente.lower() in c.lower() for c in clientes]
    capeta_cliente=Cliente
    for idx, valor in enumerate(booleanos):
        if valor:
            carpeta_cliente = clientes[idx]
    carpeta_resultados = carpeta_resultados + f"{carpeta_cliente}/Resultados"

    cliente_ = Cliente.replace(' ', '_')
    archivo_resultados = f"{carpeta_resultados}/Resultados_{cliente_}.xlsx"
    Exx = pd.read_excel(archivo_resultados,sheet_name='Resumen')
    Exx.columns=Dic
    excel_resultados = xlrd.open_workbook(archivo_resultados)
    ##print(Exx)
    #print(Exx.loc[13,'A'])
    Exx.drop(Exx.index[:13],inplace=True)
    Exx.reset_index(inplace=True)
    Fin1=Exx
    print(Exx)

def buscar_columna(palabra, hoja):
    """ Busca en cada columna la ocurrencia de una palabra y devuelve el valor de la celda siguiente """
    count = 0
    while True:
        columna = [palabra in str(a) for a in hoja.col_values(count)]
        if any(columna):
            index = [i for i, x in enumerate(columna) if x][0] + 1
            return hoja.col_values(count)[index]
            break
        else:
            count += 1
        if count > 200:
            return 0
            break


def buscar_fila(palabra, hoja):
    """ Busca en cada fila la ocurrencia de una palabra y devuelve el valor de la celda siguiente """

    count = 0
    while True:
        fila = [palabra in str(a) for a in hoja.row_values(count)]
        if any(fila):
            index = [i for i, x in enumerate(fila) if x][0] + 1
            return hoja.row_values(count)[index]
            break
        else:
            count += 1
        if count > 200:
            return 0
            break

def buscar_palabra(palabra, hoja):
    """ Busca en cada fila la ocurrencia de una palabra y devuelve el valor de esa misma celda """

    count = 0
    while True:
        fila = [palabra in str(a) for a in hoja.row_values(count)]
        if any(fila):
            index = [i for i, x in enumerate(fila) if x][0]
            return hoja.row_values(count)[index]
            break
        else:
            count += 1
        if count > 200:
            return 0
            break


def varios(hoja):
    """ Se obtiene el numero de datos, tarifa, porcentaje de fugas, consumo y costo bimestral"""

    numero_datos = [a for a in hoja.row_values(0) if 'datos' in a][0].replace(',', '')
    numero_datos = [int(s) for s in numero_datos.split() if s.isdigit()][0]

    try:
        tarifa = round(buscar_fila('Tarifa', hoja), 2)
        tipo_tarifa = buscar_palabra('Tarifa', hoja)
        tipo_tarifa = tipo_tarifa.split("Tarifa ")[-1][:-1]

    except:
        tarifa = 5.2
        tipo_tarifa = "DAC"

    try:
        porcentaje_fugas = round(buscar_fila('Total de Fugas', hoja), 4)
    except:
        porcentaje_fugas = 0

    consumo_bimestral = int(buscar_columna('Consumo', hoja))
    costo_bimestral = int(buscar_columna('Costo', hoja))

    return numero_datos, tarifa, porcentaje_fugas, consumo_bimestral, costo_bimestral, tipo_tarifa


def aparatos(hoja):
    """ Se obtienen los aparatos y sus detalles. Luego se ordenan en un diccionario """
    count = 0
    while True:
        columna = ['Equipo' in str(a) for a in hoja.col_values(count)]
        if any(columna):
            col = count
            break
        else:
            count += 1
        if count > 80:
            col = 3
            break

    aparatos = [a for a in hoja.col_values(col)]
    inicio = aparatos.index('Equipo') + 1
    corte = aparatos.index('Sin Identificar')

    aparatos = list(filter(None, aparatos[inicio:corte]))
    carita = [int(e) for e in list(filter(None, [a for a in hoja.col_values(col - 2)][inicio:corte]))]
    porcentaje = [round(e, 3) for e in list(filter(None, [a for a in hoja.col_values(col + 1)][inicio:corte]))]
    consumo = [round(e, 3) for e in list(filter(None, [a for a in hoja.col_values(col + 2)][inicio:corte]))]
    costo = [int(round(e)) for e in list(filter(None, [a for a in hoja.col_values(col + 3)][inicio:corte]))]
    anual = [int(round(e)) for e in list(filter(None, [a for a in hoja.col_values(col + 4)][inicio:corte]))]
    notas = list(filter(None, [a for a in hoja.col_values(col + 8)][inicio:corte]))

    idx_fugas = [i for i, a in enumerate(aparatos) if 'fuga' not in a.lower()]

    aparatos = [aparatos[i] for i in idx_fugas]
    carita = [carita[i] for i in idx_fugas]
    porcentaje = [porcentaje[i] for i in idx_fugas]
    consumo = [consumo[i] for i in idx_fugas]
    costo = [costo[i] for i in idx_fugas]
    anual = [anual[i] for i in idx_fugas]
    notas = [notas[i] for i in idx_fugas]

    desciframiento = {}
    for i, a in enumerate(aparatos):
        desciframiento[a] = [a, carita[i], porcentaje[i], consumo[i], costo[i], anual[i], notas[i]]

    return desciframiento


def luces(hoja):
    """ Se obtiene el desgloce de luces """

    palabra_clave = 'Circuito:'
    count = 0
    while True:
        columna = [palabra_clave in str(a) for a in hoja.col_values(count)]
        if any(columna):
            col = count
            break
        else:
            count += 1
        if count > 80:
            col = 3
            break

    count = 0
    while True:
        fila = [palabra_clave in str(a) for a in hoja.row_values(count)]
        if any(fila):
            row = count
            break
        else:
            count += 1
        if count > 80:
            raise LookupError

    circuitos = [a for a in hoja.col_values(col)]
    inicio = circuitos.index(palabra_clave) + 1
    circuitos = list(filter(None, circuitos[inicio:]))
    descripcion = list(filter(None, [a for a in hoja.col_values(col + 1)][inicio:]))
    porcentaje = [round(e, 4) for e in list(filter(None, [a for a in hoja.col_values(col + 2)][inicio:]))]
    costo = [int(e) for e in list(filter(None, [a for a in hoja.col_values(col + 3)][inicio:]))]
    notas = list(filter(None, [a for a in hoja.col_values(col + 4)][inicio:]))

    if not circuitos:
        raise NameError
    else:
        detalles_luces = {}
        for i, c in enumerate(circuitos):
            detalles_luces[c] = [descripcion[i], porcentaje[i], costo[i], notas[i]]
        return detalles_luces


def fugas(hoja):
    """ Se obtienen las fugas y sus detalles. Luego se ordenan en un diccionario """

    count = 0
    while True:
        columna = ['donde' in unidecode(str(a)).lower() for a in hoja.col_values(count)]
        if any(columna):
            col = count
            break
        else:
            count += 1
        if count > 80:
            col = 3
            break

    lugar = [a for a in hoja.col_values(col)]
    try:
        inicio = lugar.index('Donde') + 1
    except:
        inicio = lugar.index('Dónde') + 1

    lugar = list(filter(None, lugar[inicio:]))
    aparato = list(filter(None, [a for a in hoja.col_values(col + 1)][inicio:]))
    potencia = [round(e, 1) for e in [a for a in hoja.col_values(col + 3)][inicio:] if e != '']
    consumo = [round(e, 1) for e in [a for a in hoja.col_values(col + 4)][inicio:] if e != '']
    atacable = list(filter(None, [a for a in hoja.col_values(col + 5)][inicio:]))
    notas = list(filter(None, [a for a in hoja.col_values(col + 6)][inicio:]))

    fugas = {}
    for i, a in enumerate(lugar):
        fugas[i] = [a, aparato[i], potencia[i], consumo[i], atacable[i], notas[i]]

    return fugas


def impacto(hoja):
    ahorro_paneles = int(buscar_columna('Ahorro por implementar:', hoja))
    co2 = int(buscar_columna('Impacto ambiental', hoja))
    arboles = round(co2*.015)
    nuevo_consumo = int(buscar_columna('Nuevo consumo', hoja))

    return ahorro_paneles, co2, arboles, nuevo_consumo


def consumo(hoja):
    """ Se obtiene el consumo del periodo de medición"""

    try:
        consumo_periodo = round(buscar_fila('Periodos al bimestre:', hoja),2)

    except:
        consumo_periodo = 0

    return consumo_periodo


def extractor(excel):
    """ Funcion que incorpora las demás y que será llamada por otros programas """

    hoja_desciframiento = excel.sheet_by_name('Desciframiento')
    hoja_detalles = excel.sheet_by_name('Detalles')
    hoja_ahorro = excel.sheet_by_name('Ahorro')

    numero_datos, tarifa, porcentaje_fugas, consumo_bimestral, costo_bimestral, tipo_tarifa = varios(hoja_desciframiento)
    desciframiento = aparatos(hoja_desciframiento)

    print(consumo(hoja_detalles))
    consumo_periodo = consumo_bimestral/635
    #(consumo(hoja_detalles))
    try:
        detalles_luces = luces(hoja_desciframiento)
    except LookupError as e:
        print(f'Error. No se pudo encontrar el desgloce de luces.')
        logging.warning(f'Error. No se pudo encontrar el desgloce de luces: {e}')
        detalles_luces = {}
    except NameError as e:
        print('No hay desgloce de luces.')
        logging.warning(f'No hay desgloce de luces: {e}')
        detalles_luces = {}
    except Exception as e:
        print('Error: ocurrió un error desconocido al buscar el desgloce de luces')
        logging.warning(f'Error: ocurrió un error desconocido al buscar el desgloce de luces: {e}')
        detalles_luces = {}

    ahorro_paneles, co2, arboles, nuevo_consumo = impacto(hoja_ahorro)

    return numero_datos, tarifa, porcentaje_fugas, consumo_bimestral, costo_bimestral, desciframiento, detalles_luces, \
           ahorro_paneles, co2, arboles, nuevo_consumo, tipo_tarifa, consumo_periodo


def extractor_fugas(excel):
    """ Extrae la infromación de la hoja de fugas """

    hoja_fugas = excel.sheet_by_name('Hoja de Fugas')

    atacables = buscar_fila('Porcentaje', hoja_fugas)

    try:
        fugas_dict = fugas(hoja_fugas)
    except Exception as e:
        logging.exception(e)

    return atacables, fugas_dict


def extractor_medidor(excel):
    """ Extrae la infromación para el veredicto de medidor, voltaje y robo """

    hoja = excel.sheet_by_name('Detalles')

    robo = buscar_fila("Robo?", hoja)
    revisar = buscar_fila("Revisar?", hoja)
    nivel = buscar_fila("Nivel:", hoja)

    return  robo, revisar, nivel


if __name__ == "__main__":
    archivo = 'Resultados_Leon_Wladislawosky.xlsx'
    hoja = xlrd.open_workbook(archivo).sheet_by_name('Desciframiento')

    numero_datos, tarifa, porcentaje_fugas, consumo_bimestral, costo_bimestral, desciframiento, detalles_luces, \
        ahorro_paneles, co2, arboles, nuevo_consumo = extractor(hoja)
