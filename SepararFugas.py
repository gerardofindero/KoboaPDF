import pandas as pd
from Correciones import Lugar


def separar_fugas(Equip):
    texto="H"
    try:
        texto=Equip.loc[['Notas', 'Marca']]
        Equip.drop(index='Notas',inplace=True)
    except:
        print(" ")
    Equipos = pd.DataFrame(columns=['Codigo','Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto','Notas'])
    Fugas   = pd.DataFrame(columns=['Codigo','Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto','Atacable','Notas'])
    Aparatos=Equip.copy()
    Fuga = Equip.copy()
    Aparatos.fillna({'Nominal': 0}, inplace=True)
    Fuga.fillna({'Standby': 0}, inplace=True)
    #Aparatos.fillna('x', inplace=True)
    #Fuga.fillna('x', inplace=True)
    Aparatos.dropna(subset=['Nominal'], inplace=True)
    Aparatos = Aparatos[Aparatos.Nominal != 0]
    Aparatos.reset_index(inplace=True)
    Equipos['Codigo'] = Aparatos['CodigoN']
    Equipos['Equipo'] = Aparatos['index']+' '+Aparatos['Marca']
    Equipos['Potencia Kobo'] = Aparatos['Nominal']
    Equipos['Lugar']  = Aparatos['Zona']
    Equipos['Ubicacion'] = 'C' + Aparatos['Circuito'].apply(str) + ' ' + Aparatos['Tablero'].apply(str)
    Equipos['Texto']  = Aparatos['index']+' '+Aparatos['Marca'].apply(str) +  ' '+Aparatos['Notas']
    Equipos['Notas']  =  Aparatos['Notas']
    Equipos['Equipo'] = Equipos['Equipo'].str.replace('Otro', "", regex=True)
    Equipos['Claves'] = Aparatos['Clave']

    Fuga.dropna(subset=['Standby'], inplace=True)
    Fuga = Fuga[Fuga.Standby != 0]
    Fuga.reset_index(inplace=True)
    Fugas['Codigo'] = Fuga['CodigoS']
    Fugas['Equipo']    = 'Fuga '+Fuga['index'] + ' ' + Fuga['Marca'].apply(str)
    Fugas['Potencia Kobo']   = Fuga['Standby']
    Fugas['Lugar']     = Fuga['Zona']
    Fugas['Ubicacion'] = 'C' + Fuga['Circuito'].apply(str) + ' ' + Fuga['Tablero'].apply(str)
    Fugas['Texto']     = Fuga['index'] + ' ' + Fuga['Marca'].apply(str)+  ' '+Fuga['Notas']
    Fugas['Notas']     = Fuga['Notas']
    Fugas['Atacable']  = Fuga['Atacable']
    Fugas['Equipo']    = Fugas['Equipo'].str.replace('Otro', "", regex=True)

    return Equipos,Fugas

def separar_fugasBB(Equip):
    texto="H"

    try:
        texto=Equip.loc[['Notas', 'Marca']]
        Equip.drop(index='Notas',inplace=True)
    except:
        print(" ")
    Equipos = pd.DataFrame(columns=['Codigo','Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto','Notas'])
    Fugas   = pd.DataFrame(columns=['Codigo','Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto','Atacable','Notas'])
    Aparatos=Equip.copy()
    Fuga = Equip.copy()
    Aparatos.fillna({'Nominal': 0}, inplace=True)
    Fuga.fillna({'Standby': 0}, inplace=True)
    Aparatos.dropna(subset=['Nominal'], inplace=True)
    Aparatos = Aparatos[Aparatos.Nominal != 0]
    Aparatos.reset_index(inplace=True)
    Equipos['Codigo'] =  Aparatos['CodigoN']
    Equipos['Equipo'] =  Aparatos['index']
    Equipos['Potencia Kobo'] = Aparatos['Nominal']
    Equipos['Lugar']  =  Aparatos['Zona']
    Equipos['Ubicacion'] = 'C' + Aparatos['Circuito'].apply(str) + ' ' + Aparatos['Tablero'].apply(str)
    Equipos['Texto']  =  Aparatos['index']+' '+Aparatos['Marca'].apply(str) +  ' '+Aparatos['Notas']
    Equipos['Notas']  =  Aparatos['Notas']
    Equipos['Equipo'] =  Equipos['Equipo'].str.replace('Otro', "", regex=True)
    Equipos['Claves'] =  Aparatos['Clave']

    Fuga.dropna(subset=['Standby'], inplace=True)
    Fuga = Fuga[Fuga.Standby != 0]
    Fuga.reset_index(inplace=True)
    Fugas['Codigo'] = Fuga['CodigoS']
    Fugas['Equipo']    = 'Fuga '+Fuga['index']
    Fugas['Potencia Kobo']   = Fuga['Standby']
    Fugas['Lugar']     = Fuga['Zona']
    Fugas['Ubicacion'] = 'C' + Fuga['Circuito'].apply(str) + ' ' + Fuga['Tablero'].apply(str)
    Fugas['Texto']     = Fuga['index'] + ' ' + Fuga['Marca'].apply(str)+  ' '+Fuga['Notas']
    Fugas['Notas']     = Fuga['Notas']
    Fugas['Atacable']  = Fuga['Atacable']
    Fugas['Equipo']    = Fugas['Equipo'].str.replace('Otro', "", regex=True)


    return Equipos,Fugas



def separar_fugasC(Equip):
    texto="H"
    try:
        texto=Equip.loc[['Notas', 'Marca']]
        Equip.drop(index='Notas',inplace=True)
    except:
        print(" ")

    Equipos = pd.DataFrame(columns=['Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto','Notas'])
    Fugas   = pd.DataFrame(columns=['Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto','Atacable','Notas'])
    Aparatos=Equip.copy()
    Fuga = Equip.copy()

    Aparatos['Marca'].fillna('!', inplace=True)
    Fuga['Marca'].fillna('!', inplace=True)
    Aparatos.fillna({'Nominal': 0}, inplace=True)
    Fuga.fillna({'Standby': 0}, inplace=True)
    Aparatos.dropna(subset=['Nominal'], inplace=True)
    Aparatos = Aparatos[Aparatos.Nominal != 0]
    Aparatos.reset_index(inplace=True)
    Equipos['Codigo'] = Aparatos['CodigoN']
    Equipos['Equipo'] = Aparatos['index']+' '+Aparatos['Marca'].apply(str)
    Equipos['Potencia Kobo'] = Aparatos['Nominal']
    Equipos['Lugar'] = Aparatos['Zona']
    Equipos['Ubicacion'] = 'C' + Aparatos['Circuito'].apply(str) + ' ' + Aparatos['Tablero'].apply(str)
    Equipos['Texto'] =Aparatos['index']+' '+Aparatos['Marca'].apply(str) +  ', '+Aparatos['Notas']
    Equipos['Notas'] = Aparatos['Notas']
    Equipos['Equipo'] = Equipos['Equipo'].replace('!', "",regex=True)
    Equipos['Texto'] = Equipos['Texto'].replace('!', "",regex=True)
    Equipos['Equipo'] = Equipos['Equipo'].str.replace('Otro', "",regex=True)
    Equipos['Claves'] = Aparatos['Clave']


    Fuga.dropna(subset=['Standby'], inplace=True)
    Fuga = Fuga[Fuga.Standby != 0]
    Fuga.reset_index(inplace=True)
    Fugas['Codigo'] = Fuga['CodigoS']
    Fugas['Equipo']    = 'Fuga '+Fuga['index'] + ' ' + Fuga['Marca'].apply(str)
    Fugas['Potencia Kobo']   = Fuga['Standby']
    Fugas['Lugar']     = Fuga['Zona']
    Fugas['Ubicacion'] = 'C' + Fuga['Circuito'].apply(str) + ' ' + Fuga['Tablero'].apply(str)
    Fugas['Texto']     = Fuga['index'] + ' ' + Fuga['Marca'].apply(str)+  ' '+Fuga['Notas']
    Fugas['Notas']     = Fuga['Notas']
    Fugas['Atacable']  = Fuga['Atacable']
    Fugas['Equipo']    = Fugas['Equipo'].replace('!', "" ,regex=True)
    Fugas['Texto']     = Fugas['Texto'].replace('!', "",regex=True)
    Fugas['Equipo']    = Fugas['Equipo'].str.replace('Otro', "",regex=True)



    return Equipos,Fugas


def separar_fugasE(Equip):
    texto="H"
    try:
        texto=Equip.loc[['Notas', 'Marca']]
        Equip.drop(index='Notas',inplace=True)
    except:
        print(" ")

    Equipos = pd.DataFrame(columns=['Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto','Notas'])
    Fugas   = pd.DataFrame(columns=['Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto','Atacable','Notas'])
    Aparatos=Equip.copy()
    Fuga = Equip.copy()

    Aparatos.fillna({'Nominal': 0}, inplace=True)
    Fuga.fillna({'Standby': 0}, inplace=True)
    Aparatos['Marca'].fillna('!', inplace=True)
    Fuga['Marca'].fillna('!', inplace=True)
    Aparatos.dropna(subset=['Nominal'], inplace=True)
    Aparatos = Aparatos[Aparatos.Nominal != 0]
    Aparatos.reset_index(inplace=True)
    Equipos['Codigo'] = Aparatos['CodigoN']
    Equipos['Equipo'] = Aparatos['Equipo']+' '+Aparatos['Marca']
    Equipos['Potencia Kobo'] = Aparatos['Nominal']
    Equipos['Lugar'] = Aparatos['Zona']
    Equipos['Ubicacion'] = 'C' + Aparatos['Circuito'].apply(str) + ' ' + Aparatos['Tablero'].apply(str)
    Equipos['Texto'] = Aparatos['Equipo']+' '+ Aparatos['Marca'].apply(str) +  ', '+Aparatos['Notas']
    Equipos['Notas'] = Aparatos['Notas']
    Equipos['Equipo'] = Equipos['Equipo'].str.replace('!', "", regex=True)
    Equipos['Equipo'] = Equipos['Equipo'].str.replace('Otro', "", regex=True)
    Equipos['Claves'] = Aparatos['Clave']

    Fuga.dropna(subset=['Standby'], inplace=True)
    Fuga = Fuga[Fuga.Standby != 0]
    Fuga.reset_index(inplace=True)
    Fugas['Codigo'] = Fuga['CodigoS']
    Fugas['Equipo']    = 'Fuga '+Fuga['Equipo'] + ' ' + Fuga['Marca'].apply(str)
    Fugas['Potencia Kobo']   = Fuga['Standby']
    Fugas['Lugar']     = Fuga['Zona']
    Fugas['Ubicacion'] = 'C' + Fuga['Circuito'].apply(str) + ' ' + Fuga['Tablero'].apply(str)
    Fugas['Texto']     = Fuga['index'] + ' ' + Fuga['Marca'].apply(str)+  ' '+Fuga['Notas']
    Fugas['Atacable'] = Fuga['Atacable']
    Fugas['Notas'] = Fuga['Notas']
    Fugas['Equipo'] = Fugas['Equipo'].str.replace('!', "", regex=True)
    Fugas['Equipo'] = Fugas['Equipo'].str.replace('Otro', "", regex=True)
    return Equipos,Fugas


def separar_fugasTV(Equipo):

    Equipos = pd.DataFrame(columns=['Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto','Notas','Claves'])
    Fugas   = pd.DataFrame(columns=['Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto','Atacable','Notas'])

    Aparatos=Equipo.copy()
    Fuga = Equipo.copy()

    #Aparatos.drop(index='Notas', inplace=True)
    Aparatos['Nominal'].fillna(0, inplace=True)
    Aparatos.fillna('X', inplace=True)
    Fuga['Standby'].fillna(0, inplace=True)


    #Aparatos['Texto'].fillna(Zona, inplace=True)
    Aparatos.dropna(subset=['Nominal'], inplace=True)
    Aparatos = Aparatos[Aparatos.Nominal != 0]
    Aparatos.reset_index(inplace=True)
    Aparatos['Pulgadas']=Aparatos['Pulgadas']
    Equipos['Codigo'] = Aparatos['CodigoN']
    Equipos['index'] = Aparatos['index'].str.replace('1', "", regex=True)
    try:
        Equipos['Equipo']        = Aparatos['index']+' '+Aparatos['Marca']+' '+Aparatos['Pulgadas'].apply(int).apply(str)+"''"
    except:
        Equipos['Equipo']        = Aparatos['index']+' '+Aparatos['Marca']
    Equipos['Potencia Kobo'] = Aparatos['Nominal']
    Equipos['Lugar']         = Aparatos['Zona']
    Equipos['Ubicacion']     = 'C' + Aparatos['Circuito'].apply(str) + ' ' + Aparatos['Tablero'].apply(str)
    Equipos['Texto'] = Aparatos['index']+' '+Aparatos['Marca']+' '+ Aparatos['Pulgadas'].apply(str) +'´´ '+Aparatos['Nota']
    Equipos['Notas'] = Aparatos['Notas']
    Equipos['Equipo'] = Equipos['Equipo'].str.replace('Equipoextra', "", regex=True)
    Equipos['Equipo'] = Equipos['Equipo'].str.replace('Equipoextra2', "", regex=True)
    Equipos['Equipo'] = Equipos['Equipo'].str.replace('Equipoextra3', "", regex=True)
    Equipos['Claves'] = Aparatos['Clave']



    Fuga.dropna(subset=['Standby'], inplace=True)
    Fuga = Fuga[Fuga.Standby != 0]
    Fuga.reset_index(inplace=True)
    Fugas['Codigo'] = Fuga['CodigoS']
    Fuga['index'] = Fuga['index'].str.replace('1', "",regex=True)
    Fugas['Equipo']          = 'Fuga '+Fuga['index'] + ' ' + Fuga['Marca'].apply(str)
    Fugas['Potencia Kobo']   = Fuga['Standby'].apply(str)
    Fugas['Lugar']           = Fuga['Zona']
    Fugas['Ubicacion']       = 'C' + Fuga['Circuito'].apply(str) + ' ' + Fuga['Tablero'].apply(str)
    Fugas['Texto'] = Fuga['Nota']
    Fugas['Notas'] = Fuga['Nota']
    Fugas['Atacable'] = Fuga['Atacable']
    Fugas['Equipo'] = Fugas['Equipo'].str.replace('Equipoextra', "", regex=True)
    Fugas['Equipo'] = Fugas['Equipo'].str.replace('Equipoextra2', "", regex=True)
    Fugas['Equipo'] = Fugas['Equipo'].str.replace('Equipoextra3', "", regex=True)

    #Fugas['Potencia Kobo'] = Fugas['Potencia Kobo'].str.replace('0.001', "NM", regex=True)
    #Aparatos.drop(Aparatos[Aparatos.Equipos.str.contains('Nota')].index, inplace=True)

    Equipos.dropna(subset=['Equipo'],inplace=True)
    Equipos=Equipos[~Equipos.Equipo.str.contains('Nota')]
    Equipos = Equipos[~Equipos.Equipo.str.contains('Lugar')]
    Equipos = Equipos[~Equipos.Equipo.str.contains('Equipo Ahorro')]

    return Equipos,Fugas


def separar_fugasA(Equip):
    texto="H"
    try:
        texto=Equip.loc[['Notas', 'Marca']]
        Equip.drop(index='Notas',inplace=True)
    except:
        print(" ")

    Equipos = pd.DataFrame(columns=['Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto','Notas'])
    Fugas   = pd.DataFrame(columns=['Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto','Atacable','Notas'])
    Aparatos=Equip.copy()
    Fuga = Equip.copy()


    Aparatos.fillna({'Nominal': 0}, inplace=True)
    Fuga.fillna({'Standby': 0}, inplace=True)
    Aparatos.dropna(subset=['Nominal'], inplace=True)
    Aparatos = Aparatos[Aparatos.Nominal != 0]
    Aparatos.reset_index(inplace=True)

    Equipos['Codigo'] = Aparatos['CodigoN']
    Equipos['Equipo'] = 'Aire Acondicionado tipo '+ Aparatos['Tecnologia']
    Equipos['Potencia Kobo'] = Aparatos['Nominal']
    Equipos['Lugar'] = Aparatos['Zona'] + ' en el' + Aparatos['Ubicacion']
    Equipos['Ubicacion'] = 'C' + Aparatos['Circuito'].apply(str) + ' ' + Aparatos['Tablero'].apply(str)
    Equipos['Texto'] = Aparatos['Notas']
    Equipos['Notas'] = Aparatos['Notas']
    Equipos['Claves'] = Aparatos['Clave']


    Fuga.dropna(subset=['Standby'], inplace=True)
    Fuga = Fuga[Fuga.Standby != 0]
    Fuga.reset_index(inplace=True)
    Fugas['Codigo'] = Fuga['CodigoS']
    Fugas['Equipo']    = 'Aire Acondicionado tipo '+ Fuga['Tecnologia']
    Fugas['Potencia Kobo']   = Fuga['Standby']
    Fugas['Lugar']     = Fuga['Zona']  + ' en el' + Fuga['Ubicacion']
    Fugas['Ubicacion'] = 'C' + Fuga['Circuito'].apply(str) + ' ' + Fuga['Tablero'].apply(str)
    Fugas['Texto']     = Fuga['Notas']
    Fugas['Notas']     = Fuga['Notas']
    Fugas['Atacable']  = Fuga['Atacable']


    return Equipos,Fugas



def separar_fugasR(Equipo):

    Equipos = pd.DataFrame(columns=['Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto', 'Notas','Claves'])
    Fugas   = pd.DataFrame(columns=['Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto','Atacable','Notas'])
    Aparatos = Equipo.copy()
    Aparatos['Nominal']=Aparatos['Pot Compresor']
    Fuga = Equipo.copy()
    Aparatos.dropna(subset=['Nominal'], inplace=True)
    Aparatos = Aparatos[Aparatos.Nominal != 0]
    Aparatos.reset_index(inplace=True)
    Equipos['Codigo'] = Aparatos['CodigoN']

    Equipos['Equipo']        = Aparatos['index'] + ' ' + Aparatos['Marca']
    Equipos['Potencia Kobo'] = Aparatos['Pot Compresor']
    Equipos['Lugar']         = Aparatos['Zona']
    Equipos['Ubicacion']     = 'C' + Aparatos['Circuito'].apply(str) + ' ' + Aparatos['Tablero'].apply(str)
    Equipos['Texto']         = Aparatos['Notas']
    Equipos['Notas'] = Aparatos['Notas']
    Equipos['Claves'] = Aparatos['Claves']

    Fuga.dropna(subset=['Standby'], inplace=True)
    Fuga = Fuga[Fuga.Standby != 0]
    Fuga.reset_index(inplace=True)
    Fugas['Codigo']         = Fuga['CodigoS']
    Fugas['Equipo']         = 'Fuga '+Fuga['index'] + ' ' + Fuga['Marca']
    Fugas['Potencia Kobo']  = Fuga['Standby']
    Fugas['Lugar']          = Fuga['Zona']
    Fugas['Ubicacion']      = 'C' + Fuga['Circuito'].apply(str) + ' ' + Fuga['Tablero'].apply(str)
    Fugas['Texto']          = Fuga['Notas']
    Fugas['Notas']          = Fuga['Notas']
    Fugas['Atacable']       = 'Si'

    return Equipos, Fugas


def separar_fugasCal(Equip):
    texto="H"
    try:
        texto=Equip.loc[['Notas', 'Marca']]
        Equip.drop(index='Notas',inplace=True)
    except:    #Aparatos.fillna('x', inplace=True)
    #Fuga.fillna('x', inplace=True)
        print(" ")

    Equipos = pd.DataFrame(columns=['Codigo','Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto','Notas'])
    Fugas   = pd.DataFrame(columns=['Codigo','Ubicacion', 'Equipo', 'Lugar', 'Potencia Kobo', 'Texto','Atacable','Notas'])
    Aparatos=Equip.copy()
    Fuga = Equip.copy()
    Aparatos.fillna({'Nominal': 0}, inplace=True)
    Fuga.fillna({'Standby': 0}, inplace=True)
    Aparatos.dropna(subset=['Nominal'], inplace=True)
    Aparatos = Aparatos[Aparatos.Nominal != 0]
    Aparatos.reset_index(inplace=True)
    Equipos['Codigo'] = Aparatos['CodigoN']
    Equipos['Equipo'] = 'Calentador '+Aparatos['index']+' '+Aparatos['Marca']
    Equipos['Potencia Kobo'] = Aparatos['Nominal']
    Equipos['Lugar']  = Aparatos['Zona']
    Equipos['Ubicacion'] = 'C' + Aparatos['Circuito'].apply(str) + ' ' + Aparatos['Tablero'].apply(str)
    Equipos['Texto']  = Aparatos['index']+' '+Aparatos['Marca'].apply(str) +  ' '+Aparatos['Notas']
    Equipos['Notas']  = Aparatos['Notas']
    Equipos['Equipo'] = Equipos['Equipo'].str.replace('Otro', "", regex=True)
    Equipos['Claves'] = Aparatos['Clave']

    Fuga.dropna(subset=['Standby'], inplace=True)
    Fuga = Fuga[Fuga.Standby != 0]
    Fuga.reset_index(inplace=True)
    Fugas['Codigo']    = Fuga['CodigoS']
    Fugas['Equipo']    = 'Fuga '+Fuga['index'] + ' ' + Fuga['Marca'].apply(str)
    Fugas['Potencia Kobo']   = Fuga['Standby']
    Fugas['Lugar']     = Fuga['Zona']
    Fugas['Ubicacion'] = 'C' + Fuga['Circuito'].apply(str) + ' ' + Fuga['Tablero'].apply(str)
    Fugas['Texto']     = Fuga['index'] + ' ' + Fuga['Marca'].apply(str)+  ' '+Fuga['Notas']
    Fugas['Texto']     = Fuga['Notas']
    Fugas['Atacable']  = Fuga['Atacable']
    Fugas['Equipo']    = Fugas['Equipo'].str.replace('Otro', "", regex=True)

    return Equipos,Fugas

