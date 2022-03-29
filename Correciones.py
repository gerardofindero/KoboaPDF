def Lugar(lugar):
    if lugar == 'rec_ppltv_c_i':
        lugar='Recámara Principal'
    if lugar == 'sala_de_tv_pa_c_i':
        lugar='Sala de TV'
    if lugar == 'sala_de_tv':
        lugar = 'Sala de TV'
    if lugar == 'sala_de_tv_pb_c_i':
        lugar='Sala de TV planta baja'
    if lugar == 'rec_ninostv_c_i':
        lugar='Recámara niños'
    if lugar == 'rec_ninastv_c_i':
        lugar='Recámara niña'
    if lugar == 'cocinatv_c_i':
        lugar='Cocina'
    if lugar == 'cuarto_de_serviciotv_c_i':
        lugar='Cuarto de servicio'
    if lugar == 'ba_o':
        lugar = 'Baño'
    if lugar == 'espacio_principal':
        lugar = 'Espacio Principal'
    if lugar == 'sala':
        lugar='Sala'
    if lugar == 'cocina':
        lugar = 'Cocina'
    if lugar == 'ba_o_de_visitas':
        lugar = 'Baño de Visitas'
    if lugar == 'rec_mara_ni_o_s':
        lugar = 'Recámara niños'
    if lugar == 'rec_mara_nino_s':
        lugar = 'Recámara niños'
    if lugar == 'rec_mara_ninas':
        lugar = 'Recámara niños'
    if lugar == 'rec_mara_ni_a_s':
        lugar = 'Recámara niñas'
    if lugar == 'rec_mara_principal':
        lugar = 'Recámara principal'
    if lugar == 'recamara_principal':
        lugar = 'Recámara principal'
    if lugar == 'jard_n':
        lugar='Jardín'
    if lugar == 'bibliotecatv_c_i':
        lugar='Biblioteca'
    if lugar == 'recamara_servicio':
        lugar = 'Cuarto de servicio'
    if lugar == 'salatv_PB':
        lugar = 'Sala de TV planta baja'
    if lugar == 'salatv_PA':
        lugar = 'Sala de TV planta alta'
    if lugar == 'cuarto_servicio':
        lugar = 'Cuarto de servicio'
    if lugar == 'oficina_estudio':
        lugar = 'Oficina'

    lugar.replace('recamara','Recámara')


    return lugar


def LugarS(lugar):

    lugar = lugar.replace('oficina_estudio', 'Oficina')
    lugar = lugar.replace('estudio_oficina  ', 'Estudio')
    lugar = lugar.replace('estudio_oficina', 'Estudio')
    lugar = lugar.replace('salatv', 'Sala de TV')


    return lugar

def FugasCorrec(fugas):
    fugas['Equipo']=fugas['Equipo'].str.replace('tp_link','TP link',regex=True)
    fugas['Equipo']=fugas['Equipo'].str.replace('sky','Sky',regex=True)
    fugas['Equipo']=fugas['Equipo'].str.replace('infinitum','Infinutum',regex=True)
    fugas['Equipo']=fugas['Equipo'].str.replace('motorola','Motorola',regex=True)
    fugas['Equipo']=fugas['Equipo'].str.replace('phillips','Phillips',regex=True)
    fugas['Equipo']=fugas['Equipo'].str.replace('Modem','Módem',regex=True)
    fugas['Equipo']=fugas['Equipo'].str.replace('Telefono','Teléfono',regex=True)

    return fugas

def EquipoCorrec(equipo):
    equipo['Equipo']=equipo['Equipo'].str.replace('samsung','Samsung',regex=True)
    equipo['Equipo']=equipo['Equipo'].str.replace('sub-zero','Sub Zero',regex=True)
    equipo['Equipo']=equipo['Equipo'].str.replace('maytab','Maytab',regex=True)
    equipo['Equipo']=equipo['Equipo'].str.replace('samsung','Samsung',regex=True)
    equipo['Equipo']=equipo['Equipo'].str.replace('sony','Sony',regex=True)
    equipo['Equipo']=equipo['Equipo'].str.replace('philips','Phillips',regex=True)



    return equipo

def Mayuscula(series):
   newSeries = series.str.capitalize()
   return newSeries