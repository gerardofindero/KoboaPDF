import pandas as pd

def textodeconsejos(equipo):
    texto=''
    if 'microondas' in equipo:
        texto = texto+' ' + 'Desconecta el microondas cuando no se use para ahorrar energía. <br /> '
    elif 'sensor' in equipo:
        texto = texto+' ' +  'El sensor es suficiente para ahorrar energía. <br />'

    else:
        if 'decodificador' in equipo:
            texto = texto+' ' + 'El decodificador puede mantenerse apagado y prenderse el domingo en la madrugada para actualizarse. <br />'
        if 'consola' in equipo:
            texto = texto+' ' + 'Lo mejor es mantener completamente apagada la consola, muchas veces se queda en modo espera. <br />'

        linkA='https://amzn.to/3sEMbJk'
        Address = 'Link de compra'
        LinkS = '<link href="' + str(linkA) + '"color="blue">' + Address + ' </link>'

        texto = texto+' ' + 'Te puedes apoyar de un timer inteligente ' \
                            'para reducir el consumo de energía de tus ' \
                            'dispositivos y recuperar tu inversión en el corto ' \
                            'plazo.' + '<br /> '+  '<br /> '+LinkS + \
                '<br /> '+ ' Timer NINE <br /> <br />'

    return texto
