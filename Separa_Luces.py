import pandas as pd

######################################################################################################
def UnirLuces(df):
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    #df['A'] = df['A'].str.replace('tira','led')
    df['L']=df['L'].astype(float).round(5)
    ## Juntar luces con mismo PP
    ## Pepes = pd.unique(df['B'])
    zonas =  pd.unique(df['E'])

    for i in zonas:
        dfxpepes=df[df["E"] == i]
        # dfxpepes.sort_values(by=['Z'], inplace=True, ascending=False)
        if len(dfxpepes)>1:
            ## Checar si tienen el mismo porcentaje
            PorC = pd.unique(dfxpepes['L'])




            if len(PorC)==1:
                dfx=dfxpepes.copy()
                ## Juntar focos de tecnologías iguales
                dfx=sumariguales1(dfx,'halogena')
                dfx=sumariguales1(dfx,'incandescente')
                dfx=sumariguales1(dfx,'fluorescente')
                dfx=sumariguales1(dfx,'led')
                dfx=sumariguales1(dfx,'tira')



                ## Asignar los porcentajes por tecnología
                dfx = distporc(dfx)


                ## Separar y asignar los porcentajes por tecnología
                df=separatecno(df,dfxpepes,dfx,'halogena')
                df=separatecno(df,dfxpepes,dfx,'incandescente')
                df=separatecno(df,dfxpepes,dfx,'fluorescente')
                df=separatecno(df,dfxpepes,dfx,'led')


    zonas=pd.unique(df['E'])

    for i in zonas:
        dfxzona=df[df["E"] == i]
        df,dfxzona=sumariguales(dfxzona,df,'halogena')
        df,dfxzona=sumariguales(dfxzona,df,'incandescente')
        df,dfxzona=sumariguales(dfxzona,df,'fluorescente')
        df,dfxzona=sumariguales(dfxzona,df,'led')
        dfxzona=df[df["E"] == i]
        sumazona=dfxzona['L'].sum()
        sumaDzona=dfxzona['M'].sum()

        for j in dfxzona['A'].index:
            df.loc[j,"Y"] =sumaDzona
            df.loc[j,"Z"] =sumazona


    # df['L']=df['L']/100
    return df


def separatecno(df,dfxpepes,dfx,tipo):
    tipoxpepes=dfxpepes[dfxpepes['A'].str.contains(tipo)]
    tipox=dfx[dfx['A'].str.contains(tipo)]


    if len(tipoxpepes)>1:
        separado1=tipox.A.str.split(expand=True)
        numT=separado1[0]
        porcentajeT=float(tipox['L'])

        for k in tipoxpepes.index:
            separado2=tipoxpepes.A.str.split(expand=True)
            numsep=int(separado2.loc[k,0])/int(numT)
            df.loc[k,'L']=numsep*porcentajeT
    else:

        for k in tipox.index:
            df.loc[k,'L']=dfx.loc[k,'L']


    return df


def sumariguales1(dflocal,tipo):

    tipoxzona=dflocal[dflocal['A'].str.contains(tipo)]
    if len(tipoxzona) >1:
        dff=tipoxzona.A.str.split(expand=True)
        dff[0] = dff[0].astype(int)
        sumaFocos=dff[0].sum()
        nuevototal= str(sumaFocos) +' '+  str(tipo)
        # sumaDin=tipoxzona['M'].sum()
        # sumakWh=tipoxzona['K'].sum()
        primero=True
        for j in tipoxzona['A'].index:
            if primero==False:
                dflocal.drop(index=j,inplace=True)
            else:
                dflocal.loc[j,'A']=nuevototal
                # dflocal.loc[j,'K']=sumakWh
                # dflocal.loc[j,'M']=sumaDin
            primero=False
    dflocal.sort_values(by=['M'],inplace=True)
    return dflocal

#### Sumar los focos de la misma tecnología por zona
def sumariguales(dfxzona,df,tipo):

    tipoxzona=dfxzona[dfxzona['A'].str.contains(tipo)]

    if len(tipoxzona) >1:
        dff=tipoxzona.A.str.split(expand=True)
        dff[0] = dff[0].astype(int)
        sumaFocos=dff[0].sum()
        sumaPor=tipoxzona['L'].sum()
        sumakWh=tipoxzona['K'].sum()
        sumaDin=tipoxzona['M'].sum()
        nuevototal= str(sumaFocos) +' '+  str(tipo)
        primero=True
        for j in tipoxzona['A'].index:
            if primero==False:
                df.drop(index=j,inplace=True)
                dfxzona.drop(index=j,inplace=True)
            else:
                df.loc[j,'A']=nuevototal
                df.loc[j,'L']=sumaPor
                df.loc[j,'K']=sumakWh
                df.loc[j,'M']=sumaDin
            primero=False
    return df, dfxzona

### Distribuir los porcentajes
def distporc(dfx):
    NI=0
    NF=0
    NH=0
    NL=0
    Por=0
    for i in dfx.index:
        dff=dfx.loc[i,'A'].split()
        if 'inc' in dff[1]:
            NI=int(dff[0])
        if 'led' in dff[1]:
            NL=int(dff[0])
        if 'hal' in dff[1]:
            NH=int(dff[0])
        if 'fluo' in dff[1]:
            NF=int(dff[0])
        Por=float(dfx.loc[i,'L'])
        kWh=float(dfx.loc[i,'K'])
        Din=float(dfx.loc[i,'M'])
    SumL=0
    if NL>0:
        SumL= SumL+(NL)
    if NH>0:
        SumL= SumL+((NH)*7)
    if NI>0:
        SumL= SumL+((NI)*8)
    if NF>0:
        SumL= SumL+((NF)*4)

    if NL>0:
        L=NL/SumL
        KL=(kWh*L)
        ML=(Din*L)
        L=(L*Por)
    if NH>0:
        H=7*NH/SumL
        KH=(kWh*H)
        MH=(Din*H)
        H=(H*Por)
    if NI>0:
        I=8*NI/SumL
        KI=(kWh*I)
        MI=(Din*I)
        I=(I*Por)
    if NF>0:
        F=4*NF/SumL
        KF=(kWh*F)
        MF=(Din*F)
        F=(F*Por)

    for i in dfx.index:
        dff=dfx.loc[i,'A'].split()
        if 'inc' in dff[1]:
            dfx.loc[i,'L']=I
            dfx.loc[i,'K']=KI
            dfx.loc[i,'M']=MI
        if 'led' in dff[1]:
            dfx.loc[i,'L']=L
            dfx.loc[i,'K']=KL
            dfx.loc[i,'M']=ML
        if 'hal' in dff[1]:
            dfx.loc[i,'L']=H
            dfx.loc[i,'K']=KH
            dfx.loc[i,'M']=MH
        if 'fl' in dff[1]:
            dfx.loc[i,'L']=F
            dfx.loc[i,'K']=KF
            dfx.loc[i,'M']=MF
    return(dfx)

def distporc1(dfx,df):
    if len(dfx) >1:
        NI=0
        NF=0
        NH=0
        NL=0
        Por=0
        for i in dfx.index:
            dff=dfx.loc[i,'A'].split()
            if 'inc' in dff[1]:
                NI=int(dff[0])
            if 'led' in dff[1]:
                NL=int(dff[0])
            if 'hal' in dff[1]:
                NH=int(dff[0])
            if 'fluo' in dff[1]:
                NF=int(dff[0])
            Por=float(dfx.loc[i,'L'])
            kWh=float(dfx.loc[i,'K'])
            Din=float(dfx.loc[i,'M'])
        SumL=0
        if NL>0:
            SumL= SumL+(NL)
        if NH>0:
            SumL= SumL+((NH)*7)
        if NI>0:
            SumL= SumL+((NI)*8)
        if NF>0:
            SumL= SumL+((NF)*4)

        if NL>0:
            L=NL/SumL
            KL=(kWh*L)
            ML=(Din*L)
            L=(L*Por)
        if NH>0:
            H=7*NH/SumL
            KH=(kWh*H)
            MH=(Din*H)
            H=(H*Por)
        if NI>0:
            I=8*NI/SumL
            KI=(kWh*I)
            MI=(Din*I)
            I=(I*Por)
        if NF>0:
            F=4*NF/SumL
            KF=(kWh*F)
            MF=(Din*F)
            F=(F*Por)


        for i in dfx.index:
            dff=dfx.loc[i,'A'].split()
            if 'inc' in dff[1]:
                df.loc[i,'L']=I
                df.loc[i,'K']=KI
                df.loc[i,'M']=MI
            if 'led' in dff[1]:
                df.loc[i,'L']=L
                df.loc[i,'K']=KL
                df.loc[i,'M']=ML
            if 'hal' in dff[1]:
                df.loc[i,'L']=H
                df.loc[i,'K']=KH
                df.loc[i,'M']=MH
            if 'fl' in dff[1]:
                df.loc[i,'L']=F
                df.loc[i,'K']=KF
                df.loc[i,'M']=MF
    return(df)