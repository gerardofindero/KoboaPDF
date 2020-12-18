import pandas as pd

def calentadores(Excel,Nocircuito, NomCircuito):


    Aparatos_C = pd.DataFrame(
        index=['Zona','Ambiente','Calefaccion' ,'Boiler Electrico','Boiler de Gas','Toallas', 'Calentador Otro','Notas'],
        columns=[ 'Marca','Consumo', 'Nominal','Existencia'])

    Circuito = Excel.loc[Nocircuito]
    Columnas = Excel.columns
    InfoEquipos = Columnas[Columnas.str.contains("calentador", case=False)]
    Equipos = Circuito[InfoEquipos]
    Tipo = Circuito.filter(regex='calentador_tipo_c_i')

    indx=0
    for i in Tipo:
        if i == 1:
            if indx == 1:
                InfoDeco = Circuito.filter(regex='ambiente')
                print(InfoDeco)
                Aparatos_C.loc['Ambiente', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                Aparatos_C.loc['Ambiente', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Ambiente', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Ambiente', 'Existencia'] = 1

            if indx == 2:
                InfoDeco = Circuito.filter(regex='calefaccion_fija')
                print(InfoDeco)
                Aparatos_C.loc['Calefaccion', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                Aparatos_C.loc['Calefaccion', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Calefaccion', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Calefaccion', 'Existencia'] = 1

            if indx == 3:
                InfoDeco = Circuito.filter(regex='boiler_luz')
                print(InfoDeco)
                Aparatos_C.loc['Boiler Electrico', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                Aparatos_C.loc['Boiler Electrico', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Boiler Electrico', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Boiler Electrico', 'Existencia'] = 1

            if indx == 4:
                InfoDeco = Circuito.filter(regex='boiler_gas')
                print(InfoDeco)
                Aparatos_C.loc['Boiler de Gas', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                Aparatos_C.loc['Boiler de Gas', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Boiler de Gas', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Boiler de Gas', 'Existencia'] = 1

            if indx == 5:
                InfoDeco = Circuito.filter(regex='toallas')
                print(InfoDeco)
                Aparatos_C.loc['Toallas', 'Zona'] = InfoDeco.filter(regex='zona')[0]
                Aparatos_C.loc['Toallas', 'Consumo'] = InfoDeco.filter(regex='consumo')[0]
                Aparatos_C.loc['Toallas', 'Marca'] = InfoDeco.filter(regex='marca')[0]
                Aparatos_C.loc['Toallas', 'Existencia'] = 1

            if indx == 6:
                InfoDeco = Equipos.filter(regex='otro')
                Aparatos_C.loc['Zona', 'Marca'] = InfoDeco.filter(regex='otro_zona_c_i')[0]
                Aparatos_C.loc['Calentador Otro', 'Consumo'] = InfoDeco.filter(regex='otro_consumo_c_i')[0]
                Aparatos_C.loc['Calentador Otro', 'Marca'] = InfoDeco.filter(regex='tipo_otro_c_i')[0]
                Aparatos_C.loc['Notas', 'Marca'] = InfoDeco.filter(regex='otro_notas_c_i')[0]
                Aparatos_C.loc['Calentador Otro', 'Existencia'] = 1
                Aparatos_C.loc['Notas', 'Existencia'] = 1
                Aparatos_C.loc['Zona', 'Existencia'] = 1
        indx = indx + 1

    Aparatos = Aparatos_C[Aparatos_C['Existencia'].notna()]
    Aparatos.reset_index()
    print(Aparatos)
    return Aparatos