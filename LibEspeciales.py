import pandas as pd
from unidecode import unidecode

def leerLibreria():
    try:
        fugas   = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Otros equipos y fugas/Otros equipos y fugas.xlsx",
            sheet_name='Fugas')
        equipos = pd.read_excel(
            f"../../../Recomendaciones de eficiencia energetica/Librerias/Otros equipos y fugas/Otros equipos y fugas.xlsx",
            sheet_name='Equipos')
    except:
        fugas   = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Otros equipos y fugas/Otros equipos y fugas.xlsx",
            sheet_name='Fugas')
        equipos = pd.read_excel(
            f"D:/Findero Dropbox/Recomendaciones de eficiencia energetica/Librerias/Otros equipos y fugas/Otros equipos y fugas.xlsx",
            sheet_name='Equipos')
    fugas=fugas.set_index('Codigo')
    equipos=equipos.set_index('Codigo')
    return [fugas,equipos]




def textodeconsejos(equipo,equipo1,Consejos,conta):
    #fug,equi = leerLibreria()
    #print(fug)
    texto   = Consejos
    refris  = ['refrigerador','congelador','bar','hielos','regulador']
    oficina = ['impresora','fax']
    conteo  = 1
    checa   =  any(item in equipo for item in oficina)
    timer='Timer Inteligente de Steren'
    for i in range(len(equipo)):
        equipo[i]=unidecode(equipo[i])

    for i in range(len(equipo1)):
        equipo1[i]=unidecode(equipo1[i])


    linkA='https://www.amazon.com.mx/Steren-SHOME-100-Tomacorriente-Encendido-Inalámbrico/dp/B07JB9JKFB/ref=' \
          'sr_1_2?__mk_es_MX=ÅMÅŽÕÑ&crid=NSFMP6DX5PSK&keywords=smart+plug+steren&qid=1643742539&sprefix=smart+plug+steren%2Caps%2C166&sr=8-2'
    Address = 'Link de compra'
    LinkS = '<link href="' + str(linkA) + '"color="blue">' + Address + ' </link>'

    if conta>1:
        texto=texto.replace('{s}','s')
        texto=texto.replace('{es}','es')
    else:
        texto=texto.replace('{s}','')
        texto=texto.replace('{es}','')

    if 'sensor' in equipo:
        texto = texto+' ' +  'Sigue usando tu sensor de movimiento para seguir ahorrando dinero. <br />'
    elif checa is True:
        texto = texto+' ' +  'Para equipos de oficina puedes mantener tus equipos apagados hasta ' \
                             'el momento en que los vayas a usar para ahorrar energía. <br />'

    else:
        if 'microondas' in equipo:
            texto = texto+' ' + 'Desconecta el microondas cuando no se use para ahorrar energía. <br /> '

        if 'decodificador' in equipo:
            texto = texto + ' ' + 'Puedes apagar los decodificadores en los horarios en que no usas tu TV. ' \
                                  'Solo te recomendamos prenderlos la madrugada del domingo para recibir actualizaciones. <br />'
        if 'consola' in equipo:
            texto = texto+' ' + 'Lo mejor es mantener completamente apagada la consola, muchas veces se queda en modo espera. <br />'

        if 'bifasico' in equipo:
            texto = texto+' ' + 'Para recudir el gasto de tu equipo bifásico, puedes apagar las pastillas cuando no lo uses. <br />'
        if 'bifasico' in equipo1:
            texto = texto+' ' + 'Para recudir el gasto de tu equipo bifásico, puedes apagar las pastillas cuando no lo uses. <br />'

        if 'regulador' in equipo:
            if 'bocinas' in equipo:
                texto = texto+' ' + 'Para los equipos de alta fidelidad NO te recomendamos quitar el regulador. <br />'
            if len(equipo)>1:
                texto = texto+' ' + 'Un timer inteligente te puede ayudar a ahorrar energía manteniendo tus ' \
                                    'dispositivos apagados mientras no los usas.' \
                        + '<br /> '+  '<br /> '+LinkS + \
                        '<br /> '+ timer+' <br /> <br />'

        check =  any(item in equipo for item in refris)
        if check is False:

            if conteo==1:
                texto = texto+' ' + 'Un timer inteligente te puede ayudar a ahorrar energía manteniendo tus ' \
                                    'dispositivos apagados mientras no los usas.' \
                                    + '<br /> '+  '<br /> '+LinkS + \
                                    '<br /> '+ timer+' <br /> <br />'
            if conteo==2:
                texto = texto+' ' + 'Un timer inteligente te sería util para reducir tu consumo de energía en esta zona'\
                                    + '<br /> '+  '<br /> '+LinkS + \
                                    '<br /> '+ timer+' <br /> <br />'
            if conteo==3:
                texto = texto+' ' + 'Te puedes apoyar de un timer inteligente para reducir el consumo de energía de tus ' \
                                    'dispositivos.' + '<br /> '+  '<br /> '+LinkS + \
                                    '<br /> '+ timer+' <br /> <br />'
            if conteo==4:
                texto = texto+' ' + 'Te recomendamos el uso de un timer inteligente para reducir ' \
                                    'el consumo de energía de tus' \
                                    'dispositivos.' + '<br /> '+  '<br /> '+LinkS + \
                                    '<br /> '+ timer+'  <br /> <br />'
        # else:
        #     texto=Consejos



    return texto

def textodeequiposA(equipo,nota):
    texto=nota
    equipo=unidecode(equipo)
    if 'laptop' in equipo.lower():
        texto = texto+' ' + 'Para las laptops te recomendamos desconectarlas del enchufe cuando se terminen de usar. ' \
                            'Es importante para evitar que sigan consumiendo energía y así poder generar un mayor ahorro. <br /> '
    elif 'aspirador' in equipo.lower():
        texto = texto+' ' + 'La aspiradora se usó varios días a la seman. Su consumo es un poco más elevado que la mayoría de nuestros clientes., ' \
                            ' Recuerda desconectarla cuando no la estés usando. <br /> '
    elif 'cabello' in equipo.lower():
        texto = texto+' ' + 'Por su naturaleza este equipo es de alto consumo ya que su función es generar aire caliente. ' \
                            'Recuerda usar el equipo conscientemente para evitar que se convierta en un problema mayor. <br /> '

    elif 'pelo' in equipo.lower():
        texto = texto+' ' + 'Por su naturaleza este equipo es de alto consumo ya que su función es generar aire caliente. ' \
                            'Recuerda usar el equipo conscientemente para evitar que se convierta en un problema mayor. <br /> '

    # elif 'calentador' in equipo.lower():
    #     texto = texto+' ' + 'Este equipo tiene un consumo elevado por su función de calentar el área, ' \
    #                         'te recomendamos usarlo de forma consciente para lograr un consumo aún más bajo.' \
    #                         ' Cierra puertas y ventanas cuando lo uses para evitar que entre el frío y se tenga que usar ' \
    #                         'por más tiempo. <br /> '

    elif 'horno' in equipo.lower():
        texto = texto+' ' + 'Tu horno es de alto consumo por lo que para poder evitar un gasto elevado ' \
                            'lo más eficiente es ser consciente de sus encendidos; apaga el equipo después de su uso.  <br />'

    elif 'estufa' in equipo.lower():
        texto = texto+' ' + 'Tu estufa es de alto consumo por lo que para poder evitar un gasto elevado ' \
                        'lo más eficiente es ser consciente de sus encendidos; apaga el equipo después de su uso.  <br />'

    elif 'thermomix' in equipo.lower() or 'termomix' in equipo.lower():
        texto = texto+' ' + 'Tu equipo Thermomix es de alto consumo por lo que para poder evitar un gasto elevado ' \
                            'lo más eficiente es ser consciente de sus encendidos; apaga el equipo después de su uso.  <br />'


    elif 'lavajilla' in equipo.lower():
        texto = texto+' ' + 'Recuerda usar este tipo de equipos de forma moderada, ya que son equipos de alto consumo. <br />'

    else:
        texto=nota
    return texto

def textodeequiposV(equipo,nota):
    texto=nota
    equipo=unidecode(equipo)
    if 'laptop' in equipo.lower():
        texto = texto+' ' + 'Tienes un buen consumo usando tu laptop. Para las laptops te recomendamos desconectarlas del enchufe cuando se terminen de usar. ' \
                            'Es importante para evitar que sigan consumiendo energía y así poder generar un mayor ahorro. <br /> '
    elif 'computador' in equipo.lower():
        texto = texto+' ' + 'Tienes un buen consumo usando tu computadora. Recuerda apagar completamente tus equipos de computo ' \
                            'Es importante para evitar que sigan consumiendo energía y así poder generar un mayor ahorro. <br /> '

    elif 'bomba' \
       '' in equipo.lower():
        texto = texto+' ' + 'Revisamos el funcionamiento de tu bomba, No encontramos problemas, tiene un buen funcionamiento y un ' \
                            'consumo de energía eficiente. Recuerda darle mantenimiento de manera regular <br /> '

    elif 'aspirador' in equipo.lower():
        texto = texto+' ' + 'La aspiradora se usó varios días a la semana, tienes buenos hábitos de uso, ' \
                            'recuerda desconectarla cuando no la estés usando. <br /> '


    elif 'cabello' in equipo.lower():
        texto = texto+' ' + 'El consumo por el uso de tu secadora de cabello es bueno. Por su naturaleza este equipo es de alto consumo ya que su función es generar aire caliente. Recuerda usar el equipo conscientemente para evitar que se convierta en un problema mayor. <br /> '

    elif 'pelo' in equipo.lower():
        texto = texto+' ' + 'El consumo por el uso de tu secadora de cabello es bueno. Por su naturaleza este equipo es de alto consumo ya que su función es generar aire caliente. ' \
                            'Recuerda usar el equipo conscientemente para evitar que se convierta en un problema mayor. <br /> '

    # elif 'calentador' in equipo.lower():
    #     texto = texto+' ' + 'Tienes un buen uso de tu calentador. Este equipo tiene un consumo elevado por su función' \
    #                         ' de calentar el área, Te recomendamos' \
    #                         ' cerrar puertas y ventanas cuando lo uses para evitar que el caloe y se tenga que usar ' \
    #                         'por más tiempo. <br /> '

    elif 'horno' in equipo.lower():
        texto = texto+' ' + 'Tienes buenos hábitos con tu horno. Este equipo es de alto consumo por lo que para poder' \
                            ' evitar un gasto elevado ' \
                            'lo más eficiente es ser consciente de sus encendidos; apaga el equipo después de su uso.  <br />'

    elif 'estufa' in equipo.lower():
        texto = texto+' ' + 'El consumo de tu estufa es bueno. Recuerda que es un equipo potente úsalo con moderación.' \
                            '; apaga el equipo después de su uso.  <br />'

    elif 'thermomix' in equipo.lower() or 'termomix' in equipo.lower():
        texto = texto+' ' + 'Tu consumo es bueno. Recuerda que tu equipo es de alto consumo usalo con moderación' \
                            '; apaga el equipo después de su uso.  <br />'



    elif 'belleza' in equipo.lower():
        texto = texto+' ' + 'Algunos de estos equipos de belleza son de alto consumo y se deben utilizar de forma ' \
                            'consciente. En tu caso el uso es muy eficiente, continúa con los buenos hábitos de uso' \
                            ' y no olvides desconectarlos cuando no se estén utilizando.  <br />'

    elif 'cargador' in equipo.lower() or 'cargadores' in equipo.lower():
        texto = texto+' ' + 'Los cargadores de dispositivos electrónicos no representan un impacto fuerte en tu recibo. ' \
                            'No olvides desconectarlos una vez que tu dispositivo haya alcanzado la carga completa para ' \
                            'incrementar aún más tu ahorro.  <br />'

    else:
        texto=nota
    print(texto)
    return texto

def noatac(equipo,todo):
    equipo=str(equipo)
    todo=str(todo)
    if 'refrigerador' in equipo:
        Consejos='Lamentablemente es difícil reducir el consumo de standby de un refrigerador sin reemplazarlo'
    elif 'calentador' in equipo:
        Consejos='Lamentablemente no es posible eliminar el consumo de este equipo sin reemplazarlo '
    elif 'alexa' in todo:
        Consejos= 'Es difícil desconectar los dispositivos inteligentes ya que afectan a tu comodidad. Si no llegas a usarlos te recomendamos desconectarlos. <br /> '
    elif 'lutron' in todo:
        Consejos= 'Es difícil desconectar los dispositivos inteligentes ya que afectan a tu comodidad. ' \
                            'Si no llegas a usarlos te recomendamos desconectarlos. <br /> '
    elif 'modem' in todo or 'repetidor' in todo:
        Consejos='En los equipos de comunicación no recomendamos tomar acción o desconectarlos, ' \
                 'debido a que interfieren con tu confort'
    else:
        Consejos='En los equipos de comunicación y seguridad no recomendamos tomar acción o desconectarlos, ' \
                 'debido a que pueden afectar tanto tu confort como tu seguridad'
    return Consejos