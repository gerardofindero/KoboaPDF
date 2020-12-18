import locale
import os
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas as canvas_, canvas
from reportlab.lib.pagesizes import A4
from datetime import date
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus import Frame, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.colors import Color
from unidecode import unidecode
from PIL import Image
import Estilos
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.lineplots import LinePlot
import logging
from datetime import datetime
from pathlib import Path


locale.setlocale(locale.LC_ALL, 'es-MX')
logging.basicConfig(filename="logger.log", level=logging.INFO, format='%(asctime)s %(levelname)s:  %(message)s \n',
                    datefmt='%Y-%m-%d %H:%M:%S')


def fonts():
    pdfmetrics.registerFont(TTFont('Montserrat', 'Fonts\Montserrat-Light.ttf'))
    pdfmetrics.registerFont(TTFont('Montserrat-N', 'Fonts\Montserrat-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Montserrat-B', 'Fonts\Montserrat-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Montserrat-L', 'Fonts\Montserrat-Light.ttf'))
    pdfmetrics.registerFont(TTFont('Montserrat-XL', 'Fonts\Montserrat-ExtraLight.ttf'))
    pdfmetrics.registerFontFamily('montserrat', normal='Montserrat', bold='Montserrat-B')


def set_fonts(canvas, text, color, type, size, lead=None):
    if isinstance(color, str):
        canvas.setFillColor(color)
    else:
        try:
            canvas.setFillColorRGB(color[0], color[1], color[2], color[3])
        except:
            canvas.setFillColorRGB(color[0], color[1], color[2])

    text.setFont(f'Montserrat-{type.upper()}', size)
    if lead:
        text.setLeading(lead)


def parrafo(texto, estilo, factor_w, factor_h, pos_x, pos_y, canvas):
    width = 595
    height = 841
    parrafo = Paragraph(texto, estilo)
    w, h = parrafo.wrap(int(width * factor_w), int(height * factor_h))
    parrafo.drawOn(canvas, width * pos_x, height * pos_y - h)


def parrafo_frame(texto, estilo, pos_x, pos_y, ancho, alto,canvas):
    width = 595
    height = 841
    parrafo = [Paragraph(texto, estilo)]
    frame = Frame(pos_x, pos_y, width * ancho, height * alto)
    frame.addFromList(parrafo, canvas)


def parrafo_en_imagen(texto, estilo, pos_x, pos_y, ancho, alto):
    parrafo = [Paragraph(texto, estilo)]
    frame = Frame(pos_x, pos_y, ancho, alto)
    frame.addFromList(parrafo, canvas)


def texto(texto, tamano, color, font, ancho, alto, canvas):
    text = canvas.beginText(ancho, alto)
    canvas.setFillColorRGB(color[0], color[1], color[2])
    text.setFont(font, tamano)
    text.textLines(texto)
    canvas.drawText(text)


def cuatro_lineas(canvas):
    width = 595
    height = 841
    for i in range(4):
        canvas.line(60, height - 150 - (i * 210), width - 60, height - 150 - (i * 210))


def costado(canvas, color='black'):
    """ Se crea el banner vertical que va al costado de cada hoja"""

    canvas.rotate(90)
    text = canvas.beginText(100, -18)
    set_fonts(canvas, text, color, 'B', 7)
    text.textLine('RESULTADOS Y RECOMENDACIONES')
    canvas.drawText(text)
    text = canvas.beginText(236, -18)
    set_fonts(canvas, text, color, 'L', 7)
    text.textLine(' / ESTUDIO DE CONSUMO DE ELECTRICIDAD')
    canvas.drawText(text)
    canvas.rotate(270)
    canvas.setFillColorRGB(2 / 255, 142 / 255, 200 / 255, alpha=0.9)  # azul
    canvas.rect(15, 0, 2, 60, fill=True, stroke=False)
    canvas.setFillColorRGB(118 / 225, 163 / 255, 65 / 255, alpha=0.9)  # verde
    canvas.rect(15, 35, 2, 60, fill=True, stroke=False)


def atacable_o_no(canvas, idx, pos_x, pos_y):
    """ Escribe si es atacble o no en el costado de color verde o rojo """

    blanco = [1, 1, 1]

    mensaje = {0: "ATACABLE", 1: "NO ATACABLE"}
    espacio = 16

    for indx, letra in enumerate(mensaje[idx]):
        texto(letra, 16, blanco, 'Montserrat-B', width * (pos_x + .346), height * (pos_y + 0.28) - espacio * indx,
              canvas)


def detalles_fugas(canvas, width, height, zona, idx, costo, consumo):
    """ Crea una pagina nueva para las fugas """

    azul_1 = [0 / 255, 76 / 255, 101 / 255]
    azul_2 = [2 / 255, 142 / 255, 200 / 255]
    gris = [65 / 255, 65 / 255, 65 / 255]
    blanco = [1, 1, 1]

    largo_encabezado = pdfmetrics.stringWidth('DESCIFRAMIENTO DE COSNUMO Y PÉRDIDAS DE ENERGÍA', 'Montserrat-B', 12)
    canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
    texto('DESCIFRAMIENTO DE PÉRDIDAS DE ENERGÍA', 12, gris, 'Montserrat-B', 60, height - 65, canvas)

    largo_titulo = pdfmetrics.stringWidth(zona.upper(), 'Montserrat-B', 12)
    parrafo_frame(f"<b>{zona.upper()}</b>", Estilos.titulos, 60, 500, .8, .25)

    if largo_titulo > 150:
        extra = 40
    elif largo_titulo > 300:
        extra = 80
    else:
        extra = 0
    canvas.drawImage(f"Imagenes/icono_fuga.png", 60, height - 310 - extra, width=115, height=115)

    margen = 50
    if len(str(costo)) < 4:
        tamano_dinero = 125
    else:
        tamano_dinero = 120

    largo_precio = pdfmetrics.stringWidth('{:,}'.format(costo), 'Montserrat-B', tamano_dinero)
    largo_signo = pdfmetrics.stringWidth('$', 'Montserrat-B', 70)
    texto('{:,}'.format(costo), tamano_dinero, azul_2, 'Montserrat-B', width - margen - largo_precio, height * 0.5 + 60,
          canvas)
    texto('$', 70, azul_2, 'Montserrat-B', width - margen - largo_precio - largo_signo, height * 0.5 + 60, canvas)

    largo_cons = pdfmetrics.stringWidth('{:,}'.format(consumo), 'Montserrat-B', 30)
    largo_kwh = pdfmetrics.stringWidth('kWh', 'Montserrat-B', 30)
    texto('{:,}'.format(consumo), 30, azul_2, 'Montserrat-B', width - margen - largo_cons - largo_kwh - 5,
          height * 0.5 + 20, canvas)
    texto('kWh', 30, azul_2, 'Montserrat-B', width - margen - largo_kwh, height * 0.5 + 20, canvas)

    factor = .45
    w, h = Image.open(f"Imagenes/Figuras/Figuras-0{idx + 1}.png").size
    pos_x = .55
    pos_y = 0.13
    canvas.drawImage(f"Imagenes/Figuras/figuras-0{idx + 1}.png", width * pos_x, height * pos_y, w * factor, h * factor)
    frame = Frame(width * 0.55 + 10, height * 0.05 - 125, width * 0.3, height * 0.5)
    texto('¿QUÉ HACER?', 16, blanco, 'Montserrat-B', width * (pos_x + .055), height * (pos_y + .323), canvas)
    atacable_o_no(canvas, idx, pos_x, pos_y)

def Enxyy(canvas):
    for i in range(0,600,10):
        canvas.setFont("Helvetica", 5)
        canvas.drawString(i, 1, str(i))
        canvas.line(i, 0, i, 1000)


    for i in range(0,1000,10):
        canvas.setFont("Helvetica", 5)
        canvas.drawString(1, i, str(i))
        canvas.line(0, i, 600, i)

    canvas.showPage()

def portada(canvas, width, height):
    """ Portada del documento """

    canvas.drawImage('Imagenes\Figuras\Portada.png', 0, 0, width=width, height=height)
    locale.setlocale(locale.LC_TIME, '')
    today = date.today()
    timestampStr = today.strftime("%Y-%B-%d")
    text = canvas.beginText(30, 40)
    canvas.setFillColor('white')
    text.setFont("Montserrat-L", 13)
    text.textLines(timestampStr[5:-3].upper() + ' ' + timestampStr[0:4])
    canvas.drawText(text)
    canvas.showPage()

def Solar(canvas):
    DAC = 5.2

    consumo    =  1500
    costo      = consumo*DAC
    generacion = 315
    cobrada    = 315
    costoCob   = cobrada*DAC


    factor=0.5
    x=0
    y=80
    w, h = Image.open(f"Imagenes/Figuras/Psolar.png").size
    canvas.drawImage(f"Imagenes/Figuras/Psolar.png", x + 55, y + 5, w * factor, h * factor)
    w, h = Image.open(f"Imagenes/Figuras/PsolarA.png").size
    canvas.drawImage(f"Imagenes/Figuras/PsolarA.png", x + 10, y + 450, w * factor, h * factor)
    #parrafo_frame({}, Estilos.negro, 49, 50, .4, .5)

    parrafo_frame("<b>${:,}</b>".format(round(costoCob)), Estilos.azul_1_grande, x + 437, y + 380, .15, .15, canvas)
    parrafo_frame("<b>${:,}</b>".format(round(costo)), Estilos.azul_1_grande, x + 297, y + 380, .15, .15, canvas)
    parrafo_frame("<b>{:,}</b>".format(round(consumo)), Estilos.azul_1_grande, x + 441, y + 415, .15, .15, canvas)
    parrafo_frame("<b>{:,}</b>".format(round(cobrada)), Estilos.azul_1_grande, x + 301, y + 415, .15, .15, canvas)

    costado(canvas)
    canvas.showPage()


def intro(canvas, width, height, datos=1545236):
    """ Pagina de color azul antes de presentar los resultados."""

    canvas.setFillColorRGB(96 / 255, 192 / 255, 215 / 255)
    canvas.rect(0, 0, width, height, fill=1, stroke=False)
    canvas.drawImage("Imagenes\Spark1_blueBG.png", width - 70, height - 65, width=40, height=40)
    costado(canvas, 'white')

    text = canvas.beginText(60, height * 0.5 + 150)
    set_fonts(canvas, text, (1, 1, 1), 'B', 36)
    text.textLines('DESCIFRAMIENTO \n'
                   + 'DE CONSUMO Y \n'
                   + 'PÉRDIDAS DE ENERGÍA')
    canvas.drawText(text)

    with open('Textos\introduccion_1.txt', 'r', encoding='utf-8') as file:
        parrafo_1 = file.read()
    with open('Textos\introduccion_2.txt', 'r', encoding='utf-8') as file:
        parrafo_2 = file.read()

    factor_w = .3
    factor_h = .1

    parrafo(parrafo_1.format(datos), Estilos.base, factor_w, factor_h, .1, .48, canvas)
    parrafo(parrafo_2, Estilos.base, factor_w, factor_h, .1, .14, canvas)

    mensajes = {1: 'Consumo óptimo', 2: 'Consumo promedio', 3: 'Consumo innecesario'}
    for i in range(3):
        text = canvas.beginText(60 + 36, height * 0.5 - (12 * (17 + i * 3)))
        set_fonts(canvas, text, (65 / 255, 65 / 255, 65 / 255), 'B', 12)
        text.textLines(mensajes[3 - i])
        canvas.drawText(text)
        canvas.drawImage(f"Imagenes\cara_{3 - i}_b.png", 60, height * 0.5 - (6 + (12 * (17 + i * 3))), width=22,
                         height=22)

    canvas.showPage()


def potencial_ahorro(canvas, width, height,consumo_bimestral, tarifa,ahorro_bimestral, tipo_tarifa):
    """ Se hace la página que muestra el potencial de ahorro """

    NoPaneles=round(ahorro_bimestral/68)
    ahorro_paneles=round(NoPaneles*13500)
    co2=round(ahorro_bimestral*0.52*6)
    arboles=round(co2*0.015)

    nuevo_consumo= consumo_bimestral-ahorro_bimestral
    costo_bimestral=consumo_bimestral*tarifa

    actual = consumo_bimestral * tarifa

    azul_1 = [0 / 255, 76 / 255, 101 / 255]

    canvas.line(60, height - 50, 400, height - 50)

    texto('POTENCIAL DE AHORRO', 36, azul_1, 'Montserrat-B', 60, height - 170, canvas)

    parrafo('Al momento de implementar las recomendaciones de este reporte, tu consumo energético sería de:',
            Estilos.base, .7, .2, .1, .7, canvas)

    asterisco = "*"
    if nuevo_consumo < 500:
        asterisco = "**"

    if nuevo_consumo < 500:
        if nuevo_consumo <= 150:
            nuevo = nuevo_consumo * .8 * 0.99
        elif nuevo_consumo <= 280:
            nuevo = (150*0.94+130 + (nuevo_consumo - 150) * 1.14)
        elif nuevo_consumo > 280:
            nuevo = (150*0.94+130*1.14 + (nuevo_consumo - 280) * 3.35)

        nuevo = int(nuevo)
    else:
        nuevo = int(nuevo_consumo * tarifa)

    factor = .25
    w, h = Image.open(f"Imagenes/Figuras/barra_consumo1.png").size
    w = w * factor
    h = h * factor
    x = (width - w) / 2
    y = height * 0.6
    canvas.drawImage(f"Imagenes/Figuras/barra_consumo1.png", x, y-20, w, h)

    texto('0 kWh', 8, (0,0,0), 'Montserrat-B', 85, height-325 , canvas)
    texto('500 kWh', 8, (0, 0, 0), 'Montserrat-B', 270, height - 325, canvas)
    texto('Tarifa DAC', 8, (20, 0, 0), 'Montserrat-B', 265, height - 305, canvas)
    texto('1000 kWh', 8, (0, 0, 0), 'Montserrat-B', 480, height - 325, canvas)


    factor = .5
    w_, h_ = Image.open(f"Imagenes/Figuras/rayo.png").size
    w_ = w_ * factor
    h_ = h_ * factor
    canvas.drawImage(f"Imagenes/Figuras/rayo.png", x + w * nuevo_consumo / 1000 - w_ / 2 + 5, y - 50, w_, h_,
                     mask='auto')
    canvas.drawImage(f"Imagenes/Figuras/rayo.png", x + w * consumo_bimestral / 1000 - w_ / 2 + 5, y - 50, w_, h_,
                     mask='auto')

    parrafo_frame("<b>Tu nuevo consumo energético:</b>", Estilos.azul_1_chico, x + w * nuevo_consumo / 1000 - 25, y - 130, .15, .1,canvas)
    parrafo_frame("<b>Tu consumo energético actual:</b>", Estilos.azul_1_chico, x + w * consumo_bimestral / 1000 - 25, y - 130, .15, .1,canvas)
    parrafo_frame("<b>{:,} kWh</b>".format(nuevo_consumo), Estilos.azul_1_grande, x + w * nuevo_consumo / 1000 - 25, y - 205, .15, .15,canvas)
    parrafo_frame("<b>{:,} kWh</b>".format(consumo_bimestral), Estilos.azul_1_grande,  x + w * consumo_bimestral / 1000 - 25, y - 205, .15, .15,canvas)

    parrafo_frame("<b>${:,}{asterisco}</b>".format(nuevo, asterisco=asterisco), Estilos.azul_1_grande,
                  x + w * nuevo_consumo / 1000 - 25, y - 191, .15, .15,canvas)
    parrafo_frame("<b>${:,}</b>".format(round(actual), asterisco=asterisco), Estilos.azul_1_grande,
                  x + w * consumo_bimestral / 1000 - 25, y - 191, .15, .15,canvas)

    factor = .22
    w, h = Image.open(f"Imagenes/Figuras/Figuras-06.png").size
    x = (width - w * factor) / 2
    y = height * 0.1
    #canvas.drawImage(f"Imagenes/Figuras/Figuras-06.png", x, y, w * factor, h * factor)
    w, h = Image.open(f"Imagenes/Figuras/1_cuadro.png").size
    canvas.drawImage(f"Imagenes/Figuras/1_cuadro.png", x+5, y+5, w * factor, h * factor)

    factor = .25
    w, h = Image.open(f"Imagenes/Figuras/1_potencial.png").size
    canvas.drawImage(f"Imagenes/Figuras/1_potencial.png", x-110, y+130, w * factor, h * factor)

    w, h = Image.open(f"Imagenes/Figuras/1_recibo2.png").size
    canvas.drawImage(f"Imagenes/Figuras/1_recibo2.png", x+150, y+110, w * factor, h * factor)

    factor = .3
    w, h = Image.open(f"Imagenes/Figuras/1_barra_02.png").size
    canvas.drawImage(f"Imagenes/Figuras/1_barra_02.png", x + 210, y + 60, w * factor, h * factor)

    x=x-80

    parrafo_frame("Potencial de ahorro a corto plazo:", Estilos.centrado, x , y - 7, .22, .3,canvas)
    parrafo_frame(f"Tu nuevo recibo en tarifa {tipo_tarifa}:", Estilos.centrado, x + 220, y - 10, .3, .3,canvas)

    parrafo_frame("<b>ALREDEDOR DE</b>", Estilos.blanco_chico, x, y - 45, .22, .3,canvas)
    parrafo_frame("<b>ALREDEDOR DE</b>", Estilos.blanco_chico, x + 260, y - 45, .22, .3,canvas)

    ahorro = int(costo_bimestral - nuevo_consumo * tarifa)

    parrafo_frame("<b>${:,}</b>".format(ahorro), Estilos.blanco_grande, x , y - 60, .22, .3,canvas)
    parrafo_frame("<b>${:,}{asterisco}</b>".format(int(nuevo_consumo * tarifa), asterisco=asterisco),
                  Estilos.blanco_grande, x + 262, y - 60, .22, .3,canvas)

    parrafo_frame("Tu ahorro tiene un impacto ambiental de:", Estilos.chica, x + 300, y - 55, .22, .2,canvas)
    parrafo_frame("<b>{:,} kg de CO<sub>2</sub>E al año</b>".format(co2), Estilos.chica, x + 300, y - 84, .25, .2,canvas)
    parrafo_frame(
        "Lo que equivale a <b>{:,} árboles</b> plantados que absorben esta cantidad de CO<sub>2</sub>E a lo largo de 30 años.".format(
            round(arboles)), Estilos.chica, x + 300, y - 105, .20, .2,canvas)




    if nuevo_consumo < 500:
        parrafo_frame('&nbsp; Tu nuevo recibo en &nbsp; &nbsp; tarifa subsidiada sería de:', Estilos.centrado_chico,
                      x + 125, y - 125, .25, .33,canvas)
        parrafo_frame("<b>ALREDEDOR DE</b>", Estilos.azul_2_chico, x + 145, y - 46, .2, .2,canvas)
        parrafo_frame("<b>${:,}</b>".format(nuevo), Estilos.azul_2_grande, x + 150, y - 53, .2, .2,canvas)
        parrafo_frame("Si sigues nustras recomendaciones, <b>es posible que logres bajar de tarifa.</b> Para esto,"
                      " te sugerimos acciones para conseguirlo. Además, <b>te estarías ahorrando ${:,} en paneles solares</b>".format(
            ahorro_paneles),
                      Estilos.chica, x + 100, y - 80, .33, .2,canvas)
        parrafo_frame("Nota: * Aplicando nuestras recomendaciones. "
                      "**La tarifa doméstica de alto consumo considera el promedio de consumo de los últimos 12 meses"
                      " así que el cambio de tarifa sería menos inmediato.", Estilos.mini, 60, 0, .8, .05,canvas)
    else:
        parrafo_frame("<b>No es posible bajar de tarifa</b>", Estilos.centrado_chico, x + 145, y - 125, .18, .33,canvas)
        parrafo_frame(
            "A pesar de implementar nuestras recomendaciones, tu consumo sigue estando por encima del límite de tarifa Doméstica de Alto Consumo."
            " Sin embargo, <b>te estarías ahorrando ${:,} en paneles solares</b>".format(ahorro_paneles), Estilos.chica,
            x + 100, y - 75, .33, .2,canvas)


    costado(canvas)
    canvas.showPage()


def iluminacion(canvas, width, height, luces, detalles_luces):
    """ Se crean las páginas en donde se muestra el consumo de luz a detalle """

    azul_1 = [0 / 255, 76 / 255, 101 / 255]
    azul_2 = [2 / 255, 142 / 255, 200 / 255]
    gris = [65 / 255, 65 / 255, 65 / 255]
    blanco = [1, 1, 1]

    gristabla = colors.Color(red=(65 / 255), green=(65 / 255), blue=(65 / 255))
    azul2tabla = colors.Color(red=(2 / 255), green=(142 / 255), blue=(200 / 255))

    largo_encabezado = pdfmetrics.stringWidth('DESCIFRAMIENTO DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 'Montserrat-B', 12)
    canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
    texto('DESCIFRAMIENTO DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
    texto('ILUMINACIÓN', 36, azul_1, 'Montserrat-B', 60, height - 170, canvas)
    canvas.drawImage(f"Imagenes/icono_luces.png", 60, height - 295, width=115, height=115)
    canvas.drawImage(f"Imagenes/cara_{luces[1]}.png", 60, height * 0.5 - 10, width=80, height=80)

    margen = 50
    dinero = round(luces[4])
    if len(str(dinero)) < 4:
        tamano_dinero = 125
    else:
        tamano_dinero = 120
    largo_precio = pdfmetrics.stringWidth('{:,}'.format(dinero), 'Montserrat-B', tamano_dinero)
    largo_signo = pdfmetrics.stringWidth('$', 'Montserrat-B', 70)
    texto('{:,}'.format(dinero), tamano_dinero, azul_2, 'Montserrat-B', width - margen - largo_precio,
          height * 0.5 + 60, canvas)
    texto('$', 70, azul_2, 'Montserrat-B', width - margen - largo_precio - largo_signo, height * 0.5 + 60, canvas)

    consumo = round(luces[3])
    largo_cons = pdfmetrics.stringWidth('{:,}'.format(consumo), 'Montserrat-B', 30)
    largo_kwh = pdfmetrics.stringWidth('kWh', 'Montserrat-B', 30)
    texto('{:,}'.format(consumo), 30, azul_2, 'Montserrat-B', width - margen - largo_cons - largo_kwh - 5,
          height * 0.5 + 20, canvas)
    texto('kWh', 30, azul_2, 'Montserrat-B', width - margen - largo_kwh, height * 0.5 + 20, canvas)

    porcentaje = str(round(luces[2] * 100, 1))
    largo_pct = pdfmetrics.stringWidth(porcentaje, 'Montserrat-N', 25)
    largo_sign = pdfmetrics.stringWidth('% de tu consumo', 'Montserrat-N', 25)
    texto(porcentaje, 25, gris, 'Montserrat-N', width - margen - largo_pct - largo_sign, height * 0.5 - 10, canvas)
    texto('% de tu consumo', 25, gris, 'Montserrat-N', width - margen - largo_sign, height * 0.5 - 10, canvas)

    with open('Textos/iluminacion_1.txt', 'r', encoding='utf-8') as file:
        parrafo_1 = file.read()
    if luces[1] == 3:
        muy = 'muy '
    else:
        muy = ''
    parrafo(parrafo_1.format(muy=muy), Estilos.base, .4, .45, .1, .45, canvas)

    parrafos = []  # Append del parrafo sobre la imagen
    with open('Textos/iluminacion_2.txt', 'r', encoding='utf-8') as file:
        parrafo_2 = file.read()[1:]  # Existía un caracter inicial que no debia imprimirse.
    parrafos.append(Paragraph(parrafo_2, Estilos.cuadros))
    canvas.drawImage("Imagenes/Figuras/figuras-03.png", width * .55, height * 0.05, width * .35, height * .4)
    frame = Frame(width * 0.55 + 10, height * 0.05 - 125, width * 0.3, height * 0.5)
    texto('¿QUÉ HACER?', 16, blanco, 'Montserrat-B', width * .605, height * 0.422, canvas)
    frame.addFromList(parrafos, canvas)
    costado(canvas)
    canvas.showPage()

    canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
    texto('DESCIFRAMIENTO DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
    texto('ILUMINACIÓN', 36, azul_1, 'Montserrat-B', 60, height - 170, canvas)
    canvas.drawImage(f"Imagenes/icono_luces.png", 60, height - 295, width=115, height=115)

    tabla = []
    for values in detalles_luces.values():
        aparato = []
        aparato.append(Paragraph('<b>' + values[0] + '</b>', Estilos.tabla))
        aparato.append(str(round(values[1] * 100, 1)) + '%')
        aparato.append('$' + '{:,}'.format(values[2]))
        aparato.append(Paragraph(values[3], Estilos.tabla))
        tabla.append(aparato)
    tabla.insert(0, ['Ubicación', 'Porcentaje', 'Costo', 'Detalles'])

    tabla = Table(tabla, colWidths=(None, None, None, width * 0.3))
    tabla.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('TEXTCOLOR', (0, 0), (-1, -1), gristabla),
                               ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (3, 0), 1, colors.black),
                               ('BACKGROUND', (0, 0), (3, 0), azul2tabla),
                               ('TEXTCOLOR', (0, 0), (3, 0), colors.white),
                               ]))
    tabla.wrapOn(canvas, 400, 100)
    tabla.drawOn(canvas, 100, 100)
    costado(canvas)
    canvas.showPage()


def aparatos_grandes(canvas, width, height):
    """ Se crean las páginas en donde se muestran los consumos que ocupan una página completa """

    azul_1 = [0 / 255, 76 / 255, 101 / 255]
    azul_2 = [2 / 255, 142 / 255, 200 / 255]
    gris = [65 / 255, 65 / 255, 65 / 255]
    blanco = [1, 1, 1]
    deciframiento=['Refrigerador','1','0.3','20','175','1750',' ']
    #for aparato in desciframiento.values():
        # nombre = aparato[0]
        # carita = aparato[1]
        # porcentaje = aparato[2]
        # consumo = round(aparato[3])
        # dinero = round(aparato[4])
        # anual = aparato[5]
        # notas = aparato[6]
    nombre = 'Refrigerador'
    carita = 1
    porcentaje = 0.3
    consumo = 50
    dinero = 250
    anual = 3000
    notas = '.'


    # if carita < 2 or dinero < 300:
    #     continue
    # if nombre in ['Luces', 'Iluminación', 'Iluminacion']:
    #     continue

    nombre_ = unidecode(nombre.lower())
    abreviados = ['tv', 'bomba', 'calefaccion', 'refrigerador', 'estufa', 'luces', 'computadora', 'aire']
    for a in abreviados:
        if a in nombre_:
            nombre_ = a
            break

    largo_encabezado = pdfmetrics.stringWidth('DESCIFRAMIENTO DE COSNUMO Y PÉRDIDAS DE ENERGÍA', 'Montserrat-B', 12)
    canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
    texto('DESCIFRAMIENTO DE PÉRDIDAS DE ENERGÍA', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
    texto(nombre.upper(), 36, azul_1, 'Montserrat-B', 60, height - 130, canvas)
    try:
        canvas.drawImage(f"Imagenes/icono_{nombre_}.png", 60, height - 265, width=115, height=115)
    except:
        canvas.drawImage(f"Imagenes/icono_pendiente.png", 60, height - 265, width=115, height=115)

    ##Carita
    canvas.drawImage(f"Imagenes/cara_{carita}_c.png", 475, 670, width=55, height=55)

    margen = 50
    if len(str(round(dinero))) < 4:
        tamano_dinero = 125
    else:
        tamano_dinero = 120
    largo_precio = pdfmetrics.stringWidth('{:,}'.format(dinero), 'Montserrat-B', tamano_dinero)
    largo_signo  = pdfmetrics.stringWidth('$', 'Montserrat-B', 70)
    texto('{:,}'.format(dinero), tamano_dinero, azul_2, 'Montserrat-B', width - margen - largo_precio,
          height * 0.6 + 60, canvas)
    texto('$', 70, azul_2, 'Montserrat-B', width - margen - largo_precio - largo_signo, height * 0.6 + 60, canvas)

    largo_cons = round(pdfmetrics.stringWidth('{:,}'.format(consumo), 'Montserrat-B', 30))
    largo_kwh  = pdfmetrics.stringWidth('kWh', 'Montserrat-B', 30)
    texto('{:,}'.format(consumo), 30, azul_2, 'Montserrat-B', width - margen - largo_cons - largo_kwh - 5,
          height * 0.6 + 20, canvas)
    texto('kWh', 30, azul_2, 'Montserrat-B', width - margen - largo_kwh, height * 0.6 + 20, canvas)

    porcentaje = str(round(porcentaje * 100, 1))
    largo_pct = pdfmetrics.stringWidth(porcentaje, 'Montserrat-N', 25)
    largo_sign = pdfmetrics.stringWidth('% de tu consumo', 'Montserrat-N', 25)
    texto(porcentaje, 25, gris, 'Montserrat-N', width - margen - largo_pct - largo_sign, height * 0.6- 10, canvas)
    texto('% de tu consumo', 25, gris, 'Montserrat-N', width - margen - largo_sign, height * 0.6 - 10, canvas)

    parrafos = []
    if notas == '.':
        parrafos.append(Paragraph('Su consumo es óptimo', Estilos.cuadros_bajo))
    else:
        parrafos.append(Paragraph(notas, Estilos.aparatos))
    frame = Frame(60, 20, width * 0.5, height * 0.5)
    frame.addFromList(parrafos, canvas)

    Consejos = 'Este espacio está hecho para que los consejos se muestren aquí \n' \
               'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vehicula mi et lorem ultrices, ' \
               'in pharetra urna sollicitudin. Nullam ut quam sem. Proin condimentum ipsum eget porta porttitor. ' \
               'Proin ac magna eu neque ornare bibendum. Duis leo mi, mollis et leo et, semper egestas dolor. ' \
               'Vivamus venenatis aliquet sapien, semper volutpat urna. Nam tortor leo, laoreet in elit ac, ' \
               'gravida condimentum neque. Vestibulum commodo posuere leo vitae varius.'



        # parrafos = []
        # tipo = ''
        # variable_1 = ''
        # if nombre_ in ['refrigerador', 'tv']:
        #     numeros = re.findall(r'\d+', notas)
        #     tipo = '_'+numeros[0]
        #     variable_1 = numeros[1]
        #     variable_2 = numeros[2]
        # if 'lavado' in nombre_ or 'secado' in nombre_:
        #     numeros = re.findall(r'\d+', notas)
        #     tipo = '_'+numeros[0]
        #     variable_1 = numeros[1]
        #     variable_2 = numeros[2]
        #     variable_3 = numeros[3]
        #
        # with open(f'Textos/{nombre_}{tipo}.txt', 'r', encoding='utf-8') as file:
        #     parrafo_1 = file.read()
        # try:
        #     parrafo_1 = parrafo_1.format(var_1=variable_1)
        # except KeyError:
        #     try:
        #         parrafo_1 = parrafo_1.format(var_1=variable_1, var_2=variable_2)
        #     except KeyError:
        #         parrafo_1 = parrafo_1.format(var_1=variable_1, var_2=variable_2, var_3=variable_3)
        #
        # parrafo(parrafo_1, estilos.base, .4, .45, .1, .45, canvas)
        #
        # with open(f'Textos/Recomendaciones/{nombre_}{tipo}.txt', 'r', encoding='utf-8') as file:
        #     parrafo_1 = file.read()
        # parrafos.append(Paragraph(parrafo_1, estilos.cuadros))
    canvas.drawImage("Imagenes/Figuras/figuras-03.png", width * .47, height * 0.05, width * .45, height * .5)
        # frame = Frame(width * 0.55 + 10, height * 0.05 - 125, width * 0.3, height * 0.5)
        # frame.addFromList(parrafos, canvas)

##### Escribir en cuadro recomendaciones
    texto('¿QUÉ HACER?', 22, (255,255,255), 'Montserrat-B', width * .555, height * 0.512, canvas)
    parrafos.append(Paragraph(Consejos, Estilos.aparatos))
    frame = Frame(282, 46, width * 0.442, height * 0.44,showBoundary = 0 )
    frame.addFromList(parrafos, canvas)

    ##LogoRayo
    canvas.drawImage(f"Imagenes/Figuras/2_datos_rayo.png", 550, 780,
                     width=40, height=40)

    costado(canvas)
    canvas.showPage()


def aparatos_bajos(canvas, width, height):
    """ Se crean las hojas con aparatos de consumo bajo """

    azul_2 = [2 / 255, 142 / 255, 200 / 255]
    gris = [65 / 255, 65 / 255, 65 / 255]
    azul_1 = [0 / 255, 76 / 255, 101 / 255]

    #lista_condicion = [i for i, v in enumerate(list(desciframiento.values())) if v[1] < 2 or v[4] <= 300]
    #chunks = [lista_condicion[x:x + 3] for x in range(0, len(lista_condicion), 3)]
    chunks=[1]

    for k in range(1):
        for i in range(1):
            nombre = 'Lavadora'
            carita = 1
            porcentaje = 0.1
            consumo = 50
            dinero = 255
            nota   = 'Todo bien'

            largo_encabezado = pdfmetrics.stringWidth('DESCIFRAMIENTO DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 'Montserrat-B',
                                                      12)
            canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
            texto('DESCIFRAMIENTO DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
            #cuatro_lineas(canvas)
            costado(canvas)

            nombre_ = unidecode(nombre.lower())
            abreviados = ['tv', 'bomba', 'calefaccion', 'refrigerador', 'plancha', 'estufa', 'luces', 'computadora',
                          'aire']
            for a in abreviados:
                if a in nombre_:
                    nombre_ = a
                    break



            ##Imagen y nombre
            texto(nombre.upper(), 23, azul_1, 'Montserrat-B', 60, 660, canvas)
            try:
                canvas.drawImage(f"Imagenes/icono_{nombre_}.png", 60, 580, width=65,
                                 height=65, mask='auto')
            except:
                canvas.drawImage(f"Imagenes/icono_pendiente.png", 60, 580, width=65,
                                 height=65, mask='auto')


            ##Cuadros
            canvas.drawImage(f"Imagenes/Figuras/bannerG_{carita}.png", 60, 360,
                             width=width - 120, height=200)

            #Cara
            canvas.drawImage(f"Imagenes/caraB_{carita}.png", 75, 510,
                             width=35, height=35,mask='auto')




            largo_cifra = pdfmetrics.stringWidth('{:,}'.format(dinero), 'Montserrat-B', 80)
            largo_signo = pdfmetrics.stringWidth('$', 'Montserrat-B', 40)

            ## Dinero
            texto('$', 40, azul_2, 'Montserrat-B', width - 60 - largo_cifra - largo_signo,
                  615, canvas)

            texto('{:,}'.format(dinero), 80, azul_2, 'Montserrat-B', width - 60 - largo_cifra,
                  615, canvas)

            ##Prociento
            largo_cifra = pdfmetrics.stringWidth('{:.1%}'.format(porcentaje) + ' de tu consumo', 'Montserrat-B', 15)

            texto('{:.1%}'.format(porcentaje) + ' de tu consumo', 15, azul_2, 'Montserrat-B', width - 55 - largo_cifra,
                  590, canvas)

            ##KWH
            largo_cifra = pdfmetrics.stringWidth('{:,}'.format(consumo) + ' kWh', 'Montserrat-L', 15)

            texto('{:,}'.format(consumo) + ' kWh', 15, azul_2, 'Montserrat-L', width - 60 - largo_cifra,
                  570, canvas)



            parrafos = []
            if nota == '.':
                parrafos.append(Paragraph('Su consumo es óptimo', Estilos.cuadros_bajo))
            else:
                parrafos.append(Paragraph(nota, Estilos.cuadros_bajo))
            frame = Frame(120, height - 185 - ((i + 1) * 210), width * 0.7, height * 0.1)
            frame.addFromList(parrafos, canvas)

        ##LogoRayo
        canvas.drawImage(f"Imagenes/Figuras/2_datos_rayo.png", 550, 780,
                         width=40, height=40)
        canvas.showPage()

def portada_fugas(canvas, width, height, porcentaje_fugas, costo_bimestral, atacables,Tfugas):
    """ Pagina de color azul antes de presentar los resultados."""

    canvas.setFillColorRGB(96 / 255, 192 / 255, 215 / 255)
    canvas.rect(0, 0, width, height, fill=1, stroke=False)
    canvas.drawImage("Imagenes\Spark1_blueBG.png", width - 70, height - 65, width=40, height=40)
    costado(canvas, 'white')

    parrafo_frame('<b>PÉRDIDAS DE ENERGÍA</b>', Estilos.titulo_blanco, 50, 500, .8, .1)

    costo = round(porcentaje_fugas * costo_bimestral)
    mensaje = "A continuación te presentamos puntualmente dónde encontramos pérdidas de energía y que acciones"\
                  " tomar para eliminarlas o reducir su consumo. <br/><br/>"\
                 f"Durante nuestras mediciones encontramos que el <b>{round(porcentaje_fugas * 100, 1):,}%</b> de tu consumo total y con un costo de <b>${Tfugas:,}</b>"\
                  " al bimestre, son perdidas por algún tipo de fuga, como: <br/><br/>"\
                "1° Fuga de equipo <br/><br/>2° Fuga de circuito <br/><br/>3° Fuga de Stand-by<br/><br/>"\
                f"Aproximadamente el <b>{round(atacables * 100, 1):,}%</b> de estas pérdidas son atacables y tienen un gran potencial de ahorro."

    parrafo_frame(mensaje, Estilos.negro, 49, 50, .4, .5)
    canvas.showPage()


def hojas_fugas(canvas, width, height, fugas_, tarifa):
    """ Crea la hoja que muestra donde esta la fuga, que aparatos hay y si es atacable o no """

    # fugas = {}
    # for f in fugas_.values():
    #     atacable = []
    #     no_atacable = []
    #     for f_ in fugas_.values():
    #         if f[0] == f_[0]:
    #             if f_[4].lower() == "no":
    #                 no_atacable.append(f_[1:])
    #             else:
    #                 atacable.append(f_[1:])
    #     fugas[f[0]] = [atacable, no_atacable]
    #
    # for zona, valor in fugas.items():
    #
    #     for idx, lista in enumerate(valor):
    #
    #         if not lista:
    #             continue
    #
    #         consumo = 0
    #         for perdida in lista:
    #             consumo += round (perdida[2])
    #         costo = round(consumo * tarifa)
    #
    #         if costo < 10:
    #             continue
    #
    #         count = 0
    #         count_ = 0
    #         largo = 0
    #         while True:
    #             if count >= 3:
    #                 try:
    #                     a = lista[count_][0]
    #                     count = 0
    #                     canvas.showPage()
    #                 except IndexError:
    #                     canvas.showPage()
    #                     break
    #
    #             if count == 0:
    #                 detalles_fugas(canvas, width, height, zona, idx, costo, consumo)
    #
    #             try:
    #                 pos_x = .1
    #                 w = .4
    #                 h = .2
    #
    #                 if largo < 226:
    #                     salto_linea = 100
    #                     salto_parrafo = .12
    #                 elif largo < 452:
    #                     salto_linea = 110
    #                     salto_parrafo = .13
    #                 else:
    #                     salto_linea = 120
    #                     salto_parrafo = .14
    #
    #                 pos_y = .47 - salto_parrafo * count
    #                 parrafo(f"<b>{lista[count_][0]}</b>", Estilos.base, w, h, pos_x, pos_y, canvas)
    #
    #                 inicio_y = 400
    #                 inicio_x = 55
    #                 largo = 235
    #
    #                 canvas.line(inicio_x, inicio_y - salto_linea * count, inicio_x + largo,
    #                             inicio_y - salto_linea * count)
    #
    #                 largo = pdfmetrics.stringWidth(lista[count_][0], 'Montserrat-B', 12)
    #                 if largo < 226:
    #                     off_y = 95
    #                 elif largo < 452:
    #                     off_y = 115
    #                 else:
    #                     off_y = 130
    #                 off_x = 80
    #                 parrafo_frame("Potencia", Estilos.base, width * pos_x, height * pos_y - off_y, .2, .1)
    #                 parrafo_frame("Consumo", Estilos.base, width * pos_x + off_x * 1, height * pos_y - off_y, .2, .1)
    #                 parrafo_frame("Costo", Estilos.base, width * pos_x + off_x * 2, height * pos_y - off_y, .2, .1)
    #
    #
    #                 parrafo_frame(f"<b>{round(lista[count_][1],1)} W</b>", Estilos.base, width * pos_x + 10, height * pos_y - off_y - 25, .2, .1)
    #                 if (lista[count_][2])> 1 :
    #
    #                     parrafo_frame(f"<b>{round(lista[count_][2])} kWh</b>", Estilos.base, width * pos_x + off_x * 1 + 5, height * pos_y - off_y - 25, .2, .1)
    #                 else:
    #                     parrafo_frame("1 kWh", Estilos.base, width * pos_x + off_x * 1 + 5, height * pos_y - off_y - 25, .2, .1)
    #
    #
    #                 costoP=round(lista[count_][2])* tarifa
    #
    #                 if costoP > 1:
    #                     parrafo_frame(f"<b>${round(costoP):,}</b>", Estilos.base, width * pos_x + off_x * 2 + 3, height * pos_y - off_y - 25, .2, .1)
    #                 else:
    #                     parrafo_frame(f"<b>${round(1):,}</b>", Estilos.base, width * pos_x + off_x * 2 + 3,
    #                                   height * pos_y - off_y - 25, .2, .1)
    #                 if largo < 226:
    #                     off_y = 95
    #                 elif largo < 452:
    #                     off_y = 110
    #                 else:
    #                     off_y = 120
    #
    #                 inicio_y = 310 - off_y * count
    #                 inicio_x = 133
    #                 largo_y = 50
    #                 off_x = 83
    #
    #                 canvas.line(inicio_x, inicio_y, inicio_x, inicio_y + largo_y)
    #                 canvas.line(inicio_x + off_x, inicio_y, inicio_x + off_x, inicio_y + largo_y)
    #
    #                 count += 1
    #                 count_ += 1
    #             except IndexError:
    #                 canvas.showPage()
    #                 largo = 0
    #                 break
    #             except:
    #                 print("Error desconocido al imprimir fugas")
    #                 canvas.showPage()
    #                 break


def voltaje(width, height, canvas, graficas_voltaje, nivel_voltaje):
    costado(canvas)
    gris = [65 / 255, 65 / 255, 65 / 255]
    azul_1 = [0 / 255, 76 / 255, 101 / 255]
    largo_encabezado = pdfmetrics.stringWidth('PÉRDIDAS DE ENERGÍA Y MEDICIÓN DE VOLTAJE', 'Montserrat-B', 12)
    canvas.line(60, height - 50, 60 + largo_encabezado, height - 50)
    texto('PÉRDIDAS DE ENERGÍA Y MEDICIÓN DE VOLTAJE', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
    texto('TU VOLTAJE',25,azul_1,'Montserrat-B',70,height - 120, canvas)

    if len(graficas_voltaje) == 1:
        texto('Aquí te mostramos la gráfica del voltaje durante el período de medición:', 12, gris, 'Montserrat-N', 70, height - 200, canvas)
        canvas.drawImage(graficas_voltaje[0], 60, height * 0.375, width =width * 0.8, height =height * .35)
    elif len(graficas_voltaje) == 2:
        texto('Aquí te mostramos las gráficas del voltaje durante el período de medición:', 12, gris, 'Montserrat-N', 70, height - 200, canvas)
        mult = 1.15
        ancho = (width * 0.36) * mult
        alto = (height * 0.2) * mult
        canvas.drawImage(graficas_voltaje[0], 40, 370, width=ancho, height=alto)
        canvas.drawImage(graficas_voltaje[1], 40 + ancho + 30, 370, width=ancho, height=alto)
    elif len(graficas_voltaje) == 3:
        texto('Aquí te mostramos las gráficas del voltaje durante el período de medición:', 12, gris, 'Montserrat-N', 70, height - 200, canvas)
        canvas.drawImage(graficas_voltaje[0], width * 0.35 - 15, height * 0.55, width=width * 0.35, height=height * 0.2)
        canvas.drawImage(graficas_voltaje[1], 60, height * 0.35, width=width * 0.35, height=height * 0.2)
        canvas.drawImage(graficas_voltaje[2], width * (1 - 0.35) - 60, height * 0.35, width=width * 0.35, height=height * 0.2)

    canvas.drawImage(f"Imagenes/Figuras/recuadro2.png",30, height*0.075,width=width*0.9,height=height*0.25)

    bajo = nivel_voltaje[0]
    alto = nivel_voltaje[1]

    if bajo or alto:
        color = "rojo"
    else:
        color = "verde"

    if bajo:
        picos_bajos = "picos bajos"
    else:
        picos_bajos = ""

    if alto:
        picos_altos = "picos altos"
    else:
        picos_altos = ""

    if bajo and alto:
        y = " y "
    else:
        y = ""

    mensaje = {}
    mensaje["rojo"] = f"Tu suministro de voltaje tiene {picos_bajos}{y}{picos_altos}. Es"\
            " necesario proteger ciertos equipos. Ya estamos reportando"\
            " las variaciones de voltaje con la CFE para que lo atiendan y no"\
            " te dañen tus equipos.<br/><br/>"\
            "Ponemos a tu disposición una consulta telefónica para"\
            " entender mejor estos resultados y explicarte cómo podemos"\
            " ayudarte a bajar el gasto."

    mensaje["verde"] = "Tu suministro de voltaje es bueno. Si todo el tiempo se comporta así, no es"\
            " necesario proteger tus equipos."\
            " Ponemos a tu disposición una consulta telefónica para"\
            " entender mejor estos resultados y explicarte cómo podemos"\
            " ayudarte a disminuir tu gasto."

    parrafos = []
    parrafos.append(Paragraph(mensaje[color], Estilos.cuadros_bajo))
    frame = Frame(120, height*0.075, width * 0.7, height * 0.2)
    frame.addFromList(parrafos, canvas)
    canvas.drawImage(f"Imagenes/Figuras/cara_{color}.png",30+25, height*0.10 + 75 ,width=width*0.08,height=height*0.06,mask='auto')
    canvas.showPage()
    return color

def cuadro_resumen(canvas, width, height, desciframiento, porcentaje_fugas, consumo_bimestral, costo_bimestral):
    azul_1 = [0 / 255, 76 / 255, 101 / 255]
    azul_2 = [2 / 255, 142 / 255, 200 / 255]
    gris = [65 / 255, 65 / 255, 65 / 255]
    blanco = [1, 1, 1]

    max_por_hoja = 20

    hojas = int(len(desciframiento) / max_por_hoja) + 1
    por_hoja = round((len(desciframiento) + 1) / hojas)

    def sortSecond(val):
        return val[1]

    porcentajes = []
    for id, l in enumerate(desciframiento.values()):
        porcentajes.append((id, l[2]))

    porcentajes.append((len(desciframiento.values()), porcentaje_fugas))
    porcentajes.sort(key=sortSecond, reverse=True)

    resumen = []
    for id, porc in porcentajes:
        try:
            resumen.append(list(desciframiento.values())[id])
        except:
            resumen.append(['Pérdidas', 3, porcentaje_fugas, round(porcentaje_fugas * consumo_bimestral),
                            round(porcentaje_fugas * costo_bimestral), round(porcentaje_fugas * costo_bimestral * 6),
                            ''])

    for j in range(hojas):

        costado(canvas)

        largo_encabezado = pdfmetrics.stringWidth('DESCIFRAMIENTO DE COSNUMO Y PÉRDIDAS DE ENERGÍA', 'Montserrat-B', 12)
        canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
        texto('DESCIFRAMIENTO DE PÉRDIDAS DE ENERGÍA', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
        texto("CUADRO RESUMEN", 36, azul_1, 'Montserrat-B', 60, height - 170, canvas)

        pos_x = .14
        pos_y = .73
        ancho = .12
        alto = .04

        separado = .37
        sep_porcent = separado + .12
        sep_costo = sep_porcent + .13

        parrafo("<b>Equipo</b>", Estilos.resumen, ancho, alto, pos_x, pos_y, canvas)
        parrafo("<b>Consumo</b>", Estilos.resumen, ancho, alto, pos_x + separado, pos_y, canvas)
        parrafo("<b>Porcentaje</b>", Estilos.resumen, ancho, alto, pos_x + sep_porcent, pos_y, canvas)
        parrafo("<b>Costo</b>", Estilos.resumen, ancho, alto, pos_x + sep_costo, pos_y, canvas)

        inicio_x_linea = 75
        inicio_y_linea = height * pos_y + 3
        largo = 420
        sep_linea = 30

        sep_texto = sep_linea / height
        correccion = .005

        for i in range(por_hoja):

            idx = i + j * por_hoja

            try:
                parrafo(resumen[idx][0].lower().title(), Estilos.resumen, .25, alto, pos_x,
                        pos_y - sep_texto * (i + 1) - correccion, canvas)
                parrafo(f"{resumen[idx][3]:,} kWh", Estilos.resumen, ancho, alto, pos_x + separado + .008,
                        pos_y - sep_texto * (i + 1) - correccion, canvas)
                parrafo(f"{resumen[idx][2]:.1%}", Estilos.resumen, ancho, alto, pos_x + sep_porcent + .03,
                        pos_y - sep_texto * (i + 1) - correccion, canvas)
                parrafo(f"${resumen[idx][4]:,}", Estilos.resumen, ancho, alto, pos_x + sep_costo + .01,
                        pos_y - sep_texto * (i + 1) - correccion, canvas)

                canvas.drawImage(f"Imagenes/cara_{resumen[idx][1]}.png", pos_x * width + 170,
                                 (pos_y - sep_texto * (i + 1) - correccion) * height - 18, width=20, height=20,
                                 mask='auto')

                canvas.line(inicio_x_linea, inicio_y_linea - sep_linea * i, inicio_x_linea + largo,
                            inicio_y_linea - sep_linea * i)

            except:
                i -= 1

        canvas.line(inicio_x_linea, inicio_y_linea - sep_linea * (i + 1), inicio_x_linea + largo,
                    inicio_y_linea - sep_linea * (i + 1))
        canvas.line(inicio_x_linea, inicio_y_linea - sep_linea * (i + 2), inicio_x_linea + largo,
                    inicio_y_linea - sep_linea * (i + 2))

        canvas.showPage()


def estrategia_ahorro(canvas, width, height, n, ):
    gris = [65 / 255, 65 / 255, 65 / 255]
    azul_1 = [0 / 255, 76 / 255, 101 / 255]
    consumo_subsidiado =344
    consumo_actual=744
    consumo_recomendaciones=344

    for i in range(n):
        largo_encabezado = pdfmetrics.stringWidth('ESTRATEGIA DE AHORRO', 'Montserrat-B', 12)
        canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
        texto('ESTRATEGIA DE AHORRO', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
        texto('TU ESTRATEGIA \n' + 'DE AHORRO', 36, azul_1, 'Montserrat-B', 60, height - 170, canvas)

        costado(canvas)
        canvas.showPage()

    largo_encabezado = pdfmetrics.stringWidth('ESTRATEGIA DE AHORRO', 'Montserrat-B', 12)
    canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
    texto('ESTRATEGIA DE AHORRO', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
    texto('TU ESTRATEGIA \n' + 'DE AHORRO', 36, azul_1, 'Montserrat-B', 60, height - 170, canvas)

    d = Drawing(500, 300)
    lin = LinePlot()
    lin.x = 50
    lin.y = 50
    lin.height = 225
    lin.width = 400
    if consumo_subsidiado < 500:
        data = [((0, consumo_actual), (1, consumo_actual), (1, (consumo_actual + consumo_recomendaciones) / 2)),
                ((1, (consumo_actual + consumo_recomendaciones) / 2), (1, consumo_recomendaciones),
                 (2, consumo_recomendaciones), (2, (consumo_recomendaciones + consumo_subsidiado) / 2)),
                ((2, (consumo_recomendaciones + consumo_subsidiado) / 2), (2, consumo_subsidiado),
                 (3, consumo_subsidiado)),
                ((0, 500), (3, 500))]
        lin.data = data
        lin.joinedLines = 1
        lin.xValueAxis.valueMin = 0
        lin.xValueAxis.valueMax = 3
        lin.yValueAxis.valueMin = 0
        lin.yValueAxis.valueMax = consumo_actual + 200
        lin.xValueAxis.valueStep = 10
        lin.yValueAxis.valueStep = 500
        lin.yValueAxis.labelTextFormat = '%0.0f kWh '
        lin.lines[0].strokeColor = Color(255 / 255, 0, 0, alpha=0.6)
        lin.lines[1].strokeColor = Color(255 / 255, 165 / 255, 0, alpha=0.6)
        lin.lines[2].strokeColor = Color(50 / 255, 205 / 255, 50 / 255, alpha=0.6)
        lin.lines[3].strokeColor = Color(255 / 255, 0, 0)
        lin.lines[0].strokeWidth = 10
        lin.lines[1].strokeWidth = 10
        lin.lines[2].strokeWidth = 10
        lin.lines[3].strokeWidth = 1
        lin.lines[3].strokeDashArray = (6, 8)
    else:
        data = [((0, consumo_actual), (1, consumo_actual), (1, (consumo_actual + consumo_subsidiado) / 2)),
                ((1, (consumo_actual + consumo_subsidiado) / 2), (1, consumo_subsidiado), (2, consumo_subsidiado)),
                ((0, 500), (2, 500))]
        lin.data = data
        lin.joinedLines = 1
        lin.xValueAxis.valueMin = 0
        lin.xValueAxis.valueMax = 2
        lin.yValueAxis.valueMin = 0
        lin.yValueAxis.valueMax = consumo_actual + 200
        lin.xValueAxis.valueStep = 10
        lin.yValueAxis.valueStep = 500
        lin.yValueAxis.labelTextFormat = '%0.0f kWh '
        lin.lines[0].strokeColor = Color(255 / 255, 0, 0, alpha=0.6)
        lin.lines[1].strokeColor = Color(50 / 255, 205 / 255, 50 / 255, alpha=0.6)
        lin.lines[2].strokeColor = Color(255 / 255, 0, 0)
        lin.lines[0].strokeWidth = 10
        lin.lines[1].strokeWidth = 10
        lin.lines[2].strokeWidth = 1
        lin.lines[2].strokeDashArray = (6, 8)
    d.add(lin)
    d.wrapOn(canvas, 500, 300)
    d.drawOn(canvas, 40, height - 580)

    if consumo_subsidiado < 500:
        canvas.drawImage("Imagenes\Figuras\Figuras-12.png", 140, height - 570 + (225 * 1), width=150, height=50,
                         mask='auto')
        canvas.drawImage("Imagenes\Figuras\Figuras-13.png", 260,
                         height - 550 + (225 * consumo_recomendaciones / consumo_actual), width=150, height=50,
                         mask='auto')
        canvas.drawImage("Imagenes\Figuras\Figuras-14.png", 380,
                         height - 550 + (225 * consumo_subsidiado / consumo_actual), width=150, height=50, mask='auto')
        canvas.drawImage("Imagenes\Figuras\Figuras-15.png", 140, height - 540, width=20, height=20, mask='auto')
        canvas.drawImage("Imagenes\Figuras\Figuras-16.png", 260, height - 540, width=20, height=20, mask='auto')
        canvas.drawImage("Imagenes\Figuras\Figuras-17.png", 380, height - 540, width=20, height=20, mask='auto')
        msg = 'Si implementas nuestras recomendaciones, verás tu ahorro en tres momentos:' \
              '<br/><br/>' \
              '<b>1.</b> Al implementar nuestras recomendaciones para disminuir el consumo de tu hogar, ' \
              'tu próximo recibo mostrará un pequeño ahorro.' \
              '<br/><br/>' \
              '<b>2.</b> Luego de un período de facturación completo, siguiendo nuestras recomendaciones, ' \
              'tu siguiente recibo debería mostrar un segundo nivel de ahorro.' \
              '<br/><br/>' \
              '<b>3.</b> De cuatro a cinco recibos posteriores, <b>si tu consumo está ahora por debajo del límite de tarifa DAC</b> ' \
              '(500 kWh al bimestre), verás un ahorro más significativo, pues ahora tendras tarifa subsidiada.'
    else:
        canvas.drawImage("Imagenes\Figuras\Figuras-12.png", 125, height - 570 + (225 * 1), width=150, height=50,
                         mask='auto')
        canvas.drawImage("Imagenes\Figuras\Figuras-13.png", 325,
                         height - 550 + (225 * consumo_subsidiado / consumo_actual), width=150, height=50, mask='auto')
        canvas.drawImage("Imagenes\Figuras\Figuras-15.png", 200, height - 540, width=20, height=20, mask='auto')
        canvas.drawImage("Imagenes\Figuras\Figuras-16.png", 400, height - 540, width=20, height=20, mask='auto')
        msg = 'Si implementas nuestras recomendaciones, verás tu ahorro en tres momentos:' \
              '<br/><br/>' \
              '<b>1.</b> Al implementar nuestras recomendaciones para disminuir el consumo de tu hogar, ' \
              'tu próximo recibo mostrará un pequeño ahorro.' \
              '<br/><br/>' \
              '<b>2.</b> Luego de un período de facturación completo, siguiendo nuestras recomendaciones, ' \
              'tu siguiente recibo debería mostrar un segundo nivel de ahorro.'
    parrafo("Tarifa DAC consumo mayor a 500 kWh", Estilos.plot, 0.25, 0.2, 0.17, 0.52, canvas)
    parrafo('Tarifa subsidiada consumo menor a 500 kWh', Estilos.plot, 0.267, 0.2, 0.17, 0.46, canvas)
    parrafo(msg, Estilos.plot, 0.8, 0.3, 0.1, 0.3, canvas)




    costado(canvas)
    canvas.showPage()


def medidor(canvas, width, height, robo, revisar, nivel, color_voltaje):
    """ Páginas que dicen si hay robo, si el medidor mide mal o si el voltaje está mal. """
    if not robo or not revisar or not nivel:
        logging.warning("Error con la sección de robo, medidor y voltaje.")
        raise Exception
    gris = [65 / 255, 65 / 255, 65 / 255]
    azul_1 = [0 / 255, 76 / 255, 101 / 255]

    largo_encabezado = pdfmetrics.stringWidth('EVALUACIÓN DEL MEDIDOR', 'Montserrat-B', 12)
    canvas.line(60, height - 30, largo_encabezado + 60, height - 30)
    texto('EVALUACIÓN DEL MEDIDOR', 12, gris, 'Montserrat-B', 60, height - 45, canvas)
    texto('EL ESTADO\n' + 'DE TU MEDIDOR', 36, azul_1, 'Montserrat-B', 60, height - 110, canvas)

    pos_x = 150
    pos_y = 410

    if robo.lower() in ["s", "si", "sí"]:
        candado = 2
    elif robo.lower() in ["n", "no"]:
        candado = 1
    else:
        print("Error en la celda de robo")
        candado = 1
        logging.warning("Hay un error en la celda de robo.")

    if revisar.lower() in ["s", "si", "sí"]:
        medidor = 2
    elif revisar.lower() in ["n", "no"]:
        medidor = 1
    else:
        print("Error en la celda de revisar medidor")
        medidor = 1
        logging.warning("Hay un error en la celda de revisar medidor")

    if color_voltaje == "rojo":
        rayo = 3
    elif color_voltaje == "verde":
        rayo = 1
    else:
        rayo = 2

    # if nivel in [1, 2, 3]:
    #     rayo = int(nivel)
    # else:
    #     print("Error en la celda de nivel de voltaje")
    #     rayo = 1
    #     logging.warning("Hay un error en la celda de nivel de voltaje")

    im = "Imagenes/Figuras/medidor.png"
    w, h = Image.open(im).size
    esc = 3.3
    canvas.drawImage(im, pos_x, pos_y, width=int(w / esc), height=int(h / esc), mask='auto')

    im = f"Imagenes/Figuras/medidor_{medidor}.png"
    w, h = Image.open(im).size
    esc = 3.25
    canvas.drawImage(im, pos_x + 87, pos_y + 130, width=int(w / esc), height=int(h / esc), mask='auto')

    im = f"Imagenes/Figuras/candado_{candado}.png"
    w, h = Image.open(im).size
    esc = 5
    canvas.drawImage(im, pos_x - 25, pos_y + 25, width=int(w / esc), height=int(h / esc), mask='auto')

    im = f"Imagenes/Figuras/rayo_{rayo}.png"
    w, h = Image.open(im).size
    esc = 4.6
    canvas.drawImage(im, pos_x + 177, pos_y + 36, width=int(w / esc), height=int(h / esc), mask='auto')

    cuadros_x = 90
    cuadros_y = 280
    im = f"Imagenes/Figuras/cuadro.png"
    w, h = Image.open(im).size
    esc = 2.3
    separado = int(h / esc) + 6

    for i in range(3):
        im = f"Imagenes/Figuras/cuadro.png"
        w, h = Image.open(im).size
        esc = 2.3
        canvas.drawImage(im, cuadros_x, cuadros_y - separado * i, width=int(w / esc), height=int(h / esc), mask='auto')
        if i == 0:
            im = f"Imagenes/Figuras/medidor_{medidor}.png"
            w, h = Image.open(im).size
            esc = 6.3
            canvas.drawImage(im, cuadros_x + 25, cuadros_y - separado * i + 36, width=int(w / esc), height=int(h / esc),
                             mask='auto')
            texto('EL MEDIDOR', 14, azul_1, 'Montserrat-B', cuadros_x + 100, cuadros_y - separado * i + 75, canvas)
            with open(f'Textos/medidor_{medidor}.txt', 'r', encoding='utf-8') as file:
                texto_ = file.read()
            parrafo_en_imagen(texto_, Estilos.gris_grande, cuadros_x + 92, cuadros_y - separado * i + 20, 300, 50)

        elif i == 1:
            im = f"Imagenes/Figuras/candado_{candado}.png"
            w, h = Image.open(im).size
            esc = 7.2
            canvas.drawImage(im, cuadros_x + 30, cuadros_y - separado * i + 28, width=int(w / esc), height=int(h / esc),
                             mask='auto')
            texto('ROBO DE ENERGÍA', 14, azul_1, 'Montserrat-B', cuadros_x + 100, cuadros_y - separado * i + 75, canvas)
            with open(f'Textos/robo_{candado}.txt', 'r', encoding='utf-8') as file:
                texto_ = file.read()
            parrafo_en_imagen(texto_, estilos.gris_grande, cuadros_x + 92, cuadros_y - separado * i + 20, 300, 50)

        elif i == 2:
            im = f"Imagenes/Figuras/rayo_{rayo}.png"
            w, h = Image.open(im).size
            esc = 5
            canvas.drawImage(im, cuadros_x + 37, cuadros_y - separado * i + 25, width=int(w / esc), height=int(h / esc),
                             mask='auto')
            texto('VOLTAJE', 14, azul_1, 'Montserrat-B', cuadros_x + 100, cuadros_y - separado * i + 75, canvas)
            with open(f'Textos/voltaje_{rayo}.txt', 'r', encoding='utf-8') as file:
                texto_ = file.read()
            parrafo_en_imagen(texto_, Estilos.gris_grande, cuadros_x + 92, cuadros_y - separado * i + 20, 300, 50)

    costado(canvas)
    canvas.showPage()


def notas(canvas):
    width = 595
    height = 841
    gris = [65 / 255, 65 / 255, 65 / 255]
    azul_1 = [0 / 255, 76 / 255, 101 / 255]
    largo_encabezado = pdfmetrics.stringWidth('DESCIFRAMIENTO DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 'Montserrat-B', 12)
    canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
    texto('NOTAS', 36, azul_1, 'Montserrat-B', 60, height - 170, canvas)

    largo_1 = pdfmetrics.stringWidth('LLÁMANOS', 'Montserrat-B', 12)
    canvas.setFillColorRGB(253 / 255, 211 / 255, 0 / 255)
    canvas.rect(60 + 5, height - 250 - 5, largo_1 + 15, 13 + 7, stroke=0, fill=1)
    texto('LLÁMANOS', 13, gris, 'Montserrat-B', 60 + 10, height - 250, canvas)
    msg = 'Sabemos que el comportamiento de consumo en cada casa es diferente, y la ' \
          'asesoría que te podamos dar por teléfono te pudiera ayudar a ahorrar aún ' \
          f'más. Escríbenos o llámanos al <b>(55) 7595 - 3352</b> para agendar tu llamada de asesoría con uno de nuestros expertos.' \
          '<br/><br/><b>Estamos para ayudarte a ahorrar.</b>'
    parrafo(msg, Estilos.base, 0.8, 0.3, 0.117, 0.66, canvas)

    largo_2 = pdfmetrics.stringWidth('OBSERVACIONES', 'Montserrat-B', 12)
    canvas.setFillColorRGB(253 / 255, 211 / 255, 0 / 255)
    canvas.rect(60 + 5, height - 450 - 5, largo_2 + 17, 13 + 7, stroke=0, fill=1)
    texto('OBSERVACIONES', 13, gris, 'Montserrat-B', 60 + 10, height - 450, canvas)
    msg = 'Para concluir nuestro servicio Premium realizamos una limpieza de la caja de ' \
          'circuitos y un balanceo de cargas de tu casa para brindarte una mejor ' \
          'seguridad y certeza de que tus equipos están recibiendo la energía adecuada ' \
          'sin correr riesgos de sobrevoltaje'
    parrafo(msg, Estilos.base, 0.8, 0.3, 0.117, 0.43, canvas)

    costado(canvas)
    canvas.showPage()

def contraportada(canvas, width, height):
    """ Contra portada del documento """
    canvas.drawImage('Imagenes\Figuras\Contraportada.png', 0, 0, width = width, height = height)
    canvas.showPage()

def CrearPDF():

    cliente ="Arturo Bravo"
    cliente_ = cliente.replace(' ', '_')
    filename = f"{cliente_}.pdf"
    canvas = canvas_.Canvas(filename)
    width, height = A4
    consumo_bimestral= 744
    tarifa= 5.2
    ahorro_bimestral=398
    tipo_tarifa='DAC'
    fonts()
    #Enxyy(canvas)
    portada(canvas, width, height)
    intro(canvas, width, height)
    potencial_ahorro(canvas, width, height,consumo_bimestral, tarifa,ahorro_bimestral, tipo_tarifa)
    # iluminacion(canvas, width, height, desciframiento['Luces'], detalles_luces)
    Solar(canvas)
    aparatos_grandes(canvas, width, height)

    aparatos_bajos(canvas, width, height)
    # portada_fugas(canvas, width, height, porcentaje_fugas, costo_bimestral, atacables,Tfugas)
    # hojas_fugas(canvas, width, height, fugas, tarifa)
    # cuadro_resumen(canvas, width, height, desciframiento, porcentaje_fugas, consumo_bimestral, costo_bimestral)
    estrategia_ahorro(canvas,width,height,2)

    notas(canvas)

    contraportada(canvas, width, height)

    try:
        canvas.save()
    except Exception as e:
        print("No se guardó el archivo. Revisar que no esté abierto.")