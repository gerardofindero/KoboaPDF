from SepararFugas import *
from pandas import ExcelWriter
from pathlib         import Path
import pandas as pd
import xlwings
from Tarifa          import leer_tarifa_Dac
from Leer_Lista      import leer_lista
from Leer_Deciframiento import leer_solar
from Carpeta_Clientes import carpeta_clientes

#### Excel
def ExcelDes(Equipos, Luminarias, Fugas,archivo_resultados,Cliente,Solar)    :

    FugasC=Fugas.copy()
    LuminariasC=Luminarias.copy()

    Atacable = Fugas['Atacable'].values
    Fugas.drop(['Atacable'], axis=1, inplace=True)
    Fugas.reset_index(inplace=True, drop=True)
    Tipo = Luminarias['Tipo'].values
    Numero = Luminarias['Numero'].values.astype(int)
    Luminarias.drop(['Numero'], axis=1, inplace=True)
    Luminarias.drop(['Tipo'], axis=1, inplace=True)
    Luminarias.reset_index(inplace=True, drop=True)
    workbook = xlwings.Book(archivo_resultados)
    gris = (200, 200, 200)
    Consumo_bimestral = '=Resumen!A9'
    Tarifa = leer_tarifa_Dac()
###################SOLAR
    if not Solar.empty:
        try:
            workbook.sheets.add('Solar')
        except:
            print('Hoja ya creada')
        print(Solar)
        Sheet1 = workbook.sheets['Solar']
        Sheet1.range('A1').color = gris
        Sheet1.range('A1').value = 'Solar'
        Sheet1.range('A4').color = gris
        Sheet1.range('A4').value = 'No. Modulos'
        Sheet1.range('B4').value = Solar.loc['Modulos','Cantidad']
        Sheet1.range('A5').color = gris
        Sheet1.range('A5').value = 'Potencia'
        Sheet1.range('B5').value = Solar.loc['Modulos','Potencia']
        Sheet1.range('A6').color = gris
        Sheet1.range('A6').value = 'Sombreados'
        Sheet1.range('B6').value = str(Solar.loc['Modulos','Sombreado'])
        Sheet1.range('A7').color = gris
        Sheet1.range('A7').value = 'Inclinacion'
        Sheet1.range('B7').value = str(Solar.loc['Modulos','Inclinacion'])
        Sheet1.range('A8').color = gris
        Sheet1.range('A8').value = 'Orientacion'
        Sheet1.range('B8').value = str(Solar.loc['Modulos','Orientacion'])
        Sheet1.range('A9').color = gris
        Sheet1.range('A9').value = 'Hot Spot'
        Sheet1.range('B9').value = str(Solar.loc['Modulos','Hotspot'])
        Sheet1.range('D4').color = gris
        Sheet1.range('D4').value = 'Arreglo Notas'
        Sheet1.range('E4').value = str(Solar.loc['Modulos','Arreglo'])
        Sheet1.range('D5').color = gris
        Sheet1.range('D5').value = 'Sombreado Notas'
        Sheet1.range('E5').value = str(Solar.loc['Modulos','Sombreado_Notas'])
        Sheet1.range('D6').color = gris
        Sheet1.range('D6').value = 'Interconexion Notas'
        Sheet1.range('E6').value = str(Solar.loc['Modulos','Inter_Notas'])
        Sheet1.range('D7').color = gris
        Sheet1.range('D7').value = 'Hotspot Notas'
        Sheet1.range('E7').value = str(Solar.loc['Modulos','Hotspot_Notas'])
        Sheet1.range("$D$4:$E$9").api.Borders.Weight = 2
        Sheet1.range("$A$4:$B$9").api.Borders.Weight = 2
        Sheet1.range('E1').column_width = 100
        Sheet1.range('A1').column_width = 30
        Sheet1.range('D1').column_width = 30
        Sheet1.range('$E$4:$E$9').api.WrapText = True

    try:
        workbook.sheets.add('Desciframiento')
    except:
        print('Hoja ya creada')

    celdaFinal = len(Equipos) + len(Luminarias) + len(Fugas) + 12
    Sheet1 = workbook.sheets['Desciframiento']
    #Deciframiento = pd.concat([Equipos, Luminarias, Fugas])
    Sheet1.range('A6').value = Equipos
    Sheet1.range(len(Equipos)+9,1).value = Luminarias
    Sheet1.range(len(Equipos)+len(Luminarias)+12,1).value= Fugas

    Sheet1.range('C2').value = Consumo_bimestral
    Sheet1.range('C3').value = '=SUM(K7:K'+str(celdaFinal)+')'
    Sheet1.range('C1').value = 'Consumo'
    Sheet1.range('C1').color = gris
    Sheet1.range('D1').value = 'Costo'
    Sheet1.range('D1').color = gris
    Sheet1.range('D2').value = '=C2*G1'
    Sheet1.range('D3').value = '=(C3*G1)+263.32'
    Sheet1.range('B2').value = 'Bimestral'
    Sheet1.range('B2').color = gris
    Sheet1.range('B3').value = 'Ajustado con costo fijo'
    Sheet1.range('B3').color = gris
    Sheet1.range('G1').value =  Tarifa
    Sheet1.range('F1').value = 'Tarifa'
    Sheet1.range('F1').color = gris
    Sheet1.range('F2').value = 'Medidor'
    Sheet1.range('F2').color = gris
    Sheet1.range('F3').value = 'Voltaje'
    Sheet1.range('F3').color = gris
    Sheet1.range('G2').value = '1'
    Sheet1.range('G3').value = '1'



    Sheet1.range(6, 16).value = 'Descripcion de Señal'
    Sheet1.range(6, 14).value = 'Texto a PDF'
    Sheet1.range(6, 17).value = 'Claves'

    for i in range(len(Equipos)):
        Sheet1.range(7+i, 9).value = '=F'+str(7+i)+'*C$2'
        #Sheet1.range(7+i, 11).value = '=IF(J'+str(7+i)+'="NM",I'+str(7+i)+',(J'+str(7+i)+' / G'+str(7+i)+') * I'+str(7+i)+')'
        Sheet1.range(7 + i, 11).value ='=I'+str(7+i)
        Sheet1.range(7+i, 12).value = '=K'+str(7+i)+' / C$3'
        Sheet1.range(7+i, 13).value = '=K'+str(7+i)+'*G$1'

    Sheet1.range(len(Equipos)+9, 4).value= 'Luminaria'
    Sheet1.range(len(Equipos) + 9, 14).value = 'Texto a PDF'
    Sheet1.range(len(Equipos) + 9, 16).value = 'Descripcion de Señal'
    Sheet1.range(len(Equipos) + 9, 17).value = 'Entrada y Tipo'

    #=K38*1000/(G38*60)
    for i in range(len(Luminarias)):
        inicioL=len(Equipos)+10
        Sheet1.range(inicioL+i,  9).value = '=F'+str(i+inicioL)+'*C$2'
        Sheet1.range(inicioL+i, 11).value = '=I'+str(i+inicioL)
        Sheet1.range(inicioL+i, 12).value = '=K'+str(i+inicioL)+' / C$3'
        Sheet1.range(inicioL+i, 13).value = '=K'+str(i+inicioL)+'*G$1'
        Sheet1.range(inicioL+i,  8).value = '=K'+str(i+inicioL)+'*1000/(G'+str(i+inicioL) +'*60)'

    Sheet1.range(len(Equipos) + len(Luminarias)+12, 4).value = 'Perdidas'
    Sheet1.range(len(Equipos) + len(Luminarias) + 12, 16).value = 'Descripcion'
    Fugas=Fugas.sort_values(by=['Ubicacion'])
    for i in range(len(Fugas)):
        inicioF=len(Equipos)+len(Luminarias)+13
        #Sheet1.range(inicioL+i, 8).value = '=E'+str(inicioL+i)+'*C$2'
        Sheet1.range(inicioF+i, 11).value = '=J'+str(inicioF+i)+'*24*60/1000'
        Sheet1.range(inicioF+i, 12).value = '=K'+str(inicioF+i)+' / C$3'
        Sheet1.range(inicioF+i, 13).value = '=K'+str(inicioF+i)+'*G$1'



############## Rellena con Atacables y tipo de luminaria ##############3
    i = 0
    inicioL = len(Equipos) + 10
    Sheet1.range(inicioL - 1, 1).value = 'Numero y Tipo'
    Tipo= ' '+Tipo
    Tipo= Numero.astype(str) + Tipo

    for tipo in Tipo:
        Sheet1.range(inicioL + i, 1).value = tipo
        i = i + 1

    i=0
    inicioL = len(Equipos) + len(Luminarias) + 13
    Sheet1.range(inicioL -1, 1).value = 'Atacable'
    for atac in Atacable:
        Sheet1.range(inicioL + i, 1).value = atac
        i=i+1


####### Color y Bordes ##################
    CelF="$A$6:$Q$"+str(celdaFinal)
    for i in range(17):
        Sheet1.range(6,i+1).color = gris
        Sheet1.range(len(Equipos) + 9, 1+i).color = gris
        Sheet1.range(len(Equipos) + len(Luminarias) + 12, 1+i).color = gris

    Sheet1.range(CelF).api.Borders.Weight = 2
    Sheet1.range("$B$1:$D$3").api.Borders.Weight = 2
    Sheet1.range("$F$1:$G$3").api.Borders.Weight = 2
    Sheet1.range(CelF).columns.autofit()
    Sheet1['1:1'].api.ColumnWidth = 10
    Sheet1.range('N1').column_width = 100
    Sheet1.range('O1').column_width = 100
    Sheet1.range('P1').column_width = 100
    Sheet1.range('D1').column_width = 30
    Sheet1.range('E1').column_width = 20

    Sheet1.range('N11').api.WrapText = True



###################### Parte de matchear códigos PP y QQ ###############################
    infoL= leer_lista(Cliente)
    infoL['B']=infoL['B'].str.upper()
    cony=0
    infoL['J'].fillna('X')
    #Equipos = Equipos[~Equipos['Codigo'].str.contains('QQ', regex=False, na=False)]
    lista_encontrado=[]
    PorcentajesTotales=''
    for i in Equipos['Codigo']:
        try:
            separado=i.split(',')
        except:
            separado ='1'
        PorcentajesTotales=''
        PotenciasTotales=0
        if len(separado)>1:
            for jj in separado:
                jj = jj.replace(' ','')
                jj = jj.upper()
                identificadosPP= infoL[infoL['B'].str.contains(jj)].index
                if not 'QQ' in identificadosPP:
                    if not identificadosPP.empty:
                        PorcentajesTotales =  'Lista!D'+str(identificadosPP[0]+2)+'+'+PorcentajesTotales
                        if PotenciasTotales > infoL.loc[identificadosPP[0], 'F']:
                            PotenciasTotales =  PotenciasTotales
                        else:
                            PotenciasTotales =  infoL.loc[identificadosPP[0], 'F']
                        #Sheet1.range(7 + cony, 6).value =   str(PorcentajesTotales)
                        Sheet1.range(7 + cony, 8).value =   '=Lista!K'+str(identificadosPP[0]+2)
                        Sheet1.range(2, identificadosPP[0]+2).color = (10, 255, 10)
                        lista_encontrado.append(identificadosPP[0])
                        PrcTo='='+ PorcentajesTotales+'0'
                        PrcTo =PrcTo.replace('+0','')
                        Sheet1.range(7 + cony, 6).value  = PrcTo
                        Sheet1.range(7 + cony, 7).value  = str(PotenciasTotales)
        else:
            i = i.upper()
            identificados= infoL[infoL['B'].str.contains(i)].index
            if not 'QQ' in identificados:
                if not identificados.empty:
                    Sheet1.range(7 + cony, 6).value =   '=Lista!D'+str(identificados[0]+2)
                    Sheet1.range(7 + cony, 8).value =   '=Lista!K'+str(identificados[0]+2)
                    Sheet1.range(7 + cony, 7).value =   infoL.loc[identificados[0], 'F']
                    Sheet1.range(7 + cony, 14).value =  infoL.loc[identificados[0], 'H']
                    Sheet1.range(7 + cony, 16).value =  infoL.loc[identificados[0], 'H']
                    lista_encontrado.append(identificados[0])


        cony=cony+1


    cony = 0
    inicioL = len(Equipos) + 10
    for i in Luminarias['Codigo']:
        i=str(i)
        i=i.upper()
        separados= i.split(',')
        if len(separados)==1:
            identificados= infoL[infoL['B'].str.contains(i)].index

            if not identificados.empty:
                PorcentajesTotales =   '=Lista!D'+str(identificados[0]+2)
                Sheet1.range(inicioL + cony, 6).value = PorcentajesTotales
                Sheet1.range(inicioL + cony, 7).value = infoL.loc[identificados[0], 'F']
                Sheet1.range(inicioL + cony, 16).value = infoL.loc[identificados[0], 'H']
                lista_encontrado.append(identificados[0])
        else:
            PorcentajesTotales=''
            PotenciasTotales=''
            NotasTotales=''
            HorasT=0
            cont=0
            for k in separados:
                k=k.replace(' ','')
                identificados= infoL[infoL['B'].str.contains(k)].index
                if not identificados.empty:
                    PorcentajesTotales =  PorcentajesTotales + 'Lista!D'+ str(identificados[0]+2)+'+'
                    PotenciasTotales =  PotenciasTotales + str(infoL.loc[identificados[0], 'F'])+','
                    NotasTotales =  str(NotasTotales)+ str(infoL.loc[identificados[0], 'H'])
                    HorasT= str(HorasT)+str(infoL.loc[identificados[0], 'J'])
                    cont=cont+1
                    lista_encontrado.append(identificados[0])

            Sheet1.range(inicioL + cony, 6).value  ='='+ PorcentajesTotales+'0'
            Sheet1.range(inicioL + cony, 7).value  = PotenciasTotales[:-1]
            Sheet1.range(inicioL + cony, 16).value = NotasTotales
            #Sheet1.range(inicioL + cony, 8).value = str(round(HorasT/cont,1))

        cony = cony + 1


    cony = 0
    inicioF = len(Equipos) + len(Luminarias) + 13
    FugasC['Codigo'].fillna('FFX',inplace=True)
    #Fugas['Watts Circuito']=np.where(Fugas['Codigo']!= 'FFX', infoL.loc[identificados[0], 'D'], '')
    for i in FugasC['Codigo']:
        i = i.upper()
        identificados= infoL[infoL['B'].str.contains(i)].index
        if not identificados.empty:
            lista_encontrado.append(identificados[0])
            if 'QQ'in i or 'FFX' in i or i=='FF':
                Sheet1.range(inicioF + cony, 9).value = 'X'
            else:
                Sheet1.range(inicioF + cony, 6).value = infoL.loc[identificados[0], 'D']
                Sheet1.range(inicioF + cony, 9).value = '=Lista!G'+str(identificados[0]+2)

        cony=cony+1

    workbook.save()
    #workbook.close()
    #print(lista_encontrado)
    try:
        workbook.sheets.add('Lista')
    except:
        print('Hoja ya creada')

    Sheet1 = workbook.sheets['Lista']

    for i in lista_encontrado:
        Sheet1.range(i+2,2).color = (50, 255, 50)

    PEPES = infoL[infoL['B'].str.contains('FF|PP')]

    porcentaje=(1-(len(lista_encontrado)/ len(PEPES)))*100
    print(porcentaje)
    workbook.save()

    return Equipos, Luminarias, Fugas




##################################################################################################################
# FUNCION QUE CREA PESTANA DE EXCEL 'DESCIFRAMIENTO'

def Archivo(Cliente,Luz,Clust,Coci,Esp,Lava,Refri,Bomba,PCs,Comu,Cal,Segu,Aire,Tluz,Solar):

    Luminaria=Luz.copy()
    Luminarias = pd.DataFrame(
        columns=['Codigo','Ubicacion', 'Equipo', 'Lugar', '% Equipo', 'Potencia', 'Horas de la semana', 'kWh', 'Potencia Kobo',
                 'kWh Ajustado','% Ajustado','$ Bimestre', 'Texto','Notas',' ', 'Claves'])
    Equipos = pd.DataFrame(
        columns=['Codigo','Ubicacion', 'Equipo', 'Lugar', '% Equipo', 'Potencia', 'Horas de la semana', 'kWh', 'Potencia Kobo',
                 'kWh Ajustado','% Ajustado','$ Bimestre', 'Texto','Notas',' ', 'Claves'])
    Fugas = pd.DataFrame(
        columns=['Atacable','Codigo','Ubicacion', 'Equipo', 'Lugar', '% Equipo', 'Potencia', 'Horas de la semana', 'Watts Circuito', 'Potencia Kobo',
                 'kWh Ajustado','% Ajustado','$ Bimestre', 'Texto','Notas',' ', 'Claves'])

    Dic=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q']

    print(f"Comenzó el reporte de {Cliente}")

    archivo_resultados = carpeta_clientes(Cliente)

    Exx = pd.read_excel(archivo_resultados,sheet_name='Resumen')
    Exx.columns=Dic

    Exx.drop(Exx.index[:12],inplace=True)
    donde=Exx.loc[Exx['A'] == 'Periodo:']
    Exx = Exx.drop(Exx[Exx['C'] == 'Total'].index)

    if not Refri.empty:

        print("Refri")
        Equipo,Fuga = separar_fugasR(Refri)
        Equipos = Equipos.append(Equipo,sort=False)[Equipos.columns.tolist()]
        Fugas   = Fugas.append(Fuga,sort=False)[Fugas.columns.tolist()]

    if not Clust.empty:
        print("Cluster")
        Equipo, Fuga = separar_fugasTV(Clust)
        Equipos = Equipos.append(Equipo, sort=False)[Equipos.columns.tolist()]
        Fugas = Fugas.append(Fuga, sort=False)[Fugas.columns.tolist()]

    if not Lava.empty:
        print("Lava")
        Equipo,Fuga = separar_fugas(Lava)
        Equipos = Equipos.append(Equipo,sort=False)[Equipos.columns.tolist()]
        Fugas   = Fugas.append(Fuga,sort=False)[Fugas.columns.tolist()]

    if not Coci.empty:
        print("Cocina")
        Equipo,Fuga = separar_fugasC(Coci)
        Equipos = Equipos.append(Equipo,sort=False)[Equipos.columns.tolist()]
        Fugas   = Fugas.append(Fuga,sort=False)[Fugas.columns.tolist()]


    if not PCs.empty:
        print("Computo")
        Equipo, Fuga = separar_fugas(PCs)
        Equipos = Equipos.append(Equipo, sort=False)[Equipos.columns.tolist()]
        Fugas = Fugas.append(Fuga, sort=False)[Fugas.columns.tolist()]

    if not Comu.empty:
        print("Comunicaciones")
        Equipo, Fuga = separar_fugas(Comu)
        Equipos = Equipos.append(Equipo, sort=False)[Equipos.columns.tolist()]
        Fugas = Fugas.append(Fuga, sort=False)[Fugas.columns.tolist()]

    if not Cal.empty:
        print("Calefaccion")
        Equipo, Fuga = separar_fugasCal(Cal)
        Equipos = Equipos.append(Equipo, sort=False)[Equipos.columns.tolist()]
        Fugas = Fugas.append(Fuga, sort=False)[Fugas.columns.tolist()]

    if not Bomba.empty:
        print("Bomba")
        Equipo, Fuga = separar_fugasBB(Bomba)
        Equipos = Equipos.append(Equipo, sort=False)[Equipos.columns.tolist()]
        Fugas = Fugas.append(Fuga, sort=False)[Fugas.columns.tolist()]

    if not Segu.empty:
        print("Seguridad")
        Equipo, Fuga = separar_fugas(Segu)
        Equipos = Equipos.append(Equipo, sort=False)[Equipos.columns.tolist()]
        Fugas = Fugas.append(Fuga, sort=False)[Fugas.columns.tolist()]

    if not Aire.empty:
        print("Aires Acondicionados")
        Equipo, Fuga = separar_fugasA(Aire)
        Equipos = Equipos.append(Equipo, sort=False)[Equipos.columns.tolist()]
        Fugas = Fugas.append(Fuga, sort=False)[Fugas.columns.tolist()]

    if not Esp.empty:
        print("Especial")
        Equipo,Fuga = separar_fugasE(Esp)
        Equipos = Equipos.append(Equipo,sort=False)[Equipos.columns.tolist()]
        Fugas   = Fugas.append(Fuga,sort=False)[Fugas.columns.tolist()]

    #regusDF= Fugas.loc[Fugas['Equipo'].str.contains('Regulador')]
    #print(regusDF)

    Luminaria.fillna(' ', inplace=True)
    Ldicc=['mr16','mr11','espiral','bombilla','vela','globo','cacahuate','flama','par']
    Luminaria.loc[Luminaria['TipoyTam'].str.contains('tubo'), 'Tipytam'] = 'tubos'
    Luminaria.loc[Luminaria['TipoyTam'].isin(Ldicc), 'Tipytam'] = 'focos'
    Luminaria['Tipytam'].fillna('focos', inplace=True)
    Luminarias['Numero'] = Luminaria['Numero']
    Luminarias['Codigo'] = Luminaria['CodigoN']
    Luminarias['Equipo'] = 'Luces '+ Luminaria['Lugar']
    Luminarias['Lugar']=Luminaria['Lugar'] +' '+ Luminaria['LugarEs']
    Luminarias['Ubicacion'] = 'C'+ Luminaria['Circuito'].apply(str)+' '+Luminaria['Tablero'].apply(str)
    Luminarias['Potencia Kobo'] = Luminaria['Consumo']
    #Luminarias['Potencia Kobo'] = 'X'

    Luminarias['Texto']=Luminaria['Adicional']
    Luminarias['Notas'] = Luminaria['Notas']
    Luminarias['Tipo'] = Luminaria['Tecnologia']

    Tdos=pd.DataFrame()
    eq=Equipos[['Ubicacion','Equipo','Lugar','Texto']]
    Tdos= Tdos.append(eq)
    eq = Luminarias[['Ubicacion', 'Equipo', 'Lugar', 'Texto']]
    Tdos = Tdos.append(eq)
    eq = Fugas[['Ubicacion', 'Equipo', 'Lugar', 'Texto']]
    Tdos = Tdos.append(eq)
    Tdos =Tdos[['Ubicacion', 'Equipo', 'Lugar', 'Texto']]
    Tdos.columns=['Ubicacion', 'Equipo', 'Lugar', 'Notas']

    Nombre = 'Notas_' + Cliente + '.xlsx'
    writer2 = ExcelWriter(Path.home() / 'Desktop' / Nombre, engine='xlsxwriter')
    Tdos.to_excel(writer2, index=True,startrow=2)
    writer2.save()


    Luminaria['LugarEs'].fillna('_',inplace=True)
    #Luminarias['Texto']=Tluz #+' '+ Luminaria['TipoyTam']+'  '+ Luminaria['Entrada']
    Luminarias['Texto']=Luminaria['Datos']
    Luminaria['Datos']=Luminaria['Datos'].replace(',X','')
    Luminaria['Datos']=Luminaria['Datos'].str.replace('////,','')
    Luminarias['Claves'] = Luminaria['Datos']
    Luminarias=Luminarias.reset_index(drop=True)

    Equipos.reset_index(inplace=True, drop=True)
    Fugas.reset_index(inplace=True, drop=True)
    Luminarias.reset_index(inplace=True, drop=True)
    Equipos.drop(Equipos[Equipos.Codigo == 'X'].index, inplace=True)
    Equipos.reset_index(inplace=True, drop=True)

    Luminarias.sort_values(by='Lugar', ascending=True, inplace=True)
    Fugas.sort_values(by='Atacable', ascending=True, inplace=True)
    Fugas.sort_values(by='Lugar', ascending=True,inplace=True)


    Equipos.replace(0.01,'NM',inplace=True)
    Fugas.replace(0.00001,'NM',inplace=True)
    Equipos.replace(0.00001,'NM',inplace=True)
    Luminarias.replace(0.00001,'NM',inplace=True)
    Equipos['Codigo']=Equipos['Codigo'].str.upper()
    Fugas['Codigo']=Fugas['Codigo'].str.upper()
    Luminarias['Codigo']=Luminarias['Codigo'].str.upper()
    #Equipos = Equipos[~Equipos['Codigo'].str.contains('FF', regex=False, na=False)]

    j=0
    for i in Fugas.index:
        j = j + 1
        num = 'FG' + str(j)
        Fugas.loc[i, 'Claves'] = num




    ExcelDes(Equipos, Luminarias, Fugas, archivo_resultados, Cliente,Solar)


