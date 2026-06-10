import base64
import io
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import Objeto
from Objeto import *
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

#Librerias de objeto
TamañoEsperado = 1024;
Matriz = Objeto.ClassCreacionMatrices()
Curva = Objeto.AjusteDeCurvas()
Stats = Objeto.Estadistica()

#Fuente Graficas
fuente = 'sans-serif'

#Estilo Graficas
label_style = {
    'width': '80%',
    'backgroundColor':'transparent',
    'border': '3px solid #b5b5b5',
    'borderRadius': '10px',
    'margin': '0 auto 40px auto',
    'display': 'inline-block',
    'fontWeight': 'bold',
    'backgroundImage': 'linear-gradient(135deg, #777 0%, #ccc 25%, #fff 50%, #ccc 75%, #555 100%)',
    'backgroundClip': 'text',
    'WebkitBackgroundClip': 'text',
    'color': 'transparent',
    'WebkitTextFillColor': 'transparent'
}

div_style = {
    'display': 'flex',
    'justifyContent': 'center',
    'gap': '2%',
    'paddingTop': '10px',
    'paddingBottom': '10px',
    'margin': '0 auto 40px auto',
    'width': '90%',
}

#Creacion de la App
app = Dash(__name__)
appEstacion = Dash(__name__)

#Graficas 1. [1 - 2 - 3]
#Temperaturas interiores
IndiceInsideTemp = 1;     IndiceInsideTempMax = 2;  IndiceInsideTempMin = 3;
IndiceInsideHum = 4;      IndiceInsideHumMax = 5;   IndiceInsideHumMin = 6;

#Graficas 1. [4 - 5]
#Dew-Wet-Heat-Heat-Max interiores
IndiceInsideDew = 7;      IndiceInsideWet = 8;      IndiceInsideHeat = 9;     IndiceInsideHeatMax = 10;


#Graficas 2. [1 - 2 - 3]
#Temperaturas exteriores
IndiceExteriorTemp = 15;     IndiceExteriorTempMax = 16;  IndiceExteriorTempMin = 17;
IndiceExteriorHum = 18;      IndiceExteriorHumMax = 19;   IndiceExteriorHumMin = 20;

#Graficas 2. [4 - 5 - 6]
#Dew-Wet-Heat-Heat-Max exteriores
IndiceExteriorDew = 21;      IndiceExteriorDewMax = 22;      IndiceExteriorDewMin = 23;
IndiceExteriorWet = 24;      IndiceExteriorWetMax = 25;      IndiceExteriorWetMin = 26;

#Graficas 3. [1 - 2]
#Presiones
IndiceBar = 11;     IndiceBarMax = 12;  IndiceBarMin = 13;  Pabs = 14;

#Graficas 4. [1 - 2]
#Dew-Wet-Heat-Heat-Max exteriores
AvgWindSpeed = 27;      PrevalentDir = 28;      AverageDir = 29;
WindRun = 30;           HighWindSpeed = 31;     HighWindDir = 32;

#Lectura del archivo, salto de filas, le decimos que no posee header
df = pd.read_csv('ObjetoEjemploMatrizPuntos04.csv', skiprows=5, encoding='utf-8-sig', header=None, dtype=str)

#Datos del header
DatosHeader = [x.item() if hasattr(x, 'item') else x for x in df.iloc[0].tolist()]

#Separar las fechas en una lista
Fechas = [str(x).split(" ",1)[0] for x in df.iloc[:, 0].tolist()[1:]]
Mes = [str(x).split("/",1)[0] for x in Fechas]
Dia = [str(x).split("/",2)[1] for x in Fechas]

#Vectores Posicionadores Mes
PosicionesInicio = [];                  PosicionesFinal = [];
#Vectores Posicionadores Auxiliares
PosicionesAuxiliaresDiasInicio = [];    PosicionesAuxiliaresDiasFinal = [];
PosicionesAuxiliaresDiasContador = [];  PosicionesContador = [];
#Vectores Posicionadores Dias
PosicionesDiasInicio = [];              PosicionesDiasFinal = [];
#IndiceInicial
IndiceMes = Mes[0];         IndiceDia = Dia[0];
#Vectores para Label
Dias = [];
LabelMeses = [];            LabelDias = []
LabelOpcionesNumeros = [];  LabelOpcionesMeses = [];
#Rango
i = 0;  j = 0;  k = 0;  Ante = len(Mes)
#Inicializacion Vectores
Dias.append(Dia[0]);    LabelMeses.append(Mes[0]);  LabelOpcionesMeses.append(Mes[0])
PosicionesInicio.append(i);
PosicionesAuxiliaresDiasInicio.append(i);    PosicionesAuxiliaresDiasContador.append(k);
k = k + 1;

#Inicio del ciclo
while(i < Ante):
    #Es este mes diferente?
    if(Mes[i] != IndiceMes):
        #Intercepta un nuevo indice str
        IndiceMes = Mes[i]
        IndiceDia = Dia[i]
        j = 0;  k = 0;
        #Añadimos las listas
        PosicionesDiasInicio.append(PosicionesAuxiliaresDiasInicio)
        PosicionesDiasFinal.append(PosicionesAuxiliaresDiasFinal)
        PosicionesContador.append(PosicionesAuxiliaresDiasContador)
        for m in range(len(PosicionesAuxiliaresDiasInicio)):
            LabelDias.append(Dia[PosicionesAuxiliaresDiasInicio[m]])
        #Volvemos a crear los vectores
        PosicionesAuxiliaresDiasInicio = [];
        PosicionesAuxiliaresDiasFinal = [];
        PosicionesAuxiliaresDiasContador = [];
        #Añade la posicion de este nuevo elemento
        PosicionesInicio.append(i)
        PosicionesAuxiliaresDiasInicio.append(i)
        PosicionesAuxiliaresDiasContador.append(k)
        i = i + 1; k = k + 1;
    #Si es el mismo mes
    if(Mes[i] == IndiceMes):
        #Si es un dia diferente
        if(Dia[i] != IndiceDia):
            PosicionesAuxiliaresDiasInicio.append(i)
            PosicionesAuxiliaresDiasContador.append(k)
            k = k + 1;
            if(i != (len(Mes) - 1)):
                IndiceDia = Dia[i+1]
        #Si es el mismo dia
        if(Dia[i] == IndiceDia):
            #Esta el array antes de su ultimo elemento?
            if(i == (len(Mes) - 1)):
                #Ultima posicion del dia
                PosicionesAuxiliaresDiasFinal.append(i)
            #Ha cambiado el dia?
            elif(Dia[i+1] != IndiceDia):
                LabelMeses.append(Mes[i+1])
                LabelOpcionesNumeros.append(j)
                j = j + 1
                #Ultima posicion del dia
                PosicionesAuxiliaresDiasFinal.append(i)
        #Esta el array antes de su ultimo elemento?
        if(i == (len(Mes) - 1)):
            PosicionesFinal.append(i)
        #Si detecta un cambio en el siquiente indice toma la posicion final de este
        elif(Mes[i+1] != IndiceMes):
            LabelOpcionesMeses.append(Mes[i+1])
            PosicionesFinal.append(i)
        i = i + 1;
PosicionesDiasInicio.append(PosicionesAuxiliaresDiasInicio);    PosicionesDiasFinal.append(PosicionesAuxiliaresDiasFinal)
PosicionesContador.append(PosicionesAuxiliaresDiasContador);    LabelOpcionesNumeros.append(j)
for m in range(len(PosicionesAuxiliaresDiasInicio)):
    LabelDias.append(Dia[PosicionesAuxiliaresDiasInicio[m]])

#Dia = [float(i) for i in Dia]
#Mes = [float(i) for i in Mes]

#Valor de mes a fecha
def ValueToMonth(Vector):
    i = 0;
    while(i < len(Vector)):
        if Vector[i] == '1':
            Vector[i] = "Enero"
            i = i + 1;
        elif Vector[i] == '2':
            Vector[i] = "Febrero"
            i = i + 1;
        elif Vector[i] == '3':
            Vector[i]= "Marzo"
            i = i + 1;
        elif Vector[i] == '4':
            Vector[i]= "Abril"
            i = i + 1;
        elif Vector[i] == '5':
            Vector[i]= "Mayo"
            i = i + 1;
        elif Vector[i] == '6':
            Vector[i]= "Junio"
            i = i + 1;
        elif Vector[i] == '7':
            Vector[i]= "Julio"
            i = i + 1;
        elif Vector[i] == '8':
            Vector[i]= "Agosto"
            i = i + 1;
        elif Vector[i] == '9':
            Vector[i]= "Septiembre"
            i = i + 1;
        elif Vector[i] == '10':
            Vector[i]= "Octubre"
            i = i + 1;
        elif Vector[i] == '11':
            Vector[i]= "Noviembre"
            i = i + 1;
        elif Vector[i] == '12':
            Vector[i]= "Diciembre"
            i = i + 1;
#Alinear cantidad de datos con direccion del viento
def DireccionesGrados(Vector, Datos):
    vector1 = [0] * 16; vector2 = [0] * 16; vector3 = [0] * 16; vector4 = [0] * 16;
    vector5 = [0] * 16; vector6 = [0] * 16; vector7 = [0] * 16; vector8 = 0;
    Rango = len(Vector);
    for i in range(Rango):
        if(Vector[i] == 'E'):
            #Vector[i] = '270';
            j = 0;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == 'ENE'):
            #Vector[i] = '292.5';
            j = 1;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == 'NE'):
            #Vector[i] = '315';
            j = 2;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == 'NNE'):
            #Vector[i] = '337.5';
            j = 3;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == 'N'):
            #Vector[i] = '0';
            j = 4;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == 'NNW'):
            #Vector[i] = '22.5';
            j = 5;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == 'NW'):
            #Vector[i] = '45';
            j = 6;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == 'WNW'):
            #Vector[i] = '67.5';
            j = 7;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == 'W'):
            #Vector[i] = '90';
            j = 8;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == 'WSW'):
            #Vector[i] = '112.5';
            j = 9;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == 'SW'):
            #Vector[i] = '135';
            j = 10;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == 'SSW'):
            #Vector[i] = '157.5';
            j = 11;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == 'S'):
            #Vector[i] = '180';
            j = 12;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == 'SSE'):
            #Vector[i] = '202.5';
            j = 13;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == 'SE'):
            #Vector[i] = '225';
            j = 14;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == 'ESE'):
            #Vector[i] = '247.5';
            j = 15;
            if(Datos[i] >= 0.0 and Datos[i] <= 3.0):
                vector1[j] = vector1[j] + 1
            elif(Datos[i] > 3.0 and Datos[i] <= 6.0):
                vector2[j] = vector2[j] + 1;
            elif(Datos[i] > 6.0 and Datos[i] <= 10.0):
                vector3[j] = vector3[j] + 1;
            elif(Datos[i] > 10.0 and Datos[i] <= 13.0):
                vector4[j] = vector4[j] + 1;
            elif(Datos[i] > 13.0 and Datos[i] <= 16.0):
                vector5[j] = vector5[j] + 1;
            elif(Datos[i] > 16.0 and Datos[i] <= 32.0):
                vector6[j] = vector6[j] + 1;
            elif(Datos[i] > 32.0):
                vector7[j] = vector7[j] + 1;
        elif(Vector[i] == '--'):
            #Vector[i] = '281.25';
            vector8 = vector8 + 1;
    return vector1,vector2,vector3,vector4,vector5,vector6,vector7,vector8
#Calcular bins de histograma
def RegladeSturges(n):
    k = 1 + math.log2(n)
    kr = round(k);
    if kr % 2 != 0:
        return kr;
    OptMin = kr - 1;    OptMax = kr + 1;
    if abs(kr - OptMin) < abs(kr - OptMax):
        return OptMin;
    else:
        return OptMax;

ValueToMonth(LabelMeses);   ValueToMonth(LabelOpcionesMeses);
LabelOpciones = [];
for k in range(len(LabelDias)):
    LabelOpciones.append(LabelDias[k]+"/"+LabelMeses[k])

#Separar las horas en una lista
#Horas = [str(x).split(" ", 1)[1] for x in df.iloc[:, 0].tolist()[1:]]

appEstacion.layout = html.Div(
    id='interfaz-grafica',
    style={
        'backgroundImage': 'url("/assets/fondo_sol.jpg")',  #Imagen De Fondo
        #'backgroundImage': 'url("/assets/mifondo.jpg")',
        'backgroundAttachment': 'fixed',                    #Fijar Imagen 
        'backgroundSize': 'cover',                          #Toma toda la pantalla
        'backgroundPosition': 'center',                     #Centrar Imagen
        'backgroundRepeat': 'no-repeat',                    #No repetir imagen aunque el tamaño de los elementos supere la pantalla
        'height': '3000px',                                 #Altura de la imagen que queremos mostrar
    },
    children=[
        html.Div(
            id='header-estacion',
            style={ 'paddingTop': '30px','paddingBottom': '10px'},  #Espaciado arriba y abajo de la imagen traslucida
            children=[
                html.H1(
                    id='header-estacion-texto',
                    style={
                        'color': 'white',                                       #Color del texto
                        'textAlign': 'center',                                  #Alineacion del texto
                        'fontSize': '24px',                                     #Tamaño de la fuente
                        'backgroundImage': 'url("/assets/el_fondo.jpg")',       #Imagen de la carpeta assets/el_fondo.jpg
                        'borderRadius': '25px',                                 #Bordes Curvos
                        'padding': '15px 30px',                                 #Espaciado
                        'width': 'fit-content',                                 #Borde automatico
                        'margin': '0 auto 30px auto',                           #Margen del texto
                    },
                    children=[
                        "Graficos estacion metereologica 7GT-EEP",              #Texto
                    ]
                )
            ]
        ),
        html.Div(
            id='interfaz-traslucida',
            style={
                'width': '80%',                                     #Que tanto ocupa de la pantalla
                'borderRadius': '15px',                             #Bordes Curvos
                'paddingTop': '20px',                               #Espaciado Superior
                'paddingBottom': '20',                              #Espaciado Inferior
                'backgroundColor': 'rgba(255, 255, 255, 0.15)',     #Fondo blanco de opacidad (0.15)
                'backdropFilter': 'blur(10px)',                     #Efecto de desenfoque
                'border': '1px solid rgba(255, 255, 255, 0.2)',     #Efecto de desenfoque
                'boxShadow': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',    #Efecto de desenfoque
                'margin': '0 auto 20px auto',                       #Margen     #'width': 'fit-content'
            },
            children=[
                html.H1(
                    id='subheader-estacion-texto',
                    style={
                        'color': '#5BC6E1',               #Color del texto
                        'textAlign': 'center',              #Alineacion del texto
                        'fontSize': '20px',                 #Tamaño de la fuente
                        'padding': '15px 30px',             #Espaciado
                        'margin': '0 auto 40px auto'        #Margen
                    },
                    children=[
                        "Datos recopilados de la estacion", #Texto
                    ]
                ),
                html.Div(
                    style={
                        'display': 'flex',              #Activar flexibildad
                        'flexDirection': 'row',         #Que se ordenen en columna
                        'justifyContent': 'center',     #Intentar centrar todo
                        'gap': '4%',                    #Espaciado entre elementos
                        'paddingLeft': '4%',            #Espaciado izquierda
                        'paddingRight': '4%'            #Espaciado derecha
                    },
                    children=[
                        dcc.Dropdown(
                            id='dropdown-datos',
                            options=[
                                {'label': 'Temperaturas y Humedad Interiores', 'value': 'TemperaturasI'},   #Opcion 1
                                {'label': 'Temperaturas y Humedad Exteriores', 'value': 'TemperaturasE'},   #Opcion 2
                                {'label': 'Presiones', 'value': 'Presiones'},                               #Opcion 3
                                {'label': 'Viento y su direccion', 'value': 'Vientos'}                      #Opcion 4
                            ],
                            value='TemperaturasI',      # Valor inicial por defecto
                            clearable=False,            # Evita que el usuario deje el menú vacío
                            style={ 'width': '40%', 'color': '#0E94B5' }
                        ),
                        dcc.Dropdown(
                            id='dropdown-meses',
                            options=[{'label': mes, 'value': i} for i, mes in enumerate(LabelOpcionesMeses)],
                            value=0, clearable=False,
                            style={ 'width': '30%', 'color': '#0E94B5' }
                        ),
                        dcc.Dropdown(
                            id='dropdown-dias',
                            options=[{'label': 'Todos los dias', 'value': -1}],
                            value=-1, clearable=False,
                            style={ 'width': '30%', 'color': "#0E94B5" }
                        )
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            [
                                html.Div(id='Graph1'),
                                html.Div(id='Graph2'),
                                html.Div(id='Graph3'),
                            ],
                            style=div_style
                        ),
                        html.Div(
                            [   
                                html.Div(id='Hist1'),
                                html.Div(id='Hist2'),
                                html.Div(id='Hist3'),
                                html.Div(id='Hist4')
                            ],
                            style=div_style
                        ),
                        html.Div(
                            [   
                                html.Div(id='Graph4'),
                                html.Div(id='Graph5'),
                                html.Div(id='Graph6'),
                            ],
                            style=div_style
                        ),
                        html.Div(
                            [   
                                html.Div(id='Hist5'),
                                html.Div(id='Hist6'),
                                html.Div(id='Hist7'),
                                html.Div(id='Hist8')
                            ],
                            style=div_style
                        ),
                    ]
                )
            ]
        )
    ]
)
@appEstacion.callback(
    Output('dropdown-dias', 'options'),
    Input('dropdown-meses', 'value')
)
def actualizar_dropdown_dias(IndiceMesDCC):
    if IndiceMesDCC == -1 or IndiceMesDCC is None:
        return [{'label': 'Todos los días', 'value': -1}]
    IndexDias = PosicionesContador[IndiceMesDCC]
    IndexMesesDias = [];    f = 0;
    for i in range(len(PosicionesContador)):
        j = 0; 
        IndexMeses = [];
        while(j < len(PosicionesContador[i])):
            IndexMeses.append(LabelDias[f]+"/"+LabelOpcionesMeses[i])
            j = j + 1; f = f + 1;
        IndexMesesDias.append(IndexMeses)
    IndexMeses = IndexMesesDias[IndiceMesDCC]
    return [{'label': 'Todos los dias', 'value': -1}] + [{'label': mes, 'value': dia} for dia, mes in zip(IndexDias, IndexMeses)]

@appEstacion.callback(
    Output("Graph1", 'children'),Output("Graph2", "children"),Output("Graph3", "children"),
    Output("Hist1", 'children'),Output("Hist2", "children"),Output("Hist3", "children"),Output("Hist4", "children"),
    Output("Graph4", 'children'),Output("Graph5", "children"),Output("Graph6", "children"),
    Output("Hist5", 'children'),Output("Hist6", "children"),Output("Hist7", "children"),Output("Hist8", "children"),
    Input('dropdown-datos', 'value'),
    Input('dropdown-meses', 'value'),
    Input('dropdown-dias', 'value')
)
def actualizar_grafico_o_datos(opcion, indiceMesDCC, indiceDiaDCC):
    if (indiceDiaDCC == - 1):
        #Posiciones de Vectores para Meses Inicio
        Pos1 = PosicionesInicio[indiceMesDCC] + 1;
        #Posiciones de Vectores para Meses Final
        Pos2 = PosicionesFinal[indiceMesDCC] + 2;
    else:
        Pos1 = PosicionesDiasInicio[indiceMesDCC][indiceDiaDCC] + 1;
        Pos2 = PosicionesDiasFinal[indiceMesDCC][indiceDiaDCC] + 2;
    Percentiles = [25,50,70];   ColorPerc = ['orange', 'red', 'green']
    #Graficas Temperaturas
    if opcion == "TemperaturasI":
        print("Registro Temperaturas Interiores")
        #Vectores Temperatura Interior
        VectorInsTempHum = [];  VectorInsDewWetHeat = [];   VectorTempHum = [];    VectorHeat = []; VectorInsDWH = [];
        #Inicio y Final del indice
        i = IndiceInsideTemp; Ante = IndiceInsideHeatMax;
        #Marcos color plata y bordes gruesos
        plt.rcParams['axes.edgecolor'] = '#FFFFFF'    
        plt.rcParams['axes.linewidth'] = 3.0
        while(i <= Ante):
            DatosFilas = df.iloc[Pos1:Pos2, i].tolist()                             #Datos de la fila del Mes seleccionado
            Datos = [x.item() if hasattr(x, 'item') else x for x in DatosFilas]     #Datos de la columna del rango de filas
            Indice = list(range(0, len(Datos)))                                     #Verificar integridad de los datos
            Curva.InterpolacionLinealNoGraph(Datos, Indice, len(Datos))             #Interpolar datos faltantes
            Datos = [float(i) for i in Datos]                                       #Convertir en Datos tipo float
            #Temperatura vs Humedad
            if(i == IndiceInsideTemp or i == IndiceInsideHum):
                #Vector media temp - hum
                VectorInsTempHum.append(Stats.MediaVector(Datos))
                #Vector Recolector graficas
                VectorTempHum.append(Datos)
                i = i + 1;
            #Temperatura vs Humedad Maximas
            elif(i == IndiceInsideTempMax or i == IndiceInsideHumMax):
                #Vector Recolector graficas
                VectorTempHum.append(Datos)
                i = i + 1;
            #Temperatura vs Humedad Minimas
            elif(i == IndiceInsideTempMin or i == IndiceInsideHumMin):
                #Vector Recolector graficas
                VectorTempHum.append(Datos)
                i = i + 1;
            #Dew vs Wet vs Heat Interiores
            elif(i == IndiceInsideDew or i == IndiceInsideWet or i == IndiceInsideHeat): 
                #Vector Recolector graficas
                VectorInsDewWetHeat.append(Stats.MediaVector(Datos))
                VectorInsDWH.append(Datos)
                if(i == IndiceInsideHeat):
                    #Vector Heat
                    VectorHeat.append(Datos)
                i = i + 1;
            #Heat vs Picos de calor
            elif(i == IndiceInsideHeatMax):
                #Vector Heat
                VectorHeat.append(Datos)
                i = i + 1;
        
        #################################################################
        ###                                                           ###
        ###     Grafica de medias de las Temperaturas y Humedades     ###
        ###                                                           ###
        #################################################################

        #Grafica de Battas Temperatura
        IndiceBarrasDobleAxial = [f"Temp: {VectorInsTempHum[0]:.4f}",f"Hum: {VectorInsTempHum[1]:.4f}"]
        figInsideTempHum, x1InsideTempHum = plt.subplots(figsize=(10, 6))
        figInsideTempHum.patch.set_alpha(0.0);  x1InsideTempHum.patch.set_alpha(0.0)
        barrasx1 = x1InsideTempHum.bar(IndiceBarrasDobleAxial[0], VectorInsTempHum[0],edgecolor = "#F76A25",linewidth=6.0, color="#F99462", alpha=0.9)
        x1InsideTempHum.bar_label(barrasx1, color='#DBDBDB', fontsize=12, fontweight='bold')
        x1InsideTempHum.set_ylabel('Temperatura Interior (°C)', color='#DBDBDB', fontname=fuente, fontsize=16, fontweight='bold')
        x1InsideTempHum.tick_params(axis='y', labelcolor='blue')
        x1InsideTempHum.set_yticks([0, 5, 10, 15, 20, 25, 30, 35])
        x1InsideTempHum.set_yticklabels(["0°C", "5°C", "10°C", "15°C", "20°C", "25°C", "30°C", "35°C"], color='#DBDBDB', fontsize=14, fontname=fuente)
        x2InsideTempHum = x1InsideTempHum.twinx()
        barrasx2 = x2InsideTempHum.bar(IndiceBarrasDobleAxial[1], VectorInsTempHum[1],edgecolor = "#25B1F7",linewidth=6.0,color ="#8ED7FB", alpha=0.9)
        x2InsideTempHum.bar_label(barrasx2, color='#DBDBDB', fontsize=12, fontweight='bold')
        x2InsideTempHum.set_ylabel('Humedad Interior (°C)', color='#DBDBDB', fontname=fuente, fontsize=16, fontweight='bold')
        x2InsideTempHum.set_yticks([10, 20, 30, 40, 50, 60, 70, 80, 90, 100]) 
        x2InsideTempHum.set_yticklabels(["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"], color='#DBDBDB', fontsize=14, fontname=fuente)
        x1InsideTempHum.set_xlabel("Temperatura Nominal - - - Humedad Relativa", color='#FFFFFF', fontname=fuente, fontsize=16, fontweight='bold')
        #Codificar
        bufInsideTempHum = io.BytesIO()
        plt.savefig(bufInsideTempHum, format="png", bbox_inches="tight", transparent=True)
        plt.close(figInsideTempHum)
        #Crear Objeto Doble Axial
        src_ins_temp_hum = f"data:image/png;base64,{base64.b64encode(bufInsideTempHum.getvalue()).decode('utf-8')}"
        BloqueInsideTempHum = html.Div([
            html.Label(id='input-ins-temp-hum',style=label_style,children=['Temperatura y Humedad']),
            html.Img(src=src_ins_temp_hum, style={'width': '100%', 'height': '300px'})
            ],  
            style={'width': '100%','textAlign': 'center'}
        )

        ####################################################################
        ###                                                              ###
        ###     Grafica de los Maximos y Minimos de las Temperaturas     ###
        ###                                                              ###
        ####################################################################

        #Grafica x,y de Temperaturas
        y1 = VectorTempHum[0];  y2 = VectorTempHum[1];  y3 = VectorTempHum[2]
        x = list(range(len(VectorTempHum[0])))
        figInsTempMaxMin, xInsTempMaxMin = plt.subplots(figsize=(10, 6))
        figInsTempMaxMin.patch.set_alpha(0.0);  xInsTempMaxMin.patch.set_alpha(0.0)
        XlimInf = min(x); XlimSup = max(x);     YlimInf = min(y1); YlimSup = max(y1);
        plt.xlim(XlimInf, XlimSup);             plt.ylim(YlimInf-0.5, YlimSup+0.5)
        xInsTempMaxMin.plot(x, y1, color = '#9D061F', alpha=0.4)
        xInsTempMaxMin.plot(x, y2, color = '#710416', alpha=0.4)
        xInsTempMaxMin.plot(x, y3, color = '#45020E', alpha=0.4)
        VectorNum = []; VectorLetter = []
        for i in range(11):
            factor = (i)*0.1
            VectorNum.append(((XlimSup - XlimInf)*factor)+XlimInf)
            VectorLetter.append(f'{((XlimSup - XlimInf)*factor)+XlimInf:.0f}')
        xInsTempMaxMin.set_xticks(VectorNum)
        xInsTempMaxMin.set_xticklabels(VectorLetter, color='#DBDBDB', fontsize=14, fontname=fuente)
        xInsTempMaxMin.set_yticks([YlimInf, YlimSup])
        xInsTempMaxMin.set_yticklabels([f'{YlimInf:.0f}°C', f'{YlimSup:.0f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        #Guardar imagen de MatplotLib
        bufTempMaxMin = io.BytesIO()
        plt.savefig(bufTempMaxMin, format="png", bbox_inches='tight', transparent=True)
        plt.close(figInsTempMaxMin)
        #Crear Objeto Temperaturas
        src_ins_temp_max_min = f"data:image/png;base64,{base64.b64encode(bufTempMaxMin.getvalue()).decode('utf-8')}"
        BloqueInsTempMaxMin = html.Div(
            [
                html.Label(id='input-interior-temp-max-min',style=label_style,children=['Maximos y minimos de la Temperatura °C']),
                html.Img(src=src_ins_temp_max_min, style={'width': '100%', 'height': '300px'})
            ],
            style={'width': '100%','textAlign': 'center'}
        )
        
        #################################################################
        ###                                                           ###
        ###     Grafica de los Maximos y Minimos de las Humedades     ###
        ###                                                           ###
        #################################################################

        y1 = VectorTempHum[3];  y2 = VectorTempHum[4];  y3 = VectorTempHum[5]
        x = list(range(len(VectorTempHum[0])))
        figInsHumMaxMin, xInsHumMaxMin = plt.subplots(figsize=(10, 6))
        figInsHumMaxMin.patch.set_alpha(0.0)
        xInsHumMaxMin.patch.set_alpha(0.0)
        XlimInf = min(x); XlimSup = max(x);
        YlimInf = min(y1); YlimSup = max(y1);
        plt.xlim(XlimInf, XlimSup);   plt.ylim(YlimInf-0.5, YlimSup+0.5)
        xInsHumMaxMin.plot(x, y1, color = '#2900A1', alpha=0.4)
        xInsHumMaxMin.plot(x, y2, color = '#1D0075', alpha=0.4)
        xInsHumMaxMin.plot(x, y3, color = '#120047', alpha=0.4)
        VectorNum = []; VectorLetter = []
        for i in range(11):
            factor = (i)*0.1
            VectorNum.append(((XlimSup - XlimInf)*factor)+XlimInf)
            VectorLetter.append(f'{((XlimSup - XlimInf)*factor)+XlimInf:.0f}')
        xInsHumMaxMin.set_xticks(VectorNum)
        xInsHumMaxMin.set_xticklabels(VectorLetter, color='#DBDBDB', fontsize=14, fontname=fuente)
        xInsHumMaxMin.set_yticks([YlimInf, YlimSup])
        xInsHumMaxMin.set_yticklabels([f'{YlimInf:.0f} (%)', f'{YlimSup:.0f} (%)'], color='#DBDBDB', fontsize=14, fontname=fuente)
        #Guardar imagen de MatplotLib
        bufInsHumMaxMin = io.BytesIO() 
        plt.savefig(bufInsHumMaxMin, format="png", bbox_inches='tight', transparent=True)
        plt.close(figInsHumMaxMin)

        #Codificacion
        src_ins_hum_max_min = f"data:image/png;base64,{base64.b64encode(bufInsHumMaxMin.getvalue()).decode('utf-8')}"
        BloqueInsHumMaxMin = html.Div([
            html.Label(id='input-titulo-hum-max-min',style=label_style,children=['Maximos y minimos de la Humeadad %']),
            html.Img(src=src_ins_hum_max_min, style={'width': '100%', 'height': '300px'})
            ],
            style={'width': '100%','textAlign': 'center'}
        )

        ##############################################################
        ###                                                        ###
        ###     Grafica de barra de interior de Dew, Wet, Heat     ###
        ###                                                        ###
        ##############################################################

        IndiceBarrasDWH = [f"Dew: {VectorInsDewWetHeat[0]:.4f}",f"Wet: {VectorInsDewWetHeat[1]:.4f}",f"Heat: {VectorInsDewWetHeat[2]:.4f}"]
        figInsDWH, xInsDWH = plt.subplots(figsize=(10, 6))
        figInsDWH.patch.set_alpha(0.0); xInsDWH.patch.set_alpha(0.0);
        barrasx01 = xInsDWH.bar(IndiceBarrasDWH[0], VectorInsDewWetHeat[0],edgecolor = "#20564E",linewidth=2.5,color="#88D3C9", alpha=0.9)
        barrasx02 = xInsDWH.bar(IndiceBarrasDWH[1], VectorInsDewWetHeat[1],edgecolor = '#204256',linewidth=2.5,color="#57B1EB", alpha=0.9)
        barrasx03 = xInsDWH.bar(IndiceBarrasDWH[2], VectorInsDewWetHeat[2],edgecolor = '#680D47',linewidth=2.5,color="#E535A4", alpha=0.9)
        xInsDWH.set_yticks([0, 5, 10, 15, 20, 25, 30, 35, 40])
        xInsDWH.set_yticklabels(["0°C", "5°C", "10°C", "15°C", "20°C", "25°C", "30°C", "35°C", "40°C"], color='#DBDBDB', fontsize=14, fontname=fuente)
        xInsDWH.bar_label(barrasx01, color='#88D3C9', fontsize=12, fontweight='bold')
        xInsDWH.bar_label(barrasx02, color='#57B1EB', fontsize=12, fontweight='bold')
        xInsDWH.bar_label(barrasx03, color='#E535A4', fontsize=12, fontweight='bold')
        #Codificar
        bufInsDWH = io.BytesIO()
        plt.savefig(bufInsDWH, format="png", bbox_inches="tight", transparent=True)
        plt.close(figInsDWH)
        #Crear Objeto Doble Axial
        src_ins_dwh = f"data:image/png;base64,{base64.b64encode(bufInsDWH.getvalue()).decode('utf-8')}"
        BloqueInsDWH = html.Div([
            html.Label(id='input-ins-dew-wet-heat',style=label_style,children=["'Punto de Rocio °C'   'Bulbo Húmedo °C'   'Sensación de calor °C'"]),
            html.Img(src=src_ins_dwh, style={'width': '100%', 'height': '400px'})
            ],
            style={'width': '100%','textAlign': 'center'}
        )

        ###########################################
        ###                                     ###
        ###     Grafica de Heat vs Heat Max     ###
        ###                                     ###
        ###########################################

        y1 = VectorHeat[0]; y2 = VectorHeat[1];
        x = list(range(len(VectorHeat[0])))
        figInsHMax, xInsHmax = plt.subplots(figsize=(10, 6))
        figInsHMax.patch.set_alpha(0.0)
        xInsHmax.patch.set_alpha(0.0)
        XlimInf = min(x); XlimSup = max(x);
        YlimInf = min(y1); YlimSup = max(y1);
        plt.xlim(XlimInf, XlimSup);   plt.ylim(YlimInf-0.5, YlimSup+0.5)
        xInsHmax.plot(x, y1, color = '#9FFF8A', alpha=0.4)
        xInsHmax.plot(x, y2, color = '#1EA300', alpha=0.4)
        VectorNum = []; VectorLetter = []
        for i in range(11):
            factor = (i)*0.1
            VectorNum.append(((XlimSup - XlimInf)*factor)+XlimInf)
            VectorLetter.append(f'{((XlimSup - XlimInf)*factor)+XlimInf:.0f}')
        xInsHmax.set_xticks(VectorNum)
        xInsHmax.set_xticklabels(VectorLetter, color='#DBDBDB', fontsize=14, fontname=fuente)
        xInsHmax.set_yticks([YlimInf, YlimSup])
        xInsHmax.set_yticklabels([f'{YlimInf:.0f}°C', f'{YlimSup:.0f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        #Guardar imagen de MatplotLib
        bufInsHMax = io.BytesIO() 
        plt.savefig(bufInsHMax, format="png", bbox_inches='tight', transparent=True)
        plt.close(figInsHMax)

        #Codificacion
        src_ins_h_max = f"data:image/png;base64,{base64.b64encode(bufInsHMax.getvalue()).decode('utf-8')}"
        BloqueInsHMax = html.Div([
            html.Label(id='input-ins-heat-heat_max',style=label_style,children=['Sensación Termica vs Picos de calor']),
            html.Img(src=src_ins_h_max, style={'width': '100%', 'height': '400px'})
            ],
            style={'width': '100%','textAlign': 'center'}
        )

        ###########################
        ###                     ###
        ###     Histogramas     ###
        ###                     ###
        ###########################

        #Histograma Temperatura
        figHistInsideTempHum, x1HistInsideTempHum = plt.subplots(figsize=(10, 6))
        y1 = VectorTempHum[0];      Stats.timsort(y1);  DatoModa1 = Stats.ModaVectorValor(y1);  MedianaInsTemp = Stats.MedianaVector(y1);
        VarianzaInsesgadaInsTemp = Stats.DesviacionMediaVector(y1, VectorInsTempHum[0]);
        DesviacionInsTemp = Stats.DesviacionNewton(VarianzaInsesgadaInsTemp);
        Varianza1 = Stats.VarianzaVector(y1);
        DesviacionInsTempNM = Stats.DesviacionNewton(Varianza1);
        PercInsTemp = Stats.Percentil(y1, Percentiles);
        figHistInsideTempHum.patch.set_alpha(0.0);  x1HistInsideTempHum.patch.set_alpha(0.0);
        XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(y1[len(y1) - 1]))
        x1HistInsideTempHum.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = '#F76A25', color="#F99462",linewidth=4.0, alpha=0.6)
        x1HistInsideTempHum.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
        x1HistInsideTempHum.set_xticks([XlimInf1,PercInsTemp[0],PercInsTemp[1],PercInsTemp[2],XlimSup1])
        x1HistInsideTempHum.set_xticklabels([f'{XlimInf1:.2f}°C',f'{PercInsTemp[0]:.0f}°C',f'{PercInsTemp[1]:.0f}°C',f'{PercInsTemp[2]:.0f}°C',f'{XlimSup1:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        for p, val, col in zip(Percentiles,PercInsTemp,ColorPerc):
            x1HistInsideTempHum.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistInsideTempHum1 = io.BytesIO()
        plt.savefig(bufHistInsideTempHum1, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistInsideTempHum)
        src_hist_ins_temp_hum_1 = f"data:image/png;base64,{base64.b64encode(bufHistInsideTempHum1.getvalue()).decode('utf-8')}"
        BloqueHistInsideTempHum1 = html.Div([
            html.Img(src=src_hist_ins_temp_hum_1, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ins-temp-hum',style=label_style,children=['Temperatura °C']),
            html.P([
                html.Strong('Media Aritmética'),html.Br(),
                f'{VectorInsTempHum[0]:.4f}',html.Br(),
                html.Strong('Mediana'),html.Br(),
                f'{MedianaInsTemp:.0f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'{VarianzaInsesgadaInsTemp:.8f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'{DesviacionInsTemp:.8f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'{Varianza1:.8f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'{DesviacionInsTempNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Minimo: {y1[0]:.0f}',f'\tMaximo: {y1[len(y1) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'{DatoModa1:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'P{Percentiles[0]}: {PercInsTemp[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercInsTemp[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercInsTemp[2]:.0f}°C'
            ])
            ],
            style={'width': '100%','textAlign': 'center'}
        )
        #Histograma Humedad
        figHistInsideTempHum, x2HistInsideTempHum = plt.subplots(figsize=(10, 6))
        y2 = VectorTempHum[3];      Stats.timsort(y2);  DatoModa2 = Stats.ModaVectorValor(y2); MedianaInsHum = Stats.MedianaVector(y2);
        VarianzaInsesgadaInsHum = Stats.DesviacionMediaVector(y2, VectorInsTempHum[1]);
        DesviacionInsHum = Stats.DesviacionNewton(VarianzaInsesgadaInsHum);
        Varianza2 = Stats.VarianzaVector(y2);
        DesviacionInsHumNM = Stats.DesviacionNewton(Varianza2);
        PercInsHum = Stats.Percentil(y2, Percentiles);
        figHistInsideTempHum.patch.set_alpha(0.0);  x2HistInsideTempHum.patch.set_alpha(0.0);
        XlimInf2 = y2[0];    XlimSup2 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(y2[len(y2) - 1]))
        x2HistInsideTempHum.hist(y2, bins=Rango2,rwidth = 1.2, edgecolor = '#25B1F7',color ="#8ED7FB",linewidth=4.0, alpha=0.6)
        x2HistInsideTempHum.set_xticks([XlimInf2,PercInsHum[0],PercInsHum[1],PercInsHum[2],XlimSup2])
        x2HistInsideTempHum.set_xticklabels([f'{XlimInf2:.2f}%',f'{PercInsHum[0]:.0f}%',f'{PercInsHum[1]:.0f}%',f'{PercInsHum[2]:.0f}%',f'{XlimSup2:.2f}%'], color='#DBDBDB', fontsize=14, fontname=fuente)
        x2HistInsideTempHum.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercInsHum,ColorPerc):
            x2HistInsideTempHum.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistInsideTempHum2 = io.BytesIO()
        plt.savefig(bufHistInsideTempHum2, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistInsideTempHum)
        src_hist_ins_temp_hum_2 = f"data:image/png;base64,{base64.b64encode(bufHistInsideTempHum2.getvalue()).decode('utf-8')}"
        BloqueHistInsideTempHum2 = html.Div([
            html.Img(src=src_hist_ins_temp_hum_2, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ins-temp-hum',style=label_style,children=['Humedad (%)']),
            html.P([
                html.Strong('Media Aritmética'),html.Br(),
                f'{VectorInsTempHum[1]:.0f}',html.Br(),
                html.Strong('Mediana'),html.Br(),
                f'{MedianaInsHum:.4f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'{VarianzaInsesgadaInsHum:.8f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'{DesviacionInsHum:.8f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'{Varianza2:.8f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'{DesviacionInsHumNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Minimo: {y2[0]:.0f}',f'\tMaximo: {y2[len(y2) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'{DatoModa2:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'P{Percentiles[0]}: {PercInsHum[0]:.0f}%',f'\tP{Percentiles[1]}: {PercInsHum[1]:.0f}%',f'\tP{Percentiles[2]}: {PercInsHum[2]:.0f}%'
            ])
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histrograma Temperaturas
        y2 = VectorTempHum[1];  y3 = VectorTempHum[2]
        Stats.timsort(y2);                      Stats.timsort(y3);
        Media2 = Stats.MediaVector(y2);         Media3 = Stats.MediaVector(y3);
        Mediana2 = Stats.MedianaVector(y2);     Mediana3 = Stats.MedianaVector(y3);
        VarianzaInsesgadaInsTempMax = Stats.DesviacionMediaVector(y2, Media2);
        DesviacionInsTempMax = Stats.DesviacionNewton(VarianzaInsesgadaInsTempMax);
        VarianzaInsesgadaInsTempMin = Stats.DesviacionMediaVector(y3, Media3);
        DesviacionInsTempMin = Stats.DesviacionNewton(VarianzaInsesgadaInsTempMin);
        Moda2 = Stats.ModaVector(y2);           DatoModa2 = Stats.ModaVectorValor(y2);
        Moda3 = Stats.ModaVector(y3);           DatoModa3 = Stats.ModaVectorValor(y3);
        Varianza2 = Stats.VarianzaVector(y2);   Varianza3 = Stats.VarianzaVector(y3);
        DesviacionInsTempMaxNM = Stats.DesviacionNewton(Varianza2);
        DesviacionInsTempMinNM = Stats.DesviacionNewton(Varianza3);
        PercInsTempMax = Stats.Percentil(y2, Percentiles);
        PercInsTempMin = Stats.Percentil(y3, Percentiles);
        figHistInsTempMaxMin, xHistInsTempMaxMin = plt.subplots(figsize=(10, 6));
        figHistInsTempMaxMin.patch.set_alpha(0.0);  xHistInsTempMaxMin.patch.set_alpha(0.0);
        XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(y2[len(y2) - 1]))
        xHistInsTempMaxMin.hist(y2, bins=Rango,rwidth = 1.2, color = '#9D061F',linewidth=4.0, edgecolor = 'black', alpha=0.3)
        xHistInsTempMaxMin.hist(y3, bins=Rango,rwidth = 1.2, color = '#45020E',linewidth=4.0, edgecolor = 'black', alpha=0.3)
        xHistInsTempMaxMin.set_xticks([XlimInf2,PercInsTempMax[0],PercInsTempMax[1],PercInsTempMax[2],PercInsTempMin[0],PercInsTempMin[1],PercInsTempMin[2],XlimSup2])
        xHistInsTempMaxMin.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercInsTempMax[0]:.0f}°C',f'{PercInsTempMax[1]:.0f}°C',f'{PercInsTempMax[2]:.0f}°C',f'{PercInsTempMin[0]:.0f}°C',f'{PercInsTempMin[1]:.0f}°C',f'{PercInsTempMin[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        xHistInsTempMaxMin.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercInsTempMax,ColorPerc):
            xHistInsTempMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        for p, val, col in zip(Percentiles,PercInsTempMin,ColorPerc):
            xHistInsTempMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistInsTempMaxMin = io.BytesIO()
        plt.savefig(bufHistInsTempMaxMin, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistInsTempMaxMin)
        src_hist_ins_temp_max_min = f"data:image/png;base64,{base64.b64encode(bufHistInsTempMaxMin.getvalue()).decode('utf-8')}"
        BloqueHistInsideTempMaxMin = html.Div([
            html.Img(src=src_hist_ins_temp_max_min, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ins-temp-max-min',style=label_style,children=['Temperaturas °C']),
            html.P([
                html.Strong('Medias Aritméticas'),html.Br(),
                f'Para maximas: {Media2:.4f}',f'\tPara Minimos: {Media3:.4f}',html.Br(),
                html.Strong('Medianas'),html.Br(),
                f'Para maximas: {Mediana2:.0f}',f'\tPara Minimos: {Mediana3:.0f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'Para maximas: {VarianzaInsesgadaInsTempMax:.4f}',f'\tPara Minimos: {VarianzaInsesgadaInsTempMin:.4f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'Para maximas: {DesviacionInsTempMax:.4f}',f'\tPara Minimos: {DesviacionInsTempMin:.4f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'Para maximas: {Varianza2:.4f}',f'\tPara Minimos: {Varianza3:.4f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'Para maximas: {DesviacionInsTempMaxNM:.4f}',f'\tPara Minimos: {DesviacionInsTempMinNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Para maximas: {y2[0]:.0f}',f',{y2[len(y2) - 1]:.0f}',f'\tPara Minimos: {y3[0]:.0f}',f' {y3[len(y3) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'Para maximas: {DatoModa2:.0f}',f'\tPara Minimos: {DatoModa3:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'Maximas: P{Percentiles[0]}: {PercInsTempMax[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercInsTempMax[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercInsTempMax[2]:.0f}°C',html.Br(),
                f'Minimas: P{Percentiles[0]}: {PercInsTempMin[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercInsTempMin[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercInsTempMin[2]:.0f}°C'
            ])  
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histrograma Humedades
        y2 = VectorTempHum[4];  y3 = VectorTempHum[5]
        Stats.timsort(y2);                      Stats.timsort(y3);
        Media2 = Stats.MediaVector(y2);         Media3 = Stats.MediaVector(y3);
        Mediana2 = Stats.MedianaVector(y2);     Mediana3 = Stats.MedianaVector(y3);
        VarianzaInsesgadaInsHumMax = Stats.DesviacionMediaVector(y2, Media2);
        DesviacionInsHumMax = Stats.DesviacionNewton(VarianzaInsesgadaInsHumMax);
        VarianzaInsesgadaInsHumMin = Stats.DesviacionMediaVector(y3, Media3);
        DesviacionInsHumMin = Stats.DesviacionNewton(VarianzaInsesgadaInsHumMin);
        DatoModa2 = Stats.ModaVectorValor(y2);  DatoModa3 = Stats.ModaVectorValor(y3);
        Varianza2 = Stats.VarianzaVector(y2);   Varianza3 = Stats.VarianzaVector(y3);
        DesviacionInsHumMaxNM = Stats.DesviacionNewton(Varianza2);
        DesviacionInsHumMinNM = Stats.DesviacionNewton(Varianza3);
        PercInsHumMax = Stats.Percentil(y2, Percentiles);
        PercInsHumMin = Stats.Percentil(y3, Percentiles);
        figHistInsHumMaxMin, xHistInsHumMaxMin = plt.subplots(figsize=(10, 6));
        figHistInsHumMaxMin.patch.set_alpha(0.0);  xHistInsHumMaxMin.patch.set_alpha(0.0);
        XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(y2[len(y2) - 1]));
        xHistInsHumMaxMin.hist(y2, bins=Rango+1,rwidth = 1.2, color = '#2900A1',linewidth=4.0, edgecolor = "#35A8F5", alpha=0.3)
        xHistInsHumMaxMin.hist(y3, bins=Rango+1,rwidth = 1.2, color = '#120047',linewidth=4.0, edgecolor = "#2E02B2", alpha=0.3)
        xHistInsHumMaxMin.set_xticks([XlimInf2,PercInsHumMax[0],PercInsHumMax[1],PercInsHumMax[2],PercInsHumMin[0],PercInsHumMin[1],PercInsHumMin[2],XlimSup2])
        xHistInsHumMaxMin.set_xticklabels([f'{XlimInf2:.2f} %',f'{PercInsHumMax[0]:.0f}°C',f'{PercInsHumMax[1]:.0f}°C',f'{PercInsHumMax[2]:.0f}°C',f'{PercInsHumMin[0]:.0f}°C',f'{PercInsHumMin[1]:.0f}°C',f'{PercInsHumMin[2]:.0f}°C',f'{XlimSup2:.2f} %'], color='#DBDBDB', fontsize=14, fontname=fuente)
        xHistInsHumMaxMin.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercInsHumMax,ColorPerc):
            xHistInsHumMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        for p, val, col in zip(Percentiles,PercInsHumMin,ColorPerc):
            xHistInsHumMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistInsHumMaxMin = io.BytesIO()
        plt.savefig(bufHistInsHumMaxMin, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistInsHumMaxMin)
        src_hist_ins_hum_max_min = f"data:image/png;base64,{base64.b64encode(bufHistInsHumMaxMin.getvalue()).decode('utf-8')}"
        BloqueHistInsideHumMaxMin = html.Div([
            html.Img(src=src_hist_ins_hum_max_min, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ins-hum-max-min',style=label_style,children=['Humedades (%)']),
            html.P([
                html.Strong('Medias Aritméticas'),html.Br(),
                f'Para maximas: {Media2:.4f}',f'\tPara Minimos: {Media3:.4f}',html.Br(),
                html.Strong('Medianas'),html.Br(),
                f'Para maximas: {Mediana2:.0f}',f'\tPara Minimos: {Mediana3:.0f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'Para maximas: {VarianzaInsesgadaInsHumMax:.4f}',f'\tPara Minimos: {VarianzaInsesgadaInsHumMin:.4f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'Para maximas: {DesviacionInsHumMax:.4f}',f'\tPara Minimos: {DesviacionInsHumMin:.4f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'Para maximas: {Varianza2:.4f}',f'\tPara Minimos: {Varianza3:.4f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'Para maximas: {DesviacionInsHumMaxNM:.4f}',f'\tPara Minimos: {DesviacionInsHumMinNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Para maximas: {y2[0]:.0f}',f',{y2[len(y2) - 1]:.0f}',f'\tPara Minimos: {y3[0]:.0f}',f' {y3[len(y3) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'Para maximas: {DatoModa2:.0f}',f'\tPara Minimos: {DatoModa3:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'Maximas: P{Percentiles[0]}: {PercInsHumMax[0]:.0f}%',f'\tP{Percentiles[1]}: {PercInsHumMax[1]:.0f}%',f'\tP{Percentiles[2]}: {PercInsHumMax[2]:.0f}%',html.Br(),
                f'Minimas: P{Percentiles[0]}: {PercInsHumMin[0]:.0f}%',f'\tP{Percentiles[1]}: {PercInsHumMin[1]:.0f}%',f'\tP{Percentiles[2]}: {PercInsHumMin[2]:.0f}%'
            ])
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histograma del Punto de Rocio Interior
        figHistInsideD, x1HistInsideD = plt.subplots(figsize=(10, 6))
        y4 = VectorInsDWH[0];      Stats.timsort(y4);  DatoModa4 = Stats.ModaVectorValor(y4); MedianaInsD = Stats.MedianaVector(y4);
        VarianzaInsesgadaInsD = Stats.DesviacionMediaVector(y4, VectorInsDewWetHeat[0]);
        DesviacionInsD = Stats.DesviacionNewton(VarianzaInsesgadaInsD);
        Varianza4 = Stats.VarianzaVector(y4);
        DesviacionInsDNM = Stats.DesviacionNewton(Varianza4);
        PercInsD = Stats.Percentil(y4, Percentiles);
        figHistInsideD.patch.set_alpha(0.0);  x1HistInsideD.patch.set_alpha(0.0);
        XlimInf2 = y4[0];    XlimSup2 = y4[len(y4) - 1];  Rango4 = int(RegladeSturges(y4[len(y4) - 1]))
        x1HistInsideD.hist(y4, bins=Rango4,rwidth = 1.2, edgecolor = '#20564E',color ="#20564E",linewidth=4.0, alpha=0.6)
        x1HistInsideD.set_xticks([XlimInf2,PercInsD[0],PercInsD[1],PercInsD[2],XlimSup2])
        x1HistInsideD.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercInsD[0]:.0f}°C',f'{PercInsD[1]:.0f}°C',f'{PercInsD[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        x1HistInsideD.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercInsD,ColorPerc):
            x1HistInsideD.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistInsideD = io.BytesIO()
        plt.savefig(bufHistInsideD, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistInsideD)
        src_hist_ins_d = f"data:image/png;base64,{base64.b64encode(bufHistInsideD.getvalue()).decode('utf-8')}"
        BloqueHistInsideD = html.Div([
            html.Img(src=src_hist_ins_d, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ins-d',style=label_style,children=['Punto de Rocio°C']),
            html.P([
                html.Strong('Media Aritmética'),html.Br(),
                f'{VectorInsDewWetHeat[0]:.0f}',html.Br(),
                html.Strong('Mediana'),html.Br(),
                f'{MedianaInsD:.4f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'{VarianzaInsesgadaInsD:.8f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'{DesviacionInsD:.8f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'{Varianza4:.8f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'{DesviacionInsDNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Minimo: {y4[0]:.0f}',f'\tMaximo: {y4[len(y4) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'{DatoModa4:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'P{Percentiles[0]}: {PercInsD[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercInsD[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercInsD[2]:.0f}°C'
            ])
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histograma del Bulbo Húmedo
        figHistInsideW, x2HistInsideW = plt.subplots(figsize=(10, 6))
        y5 = VectorInsDWH[1];      Stats.timsort(y5);  DatoModa5 = Stats.ModaVectorValor(y5); MedianaInsW = Stats.MedianaVector(y5);
        VarianzaInsesgadaInsW = Stats.DesviacionMediaVector(y5, VectorInsDewWetHeat[1]);
        DesviacionInsW = Stats.DesviacionNewton(VarianzaInsesgadaInsW);
        Varianza5 = Stats.VarianzaVector(y5);
        DesviacionInsWNM = Stats.DesviacionNewton(Varianza5);
        PercInsW = Stats.Percentil(y5, Percentiles);
        figHistInsideW.patch.set_alpha(0.0);  x2HistInsideW.patch.set_alpha(0.0);
        XlimInf2 = y5[0];    XlimSup2 = y5[len(y5) - 1];  Rango5 = int(RegladeSturges(y5[len(y5) - 1]))
        x2HistInsideW.hist(y5, bins=Rango5,rwidth = 1.2, edgecolor = '#204256',color ="#57B1EB",linewidth=4.0, alpha=0.6)
        x2HistInsideW.set_xticks([XlimInf2,PercInsW[0],PercInsW[1],PercInsW[2],XlimSup2])
        x2HistInsideW.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercInsW[0]:.0f}°C',f'{PercInsW[1]:.0f}°C',f'{PercInsW[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        x2HistInsideW.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercInsW,ColorPerc):
            x2HistInsideW.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistInsideW = io.BytesIO()
        plt.savefig(bufHistInsideW, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistInsideW)
        src_hist_ins_w = f"data:image/png;base64,{base64.b64encode(bufHistInsideW.getvalue()).decode('utf-8')}"
        BloqueHistInsideW = html.Div([
            html.Img(src=src_hist_ins_w, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ins-w',style=label_style,children=['Bulbo Húmedo°C']),
            html.P([
                html.Strong('Media Aritmética'),html.Br(),
                f'{VectorInsDewWetHeat[1]:.0f}',html.Br(),
                html.Strong('Mediana'),html.Br(),
                f'{MedianaInsW:.4f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'{VarianzaInsesgadaInsW:.8f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'{DesviacionInsW:.8f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'{Varianza5:.8f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'{DesviacionInsWNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Minimo: {y5[0]:.0f}',f'\tMaximo: {y5[len(y5) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'{DatoModa5:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'P{Percentiles[0]}: {PercInsW[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercInsW[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercInsW[2]:.0f}°C'
            ])
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histograma de sensacion termica
        figHistInsideH, x3HistInsideH = plt.subplots(figsize=(10, 6))
        y6 = VectorInsDWH[2];      Stats.timsort(y6);  DatoModa6 = Stats.ModaVectorValor(y6); MedianaInsH = Stats.MedianaVector(y6);
        VarianzaInsesgadaInsH = Stats.DesviacionMediaVector(y6, VectorInsDewWetHeat[2]);
        DesviacionInsH = Stats.DesviacionNewton(VarianzaInsesgadaInsH);
        Varianza6 = Stats.VarianzaVector(y6);
        DesviacionInsHNM = Stats.DesviacionNewton(Varianza6);
        PercInsH = Stats.Percentil(y6, Percentiles);
        figHistInsideH.patch.set_alpha(0.0);  x3HistInsideH.patch.set_alpha(0.0);
        XlimInf2 = y6[0];    XlimSup2 = y6[len(y6) - 1];  Rango6 = int(RegladeSturges(y6[len(y6) - 1]))
        x3HistInsideH.hist(y6, bins=Rango6,rwidth = 1.2, edgecolor = '#680D47',color ="#E535A4",linewidth=4.0, alpha=0.6)
        x3HistInsideH.set_xticks([XlimInf2,PercInsH[0],PercInsH[1],PercInsH[2],XlimSup2])
        x3HistInsideH.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercInsH[0]:.0f}°C',f'{PercInsH[1]:.0f}°C',f'{PercInsH[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        x3HistInsideH.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercInsH,ColorPerc):
            x3HistInsideH.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistInsideH = io.BytesIO()
        plt.savefig(bufHistInsideH, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistInsideH)
        src_hist_ins_h = f"data:image/png;base64,{base64.b64encode(bufHistInsideH.getvalue()).decode('utf-8')}"
        BloqueHistInsideH = html.Div([
            html.Img(src=src_hist_ins_h, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ins-h',style=label_style,children=['Sensacion calorica°C']),
            html.P([
                html.Strong('Media Aritmética'),html.Br(),
                f'{VectorInsDewWetHeat[2]:.0f}',html.Br(),
                html.Strong('Mediana'),html.Br(),
                f'{MedianaInsH:.4f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'{VarianzaInsesgadaInsH:.8f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'{DesviacionInsH:.8f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'{Varianza6:.8f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'{DesviacionInsHNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Minimo: {y6[0]:.0f}',f'\tMaximo: {y6[len(y6) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'{DatoModa6:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'P{Percentiles[0]}: {PercInsH[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercInsH[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercInsH[2]:.0f}°C'
            ])
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histograma de sensacion termica maxima
        figHistInsideHMax, x4HistInsideHMax = plt.subplots(figsize=(10, 6))
        y7 = VectorHeat[1];      Stats.timsort(y7);  DatoModa7 = Stats.ModaVectorValor(y7); MedianaInsHMax = Stats.MedianaVector(y7); Media7=Stats.MediaVector(y7)
        VarianzaInsesgadaInsHMax = Stats.DesviacionMediaVector(y7, Media7);
        DesviacionInsHMax = Stats.DesviacionNewton(VarianzaInsesgadaInsHMax);
        Varianza7 = Stats.VarianzaVector(y7);
        DesviacionInsHMaxNM = Stats.DesviacionNewton(Varianza7);
        PercInsHMax = Stats.Percentil(y7, Percentiles);
        figHistInsideHMax.patch.set_alpha(0.0);  x4HistInsideHMax.patch.set_alpha(0.0);
        XlimInf2 = y7[0];    XlimSup2 = y7[len(y7) - 1];  Rango7 = int(RegladeSturges(y7[len(y7) - 1]))
        x4HistInsideHMax.hist(y7, bins=Rango7,rwidth = 1.2, edgecolor = "#6D0B10",color ="#ED1932",linewidth=4.0, alpha=0.6)
        x4HistInsideHMax.set_xticks([XlimInf2,PercInsHMax[0],PercInsHMax[1],PercInsHMax[2],XlimSup2])
        x4HistInsideHMax.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercInsHMax[0]:.0f}°C',f'{PercInsHMax[1]:.0f}°C',f'{PercInsHMax[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        x4HistInsideHMax.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercInsHMax,ColorPerc):
            x4HistInsideHMax.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistInsideHMax = io.BytesIO()
        plt.savefig(bufHistInsideHMax, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistInsideHMax)
        src_hist_ins_h_max = f"data:image/png;base64,{base64.b64encode(bufHistInsideHMax.getvalue()).decode('utf-8')}"
        BloqueHistInsideHMax = html.Div([
            html.Img(src=src_hist_ins_h_max, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ins-h-max',style=label_style,children=['Sensacion calorica maxima°C']),
            html.P([
                html.Strong('Media Aritmética'),html.Br(),
                f'{Media7:.4f}',html.Br(),
                html.Strong('Mediana'),html.Br(),
                f'{MedianaInsHMax:.0f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'{VarianzaInsesgadaInsHMax:.8f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'{DesviacionInsHMax:.8f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'{Varianza7:.8f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'{DesviacionInsHMaxNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Minimo: {y7[0]:.0f}',f'\tMaximo: {y7[len(y7) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'{DatoModa7:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'P{Percentiles[0]}: {PercInsHMax[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercInsHMax[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercInsHMax[2]:.0f}°C'
            ])
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        return BloqueInsideTempHum, BloqueInsTempMaxMin, BloqueInsHumMaxMin,BloqueHistInsideTempHum1, BloqueHistInsideTempHum2, BloqueHistInsideTempMaxMin, BloqueHistInsideHumMaxMin, BloqueInsDWH, BloqueInsHMax, None,BloqueHistInsideD, BloqueHistInsideW, BloqueHistInsideH, BloqueHistInsideHMax
    
    if opcion == "TemperaturasE":
        print("Registro Temperaturas Exteriores")
        #Vectores Temperatura Exterior
        VectorExtTempHumM = [];     VectorExtTempHum = [];  
        #Vectores Dew - Wet
        VectorExtDewWetM = [];      VectorExtDewWet = [];
        #Inicio y Final del indice
        i = IndiceExteriorTemp; Ante = IndiceExteriorWetMin;
        #Marcos color plata y bordes gruesos
        plt.rcParams['axes.edgecolor'] = '#FFFFFF'    
        plt.rcParams['axes.linewidth'] = 3.0
        while(i <= Ante):
            #Datos de la fila del Mes seleccionado
            DatosFilas = df.iloc[Pos1:Pos2, i].tolist()
            #Datos de la columna del rango de filas
            Datos = [x.item() if hasattr(x, 'item') else x for x in DatosFilas]
            #Verificar integridad de los datos
            Indice = list(range(0, len(Datos)))
            Curva.InterpolacionLinealNoGraph(Datos, Indice, len(Datos))
            #Convertir en Datos
            Datos = [float(i) for i in Datos]
            if(i == IndiceExteriorTemp or i == IndiceExteriorHum):
                #Vector media temp - hum
                VectorExtTempHumM.append(Stats.MediaVector(Datos))
                #Vector Recolector graficas
                VectorExtTempHum.append(Datos)
                i = i + 1;
            #Temperatura vs Humedad Maximas
            elif(i == IndiceExteriorTempMax or i == IndiceExteriorHumMax):
                #Vector Recolector graficas
                VectorExtTempHum.append(Datos)
                i = i + 1;
            #Temperatura vs Humedad Minimas
            elif(i == IndiceExteriorTempMin or i == IndiceExteriorHumMin):
                #Vector Recolector graficas
                VectorExtTempHum.append(Datos)
                i = i + 1;
            #Vector media dew - wet
            elif(i == IndiceExteriorDew or i == IndiceExteriorWet):
                #Vector media dew - wet
                VectorExtDewWetM.append(Stats.MediaVector(Datos))
                #Vector Recolector graficas
                VectorExtDewWet.append(Datos)
                i = i + 1;
            #Punto de Rocio vs Bobina Humedad Maximos
            elif(i == IndiceExteriorDewMax or i == IndiceExteriorWetMax):
                #Vector Recolector graficas
                VectorExtDewWet.append(Datos)
                i = i + 1;
            #Punto de Rocio vs Bobina Humedad Minimos
            elif(i == IndiceExteriorDewMin or i == IndiceExteriorWetMin):
                #Vector Recolector graficas
                VectorExtDewWet.append(Datos)
                i = i + 1;

        #################################################################
        ###                                                           ###
        ###     Grafica de medias de las Temperaturas y Humedades     ###
        ###                                                           ###
        #################################################################

        #Grafica Temperatura vs Humedad
        IndiceBarrasDobleAxial = [f"Temp: {VectorExtTempHumM[0]:.4f}",f"Hum: {VectorExtTempHumM[1]:.4f}"]
        figExteriorTempHum, x1ExteriorTempHum = plt.subplots(figsize=(10, 6))
        figExteriorTempHum.patch.set_alpha(0.0);    x1ExteriorTempHum.patch.set_alpha(0.0)
        barrasx1 = x1ExteriorTempHum.bar(IndiceBarrasDobleAxial[0], VectorExtTempHumM[0],edgecolor = "#91122B",linewidth=4.0, color="#E84163", alpha=0.9)
        x1ExteriorTempHum.bar_label(barrasx1, color='#C2C2C2', fontsize=12, fontweight='bold')
        x1ExteriorTempHum.set_ylabel('Temperatura Exterior (°C)', color='#C2C2C2', fontname=fuente, fontsize=16, fontweight='bold')
        x1ExteriorTempHum.set_yticks([0, 5, 10, 15, 20, 25, 30, 35])
        x1ExteriorTempHum.set_yticklabels(["0°C", "5°C", "10°C", "15°C", "20°C", "25°C", "30°C", "35°C"], color='#DBDBDB', fontsize=14, fontname=fuente)
        x2ExteriorTempHum = x1ExteriorTempHum.twinx();  #Axis alterno
        barrasx2 = x2ExteriorTempHum.bar(IndiceBarrasDobleAxial[1], VectorExtTempHumM[1],edgecolor = "#060047",linewidth=4.0,color ="#1B08FF", alpha=0.9, label='Porcentaje de Humedad')
        x2ExteriorTempHum.bar_label(barrasx2, color='#C2C2C2', fontsize=12, fontweight='bold')
        x2ExteriorTempHum.set_ylabel('Humedad Exterior (%)', color='#C2C2C2', fontname=fuente, fontsize=16, fontweight='bold')
        x2ExteriorTempHum.set_yticks([10, 20, 30, 40, 50, 60, 70, 80, 90, 100]) 
        x2ExteriorTempHum.set_yticklabels(["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"], color='#DBDBDB', fontsize=14, fontname=fuente)
        #Codificar
        bufExtTempHum = io.BytesIO()
        plt.savefig(bufExtTempHum, format="png", bbox_inches="tight", transparent=True)
        plt.close(figExteriorTempHum)
        #Crear Objeto Doble Axial
        src_ext_temp_hum = f"data:image/png;base64,{base64.b64encode(bufExtTempHum.getvalue()).decode('utf-8')}"
        BloqueExtTempHum = html.Div([
            html.Label(id='input-ext-temp-hum',style=label_style,children=['Temperatura y Humedad' ]),
            html.Img(src=src_ext_temp_hum, style={'width': '100%', 'height': '300px'})
            ],  
            style={'width': '100%','textAlign': 'center'}
        )  

        ############################################################################
        ###                                                                      ###
        ###     Grafica de los Maximos y Minimos de la Temperatura Exterior      ###
        ###                                                                      ###
        ############################################################################
    
        y1 = VectorExtTempHum[0];   y2 = VectorExtTempHum[1];   y3 = VectorExtTempHum[2]
        x = list(range(len(VectorExtTempHum[0])))
        figExtTempMaxMin, xExtTempMaxMin = plt.subplots(figsize=(10, 6))
        figExtTempMaxMin.patch.set_alpha(0.0)
        xExtTempMaxMin.patch.set_alpha(0.0)
        XlimInf = min(x); XlimSup = max(x);
        YlimInf = min(y1); YlimSup = max(y1);
        plt.xlim(XlimInf, XlimSup);   plt.ylim(YlimInf-0.5, YlimSup+0.5)
        
        xExtTempMaxMin.plot(x, y1, color = '#9D061F', alpha=0.4)
        xExtTempMaxMin.plot(x, y2, color = '#710416', alpha=0.4)
        xExtTempMaxMin.plot(x, y3, color = '#45020E', alpha=0.4)
        VectorNum = []; VectorLetter = []
        for i in range(11):
            factor = (i)*0.1
            VectorNum.append(((XlimSup - XlimInf)*factor)+XlimInf)
            VectorLetter.append(f'{((XlimSup - XlimInf)*factor)+XlimInf:.0f}')
        xExtTempMaxMin.set_xticks(VectorNum)
        xExtTempMaxMin.set_xticklabels(VectorLetter, color='#DBDBDB', fontsize=14, fontname=fuente)
        xExtTempMaxMin.set_yticks([YlimInf, YlimSup])
        xExtTempMaxMin.set_yticklabels([f'{YlimInf:.0f}°C', f'{YlimSup:.0f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        #Guardar imagen de MatplotLib
        bufExtTempMaxMin = io.BytesIO()
        plt.savefig(bufExtTempMaxMin, format="png", bbox_inches='tight', transparent=True)
        plt.close(figExtTempMaxMin)
        
        #Crear Objeto Temperatura
        src_ext_temp_max_min = f"data:image/png;base64,{base64.b64encode(bufExtTempMaxMin.getvalue()).decode('utf-8')}"
        BloqueExtTempMaxMin = html.Div(
            [
                html.Label(id='input-ext-temp-max-min',style=label_style,children=['Maximos y minimos de la Temperatura °C']),
                html.Img(src=src_ext_temp_max_min, style={'width': '100%', 'height': '300px'})
            ],
            style={'width': '100%','textAlign': 'center'}
        )

        ##########################################################################
        ###                                                                    ###
        ###     Grafica de los Maximos y Minimos de la Humedades Exterior      ###
        ###                                                                    ###
        ##########################################################################

        y1 = VectorExtTempHum[3];   y2 = VectorExtTempHum[4];   y3 = VectorExtTempHum[5]
        x = list(range(len(VectorExtTempHum[0])))
        figExtHumMaxMin, xExtHumMaxMin = plt.subplots(figsize=(10, 6))
        figExtHumMaxMin.patch.set_alpha(0.0)
        xExtHumMaxMin.patch.set_alpha(0.0)
        XlimInf = min(x); XlimSup = max(x);
        YlimInf = min(y1); YlimSup = max(y1);
        plt.xlim(XlimInf, XlimSup);   plt.ylim(YlimInf-0.5, YlimSup+0.5)
        xExtHumMaxMin.plot(x, y1, color = '#2900A1', alpha=0.4)
        xExtHumMaxMin.plot(x, y2, color = '#1D0075', alpha=0.4)
        xExtHumMaxMin.plot(x, y3, color = '#120047', alpha=0.4)
        VectorNum = []; VectorLetter = []
        for i in range(11):
            factor = (i)*0.1
            VectorNum.append(((XlimSup - XlimInf)*factor)+XlimInf)
            VectorLetter.append(f'{((XlimSup - XlimInf)*factor)+XlimInf:.0f}')
        xExtHumMaxMin.set_xticks(VectorNum)
        xExtHumMaxMin.set_xticklabels(VectorLetter, color='#DBDBDB', fontsize=14, fontname=fuente)
        xExtHumMaxMin.set_yticks([YlimInf, YlimSup])
        xExtHumMaxMin.set_yticklabels([f'{YlimInf:.0f}°C', f'{YlimSup:.0f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        #Guardar imagen de MatplotLib
        bufExtHumMaxMin = io.BytesIO() 
        plt.savefig(bufExtHumMaxMin, format="png", bbox_inches='tight', transparent=True)
        plt.close(figExtHumMaxMin)

        #Codificacion
        src_ext_hum_max_min = f"data:image/png;base64,{base64.b64encode(bufExtHumMaxMin.getvalue()).decode('utf-8')}"
        BloqueExtHumMaxMin = html.Div([
            html.Label(id='input-ext-hum-max-min',style=label_style,children=['Maximos y minimos de la Humeadad (%)']),
            html.Img(src=src_ext_hum_max_min, style={'width': '100%', 'height': '300px'})
            ],
            style={'width': '100%','textAlign': 'center'}
        )

        ######################################################
        ###                                                ###
        ###     Grafica de medias del Rocio y Humedad      ###
        ###                                                ###
        ######################################################

        #Grafica Punto de Rocio y Bulbo Húmedo
        IndiceBarrasDobleAxial = [f"Temp: {VectorExtDewWetM[0]:.4f}",f"Hum: {VectorExtDewWetM[1]:.4f}"]
        figExtDewWetM, x1ExtDewWetM = plt.subplots(figsize=(10, 6))
        figExtDewWetM.patch.set_alpha(0.0); x1ExtDewWetM.patch.set_alpha(0.0);
        barrasx1 = x1ExtDewWetM.bar(IndiceBarrasDobleAxial[0], VectorExtDewWetM[0],edgecolor = "#009EA3",linewidth=4.0, color="#08F7FF", alpha=0.9)
        x1ExtDewWetM.bar_label(barrasx1, color='#08F7FF', fontsize=12, fontweight='bold')
        x1ExtDewWetM.set_ylabel('Punto de Rocio °C', color='#DBDBDB', fontname=fuente, fontsize=16, fontweight='bold')
        x1ExtDewWetM.set_yticks([15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0])
        x1ExtDewWetM.set_yticklabels(["15.0°C", "17.5°C", "20.0°C", "22.5°C", "25.0°C", "27.5°C", "30.0°C"], color='#DBDBDB', fontsize=14, fontname=fuente)
        x2ExtDewWetM = x1ExtDewWetM.twinx()
        barrasx2 = x2ExtDewWetM.bar(IndiceBarrasDobleAxial[1], VectorExtDewWetM[1],edgecolor = "#0B3B6B",linewidth=4.0,color ="#1266B8", alpha=0.9)
        x2ExtDewWetM.bar_label(barrasx2, color='#08F7FF', fontsize=12, fontweight='bold')
        x2ExtDewWetM.set_ylabel('Bulbo Húmedo °C', color='#DBDBDB', fontname=fuente, fontsize=16, fontweight='bold')
        x2ExtDewWetM.set_yticks([15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0]) 
        x2ExtDewWetM.set_yticklabels(["15.0°C", "17.5°C", "20.0°C", "22.5°C", "25.0°C", "27.5°C", "30.0°C"], color='#DBDBDB', fontsize=14, fontname=fuente)
        x1ExtDewWetM.set_xlabel("Punto de Rocio - - - Bulbo Húmedo", color='#FFFFFF', fontname=fuente, fontsize=16, fontweight='bold')
        #Codificar
        bufExtDewWetM = io.BytesIO()
        plt.savefig(bufExtDewWetM, format="png", bbox_inches="tight", transparent=True)
        plt.close(figExtDewWetM)
        #Crear Objeto Doble Axial
        src_ext_dew_wet_m = f"data:image/png;base64,{base64.b64encode(bufExtDewWetM.getvalue()).decode('utf-8')}"
        BloqueExtDewWetM = html.Div([
            html.Label(id='input-titulo-dew-wet-ext',style=label_style,children=['Punto de Rocio y Bulbo Humedo']),
            html.Img(src=src_ext_dew_wet_m, style={'width': '100%', 'height': '350px'})
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        ####################################################################
        ###                                                              ###
        ###     Grafica de los Maximos y Minimos del Punto de Rocio      ###
        ###                                                              ###
        ####################################################################

        y1 = VectorExtDewWet[0];    y2 = VectorExtDewWet[1];    y3 = VectorExtDewWet[2]
        x = list(range(len(VectorExtDewWet[0])))
        figExtDewMaxMin, xExtDewMaxMin = plt.subplots(figsize=(10, 6))
        figExtDewMaxMin.patch.set_alpha(0.0);   xExtDewMaxMin.patch.set_alpha(0.0)
        XlimInf = min(x); XlimSup = max(x);     YlimInf = min(y1); YlimSup = max(y1);
        plt.xlim(XlimInf, XlimSup);   plt.ylim(YlimInf-0.5, YlimSup+0.5)
        xExtDewMaxMin.plot(x, y1, color = '#6F34F9', alpha=0.4)
        xExtDewMaxMin.plot(x, y2, color = '#4707DE', alpha=0.4)
        xExtDewMaxMin.plot(x, y3, color = '#33059E', alpha=0.4)
        VectorNum = []; VectorLetter = []
        for i in range(11):
            factor = (i)*0.1
            VectorNum.append(((XlimSup - XlimInf)*factor)+XlimInf)
            VectorLetter.append(f'{((XlimSup - XlimInf)*factor)+XlimInf:.0f}')
        xExtDewMaxMin.set_xticks(VectorNum)
        xExtDewMaxMin.set_xticklabels(VectorLetter, color='#DBDBDB', fontsize=14, fontname=fuente)
        xExtDewMaxMin.set_yticks([YlimInf, YlimSup])
        xExtDewMaxMin.set_yticklabels([f'{YlimInf:.0f}°C', f'{YlimSup:.0f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        bufExtHumMaxMin = io.BytesIO() 
        plt.savefig(bufExtHumMaxMin, format="png", bbox_inches='tight', transparent=True)
        plt.close(figExtHumMaxMin)
        #Codificar
        bufExtDewMaxMin = io.BytesIO()
        plt.savefig(bufExtDewMaxMin, format="png", bbox_inches='tight', transparent=True)
        plt.close(figExtDewMaxMin)
        src_ext_dew_max_min_ext = f"data:image/png;base64,{base64.b64encode(bufExtDewMaxMin.getvalue()).decode('utf-8')}"
        BloqueExtDewMaxMin = html.Div(
            [
                html.Label(id='input-titulo-dew-max-min-ext',style=label_style,children=['Maximos y minimos del Punto de Rocio °C']),
                html.Img(src=src_ext_dew_max_min_ext, style={'width': '100%', 'height': '350px'})
            ],
            style={'width': '100%','textAlign': 'center'}
        )

        #################################################################
        ###                                                           ###
        ###     Grafica de los Maximos y Minimos del Bulbo Húmedo     ###
        ###                                                           ###
        #################################################################

        y1 = VectorExtDewWet[3];    y2 = VectorExtDewWet[4];    y3 = VectorExtDewWet[5];
        x = list(range(len(VectorExtDewWet[0])))
        figExtWetMaxMin, xExtWetMaxMin = plt.subplots(figsize=(10, 6))
        figExtWetMaxMin.patch.set_alpha(0.0);   xExtWetMaxMin.patch.set_alpha(0.0)
        XlimInf = min(x); XlimSup = max(x);     YlimInf = min(y1); YlimSup = max(y1);
        plt.xlim(XlimInf, XlimSup);   plt.ylim(YlimInf-0.5, YlimSup+0.5)
        xExtWetMaxMin.plot(x, y1, color = '#D007DE', alpha=0.4)
        xExtWetMaxMin.plot(x, y2, color = '#94059E', alpha=0.4)
        xExtWetMaxMin.plot(x, y3, color = '#6A0472', alpha=0.4)
        VectorNum = []; VectorLetter = []
        for i in range(11):
            factor = (i)*0.1
            VectorNum.append(((XlimSup - XlimInf)*factor)+XlimInf)
            VectorLetter.append(f'{((XlimSup - XlimInf)*factor)+XlimInf:.0f}')
        xExtWetMaxMin.set_xticks(VectorNum)
        xExtWetMaxMin.set_xticklabels(VectorLetter, color='#DBDBDB', fontsize=14, fontname=fuente)
        xExtWetMaxMin.set_yticks([YlimInf, YlimSup])
        xExtWetMaxMin.set_yticklabels([f'{YlimInf:.0f}°C', f'{YlimSup:.0f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        bufExtWetMaxMin = io.BytesIO() 
        plt.savefig(bufExtWetMaxMin, format="png", bbox_inches='tight', transparent=True)
        plt.close(figExtWetMaxMin)
        #Codificacion
        src_ext_wet_max_min = f"data:image/png;base64,{base64.b64encode(bufExtWetMaxMin.getvalue()).decode('utf-8')}"
        BloqueExtWetMaxMin = html.Div([
            html.Label(id='input-ext-wet-max-min',style=label_style,children=['Maximos y minimos del bulbo húmedo']),
            html.Img(src=src_ext_wet_max_min, style={'width': '100%', 'height': '350px'})
            ],
            style={'width': '100%','textAlign': 'center'}
        )

        ###########################
        ###                     ###
        ###     Histogramas     ###
        ###                     ###
        ###########################

        #Histograma de temperatura exterior
        figHistExtTemp, x1HistExtTemp = plt.subplots(figsize=(10, 6))
        y1 = VectorExtTempHum[0];      Stats.timsort(y1);  DatoModa1 = Stats.ModaVectorValor(y1); MedianaExtTemp = Stats.MedianaVector(y1);
        VarianzaInsesgadaExtTemp = Stats.DesviacionMediaVector(y1, VectorExtTempHumM[0]);
        DesviacionExtTemp = Stats.DesviacionNewton(VarianzaInsesgadaExtTemp);
        Varianza1 = Stats.VarianzaVector(y1);
        DesviacionExtTempNM = Stats.DesviacionNewton(Varianza1);
        PercExtTemp = Stats.Percentil(y1, Percentiles);
        figHistExtTemp.patch.set_alpha(0.0);  x1HistExtTemp.patch.set_alpha(0.0);
        XlimInf2 = y1[0];    XlimSup2 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(y1[len(y1) - 1]))
        x1HistExtTemp.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = '#91122B',color ="#E84163",linewidth=4.0, alpha=0.6)
        x1HistExtTemp.set_xticks([XlimInf2,PercExtTemp[0],PercExtTemp[1],PercExtTemp[2],XlimSup2])
        x1HistExtTemp.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtTemp[0]:.0f}°C',f'{PercExtTemp[1]:.0f}°C',f'{PercExtTemp[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        x1HistExtTemp.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercExtTemp,ColorPerc):
            x1HistExtTemp.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistExtTemp = io.BytesIO()
        plt.savefig(bufHistExtTemp, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistExtTemp)
        src_hist_ext_temp = f"data:image/png;base64,{base64.b64encode(bufHistExtTemp.getvalue()).decode('utf-8')}"
        BloqueHistExteriorTemp = html.Div([
            html.Img(src=src_hist_ext_temp, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ext-temp',style=label_style,children=['Temperatura °C']),
            html.P([
                html.Strong('Media Aritmética'),html.Br(),
                f'{VectorExtTempHumM[0]:.0f}',html.Br(),
                html.Strong('Mediana'),html.Br(),
                f'{MedianaExtTemp:.4f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'{VarianzaInsesgadaExtTemp:.8f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'{DesviacionExtTemp:.8f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'{Varianza1:.8f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'{DesviacionExtTempNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Minimo: {y1[0]:.0f}',f'\tMaximo: {y1[len(y1) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'{DatoModa1:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'P{Percentiles[0]}: {PercExtTemp[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtTemp[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtTemp[2]:.0f}°C'
            ])
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histograma de humedad exterior
        figHistExtHum, x2HistExtHum = plt.subplots(figsize=(10, 6))
        y2 = VectorExtTempHum[3];      Stats.timsort(y2);  DatoModa2 = Stats.ModaVectorValor(y2); MedianaExtHum = Stats.MedianaVector(y2);
        VarianzaInsesgadaExtHum = Stats.DesviacionMediaVector(y1, VectorExtTempHumM[1]);
        DesviacionExtHum = Stats.DesviacionNewton(VarianzaInsesgadaExtHum);
        Varianza2 = Stats.VarianzaVector(y2);
        DesviacionExtHumNM = Stats.DesviacionNewton(Varianza2);
        PercExtHum = Stats.Percentil(y2, Percentiles);
        figHistExtHum.patch.set_alpha(0.0);  x2HistExtHum.patch.set_alpha(0.0);
        XlimInf2 = y2[0];    XlimSup2 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(y2[len(y2) - 1]))
        x2HistExtHum.hist(y2, bins=Rango2,rwidth = 1.2, edgecolor = '#060047',color ="#1B08FF",linewidth=4.0, alpha=0.6)
        x2HistExtHum.set_xticks([XlimInf2,PercExtHum[0],PercExtHum[1],PercExtHum[2],XlimSup2])
        x2HistExtHum.set_xticklabels([f'{XlimInf2:.2f}%',f'{PercExtHum[0]:.0f}%',f'{PercExtHum[1]:.0f}%',f'{PercExtHum[2]:.0f}%',f'{XlimSup2:.2f}%'], color='#DBDBDB', fontsize=14, fontname=fuente)
        x2HistExtHum.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercExtHum,ColorPerc):
            x2HistExtHum.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistExtTemp = io.BytesIO()
        plt.savefig(bufHistExtTemp, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistExtHum)
        src_hist_ext_hum = f"data:image/png;base64,{base64.b64encode(bufHistExtTemp.getvalue()).decode('utf-8')}"
        BloqueHistExteriorHum = html.Div([
            html.Img(src=src_hist_ext_hum, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ext-hum',style=label_style,children=['Humedad (%)']),
            html.P([
                html.Strong('Media Aritmética'),html.Br(),
                f'{VectorExtTempHumM[1]:.0f}',html.Br(),
                html.Strong('Mediana'),html.Br(),
                f'{MedianaExtHum:.4f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'{VarianzaInsesgadaExtHum:.8f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'{DesviacionExtHum:.8f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'{Varianza2:.8f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'{DesviacionExtHumNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Minimo: {y2[0]:.0f}',f'\tMaximo: {y2[len(y2) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'{DatoModa2:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'P{Percentiles[0]}: {PercExtHum[0]:.0f}%',f'\tP{Percentiles[1]}: {PercExtHum[1]:.0f}%',f'\tP{Percentiles[2]}: {PercExtHum[2]:.0f}%'
            ])
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histrograma Temperaturas exteriores
        y2 = VectorExtTempHum[1];  y3 = VectorExtTempHum[2]
        Stats.timsort(y2);                      Stats.timsort(y3);
        Media2 = Stats.MediaVector(y2);         Media3 = Stats.MediaVector(y3);
        Mediana2 = Stats.MedianaVector(y2);     Mediana3 = Stats.MedianaVector(y3);
        VarianzaInsesgadaExtTempMax = Stats.DesviacionMediaVector(y2, Media2);
        DesviacionExtTempMax = Stats.DesviacionNewton(VarianzaInsesgadaExtTempMax);
        VarianzaInsesgadaExtTempMin = Stats.DesviacionMediaVector(y3, Media3);
        DesviacionExtTempMin = Stats.DesviacionNewton(VarianzaInsesgadaExtTempMin);
        DatoModa2 = Stats.ModaVectorValor(y2);  DatoModa3 = Stats.ModaVectorValor(y3);
        Varianza2 = Stats.VarianzaVector(y2);   Varianza3 = Stats.VarianzaVector(y3);
        DesviacionExtTempMaxNM = Stats.DesviacionNewton(Varianza2);
        DesviacionExtTempMinNM = Stats.DesviacionNewton(Varianza3);
        PercExtTempMax = Stats.Percentil(y2, Percentiles);
        PercExtTempMin = Stats.Percentil(y3, Percentiles);
        figHistExtTempMaxMin, xHistExtTempMaxMin = plt.subplots(figsize=(10, 6));
        figHistExtTempMaxMin.patch.set_alpha(0.0);  xHistExtTempMaxMin.patch.set_alpha(0.0);
        XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(y2[len(y2) - 1]))
        xHistExtTempMaxMin.hist(y2, bins=Rango,rwidth = 1.2, color = '#9D061F',linewidth=4.0, edgecolor = 'black', alpha=0.3)
        xHistExtTempMaxMin.hist(y3, bins=Rango,rwidth = 1.2, color = '#45020E',linewidth=4.0, edgecolor = 'black', alpha=0.3)
        xHistExtTempMaxMin.set_xticks([XlimInf2,PercExtTempMax[0],PercExtTempMax[1],PercExtTempMax[2],PercExtTempMin[0],PercExtTempMin[1],PercExtTempMin[2],XlimSup2])
        xHistExtTempMaxMin.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtTempMax[0]:.0f}°C',f'{PercExtTempMax[1]:.0f}°C',f'{PercExtTempMax[2]:.0f}°C',f'{PercExtTempMin[0]:.0f}°C',f'{PercExtTempMin[1]:.0f}°C',f'{PercExtTempMin[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        xHistExtTempMaxMin.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercExtTempMax,ColorPerc):
            xHistExtTempMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        for p, val, col in zip(Percentiles,PercExtTempMin,ColorPerc):
            xHistExtTempMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistExtTempMaxMin = io.BytesIO()
        plt.savefig(bufHistExtTempMaxMin, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistExtTempMaxMin)
        src_hist_ext_temp_max_min = f"data:image/png;base64,{base64.b64encode(bufHistExtTempMaxMin.getvalue()).decode('utf-8')}"
        BloqueHistExteriorTempMaxMin = html.Div([
            html.Img(src=src_hist_ext_temp_max_min, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ext-temp-max-min',style=label_style,children=['Temperaturas °C']),
            html.P([
                html.Strong('Medias Aritméticas'),html.Br(),
                f'Para maximas: {Media2:.4f}',f'\tPara Minimos: {Media3:.4f}',html.Br(),
                html.Strong('Medianas'),html.Br(),
                f'Para maximas: {Mediana2:.0f}',f'\tPara Minimos: {Mediana3:.0f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'Para maximas: {VarianzaInsesgadaExtTempMax:.4f}',f'\tPara Minimos: {VarianzaInsesgadaExtTempMin:.4f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'Para maximas: {DesviacionExtTempMax:.4f}',f'\tPara Minimos: {DesviacionExtTempMin:.4f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'Para maximas: {Varianza2:.4f}',f'\tPara Minimos: {Varianza3:.4f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'Para maximas: {DesviacionExtTempMaxNM:.4f}',f'\tPara Minimos: {DesviacionExtTempMinNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Para maximas: {y2[0]:.0f}',f',{y2[len(y2) - 1]:.0f}',f'\tPara Minimos: {y3[0]:.0f}',f' {y3[len(y3) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'Para maximas: {DatoModa2:.0f}',f'\tPara Minimos: {DatoModa3:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'Maximas: P{Percentiles[0]}: {PercExtTempMax[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtTempMax[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtTempMax[2]:.0f}°C',html.Br(),
                f'Minimas: P{Percentiles[0]}: {PercExtTempMin[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtTempMin[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtTempMin[2]:.0f}°C'
            ])  
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histrograma Humedades
        y2 = VectorExtTempHum[4];  y3 = VectorExtTempHum[5]
        Stats.timsort(y2);                      Stats.timsort(y3);
        Media2 = Stats.MediaVector(y2);         Media3 = Stats.MediaVector(y3);
        Mediana2 = Stats.MedianaVector(y2);     Mediana3 = Stats.MedianaVector(y3);
        VarianzaInsesgadaExtHumMax = Stats.DesviacionMediaVector(y2, Media2);
        DesviacionExtHumMax = Stats.DesviacionNewton(VarianzaInsesgadaExtHumMax);
        VarianzaInsesgadaExtHumMin = Stats.DesviacionMediaVector(y3, Media3);
        DesviacionExtHumMin = Stats.DesviacionNewton(VarianzaInsesgadaExtHumMin);
        DatoModa2 = Stats.ModaVectorValor(y2);  DatoModa3 = Stats.ModaVectorValor(y3);
        Varianza2 = Stats.VarianzaVector(y2);   Varianza3 = Stats.VarianzaVector(y3);
        DesviacionExtHumMaxNM = Stats.DesviacionNewton(Varianza2);
        DesviacionExtHumMinNM = Stats.DesviacionNewton(Varianza3);
        PercExtHumMax = Stats.Percentil(y2, Percentiles);
        PercExtHumMin = Stats.Percentil(y3, Percentiles);
        figHistExtHumMaxMin, xHistExtHumMaxMin = plt.subplots(figsize=(10, 6));
        figHistExtHumMaxMin.patch.set_alpha(0.0);  xHistExtHumMaxMin.patch.set_alpha(0.0);
        XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(y2[len(y2) - 1]));
        xHistExtHumMaxMin.hist(y2, bins=Rango,rwidth = 1.2, color = '#2900A1',linewidth=4.0, edgecolor = 'black', alpha=0.3)
        xHistExtHumMaxMin.hist(y3, bins=Rango,rwidth = 1.2, color = '#120047',linewidth=4.0, edgecolor = 'black', alpha=0.3)
        xHistExtHumMaxMin.set_xticks([XlimInf2,PercExtHumMax[0],PercExtHumMax[1],PercExtHumMax[2],PercExtHumMin[0],PercExtHumMin[1],PercExtHumMin[2],XlimSup2])
        xHistExtHumMaxMin.set_xticklabels([f'{XlimInf2:.2f} %',f'{PercExtHumMax[0]:.0f}°C',f'{PercExtHumMax[1]:.0f}°C',f'{PercExtHumMax[2]:.0f}°C',f'{PercExtHumMin[0]:.0f}°C',f'{PercExtHumMin[1]:.0f}°C',f'{PercExtHumMin[2]:.0f}°C',f'{XlimSup2:.2f} %'], color='#DBDBDB', fontsize=14, fontname=fuente)
        xHistExtHumMaxMin.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercExtHumMax,ColorPerc):
            xHistExtHumMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        for p, val, col in zip(Percentiles,PercExtHumMin,ColorPerc):
            xHistExtHumMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistExtHumMaxMin = io.BytesIO()
        plt.savefig(bufHistExtHumMaxMin, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistExtHumMaxMin)
        src_hist_ext_hum_max_min = f"data:image/png;base64,{base64.b64encode(bufHistExtHumMaxMin.getvalue()).decode('utf-8')}"
        BloqueHistExteriorHumMaxMin = html.Div([
            html.Img(src=src_hist_ext_hum_max_min, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ext-hum-max-min',style=label_style,children=['Humedades (%)']),
            html.P([
                html.Strong('Medias Aritméticas'),html.Br(),
                f'Para maximas: {Media2:.4f}',f'\tPara Minimos: {Media3:.4f}',html.Br(),
                html.Strong('Medianas'),html.Br(),
                f'Para maximas: {Mediana2:.0f}',f'\tPara Minimos: {Mediana3:.0f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'Para maximas: {VarianzaInsesgadaExtHumMax:.4f}',f'\tPara Minimos: {VarianzaInsesgadaExtHumMin:.4f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'Para maximas: {DesviacionExtHumMax:.4f}',f'\tPara Minimos: {DesviacionExtHumMin:.4f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'Para maximas: {Varianza2:.4f}',f'\tPara Minimos: {Varianza3:.4f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'Para maximas: {DesviacionExtHumMaxNM:.4f}',f'\tPara Minimos: {DesviacionExtHumMinNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Para maximas: {y2[0]:.0f}',f',{y2[len(y2) - 1]:.0f}',f'\tPara Minimos: {y3[0]:.0f}',f' {y3[len(y3) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'Para maximas: {DatoModa2:.0f}',f'\tPara Minimos: {DatoModa3:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'Maximas: P{Percentiles[0]}: {PercExtHumMax[0]:.0f}%',f'\tP{Percentiles[1]}: {PercExtHumMax[1]:.0f}%',f'\tP{Percentiles[2]}: {PercExtHumMax[2]:.0f}%',html.Br(),
                f'Minimas: P{Percentiles[0]}: {PercExtHumMin[0]:.0f}%',f'\tP{Percentiles[1]}: {PercExtHumMin[1]:.0f}%',f'\tP{Percentiles[2]}: {PercExtHumMin[2]:.0f}%'
            ])
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histograma de punto de rocio
        figHistExtD, x1HistExtD = plt.subplots(figsize=(10, 6))
        y1 = VectorExtDewWet[0];      Stats.timsort(y1);  DatoModa1 = Stats.ModaVectorValor(y1); MedianaExtD = Stats.MedianaVector(y1);
        VarianzaInsesgadaExtD = Stats.DesviacionMediaVector(y1, VectorExtDewWetM[0]);
        DesviacionExtD = Stats.DesviacionNewton(VarianzaInsesgadaExtD);
        Varianza1 = Stats.VarianzaVector(y1);
        DesviacionExtDNM = Stats.DesviacionNewton(Varianza1);
        PercExtD = Stats.Percentil(y1, Percentiles);
        figHistExtD.patch.set_alpha(0.0);  x1HistExtD.patch.set_alpha(0.0);
        XlimInf2 = y1[0];    XlimSup2 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(y1[len(y1) - 1]))
        x1HistExtD.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = '#0A7563',color ="#00DBB7",linewidth=4.0, alpha=0.6)
        x1HistExtD.set_xticks([XlimInf2,PercExtD[0],PercExtD[1],PercExtD[2],XlimSup2])
        x1HistExtD.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtD[0]:.0f}°C',f'{PercExtD[1]:.0f}°C',f'{PercExtD[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        x1HistExtD.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercExtD,ColorPerc):
            x1HistExtD.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistExtD = io.BytesIO()
        plt.savefig(bufHistExtD, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistExtD)
        src_hist_ext_d = f"data:image/png;base64,{base64.b64encode(bufHistExtD.getvalue()).decode('utf-8')}"
        BloqueHistExteriorDew = html.Div([
            html.Img(src=src_hist_ext_d, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ext-d',style=label_style,children=['Punto de Rocio °C']),
            html.P([
                html.Strong('Media Aritmética'),html.Br(),
                f'{VectorExtDewWetM[0]:.0f}',html.Br(),
                html.Strong('Mediana'),html.Br(),
                f'{MedianaExtD:.4f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'{VarianzaInsesgadaExtD:.8f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'{DesviacionExtD:.8f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'{Varianza1:.8f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'{DesviacionExtDNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Minimo: {y1[0]:.0f}',f'\tMaximo: {y1[len(y1) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'{DatoModa1:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'P{Percentiles[0]}: {PercExtD[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtD[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtD[2]:.0f}°C'
            ])
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histograma de bulbo húmedo
        figHistExtW, x1HistExtW = plt.subplots(figsize=(10, 6))
        y2 = VectorExtDewWet[3];      Stats.timsort(y2);  DatoModa2 = Stats.ModaVectorValor(y2); MedianaExtW = Stats.MedianaVector(y2);
        VarianzaInsesgadaExtW = Stats.DesviacionMediaVector(y2, VectorExtDewWetM[1]);
        DesviacionExtW = Stats.DesviacionNewton(VarianzaInsesgadaExtW);
        Varianza2 = Stats.VarianzaVector(y2);
        DesviacionExtWNM = Stats.DesviacionNewton(Varianza2);
        PercExtW = Stats.Percentil(y2, Percentiles);
        figHistExtW.patch.set_alpha(0.0);  x1HistExtW.patch.set_alpha(0.0);
        XlimInf2 = y2[0];    XlimSup2 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(y2[len(y2) - 1]))
        x1HistExtW.hist(y2, bins=Rango2,rwidth = 1.2, edgecolor = '#0C4574',color ="#008CFF",linewidth=4.0, alpha=0.6)
        x1HistExtW.set_xticks([XlimInf2,PercExtW[0],PercExtW[1],PercExtW[2],XlimSup2])
        x1HistExtW.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtW[0]:.0f}°C',f'{PercExtW[1]:.0f}°C',f'{PercExtW[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        x1HistExtW.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercExtW,ColorPerc):
            x1HistExtW.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistExtW = io.BytesIO()
        plt.savefig(bufHistExtW, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistExtW)
        src_hist_ext_w = f"data:image/png;base64,{base64.b64encode(bufHistExtW.getvalue()).decode('utf-8')}"
        BloqueHistExteriorWet = html.Div([
            html.Img(src=src_hist_ext_w, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ext-w',style=label_style,children=['Bulbo Húmedo °C']),
            html.P([
                html.Strong('Media Aritmética'),html.Br(),
                f'{VectorExtDewWetM[1]:.0f}',html.Br(),
                html.Strong('Mediana'),html.Br(),
                f'{MedianaExtW:.4f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'{VarianzaInsesgadaExtW:.8f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'{DesviacionExtW:.8f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'{Varianza2:.8f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'{DesviacionExtWNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Minimo: {y2[0]:.0f}',f'\tMaximo: {y2[len(y2) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'{DatoModa2:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'P{Percentiles[0]}: {PercExtW[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtW[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtW[2]:.0f}°C'
            ])
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histrograma Punto de Rocio Maximos y Minimos exteriores
        y2 = VectorExtDewWet[1];  y3 = VectorExtDewWet[2]
        Stats.timsort(y2);                      Stats.timsort(y3);
        Media2 = Stats.MediaVector(y2);         Media3 = Stats.MediaVector(y3);
        Mediana2 = Stats.MedianaVector(y2);     Mediana3 = Stats.MedianaVector(y3);
        VarianzaInsesgadaExtDMax = Stats.DesviacionMediaVector(y2, Media2);
        DesviacionExtDMax = Stats.DesviacionNewton(VarianzaInsesgadaExtDMax);
        VarianzaInsesgadaExtDMin = Stats.DesviacionMediaVector(y3, Media3);
        DesviacionExtDMin = Stats.DesviacionNewton(VarianzaInsesgadaExtDMin);
        DatoModa2 = Stats.ModaVectorValor(y2);  DatoModa3 = Stats.ModaVectorValor(y3);
        Varianza2 = Stats.VarianzaVector(y2);   Varianza3 = Stats.VarianzaVector(y3);
        DesviacionExtDMaxNM = Stats.DesviacionNewton(Varianza2);
        DesviacionExtDMinNM = Stats.DesviacionNewton(Varianza3);
        PercExtDMax = Stats.Percentil(y2, Percentiles);
        PercExtDMin = Stats.Percentil(y3, Percentiles);
        figHistExtDMaxMin, xHistExtDMaxMin = plt.subplots(figsize=(10, 6));
        figHistExtDMaxMin.patch.set_alpha(0.0);  xHistExtDMaxMin.patch.set_alpha(0.0);
        XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(y2[len(y2) - 1]))
        xHistExtDMaxMin.hist(y2, bins=Rango,rwidth = 1.2, color = "#33059E",linewidth=4.0, edgecolor = 'black', alpha=0.3)
        xHistExtDMaxMin.hist(y3, bins=Rango,rwidth = 1.2, color = '#6F34F9',linewidth=4.0, edgecolor = 'black', alpha=0.3)
        xHistExtDMaxMin.set_xticks([XlimInf2,PercExtDMax[0],PercExtDMax[1],PercExtDMax[2],PercExtDMin[0],PercExtDMin[1],PercExtDMin[2],XlimSup2])
        xHistExtDMaxMin.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtDMax[0]:.0f}°C',f'{PercExtDMax[1]:.0f}°C',f'{PercExtDMax[2]:.0f}°C',f'{PercExtDMin[0]:.0f}°C',f'{PercExtDMin[1]:.0f}°C',f'{PercExtDMin[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        xHistExtDMaxMin.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercExtDMax,ColorPerc):
            xHistExtDMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        for p, val, col in zip(Percentiles,PercExtDMin,ColorPerc):
            xHistExtDMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistExtDMaxMin = io.BytesIO()
        plt.savefig(bufHistExtDMaxMin, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistExtDMaxMin)
        #Crear Objeto Histograma Humedad
        src_hist_ext_dew_max_min = f"data:image/png;base64,{base64.b64encode(bufHistExtDMaxMin.getvalue()).decode('utf-8')}"
        BloqueHistExteriorDewMaxMin = html.Div([
            html.Img(src=src_hist_ext_dew_max_min, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ext-dew-max-min',style=label_style,children=['Maximos y Minimos Rocio °C']),
            html.P([
                html.Strong('Medias Aritméticas'),html.Br(),
                f'Para maximas: {Media2:.4f}',f'\tPara Minimos: {Media3:.4f}',html.Br(),
                html.Strong('Medianas'),html.Br(),
                f'Para maximas: {Mediana2:.0f}',f'\tPara Minimos: {Mediana3:.0f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'Para maximas: {VarianzaInsesgadaExtDMax:.4f}',f'\tPara Minimos: {VarianzaInsesgadaExtDMin:.4f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'Para maximas: {DesviacionExtDMax:.4f}',f'\tPara Minimos: {DesviacionExtDMin:.4f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'Para maximas: {Varianza2:.4f}',f'\tPara Minimos: {Varianza3:.4f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'Para maximas: {DesviacionExtDMaxNM:.4f}',f'\tPara Minimos: {DesviacionExtDMinNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Para maximas: {y2[0]:.0f}',f',{y2[len(y2) - 1]:.0f}',f'\tPara Minimos: {y3[0]:.0f}',f' {y3[len(y3) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'Para maximas: {DatoModa2:.0f}',f'\tPara Minimos: {DatoModa3:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'Maximas: P{Percentiles[0]}: {PercExtDMax[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtDMax[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtDMax[2]:.0f}°C',html.Br(),
                f'Minimas: P{Percentiles[0]}: {PercExtDMin[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtDMin[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtDMin[2]:.0f}°C'
            ])  
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histrograma Bulbo Humedo Maximos y Minimos exteriores
        y2 = VectorExtDewWet[4];  y3 = VectorExtDewWet[5]
        Stats.timsort(y2);                      Stats.timsort(y3);
        Media2 = Stats.MediaVector(y2);         Media3 = Stats.MediaVector(y3);
        Mediana2 = Stats.MedianaVector(y2);     Mediana3 = Stats.MedianaVector(y3);
        VarianzaInsesgadaExtWMax = Stats.DesviacionMediaVector(y2, Media2);
        DesviacionExtWMax = Stats.DesviacionNewton(VarianzaInsesgadaExtWMax);
        VarianzaInsesgadaExtWMin = Stats.DesviacionMediaVector(y3, Media3);
        DesviacionExtWMin = Stats.DesviacionNewton(VarianzaInsesgadaExtWMin);
        DatoModa2 = Stats.ModaVectorValor(y2);  DatoModa3 = Stats.ModaVectorValor(y3);
        Varianza2 = Stats.VarianzaVector(y2);   Varianza3 = Stats.VarianzaVector(y3);
        DesviacionExtWMaxNM = Stats.DesviacionNewton(Varianza2);
        DesviacionExtWMinNM = Stats.DesviacionNewton(Varianza3);
        PercExtWMax = Stats.Percentil(y2, Percentiles);
        PercExtWMin = Stats.Percentil(y3, Percentiles);
        figHistExtWMaxMin, xHistExtWMaxMin = plt.subplots(figsize=(10, 6));
        figHistExtWMaxMin.patch.set_alpha(0.0);  xHistExtWMaxMin.patch.set_alpha(0.0);
        XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(y2[len(y2) - 1]))
        xHistExtWMaxMin.hist(y2, bins=Rango,rwidth = 1.2, color = '#6A0472',linewidth=4.0, edgecolor = 'black', alpha=0.3)
        xHistExtWMaxMin.hist(y3, bins=Rango,rwidth = 1.2, color = '#D007DE',linewidth=4.0, edgecolor = 'black', alpha=0.3)
        xHistExtWMaxMin.set_xticks([XlimInf2,PercExtWMax[0],PercExtWMax[1],PercExtWMax[2],PercExtWMin[0],PercExtWMin[1],PercExtWMin[2],XlimSup2])
        xHistExtWMaxMin.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtWMax[0]:.0f}°C',f'{PercExtWMax[1]:.0f}°C',f'{PercExtWMax[2]:.0f}°C',f'{PercExtWMin[0]:.0f}°C',f'{PercExtWMin[1]:.0f}°C',f'{PercExtWMin[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        xHistExtWMaxMin.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercExtWMax,ColorPerc):
            xHistExtWMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        for p, val, col in zip(Percentiles,PercExtWMin,ColorPerc):
            xHistExtWMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistExtWMaxMin = io.BytesIO()
        plt.savefig(bufHistExtWMaxMin, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHistExtWMaxMin)
        #Crear Objeto Histograma Humedad
        src_hist_ext_wet_max_min = f"data:image/png;base64,{base64.b64encode(bufHistExtWMaxMin.getvalue()).decode('utf-8')}"
        BloqueHistExteriorWetMaxMin = html.Div([
            html.Img(src=src_hist_ext_wet_max_min, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_ext-wet-max-min',style=label_style,children=['Maximos y Minimos Bulbo °C']),
            html.P([
                html.Strong('Medias Aritméticas'),html.Br(),
                f'Para maximas: {Media2:.4f}',f'\tPara Minimos: {Media3:.4f}',html.Br(),
                html.Strong('Medianas'),html.Br(),
                f'Para maximas: {Mediana2:.0f}',f'\tPara Minimos: {Mediana3:.0f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'Para maximas: {VarianzaInsesgadaExtWMax:.4f}',f'\tPara Minimos: {VarianzaInsesgadaExtWMin:.4f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'Para maximas: {DesviacionExtWMax:.4f}',f'\tPara Minimos: {DesviacionExtWMin:.4f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'Para maximas: {Varianza2:.4f}',f'\tPara Minimos: {Varianza3:.4f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'Para maximas: {DesviacionExtWMaxNM:.4f}',f'\tPara Minimos: {DesviacionExtWMinNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Para maximas: {y2[0]:.0f}',f',{y2[len(y2) - 1]:.0f}',f'\tPara Minimos: {y3[0]:.0f}',f' {y3[len(y3) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'Para maximas: {DatoModa2:.0f}',f'\tPara Minimos: {DatoModa3:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'Maximas: P{Percentiles[0]}: {PercExtWMax[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtWMax[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtWMax[2]:.0f}°C',html.Br(),
                f'Minimas: P{Percentiles[0]}: {PercExtWMin[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtWMin[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtWMin[2]:.0f}°C'
            ])  
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        return BloqueExtTempHum,BloqueExtTempMaxMin,BloqueExtHumMaxMin, BloqueHistExteriorTemp,BloqueHistExteriorHum,BloqueHistExteriorTempMaxMin,BloqueHistExteriorHumMaxMin, BloqueExtDewWetM,BloqueExtDewMaxMin,BloqueExtWetMaxMin, BloqueHistExteriorDew,BloqueHistExteriorWet,BloqueHistExteriorDewMaxMin,BloqueHistExteriorWetMaxMin
    
    if(opcion == "Presiones"):

        print("Registro Presiones")
        #Vectores Presion
        VectorPbar = [];  VectorPbarabs = []; VectorPbarMaxMin = [];
        #Inicio y Final del indice
        i = IndiceBar; Ante = Pabs;
        while(i <= Ante):
            #Datos de la fila del Mes seleccionado
            DatosFilas = df.iloc[Pos1:Pos2, i].tolist()
            #Datos de la columna del rango de filas
            Datos = [x.item() if hasattr(x, 'item') else x for x in DatosFilas]
            #Verificar integridad de los datos
            Indice = list(range(0, len(Datos)))
            Curva.InterpolacionLinealNoGraph(Datos, Indice, len(Datos))
            #Convertir en Datos
            Datos = [float(i) for i in Datos]
            if(i == IndiceBar or i == IndiceBarMax or i == IndiceBarMin):
                #Vector Pbar
                VectorPbar.append(Stats.MediaVector(Datos))
                if(i == IndiceBar):
                    VectorPbarabs.append(Datos)
                else:
                    VectorPbarMaxMin.append(Datos)
                i = i + 1;
            elif(i == Pabs):
                MediaPabs = Stats.MediaVector(Datos)
                VectorPbarabs.append(Datos)
                i = i + 1;
        
        ###################################################
        ###                                             ###
        ###     Grafica de Pbar vs PbarMax-PbarMin      ###
        ###                                             ###
        ###################################################

        IndiceBarrasPbar = [f"Presion Bar: {VectorPbar[0]:.4f}",f"Presion Bar Maxima: {VectorPbar[1]:.4f}",f"Presion Bar Minima: {VectorPbar[2]:.4f}"]
        figPbar, axPbar = plt.subplots(figsize=(10, 6))
        figPbar.patch.set_alpha(0.0)
        axPbar.patch.set_alpha(0.0)
        barrasx1 = axPbar.bar(IndiceBarrasPbar[2], VectorPbar[2],edgecolor = "#6F6269",linewidth=4.0, color="#ADA3A8", alpha=0.9)
        barrasx2 = axPbar.bar(IndiceBarrasPbar[0], VectorPbar[0],edgecolor = "#6F6269",linewidth=4.0, color="#ADA3A8", alpha=0.9)
        barrasx3 = axPbar.bar(IndiceBarrasPbar[1], VectorPbar[1],edgecolor = "#6F6269",linewidth=4.0, color="#A3ADAD", alpha=0.9)
        axPbar.bar_label(barrasx1, color='#ADA3A8', fontsize=12, fontweight='bold')
        axPbar.bar_label(barrasx2, color='#ADA3A8', fontsize=12, fontweight='bold')
        axPbar.bar_label(barrasx3, color='#A3ADAD', fontsize=12, fontweight='bold')
        plt.ylim(950, 1050)
        #Codificar
        bufPbar = io.BytesIO()
        plt.savefig(bufPbar, format="png", bbox_inches="tight", transparent=True)
        plt.close(figPbar)
        #Crear Objeto Doble Axial
        src_barras_p_bar = f"data:image/png;base64,{base64.b64encode(bufPbar.getvalue()).decode('utf-8')}"

        BloquePbar = html.Div([
            html.Label(id='input-titulo-pbar-max-min',style=label_style,children=['Minimos y Maximos de la Presion Barometrica mb']),
            html.Img(src=src_barras_p_bar, style={"width": "100%"})
            ],
            style={"width": "100%",'textAlign': 'center'}
        )

        #############################################
        ###                                       ###
        ###         Grafica Pbar vs Pabs          ###
        ###                                       ###
        #############################################

        y1 = VectorPbarabs[0];  y2 = VectorPbarabs[1]
        x = list(range(len(VectorPbarabs[0])))
        figPbarabs, axPbarabs = plt.subplots(figsize=(10, 6))
        figPbarabs.patch.set_alpha(0.0)
        axPbarabs.patch.set_alpha(0.0)
        XlimInf = min(x); XlimSup = max(x);
        YlimInf = min(y2); YlimSup = max(y1);
        plt.xlim(XlimInf, XlimSup);   plt.ylim(YlimInf-0.5, YlimSup+0.5)
        axPbarabs.plot(x, y1, color = '#EC067B', alpha = 0.4, linewidth=4.0)
        axPbarabs.plot(x, y2, color = '#06EC75', alpha = 0.4, linewidth=4.0)
        VectorNum = []; VectorLetter = []
        for i in range(11):
            factor = (i)*0.1
            VectorNum.append(((XlimSup - XlimInf)*factor)+XlimInf)
            VectorLetter.append(f'{((XlimSup - XlimInf)*factor)+XlimInf:.0f}')
        axPbarabs.set_xticks(VectorNum)
        axPbarabs.set_xticklabels(VectorLetter, color='#DBDBDB', fontsize=14, fontname=fuente)
        axPbarabs.set_yticks([YlimInf, YlimSup])
        axPbarabs.set_yticklabels([f'{YlimInf:.0f}°C', f'{YlimSup:.0f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
        #Guardar imagen de MatplotLib
        bufPbarabs = io.BytesIO() 
        plt.savefig(bufPbarabs, format="png", bbox_inches='tight', transparent=True)
        plt.close(figPbarabs)

        #Codificacion
        src_p_bar_abs = f"data:image/png;base64,{base64.b64encode(bufPbarabs.getvalue()).decode('utf-8')}"
        BloquePbarabs = html.Div([
            html.Label(id='input-titulo-pbar-pabs',style=label_style,children=['Presion barometrica mb vs Presion Absoluta mb']),
            html.Img(src=src_p_bar_abs, style={"width": "100%"})
            ],
            style={"width": "100%"}
        )
        #Histograma de presion barometrica
        figHisPbar, xHistPbar = plt.subplots(figsize=(10, 6))
        y1 = VectorPbarabs[0];      Stats.timsort(y1);  DatoModa1 = Stats.ModaVectorValor(y1); MedianaPbar = Stats.MedianaVector(y1);
        VarianzaInsesgadaPbar = Stats.DesviacionMediaVector(y1, VectorPbar[0]);
        DesviacionPbar = Stats.DesviacionNewton(VarianzaInsesgadaPbar);
        Varianza1 = Stats.VarianzaVector(y1);
        DesviacionPbarNM = Stats.DesviacionNewton(Varianza1);
        PercPbar = Stats.Percentil(y1, Percentiles);
        figHisPbar.patch.set_alpha(0.0);  xHistPbar.patch.set_alpha(0.0);
        XlimInf2 = y1[0];    XlimSup2 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(y1[len(y1) - 1]))
        xHistPbar.hist(y1, bins=Rango1, rwidth = 1.2, edgecolor = "#7C0E47",color ="#EC067B",linewidth=4.0, alpha=0.6)
        xHistPbar.set_xticks([XlimInf2,PercPbar[0],PercPbar[1],PercPbar[2],XlimSup2])
        xHistPbar.set_xticklabels([f'{XlimInf2:.2f}mb',f'{PercPbar[0]:.0f}mb',f'{PercPbar[1]:.0f}mb',f'{PercPbar[2]:.0f}mb',f'{XlimSup2:.2f}mb'], color='#DBDBDB', fontsize=14, fontname=fuente)
        xHistPbar.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercPbar,ColorPerc):
            xHistPbar.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistPbar = io.BytesIO()
        plt.savefig(bufHistPbar, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHisPbar)
        src_hist_p_bar = f"data:image/png;base64,{base64.b64encode(bufHistPbar.getvalue()).decode('utf-8')}"
        BloqueHistPBar = html.Div([
            html.Img(src=src_hist_p_bar, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_p-bar',style=label_style,children=['Presión barometrica mb']),
            html.P([
                html.Strong('Media Aritmética'),html.Br(),
                f'{VectorPbar[0]:.0f}',html.Br(),
                html.Strong('Mediana'),html.Br(),
                f'{MedianaPbar:.4f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'{VarianzaInsesgadaPbar:.8f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'{DesviacionPbar:.8f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'{Varianza1:.8f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'{DesviacionPbarNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Minimo: {y1[0]:.0f}',f'\tMaximo: {y1[len(y1) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'{DatoModa1:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'P{Percentiles[0]}: {PercPbar[0]:.0f}mb',f'\tP{Percentiles[1]}: {PercPbar[1]:.0f}mb',f'\tP{Percentiles[2]}: {PercPbar[2]:.0f}mb'
            ])
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histograma de presion barometrica maxima
        figHisPbarMax, xHistPbarMax = plt.subplots(figsize=(10, 6))
        y3 = VectorPbarMaxMin[0];      Stats.timsort(y3);  DatoModa3 = Stats.ModaVectorValor(y3); MedianaPbarMax = Stats.MedianaVector(y3);
        VarianzaInsesgadaPbarMax = Stats.DesviacionMediaVector(y3, VectorPbar[1]);
        DesviacionPbarMax = Stats.DesviacionNewton(VarianzaInsesgadaPbarMax);
        Varianza3 = Stats.VarianzaVector(y3);
        DesviacionPbarMaxNM = Stats.DesviacionNewton(Varianza3);
        PercPbarMax = Stats.Percentil(y3, Percentiles);
        figHisPbarMax.patch.set_alpha(0.0);  xHistPbarMax.patch.set_alpha(0.0);
        XlimInf2 = y3[0];    XlimSup3 = y3[len(y3) - 1];  Rango3 = int(RegladeSturges(y3[len(y3) - 1]))
        xHistPbarMax.hist(y3, bins=Rango3, rwidth = 1.2, edgecolor = "black",color ="#7A8490",linewidth=4.0, alpha=0.6)
        xHistPbarMax.set_xticks([XlimInf2,PercPbarMax[0],PercPbarMax[1],PercPbarMax[2],XlimSup2])
        xHistPbarMax.set_xticklabels([f'{XlimInf2:.2f}mb',f'{PercPbarMax[0]:.0f}mb',f'{PercPbarMax[1]:.0f}mb',f'{PercPbarMax[2]:.0f}mb',f'{XlimSup2:.2f}mb'], color='#DBDBDB', fontsize=14, fontname=fuente)
        xHistPbarMax.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercPbarMax,ColorPerc):
            xHistPbarMax.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistPbarMax = io.BytesIO()
        plt.savefig(bufHistPbarMax, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHisPbarMax)
        src_hist_p_bar_max = f"data:image/png;base64,{base64.b64encode(bufHistPbarMax.getvalue()).decode('utf-8')}"
        BloqueHistPBarMax = html.Div([
            html.Img(src=src_hist_p_bar_max, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_p-bar-max',style=label_style,children=['Presión barometrica maxima mb']),
            html.P([
                html.Strong('Media Aritmética'),html.Br(),
                f'{VectorPbar[1]:.0f}',html.Br(),
                html.Strong('Mediana'),html.Br(),
                f'{MedianaPbarMax:.4f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'{VarianzaInsesgadaPbarMax:.8f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'{DesviacionPbarMax:.8f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'{Varianza3:.8f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'{DesviacionPbarMaxNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Minimo: {y3[0]:.0f}',f'\tMaximo: {y3[len(y3) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'{DatoModa3:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'P{Percentiles[0]}: {PercPbarMax[0]:.0f}mb',f'\tP{Percentiles[1]}: {PercPbarMax[1]:.0f}mb',f'\tP{Percentiles[2]}: {PercPbarMax[2]:.0f}mb'
            ])
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histograma de presion barometrica minima
        figHisPbarMin, xHistPbarMin = plt.subplots(figsize=(10, 6))
        y4 = VectorPbarMaxMin[1];      Stats.timsort(y4);  DatoModa4 = Stats.ModaVectorValor(y4); MedianaPbarMin = Stats.MedianaVector(y4);
        VarianzaInsesgadaPbarMin = Stats.DesviacionMediaVector(y4, VectorPbar[2]);
        DesviacionPbarMin = Stats.DesviacionNewton(VarianzaInsesgadaPbarMin);
        Varianza4 = Stats.VarianzaVector(y4);
        DesviacionPbarMinNM = Stats.DesviacionNewton(Varianza4);
        PercPbarMin = Stats.Percentil(y4, Percentiles);
        figHisPbarMin.patch.set_alpha(0.0);  xHistPbarMin.patch.set_alpha(0.0);
        XlimInf2 = y4[0];    XlimSup2 = y4[len(y4) - 1];  Rango4 = int(RegladeSturges(y4[len(y4) - 1]))
        xHistPbarMin.hist(y4, bins=Rango4, rwidth = 1.2, edgecolor = "black",color ="#BBC7D1",linewidth=4.0, alpha=0.6)
        xHistPbarMin.set_xticks([XlimInf2,PercPbarMin[0],PercPbarMin[1],PercPbarMin[2],XlimSup2])
        xHistPbarMin.set_xticklabels([f'{XlimInf2:.2f}mb',f'{PercPbarMin[0]:.0f}mb',f'{PercPbarMin[1]:.0f}mb',f'{PercPbarMin[2]:.0f}mb',f'{XlimSup2:.2f}mb'], color='#DBDBDB', fontsize=14, fontname=fuente)
        xHistPbarMin.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercPbarMin,ColorPerc):
            xHistPbarMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistPbarMin = io.BytesIO()
        plt.savefig(bufHistPbarMin, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHisPbarMin)
        src_hist_p_bar_min = f"data:image/png;base64,{base64.b64encode(bufHistPbarMin.getvalue()).decode('utf-8')}"
        BloqueHistPBarMin = html.Div([
            html.Img(src=src_hist_p_bar_min, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_p-bar-min',style=label_style,children=['Presión barometrica minima mb']),
            html.P([
                html.Strong('Media Aritmética'),html.Br(),
                f'{VectorPbar[2]:.0f}',html.Br(),
                html.Strong('Mediana'),html.Br(),
                f'{MedianaPbarMin:.4f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'{VarianzaInsesgadaPbarMin:.8f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'{DesviacionPbarMin:.8f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'{Varianza4:.8f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'{DesviacionPbarMinNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Minimo: {y4[0]:.0f}',f'\tMaximo: {y4[len(y4) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'{DatoModa4:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'P{Percentiles[0]}: {PercPbarMin[0]:.0f}mb',f'\tP{Percentiles[1]}: {PercPbarMin[1]:.0f}mb',f'\tP{Percentiles[2]}: {PercPbarMin[2]:.0f}mb'
            ])
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        #Histograma de presion absoluta
        figHisPabs, xHistPabs = plt.subplots(figsize=(10, 6))
        y2 = VectorPbarabs[1];      Stats.timsort(y2);  DatoModa2 = Stats.ModaVectorValor(y2); MedianaPabs = Stats.MedianaVector(y2);
        VarianzaInsesgadaPabs = Stats.DesviacionMediaVector(y2, MediaPabs);
        DesviacionPabs = Stats.DesviacionNewton(VarianzaInsesgadaPabs);
        Varianza2 = Stats.VarianzaVector(y2);
        DesviacionPabsNM = Stats.DesviacionNewton(Varianza2);
        PercPabs = Stats.Percentil(y2, Percentiles);
        figHisPabs.patch.set_alpha(0.0);  xHistPabs.patch.set_alpha(0.0);
        XlimInf2 = y2[0];    XlimSup2 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(y2[len(y2) - 1]))
        xHistPabs.hist(y2, bins=Rango2, rwidth = 1.2, edgecolor = "#02552A",color ="#06EC75",linewidth=4.0, alpha=0.6)
        xHistPabs.set_xticks([XlimInf2,PercPabs[0],PercPabs[1],PercPabs[2],XlimSup2])
        xHistPabs.set_xticklabels([f'{XlimInf2:.2f}mb',f'{PercPabs[0]:.0f}mb',f'{PercPabs[1]:.0f}mb',f'{PercPabs[2]:.0f}mb',f'{XlimSup2:.2f}mb'], color='#DBDBDB', fontsize=14, fontname=fuente)
        xHistPabs.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
        for p, val, col in zip(Percentiles,PercPabs,ColorPerc):
            xHistPabs.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
        #Codificar
        bufHistPabs = io.BytesIO()
        plt.savefig(bufHistPabs, format="png", bbox_inches="tight", transparent=True)
        plt.close(figHisPabs)
        src_hist_p_abs = f"data:image/png;base64,{base64.b64encode(bufHistPabs.getvalue()).decode('utf-8')}"
        BloqueHistPAbs = html.Div([
            html.Img(src=src_hist_p_abs, style={'width': '100%', 'height': '300px'}),
            html.Label(id='input-hist_p-bar',style=label_style,children=['Presion Absoluta mb']),
            html.P([
                html.Strong('Media Aritmética'),html.Br(),
                f'{MediaPabs:.0f}',html.Br(),
                html.Strong('Mediana'),html.Br(),
                f'{MedianaPabs:.4f}',html.Br(),
                html.Strong('Varianza Insesgada'),html.Br(),
                f'{VarianzaInsesgadaPabs:.8f}',html.Br(),
                html.Strong('Desviacion Estandar'),html.Br(),
                f'{DesviacionPabs:.8f}',html.Br(),
                html.Strong('Varianza Sesgada'),html.Br(),
                f'{Varianza2:.8f}',html.Br(),
                html.Strong('Desviacion Estandar sin Media'),html.Br(),
                f'{DesviacionPabsNM:.4f}',html.Br(),
                html.Strong('Valores Minimos y Maximos'),html.Br(),
                f'Minimo: {y1[0]:.0f}',f'\tMaximo: {y1[len(y1) - 1]:.0f}',html.Br(),
                html.Strong('Moda de los datos'),html.Br(),
                f'{DatoModa1:.0f}',html.Br(),
                html.Strong('Percentiles'),html.Br(),
                f'P{Percentiles[0]}: {PercPbar[0]:.0f}mb',f'\tP{Percentiles[1]}: {PercPbar[1]:.0f}mb',f'\tP{Percentiles[2]}: {PercPbar[2]:.0f}mb'
            ])
            ],  
            style={'width': '100%','textAlign': 'center'}
        )
        return BloquePbar,BloquePbarabs,None, BloqueHistPBar,BloqueHistPBarMax,BloqueHistPBarMin,BloqueHistPAbs, None,None,None, None,None,None,None
    
    if opcion == "Vientos":
        print("Registro Viento y su direccion")

        # AvgWindSpeed = 27;      PrevalentDir = 28;      AverageDir = 29;
        # WindRun = 30;           HighWindSpeed = 31;     HighWindDir = 32;

        #Indices
        i = AvgWindSpeed; Ante = HighWindDir;
        #Vectores
        VectorVelWind = [];
        Vector0_3 = [];    Vector3_6 = [];   Vector6_10 = [];   Vector10_13 = [];    Vector13_16 = [];   Vector16_32 = [];  Vector32 = [];
        VectorDirection = []
        vector8 = 0;
        plt.rcParams['axes.edgecolor'] = '#FFFFFF'    
        plt.rcParams['axes.linewidth'] = 3.0
        while(i <= Ante):
            #Datos de la fila del Mes seleccionado
            DatosFilas = df.iloc[Pos1:Pos2, i].tolist()
            #Datos de la columna del rango de filas
            Datos = [x.item() if hasattr(x, 'item') else x for x in DatosFilas]
            #Direcciones del grafico
            Direcciones = ['E','ENE','NE','NNE','N','NNW','NW','WNW','W','WSW','SW','SSW','S','SSE','SE','ESE']
            if(i == AvgWindSpeed):
                #Indice
                Indice = list(range(0, len(Datos)))
                #Verificacion de los datos
                Curva.InterpolacionLinealNoGraph(Datos, Indice, len(Datos))
                #Convertir Datos a float
                Datos = [float(i) for i in Datos]
                #Obtener los datos
                VectorVelWind = Datos
                #Para el vector de 0 a 3 km
                i = i + 1;
            elif(i == PrevalentDir or i == AverageDir):
                if(i == PrevalentDir):
                    Vector0_3,Vector3_6,Vector6_10,Vector10_13,Vector13_16,Vector16_32,Vector32,vector8 = DireccionesGrados(Datos,VectorVelWind)
                    VectorDirection.append(Vector0_3);  VectorDirection.append(Vector3_6);  VectorDirection.append(Vector6_10)
                    VectorDirection.append(Vector10_13);  VectorDirection.append(Vector13_16);  VectorDirection.append(Vector16_32);  VectorDirection.append(Vector32)
                if(i == AverageDir):
                    Vector0_3,Vector3_6,Vector6_10,Vector10_13,Vector13_16,Vector16_32,Vector32,vector8 = DireccionesGrados(Datos,VectorVelWind)
                    VectorDirection.append(Vector0_3);  VectorDirection.append(Vector3_6);  VectorDirection.append(Vector6_10)
                    VectorDirection.append(Vector10_13);  VectorDirection.append(Vector13_16);  VectorDirection.append(Vector16_32);  VectorDirection.append(Vector32)
                i = i + 1;
            elif(i == WindRun or i == HighWindSpeed or i == HighWindDir):
                i = i + 1;
        #Vector de "ceros"
        VectorBottom = [0] * 16
        # El 40% de los datos se mostrara en el 80% del grafico: (0.4)^p = 0.8  ->  p = log(0.8) / log(0.4)
        p = log(0.8) / log(0.4)
        #Funcio transformacion a Logaritmica
        def EscalaRosa(ValorTotal, MaximoDelVector):
            Porcentaje = [y / MaximoDelVector for y in ValorTotal]
            Expresion = [y**p for y in Porcentaje]
            return Expresion
        #Etiquetas para el texto y Colores de las barras
        Etiquetas = ['0 - 3 km','3 - 6 km','6 - 10 km','10 - 13 km','13 - 16 km','16 - 32 km','32 > km']
        Colores = ['#3EB1AE', '#0A9E85','#0070AD','#D4068A','#FFBA00','#FF5500','#0026FF']
        #Numeros del 0 a 2pi
        theta = np.linspace(0.0, 2*np.pi, 16, endpoint=False)
        #Ancho de las barras para simular triangulos
        Width = 2 * np.pi / 16
        #Vectores Barras
        y1 = VectorDirection[0];    y2 = VectorDirection[1];    y3 = VectorDirection[2];
        y4 = VectorDirection[3];    y5 = VectorDirection[4];    y6 = VectorDirection[5];    y7 = VectorDirection[6];
        #Sumar las iteraciones de cada vector
        SumaVectores = [x1 + x2 + x3 + x4 + x5 + x6 + x7 for x1, x2, x3, x4, x5, x6, x7 in zip(y1, y2, y3, y4, y5, y6, y7)]
        MaximoVectores = max(SumaVectores)
        MatrizDatos = [y1, y2, y3, y4, y5, y6, y7]
        figPrevWind, xPrevWind = plt.subplots(subplot_kw={"projection": "polar"})
        xPrevWind.set_axisbelow(True)
        for PrevWindVector, Etiqueta, Color in zip(MatrizDatos, Etiquetas, Colores):
            VectorInf = EscalaRosa(VectorBottom, MaximoVectores)
            VectorBottom = [x1 + x2 for x1,x2 in zip(VectorBottom , PrevWindVector)]
            VectorSup = EscalaRosa(VectorBottom, MaximoVectores)
            VectorAltura = [y1 - y2 for y1,y2 in zip(VectorSup , VectorInf)]
            xPrevWind.bar(theta,VectorAltura,bottom=VectorInf, color = Color,width=Width, linewidth=2, edgecolor='k', alpha=0.9)
        xPrevWind.set_xticks(theta)
        xPrevWind.set_xticklabels(Direcciones)
        plt.ylim(0, 1.1)

        bufPrevWind = io.BytesIO() 
        plt.savefig(bufPrevWind, format="png", bbox_inches='tight', transparent=True)
        plt.close(figPrevWind)

        #Codificacion
        src_prev_wind = f"data:image/png;base64,{base64.b64encode(bufPrevWind.getvalue()).decode('utf-8')}"
        BloquePrevWind = html.Div([
            html.Img(src=src_prev_wind, style={'width': '350px', 'height': '350px'}),
            html.Label(
                id='input-prev-wind',
                style={'width': '50%','backgroundColor':'transparent','border': '3px solid #b5b5b5','margin': '0 auto 40px auto','borderRadius': '10px','fontWeight': 'bold','backgroundImage': 'linear-gradient(135deg, #777 0%, #ccc 25%, #fff 50%, #ccc 75%, #555 100%)',
                       'display': 'inline-block','backgroundClip': 'text','WebkitBackgroundClip': 'text','color': 'transparent','WebkitTextFillColor': 'transparent'},
                children=[
                    'Direccion del viento prevalescente'
                    ]
                )
            ],
            style={"width": "100%",'textAlign': 'center'}
        )
        BloquePrevWindText = html.Div(
            [
            html.Label(
                id='input-label-prev-wind',
                style={'width': '100%','backgroundColor':'transparent','border': '3px solid #b5b5b5','margin': '0 auto 40px auto','borderRadius': '10px','fontWeight': 'bold','backgroundImage': 'linear-gradient(135deg, #777 0%, #ccc 25%, #fff 50%, #ccc 75%, #555 100%)',
                       'display': 'inline-block','backgroundClip': 'text','WebkitBackgroundClip': 'text','color': 'transparent','WebkitTextFillColor': 'transparent'},
                children=['Velocidad del Viento']
            ),
            html.Div(
                [
                    html.P(
                        style={"marginTop": "15px","fontSize": "14px","color": Colores[0],"fontFamily": "sans-serif",},
                        children=[ '0 - 3 km/h']
                    ),
                    html.P(
                        style={"marginTop": "15px","fontSize": "14px","color": Colores[1],"fontFamily": "sans-serif",},
                        children=[ '3 - 6 km/h']
                    ),
                    html.P(
                        style={"marginTop": "15px","fontSize": "14px","color": Colores[2],"fontFamily": "sans-serif",},
                        children=[ '6 - 10 km/h']
                    ),
                    html.P(
                        style={"marginTop": "15px","fontSize": "14px","color": Colores[3],"fontFamily": "sans-serif",},
                        children=[ '10 - 13 km/h']
                    ),
                    html.P(
                        style={"marginTop": "15px","fontSize": "14px","color": Colores[4],"fontFamily": "sans-serif",},
                        children=[ '13 - 16 km/h']
                    ),
                    html.P(
                        style={"marginTop": "15px","fontSize": "14px","color": Colores[5],"fontFamily": "sans-serif",},
                        children=[ '16 - 32 km/h']
                    ),
                    html.P(
                        style={"marginTop": "15px","fontSize": "14px","color": Colores[6],"fontFamily": "sans-serif",},
                        children=[ '32 > km/h']
                    )
                ],
                style={"width": "100%",'textAlign': 'center'}
            ),
        ],
        style={"width": "100%",'textAlign': 'center','paddingTop': '20px'}
        )
        #Vector de "ceros"
        VectorBottom = [0] * 16
        #Vectores Barras
        y1 = VectorDirection[7];    y2 = VectorDirection[8];    y3 = VectorDirection[9];
        y4 = VectorDirection[10];    y5 = VectorDirection[11];    y6 = VectorDirection[12];    y7 = VectorDirection[13];
        #Sumar las iteraciones de cada vector
        SumaVectores = [x1 + x2 + x3 + x4 + x5 + x6 + x7 for x1, x2, x3, x4, x5, x6, x7 in zip(y1, y2, y3, y4, y5, y6, y7)]
        MaximoVectores = max(SumaVectores)
        MatrizDatos = [y1, y2, y3, y4, y5, y6, y7]
        figAvgWind, xAvgWind = plt.subplots(subplot_kw={"projection": "polar"})
        xAvgWind.set_axisbelow(True)
        for PrevWindVector, Etiqueta, Color in zip(MatrizDatos, Etiquetas, Colores):
            VectorInf = EscalaRosa(VectorBottom, MaximoVectores)
            VectorBottom = [x1 + x2 for x1,x2 in zip(VectorBottom , PrevWindVector)]
            VectorSup = EscalaRosa(VectorBottom, MaximoVectores)
            VectorAltura = [y1 - y2 for y1,y2 in zip(VectorSup , VectorInf)]
            xAvgWind.bar(theta,VectorAltura,bottom=VectorInf, color = Color,width=Width, linewidth=2, edgecolor='k', alpha=0.9)
        xAvgWind.set_xticks(theta)
        xAvgWind.set_xticklabels(Direcciones)
        plt.ylim(0, 1.1)
        
        bufAvgWind = io.BytesIO() 
        plt.savefig(bufAvgWind, format="png", bbox_inches='tight', transparent=True)
        plt.close(figAvgWind)

        #Codificacion
        src_avg_wind = f"data:image/png;base64,{base64.b64encode(bufAvgWind.getvalue()).decode('utf-8')}"
        BloqueAvgWind = html.Div([
            html.Img(src=src_avg_wind, style={'width': '350px', 'height': '350px'}),
            html.Label(
                style={'width': '50%','backgroundColor':'transparent','border': '3px solid #b5b5b5','margin': '0 auto 40px auto','borderRadius': '10px','fontWeight': 'bold','backgroundImage': 'linear-gradient(135deg, #777 0%, #ccc 25%, #fff 50%, #ccc 75%, #555 100%)',
                       'display': 'inline-block','backgroundClip': 'text','WebkitBackgroundClip': 'text','color': 'transparent','WebkitTextFillColor': 'transparent'},
                children=[
                    'Direccion del viento promedio'
                    ]
                )
            ],
            style={"width": "100%",'textAlign': 'center'}
        )
        BloqueAvgWindText = html.Div(
            [
            html.Label(
                id='input-label-avg-wind',
                style={'width': '100%','backgroundColor':'transparent','border': '3px solid #b5b5b5','margin': '0 auto 40px auto','borderRadius': '10px','fontWeight': 'bold','backgroundImage': 'linear-gradient(135deg, #777 0%, #ccc 25%, #fff 50%, #ccc 75%, #555 100%)',
                       'display': 'inline-block','backgroundClip': 'text','WebkitBackgroundClip': 'text','color': 'transparent','WebkitTextFillColor': 'transparent'},
                children=['Velocidad del Viento']
            ),
            html.Div(
                [
                    html.P(
                        style={"marginTop": "15px","fontSize": "14px","color": Colores[0],"fontFamily": "sans-serif",},
                        children=[ '0 - 3 km/h']
                    ),
                    html.P(
                        style={"marginTop": "15px","fontSize": "14px","color": Colores[1],"fontFamily": "sans-serif",},
                        children=[ '3 - 6 km/h']
                    ),
                    html.P(
                        style={"marginTop": "15px","fontSize": "14px","color": Colores[2],"fontFamily": "sans-serif",},
                        children=[ '6 - 10 km/h']
                    ),
                    html.P(
                        style={"marginTop": "15px","fontSize": "14px","color": Colores[3],"fontFamily": "sans-serif",},
                        children=[ '10 - 13 km/h']
                    ),
                    html.P(
                        style={"marginTop": "15px","fontSize": "14px","color": Colores[4],"fontFamily": "sans-serif",},
                        children=[ '13 - 16 km/h']
                    ),
                    html.P(
                        style={"marginTop": "15px","fontSize": "14px","color": Colores[5],"fontFamily": "sans-serif",},
                        children=[ '16 - 32 km/h']
                    ),
                    html.P(
                        style={"marginTop": "15px","fontSize": "14px","color": Colores[6],"fontFamily": "sans-serif",},
                        children=[ '32 > km/h']
                    )
                ],
                style={"width": "100%",'textAlign': 'center'}
            ),
        ],
        style={"width": "100%",'textAlign': 'center'}
        )

        return BloquePrevWind,None,BloquePrevWindText,BloqueAvgWind,None,BloqueAvgWindText


if __name__ == '__main__':
    appEstacion.run(debug=True)






# Media1 = Stats.MediaVector(Dia)
# Media2 = Stats.MediaVector(Mes)
# print("Media de los dias: ",Media1)
# print("Media de los meses: ",Media2)
# print();
# Desv1 = Stats.DesviacionMediaVector(Dia, Media1)
# Desv2 = Stats.DesviacionMediaVector(Mes, Media2)
# print("Desviacion Estandar de los dias:",Desv1)
# print("Desviacion Estandar de los meses:",Desv2)
# print();
# Var1 = Stats.VarianzaVector(Dia)
# Var2 = Stats.VarianzaVector(Mes)
# print("Varianza de los dias:",Var1)
# print("Varianza de los meses:",Var2)
# print();
# DesvS1 = Stats.DesviacionSinMedia(Var1)
# DesvS2 = Stats.DesviacionSinMedia(Var2)
# print("Desviacion Estandar sin media de los dias:",DesvS1)
# print("Desviacion Estandar sin media de los meses:",DesvS2)
# print();
# Med1 = Stats.MedianaVector(Dia)
# Med2 = Stats.MedianaVector(Mes)
# print("La mediana de los dias:",Med1)
# print("La mediana de los meses:",Med2)
# print();
# Stats.ModaVector(Dia)
# Stats.ModaVector(Mes)
# print();






#Vectores Graficos
# VectorInsTempHum = [];
# VectorInsTempHumMax = [];
# VectorInsTempHumMin = [];
# while(i < 6):
#     i = i + 1;
#     print(DatosHeader[i])
#     Datos = [x.item() if hasattr(x, 'item') else x for x in df.iloc[:, i].tolist()[1:]]
#     Indice = list(range(0, len(Datos)))
#     Curva.InterpolacionLinealNoGraph(Datos, Indice, len(Datos))
#     indices_datos = [float(i) for i in Datos]
#     print();
#     if(i == 1 or i == 4):
#         #plt.hist(indices_datos, bins=10,rwidth = 1.2, color = 'green', edgecolor = 'black', label = DatosHeader[i], alpha=0.6)
#         matriz_nativa = [[x] for x in indices_datos]
#         VectorInsTempHum.append(Stats.Media(matriz_nativa))
#         i = i + 3;
    # if(i == 2 or i == 5):
    #     #plt.hist(indices_datos, bins=10,rwidth = 0.8, color = 'red', edgecolor = 'black', label = DatosHeader[i], alpha=0.4)
    #     matriz_nativa = [[x] for x in indices_datos]
    #     VectorInsTempHumMax.append(Stats.Media(matriz_nativa))
    # if(i == 3 or i == 6):    
    #     #plt.hist(indices_datos, bins=10,rwidth = 0.8, color = 'darkblue', edgecolor = 'black', label = DatosHeader[i], alpha=0.4)
    #     matriz_nativa = [[x] for x in indices_datos]
    #     VectorInsTempHumMin.append(Stats.Media(matriz_nativa))

# IndiceBarras = [round(x, 2) for x in VectorInsTempHum]
# IndiceBarras = [str(i) for i in IndiceBarras]

# fig, ax1 = plt.subplots(figsize=(10, 6))
# ax1.bar(IndiceBarras[0], VectorInsTempHum[0], color='red', alpha=0.2, label='Temperatura')
#ax1.bar(IndiceBarras[0], VectorInsTempHum[0], color='red', alpha=0.2)
#ax1.bar(IndiceBarras[0], VectorInsTempHum[0], color='blue', alpha=0.2)
# ax1.set_ylabel('Temperatura Interior (°C)', color='blue')
# ax1.tick_params(axis='y', labelcolor='blue')
# ax1.set_yticks([0, 10, 20, 30, 40])
# ax1.set_yticklabels(["0°C", "10°C", "20°C", "30°C", "40°C"]) 
# ax2 = ax1.twinx()

# ax2.bar(IndiceBarras[1], VectorInsTempHum[1], color = 'green', alpha=0.2, label='Porcentaje de Humedad')
#ax2.bar(IndiceBarras[1], VectorInsTempHumMax[1], color = 'red', alpha=0.2)
#ax2.bar(IndiceBarras[1], VectorInsTempHumMin[1], color = 'blue', alpha=0.2)
# ax2.set_ylabel('Humedad Interior (°C)', color='red')
# ax2.set_yticks([10, 20, 30, 40, 50, 60, 70, 80, 90, 100]) 
# ax2.set_yticklabels(["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"], color='red', fontsize=10)
# plt.tight_layout()

# ax1.set_xlabel("Temperatura Nominal vs Humedad Relativa")
# plt.xticks(rotation=15, ha='right')
#Fechas_X = [str(x) for x in df.iloc[:, 0].tolist()[1:]]
#indices_datos = [float(i) for i in Datos]

# plt.title('Histograma de Datos')
# plt.legend()
# plt.show()

# primera_columna = df.iloc[:, 0]
# print(primera_columna)
# print();
# primera_fila = df.iloc[0].tolist()
# print(primera_fila)
# print();
# valores_nativos = [x.item() if hasattr(x, 'item') else x for x in df.iloc[0].tolist()]
# Columnas = len(valores_nativos)
# print(valores_nativos)
# print();
# print("Datos : ", Columnas)
# print();







# # Pasos para extraer los datos de un archivo, guardarlos en un string, clasificarlos, obtener la matriz de datos, y escribirla en un nuevo archivo
# # # Crear Matriz de tipo string del archivo PMU_FDR.csv;
# NombreArchivoExtraer = "PMU_FDR_1750_10250_last7days_cleaned.csv";
# SeparadorExtraer = " ";
# SaltoFilaExtraer = 7;
# SaltoColumnaExtraer = 0;
# Extractor = Matriz.CrearMatrizArchivoString(NombreArchivoExtraer, SeparadorExtraer, SaltoFilaExtraer, SaltoColumnaExtraer);
# # # Crear Matriz de tipo c double del archivo PMU_FDR.csv;
# NombreArchivoCrear = "PMU_FDR_1750_10250_last7days_cleaned.csv";
# SeparadorCrear = ",";
# SaltoFilaCrear = 7;
# SaltoColumnaCrear = 2;
# Datos = Matriz.CrearMatrizArchivo(NombreArchivoCrear, SaltoFilaCrear, SaltoColumnaCrear, SeparadorCrear, TamañoEsperado);
# # # Crear Matriz Indice del Elemento que se quiere buscar
# TextoBuscar = "21-abr.-2025";
# Indice = Matriz.CreacionIndice(Extractor, TextoBuscar, 0);
# # # Guardar los nuevos datos en un nuevo CSV
# # # Para Frecuencia
# # NuevoArchivoDatos = "MatrizFrecuencia.csv";
# # # Para Voltaje
# NuevoArchivoDatos = "MatrizVoltaje.csv";
# NuevoSeparador = ",";
# Matriz.GuardarMatrizCSV(Datos, Indice, NuevoArchivoDatos, 0, 1, NuevoSeparador);
# NombreArchivo = "MatrizFrecuencia.csv";
# MFrecuencia = Matriz.CrearMatrizArchivoFloat(NombreArchivo, ",", 0, 0);
# Frecuencia = []; 
# Indice = [0,0,len(MFrecuencia)]
# for i in range(len(MFrecuencia)):
#     Frecuencia.append(MFrecuencia[i][0]);
# Estadistica.timsort(Frecuencia);
# NuevoArchivoDatos = "Frecuencia.csv";
# NuevoSeparador = ",";
# Matriz.GuardarVectorCSV(Frecuencia, len(Frecuencia), NuevoArchivoDatos, NuevoSeparador);

# NombreArchivo = "MatrizVoltaje.csv";
# MVoltaje = Matriz.CrearMatrizArchivoFloat(NombreArchivo, ",", 0, 0);
# Voltaje = []; 
# Indice = [0,0,len(MVoltaje)]
# for i in range(len(MVoltaje)):
#     Voltaje.append(MVoltaje[i][0]);
# Estadistica.timsort(Voltaje);
# NuevoArchivoDatos = "Voltaje.csv";
# NuevoSeparador = ",";
# Matriz.GuardarVectorCSV(Voltaje, len(Voltaje), NuevoArchivoDatos, NuevoSeparador);


# ArchivoEstadistica = "Frecuencia.csv"; SaltoFila2 = 0; SaltoColumna2 = 0; Separador2 = ",";
# MatrizDatos = Matriz.CrearMatrizArchivo(ArchivoEstadistica, SaltoFila2, SaltoColumna2, Separador2, TamañoEsperado)
# Percentiles = [10,25,50,90,100];
# Estadistica.DatosEstadisticos(MatrizDatos, Percentiles, 90)



                # html.Div(
                #     [
                #         html.Img(id="DobleAxial", style={"width": "100%", "display": "inline-block"},),
                #         dcc.Input(id="input-titulo",type="text",value="Temperatura y Humedad",debounce=True,),
                #         dcc.Store(id="mi-vector-temp-oculto", data=VectorInsTempHum),
                #     ],
                #     style={"width": "31%"},
                # ),
                # html.Div(
                #     [
                #         html.Img(id="BarrasMinMaxTemp", style={ "width": "100%", "display": "inline-block"},),
                #         dcc.Input(id="input-titulo-temp",type="text",value="Maximos y minimos de la Temperatura °C",debounce=True,),
                #         dcc.Store(id="mi-vector-max-oculto", data=VectorTemp),
                #     ],
                #     style={"width": "31%"},
                # ),
                # html.Div(
                #     [
                #         html.Img(id="BarrasMinMaxHum", style={ "width": "100%", "display": "inline-block"},),
                #         dcc.Input(id="input-titulo-hum",type="text",value="Maximos y minimos de la Humeadad '%'",debounce=True,),
                #         dcc.Store(id="mi-vector-min-oculto", data=VectorTemp),
                #     ],
                #     style={"width": "31%"},
                # ),  

                # html.Div(
                #     [
                #         html.Img(id="GraficoBarras", style={"width": "100%", "display": "inline-block"},),
                #         dcc.Input(id="input-titulo-Barras",type="text",value="Interior DewWetHeat",debounce=True,),
                #         dcc.Store(id="mi-vector-DewWetHeat-oculto", data=VectorInsDewWetHeat),
                #     ],
                #     style={"width": "50%"},
                # ),
                # html.Div(
                #     [
                #         html.Img(id="GraficoHeatHigh", style={ "width": "100%", "display": "inline-block"},),
                #         dcc.Input(id="input-titulo-HeatHigh",type="text",value="Interior Heat vs Maximum",debounce=True,),
                #         dcc.Store(id="mi-vector-Heat-oculto", data=VectorHeat),
                #     ],
                #     style={"width": "50%"},
                # ),

#plt.hist(indices_datos, bins=10,rwidth = 1.2, color = 'green', edgecolor = 'black', label = DatosHeader[i], alpha=0.6)
#plt.hist(indices_datos, bins=10,rwidth = 0.8, color = 'red', edgecolor = 'black', label = DatosHeader[i], alpha=0.4)
#plt.hist(indices_datos, bins=10,rwidth = 0.8, color = 'darkblue', edgecolor = 'black', label = DatosHeader[i], alpha=0.4)


#Callback y funcion de Grafica Temperatura
# @app.callback(
#     Output('DobleAxial', 'src'), # src attribute
#     Input("selector-analisis", "value"),
#     Input("input-titulo", "value"),
#     State("mi-vector-temp-oculto", "data"),
# )
# def update_figure(eleccion, titulo_texto, VectorPuntos):
#     if eleccion == "opcion_lineal":
#         #Titulo Grafica
#         #plt.title(titulo_texto)

#         #Indice
#         IndiceBarras = [f"Temp: {VectorPuntos[0]:.4f}",f"Temp: {VectorPuntos[1]:.4f}"]
#         #Figuras
#         fig, ax1 = plt.subplots(figsize=(10, 6))
#         #Grafica Temperatura
#         ax1.bar(IndiceBarras[0], VectorPuntos[0], color='red', alpha=0.2, label='Temperatura')
#         ax1.set_ylabel('Temperatura Interior (°C)', color='blue')
#         ax1.tick_params(axis='y', labelcolor='blue')
#         ax1.set_yticks([0, 10, 20, 30, 40])
#         ax1.set_yticklabels(["0°C", "10°C", "20°C", "30°C", "40°C"])

#         #Axis alterno
#         ax2 = ax1.twinx()

#         #Grafico Humedad
#         ax2.bar(IndiceBarras[1], VectorPuntos[1], color = 'green', alpha=0.2, label='Porcentaje de Humedad')
#         ax2.set_ylabel('Humedad Interior (°C)', color='red')
#         ax2.set_yticks([10, 20, 30, 40, 50, 60, 70, 80, 90, 100]) 
#         ax2.set_yticklabels(["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"], color='red', fontsize=10)
#         plt.tight_layout()
    
#         #Label General
#         ax1.set_xlabel("Temperatura Nominal - - - Humedad Relativa")
#         #Rotar Valores
#         plt.xticks(rotation=15, ha='right')

    
#         #Guardar imagen de MatplotLib
#         buf = io.BytesIO() 
#         fig.savefig(buf, format="png", bbox_inches='tight')
#         # Cierra la figura actual para liberar memoria de root
#         plt.close(fig) 
#         #Codificacion
#         data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
#         buf.close()
#         return "data:image/png;base64,{}".format(data)


#Callback y funcion de Grafica Temps Max y Min
# @app.callback(
#     Output("BarrasMinMaxTemp", "src"),
#     Input("selector-analisis", "value"),
#     Input("input-titulo-temp", "value"),
#     State("mi-vector-max-oculto", "data"),
# )
# def update_figure(eleccion, titulo_texto, VectorPuntos):
#     if eleccion == "opcion_lineal":
#         #Temp, Max, Min
#         y1 = VectorPuntos[0]
#         y2 = VectorPuntos[1]
#         y3 = VectorPuntos[2]
#         x = list(range(len(VectorPuntos[0])))
#         fig, ax = plt.subplots(figsize=(10, 6))
#         XlimInf = min(x); XlimSup = max(x);
#         YlimInf = min(y1); YlimSup = max(y1);
#         plt.xlim(XlimInf, XlimSup);   plt.ylim(YlimInf-0.5, YlimSup+0.5)
#         ax.plot(x, y1, color = 'red')
#         ax.plot(x, y2, color = 'blue')
#         ax.plot(x, y3, color = 'black')
#         #plt.title(titulo_texto)

#         #Guardar imagen de MatplotLib
#         buf = io.BytesIO()
#         fig.savefig(buf, format="png", bbox_inches='tight')
#         #Cierra la figura actual para liberar memoria de root
#         plt.close(fig)
#         #Codificacion
#         data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
#         buf.close()
#         return "data:image/png;base64,{}".format(data)

# html.Div(
#             [      
#                 #Dew - Wet - Heat
#                 html.Div(id="Dew-Wet-Heat", style={"width": "50%"}),

#                 #Heat - Heat Max
#                 html.Div(id="Heat-HeatMax", style={"width": "50%"}),
#             ],
#             style={
#                 "display": "flex",  # Activa el modo de diseño flexible
#                 "flexDirection": "row",  # Alinea los elementos en fila (horizontal)
#                 "flexWrap": "wrap",  
#                 "justifyContent": "space-between",  # Distribuye el espacio (izq, centro, der)
#                 "rowGap": "30px",
#                 #"alignItems": "flex-start",  # Alinea las columnas desde el borde superior
#                 "width": "100%",
#             },
#         ),


#Callback y funcion de Grafica Hum Max y Min
# @app.callback(
#     Output("BarrasMinMaxHum", "src"),
#     Input("selector-analisis", "value"),
#     Input("input-titulo-hum", "value"),
#     State("mi-vector-min-oculto", "data"),
# )
# def update_figure(eleccion, titulo_texto, VectorPuntos):
#     if eleccion == "opcion_lineal":
#         #Hum, Max, Min
#         y1 = VectorPuntos[3]
#         y2 = VectorPuntos[4]
#         y3 = VectorPuntos[5]
#         x = list(range(len(VectorPuntos[0])))
#         fig, ax = plt.subplots(figsize=(10, 6))
#         XlimInf = min(x); XlimSup = max(x);
#         YlimInf = min(y1); YlimSup = max(y1);
#         plt.xlim(XlimInf, XlimSup);   plt.ylim(YlimInf-0.5, YlimSup+0.5)
#         ax.plot(x, y1, color = 'red')
#         ax.plot(x, y2, color = 'blue')
#         ax.plot(x, y3, color = 'black')

#         #Guardar imagen de MatplotLib
#         buf = io.BytesIO() 
#         fig.savefig(buf, format="png", bbox_inches='tight')
#         # Cierra la figura actual para liberar memoria de root
#         plt.close(fig) 
#         #Codificacion
#         data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
#         buf.close()
#         return "data:image/png;base64,{}".format(data)
