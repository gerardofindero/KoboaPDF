def calc_consumo(Aparatos):
    consumo = Aparatos['Consumo'].copy()
    consumo.dropna(inplace=True)
    consumo.reset_index()
    Total = sum(consumo)
    return Total

def consumoEq(consumo):
    consumo=consumo.lower()
    if "a"  in consumo:
        ampes = float(consumo.replace('a',' '))
        watts= ampes*127

    if "w" in consumo:
        watts = float(consumo.replace('w', ' '))

    return watts

def temperatura(temp):
    cel=0
    grados=temp.lower()
    if "f"  in grados:
        far = float(grados.replace('f',' '))
        cel= (far-32)*(5/9)

    if "c" in grados:
        cel = float(grados.replace('c', ' '))
    return round(cel)