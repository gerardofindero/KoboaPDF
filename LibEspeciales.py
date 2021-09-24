import pandas as pd

def textodeconsejos(equipo):
    texto=''
    refris=['refrigerador','congelador','bar','hielos']
    oficina=['impresora','fax']
    conteo =1
    checa =  any(item in equipo for item in oficina)
    if 'microondas' in equipo:
        texto = texto+' ' + 'Desconecta el microondas cuando no se use para ahorrar energía. <br /> '
    elif 'sensor' in equipo:
        texto = texto+' ' +  'Sigue usando tu sensor de movimiento para seguir ahorrando dinero. <br />'
    elif checa is True:
        texto = texto+' ' +  'Para equipos de oficina puedes mantener tus equipos apagados hasta ' \
                             'el momento en que los vayas a usar para ahorrar energía. <br />'

    else:
        if 'decodificador' in equipo:
            texto = texto + ' ' + 'Puedes apagar los decodificadores en los horarios en que no usas tu TV. ' \
                                  'Puedes encenderlo el domingo en la madrugada para recibir actualizaciones. <br />'
        if 'consola' in equipo:
            texto = texto+' ' + 'Lo mejor es mantener completamente apagada la consola, muchas veces se queda en modo espera. <br />'

        if 'regulador' in equipo:
            if 'bocinas' in equipo:
                texto = texto+' ' + 'Para los equipos de alta fidelidad NO te recomendamos quitar el regulador. <br />'

        check =  any(item in equipo for item in refris)
        if check is False:


            linkA='https://amzn.to/3sEMbJk'
            Address = 'Link de compra'
            LinkS = '<link href="' + str(linkA) + '"color="blue">' + Address + ' </link>'

            if conteo==1:
                texto = texto+' ' + 'Un timer inteligente te puede ayudar a ahorrar energía manteniendo tus ' \
                                    'dispositivos apagados mientras no los usas y encenderlos cuando lo necesites.' \
                                    ' Puedes programarlos para que se adecuen a tu estilo de vida' \
                                    + '<br /> '+  '<br /> '+LinkS + \
                                    '<br /> '+ ' Timer NINE <br /> <br />'
            if conteo==2:
                texto = texto+' ' + 'Un timer inteligente te sería util para reducir tu consumo de energía en esta zona'\
                                    + '<br /> '+  '<br /> '+LinkS + \
                                    '<br /> '+ ' Timer NINE <br /> <br />'
            if conteo==3:
                texto = texto+' ' + 'Te puedes apoyar de un timer inteligente ' \
                                    'para reducir el consumo de energía de tus ' \
                                    'dispositivos.' + '<br /> '+  '<br /> '+LinkS + \
                                    '<br /> '+ ' Timer NINE <br /> <br />'
            if conteo==4:
                texto = texto+' ' + 'Te recomendamos el uso de un timer inteligente para reducir ' \
                                    'el consumo de energía de tus' \
                                    'dispositivos.' + '<br /> '+  '<br /> '+LinkS + \
                                    '<br /> '+ ' Timer NINE <br /> <br />'



    return texto

def textodeequiposA(equipo,nota):
    texto=''
    print(equipo)
    if 'laptop' in equipo.lower():
        texto = texto+' ' + 'Para las laptops te recomendamos desconectarlas del enchufe cuando se terminen de usar. ' \
                            'Es importante para evitar que sigan consumiendo energía y así poder generar un mayor ahorro. <br /> '
    elif 'aspirador' in equipo.lower():
        texto = texto+' ' + 'La aspiradora se usó varios días a la semana, tienes buenos hábitos de uso, ' \
                            'recuerda desconectarla cuando no la estés usando. <br /> '

    elif 'cabello' in equipo.lower():
        texto = texto+' ' + 'Por su naturaleza este equipo es de alto consumo ya que su función es generar aire caliente. ' \
                            'Recuerda usar el equipo conscientemente para evitar que se convierta en un problema mayor. <br /> '

    elif 'calentador' in equipo.lower():
        texto = texto+' ' + 'Este equipo tiene un consumo elevado por su función de calentar el área, ' \
                            'te recomendamos usarlo de forma consciente para lograr un consumo aún más bajo.' \
                            ' Cierra puertas y ventanas cuando lo uses para evitar que entre el frío y se tenga que usar ' \
                            'por más tiempo. <br /> '

    elif 'horno' in equipo.lower():
        texto = texto+' ' + 'Este equipo es de alto consumo por lo que para poder evitar un gasto elevado ' \
                            'lo más eficiente es ser consciente de sus encendidos; apaga el equipo después de su uso.  <br />'

    else:
        texto=nota
    return texto

def textodeequiposV(equipo,nota):
    texto=''
    print(equipo)
    if 'laptop' in equipo.lower():
        texto = texto+' ' + 'Tienes un buen consumo usando tu laptop. Para las laptops te recomendamos desconectarlas ' \
                            'del enchufe cuando se terminen de usar. ' \
                            'Es importante para evitar que sigan consumiendo energía y así poder generar un mayor ahorro. <br /> '

    elif 'aspirador' in equipo.lower():
        texto = texto+' ' + 'La aspiradora se usó varios días a la semana, tienes buenos hábitos de uso, ' \
                            'recuerda desconectarla cuando no la estés usando. <br /> '

    elif 'cabello' in equipo.lower():
        texto = texto+' ' + 'El consumo por el uso de tu secadora de cabello es bueno. Por su naturaleza este equipo es de alto consumo ya que su función es generar aire caliente. ' \
                            'Recuerda usar el equipo conscientemente para evitar que se convierta en un problema mayor. <br /> '

    elif 'calentador' in equipo.lower():
        texto = texto+' ' + 'Tienes un buen uso de tu calentador. Este equipo tiene un consumo elevado por su función' \
                            ' de calentar el área, Te recomendamos' \
                            ' cerrar puertas y ventanas cuando lo uses para evitar que el caloe y se tenga que usar ' \
                            'por más tiempo. <br /> '

    elif 'horno' in equipo.lower():
        texto = texto+' ' + 'Tienes buenos hábitos con tu horno. Este equipo es de alto consumo por lo que para poder' \
                            ' evitar un gasto elevado ' \
                            'lo más eficiente es ser consciente de sus encendidos; apaga el equipo después de su uso.  <br />'

    elif 'belleza' in equipo.lower():
        texto = texto+' ' + 'Algunos de estos equipos de belleza son de alto consumo y se deben utilizar de forma ' \
                            'consciente. En tu caso el uso es muy eficiente, continúa con los buenos hábitos de uso' \
                            ' y no olvides desconectarlos cuando no se estén utilizando..  <br />'

    # elif 'sensor' in equipo.lower():
    #     texto = texto+' ' +  'Sigue usando tu sensor de movimiento para seguir ahorrando dinero. <br />'

    else:
        texto=nota
    return texto