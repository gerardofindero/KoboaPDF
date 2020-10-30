def calc_consumo(Aparatos_C):
    watts = Aparatos_C['Consumo']
    watts.dropna(inplace= True)
    Amperes= watts[watts.str.contains('a')]
    AaW= Amperes.str.extract(r'(\d*\.?\d*)').astype(float)*127
    Watt = watts[watts.str.contains('w')]
    Numeros=Watt.str.extract(r'(\d*\.?\d*)').astype(float)
    SumaW = Numeros.sum()
    SumaA = AaW.sum()
    Total=float(SumaW+SumaA)
    return Total

def consumoEq(consumo):
    if "a" in consumo:
        watts = float(consumo.replace('a',' '))
        print("Amperes")
    if "w" in consumo:
        watts = float(consumo.replace('w', ' '))
        print("Watts")
    return watts