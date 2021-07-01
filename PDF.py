import locale
from reportlab.pdfgen import canvas as canvas_
from reportlab.lib.pagesizes import A4
from datetime import date
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus import Frame
from reportlab.lib import colors
from unidecode import unidecode
from PIL import Image
import Estilos
import logging
import pandas as pd
import numpy as np
from LibreriaLED import variablesLuces
from LibreriaRefris import LeeClavesR,Clasifica
from LibreriaTV import LeeClavesTV,Clasifica
from LibreriaLavaSeca import  LeeClavesLavaSeca
from libreriaPlanchas import  leerConsumoPlanchas
from libreriaMicroondas import leerConsumoMicroondas
from Caritas import definircarita
from libreriaClusterTV import armarTextoCTV
from reportlab import platypus
from  reportlab.lib.styles import ParagraphStyle as PS
from reportlab.platypus import SimpleDocTemplate

locale.setlocale(locale.LC_ALL, 'es_ES')
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


def parrafo_en_imagen(texto, estilo, pos_x, pos_y, ancho, alto,canvas):
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
    width=600
    height=841
    blanco = [1, 1, 1]
    negro = [0, 0, 0]
    mensaje = {0: "ATACABLE", 1: "NO ATACABLE",2:"ATACABLE CON RESERVA"}
    espacio = 16
    for indx, letra in enumerate(mensaje[idx]):
        texto(letra, 14, blanco, 'Montserrat-B', width * (pos_x + .346), height * (pos_y + 0.28) - espacio * indx,
              canvas)


def detalles_fugas(canvas, width, height, zona, idx, costo, consumo,porciento):
    """ Crea una pagina nueva para las fugas """
    azul_1 = [0 / 255, 76 / 255, 101 / 255]
    azul_2 = [2 / 255, 142 / 255, 200 / 255]
    gris = [65 / 255, 65 / 255, 65 / 255]
    blanco = [1, 1, 1]
    largo_encabezado = pdfmetrics.stringWidth('DESCIFRAMIENTO DE COSNUMO Y PÉRDIDAS DE ENERGÍA', 'Montserrat-B', 12)
    canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
    texto('DESCIFRAMIENTO DE PÉRDIDAS DE ENERGÍA', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
    largo_titulo = pdfmetrics.stringWidth(zona.upper(), 'Montserrat-B', 12)
    if len(zona)< 35:
        parrafo_frame(f"<b>{zona.upper()}</b>", Estilos.titulos, 60, 500, .8, .25,canvas)
    if 55 >= len(zona)>= 35:
        parrafo_frame(f"<b>{zona.upper()}</b>", Estilos.titulos3, 60, 500, .9, .25, canvas)
    if len(zona) > 55:
        parrafo_frame(f"<b>{zona.upper()}</b>", Estilos.titulos4, 60, 500, .9, .25, canvas)
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
        tamano_dinero = 100
    largo_precio = pdfmetrics.stringWidth('{:,}'.format(costo), 'Montserrat-B', tamano_dinero)
    largo_signo = pdfmetrics.stringWidth('$', 'Montserrat-B', 70)
    texto('{:,}'.format(costo), tamano_dinero, azul_2, 'Montserrat-B', width - margen - largo_precio, height * 0.5 + 60,
          canvas)
    texto('$', 70, azul_2, 'Montserrat-B', width - margen - largo_precio - largo_signo, height * 0.5 + 60, canvas)
    largo_cons = pdfmetrics.stringWidth('{:,}'.format(porciento), 'Montserrat-B', 30)
    largo_kwh = pdfmetrics.stringWidth('kWh', 'Montserrat-B', 30)
    texto('{:,}'.format(porciento), 15, azul_2, 'Montserrat-B', width - margen - largo_cons - largo_kwh - 35,
          height * 0.5 + 30, canvas)
    texto('% de tu consumo', 15, azul_2, 'Montserrat-B', width - margen - largo_kwh-55, height * 0.5 + 30, canvas)
    largo_cons = pdfmetrics.stringWidth('{:,}'.format(consumo), 'Montserrat', 30)
    largo_kwh = pdfmetrics.stringWidth('kWh', 'Montserrat', 30)
    texto('{:,}'.format(consumo), 20, azul_2, 'Montserrat', width - margen - largo_cons - largo_kwh + 35,
          height * 0.5 + 0, canvas)
    texto('kWh', 20, azul_2, 'Montserrat', width - margen - largo_kwh+28, height * 0.5 + 0, canvas)
    factor = .25
    w, h = Image.open(f"Imagenes/Figuras/Figuras1-0{idx + 1}.png").size
    pos_x = .55
    pos_y = 0.13
    canvas.drawImage(f"Imagenes/Figuras/figuras1-0{idx + 1}.png", width * pos_x, (height * pos_y)-80, w * factor*0.88, h * factor*0.88)
    frame = Frame(width * 0.55 + 10, height * 0.05 - 125, width * 0.3, height * 0.5)
    #texto('¿QUÉ HACER?', 16, blanco, 'Montserrat-B', width * (pos_x + .055), height * (pos_y + .323), canvas)
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

def Solar(canvas,tarifa,costo, consumo, SolarS):
    gris = [65 / 255, 65 / 255, 65 / 255]
    AMA_1 = [235 / 255, 200 / 255, 0 / 255]
    Azul = (0 / 255, 76 / 255, 101 / 255)
    width, height = A4
    cobrada    =  float(consumo)
    consumo    = SolarS.loc['Medidor','Total']
    costoCob = consumo * DAC
    costo   = float(costo)
    totalSemana= SolarS.loc['ProduccionSem','Total']
    totalBimestre= SolarS.loc['ProduccionBim','Total']
    factor=0.5
    x=0
    y=80
    w, h = Image.open(f"Imagenes/Figuras/Psolar.png").size
    canvas.drawImage(f"Imagenes/Figuras/Psolar.png", x + 55, y + 5, w * factor, h * factor)
    w, h = Image.open(f"Imagenes/Figuras/PsolarA.png").size
    canvas.drawImage(f"Imagenes/Figuras/PsolarA.png", x + 10, y + 450, w * factor, h * factor)
    parrafo_frame("<b>${:,}</b>".format(round(costoCob)), Estilos.azul_1_grande, x + 430, y + 380, .15, .15, canvas)
    parrafo_frame("<b>${:,}</b>".format(round(costo)), Estilos.azul_1_grande, x + 290, y + 380, .15, .15, canvas)
    parrafo_frame("<b>{:,}kWh</b>".format(round(cobrada-totalBimestre)), Estilos.azul_1_grande, x + 430, y + 415, .15, .15, canvas)
    parrafo_frame("<b>{:,}kWh</b>".format(round(cobrada)), Estilos.azul_1_grande, x + 290, y + 415, .15, .15, canvas)
    parrafo_frame("<b>{:,}kWh</b>".format(round(totalSemana)), Estilos.azul_1_grande1, 410, 335, .2, .15, canvas)
    parrafo_frame("<b>{:,}kWh</b>".format(round(totalBimestre)), Estilos.azul_1_grande1, 410, 285, .2, .15, canvas)
    parrafos = []
    notasA = 'Tus paneles Solares están produciendo lo suficiente pero creemos que podrían tener una mayor producción, ' \
             'algún factor no deja sacarles el máximo provecho'
    notasB = 'Tus paneles Solares tienen un buen desempeño, producen la energía esperada tomando en cuenta la temporada del año'
    notasC = 'Tus paneles solares se encuentran muy por debajo de lo esperado, algún factor no deja que funcionen correctamente'

    parrafos.append(Paragraph(notasA, Estilos.azul_1_grande2))
    frame = Frame(60, 450, 190, 200)
    frame.addFromList(parrafos, canvas)
    notasAA = 'Pico máximo: ' + str(SolarS.loc['MaxW','F1'])+'W'
    notasAB = 'Producción máxima en un día: '+str(SolarS.loc['MaxkWh','F1']) +'kWh'
    notasAC = 'Producción mínima en un día: '+str(SolarS.loc['Min','F1']) +'kWh'
    notasBA = 'Pico máximo: ' + str(SolarS.loc['MaxW','F2'])+'W'
    notasBB = 'Producción máxima en un día: '+str(SolarS.loc['MaxkWh','F2']) +'kWh'
    notasBC = 'Producción mínima en un día: '+str(SolarS.loc['Min','F2']) +'kWh'

    if not SolarS.loc['MaxW','F3']!= np.nan:
        notasAA = 'Pico máximo: ' + str(SolarS.loc['MaxW','F3'])+'W'
        notasAB = 'Producción máxima en un día: '+str(SolarS.loc['MaxkWh','F3']) +'kWh'
        notasAC = 'Producción mínima en un día: '+str(SolarS.loc['Min','F3']) +'kWh'

    parrafos.append(Paragraph(notasAA, Estilos.azul_2_chico2))
    frame = Frame(300, 150, 190, 200)
    frame.addFromList(parrafos, canvas)
    parrafos.append(Paragraph(notasAB, Estilos.azul_2_chico2))
    frame = Frame(300, 120, 190, 200)
    frame.addFromList(parrafos, canvas)
    parrafos.append(Paragraph(notasAC, Estilos.azul_2_chico2))
    frame = Frame(300, 90, 190, 200)
    frame.addFromList(parrafos, canvas)
    parrafos.append(Paragraph(notasBA, Estilos.azul_2_chico2))
    frame = Frame(300, 20, 190, 200)
    frame.addFromList(parrafos, canvas)
    parrafos.append(Paragraph(notasBB, Estilos.azul_2_chico2))
    frame = Frame(300, -10, 190, 200)
    frame.addFromList(parrafos, canvas)
    parrafos.append(Paragraph(notasBC, Estilos.azul_2_chico2))
    frame = Frame(300, -40, 190, 200)
    frame.addFromList(parrafos, canvas)


    largo_encabezado = pdfmetrics.stringWidth('DESCIFRAMIENTO DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 'Montserrat-B', 12)
    canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
    texto('DESCIFRAMIENTO DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
    texto('PRODUCCIÓN SOLAR', 36, AMA_1, 'Montserrat-B', 60, height - 130, canvas)
    texto('Producción de energía solar semanal', 12, Azul, 'Montserrat-B', 145, 440, canvas)
    texto('Producción de energía solar bimestral', 12, Azul, 'Montserrat-B', 145, 390, canvas)
    texto('Producción solar #1', 12, Azul, 'Montserrat-B', 145, 340, canvas)
    texto('Producción solar #2', 12, Azul, 'Montserrat-B', 145, 200, canvas)
    costado(canvas)
    canvas.showPage()


def intro(canvas, width, height, datos=5287899):
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


def potencial_ahorro(canvas, width, height,consumo_bimestral, tarifaf,costo, ahorro_bimestral, tipo_tarifa):
    """ Se hace la página que muestra el potencial de ahorro """
    tarifa= float(costo)/float(consumo_bimestral)
    NoPaneles=round(ahorro_bimestral/68)
    ahorro_paneles=round(NoPaneles*13500)
    co2=round(ahorro_bimestral*0.52*6)
    arboles=round(co2*0.015)
    nuevo_consumo= consumo_bimestral-ahorro_bimestral
    costo_bimestral=float(costo)
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
    if consumo_bimestral > 1000:
        w, h = Image.open(f"Imagenes/Figuras/barra_consumo1.png").size
    else:
        w, h = Image.open(f"Imagenes/Figuras/barra_consumo.png").size
    w = w * factor
    h = h * factor
    x = (width - w) / 2
    y = height * 0.6
    if consumo_bimestral > 1000:
        Mx = int(round(consumo_bimestral +100,-2))
        x2 =  70+(consumo_bimestral*410/Mx)
        x1=   70+(nuevo_consumo*410/Mx)
        canvas.drawImage(f"Imagenes/Figuras/barra_consumo1.png", x, y - 20, w, h)
        texto('500 kWh', 8, (0, 0, 0), 'Montserrat-B', 220, height - 325, canvas)
    else:
        Mx = 1000
        x2 = 70 + (consumo_bimestral * 410 / Mx)
        x1 = 70 + (nuevo_consumo * 410 / Mx)
        canvas.drawImage(f"Imagenes/Figuras/barra_consumo.png", x, y - 20, w, h)
        texto('500 kWh', 8, (0, 0, 0), 'Montserrat-B', 270, height - 325, canvas)
    diff=consumo_bimestral- nuevo_consumo
    texto('0 kWh', 8, (0,0,0), 'Montserrat-B', 85, height-325 , canvas)
    texto('Tarifa DAC', 8, (20, 0, 0), 'Montserrat-B', 265, height - 305, canvas)
    texto(str(round(Mx,-1)) +'kWh', 8, (0, 0, 0), 'Montserrat-B', 480, height - 325, canvas)
    factor = .5
    w_, h_ = Image.open(f"Imagenes/Figuras/rayo.png").size
    w_ = w_ * factor
    h_ = h_ * factor
    canvas.drawImage(f"Imagenes/Figuras/rayo.png", x1, y - 50, w_, h_,
                     mask='auto')
    canvas.drawImage(f"Imagenes/Figuras/rayo.png", x2, y - 50, w_, h_,
                     mask='auto')
    if diff > 300:
        parrafo_frame("<b>Tu nuevo consumo energético:</b>", Estilos.azul_1_chico,x1, y - 130, .15, .1,canvas)
        parrafo_frame("<b>{:,} kWh</b>".format(round(nuevo_consumo)), Estilos.azul_1_grande, x1-50 , y - 205, .15, .15,canvas)
        parrafo_frame("<b>${:,}</b>".format(round(nuevo_consumo*tarifa), asterisco=asterisco), Estilos.azul_1_grande, x1 , y - 191, .15, .15, canvas)
    else:
        parrafo_frame("<b>Tu nuevo consumo energético:</b>", Estilos.azul_1_chico, x1-50, y - 130, .15, .1, canvas)
        parrafo_frame("<b>{:,} kWh</b>".format(round(nuevo_consumo)), Estilos.azul_1_grande, x1-50, y - 205, .15, .15,
                      canvas)
        parrafo_frame("<b>${:,}</b>".format(round(nuevo_consumo * tarifa), asterisco=asterisco), Estilos.azul_1_grande,
                      x1-50, y - 191, .15, .15, canvas)
    parrafo_frame("<b>Tu consumo energético actual:</b>", Estilos.azul_1_chico, x2,  y - 130, .15, .1, canvas)
    parrafo_frame("<b>{:,} kWh</b>".format(round(consumo_bimestral)), Estilos.azul_1_grande,x2, y - 205, .15, .15, canvas)
    parrafo_frame("<b>${:,}</b>".format(round(costo_bimestral), asterisco=asterisco), Estilos.azul_1_grande, x2, y - 191, .15, .15, canvas)
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

def iluminacion(canvas, width, height, luces,Tarifa):
    """ Se crean las páginas en donde se muestra el consumo de luz a detalle """
    Luces = luces.copy()
    Luces = Luces.loc[Luces['L'].apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna().index]
    Luces.sort_values(by=['L'], inplace=True, ascending=False)
    TotalC=Luces['K'].sum() # Suma de consumos de lueces en el consumo total de casa (KWh)
    TotalP=Luces['L'].sum() # Suma de porcentaje total de luces en el consumo total de casa (%)
    TotalD = Luces['M'].sum() # Suma de costo de luces en el costo total de casa ($)
    # Se inicializan los conteos de si ya existen focos LED, focos ineficientes y cálculos de ROI
    conteoled = 1
    conteoNOled = 1
    conteoROI = 1

    if TotalD<=200:
        notasA = 'Tu gasto en iluminación es óptimo  '
        hh=110
        carita=1
    elif 200<TotalD and TotalD<=700:
        notasA = 'Tu gasto en iluminación mayor al promedio  '
        hh=120
        carita=2
    elif TotalD>700:
        notasA = 'Tu gasto en iluminación es muy alto  '
        hh=110
        carita=3
    #luces.sort_values
    azul_1 = [0 / 255, 76 / 255, 101 / 255]
    azul_2 = [2 / 255, 142 / 255, 200 / 255]
    gris = [65 / 255, 65 / 255, 65 / 255]
    blanco = [1, 1, 1]
    gristabla = colors.Color(red=(65 / 255), green=(65 / 255), blue=(65 / 255))
    azul2tabla = colors.Color(red=(2 / 255), green=(142 / 255), blue=(200 / 255))
    largo_encabezado = pdfmetrics.stringWidth('DESCIFRAMIENTO DE CONSUMO EN LUMINARIAS', 'Montserrat-B', 12)
    canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
    texto('DESCIFRAMIENTO DE CONSUMO EN LUMINARIAS', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
    texto('ILUMINACIÓN', 36, azul_1, 'Montserrat-B', 60, height - 170, canvas)
    canvas.drawImage(f"Imagenes/icono_luces.png", 60, height - 295, width=115, height=115)
    canvas.drawImage(f"Imagenes/cara_{carita}.png", 490, 590, width=60, height=60)
    #parrafos='Tu gasto en uluminación es muy alto'
    parrafos = []
    #notasA = 'Tu gasto en iluminación es muy alto  '
    notasB = 'Normalmente vemos gastos alrededor de $200 pesos al bimestre(35kWh) para una casa completa'
    notasC = 'Como parte de nuestros servicios, encontramos estas luminarias para enfocar esfuerzos en lo que vale la pena reemplazarlos'
    parrafos.append(Paragraph(notasA, Estilos.cuadros_bajo))
    frame = Frame(60, hh, width * 0.35, height * 0.5)
    frame.addFromList(parrafos, canvas)
    parrafos.append(Paragraph(notasB, Estilos.cuadros_bajo))
    frame = Frame(60, 90, width * 0.35, height * 0.5)
    frame.addFromList(parrafos, canvas)
    parrafos.append(Paragraph(notasC, Estilos.cuadros_bajo))
    frame = Frame(60, 40, width * 0.35, height * 0.5)
    frame.addFromList(parrafos, canvas)

    margen = 50
    dinero = round(TotalD)
    if len(str(dinero)) < 4:
        tamano_dinero = 100
    else:
        tamano_dinero = 70
    largo_precio = pdfmetrics.stringWidth('{:,}'.format(dinero), 'Montserrat-B', tamano_dinero)
    largo_signo = pdfmetrics.stringWidth('$', 'Montserrat-B', 50)
    texto('{:,}'.format(dinero), tamano_dinero, azul_2, 'Montserrat-B', width - margen - largo_precio,
          height * 0.5 + 90, canvas)
    texto('$', 60, azul_2, 'Montserrat-B', width - margen - largo_precio - largo_signo, height * 0.5 + 90, canvas)
    consumo = round(TotalC)
    largo_cons = pdfmetrics.stringWidth('{:,}'.format(consumo), 'Montserrat-B', 20)
    largo_kwh = pdfmetrics.stringWidth('kWh', 'Montserrat-B', 20)
    texto('{:,}'.format(consumo), 20, azul_2, 'Montserrat-B', width - margen - largo_cons - largo_kwh - 5,
          height * 0.5 + 50, canvas)
    texto('kWh', 20, azul_2, 'Montserrat-B', width - margen - largo_kwh, height * 0.5 + 50, canvas)

    porcentaje = str(round(TotalP * 100, 1))
    largo_pct = pdfmetrics.stringWidth(porcentaje, 'Montserrat-N', 15)
    largo_sign = pdfmetrics.stringWidth('% de tu consumo', 'Montserrat-N', 15)
    texto(porcentaje, 15, gris, 'Montserrat-N', width - margen - largo_pct - largo_sign, height * 0.5 + 25, canvas)
    texto('% de tu consumo', 15, gris, 'Montserrat-N', width - margen - largo_sign, height * 0.5 +25, canvas)
    texto('Rango aceptable de $50 a $200', 15, gris, 'Montserrat-N', width - margen - largo_sign-100, height * 0.5 , canvas)

    canvas.drawImage("Imagenes/Figuras/cuadro_luces_1.png", 70, 100, 480, 250)
    canvas.setLineWidth(.3)
    canvas.line(254,100, 254, 315)
    canvas.line(154, 100, 154, 315)
    canvas.line(205, 100, 205, 315)
    altura=266
    i=0
    Luces['D']=Luces['D'].str.replace('Luces ','')
    for index, luz in Luces.iterrows():
        i=i+1
        luzz=luz[3]
        porc=str(round(luz[11]*100,1))+' %'
        cost='$ '+str(round(luz[12]))
        tex= str(luz[13])
        largoTx=(len(tex))
        tex,conteoled,conteoNOled,conteoROI = variablesLuces(luz[0], luz[9], luz[10],tex,Tarifa,luz[16],luz[4],conteoNOled,conteoled,conteoROI) # Está usando columnas, no renglones para los índices

        if len(luzz) < 15:
            parrafos.append(Paragraph(luzz, Estilos.Lumi))
            frame = Frame(72, altura - 18, 80, 60)
            frame.addFromList(parrafos, canvas)

        if 15<=len(luzz)<35:
            parrafos.append(Paragraph(luzz,Estilos.Lumi))
            frame = Frame(72, altura-15, 80, 60)
            frame.addFromList(parrafos, canvas)

        if  35<=len(luzz)<55:
            parrafos.append(Paragraph(luzz,Estilos.Lumi2))
            frame = Frame(72, altura-10, 80, 60)
            frame.addFromList(parrafos, canvas)

        if  55<=len(luzz)<75:
            parrafos.append(Paragraph(luzz,Estilos.Lumi3))
            frame = Frame(72, altura-8, 80, 60)
            frame.addFromList(parrafos, canvas)

        if len(luzz) >= 75:
            parrafos.append(Paragraph(luzz, Estilos.Lumi5))
            frame = Frame(72, altura - 5, 80, 60)
            frame.addFromList(parrafos, canvas)
        parrafos.append(Paragraph(porc, Estilos.cuadros_bajo))
        frame = Frame(160, altura, 90, 50)
        frame.addFromList(parrafos, canvas)
        parrafos.append(Paragraph(cost, Estilos.cuadros_bajo))
        frame = Frame(210, altura, 90, 50)
        frame.addFromList(parrafos, canvas)
        parrafoss=[]
        if largoTx<45:
            parrafoss.append(Paragraph(tex, Estilos.Lumi))
            frame = Frame(258, altura - 5, 295, 60)
        elif 45<=largoTx<150:
            parrafoss.append(Paragraph(tex, Estilos.Lumi))
            frame = Frame(258, altura-0, 295, 60)
        elif largoTx>150 and largoTx<=210:
            parrafoss.append(Paragraph(tex, Estilos.Lumi2))
            frame = Frame(258, altura+5, 65)
        elif 350>=largoTx>210:
            parrafoss.append(Paragraph(tex, Estilos.Lumi3))
            frame = Frame(258, altura+5, 295, 65)
        elif largoTx > 350:
            parrafoss.append(Paragraph(tex, Estilos.Lumi4))
            frame = Frame(258, altura + 5, 295, 65)
        frame.addFromList(parrafoss, canvas)
        canvas.line(70, altura + 51, 548, altura + 51)
        altura=altura-50
        cont=0
        if i==4 or i==16 or i==25:

            largo= len(luces)-4
            if i==16:
                largo = len(luces) - 15
            if i==24:
                largo = len(luces) - 24
            altura = 500
            canvas.showPage()
            largo_encabezado = pdfmetrics.stringWidth('DESCIFRAMIENTO DE CONSUMO EN LUMINARIAS', 'Montserrat-B', 12)
            canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
            canvas.setLineWidth(.3)
            texto('DESCIFRAMIENTO DE CONSUMO EN LUMINARIAS', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
            if largo > 4:
                canvas.drawImage("Imagenes/Figuras/lucesabajo.png", 70, 500-((largo-1)*50), 480, (largo*50))
                canvas.drawImage("Imagenes/Figuras/lucesarriba.png", 70, 548 , 480, 30)
            else:

                canvas.drawImage("Imagenes/Figuras/cuadro_luces_1.png", 70, ((altura+15) - ((largo-1) * 60)), 480, ((largo) * 60))
                canvas.line(254, altura-((largo-4)*40), 254, altura-((largo-4)*40))
                canvas.line(154, altura-((largo-4)*40), 154, altura-((largo-4)*33))
                canvas.line(205, altura-((largo-4)*40), 205, altura-((largo-4)*33))

            texto('ILUMINACIÓN', 36, azul_1, 'Montserrat-B', 60, height - 170, canvas)
            texto('Continuación...', 12, gris, 'Montserrat-B', 60, height - 240, canvas)
            canvas.setLineWidth(.3)
    costado(canvas)
    canvas.showPage()
    return carita

def Dicc_Aparatos(nombre):
    nombre_ = unidecode(nombre.lower())
    abreviados = ['aspiradora','tv', 'bomba', 'calentador', 'refrigerador', 'estufa', 'luces', 'computadora', 'secadora de cabello',
                  'aire acondicionado', 'cafetera', 'lavadora', 'secadora', 'plancha', 'lavavajillas', 'horno',
                  'cocina', 'pelo', 'laptop', 'monitor', 'congelador', 'minibar', 'campana', 'microondas', 'triturador', 'cava',
                  'hielos', 'sonido', 'dispensador', 'boiler','xbox','vapor']
    for a in abreviados:
        if a in nombre_:
            nombre_ = a
    return nombre_



def Recomendaciones(Claves,consumo,DAC,Uso):
    Consejos=''
    ClavesS = Claves.split(',')
    if ClavesS[0] == 'RF':
        Consejos = LeeClavesR(Claves)
    if ClavesS[0] == 'TV':
        Consejos = LeeClavesTV(Claves, Uso, consumo, DAC)
    if ClavesS[0] == 'LV' or ClavesS[0] == 'SC':
        Consejos = LeeClavesLavaSeca(Claves, consumo)
    if Claves == 'PL':
        Consejos = leerConsumoPlanchas(consumo)
    if Claves == 'MC':
        Consejos = leerConsumoMicroondas(consumo)

    return Consejos





def aparatos_grandes(canvas, width, height,aparatosG,tarifa):
    """ Se crean las páginas en donde se muestran los consumos que ocupan una página completa """

    azul_1 = [0 / 255, 76 / 255, 101 / 255]
    azul_2 = [2 / 255, 142 / 255, 200 / 255]
    gris = [65 / 255, 65 / 255, 65 / 255]
    blanco = [1, 1, 1]
    for index,aparato in aparatosG.iterrows():
        nombre = aparato[3]
        carita = aparato[0]
        porcentaje = aparato[11]
        consumo = round(aparato[10])
        dinero =  round(aparato[12])
        Uso = aparato[7]
        notas = aparato[13]
        Claves=aparato[16]
        nombre_=Dicc_Aparatos(nombre)
        parrafos = []
        largo_encabezado = pdfmetrics.stringWidth('DESCIFRAMIENTO DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 'Montserrat-B', 12)
        canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
        texto('DESCIFRAMIENTO DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
        if len(nombre)<20:
            texto(nombre.upper(), 36, azul_1, 'Montserrat-B', 60, height - 130, canvas)
        elif len(nombre)>=20 and len(nombre)<28:
            parrafos.append(Paragraph(nombre.upper(), Estilos.titulos2))
            frame = Frame(60, 620, 550, 150)
            frame.addFromList(parrafos, canvas)
        elif len(nombre)>=28:
            parrafos.append(Paragraph(nombre.upper(), Estilos.titulos3))
            frame = Frame(60, 620, 550, 150)
            frame.addFromList(parrafos, canvas)
        try:
            canvas.drawImage(f"Imagenes/icono_{nombre_}.png", 70, height - 285, width=115, height=115)
        except:
            canvas.drawImage(f"Imagenes/icono_pendiente.png", 70, height - 285, width=115, height=115)
        ##Carita
        canvas.drawImage(f"Imagenes/cara_{carita}_c.png", 100, 470, width=55, height=55)
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
            parrafos.append(Paragraph(str(notas), Estilos.aparatos2))
        frame = Frame(60, 20, width * 0.35, height * 0.5)
        frame.addFromList(parrafos, canvas)
        canvas.drawImage(f"Imagenes/Figuras/Figuras-03.png", width * .47, height * 0.05, width * .45, height * .5)
        texto('¿QUÉ HACER?', 22, (255, 255, 255), 'Montserrat-B', width * .555, height * 0.512, canvas)


# Automatizacion ######################
        Consejos=Recomendaciones(Claves,consumo,tarifa,Uso)
# Automatizacion  ######################
        parrafos.append(Paragraph(Consejos, Estilos.aparatos2))
        frame = Frame(282, 46, width * 0.442, height * 0.44,showBoundary = 0 )
        frame.addFromList(parrafos, canvas)

        ##LogoRayo
        canvas.drawImage(f"Imagenes/Figuras/2_datos_rayo.png", 550, 780,
                         width=40, height=40)
        costado(canvas)
        canvas.showPage()


def aparatos_bajos(canvas, width, height,aparatosM,aparatosC,tarifa):
    """ Se crean las hojas con aparatos de consumo bajo """
    Medio=False
    azul_2 = [2 / 255, 142 / 255, 200 / 255]
    gris = [65 / 255, 65 / 255, 65 / 255]
    azul_1 = [0 / 255, 76 / 255, 101 / 255]
    i=0
    altura = 650
    for index,aparato in aparatosM.iterrows():
        nombre = aparato[3]
        carita = aparato[0]
        porcentaje = aparato[11]
        consumo = round(aparato[10])
        dinero = round(aparato[12])
        Claves= aparato[16]
        Uso=0
        largo_encabezado = pdfmetrics.stringWidth('DESCIFRAMIENTO DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 'Montserrat-B',12)
        canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
        texto('DESCIFRAMIENTO DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
        costado(canvas)
        nombre_ = Dicc_Aparatos(nombre)
        ##Imagen y nombre
        if len(nombre)< 35:
            texto(nombre.upper(), 25, azul_1, 'Montserrat-B', 60, altura+25, canvas)
        elif 23 <= len(nombre) < 40:
            texto(nombre.upper(), 20, azul_1, 'Montserrat-B', 60, altura + 25, canvas)
        elif 40 <= len(nombre) < 60:
            #texto(nombre.upper(), 18, azul_1, 'Montserrat-B', 60, altura + 25, canvas)
            parrafos=[]
            parrafos.append(Paragraph(nombre.upper(), Estilos.titulos5))
            frame = Frame(60, altura -38, 500, 100)
            frame.addFromList(parrafos, canvas)

        elif len(nombre) >= 60 :
            #texto(nombre.upper(), 15, azul_1, 'Montserrat-B', 60, altura + 25, canvas)
            parrafos=[]
            parrafos.append(Paragraph(nombre.upper(), Estilos.titulos6))
            frame = Frame(60, altura-35 , 500, 100)
            frame.addFromList(parrafos, canvas)
        try:
            canvas.drawImage(f"Imagenes/icono_{nombre_}.png", 60, altura-80, width=65,
                             height=65, mask='auto')
        except:
            canvas.drawImage(f"Imagenes/icono_pendiente.png", 60, altura-80, width=65,
                           height=65, mask='auto')
        ##Cuadros
        canvas.drawImage(f"Imagenes/Figuras/bannerG_{carita}.png", 60, altura-255,
                         width=width - 120, height=160)
        #Cara
        canvas.drawImage(f"Imagenes/caraB_{carita}.png", 75, altura-150,
                         width=35, height=35,mask='auto')
        largo_cifra = pdfmetrics.stringWidth('{:,}'.format(dinero), 'Montserrat-B', 80)
        largo_signo = pdfmetrics.stringWidth('$', 'Montserrat-B', 40)
        ## Dinero
        texto('$', 40, azul_2, 'Montserrat-B', width - 60 - largo_cifra - largo_signo,
              altura-45, canvas)

        texto('{:,}'.format(dinero), 80, azul_2, 'Montserrat-B', width - 60 - largo_cifra,
              altura-45, canvas)
        ##Prociento
        largo_cifra = pdfmetrics.stringWidth('{:.1%}'.format(porcentaje) + ' de tu consumo', 'Montserrat-B', 15)
        texto('{:.1%}'.format(porcentaje) + ' de tu consumo', 15, azul_2, 'Montserrat-B', width - 55 - largo_cifra,
              altura-70, canvas)
        ##KWH
        largo_cifra = pdfmetrics.stringWidth('{:,}'.format(consumo) + ' kWh', 'Montserrat-L', 15)
        texto('{:,}'.format(consumo) + ' kWh', 15, azul_2, 'Montserrat-L', width - 60 - largo_cifra,
              altura-90, canvas)
        parrafos = []
        # Automatizacion ######################
        if not pd.isna(Claves):
            nota = Recomendaciones(Claves, consumo, tarifa, Uso)
        # Automatizacion  ######################
        if nota == '.':
            parrafos.append(Paragraph('Su consumo es óptimo', Estilos.cuadros_bajo))
        else:
            parrafos.append(Paragraph(str(nota), Estilos.cuadros_bajo))
        frame = Frame(120, altura-270, width * 0.7, height * 0.2)
        frame.addFromList(parrafos, canvas)
        ##LogoRayo
        canvas.drawImage(f"Imagenes/Figuras/2_datos_rayo.png", 550, 780,
                         width=40, height=40)
        altura=altura-320
        i = i + 1
        Medio=True
        if i==2:
            canvas.showPage()
            i=0
            altura=660
            Medio=False
    if i%2 != 0:
        altura=490-400
        i=2
    else:
        altura = 490
        i=0
    if Medio:
        largo=len(aparatosC)+1
    else:
        largo = len(aparatosC)-3




    for index, aparato in aparatosC.iterrows():
        nombre = aparato[3]
        carita = aparato[0]
        porcentaje = aparato[11]
        consumo = round(aparato[10])
        dinero = round(aparato[12])
        nota = aparato[13]
        Claves =aparato[16]
        largo_encabezado = pdfmetrics.stringWidth('DESCIFRAMIENTO DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 'Montserrat-B',12)
        canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
        texto('DESCIFRAMIENTO DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
        # cuatro_lineas(canvas)
        costado(canvas)
        nombre_ = Dicc_Aparatos(nombre)
        ##Imagen y nombre
        if len(nombre)<35:
            texto(nombre.upper(), 23, azul_1, 'Montserrat-B', 60,altura+190, canvas)
        elif len(nombre)>=35 and len(nombre)<40:
            texto(nombre.upper(), 20, azul_1, 'Montserrat-B', 60, altura + 190, canvas)
        elif 60>len(nombre)>=40:
            texto(nombre.upper(), 15, azul_1, 'Montserrat-B', 60, altura + 190, canvas)
        elif len(nombre)>=60:
            texto(nombre.upper(), 13, azul_1, 'Montserrat-B', 60, altura + 190, canvas)
        try:
            canvas.drawImage(f"Imagenes/icono_{nombre_}.png", 60, altura+90, width=65,
                             height=65, mask='auto')
        except:
            canvas.drawImage(f"Imagenes/icono_pendiente.png", 60, altura+90, width=65,
                             height=65, mask='auto')
        ##Cuadros
        canvas.drawImage(f"Imagenes/Figuras/bannerC_{carita}.png", 60, altura,
                         width=width - 120, height=70)
        # Cara
        canvas.drawImage(f"Imagenes/caraB_{carita}.png", 75,altura+30,
                         width=35, height=35, mask='auto')
        largo_cifra = pdfmetrics.stringWidth('{:,}'.format(dinero), 'Montserrat-B', 80)
        largo_signo = pdfmetrics.stringWidth('$', 'Montserrat-B', 40)
        ## Dinero
        texto('$', 40, azul_2, 'Montserrat-B', width - 60 - largo_cifra - largo_signo,
              altura+125, canvas)
        texto('{:,}'.format(dinero), 80, azul_2, 'Montserrat-B', width - 60 - largo_cifra,
              altura+125, canvas)
        ##Prociento
        largo_cifra = pdfmetrics.stringWidth('{:.1%}'.format(porcentaje) + ' de tu consumo', 'Montserrat-B', 15)
        texto('{:.1%}'.format(porcentaje) + ' de tu consumo', 15, azul_2, 'Montserrat-B', width - 55 - largo_cifra,
             altura+100, canvas)
        ##KWH
        largo_cifra = pdfmetrics.stringWidth('{:,}'.format(consumo) + ' kWh', 'Montserrat-L', 15)
        texto('{:,}'.format(consumo) + ' kWh', 15, azul_2, 'Montserrat-L', width - 60 - largo_cifra,
              altura+80, canvas)
        # Automatizacion ######################
        if not pd.isna(Claves):
            nota = Recomendaciones(Claves, consumo, tarifa, Uso)
        # Automatizacion  ######################
        parrafos = []
        if nota == '.':
            parrafos.append(Paragraph('Su consumo es óptimo', Estilos.cuadros_bajo))
        else:
            if len(nota)<250:
                parrafos.append(Paragraph(str(nota), Estilos.cuadros_bajo))
            elif 250<=len(nota)<500:
                parrafos.append(Paragraph(str(nota), Estilos.cuadros_bajo2))
            else:
                parrafos.append(Paragraph(str(nota), Estilos.cuadros_bajo3))

        frame = Frame(120, altura-30, width * 0.7, height * 0.12)
        frame.addFromList(parrafos, canvas)
        ##LogoRayo
        canvas.drawImage(f"Imagenes/Figuras/2_datos_rayo.png", 550, 780 ,
                         width=40, height=40)
        altura = altura - 220
        i = i + 1
        if i == 3 and largo >0 :
            canvas.showPage()
            i = 0
            altura=490
            largo=largo-3
        Medio=False
    canvas.showPage()

def por_A_fugas(Fugas):
    totalf=len(Fugas)
    Atacc=Fugas[Fugas['A'].str.contains('Si')]
    totalA=len(Atacc)
    porA=totalA/totalf
    return porA

def portada_fugas(canvas, width, height,Cfugas,Tarifa,ConsumoT,porF):
    """ Pagina de color azul antes de presentar los resultados."""
    canvas.setFillColorRGB(96 / 255, 192 / 255, 215 / 255)
    canvas.rect(0, 0, width, height, fill=1, stroke=False)
    canvas.drawImage("Imagenes\Spark1_blueBG.png", width - 70, height - 65, width=40, height=40)
    costado(canvas, 'white')
    atacables=porF
    parrafo_frame('<b>PÉRDIDAS DE ENERGÍA</b>', Estilos.titulo_blanco, 50, 500, .8, .1,canvas)
    costo= round(float(Cfugas)*float(Tarifa))
    porcentaje_fugas=float(Cfugas)/float(ConsumoT)
    mensaje = "A continuación te presentamos puntualmente dónde encontramos pérdidas de energía y que acciones"\
                  " tomar para eliminarlas o reducir su consumo. <br/><br/>"\
                 f"Durante nuestras mediciones encontramos que el <b>{round(porcentaje_fugas * 100, 1):,}%</b> de tu consumo total y con un costo de <b>${costo:,}</b>"\
                  " al bimestre, son perdidas por algún tipo de fuga, como: <br/><br/>"\
                "1° Fuga de equipo <br/><br/>2° Fuga de circuito <br/><br/>3° Fuga de Stand-by<br/><br/>"\
                f"Aproximadamente el <b>{round(atacables * 100, 1):,}%</b> de estas pérdidas son atacables y tienen un gran potencial de ahorro."
    parrafo_frame(mensaje, Estilos.negro, 49, 50, .4, .5,canvas)
    mensaje = "Para identificar el nivel de ahorro de las diferentes pérdidas de energía que detectamos, te reforzaremos visualmente con los siguientes iconos:"
    canvas.drawImage(f"Imagenes/Figuras/Fugas_cuadro.png",300, 290,  width=220,height=85, mask='auto')
    parrafo_frame(mensaje, Estilos.negro, 300, 50, .4, .5, canvas)

    canvas.showPage()


def hojas_fugas(canvas, width, height, fugas_, tarifa,voltaje):
    """ Crea la hoja que muestra donde esta la fuga, que aparatos hay y si es atacable o no """
    fugas_['D']=fugas_['D'].str.replace('Fuga', '', regex=True)
    LFugas=fugas_.copy()
    LFugas = LFugas.loc[LFugas['L'].apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna().index]
    LFugas.sort_values(by=['L'], inplace=True, ascending=False)
    LFugas = LFugas.drop_duplicates(subset=['E'], keep='first')
    Lugares=col_one_list = LFugas['E'].tolist()
    #print(Lugares)
    for lista in Lugares:
        fugas= fugas_.loc[fugas_['E']==lista]
        ata= fugas.loc[fugas['A']=='Si']
        noata=fugas.loc[fugas['A']=='No']
        atar=fugas.loc[fugas['A']=='R']
        fugasenhoja(canvas, width, height, ata, lista,0,True,voltaje)
        fugasenhoja(canvas, width, height, noata, lista,1,False,voltaje)
        fugasenhoja(canvas, width, height, atar, lista,2,True,voltaje)

def fugasenhoja(canvas, width, height,atac,lista,idx,Atacable,voltaje):
    Lequipos = []
    if not atac.empty:
        consumoT = round(atac['K'].sum(), 1)
        costoT = round(atac['M'].sum())
        porcientoT = round((atac['L'].sum()) * 100, 1)
        detalles_fugas(canvas, width, height, lista, idx, costoT, consumoT, porcientoT)
        altura = 350
        canvas.line(50, altura + 50, 300, altura + 50)
        ind=1


        np=0
        for index, fugat in atac.iterrows():
            if ind > 4:
                canvas.showPage()
                consumoT = round(atac['K'].sum(), 1)
                costoT = round(atac['M'].sum())
                porcientoT = round((atac['L'].sum()) * 100, 1)
                detalles_fugas(canvas, width, height, lista, idx, costoT, consumoT, porcientoT)
                altura = 350
                canvas.line(50, altura + 50, 300, altura + 50)
                parrafos = []
                notasA = 'Continuación...'
                parrafos.append(Paragraph(notasA, Estilos.azul_2_chico2))
                frame = Frame(45, altura+30, 100, 50)
                frame.addFromList(parrafos, canvas)
                ind = 1
                np=np+1

            Nfuga = fugat[3]
            costo = round(fugat[12])
            consumo = round(fugat[10], 1)
            porciento = round(fugat[11] * 100, 1)
            potencia = fugat[9]
            parrafos = []
            parrafos.append(Paragraph(Nfuga, Estilos.negroB))
            frame = Frame(50, altura, 250, 50)
            frame.addFromList(parrafos, canvas)
            if len(Nfuga)<40:
                parrafo_frame("Potencia", Estilos.base2, 50, altura - 55, .2, .1, canvas)
                parrafo_frame("Consumo", Estilos.base2, 150, altura - 55, .2, .1, canvas)
                parrafo_frame("Costo", Estilos.base2, 250, altura - 55, .2, .1, canvas)
                parrafos.append(Paragraph(str(potencia) + ' W', Estilos.cuadros_bajo2))
                frame = Frame(50, altura - 35, 62, 50)
                frame.addFromList(parrafos, canvas)
                parrafos.append(Paragraph(str(consumo) + ' kWh', Estilos.cuadros_bajo2))
                frame = Frame(150, altura - 35, 70, 50)
                frame.addFromList(parrafos, canvas)
                parrafos.append(Paragraph('$ ' + str(costo), Estilos.cuadros_bajo2))
                frame = Frame(250, altura - 35, 60, 50)
                frame.addFromList(parrafos, canvas)
                canvas.line(50, altura - 20, 300, altura - 20)
            else:
                parrafo_frame("Potencia", Estilos.base2, 50, altura - 70, .2, .1, canvas)
                parrafo_frame("Consumo", Estilos.base2, 150, altura - 70, .2, .1, canvas)
                parrafo_frame("Costo", Estilos.base2, 250, altura - 70, .2, .1, canvas)
                parrafos.append(Paragraph(str(potencia) + ' W', Estilos.cuadros_bajo2))
                frame = Frame(50, altura - 50, 62, 50)
                frame.addFromList(parrafos, canvas)
                parrafos.append(Paragraph(str(consumo) + ' kWh', Estilos.cuadros_bajo2))
                frame = Frame(150, altura - 50, 70, 50)
                frame.addFromList(parrafos, canvas)
                parrafos.append(Paragraph('$ ' + str(costo), Estilos.cuadros_bajo2))
                frame = Frame(250, altura - 50, 60, 50)
                frame.addFromList(parrafos, canvas)
                canvas.line(50, altura - 25, 300, altura - 25)
                altura=altura-5
            ind = ind + 1
            altura = altura - 80
            Lequipos.append(Nfuga)

            if Atacable and ind==5:
                Consejos = armarTextoCTV(consumoT, horasBimestre=100, listDisp=Lequipos, estbVol=True, toleDisp=True,
                                         timerKobo=True, maniobras=None)
                if len(Consejos)<750:
                    parrafos.append(Paragraph(Consejos, Estilos.aparatos3))
                else:
                    parrafos.append(Paragraph(Consejos, Estilos.aparatos2))
                frame = Frame(330, 50, 200, 330, showBoundary=0)
                frame.addFromList(parrafos, canvas)
                Lequipos=[]

            if Atacable and ind<5 and np>=1:
                Consejos = armarTextoCTV(consumoT, horasBimestre=100, listDisp=Lequipos, estbVol=voltaje, toleDisp=True,
                                         timerKobo=True, maniobras=None)
                parrafos.append(Paragraph(Consejos, Estilos.aparatos3))
                frame = Frame(330, 50, 200, 330, showBoundary=0)
                frame.addFromList(parrafos, canvas)
                Lequipos=[]
                np=0


        if not Atacable:
            Consejos='En los equipos de comunicación y seguridad no recomendamos tomar acción o desconectarlos, ' \
                     'debido a que pueden afectar tanto tu comfort como tu seguridad'
            parrafos.append(Paragraph(Consejos, Estilos.aparatos3))
            frame = Frame(330, 50, 200, 330,showBoundary = 0 )
            frame.addFromList(parrafos, canvas)



        canvas.showPage()


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

def cuadro_resumen(canvas, width, height, aparatos,luces,fugas,caritaL):

    azul_1 = [0 / 255, 76 / 255, 101 / 255]
    gris = [65 / 255, 65 / 255, 65 / 255]
    costado(canvas)
    Aparatos=aparatos.copy()
    ##############################################################################################################################################
    Aparatos.loc[29] = [3, '','', 'Pérdidas', '','', '', '', '', '', fugas['K'].sum(), fugas['L'].sum(),fugas['M'].sum(), 'Pérdidas','','','']
    Aparatos.loc[30] = [caritaL, '',' ', 'Luces', '','', '', '', '', '', luces['K'].sum(), luces['L'].sum(),luces['M'].sum(), 'Luces','','','']
    Aparatos = Aparatos.loc[Aparatos['L'].apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna().index]
    Aparatos.sort_values(by=['L'], inplace=True, ascending=False)
    largo_encabezado = pdfmetrics.stringWidth('TABLA RESUMEN DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 'Montserrat-B', 12)
    canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
    texto('TABLA RESUMEN DE CONSUMO Y PÉRDIDAS DE ENERGÍA', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
    texto("CUADRO RESUMEN", 36, azul_1, 'Montserrat-B', 60, height - 170, canvas)
    altura = 550
    parrafo_frame("Equipo", Estilos.negroB, 50, altura + 5, .2, .1, canvas)
    parrafo_frame("Consumo", Estilos.negroB, 300, altura +5, .2, .1, canvas)
    parrafo_frame("Porcentaje", Estilos.negroB, 400, altura+5 , .2, .1, canvas)
    parrafo_frame("Costo", Estilos.negroB, 500, altura +5, .2, .1, canvas)
    max_por_hoja = 20
    canvas.line(50, altura + 60, 550, altura + 60)
    canvas.line(50, altura +90, 550, altura +90)
    cont=0
    for index, fugat in Aparatos.iterrows():
        Nfuga = fugat[3]
        costo = round(fugat[12])
        consumo = round(fugat[10], 1)
        porciento = round(fugat[11] * 100, 1)
        carita = fugat[0]
        canvas.drawImage(f"Imagenes/cara_{carita}.png", 285, altura+30, width=20,
                         height=20,   mask='auto')
        parrafos = []
        i = 0
        largo = (len(fugat))
        i = i + 1
        if len(Nfuga)<30:
            parrafos.append(Paragraph(Nfuga, Estilos.cuadros_bajo2))
            frame = Frame(50, altura, 240, 50)
            frame.addFromList(parrafos, canvas)
        else:
            parrafos.append(Paragraph(Nfuga, Estilos.cuadros_bajo2))
            frame = Frame(50, altura+7, 240, 50)
            frame.addFromList(parrafos, canvas)

        parrafos.append(Paragraph(str(consumo) + ' kWh', Estilos.cuadros_bajo2))
        frame = Frame(320, altura , 80, 50)
        frame.addFromList(parrafos, canvas)
        parrafos.append(Paragraph(str(porciento) + ' %', Estilos.cuadros_bajo2))
        frame = Frame(420, altura , 80, 50)
        frame.addFromList(parrafos, canvas)
        parrafos.append(Paragraph('$ ' + str(costo), Estilos.cuadros_bajo2))
        frame = Frame(500, altura , 80, 50)
        frame.addFromList(parrafos, canvas)
        canvas.line(50, altura+25, 550, altura +25)
        altura = altura -30
        if cont==18:
            canvas.showPage()
            largo_encabezado = pdfmetrics.stringWidth('DESCIFRAMIENTO DE COSNUMO Y PÉRDIDAS DE ENERGÍA', 'Montserrat-B',12)
            canvas.line(60, height - 50, largo_encabezado + 60, height - 50)
            texto('DESCIFRAMIENTO DE PÉRDIDAS DE ENERGÍA', 12, gris, 'Montserrat-B', 60, height - 65, canvas)
            texto("CUADRO RESUMEN", 36, azul_1, 'Montserrat-B', 60, height - 170, canvas)
            altura = 550
            parrafo_frame("Equipo", Estilos.negroB, 50, altura + 5, .2, .1, canvas)
            parrafo_frame("Consumo", Estilos.negroB, 300, altura + 5, .2, .1, canvas)
            parrafo_frame("Porcentaje", Estilos.negroB, 400, altura + 5, .2, .1, canvas)
            parrafo_frame("Costo", Estilos.negroB, 500, altura + 5, .2, .1, canvas)
            altura=550
        cont = cont + 1

    canvas.showPage()


def estrategia_ahorro(canvas, width, height, n, ):
    gris = [65 / 255, 65 / 255, 65 / 255]
    azul_1 = [0 / 255, 76 / 255, 101 / 255]
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
    canvas.drawImage("Imagenes\Figuras\Figuras-19.png", 50,100, width=500, height=500, mask='auto')
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
    mal=True
    if mal:
        yy=-25
        hh=50
        ty=-20
        tt=10
    else:
        yy = 0
        hh = 0
        ty=0
        tt=0
    rayo=1
    for i in range(3):
        im = f"Imagenes/Figuras/cuadro.png"
        w, h = Image.open(im).size
        esc = 2.3
        if i == 0:
            canvas.drawImage(im, cuadros_x, cuadros_y - separado * i+ ty, width=int(w / esc), height=int(h / esc)+hh,
                             mask='auto')
            im = f"Imagenes/Figuras/medidor_{medidor}.png"
            w, h = Image.open(im).size
            esc = 6.3
            canvas.drawImage(im, cuadros_x + 25, cuadros_y - separado * i + 36, width=int(w / esc), height=int(h / esc),
                             mask='auto')
            texto('EL MEDIDOR', 14, azul_1, 'Montserrat-B', cuadros_x + 100, cuadros_y - separado * i + 75+tt, canvas)
            with open(f'Textos/medidor_{medidor}.txt', 'r', encoding='utf-8') as file:
                texto_ = file.read()
            parrafo_en_imagen(texto_, Estilos.gris_medio, cuadros_x + 92, cuadros_y - separado * i + 20+tt, 300, 50,canvas)

        elif i == 1:
            canvas.drawImage(im, cuadros_x, cuadros_y - separado * i+yy, width=int(w / esc), height=int(h / esc),
                             mask='auto')
            im = f"Imagenes/Figuras/candado_{candado}.png"
            w, h = Image.open(im).size
            esc = 7.2
            canvas.drawImage(im, cuadros_x + 30, cuadros_y - separado * i + 28+yy, width=int(w / esc), height=int(h / esc),
                             mask='auto')
            texto('ROBO DE ENERGÍA', 14, azul_1, 'Montserrat-B', cuadros_x + 100, cuadros_y - separado * i + 75+yy, canvas)
            with open(f'Textos/robo_{candado}.txt', 'r', encoding='utf-8') as file:
                texto_ = file.read()
            parrafo_en_imagen(texto_, Estilos.gris_grande, cuadros_x + 92, cuadros_y - separado * i + 20+yy, 300, 50,canvas)

        elif i == 2:
            canvas.drawImage(im, cuadros_x, cuadros_y - separado * i +yy, width=int(w / esc), height=int(h / esc),
                             mask='auto')
            im = f"Imagenes/Figuras/rayo_{rayo}.png"
            w, h = Image.open(im).size
            esc = 5
            canvas.drawImage(im, cuadros_x + 37, cuadros_y - separado * i + 25+yy, width=int(w / esc), height=int(h / esc),
                             mask='auto')
            texto('VOLTAJE', 14, azul_1, 'Montserrat-B', cuadros_x + 100, cuadros_y - separado * i + 75+yy, canvas)
            with open(f'Textos/voltaje_{rayo}.txt', 'r', encoding='utf-8') as file:
                texto_ = file.read()
            parrafo_en_imagen(texto_, Estilos.gris_grande, cuadros_x + 92, cuadros_y - separado * i + 20+yy, 300, 50,canvas)

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
    costado(canvas)
    canvas.showPage()

def contraportada(canvas, width, height):
    """ Contra portada del documento """
    canvas.drawImage('Imagenes\Figuras\Contraportada.png', 0, 0, width = width, height = height)
    canvas.showPage()


def Clasificador(aparatos):
    Aparatos=aparatos.copy()
    Aparatos = Aparatos.loc[Aparatos['L'].apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna().index]
    Aparatos.sort_values(by=['L'], inplace=True, ascending=False)
    Aparatos = Aparatos.loc[Aparatos['M'].apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna().index]
    Aparatos.sort_values(by=['M'], inplace=True, ascending=False)
    carita= definircarita(Aparatos)
    AparatosG = Aparatos.loc[Aparatos['A'] == 3]
    AparatosM = Aparatos.loc[Aparatos['A'] == 2]
    AparatosC = Aparatos.loc[Aparatos['A'] == 1]
    deMaG=['Refrigerador','Congelador','Minibar','Cava','Hielos','Dispensador']
    for i in deMaG:
        AparatosMaG= AparatosM.loc[AparatosM['D'].str.contains(i)]
        AparatosM=AparatosM[~AparatosM['D'].str.contains(i)]
        AparatosG=AparatosG.append(AparatosMaG)

    return AparatosG, AparatosM,AparatosC

def CrearPDF(aparatos, luces, fugas, consumo, costo, Tarifa,Cfugas,Cliente,SolarS,Voltaje):

    if SolarS.empty:
        solar=False
    else:
        solar=True

    consumo_bimestral= float(consumo)
    tarifa=Tarifa
    cliente = Cliente
    cliente_ = cliente.replace(' ', '_')
    filename = f"{cliente_}.pdf"
    canvas = canvas_.Canvas(filename)
    width, height = A4
    ahorro_bimestral=140
    tipo_tarifa='DAC'
    color_voltaje = int(Voltaje)

    fonts()
    portada(canvas, width, height)
    intro(canvas, width, height)
    potencial_ahorro(canvas, width, height,consumo_bimestral, tarifa,costo,ahorro_bimestral, tipo_tarifa)
    if solar:
        Solar(canvas,tarifa,costo,consumo,SolarS)
    porF=por_A_fugas(fugas)
    aparatosG,aparatosM, aparatosC= Clasificador(aparatos)
    aparatos_grandes(canvas, width, height,aparatosG,Tarifa)
    aparatos_bajos(canvas, width, height,aparatosM,aparatosC,Tarifa)
    caritaL = iluminacion(canvas, width, height, luces,Tarifa)
    portada_fugas(canvas, width, height, Cfugas,Tarifa,consumo,porF)
    hojas_fugas(canvas, width, height, fugas, Tarifa,color_voltaje)
    cuadro_resumen(canvas, width, height, aparatos,luces,fugas,caritaL)
    robo='no'
    revisar='no'
    nivel=1

    medidor(canvas, width, height, robo, revisar, nivel, color_voltaje)
    estrategia_ahorro(canvas,width,height,0)
    notas(canvas)
    contraportada(canvas, width, height)

    try:
        canvas.save()
    except Exception as e:
        print("No se guardó el archivo. Revisar que no esté abierto.")
