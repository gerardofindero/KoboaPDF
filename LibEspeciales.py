import pandas as pd
from unidecode import unidecode
import random
from libreriaReguladores_ import armarTxt_NAtac,armarTxt_Atac

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




def textodeconsejos(clave,voltaje):
    #fug,equi = leerLibreria()
    contador=0
    textoCompleto=''
    Conta=''
    claveSR=clave[~clave.D.str.contains("Regulador")]
    sumaP=claveSR['K'].sum()
    conteo=random.randrange(4)
    for index, claves in clave.iterrows():
        equipo     = claves[3]
        Standby =  claves[9]
        textoE      = claves[13]
        clave      = claves[16]
        refris  = ['refrigerador','congelador','bar','hielos','regulador']
        oficina = ['impresora','fax']
        checa   =  any(item in equipo for item in oficina)
        timer='Timer Inteligente'
        equipo=unidecode(equipo.lower())
        linkA="https://www.amazon.com.mx/Sengled-compatibles-requerido-electrodom%E9sticos-certificado/dp/B08FJ5LHSN/ref="\
              "sr_1_1?__mk_es_M=%C5M%C5%99%D5%D1&crid=38UNBNY6KWNQW&dchild=1&keywords=sengled+enchufe&qid=1633391443&sprefix=Sengled+enchu%2Chi%2C190&sr=8-1"

        Address = 'Link de compra'
        LinkS = '<link href="' + str(linkA) + '"color="blue">' + Address + ' </link>'

        if clave== 'AMN':
            if not 'AMN/' in Conta:
                textoCompleto = textoCompleto + '-'+textoE +'<br /> <br />'
                Conta=Conta+'AMN/ '
        else:
            if 'sensor' in equipo:
                if not 'SR' in Conta:
                    texto =  '-Sigue usando tu sensor de movimiento para seguir ahorrando dinero. <br /><br />'
                    Conta=Conta+'SR/ '
                    textoCompleto = textoCompleto + texto

            if checa is True:
                if not 'TC' in Conta:
                    texto =  '-Para equipos de oficina puedes mantener tus equipos apagados hasta ' \
                                         'el momento en que los vayas a usar para ahorrar energía.<br /> <br />'
                    Conta=Conta+'TC/ '
                    textoCompleto = textoCompleto + texto


            if 'microondas' in equipo:
                if not 'MC' in Conta:
                    texto = '-Desconecta el microondas cuando no se use para ahorrar energía. <br /><br /> '
                    Conta=Conta+'MC/ '
                    textoCompleto = textoCompleto + texto

            if 'decodificador' in equipo:
                if not 'DC' in Conta:
                    texto = '-Puedes apagar los decodificadores en los horarios en que no usas tu TV.  <br /><br />'
                    Conta=Conta+'DC/'
                    textoCompleto = textoCompleto + texto

            if 'consola' in equipo:
                if not 'CN' in Conta:
                    texto = '-Lo mejor es mantener completamente apagada la consola, muchas veces se queda en modo espera. <br /><br />'
                    Conta=Conta+'CN/'
                    textoCompleto = textoCompleto + texto

            if 'recirculacion' in equipo:
                if not 'BRC' in Conta:
                    texto = texto = '-Un timer inteligente te ayudará a ahorrar energía manteniendo tu bomba apagada ' \
                                    'mientras no la usas.'  +  '<br /> '+LinkS + '<br /> '+ timer+' <br /> <br />'
                    Conta=Conta+'BRC / '
                    textoCompleto = textoCompleto + texto

            elif 'regulador' in equipo:
                if not 'RG/' in Conta:
                    try:
                        textoCompleto = textoCompleto + '-' + armarTxt_Atac(clave,Standby,voltaje)
                        Conta = Conta + 'RG/ '
                        contador = contador + 1
                    except:
                        textoCompleto = textoCompleto + '-' + 'Ya que el voltaje en tu vivienda es estable, puedes quitar ' \
                                                              'tu regulador y sustituirlo por un protector de picos para' \
                                                              ' mantener tus equipos portegidos contra picos de voltaje <br /> <br />'
                        Conta = Conta + 'RG/ '
                        contador = contador + 1


            elif 'bifasico' in equipo:
                if not 'BF' in Conta:
                    texto = '-Para reducir el gasto de tu equipo bifásico, puedes apagar las pastillas cuando no lo uses. ' \
                            'Otra alternativa es colocar pastillas inteligentes y de esa manera programar los horarios de encendido y apagado' \
                            ' pero depende de la instalación eléctrica y de una buena señal de internet <br /><br />'

                    Conta=Conta+'BF/'
                    textoCompleto = textoCompleto + texto

            elif 'bifasica' in equipo:
                if not 'BF' in Conta:
                    texto = '-Para reducir el gasto de tu equipo bifásico, puedes apagar las pastillas cuando no lo uses. ' \
                            'Otra alternativa es colocar pastillas inteligentes y de esa manera programar los horarios de encendido y apagado' \
                            ' pero depende de la instalación eléctrica y de una buena señal de internet <br /><br />'

                    Conta=Conta+'BF/'
                    textoCompleto = textoCompleto + texto

            elif 'trifasico' in equipo:
                if not 'TF' in Conta:
                    texto = '-Para reducir el gasto de tu equipo trifásico, puedes apagar las pastillas cuando no lo uses. ' \
                            'Otra alternativa es colocar pastillas inteligentes y de esa manera programar los horarios de encendido y apagado' \
                            ' pero depende de la instalación eléctrica y de una buena señal de internet <br /><br />'
                    Conta=Conta+'TF/'
                    textoCompleto = textoCompleto + texto

            elif 'trifasica' in equipo:
                if not 'TF' in Conta:
                    texto = '-Para reducir el gasto de tu equipo trifásico, puedes apagar las pastillas cuando no lo uses. ' \
                            'Otra alternativa es colocar pastillas inteligentes y de esa manera programar los horarios de encendido y apagado' \
                            ' pero depende de la instalación eléctrica y de una buena señal de internet <br /><br />'

                    Conta=Conta+'TF/'
                    textoCompleto = textoCompleto + texto

            elif 'aires' in equipo:
                if not 'AR' in Conta:
                    texto = '-Para reducir el gasto de tu aire acondicionado, puedes apagar las pastillas cuando no lo uses. <br /><br />'
                    Conta=Conta+'AR/'
                    textoCompleto = textoCompleto + texto

            elif 'secadora' in equipo:
                if not 'regulador' in equipo:
                    if not 'SC' in Conta:
                        texto = '-Para reducir el gasto de tu secadora, lo más sencillo es desconectarla cuando no lo uses. ' \
                                'Si lo deseas puedes colocar un timer inteligente para prenderla y apagarla desde tu celular. Te dejamos el link para comprarlo.  '
                        texto = texto + LinkS +'  <br /> <br />'

                        Conta=Conta+'SC/'
                        textoCompleto = textoCompleto + texto

            elif 'lavadora' in equipo:
                if not 'regulador' in equipo:
                    if not 'LV' in Conta:
                        texto = '-Te recomendamos desconectar tu lavadora cuando no lo uses para reducir el gasto constante de tu lavadora, ' \
                                ', pero si lo deseas puedes colocar un timer inteligente para prenderla y apagarla desde tu celular. Te dejamos el link para comprarlo.  '
                        texto = texto+ LinkS + '  <br /> <br />'
                        Conta=Conta+'LV/'
                        textoCompleto = textoCompleto + texto

            elif 'hielos' in equipo:
                if not 'regulador' in equipo:
                    if not 'LV' in Conta:
                        texto = '-Te recomendamos desconectar tu máquina de hielos cuando no lo uses para reducir este gasto, con prender tu equipo un par de horas antes es suficiente para tener hielo suficiente, ' \
                                'si lo deseas puedes colocar un timer inteligente para prenderla y apagarla desde tu celular. Te dejamos el link para comprarlo.  '
                        texto = texto+ LinkS + '  <br /> <br />'
                        Conta=Conta+'LV/'
                        textoCompleto = textoCompleto + texto

            elif 'cafetera' in equipo:
                if not 'LP' in Conta:
                    texto =  '-Desconecta tu cafetera de la corriente mientras no la uses para ahorrar energía. <br /><br />'
                    Conta=Conta+'LP/'
                    textoCompleto = textoCompleto + texto

            elif 'laptop' in equipo:
                if not 'LP' in Conta:
                    texto =  '-Desconecta tu laptop de la corriente mientras no la uses para ahorrar energía. <br /><br />'
                    Conta=Conta+'LP/'
                    textoCompleto = textoCompleto + texto

            elif 'computadora' in equipo:
                if not 'PC' in Conta:
                    texto =  '-Desconecta completamente tu equipo de cómputo mientras no lo uses para ahorrar energía. <br /><br />'
                    Conta=Conta+'PC/'
                    textoCompleto = textoCompleto + texto

            elif 'puerta' in equipo or 'porton' in equipo:
                if not 'PT' in Conta:
                    texto =  '-Por tu comodidad no te recomendamos realizar ninguna acción a tu puerta eléctrica. <br /><br />'
                    Conta=Conta+'PT/'
                    textoCompleto = textoCompleto + texto

            elif 'bocinas' in equipo:
                if not 'BC' in Conta:
                    Conta=Conta+'BC/'
                    if 'regulador' in equipo:
                        texto = '-Para los equipos de alta fidelidad NO te recomendamos quitar el regulador. <br /><br />'
                    if not 'NA' in Conta:
                        texto =  '-Un timer inteligente te puede ayudar a ahorrar energía manteniendo tus ' \
                                            'dispositivos apagados mientras no los usas.' \
                                + '<br /> '+LinkS + \
                                '<br /> '+ timer+' <br /> <br />'
                        Conta=Conta+'NA/'
                        textoCompleto = textoCompleto + texto
            else:
                check =  any(item in equipo for item in refris)
                # doblecheck =all(item in excepciones for item in equipo)
                if not check:
                    if sumaP<=4:
                        texto = '-Para tu '+equipo  +', al ser un gasto pequeño, te recomendamos desconectar tu equipo mientras no se encuentre en uso. <br /> <br />'
                        textoCompleto = textoCompleto + texto
                    else:
                        if not 'NA' in Conta:
                            if conteo==1:
                                texto = '-Un timer inteligente te puede ayudar a ahorrar energía manteniendo tus ' \
                                                    'dispositivos apagados mientras no los usas.' \
                                                    +  '<br /> '+LinkS + \
                                                    '<br /> '+ timer+' <br /> <br />'

                            if conteo==2:
                                texto =  '-Un timer inteligente te sería util para reducir tu consumo de energía en esta zona'\
                                                    + '<br /> '+LinkS + \
                                                    '<br /> '+ timer+' <br /> <br />'
                            if conteo==3:
                                texto = '-Te puedes apoyar de un timer inteligente para reducir el consumo de energía de tus ' \
                                                    'dispositivos.' + '<br /> '+LinkS + \
                                                    '<br /> '+ timer+' <br /> <br />'
                            if conteo==0:
                                texto =  '-Te recomendamos el uso de un timer inteligente para reducir ' \
                                                    'el consumo de energía de tus' \
                                                    'dispositivos.' + '<br /> '+ LinkS + \
                                                    '<br /> '+ timer+'  <br /> <br />'

                            Conta = Conta+'NA / '

                            textoCompleto = textoCompleto + texto


    textoCompleto = textoCompleto.replace('X ','')

    if contador>1:
        textoCompleto=textoCompleto.replace('{s}','s')
        textoCompleto=textoCompleto.replace('{es}','es')
    else:
        textoCompleto=textoCompleto.replace('{s}','')
        textoCompleto=textoCompleto.replace('{es}','')

    return textoCompleto





def textodeequiposR(equipo,nota):

    texto=''
    equipo=unidecode(equipo)

    linkB = "https://www.amazon.com.mx/FEDBNET-Interruptor-interruptor-inteligente-recuperaci%C3%B3n/dp/B08CK4GMCQ/" \
            "ref=pd_sbs_1/142-4121552-0782331?pd_rd_w=3flMS&pf_rd_p=dee331ab-905c-48f4-8a5e-81c36ada64cb&pf_rd_" \
            "r=HCM55GJCJNZN4EH0REH9&pd_rd_r=63f711cc-ffc5-42b3-badf-5369610a49fa&pd_rd_wg=QSz35&pd_rd_i=B08CK4GMCQ&psc=1"
    Address = 'Link de compra'
    LinkTimer = '<link href="' + str(linkB) + '"color="blue">' + Address + ' </link>'

    if 'laptop' in equipo.lower():
        texto = 'Para las laptops te recomendamos desconectarlas del enchufe cuando se terminen de usar. ' \
                            'Es importante para evitar que sigan consumiendo energía y así poder generar un mayor ahorro. <br /> '



    elif 'horno' in equipo.lower() or 'hornito' in equipo.lower():
        texto = 'Tu horno es de alto consumo por lo que para poder evitar un gasto elevado ' \
                            'lo más eficiente es ser consciente de sus encendidos; apaga el equipo después de su uso. ' \
                            'Puedes cambiar a un horno de gas para ahorrar en energía electrica, también puedes usar tu estufa para ' \
                            'cocinar algunos de los alimentos y de esa forma ahorrar en energía eléctrica  <br />'

    elif 'parrila' in equipo.lower():
        texto =  'Una parrilla elétrica es un equipo de alta potencia por lo que para poder evitar un gasto elevado ' \
                            'lo más eficiente es ser consciente de sus encendidos, úsala con moderación. ' \
                            'Puedes usar tu estufa de gas para cocinar algunos de los alimentos y de esa forma ahorrar en energía eléctrica  <br />'


    elif 'estufa' in equipo.lower():
        texto =  'Tu estufa es de alto consumo por lo que para poder evitar un gasto elevado ' \
                            'lo más eficiente es ser consciente de sus encendidos; apaga el equipo después de su uso.' \
                            'Puedes considerar cambiar a una estufa de gas para disminuir tu consumo de energía electrica.  <br />'

    elif 'thermomix' in equipo.lower() or 'termomix' in equipo.lower():
        texto = 'Tu equipo Thermomix es de alto consumo por lo que para poder evitar un gasto elevado ' \
                        'lo más eficiente es ser consciente de sus encendidos; apaga el equipo después de su uso.  <br />'

    elif 'calentador' in equipo.lower():
        texto =  'Este equipo tiene un consumo elevado por su función de calentar el área, ' \
                            'te recomendamos usarlo de forma consciente para lograr un consumo aún más bajo.' \
                            ' Cierra puertas y ventanas cuando lo uses para evitar que entre el frío y se tenga que usar ' \
                            'por más tiempo. <br /> '
    elif 'boiler' in equipo.lower():
        texto = 'Este equipo tiene un consumo elevado por su función de calentar el agua, ' \
                            'te recomendamos apagarlo completamente mientras no se vaya a usar y prenderlo 20 minutos antes de bañarse. ' \
                            'Te puedes ayudar de un sistema de pastillas inteligentes para apagar y prender el boiler de forma remota desde tu celular ' \
                            ' <br /><br /> Te dejamos un link donde puedes comprarla. <br />'+LinkTimer

    elif 'calefaccion' in equipo.lower():
        texto = 'Este equipo tiene un consumo elevado por su función de calentar el área, ' \
                            'te recomendamos usarlo de forma consciente para lograr un consumo aún más bajo.' \
                            ' Cierra puertas y ventanas cuando lo uses para evitar que entre el frío y se tenga que usar ' \
                            'por más tiempo. En tiempos de calor este consumo disminuirá drasticamente. <br /> '


    elif 'gravitacion' in equipo.lower():
        texto = 'La bomba tiene un consumo completamente fuera de lo normal en comparacion con otros de nuestros clientes. ' \
                            'Esto se debe que se prende por periodos largos de tiempo durante el día. ' \
                            'No encontramos porblemas con los controles ni encontramos fugas <br /> '

    elif 'biodigestor' in equipo.lower():
        texto = 'Nuestra recomendación es que al ser un equipo que se mantiene funcionando todo el tiempo, se apague durante los momentos en los que no haya nadie en la casa.' \
                            'Otra alternativa sería programarlo, con un timer en las pastillas o si es posible desde el mismo equipo, para que se mantenga apagado durante el tiempo que no se necesite o' \
                            'periodos en donde no sea tan necesario que se limpie tan seguido '


    elif 'lavajilla' in equipo.lower():
        texto =  'Recuerda usar este tipo de equipos de forma moderada, ya que son equipos de alto consumo. <br />'

    elif 'jacuzzi' in equipo.lower():
        texto =  'El gasto elevado se debe a un uso prolongado de la bomba. Te recomendamos usar este equipo de forma moderada' \
                            ' ya que la bomba que utiliza es de alto consumo. <br />'

    elif 'computo' in equipo.lower():
        texto =  'Tu equipo de computo tiene un alto consumo debido a que se usa de forma prolongada. ' \
                            'Sabemos que a veces no es posible reducir su tiempo de uso por cuestiones de trabajo pero te dejamos unos consejos para ahorrar:' \
                            '<br />De ser posible, asegurate de apagar los monitores y todos tus dispositivos completamente cuando no los estés usando. ' \
                            'Tambien asegurate de apagar por completo la computadora cuando ya no la vayas a ocupar, ' \
                            'ya que si solo la dejas suspendida seguirá consumiendo energía y generandote un gasto innecesario. <br />'

    # elif 'computadora' in equipo.lower():
    #     texto = texto+' ' + 'Tu equipo de computo tiene un alto consumo debido a que se usa de forma prolongada. ' \
    #                         'Sabemos que a veces no es posible reducir su tiempo de uso por cuestiones de trabajo pero te dejamos unos consejos para ahorrar:' \
    #                         '<br />De ser posible, asegurate de apagar por completo la computadora cuando ya no la vayas a ocupar, ' \
    #                         'ya que si solo la dejas suspendida seguirá consumiendo energía y generandote un gasto innecesario. <br />'
    #
    #
    # elif 'monitor' in equipo.lower() or 'monitores' in equipo.lower():
    #     texto = texto+' ' + 'Tus monitores tiene un impacto fuerte en tu consumo de energía debido a que se mantienen encendidos por largos periodos de tiempo.' \
    #                         'Sabemos que a veces no es posible reducir su tiempo de uso por cuestiones de trabajo pero te dejamos unos consejos para ahorrar:' \
    #                         '<br />De ser posible, asegurate de apagar los monitores y todos tus dispositivos de oficina completamente cuando no los estés usando. ' \
    #                         'Tambien asegurate de apagar por completo la computadora cuando ya no la vayas a ocupar, ' \
    #                         'ya que si solo la dejas suspendida seguirá consumiendo energía y generandote un gasto innecesario. <br />'

    else:
        texto=nota

    return texto


def textodeequiposA(equipo,nota):
    texto=''
    equipo=unidecode(equipo).lower()
    if 'laptop' in equipo:
        texto = texto+' ' + 'Para las laptops te recomendamos desconectarlas del enchufe cuando se terminen de usar. ' \
                            'Es importante para evitar que sigan consumiendo energía y así poder generar un mayor ahorro. <br /> '
    elif 'computadora' in equipo or 'PC' in equipo:
        texto = texto+' ' + 'Tu equipo de computo gasta ligeramente más que el promedio de nuestros clientes, para estos equipos' \
                            'recomendamos apagarlos completamente cuando no están en uso, asegurate de que tu computadora se apague completamente' \
                            ' y que no se encuentre en modo de suspención ya que seguirá gastando energía. Es importante para evitar que sigan consumiendo energía y así poder generar un mayor ahorro. <br /> '

    elif 'equipos de cocina' in equipo:
        texto = texto+' ' + 'La gran mayoría de los equipos de cocina, por su naturaleza, son de alto consumo por lo que para poder evitar un gasto elevado ' \
                            'lo más eficiente es ser consciente de sus encendidos. Recuerda apagarlos completamente o de ser posible desconectarlos si no los estás usando ' \
                            ' <br />'

    elif 'bluray' in equipo:
        texto = texto+' ' + 'Los Blue Rays/Videocaseteras ya son una tecnología más antigua que no se usa, así que se ' \
                            'puede agregar un texto como "Seguido, los Blue Rays y videocaseteras ya están en desuso. ' \
                            'Sin embargo, pueden representar un consumo de energía en este momento o a futuro ' \
                            'por lo que puede ser prudente desconectarlos completamente'

    elif 'aspirador' in equipo:
        texto = texto+' ' + 'La aspiradora se usó varios días a la seman. Su consumo es un poco más elevado que la mayoría de nuestros clientes., ' \
                            ' Recuerda desconectarla cuando no la estés usando. <br /> '


    elif 'cabello' in equipo:
        texto = texto+' ' + 'Por su naturaleza este equipo es de alto consumo ya que su función es generar aire caliente. ' \
                            'Recuerda usar el equipo conscientemente para evitar que se convierta en un problema mayor. <br /> '

    elif 'pelo' in equipo:
        texto = texto+' ' + 'Por su naturaleza este equipo es de alto consumo ya que su función es generar aire caliente. ' \
                            'Recuerda usar el equipo conscientemente para evitar que se convierta en un problema mayor. <br /> '

    elif 'calentador' in equipo:
        texto = texto+' ' + 'Este equipo tiene un consumo elevado por su función de calentar el área, ' \
                            'te recomendamos usarlo de forma consciente para lograr un consumo aún más bajo.' \
                            ' Cierra puertas y ventanas cuando lo uses para evitar que entre el frío y se tenga que usar ' \
                            'por más tiempo. <br /> '

    elif 'horno' in equipo or 'hornito' in equipo:
        texto = texto+' ' + 'Tu horno es de alto consumo por lo que para poder evitar un gasto elevado ' \
                            'lo más eficiente es ser consciente de sus encendidos; apaga el equipo después de su uso.  <br />'

    elif 'estufa' in equipo:
        texto = texto+' ' + 'Tu estufa es de alto consumo por lo que para poder evitar un gasto elevado ' \
                        'lo más eficiente es ser consciente de sus encendidos; apaga el equipo después de su uso.  <br />'

    elif 'thermomix' in equipo or 'termomix' in equipo:
        texto = texto+' ' + 'Tu equipo Thermomix es de alto consumo por lo que para poder evitar un gasto elevado ' \
                            'lo más eficiente es ser consciente de sus encendidos; apaga el equipo después de su uso.  <br />'

    elif 'horno' in equipo:
        texto = texto+' ' + 'Tu horno es de alto consumo por lo que para poder evitar un gasto elevado ' \
                            'lo más eficiente es ser consciente de sus encendidos; apaga el equipo después de su uso. ' \
                            'Puedes cambiar a un horno de gas para ahorrar en energía electrica, también puedes usar tu estufa para ' \
                            'cocinar algunos de los alimentos y de esa forma ahorrar en energía eléctrica  <br />'

    elif 'lavavajilla' in equipo:
        texto = texto+' ' + 'El consumo de tu lavavajillas es un poco más alto que el promedio de nuestros clientes. recuerda usarlo' \
                            ' de forma moderada, ya que es un equipo de alto consumo. <br />'

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

    elif 'computo' in equipo.lower():
        texto = texto+' ' + 'Tienes un buen consumo usando tu equipo de computo. Recuerda apagar completamente tus equipos. ' \
                            'Es importante para evitar que sigan consumiendo energía y así poder generar un mayor ahorro de energía. <br /> '

    elif 'monitor' in equipo.lower():
        texto = texto + ' ' + 'Tienes un buen consumo usando tu equipo de computo. Recuerda apagar completamente tus equipos ' \
                'para evitar que sigan consumiendo energía y así poder generar un mayor ahorro de energía. <br /> '


    elif 'bomba'in equipo.lower():
        texto = texto+' ' + 'Revisamos el funcionamiento de tu bomba, No encontramos problemas, tiene un buen desempeño y un ' \
                            'consumo de energía eficiente. Recuerda darle mantenimiento de manera regular <br /> '

    elif 'tetera' in equipo.lower():
        texto = texto + ' ' +    "El consumo de energía de tu tetera se encuentra por debajo del consumo promedio de otros de nuestros clientes. Sigue usandola con moderación."

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
                            'lo más eficiente es ser consciente de sus encendidos; apaga el equipo después de su uso. '

    elif 'estufa' in equipo.lower():
        texto = texto+' ' + 'El consumo de tu estufa es bueno. Recuerda que es un equipo potente úsalo con moderación.' \
                            '; apaga el equipo después de su uso. '

    elif 'thermomix' in equipo.lower() or 'termomix' in equipo.lower():
        texto = texto+' ' + 'Tu consumo es bueno. Recuerda que tu equipo es de alto consumo usalo con moderación' \
                            '; apaga el equipo después de su uso.'



    elif 'belleza' in equipo.lower():
        texto = texto+' ' + 'Algunos de estos equipos de belleza son de alto consumo y se deben utilizar de forma ' \
                            'consciente. En tu caso el uso es muy eficiente, continúa con los buenos hábitos de uso' \
                            ' y no olvides desconectarlos cuando no se estén utilizando.'

    elif 'cargador' in equipo.lower() or 'cargadores' in equipo.lower():
        texto = texto+' ' + 'Existe la creencia de que al dejar los cargadores de celular conectados, ' \
                            'estos siguen consumiendo energía. Probablemente ese era el caso de diseños más viejos, ' \
                            'pero hoy en día un cargador de celular que se queda conectado a la pared no está usando' \
                            ' energía (¡y lo hemos medido cientos de veces!). El único momento en que el cargador ' \
                            'toma energía, es cuando tiene un equipo conectado y está cargando su batería. ' \
                            'En tu caso, puedes quitarte de la preocupación de estar desconectando cargadores.'

    elif 'cpap' in equipo.lower() or 'bipap' in equipo.lower():
        texto = texto+' ' + 'Este dispositivo, a pesar de utilizarse todas las noches, tiene un consumo muy eficiente de energía.'

    else:
        texto=nota

    return texto

def noatac(equipos):
    ConsejosCompletos=''
    Conta=''


    for index, claves in equipos.iterrows():
        equipo     = claves[3]
        potencia   = claves[9]
        texto      = claves[13]
        clave      = claves[16]
        equipo=unidecode(equipo.lower())


        if clave=='AMN':
            if not 'AM' in Conta:
                Consejos='-'+texto+' <br /> <br />'
                ConsejosCompletos=ConsejosCompletos+Consejos
                Conta=Conta+'AM /'
        else:
            if 'refrigerador' in equipo:
                if not 'RF' in Conta:
                    if not 'regulador' in equipo:
                        Consejos='-Lamentablemente es difícil reducir el consumo de standby de un refrigerador ' \
                                 'sin tener que reemplazarlo o afectar alguna de sus caracteristicas. <br /> <br />'
                        Conta = Conta+'RF /'
                        ConsejosCompletos=ConsejosCompletos+Consejos

            elif 'congelador' in equipo:
                if not 'CN' in Conta:
                    if not 'regulador' in equipo:
                        Consejos='-Es difícil reducir el consumo de standby de un congelador' \
                                 'sin reemplazarlo. <br /> <br />'
                        Conta = Conta+'CN /'
                        ConsejosCompletos=ConsejosCompletos+Consejos

            elif 'cava' in equipo:
                if not 'CV' in Conta:
                    if not 'regulador' in equipo:
                        Consejos='-No es fácil reducir el consumo de standby de tu cava sin afectar su buen funcionamiento ' \
                                 '. <br /> <br />'
                        Conta = Conta+'CV /'
                        ConsejosCompletos=ConsejosCompletos+Consejos



            elif 'calentador' in equipo and not 'CL' in Conta:
                Consejos='-Lamentablemente no es posible eliminar el consumo de este equipo sin reemplazarlo. <br /> <br />'
                ConsejosCompletos=ConsejosCompletos+Consejos
                Conta = Conta+'CL /'

            elif 'alexa' in equipo:
                Consejos= '-Es difícil desconectar los dispositivos inteligentes ya que afectan a tu comodidad. ' \
                          'Si no llegas a usarlos te recomendamos desconectarlos. <br /> <br />'
                ConsejosCompletos=ConsejosCompletos+Consejos

            elif 'lutron' in equipo:
                Consejos= '-Es difícil desconectar los dispositivos inteligentes ya que afectan a tu comodidad. ' \
                                    'Si no llegas a usarlos te recomendamos desconectarlos. <br /> <br />'
                ConsejosCompletos=ConsejosCompletos+Consejos

            elif 'sensor' in equipo:
                if not 'SN' in Conta:
                    Consejos= 'Te recomendamos mantener tu sensor encendido ya que esto te está ahorrando mucha más energía de la que consume.  <br /> <br />'
                    ConsejosCompletos=ConsejosCompletos+Consejos
                    Conta = Conta+'SN /'

            elif 'camara' in equipo:
                if not 'SG' in Conta:
                    Consejos='-En los equipos de seguridad no recomendamos tomar acción o desconectarlos, ' \
                             'debido a que pueden afectar tanto tu confort como tu seguridad <br /> <br />'
                    ConsejosCompletos=ConsejosCompletos+Consejos
                    Conta = Conta+'SG /'


            elif 'modem' in equipo or 'repetidor' in equipo:
                if not 'MD' in Conta:
                    Consejos='-En los equipos de comunicación no recomendamos tomar acción o desconectarlos, ' \
                         'debido a que interfieren con tu confort. <br /> <br />'
                    Conta = Conta+'MD /'
                    ConsejosCompletos=ConsejosCompletos+Consejos

            elif 'puerta' in equipo or 'porton' in equipo:
                Consejos= '-Por tu comodidad no te recomendamos realizar ninguna acción a tu puerta eléctrica. <br /> <br />'
                ConsejosCompletos=ConsejosCompletos+Consejos

            elif 'puerta' in equipo or 'porton' in equipo:
                Consejos= '-Por tu comodidad no te recomendamos realizar ninguna acción a tu puerta eléctrica. <br /> <br />'
                ConsejosCompletos=ConsejosCompletos+Consejos

            elif 'seguridad' in equipo and not 'SG' in Conta:
                Consejos='-En los equipos de seguridad no recomendamos tomar acción o desconectarlos, ' \
                         'debido a que pueden afectar tanto tu confort como tu seguridad <br /> <br />'
                Conta = Conta+'SG /'
                ConsejosCompletos=ConsejosCompletos+Consejos
            elif 'lavadora' in equipo and not 'SG' in Conta:
                Consejos='-Lamentablemente encontramos díficil que puedas desconectar tu lavadora o que puedas colocar un timer <br /> <br />'
                Conta = Conta+'LV /'
                ConsejosCompletos=ConsejosCompletos+Consejos
            elif 'secadora' in equipo and not 'SG' in Conta:
                Consejos='-Lamentablemente encontramos díficil que puedas desconectar tu secadora o que puedas colocar un timer <br /> <br />'
                Conta = Conta+'SC /'
                ConsejosCompletos=ConsejosCompletos+Consejos

            else:
                if not 'NA' in Conta:
                    Consejos='-Lamentablemente por su naturaleza tu equipo no se puede desconectar. <br /> <br />'
                    Conta = Conta+'NA /'
                    ConsejosCompletos=ConsejosCompletos+Consejos

            if 'regulador' in equipo:
                if not 'RG' in Conta:
                    Consejos= armarTxt_NAtac(clave)
                    Conta = Conta +'RG /'
                    ConsejosCompletos=ConsejosCompletos+Consejos




    return ConsejosCompletos