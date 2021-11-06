import pandas as pd

def calc_consumo(Aparatos):
    consumo = Aparatos['Standby'].copy()
    consumo.dropna(inplace=True)
    consumo.reset_index()
    print(consumo)
    Total = sum(consumo)
    return Total

def consumoEq(consumo):
    watts=0
    if pd.isna(consumo):
        consumo=0

    try:
        watts = round(float(consumo),1)
        #print('El consumo se tomó en watts al no venir especificado')

    except:
        consumo = consumo.lower()
        consumo= consumo.replace(' ','')
        consumo = consumo.replace('o','0')
        if "a" in consumo:
            ampes = float(consumo.replace('a', ' '))
            watts = ampes * 127
        if "w" in consumo:
            watts = float(consumo.replace('w', ' '))
        if consumo=='nm':
            watts = 0.00001

    return watts

def temperatura(temp):
    cel=0
    if pd.isna(temp):
        temp='NM'
    try:
        cel = round(float(temp))
        print('La temperatura se tomó en Celsius al no venir especificado')

    except:

        grados=temp.lower()

        if "°" in grados:
            grados= grados.replace('°',' ')


        if "f"  in grados:
            far = float(grados.replace('f',' '))
            cel= (far-32)*(5/9)

        if "c" in grados:
            cel = float(grados.replace('c', ' '))

        if 'nm'in grados:
            cel = 999
    return round(cel)

def Def_Tolerante(tolerancia):
    Tolerancia=False
    if pd.isna(tolerancia):
        Tolerancia=False
    else:
        if "127_volts" in tolerancia:
            Tolerancia=False

        if "100_110_a_220_240_volts" in tolerancia:
            Tolerancia=True

        if "no_haydatos" in tolerancia:
            Tolerancia=False

    return Tolerancia