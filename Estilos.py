from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY
from reportlab.lib import colors

gris = (65 / 255, 65 / 255, 65 / 255)
blanco = (1, 1, 1)
negro = (0, 0, 0)
azul_1 = (0 / 255, 76 / 255, 101 / 255)
azul_2 = (2 / 255, 142 / 255, 200 / 255)

base = ParagraphStyle(name='Findero',
                        fontName='montserrat',
                        fontSize=12,
                        leading=17,
                        textColor=gris
                        )

base2 = ParagraphStyle(name='Findero',
                        fontName='montserrat',
                        fontSize=10,
                        leading=17,
                        textColor=negro
                        )

plot = ParagraphStyle(name='Findero',
                        fontName='montserrat',
                        fontSize=11,
                        leading=15,
                        textColor=gris
                        )

negro = ParagraphStyle(name='Findero',
                        fontName='montserrat',
                        fontSize=12,
                        leading=17,
                        textColor=negro
                        )

chica = ParagraphStyle(name='Chica',
                                  fontName='montserrat',
                                  fontSize=10,
                                  leading=12,
                                  textColor=gris
                                  )

mini = ParagraphStyle(name='Mini',
                                  fontName='montserrat',
                                  fontSize=8,
                                  leading=10,
                                  textColor=gris
                                  )

resumen = ParagraphStyle(name='Resuman',
                                  fontName='montserrat',
                                  fontSize=11,
                                  leading=12,
                                  textColor=gris
                                  )

titulos = ParagraphStyle(name='Titlulos',
                                  fontName='montserrat',
                                  fontSize=36,
                                  leading=40,
                                  textColor=azul_1
                                  )

titulos2 = ParagraphStyle(name='Titlulos',
                                  fontName='Montserrat-B',
                                  fontSize=32,
                                  leading=40,
                                  textColor=azul_1
                                  )
titulos3 = ParagraphStyle(name='Titlulos',
                                  fontName='Montserrat-B',
                                  fontSize=25,
                                  leading=40,
                                  textColor=azul_1
                                  )
titulos4 = ParagraphStyle(name='Titlulos',
                                  fontName='Montserrat-B',
                                  fontSize=25,
                                  leading=30,
                                  textColor=azul_1
                                  )

titulos5 = ParagraphStyle(name='Titlulos',
                                  fontName='Montserrat-B',
                                  fontSize=20,
                                  leading=20,
                                  textColor=azul_1
                                  )

titulos6 = ParagraphStyle(name='Titlulos',
                                  fontName='Montserrat-B',
                                  fontSize=18,
                                  leading=00,
                                  textColor=azul_1
                                  )


centrado = ParagraphStyle(name='Findero',
                                 fontName='montserrat',
                                 alignment=TA_CENTER,
                                 fontSize=12,
                                 leading=17,
                                 textColor=gris
                                 )

centrado_chico = ParagraphStyle(name='Findero',
                                 fontName='montserrat',
                                 alignment=TA_CENTER,
                                 fontSize=11,
                                 leading=12,
                                 textColor=gris
                                 )

cuadros = ParagraphStyle(name='Cuadros',
                                fontName='montserrat',
                                fontSize=9,
                                leading=12,
                                textColor=gris
                                )

cuadros_numero = ParagraphStyle(name='Cuadros',
                                fontName='montserrat',
                                fontSize=17,
                                leading=12,
                                textColor=azul_1
                                )

cuadros_bajo = ParagraphStyle(name='Cuadros',
                                fontName='montserrat',
                                fontSize=14,
                                leading=14,
                                textColor=gris
                                )

cuadros_bajo2 = ParagraphStyle(name='Cuadros',
                                fontName='montserrat',
                                fontSize=12,
                                leading=12,
                                textColor=gris
                                )

cuadros_bajo3 = ParagraphStyle(name='Cuadros',
                                fontName='montserrat',
                                fontSize=9,
                                leading=9,
                                textColor=gris
                                )

cuadros_bajo4 = ParagraphStyle(name='Cuadros',
                                fontName='montserrat',
                                fontSize=6,
                                leading=6,
                                textColor=gris
                                )

negroB = ParagraphStyle(name='Cuadros',
                        fontName='montserrat-B',
                        fontSize=11,
                        leading=17,
                        textColor=(0, 0, 0)
                        )

Lumi = ParagraphStyle(name='Cuadros',
                                fontName='montserrat',
                                fontSize=10,
                                leading=11,
                                textColor=gris
                                )
Lumi2 = ParagraphStyle(name='Cuadros',
                                fontName='montserrat',
                                fontSize=9,
                                leading=11,
                                textColor=gris
                                )

Lumi3 = ParagraphStyle(name='Cuadros',
                                fontName='montserrat',
                                fontSize=8,
                                leading=9,
                                textColor=gris
                                )

Lumi4 = ParagraphStyle(name='Cuadros',
                                fontName='montserrat',
                                fontSize=7,
                                leading=9,
                                textColor=gris
                                )
Lumi5 = ParagraphStyle(name='Cuadros',
                                fontName='montserrat',
                                fontSize=6,
                                leading=8,
                                textColor=gris
                                )



aparatos = ParagraphStyle(name='Aparatos',
                                fontName='montserrat',
                                alignment=TA_JUSTIFY,
                                fontSize=12,
                                leading=15,
                                textColor=gris
                                )

aparatos2 = ParagraphStyle(name='Aparatos',
                                fontName='montserrat',
                                alignment=TA_JUSTIFY,
                                fontSize=10,
                                leading=13,
                                textColor=gris
                                )

aparatos3 = ParagraphStyle(name='Aparatos',
                                fontName='montserrat',
                                alignment=TA_JUSTIFY,
                                fontSize=11,
                                leading=15,
                                textColor=gris
                                )

aparatos4 = ParagraphStyle(name='Aparatos',
                                fontName='montserrat',
                                alignment=TA_JUSTIFY,
                                fontSize=10,
                                leading=12,
                                textColor=gris
                                )

tabla = ParagraphStyle(name='Tabla',
                                  fontName='montserrat',
                                  fontSize=11,
                                  leading=11,
                                  textColor=gris
                                  )

blanco_chico = ParagraphStyle(name='Blanco chico',
                                  fontName='montserrat',
                                  fontSize=10,
                                  leading=11,
                                  textColor=blanco
                                  )

blanco_grande = ParagraphStyle(name='Blanco grande',
                                  fontName='montserrat',
                                  fontSize=23,
                                  leading=11,
                                  textColor=blanco
                                  )

azul_1_chico = ParagraphStyle(name='Azul 1 chico',
                                  fontName='montserrat',
                                  fontSize=7,
                                  leading=8,
                                  textColor=azul_1
                                  )

azul_1_grande = ParagraphStyle(name='Azul 1 grande',
                                  fontName='montserrat',
                                  fontSize=12,
                                  leading=8,
                                  textColor=azul_1
                                  )

azul_1_grande1 = ParagraphStyle(name='Azul 1 grande',
                                  fontName='montserrat',
                                  fontSize=18,
                                  leading=8,
                                  textColor=azul_1
                                  )

azul_1_grande2 = ParagraphStyle(name='Azul 1 grande',
                                  fontName='montserrat',
                                  fontSize=14,
                                  leading=15,
                                  textColor=azul_1
                                  )

azul_2_chico = ParagraphStyle(name='Azul 2 chico',
                                  fontName='montserrat',
                                  fontSize=10,
                                  leading=7,
                                  textColor=azul_2
                                  )
azul_2_chico2 = ParagraphStyle(name='Azul 2 chico',
                                  fontName='montserrat-B',
                                  fontSize=8,
                                  leading=7,
                                  textColor=azul_1
                                  )
azul_2_grande = ParagraphStyle(name='Azul 2 grande',
                                  fontName='montserrat',
                                  fontSize=23,
                                  leading=11,
                                  textColor=azul_2
                                  )

gris_grande = ParagraphStyle(name='Gris grande',
                                  fontName='montserrat',
                                  fontSize=12,
                                  leading=14,
                                  textColor=gris
                                  )

gris_medio = ParagraphStyle(name='Gris grande',
                                  fontName='montserrat',
                                  fontSize=10,
                                  leading=11,
                                  textColor=gris
                                  )

titulo_blanco = ParagraphStyle(name='Titulo blanco',
                                  fontName='montserrat',
                                  fontSize=36,
                                  leading=11,
                                  textColor=blanco
                                  )
