def calc_consumo(Aparatos):
    consumo = Aparatos['Standby'].copy()
    consumo.dropna(inplace=True)
    consumo.reset_index()
    Total = sum(consumo)
    return Total

def consumoEq(consumo):
    watts=0
    try:
        watts = round(float(consumo))
        print('El consumo se tomó en watts al no venir especificado')

    except:
        #print(consumo)
        consumo = consumo.lower()
        consumo= consumo.replace(' ','')
        consumo = consumo.replace('o','0')
        if "a" in consumo:
            ampes = float(consumo.replace('a', ' '))
            watts = ampes * 127
        if "w" in consumo:
            watts = float(consumo.replace('w', ' '))
        if consumo=='nm':
            watts = 0.01

    return watts

def temperatura(temp):
    cel=0
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
    return round(cel)