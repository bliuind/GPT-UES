import base64
import io
import dash
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
from matplotlib.image import BboxImage
from matplotlib.transforms import Bbox
import plotly.graph_objects as go
import random

#Librerias de objeto
TamañoEsperado = 1024;
Matriz = Objeto.ClassCreacionMatrices()
Curva = Objeto.AjusteDeCurvas()
Stats = Objeto.Estadistica()

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


#Graficas 4. [1 - 2 - 3]
#Dew-Wet-Heat-Heat-Max exteriores
AvgWindSpeed = 27;      PrevalentDir = 28;      AverageDir = 29;
WindRun = 30;           HighWindSpeed = 31;     HighWindDir = 32;


#Graficas 5. [1 - 2]
#Dew-Wet-Heat-Heat-Max exteriores
WindChill = 33;          MinimoWindChill=34;      HeatIndex = 35;          HighHeatIndex = 36;
#Graficas 5. [3 - 4]
#THW Y THSW
THWIndex = 37;           MaximoTHWIndex = 38;     MinimoTHWIndex = 39;
THSWIndex = 40;          MaximoTHSWIndex = 41;    MinimoTHSWIndex = 42;

#Graficas 6. [1 - 2]
ETpot = 43 ;   Rain = 44;  HighRain = 45;


#Graficas 7. [1 - 2]
SolarRad = 46;  HighSolarRad = 47;
SolarE = 48;    UVIndex = 49;   HighUVIndex = 50;   UVDose = 51;
HeatD = 52;     CoolD = 53;
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

label_style_minus = {
    'width': '80%',
    'backgroundColor':'transparent',
    'border': '3px solid #b5b5b5',
    'borderRadius': '10px',
    'margin': '0 auto 40px auto',
    'display': 'inline-block',
    'fontWeight': 'bold',
    'fontSize': '14px',
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
appEstacion = dash.Dash(__name__)
server = appEstacion.server 

#Vectores Posicionadores Mes
PosicionesInicio = [];                  PosicionesFinal = [];
#Vectores Posicionadores Dias
PosicionesDiasInicio = [];              PosicionesDiasFinal = [];
Fechas = []
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
#Alinear la velocidad del viento de datos con direccion del viento
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
#Calcular Posiciones segun mes y fecha
def VectoresPosiciones(Month,Day,IndiceMes,IndiceDia):
    print("Entrada al calculador de Vectores de Posicion")
    #Reiniciar Vectores Posicionadores Mes
    global PosicionesInicio;                global PosicionesFinal;
    PosicionesInicio = [];                  PosicionesFinal = [];
    #Reiniciar Vectores Posicionadores Dias
    global PosicionesDiasInicio;            global PosicionesDiasFinal;
    PosicionesDiasInicio = [];              PosicionesDiasFinal = [];
    #Vectores para Label
    LabelMeses = [];            LabelDias = []
    LabelOpcionesNumeros = [];  LabelOpcionesMeses = [];
    #Vectores Posicionadores Auxiliares
    PosicionesAuxiliaresDiasInicio = [];    PosicionesAuxiliaresDiasFinal = [];
    PosicionesAuxiliaresDiasContador = [];  PosicionesContador = [];
    PosicionesAuxiliaresMesesNombre = [];
    #Rango
    i = 0;  j = 0;  k = 0;  Ante = len(Month)
    #Inicializacion Vectores
    LabelOpcionesMeses.append(Month[0])
    PosicionesInicio.append(i);
    PosicionesAuxiliaresDiasInicio.append(i);    PosicionesAuxiliaresDiasContador.append(k);
    PosicionesAuxiliaresMesesNombre.append(i)
    k = k + 1;
    while(i < Ante):
        #Es este mes diferente?
        if(Month[i] != IndiceMes):
            #Intercepta un nuevo indice str
            IndiceMes = Month[i]
            IndiceDia = Day[i]
            j = 0;  k = 0;
            #Añadimos las listas
            PosicionesDiasInicio.append(PosicionesAuxiliaresDiasInicio)
            PosicionesDiasFinal.append(PosicionesAuxiliaresDiasFinal)
            PosicionesContador.append(PosicionesAuxiliaresDiasContador)
            for m in range(len(PosicionesAuxiliaresDiasInicio)):
                LabelDias.append(Day[PosicionesAuxiliaresDiasInicio[m]])
                LabelMeses.append(Month[PosicionesAuxiliaresMesesNombre[m]])
            #Volvemos a crear los vectores
            PosicionesAuxiliaresDiasInicio = [];
            PosicionesAuxiliaresDiasFinal = [];
            PosicionesAuxiliaresDiasContador = [];
            PosicionesAuxiliaresMesesNombre = [];
            #Añade la posicion de este nuevo elemento
            PosicionesInicio.append(i)
            PosicionesAuxiliaresDiasInicio.append(i)
            PosicionesAuxiliaresMesesNombre.append(i)
            PosicionesAuxiliaresDiasContador.append(k)
            i = i + 1; k = k + 1;
        #Si es el mismo mes
        elif(Month[i] == IndiceMes):
            #Si es un dia diferente
            if(Day[i] != IndiceDia):
                PosicionesAuxiliaresDiasInicio.append(i)
                PosicionesAuxiliaresMesesNombre.append(i)
                PosicionesAuxiliaresDiasContador.append(k)
                k = k + 1;
                if(i != (len(Month) - 1)):
                    IndiceDia = Day[i+1]
            #Si es el mismo dia
            if(Day[i] == IndiceDia):
                #Esta el array antes de su ultimo elemento?
                if(i == (len(Month) - 1)):
                    #Ultima posicion del dia
                    PosicionesAuxiliaresDiasFinal.append(i)
                #Ha cambiado el dia?
                elif(Day[i+1] != IndiceDia):
                    LabelOpcionesNumeros.append(j)
                    j = j + 1
                    #Ultima posicion del dia
                    PosicionesAuxiliaresDiasFinal.append(i)
            #Esta el array antes de su ultimo elemento?
            if(i == (len(Month) - 1)):
                PosicionesFinal.append(i)
            #Si detecta un cambio en el siquiente indice toma la posicion final de este
            elif(Month[i+1] != IndiceMes):
                LabelOpcionesMeses.append(Month[i+1])
                PosicionesFinal.append(i)
            i = i + 1;
    PosicionesDiasInicio.append(PosicionesAuxiliaresDiasInicio);    PosicionesDiasFinal.append(PosicionesAuxiliaresDiasFinal)
    PosicionesContador.append(PosicionesAuxiliaresDiasContador);    LabelOpcionesNumeros.append(j)
    for m in range(len(PosicionesAuxiliaresDiasInicio)):
        LabelDias.append(Day[PosicionesAuxiliaresDiasInicio[m]])
        LabelMeses.append(Month[PosicionesAuxiliaresMesesNombre[m]])
    ValueToMonth(LabelMeses);   ValueToMonth(LabelOpcionesMeses);
    LabelOpciones = [];
    for k in range(len(LabelDias)):
        LabelOpciones.append(LabelDias[k]+"/"+LabelMeses[k])
    return LabelDias, PosicionesContador, LabelOpcionesMeses;

appEstacion.layout = html.Div(
    id='interfaz-grafica',
    style={
        'backgroundColor': "#3298FF",                         #Color del fondo
        #'backgroundImage': 'url("/assets/fondo_sol.jpg")',  #Imagen De Fondo
        #'backgroundImage': 'url("/assets/mifondo.jpg")',
        'backgroundAttachment': 'fixed',                    #Fijar Imagen 
        'backgroundSize': 'cover',                          #Toma toda la pantalla
        'backgroundPosition': 'center',                     #Centrar Imagen
        'backgroundRepeat': 'no-repeat',                    #No repetir imagen aunque el tamaño de los elementos supere la pantalla
        'height': '3000px',                                 #Altura de la imagen que queremos mostrar
    },
    children = [
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
                        "Graficos estacion meteorologica 7GT-EEP",              #Texto
                    ]
                )
            ]
        ),
        html.Div(
            id='interfaz-traslucida',
            style={
                'width': '98%',                                     #Que tanto ocupa de la pantalla
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
                        'color': "#1600B9",               #Color del texto
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
                            id='dropdown-estacion',
                            options=[
                                {'label': 'Pagina Principal', 'value': '-1'},                           #Opcion 1
                                {'label': 'Estación Meteorológica 7GT-EEP', 'value': '0'},              #Opcion 2
                                {'label': 'Estación Meteorológica 7GT-UES', 'value': '1'},              #Opcion 3
                            ],
                            value='-1',      # Valor inicial por defecto
                            clearable=False,            # Evita que el usuario deje el menú vacío
                            style={ 'width': '20%', 'color': "#006A85" }
                        ),
                        dcc.Dropdown(
                            id='dropdown-datos',
                            options=[
                                {'label': 'Temperaturas y Humedad Interiores', 'value': 'TemperaturasI'},   #Opcion 1
                                {'label': 'Temperaturas y Humedad Exteriores', 'value': 'TemperaturasE'},   #Opcion 2
                                {'label': 'Sensaciones Termicas', 'value': 'Sensaciones'},                  #Opcion 3
                                {'label': 'Presiones', 'value': 'Presiones'},                               #Opcion 4
                                {'label': 'Vendaval', 'value': 'Vientos'},                                  #Opcion 5
                                {'label': 'Precipitacion', 'value': 'DatosLluvia'},                         #Opcion 6
                                {'label': 'Irradiancia', 'value': 'DatosSol'}                           #Opcion 7
                            ],
                            value='TemperaturasI',      # Valor inicial por defecto
                            clearable=False,            # Evita que el usuario deje el menú vacío
                            style={ 'width': '30%', 'color': '#006A85' }
                        ),
                        dcc.Dropdown(
                            id='drop-años',
                            options=[{'label': 'Elegir Estacion', 'value': '-1'}],
                            value='-1',      # Valor inicial por defecto
                            clearable=False,            # Evita que el usuario deje el menú vacío
                            style={ 'width': '10%', 'color': '#006A85' }
                        ),
                        dcc.Dropdown(
                            id='drop-meses',
                            options=[
                                {'label': 'Escoger Estación', 'value': '-1'}
                            ],
                            value='-1', clearable=False,
                            style={ 'width': '20%', 'color': "#006A85" }
                        ),
                        dcc.Dropdown(
                            id='drop-dias',
                            options=[
                                {'label': 'Escoger Estación', 'value': '-1'}
                            ],
                            value='-1', clearable=False,
                            style={ 'width': '20%', 'color': "#006A85" }
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
#Los años dependen de la estacion   |   Devuelve opciones de años y valor por defecto   |   Recibe la estacion
@appEstacion.callback(
    Output('drop-años', 'options'),
    Output('drop-años', 'value'),
    Input('dropdown-estacion', 'value')
)
def actualizar_dropdowns_años(IndiceEstacionDCC):
    #Si es la pagina principal devuelve "Elegir Estación"
    if(IndiceEstacionDCC == '-1'):
        return [{'label': 'Elegir Estación', 'value': '-1'}],'-1'
    #Si no, devuelve los dos años de los csv
    else:
        return [{'label': '2025', 'value': '0'},{'label': '2026', 'value': '1'}],'0'
    
#Modificar meses segun estación |   Devuelve opciones de meses y valor por defecto   |   Recibe la estacion y el año
@appEstacion.callback(
    Output('drop-meses', 'options'),
    Output('drop-meses', 'value'),
    Input('dropdown-estacion', 'value'),
    Input('drop-años', 'value'),
)
def actualizar_dropdown_meses(IndiceEstacionDCC, IndiceAñoDCC):
    #La pagina principal
    global Fechas;
    if(IndiceEstacionDCC == '-1'):
        return [{'label': 'Elegir Estacion', 'value': '-1'}],'-1'
    #Estacion 7GT-EEP 2025
    elif(IndiceEstacionDCC == '0' and IndiceAñoDCC == '0'):
        df = pd.read_csv('Recreated_7GT-EEP_1-1-25_12-00_AM_1_Year_1779324867_v2.csv', skiprows=0, encoding='utf-8-sig', header=None, dtype=str)
        Fechas = [str(x).split(" ",1)[0] for x in df.iloc[:, 0].tolist()[1:]]
        Mes = [str(x).split("/",1)[0] for x in Fechas]
        Dia = [str(x).split("/",2)[1] for x in Fechas]
        #IndiceInicial
        IndexMes = Mes[0];         IndexDia = Dia[0];
        LabelDias, PosicionesContador,LabelOpcionesMeses = VectoresPosiciones(Mes,Dia,IndexMes,IndexDia)
        return [{'label': 'Todos los meses', 'value': '-1'}]+[{'label': mes, 'value': i} for i, mes in enumerate(LabelOpcionesMeses)],0
    #Estacion 7GT-EEP 2026
    elif(IndiceEstacionDCC == '0' and IndiceAñoDCC == '1'):
        df = pd.read_csv('Recreated_7GT-EEP_1-1-26_12-00_AM_1_Year_1779324876_v2.csv', skiprows=0, encoding='utf-8-sig', header=None, dtype=str)
        Fechas = [str(x).split(" ",1)[0] for x in df.iloc[:, 0].tolist()[1:]]
        Mes = [str(x).split("/",1)[0] for x in Fechas]
        Dia = [str(x).split("/",2)[1] for x in Fechas]
        #IndiceInicial
        IndexMes = Mes[0];         IndexDia = Dia[0];
        LabelDias, PosicionesContador,LabelOpcionesMeses = VectoresPosiciones(Mes,Dia,IndexMes,IndexDia)
        return [{'label': 'Todos los meses', 'value': '-1'}]+[{'label': mes, 'value': i} for i, mes in enumerate(LabelOpcionesMeses)],0
    #Estacion 7GT-UES 2025
    elif(IndiceEstacionDCC == '1' and IndiceAñoDCC == '0'):
        df = pd.read_csv('Recreated_7GT-UES_1-1-25_12-00_AM_1_Year_1779324630_v2.csv', skiprows=0, encoding='utf-8-sig', header=None, dtype=str)
        Fechas = [str(x).split(" ",1)[0] for x in df.iloc[:, 0].tolist()[1:]]
        Mes = [str(x).split("/",1)[0] for x in Fechas]
        Dia = [str(x).split("/",2)[1] for x in Fechas]
        #IndiceInicial
        IndexMes = Mes[0];         IndexDia = Dia[0];
        LabelDias, PosicionesContador,LabelOpcionesMeses = VectoresPosiciones(Mes,Dia,IndexMes,IndexDia)
        return [{'label': 'Todos los meses', 'value': '-1'}]+[{'label': mes, 'value': i} for i, mes in enumerate(LabelOpcionesMeses)],0
    #Estacion 7GT-UES 2026
    elif(IndiceEstacionDCC == '1' and IndiceAñoDCC == '1'):
        df = pd.read_csv('Recreated_7GT-UES_1-1-26_12-00_AM_1_Year_1779324751_v2.csv', skiprows=0, encoding='utf-8-sig', header=None, dtype=str)
        Fechas = [str(x).split(" ",1)[0] for x in df.iloc[:, 0].tolist()[1:]]
        Mes = [str(x).split("/",1)[0] for x in Fechas]
        Dia = [str(x).split("/",2)[1] for x in Fechas]
        #IndiceInicial
        IndexMes = Mes[0];         IndexDia = Dia[0];
        LabelDias, PosicionesContador,LabelOpcionesMeses = VectoresPosiciones(Mes,Dia,IndexMes,IndexDia)
        return [{'label': 'Todos los meses', 'value': '-1'}]+[{'label': mes, 'value': i} for i, mes in enumerate(LabelOpcionesMeses)],0
#Modificar dias segun estacion y meses
@appEstacion.callback(
    Output('drop-dias', 'options'),
    Output('drop-dias', 'value'),
    Input('drop-meses', 'value'),
    Input('dropdown-estacion', 'value'),
    Input('drop-años', 'value')
)
def actualizar_dropdown_dias(IndiceMesDCC, IndiceEstacionDCC, IndiceAñosDCC):
    if(IndiceEstacionDCC == '-1'):
        return [{'label': 'Todos los dias', 'value': '-1'}],'-1'
    elif(IndiceMesDCC == '-1'):
        return [{'label': 'Todos los dias', 'value': '-1'}],'-1'
    else:
        if IndiceMesDCC == -1 or IndiceMesDCC is None:
            return [{'label': 'Todos los días', 'value': -1}]
        PosicionesContador = [];    LabelDias = []; LabelOpcionesMeses = [];
        if(IndiceEstacionDCC == '0' and IndiceAñosDCC == '0'):
            df = pd.read_csv('Recreated_7GT-EEP_1-1-25_12-00_AM_1_Year_1779324867_v2.csv', skiprows=0, encoding='utf-8-sig', header=None, dtype=str)
            Fechas = [str(x).split(" ",1)[0] for x in df.iloc[:, 0].tolist()[1:]]
            Mes = [str(x).split("/",1)[0] for x in Fechas]
            Dia = [str(x).split("/",2)[1] for x in Fechas]
            IndexMes = Mes[0];         IndexDia = Dia[0];
            LabelDias, PosicionesContador,LabelOpcionesMeses = VectoresPosiciones(Mes,Dia,IndexMes,IndexDia)
        elif(IndiceEstacionDCC == '0' and IndiceAñosDCC == '1'):
            df = pd.read_csv('Recreated_7GT-EEP_1-1-26_12-00_AM_1_Year_1779324876_v2.csv', skiprows=0, encoding='utf-8-sig', header=None, dtype=str)
            Fechas = [str(x).split(" ",1)[0] for x in df.iloc[:, 0].tolist()[1:]]
            Mes = [str(x).split("/",1)[0] for x in Fechas]
            Dia = [str(x).split("/",2)[1] for x in Fechas]
            IndexMes = Mes[0];         IndexDia = Dia[0];
            LabelDias, PosicionesContador,LabelOpcionesMeses = VectoresPosiciones(Mes,Dia,IndexMes,IndexDia)
        elif(IndiceEstacionDCC == '1' and IndiceAñosDCC == '0'):
            df = pd.read_csv('Recreated_7GT-UES_1-1-25_12-00_AM_1_Year_1779324630_v2.csv', skiprows=0, encoding='utf-8-sig', header=None, dtype=str)
            Fechas = [str(x).split(" ",1)[0] for x in df.iloc[:, 0].tolist()[1:]]
            Mes = [str(x).split("/",1)[0] for x in Fechas]
            Dia = [str(x).split("/",2)[1] for x in Fechas]
            IndexMes = Mes[0];         IndexDia = Dia[0];
            LabelDias, PosicionesContador,LabelOpcionesMeses = VectoresPosiciones(Mes,Dia,IndexMes,IndexDia)
        elif(IndiceEstacionDCC == '1' and IndiceAñosDCC == '1'):
            df = pd.read_csv('Recreated_7GT-UES_1-1-26_12-00_AM_1_Year_1779324751_v2.csv', skiprows=0, encoding='utf-8-sig', header=None, dtype=str)
            Fechas = [str(x).split(" ",1)[0] for x in df.iloc[:, 0].tolist()[1:]]
            Mes = [str(x).split("/",1)[0] for x in Fechas]
            Dia = [str(x).split("/",2)[1] for x in Fechas]
            IndexMes = Mes[0];         IndexDia = Dia[0];
            LabelDias, PosicionesContador,LabelOpcionesMeses = VectoresPosiciones(Mes,Dia,IndexMes,IndexDia)
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
        return [{'label': 'Todos los dias', 'value': -1}] + [{'label': mes, 'value': dia} for dia, mes in zip(IndexDias, IndexMeses)], -1
#Callback Principal
@appEstacion.callback(
    Output("Graph1", 'children'),Output("Graph2", "children"),Output("Graph3", "children"),
    Output("Hist1", 'children'),Output("Hist2", "children"),Output("Hist3", "children"),Output("Hist4", "children"),
    Output("Graph4", 'children'),Output("Graph5", "children"),Output("Graph6", "children"),
    Output("Hist5", 'children'),Output("Hist6", "children"),Output("Hist7", "children"),Output("Hist8", "children"),
    Input('dropdown-estacion', 'value'),
    Input('dropdown-datos', 'value'),
    Input('drop-meses', 'value'),
    Input('drop-dias', 'value'),
    Input('drop-años', 'value')
)
def actualizar_grafico_o_datos(estacion,opcion, indiceMesDCC, indiceDiaDCC, indiceAñoDCC):
    if(estacion == '-1'):
        dfEEP = pd.DataFrame({'Lat': [13.473936346091364],'Lon': [-89.09600809463653],'Ciudad': ['San Salvador']})
        figEEP = px.scatter_map(dfEEP, lat='Lat', lon='Lon', hover_name='Ciudad',zoom=13)
        figEEP.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(r=0, t=0, l=0, b=0), map_style="open-street-map")
        dfUES = pd.DataFrame({'Lat': [13.717910872835937],'Lon': [-89.20180465021097],'Ciudad': ['San Salvador']})
        figUES = px.scatter_map(dfUES, lat='Lat', lon='Lon', hover_name='Ciudad',zoom=13)
        figUES.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(r=0, t=0, l=0, b=0), map_style="open-street-map")
        BloqueEEP = html.Div([
            html.Div([
                html.H1(
                id='map-eep',
                style={'color': '#5BC6E1','textAlign': 'center','fontSize': '20px','margin': '0 auto 20px auto'},
                children=["Mapa de la estacion metereologica EEP"]
                ),
            ]),
            html.Div([
                dcc.Graph(figure=figEEP, style={'width': '100%', 'height': '100%'},)
                ],
                style={'borderRadius': '20px','overflow': 'hidden','margin': '0 auto','boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.1)'}
            )
            ],
            style={'display': 'flex','flexDirection': 'column','justifyContent': 'center','alignItems': 'center','height': '60vh', 'width': '80%'}
        )
        BloqueUES = html.Div([
            html.Div([
                html.H1(
                    id='map-ues',
                    style={'color': '#5BC6E1','textAlign': 'center','fontSize': '20px','margin': '0 auto 20px auto'},
                    children=["Mapa del sistema de metereologica UES"]
                ),
            ]),
            html.Div([
                dcc.Graph(figure=figUES, style={'width': '100%', 'height': '100%'},)
                ],
                style={'borderRadius': '20px','overflow': 'hidden','margin': '0 auto','boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.1)'}
            )
            ],
            style={'display': 'flex','flexDirection': 'column','justifyContent': 'center','alignItems': 'center','height': '60vh', 'width': '80%'}
        )

        return None,BloqueEEP,None, None,None,None,None, None,BloqueUES,None, None,None,None,None
    else:
        if(estacion == '0' and indiceAñoDCC == '0'):
            df = pd.read_csv('Recreated_7GT-EEP_1-1-25_12-00_AM_1_Year_1779324867_v2.csv', skiprows=0, encoding='utf-8-sig', header=None, dtype=str)
            print("Estacion 7G7-EEP AÑO 2025")
        elif(estacion == '0' and indiceAñoDCC == '1'):
            df = pd.read_csv('Recreated_7GT-EEP_1-1-26_12-00_AM_1_Year_1779324876_v2.csv', skiprows=0, encoding='utf-8-sig', header=None, dtype=str)
            print("Estacion 7G7-EEP AÑO 2026")
        elif(estacion == '1' and indiceAñoDCC == '0'):
            df = pd.read_csv('Recreated_7GT-UES_1-1-25_12-00_AM_1_Year_1779324630_v2.csv', skiprows=0, encoding='utf-8-sig', header=None, dtype=str)
            print("Estacion 7G7-UES AÑO 2025")
        elif(estacion == '1'and indiceAñoDCC == '1'):
            df = pd.read_csv('Recreated_7GT-UES_1-1-26_12-00_AM_1_Year_1779324751_v2.csv', skiprows=0, encoding='utf-8-sig', header=None, dtype=str)
            print("Estacion 7G7-UES AÑO 2026")
        if (indiceDiaDCC == -1 and indiceMesDCC != '-1'):
            print("No se escogio un día en especifico")
            #Posiciones de Vectores para Meses Inicio
            Pos1 = PosicionesInicio[indiceMesDCC] + 1;
            #Posiciones de Vectores para Meses Final
            Pos2 = PosicionesFinal[indiceMesDCC] + 2;
        elif(indiceMesDCC == '-1'):
            print("No se escogio un mes en especifico")
            Pos1 = PosicionesInicio[0] + 1;
            #Posiciones de Vectores para Meses Final
            Pos2 = PosicionesFinal[len(PosicionesFinal) - 1] + 2;
        else:
            print("Se ha escogido un dia y un mes en especifico")
            Pos1 = PosicionesDiasInicio[indiceMesDCC][indiceDiaDCC] + 1;
            Pos2 = PosicionesDiasFinal[indiceMesDCC][indiceDiaDCC] + 2;
        
        Percentiles = [25,50,75];   ColorPerc = ['orange', 'red', 'green']
        #Temperaturas Interiores
        if opcion == "TemperaturasI":
            print("Registro Temperaturas Interiores")
            #Vectores Temperatura Interior
            VectorInsTempHum = [];  VectorInsDewWetHeat = [];   VectorTempHum = [];    VectorHeat = []; VectorInsDWH = [];
            #Inicio y Final del indice
            i = IndiceInsideTemp; Ante = IndiceInsideHeatMax;
            #Marcos color plata y bordes gruesos
            plt.rcParams['axes.edgecolor'] = "#000000"    
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
    
            #Grafica de Barras Temperatura
            IndiceBarrasDobleAxial = ["Temp","Hum"]
            figInsideTempHum = go.Figure()
            figInsideTempHum.add_trace(go.Bar(x=[IndiceBarrasDobleAxial[0]],y=[VectorInsTempHum[0]],
                name='Temperatura',marker=dict(color='#F99462',line=dict(color='#F76A25', width=6)),
                opacity=0.9,text=[f"{VectorInsTempHum[0]:.1f}°C"],  # Equivalente a bar_label
                textposition='outside',textfont=dict(color="#F76A25", size=12, family='sans-serif')
            ))
            figInsideTempHum.add_trace(go.Bar(x=[IndiceBarrasDobleAxial[1]],y=[VectorInsTempHum[1]],
                name='Humedad',yaxis='y2',marker=dict(color='#8ED7FB',line=dict(color="#01476B", width=6)),
                opacity=0.9,text=[f"{VectorInsTempHum[1]:.1f}%"],
                textposition='outside',textfont=dict(color="#01476B", size=12, family='sans-serif')
            ))
            figInsideTempHum.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    title=dict(text="Temperatura | Humedad",font=dict(color="#000000", size=16)),
                    tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                yaxis=dict(
                    title=dict(text='Temperatura Interior (°C)',font=dict(color="#000000", size=16)),range=[0, 35],
                    tickvals=[0, 5, 10, 15, 20, 25, 30, 35],ticktext=["0°C", "5°C", "10°C", "15°C", "20°C", "25°C", "30°C", "35°C"],
                    tickfont=dict(color='#F76A25', size=14),showgrid=False
                ),
                yaxis2=dict(
                    title=dict(text='Humedad Interior (%)',font=dict(color="#000000", size=16)),range=[0, 100],
                    tickvals=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100],ticktext=["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"],
                    tickfont=dict(color='#01476B', size=14),overlaying='y',side='right',showgrid=False
                ),
                margin=dict(l=60, r=60, t=30, b=60),showlegend=False,width=280,height=320
            )
            BloqueInsideTempHum = html.Div([
                html.Label(id='input-ins-temp-hum',style={'color': "#000000", 'fontSize': '16px'},children=['Temperatura y Humedad']),
                dcc.Graph(id='grafico-barras-doble-axial',figure=figInsideTempHum,config={'displayModeBar': False})
            ], style={'width': '300px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})

            ####################################################################
            ###                                                              ###
            ###     Grafica de los Maximos y Minimos de las Temperaturas     ###
            ###                                                              ###
            ####################################################################
    
            #Grafica x,y de Temperaturas
            figInsTempMaxMin = go.Figure()
            y1 = VectorTempHum[0];  y2 = VectorTempHum[1];  y3 = VectorTempHum[2];  x = list(range(len(VectorTempHum[0])))
            figInsTempMaxMin.add_trace(go.Scatter(x=x, y=y3,mode='lines',line=dict(color='#9D061F'),opacity=0.4,name='Minimos °C'))
            figInsTempMaxMin.add_trace(go.Scatter(x=x, y=y1,mode='lines',line=dict(color='#710416'),opacity=0.4,name='Temperatura °C'))
            figInsTempMaxMin.add_trace(go.Scatter(x=x, y=y2,mode='lines',line=dict(color='#45020E'),opacity=0.4,name='Maximos °C'))
            XlimInf = x[0]; XlimSup = x[len(x)-1];  YlimInf = Stats.DatoMinimoVector(y3); YlimSup = Stats.DatoMaximoVector(y2);
            tickvals_x = [XlimInf + (i * 0.1 * (XlimSup - XlimInf)) for i in range(11)]
            ticktext_x = [f'{val:.0f}' for val in tickvals_x]
            figInsTempMaxMin.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    range=[XlimInf, XlimSup],tickvals=tickvals_x,ticktext=ticktext_x,tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                yaxis=dict(range=[YlimInf - 0.5, YlimSup + 0.5],tickvals=[YlimInf, YlimSup],ticktext=[f'{YlimInf:.0f}°C', f'{YlimSup:.0f}°C'],
                    tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                margin=dict(l=40, r=40, t=20, b=40),showlegend=False,width=420,height=320
            )
            BloqueInsTempMaxMin = html.Div([
                html.Label(id='input-ins-temp-max-min',style={'color': "#000000", 'fontSize': '16px'}, children=['Maximos y minimos de la Temperatura °C']),
                dcc.Graph(id='grafico-ins-temp-max-min',figure=figInsTempMaxMin,config={'displayModeBar': True})   
            ], style={'width': '440px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            figInsTempMaxMin, xInsTempMaxMin = plt.subplots(figsize=(10, 6))
            figInsTempMaxMin.patch.set_alpha(0.0);  xInsTempMaxMin.patch.set_alpha(0.0)
            
            #################################################################
            ###                                                           ###
            ###     Grafica de los Maximos y Minimos de las Humedades     ###
            ###                                                           ###
            #################################################################
    
            figInsHumMaxMin = go.Figure()
            y1 = VectorTempHum[3];  y2 = VectorTempHum[4];  y3 = VectorTempHum[5];  x = list(range(len(VectorTempHum[3])))
            figInsHumMaxMin.add_trace(go.Scatter(x=x, y=y3,mode='lines',line=dict(color='#2900A1'),opacity=0.4,name='Minimos (%)'))
            figInsHumMaxMin.add_trace(go.Scatter(x=x, y=y1,mode='lines',line=dict(color='#1D0075'),opacity=0.4,name='Humedad (%)'))
            figInsHumMaxMin.add_trace(go.Scatter(x=x, y=y2,mode='lines',line=dict(color='#120047'),opacity=0.4,name='Maximos (%)'))
            XlimInf = x[0]; XlimSup = x[len(x)-1];  YlimInf = Stats.DatoMinimoVector(y3); YlimSup = Stats.DatoMaximoVector(y2);
            tickvals_x = [XlimInf + (i * 0.1 * (XlimSup - XlimInf)) for i in range(11)]
            ticktext_x = [f'{val:.0f}' for val in tickvals_x]
            figInsHumMaxMin.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    range=[XlimInf, XlimSup],tickvals=tickvals_x,ticktext=ticktext_x,tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                yaxis=dict(range=[YlimInf - 0.5, YlimSup + 0.5],tickvals=[YlimInf, YlimSup],ticktext=[f'{YlimInf:.0f}%', f'{YlimSup:.0f}%'],
                    tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                margin=dict(l=40, r=40, t=20, b=40),showlegend=False,width=420,height=320
            )
            BloqueInsHumMaxMin = html.Div([
                html.Label(id='input-ins-hum-max-min',style={'color': "#000000", 'fontSize': '16px'}, children=['Maximos y minimos de la Humeadad %']),
                dcc.Graph(id='grafico-ins-hum-max-min',figure=figInsHumMaxMin,config={'displayModeBar': True})   
            ], style={'width': '440px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})

            ##############################################################
            ###                                                        ###
            ###     Grafica de barra de interior de Dew, Wet, Heat     ###
            ###                                                        ###
            ##############################################################

            IndiceBarrasDWH = [f"Rocio",f"Bulbo",f"Calor"]
            figInsDWH = go.Figure()
            figInsDWH.add_trace(go.Bar(x=[IndiceBarrasDWH[0]],y=[VectorInsDewWetHeat[0]],
                name='Dew',marker=dict(color='#88D3C9',line=dict(color='#20564E', width=2.5)),
                opacity=0.9,text=[f"{VectorInsDewWetHeat[0]:.1f}°C"],textposition='outside',textfont=dict(color="#88D3C9", size=12, weight='bold')))
            figInsDWH.add_trace(go.Bar(x=[IndiceBarrasDWH[1]],y=[VectorInsDewWetHeat[1]],
                name='Wet',marker=dict(color='#57B1EB',line=dict(color='#204256', width=2.5)),
                opacity=0.9,text=[f"{VectorInsDewWetHeat[1]:.1f}°C"],textposition='outside',textfont=dict(color="#57B1EB", size=12, weight='bold')))
            figInsDWH.add_trace(go.Bar(x=[IndiceBarrasDWH[2]],y=[VectorInsDewWetHeat[2]],
                name='Heat',marker=dict(color='#E535A4',line=dict(color='#680D47', width=2.5)),
                opacity=0.9,text=[f"{VectorInsDewWetHeat[2]:.1f}°C"],textposition='outside',textfont=dict(color='#E535A4', size=12, weight='bold')))
            figInsDWH.update_layout(width=420,height=320,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(range=[0, 40],tickvals=[0, 5, 10, 15, 20, 25, 30, 35, 40],ticktext=["0°C", "5°C", "10°C", "15°C", "20°C", "25°C", "30°C", "35°C", "40°C"],
                tickfont=dict(color="#000000", size=14),showgrid=False),
                xaxis=dict(tickfont=dict(color="#000000", size=11),showgrid=False),
                margin=dict(l=45, r=15, t=30, b=40),showlegend=False)
            BloqueInsDWH = html.Div([
                html.Label(id='input-ins-dew-wet-heat',style={'color': "#000000", 'fontSize': '16px'}, children=["Punto de Rocío / Bulbo Húmedo / Sensación de calor"]),
                dcc.Graph(id='grafico-ins-dew-wet-heat',figure=figInsDWH,config={'displayModeBar': False},style={'margin': '0 auto', 'display': 'block'})
            ], style={'width': '440px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
    
            ###########################################
            ###                                     ###
            ###     Grafica de Heat vs Heat Max     ###
            ###                                     ###
            ###########################################

            figInsHMax = go.Figure()
            y1 = VectorHeat[0]; y2 = VectorHeat[1];  x = list(range(len(VectorHeat[0])))
            figInsHMax.add_trace(go.Scatter(x=x, y=y2,mode='lines',line=dict(color='#1EA300'),opacity=0.4,name='Maximos °C'))
            figInsHMax.add_trace(go.Scatter(x=x, y=y1,mode='lines',line=dict(color='#9FFF8A'),opacity=0.4,name='Sensacion de Calor °C'))
            XlimInf = x[0]; XlimSup = x[len(x)-1];  YlimInf = Stats.DatoMinimoVector(y1); YlimSup = Stats.DatoMaximoVector(y2);
            tickvals_x = [XlimInf + (i * 0.1 * (XlimSup - XlimInf)) for i in range(11)]
            ticktext_x = [f'{val:.0f}' for val in tickvals_x]
            figInsHMax.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    range=[XlimInf, XlimSup],tickvals=tickvals_x,ticktext=ticktext_x,tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                yaxis=dict(range=[YlimInf - 0.5, YlimSup + 0.5],tickvals=[YlimInf, YlimSup],ticktext=[f'{YlimInf:.0f}°C', f'{YlimSup:.0f}°C'],
                    tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                margin=dict(l=40, r=40, t=20, b=40),showlegend=False,width=520,height=320
            )
            BloqueInsHMax = html.Div([
                html.Label(id='input-ins-heat-heat_max',style={'color': "#000000", 'fontSize': '16px'}, children=['Sensación Termica vs Picos de calor °C']),
                dcc.Graph(id='grafico-ins-heat-heat_max',figure=figInsHMax,config={'displayModeBar': True})   
            ], style={'width': '540px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
    
            ###########################
            ###                     ###
            ###     Histogramas     ###
            ###                     ###
            ###########################

            #Histograma Temperatura
            figHistInsideTempHum, x1HistInsideTempHum = plt.subplots(figsize=(10, 6));  y1 = VectorTempHum[0];
            Media1,VarianzaInsesgadaInsTemp,Varianza1,DesviacionInsTempNM,DatoMaxInsTemp,IndiceMaxInsTemp,DatoMinInsTemp,IndiceMinInsTemp,DatoModa1 = Curva.DatosHTML(y1)
            Stats.timsort(y1);MedianaInsTemp = Stats.MedianaVector(y1);
            DesviacionInsTemp = Stats.DesviacionNewton(VarianzaInsesgadaInsTemp);
            Pearson1, r1 = Curva.RegresionLinealHTML(y1, VarianzaInsesgadaInsTemp)
            PercInsTemp = Stats.Percentil(y1, Percentiles);
            figHistInsideTempHum.patch.set_alpha(0.0);  x1HistInsideTempHum.patch.set_alpha(0.0);
            XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
            x1HistInsideTempHum.hist(y1, bins=Rango1,rwidth = 1.3, edgecolor = '#F76A25', color="#F99462",linewidth=4.0)
            x1HistInsideTempHum.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
            x1HistInsideTempHum.set_xticks([XlimInf1,PercInsTemp[0],PercInsTemp[1],PercInsTemp[2],XlimSup1])
            x1HistInsideTempHum.set_xticklabels([f'{XlimInf1:.2f}°C',f'{PercInsTemp[0]:.0f}°C',f'{PercInsTemp[1]:.0f}°C',f'{PercInsTemp[2]:.0f}°C',f'{XlimSup1:.2f}°C'], color="#000000", fontsize=14, fontname=fuente)
            for p, val, col in zip(Percentiles,PercInsTemp,ColorPerc):
                x1HistInsideTempHum.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistInsideTempHum1 = io.BytesIO()
            plt.savefig(bufHistInsideTempHum1, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistInsideTempHum)
            src_hist_ins_temp_hum_1 = f"data:image/png;base64,{base64.b64encode(bufHistInsideTempHum1.getvalue()).decode('utf-8')}"
            BloqueHistInsideTempHum1 = html.Div([
                html.Img(src=src_hist_ins_temp_hum_1, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ins-temp-hum',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Temperatura °C']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{Media1:.4f}',html.Br(),
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
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxInsTemp + Pos1]}',f', : {Fechas[IndiceMinInsTemp + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxInsTemp:.0f}°C',f',: {DatoMinInsTemp:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa1:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Temperatura: CD:{Pearson1:.4f}',f',CC:{r1:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercInsTemp[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercInsTemp[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercInsTemp[2]:.0f}°C'
                ],style={'textAlign': 'center'})
                ], style={'width': '380px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma Humedad
            figHistInsideTempHum, x2HistInsideTempHum = plt.subplots(figsize=(10, 6));  y2 = VectorTempHum[3];
            Media2,VarianzaInsesgadaInsHum,Varianza2,DesviacionInsHumNM,DatoMaxInsHum,IndiceMaxInsHum,DatoMinInsHum,IndiceMinInsHum,DatoModa2 = Curva.DatosHTML(y2)
            Stats.timsort(y2);  MedianaInsHum = Stats.MedianaVector(y2);
            DesviacionInsHum = Stats.DesviacionNewton(VarianzaInsesgadaInsHum);
            Pearson2, r2 = Curva.RegresionLinealHTML(y2, VarianzaInsesgadaInsHum)
            PercInsHum = Stats.Percentil(y2, Percentiles);
            figHistInsideTempHum.patch.set_alpha(0.0);  x2HistInsideTempHum.patch.set_alpha(0.0);
            XlimInf2 = y2[0];    XlimSup2 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(len(y2) - 1))
            x2HistInsideTempHum.hist(y2, bins=Rango2,rwidth = 1.2, edgecolor = '#25B1F7',color ="#8ED7FB",linewidth=4.0, alpha=0.6)
            x2HistInsideTempHum.set_xticks([XlimInf2,PercInsHum[0],PercInsHum[1],PercInsHum[2],XlimSup2])
            x2HistInsideTempHum.set_xticklabels([f'{XlimInf2:.2f}%',f'{PercInsHum[0]:.0f}%',f'{PercInsHum[1]:.0f}%',f'{PercInsHum[2]:.0f}%',f'{XlimSup2:.2f}%'], color="#000000", fontsize=14, fontname=fuente)
            x2HistInsideTempHum.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercInsHum,ColorPerc):
                x2HistInsideTempHum.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistInsideTempHum2 = io.BytesIO()
            plt.savefig(bufHistInsideTempHum2, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistInsideTempHum)
            src_hist_ins_temp_hum_2 = f"data:image/png;base64,{base64.b64encode(bufHistInsideTempHum2.getvalue()).decode('utf-8')}"
            BloqueHistInsideTempHum2 = html.Div([
                html.Img(src=src_hist_ins_temp_hum_2, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ins-temp-hum',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Humedad (%)']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{Media2:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaInsHum:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaInsHum:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionInsHum:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza2:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionInsHumNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxInsHum + Pos1]}',f', : {Fechas[IndiceMinInsHum + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxInsHum:.0f}%',f',: {DatoMinInsHum:.0f}%',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa2:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Humedad: CD:{Pearson2:.4f}',f',CC:{r2:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercInsHum[0]:.0f}%',f'\tP{Percentiles[1]}: {PercInsHum[1]:.0f}%',f'\tP{Percentiles[2]}: {PercInsHum[2]:.0f}%'
                ],style={'textAlign': 'center'})
                ], style={'width': '380px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histrograma Temperaturas
            y2 = VectorTempHum[1];  y3 = VectorTempHum[2]
            Media2,VarianzaInsesgadaInsTempMax,Varianza2,DesviacionInsTempMaxNM,DatoMaxInsTempMax,IndiceMaxInsTempMax,DatoMinInsTempMax,IndiceMinInsTempMax,DatoModa2 = Curva.DatosHTML(y2)
            Media3,VarianzaInsesgadaInsTempMin,Varianza3,DesviacionInsTempMinNM,DatoMaxInsTempMin,IndiceMaxInsTempMin,DatoMinInsTempMin,IndiceMinInsTempMin,DatoModa3 = Curva.DatosHTML(y3)
            Stats.timsort(y2);                      Stats.timsort(y3);
            Mediana2 = Stats.MedianaVector(y2);     Mediana3 = Stats.MedianaVector(y3);
            DesviacionInsTempMax = Stats.DesviacionNewton(VarianzaInsesgadaInsTempMax);
            DesviacionInsTempMin = Stats.DesviacionNewton(VarianzaInsesgadaInsTempMin);
            Pearson2, r2 = Curva.RegresionLinealHTML(y2, VarianzaInsesgadaInsTempMax)
            Pearson3, r3 = Curva.RegresionLinealHTML(y3, VarianzaInsesgadaInsTempMin)
            PercInsTempMax = Stats.Percentil(y2, Percentiles);
            PercInsTempMin = Stats.Percentil(y3, Percentiles);
            figHistInsTempMaxMin, xHistInsTempMaxMin = plt.subplots(figsize=(10, 6));
            figHistInsTempMaxMin.patch.set_alpha(0.0);  xHistInsTempMaxMin.patch.set_alpha(0.0);
            XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(len(y2) - 1))
            print(len(y2)); print(len(y3))
            xHistInsTempMaxMin.hist(y2, bins=Rango,rwidth = 1.2, color = "#F2042C",linewidth=4.0, edgecolor = "#780014", alpha=0.3, zorder = 0)
            xHistInsTempMaxMin.hist(y3, bins=Rango,rwidth = 1.2, color = "#EC3925",linewidth=4.0, edgecolor = "#A11500", alpha=0.3, zorder = 1)
            xHistInsTempMaxMin.set_xticks([XlimInf2,PercInsTempMax[0],PercInsTempMax[1],PercInsTempMax[2],PercInsTempMin[0],PercInsTempMin[1],PercInsTempMin[2],XlimSup2])
            xHistInsTempMaxMin.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercInsTempMax[0]:.0f}°C',f'{PercInsTempMax[1]:.0f}°C',f'{PercInsTempMax[2]:.0f}°C',f'{PercInsTempMin[0]:.0f}°C',f'{PercInsTempMin[1]:.0f}°C',f'{PercInsTempMin[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color="#000000", fontsize=14, fontname=fuente)
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
                html.Img(src=src_hist_ins_temp_max_min, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ins-temp-max-min',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Temperaturas °C']),
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
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxInsTempMax + Pos1]}',f', : {Fechas[IndiceMinInsTempMax + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxInsTempMax:.0f}°C',f',: {DatoMinInsTempMax:.0f}°C',html.Br(),
                    f'Fecha Minimos: {Fechas[IndiceMaxInsTempMin + Pos1]}',f', : {Fechas[IndiceMinInsTempMin + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxInsTempMin:.0f}°C',f',: {DatoMinInsTempMin:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para maximas: {DatoModa2:.0f}',f'\tPara Minimos: {DatoModa3:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para maximas: CD:{Pearson2:.4f}',f',CC:{r2:.4f}',html.Br(),f'Para Minimos: CD:{Pearson3:.4f}',f'CC:{r3:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Maximas: P{Percentiles[0]}: {PercInsTempMax[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercInsTempMax[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercInsTempMax[2]:.0f}°C',html.Br(),
                    f'Minimas: P{Percentiles[0]}: {PercInsTempMin[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercInsTempMin[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercInsTempMin[2]:.0f}°C'
                ],style={'textAlign': 'center'})  
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histrograma Humedades
            y2 = VectorTempHum[4];  y3 = VectorTempHum[5]
            Media2,VarianzaInsesgadaInsHumMax,Varianza2,DesviacionInsHumMaxNM,DatoMaxInsHumMax,IndiceMaxInsHumMax,DatoMinInsHumMax,IndiceMinInsHumMax,DatoModa2 = Curva.DatosHTML(y2)
            Media3,VarianzaInsesgadaInsHumMin,Varianza3,DesviacionInsHumMinNM,DatoMaxInsHumMin,IndiceMaxInsHumMin,DatoMinInsHumMin,IndiceMinInsHumMin,DatoModa3 = Curva.DatosHTML(y3)
            Stats.timsort(y2);                      Stats.timsort(y3);
            Mediana2 = Stats.MedianaVector(y2);     Mediana3 = Stats.MedianaVector(y3);
            DesviacionInsHumMax = Stats.DesviacionNewton(VarianzaInsesgadaInsHumMax);
            DesviacionInsHumMin = Stats.DesviacionNewton(VarianzaInsesgadaInsHumMin);
            Pearson2, r2 = Curva.RegresionLinealHTML(y2, VarianzaInsesgadaInsHumMax)
            Pearson3, r3 = Curva.RegresionLinealHTML(y3, VarianzaInsesgadaInsHumMin)
            PercInsHumMax = Stats.Percentil(y2, Percentiles);
            PercInsHumMin = Stats.Percentil(y3, Percentiles);
            figHistInsHumMaxMin, xHistInsHumMaxMin = plt.subplots(figsize=(10, 6));
            figHistInsHumMaxMin.patch.set_alpha(0.0);  xHistInsHumMaxMin.patch.set_alpha(0.0);
            XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(len(y2) - 1));
            xHistInsHumMaxMin.hist(y2, bins=Rango+1,rwidth = 1.2, color = '#2900A1',linewidth=4.0, edgecolor = "#35A8F5", alpha=0.3, zorder = 0)
            xHistInsHumMaxMin.hist(y3, bins=Rango+1,rwidth = 1.2, color = '#120047',linewidth=4.0, edgecolor = "#2E02B2", alpha=0.3, zorder = 1)
            xHistInsHumMaxMin.set_xticks([XlimInf2,PercInsHumMax[0],PercInsHumMax[1],PercInsHumMax[2],PercInsHumMin[0],PercInsHumMin[1],PercInsHumMin[2],XlimSup2])
            xHistInsHumMaxMin.set_xticklabels([f'{XlimInf2:.2f} %',f'{PercInsHumMax[0]:.0f}°C',f'{PercInsHumMax[1]:.0f}°C',f'{PercInsHumMax[2]:.0f}°C',f'{PercInsHumMin[0]:.0f}°C',f'{PercInsHumMin[1]:.0f}°C',f'{PercInsHumMin[2]:.0f}°C',f'{XlimSup2:.2f} %'], color="#000000", fontsize=14, fontname=fuente)
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
                html.Img(src=src_hist_ins_hum_max_min, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ins-hum-max-min',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Humedades (%)']),
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
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxInsHumMax + Pos1]}',f', : {Fechas[IndiceMinInsHumMax + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxInsHumMax:.0f}%',f',: {DatoMinInsHumMax:.0f}%',html.Br(),
                    f'Fecha Minimos: {Fechas[IndiceMaxInsHumMin + Pos1]}',f', : {Fechas[IndiceMinInsHumMin + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxInsHumMin:.0f}%',f',: {DatoMinInsHumMin:.0f}%',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para maximas: {DatoModa2:.0f}',f'\tPara Minimos: {DatoModa3:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para maximas: CD:{Pearson2:.4f}',f',CC:{r2:.4f}',html.Br(),f'Para Minimos: CD:{Pearson3:.4f}',f'CC:{r3:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Maximas: P{Percentiles[0]}: {PercInsHumMax[0]:.0f}%',f'\tP{Percentiles[1]}: {PercInsHumMax[1]:.0f}%',f'\tP{Percentiles[2]}: {PercInsHumMax[2]:.0f}%',html.Br(),
                    f'Minimas: P{Percentiles[0]}: {PercInsHumMin[0]:.0f}%',f'\tP{Percentiles[1]}: {PercInsHumMin[1]:.0f}%',f'\tP{Percentiles[2]}: {PercInsHumMin[2]:.0f}%'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma del Punto de Rocio Interior
            figHistInsideD, x1HistInsideD = plt.subplots(figsize=(10, 6));  y4 = VectorInsDWH[0];
            Media4,VarianzaInsesgadaInsD,Varianza4,DesviacionInsDNM,DatoMaxInsD,IndiceMaxInsD,DatoMinInsD,IndiceMinInsD,DatoModa4 = Curva.DatosHTML(y4)
            Stats.timsort(y4);  MedianaInsD = Stats.MedianaVector(y4);
            DesviacionInsD = Stats.DesviacionNewton(VarianzaInsesgadaInsD);
            Pearson4, r4 = Curva.RegresionLinealHTML(y4, VarianzaInsesgadaInsD)
            PercInsD = Stats.Percentil(y4, Percentiles);
            figHistInsideD.patch.set_alpha(0.0);  x1HistInsideD.patch.set_alpha(0.0);
            XlimInf2 = y4[0];    XlimSup2 = y4[len(y4) - 1];  Rango4 = int(RegladeSturges(len(y4) - 1))
            x1HistInsideD.hist(y4, bins=Rango4,rwidth = 1.2, edgecolor = '#20564E',color ="#20564E",linewidth=4.0, alpha=0.6)
            x1HistInsideD.set_xticks([XlimInf2,PercInsD[0],PercInsD[1],PercInsD[2],XlimSup2])
            x1HistInsideD.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercInsD[0]:.0f}°C',f'{PercInsD[1]:.0f}°C',f'{PercInsD[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color="#000000", fontsize=14, fontname=fuente)
            x1HistInsideD.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercInsD,ColorPerc):
                x1HistInsideD.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistInsideD = io.BytesIO()
            plt.savefig(bufHistInsideD, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistInsideD)
            src_hist_ins_d = f"data:image/png;base64,{base64.b64encode(bufHistInsideD.getvalue()).decode('utf-8')}"
            BloqueHistInsideD = html.Div([
                html.Img(src=src_hist_ins_d, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ins-d',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Punto de Rocio°C']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{Media4:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaInsD:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaInsD:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionInsD:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza4:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionInsDNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxInsD + Pos1]}',f', : {Fechas[IndiceMinInsD + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxInsD:.0f}°C',f',: {DatoMinInsD:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa4:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Punto de Rocio: CD:{Pearson4:.4f}',f',CC:{r4:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercInsD[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercInsD[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercInsD[2]:.0f}°C'
                ],style={'textAlign': 'center'})
                ], style={'width': '380px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma del Bulbo Húmedo
            figHistInsideW, x2HistInsideW = plt.subplots(figsize=(10, 6));            y5 = VectorInsDWH[1];
            Media5,VarianzaInsesgadaInsW,Varianza5,DesviacionInsWNM,DatoMaxInsW,IndiceMaxInsW,DatoMinInsW,IndiceMinInsW,DatoModa5 = Curva.DatosHTML(y5)
            Stats.timsort(y5);  DatoModa5 = Stats.ModaVectorValor(y5); MedianaInsW = Stats.MedianaVector(y5);
            DesviacionInsW = Stats.DesviacionNewton(VarianzaInsesgadaInsW);
            Pearson5, r5 = Curva.RegresionLinealHTML(y5, VarianzaInsesgadaInsW)
            PercInsW = Stats.Percentil(y5, Percentiles);
            figHistInsideW.patch.set_alpha(0.0);  x2HistInsideW.patch.set_alpha(0.0);
            XlimInf2 = y5[0];    XlimSup2 = y5[len(y5) - 1];  Rango5 = int(RegladeSturges(len(y5) - 1))
            x2HistInsideW.hist(y5, bins=Rango5,rwidth = 1.2, edgecolor = '#204256',color ="#57B1EB",linewidth=4.0, alpha=0.6)
            x2HistInsideW.set_xticks([XlimInf2,PercInsW[0],PercInsW[1],PercInsW[2],XlimSup2])
            x2HistInsideW.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercInsW[0]:.0f}°C',f'{PercInsW[1]:.0f}°C',f'{PercInsW[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color="#000000", fontsize=14, fontname=fuente)
            x2HistInsideW.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercInsW,ColorPerc):
                x2HistInsideW.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistInsideW = io.BytesIO()
            plt.savefig(bufHistInsideW, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistInsideW)
            src_hist_ins_w = f"data:image/png;base64,{base64.b64encode(bufHistInsideW.getvalue()).decode('utf-8')}"
            BloqueHistInsideW = html.Div([
                html.Img(src=src_hist_ins_w, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ins-w',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Bulbo Húmedo°C']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{Media5:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaInsW:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaInsW:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionInsW:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza5:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionInsWNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxInsW + Pos1]}',f', : {Fechas[IndiceMinInsW + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxInsW:.0f}°C',f',: {DatoMinInsW:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa5:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Bulbo Húmedo: CD:{Pearson5:.4f}',f',CC:{r5:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercInsW[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercInsW[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercInsW[2]:.0f}°C'
                ],style={'textAlign': 'center'})
                ], style={'width': '380px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma de sensacion termica
            figHistInsideH, x3HistInsideH = plt.subplots(figsize=(10, 6));      y6 = VectorInsDWH[2];
            Media6,VarianzaInsesgadaInsH,Varianza6,DesviacionInsHNM,DatoMaxInsH,IndiceMaxInsH,DatoMinInsH,IndiceMinInsH,DatoModa6 = Curva.DatosHTML(y6)
            Stats.timsort(y6);  MedianaInsH = Stats.MedianaVector(y6);
            DesviacionInsH = Stats.DesviacionNewton(VarianzaInsesgadaInsH);
            Pearson6, r6 = Curva.RegresionLinealHTML(y5, VarianzaInsesgadaInsH)
            PercInsH = Stats.Percentil(y6, Percentiles);
            figHistInsideH.patch.set_alpha(0.0);  x3HistInsideH.patch.set_alpha(0.0);
            XlimInf2 = y6[0];    XlimSup2 = y6[len(y6) - 1];  Rango6 = int(RegladeSturges(len(y6) - 1))
            x3HistInsideH.hist(y6, bins=Rango6,rwidth = 1.2, edgecolor = '#680D47',color ="#E535A4",linewidth=4.0, alpha=0.6)
            x3HistInsideH.set_xticks([XlimInf2,PercInsH[0],PercInsH[1],PercInsH[2],XlimSup2])
            x3HistInsideH.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercInsH[0]:.0f}°C',f'{PercInsH[1]:.0f}°C',f'{PercInsH[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color="#000000", fontsize=14, fontname=fuente)
            x3HistInsideH.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercInsH,ColorPerc):
                x3HistInsideH.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistInsideH = io.BytesIO()
            plt.savefig(bufHistInsideH, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistInsideH)
            src_hist_ins_h = f"data:image/png;base64,{base64.b64encode(bufHistInsideH.getvalue()).decode('utf-8')}"
            BloqueHistInsideH = html.Div([
                html.Img(src=src_hist_ins_h, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ins-h',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Sensacion calorica°C']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{Media6:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaInsH:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaInsH:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionInsH:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza6:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionInsHNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxInsH + Pos1]}',f', : {Fechas[IndiceMinInsH + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxInsH:.0f}°C',f',: {DatoMinInsH:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa6:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Bulbo Húmedo: CD:{Pearson6:.4f}',f',CC:{r6:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercInsH[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercInsH[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercInsH[2]:.0f}°C'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma de sensacion termica maxima
            figHistInsideHMax, x4HistInsideHMax = plt.subplots(figsize=(10, 6));        y7 = VectorHeat[1];
            Media7,VarianzaInsesgadaInsHMax,Varianza7,DesviacionInsHMaxNM,DatoMaxInsHMax,IndiceMaxInsHMax,DatoMinInsHMax,IndiceMinInsHMax,DatoModa7 = Curva.DatosHTML(y7)
            Stats.timsort(y7);  MedianaInsHMax = Stats.MedianaVector(y7); 
            DesviacionInsHMax = Stats.DesviacionNewton(VarianzaInsesgadaInsHMax);
            Pearson7, r7 = Curva.RegresionLinealHTML(y5, VarianzaInsesgadaInsHMax)
            PercInsHMax = Stats.Percentil(y7, Percentiles);
            figHistInsideHMax.patch.set_alpha(0.0);  x4HistInsideHMax.patch.set_alpha(0.0);
            XlimInf2 = y7[0];    XlimSup2 = y7[len(y7) - 1];  Rango7 = int(RegladeSturges(len(y7) - 1))
            x4HistInsideHMax.hist(y7, bins=Rango7,rwidth = 1.2, edgecolor = "#6D0B10",color ="#ED1932",linewidth=4.0, alpha=0.6)
            x4HistInsideHMax.set_xticks([XlimInf2,PercInsHMax[0],PercInsHMax[1],PercInsHMax[2],XlimSup2])
            x4HistInsideHMax.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercInsHMax[0]:.0f}°C',f'{PercInsHMax[1]:.0f}°C',f'{PercInsHMax[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color="#000000", fontsize=14, fontname=fuente)
            x4HistInsideHMax.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercInsHMax,ColorPerc):
                x4HistInsideHMax.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistInsideHMax = io.BytesIO()
            plt.savefig(bufHistInsideHMax, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistInsideHMax)
            src_hist_ins_h_max = f"data:image/png;base64,{base64.b64encode(bufHistInsideHMax.getvalue()).decode('utf-8')}"
            BloqueHistInsideHMax = html.Div([
                html.Img(src=src_hist_ins_h_max, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ins-h-max',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Sensacion calorica maxima°C']),
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
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxInsHMax + Pos1]}',f', : {Fechas[IndiceMinInsHMax + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxInsHMax:.0f}°C',f',: {DatoMinInsHMax:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa7:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Bulbo Húmedo: CD:{Pearson7:.4f}',f',CC:{r7:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercInsHMax[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercInsHMax[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercInsHMax[2]:.0f}°C'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            return BloqueInsideTempHum, BloqueInsTempMaxMin, BloqueInsHumMaxMin,BloqueHistInsideTempHum1, BloqueHistInsideTempHum2, BloqueHistInsideTempMaxMin, BloqueHistInsideHumMaxMin, BloqueInsDWH, BloqueInsHMax, None,BloqueHistInsideD, BloqueHistInsideW, BloqueHistInsideH, BloqueHistInsideHMax
        #Temperaturas exteriores
        if opcion == "TemperaturasE":
            print("Registro Temperaturas Exteriores")
            #Vectores Temperatura Exterior
            VectorExtTempHumM = [];     VectorExtTempHum = [];  
            #Vectores Dew - Wet
            VectorExtDewWetM = [];      VectorExtDewWet = [];
            #Inicio y Final del indice
            i = IndiceExteriorTemp; Ante = IndiceExteriorWetMin;
            #Marcos color plata y bordes gruesos
            plt.rcParams['axes.edgecolor'] = "#060202"    
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
            IndiceBarrasDobleAxial = ["Temp","Hum"]
            figExteriorTempHum = go.Figure()
            figExteriorTempHum.add_trace(go.Bar(x=[IndiceBarrasDobleAxial[0]],y=[VectorExtTempHumM[0]],
                name='Temperatura',marker=dict(color='#E84163',line=dict(color='#91122B', width=6)),
                opacity=0.9,text=[f"{VectorExtTempHumM[0]:.1f}°C"],  # Equivalente a bar_label
                textposition='outside',textfont=dict(color="#91122B", size=12, family='sans-serif')
            ))
            figExteriorTempHum.add_trace(go.Bar(x=[IndiceBarrasDobleAxial[1]],y=[VectorExtTempHumM[1]],
                name='Humedad',yaxis='y2',marker=dict(color='#1B08FF',line=dict(color="#060047", width=6)),
                opacity=0.9,text=[f"{VectorExtTempHumM[1]:.1f}%"],
                textposition='outside',textfont=dict(color="#060047", size=12, family='sans-serif')
            ))
            figExteriorTempHum.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    title=dict(text="Temperatura | Humedad",font=dict(color="#000000", size=16)),
                    tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                yaxis=dict(
                    title=dict(text='Temperatura Exterior (°C)',font=dict(color="#000000", size=16)),range=[0, 35],
                    tickvals=[0, 5, 10, 15, 20, 25, 30, 35],ticktext=["0°C", "5°C", "10°C", "15°C", "20°C", "25°C", "30°C", "35°C"],
                    tickfont=dict(color='#91122B', size=14),showgrid=False
                ),
                yaxis2=dict(
                    title=dict(text='Humedad Exterior (%)',font=dict(color="#000000", size=16)),range=[0, 100],
                    tickvals=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100],ticktext=["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"],
                    tickfont=dict(color='#060047', size=14),overlaying='y',side='right',showgrid=False
                ),
                margin=dict(l=60, r=60, t=30, b=60),showlegend=False,width=280,height=320
            )
            BloqueExtTempHum = html.Div([
                html.Label(id='input-ext-temp-hum',style={'color': "#000000", 'fontSize': '16px'},children=['Temperatura y Humedad']),
                dcc.Graph(id='grafico-ext-temp-hum',figure=figExteriorTempHum,config={'displayModeBar': False})
            ], style={'width': '300px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})

            ############################################################################
            ###                                                                      ###
            ###     Grafica de los Maximos y Minimos de la Temperatura Exterior      ###
            ###                                                                      ###
            ############################################################################
        
            figExtTempMaxMin = go.Figure()
            y1 = VectorExtTempHum[0];   y2 = VectorExtTempHum[1];   y3 = VectorExtTempHum[2]; x = list(range(len(VectorExtTempHum[0])))
            figExtTempMaxMin.add_trace(go.Scatter(x=x, y=y3,mode='lines',line=dict(color='#45020E'),opacity=0.4,name='Minimos °C'))
            figExtTempMaxMin.add_trace(go.Scatter(x=x, y=y1,mode='lines',line=dict(color='#9D061F'),opacity=0.4,name='Temperatura °C'))
            figExtTempMaxMin.add_trace(go.Scatter(x=x, y=y2,mode='lines',line=dict(color='#710416'),opacity=0.4,name='Maximos °C'))
            XlimInf = x[0]; XlimSup = x[len(x)-1];  YlimInf = Stats.DatoMinimoVector(y3); YlimSup = Stats.DatoMaximoVector(y2);
            tickvals_x = [XlimInf + (i * 0.1 * (XlimSup - XlimInf)) for i in range(11)]
            ticktext_x = [f'{val:.0f}' for val in tickvals_x]
            figExtTempMaxMin.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    range=[XlimInf, XlimSup],tickvals=tickvals_x,ticktext=ticktext_x,tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                yaxis=dict(range=[YlimInf - 0.5, YlimSup + 0.5],tickvals=[YlimInf, YlimSup],ticktext=[f'{YlimInf:.0f}°C', f'{YlimSup:.0f}°C'],
                    tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                margin=dict(l=40, r=40, t=20, b=40),showlegend=False,width=420,height=320
            )
            BloqueExtTempMaxMin = html.Div([
                html.Label(id='input-ext-temp-max-min',style={'color': "#000000", 'fontSize': '16px'}, children=['Maximos y minimos de la Temperatura °C']),
                dcc.Graph(id='grafico-ext-temp-max-min',figure=figExtTempMaxMin,config={'displayModeBar': True})   
            ], style={'width': '440px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
    
            ##########################################################################
            ###                                                                    ###
            ###     Grafica de los Maximos y Minimos de la Humedades Exterior      ###
            ###                                                                    ###
            ##########################################################################

            figExtHumMaxMin = go.Figure()
            y1 = VectorExtTempHum[3];   y2 = VectorExtTempHum[4];   y3 = VectorExtTempHum[5];  x = list(range(len(VectorExtTempHum[3])))
            figExtHumMaxMin.add_trace(go.Scatter(x=x, y=y3,mode='lines',line=dict(color='#120047'),opacity=0.4,name='Minimos (%)'))
            figExtHumMaxMin.add_trace(go.Scatter(x=x, y=y1,mode='lines',line=dict(color='#2900A1'),opacity=0.4,name='Humedad (%)'))
            figExtHumMaxMin.add_trace(go.Scatter(x=x, y=y2,mode='lines',line=dict(color='#1D0075'),opacity=0.4,name='Maximos (%)'))
            XlimInf = x[0]; XlimSup = x[len(x)-1];  YlimInf = Stats.DatoMinimoVector(y3); YlimSup = Stats.DatoMaximoVector(y2);
            tickvals_x = [XlimInf + (i * 0.1 * (XlimSup - XlimInf)) for i in range(11)]
            ticktext_x = [f'{val:.0f}' for val in tickvals_x]
            figExtHumMaxMin.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    range=[XlimInf, XlimSup],tickvals=tickvals_x,ticktext=ticktext_x,tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                yaxis=dict(range=[YlimInf - 0.5, YlimSup + 0.5],tickvals=[YlimInf, YlimSup],ticktext=[f'{YlimInf:.0f}%', f'{YlimSup:.0f}%'],
                    tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                margin=dict(l=40, r=40, t=20, b=40),showlegend=False,width=420,height=320
            )
            BloqueExtHumMaxMin = html.Div([
                html.Label(id='input-ext-hum-max-min',style={'color': "#000000", 'fontSize': '16px'}, children=['Maximos y minimos de la Humeadad %']),
                dcc.Graph(id='grafico-ext-hum-max-min',figure=figExtHumMaxMin,config={'displayModeBar': True})   
            ], style={'width': '440px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
    
            ######################################################
            ###                                                ###
            ###     Grafica de medias del Rocio y Humedad      ###
            ###                                                ###
            ######################################################

            IndiceBarrasDobleAxial = ["Dew Point","Wet Bulb"]
            figExtDewWetM = go.Figure()
            figExtDewWetM.add_trace(go.Bar(x=[IndiceBarrasDobleAxial[0]],y=[VectorExtDewWetM[0]],
                name='DewPoint',marker=dict(color='#08F7FF',line=dict(color='#009EA3', width=6)),
                opacity=0.9,text=[f"{VectorExtDewWetM[0]:.1f}°C"],
                textposition='outside',textfont=dict(color="#009EA3", size=12, family='sans-serif')
            ))
            figExtDewWetM.add_trace(go.Bar(x=[IndiceBarrasDobleAxial[1]],y=[VectorExtDewWetM[1]],
                name='WetBulb',marker=dict(color='#1266B8',line=dict(color="#0B3B6B", width=6)),
                opacity=0.9,text=[f"{VectorExtDewWetM[1]:.1f}%"],
                textposition='outside',textfont=dict(color="#0B3B6B", size=12, family='sans-serif')
            ))
            figExtDewWetM.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    title=dict(text="Punto de Rocio Exterior | Bulbo Húmedo",font=dict(color="#000000", size=16)),
                    tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                yaxis=dict(
                    title=dict(text='Exteriores',font=dict(color="#000000", size=16)),range=[0, 35],
                    tickvals=[0, 5, 10, 15, 20, 25, 30, 35],ticktext=["0°C", "5°C", "10°C", "15°C", "20°C", "25°C", "30°C", "35°C"],
                    tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                margin=dict(l=60, r=60, t=30, b=60),showlegend=False,width=360,height=320
            )
            BloqueExtDewWetM = html.Div([
                html.Label(id='input-titulo-dew-max-min-ext',style={'color': "#000000", 'fontSize': '16px'},children=['Punto de Rocio y Bulbo Humedo']),
                dcc.Graph(id='grafico-dew-max-min-ext',figure=figExtDewWetM,config={'displayModeBar': False})
            ], style={'width': '380px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})

            ####################################################################
            ###                                                              ###
            ###     Grafica de los Maximos y Minimos del Punto de Rocio      ###
            ###                                                              ###
            ####################################################################
    
            figExtDewMaxMin = go.Figure()
            y1 = VectorExtDewWet[0];   y2 = VectorExtDewWet[1];   y3 = VectorExtDewWet[2];  x = list(range(len(VectorExtDewWet[0])))
            figExtDewMaxMin.add_trace(go.Scatter(x=x, y=y3,mode='lines',line=dict(color='#33059E'),opacity=0.4,name='Minimos °C'))
            figExtDewMaxMin.add_trace(go.Scatter(x=x, y=y1,mode='lines',line=dict(color='#6F34F9'),opacity=0.4,name='Punto de Rocio °C'))
            figExtDewMaxMin.add_trace(go.Scatter(x=x, y=y2,mode='lines',line=dict(color='#4707DE'),opacity=0.4,name='Maximos °C'))
            XlimInf = x[0]; XlimSup = x[len(x)-1];  YlimInf = Stats.DatoMinimoVector(y3); YlimSup = Stats.DatoMaximoVector(y2);
            tickvals_x = [XlimInf + (i * 0.1 * (XlimSup - XlimInf)) for i in range(11)]
            ticktext_x = [f'{val:.0f}' for val in tickvals_x]
            figExtDewMaxMin.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    range=[XlimInf, XlimSup],tickvals=tickvals_x,ticktext=ticktext_x,tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                yaxis=dict(range=[YlimInf - 0.5, YlimSup + 0.5],tickvals=[YlimInf, YlimSup],ticktext=[f'{YlimInf:.0f}%', f'{YlimSup:.0f}%'],
                    tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                margin=dict(l=40, r=40, t=20, b=40),showlegend=False,width=420,height=320
            )
            BloqueExtDewMaxMin = html.Div([
                html.Label(id='input-titulo-dew-max-min-ext',style={'color': "#000000", 'fontSize': '16px'}, children=['Maximos y minimos del Punto de Rocio °C']),
                dcc.Graph(id='grafico-dew-max-min-ext',figure=figExtDewMaxMin,config={'displayModeBar': True})   
            ], style={'width': '440px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
    
            #################################################################
            ###                                                           ###
            ###     Grafica de los Maximos y Minimos del Bulbo Húmedo     ###
            ###                                                           ###
            #################################################################
    
            figExtDewMaxMin = go.Figure()
            y1 = VectorExtDewWet[3];    y2 = VectorExtDewWet[4];    y3 = VectorExtDewWet[5];  x = list(range(len(VectorExtDewWet[3])))
            figExtDewMaxMin.add_trace(go.Scatter(x=x, y=y3,mode='lines',line=dict(color='#6A0472'),opacity=0.4,name='Minimos °C'))
            figExtDewMaxMin.add_trace(go.Scatter(x=x, y=y1,mode='lines',line=dict(color='#D007DE'),opacity=0.4,name='Bulbo Húmedo °C'))
            figExtDewMaxMin.add_trace(go.Scatter(x=x, y=y2,mode='lines',line=dict(color='#94059E'),opacity=0.4,name='Maximos °C'))
            XlimInf = x[0]; XlimSup = x[len(x)-1];  YlimInf = Stats.DatoMinimoVector(y3); YlimSup = Stats.DatoMaximoVector(y2);
            tickvals_x = [XlimInf + (i * 0.1 * (XlimSup - XlimInf)) for i in range(11)]
            ticktext_x = [f'{val:.0f}' for val in tickvals_x]
            figExtDewMaxMin.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    range=[XlimInf, XlimSup],tickvals=tickvals_x,ticktext=ticktext_x,tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                yaxis=dict(range=[YlimInf - 0.5, YlimSup + 0.5],tickvals=[YlimInf, YlimSup],ticktext=[f'{YlimInf:.0f}%', f'{YlimSup:.0f}%'],
                    tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                margin=dict(l=40, r=40, t=20, b=40),showlegend=False,width=420,height=320
            )
            BloqueExtWetMaxMin = html.Div([
                html.Label(id='input-titulo-ext-wet-max-min',style={'color': "#000000", 'fontSize': '16px'}, children=['Maximos y minimos Bulbo Húmedo °C']),
                dcc.Graph(id='grafico-ext-wet-max-min',figure=figExtDewMaxMin,config={'displayModeBar': True})   
            ], style={'width': '440px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
    
            ###########################
            ###                     ###
            ###     Histogramas     ###
            ###                     ###
            ###########################
    
            #Histograma de temperatura exterior
            figHistExtTemp, x1HistExtTemp = plt.subplots(figsize=(10, 6));  y1 = VectorExtTempHum[0];
            Media1,VarianzaInsesgadaExtTemp,Varianza1,DesviacionExtTempNM,DatoMaxExtTemp,IndiceMaxExtTemp,DatoMinExtTemp,IndiceMinExtTemp,DatoModa1 = Curva.DatosHTML(y1)
            Stats.timsort(y1);      MedianaExtTemp = Stats.MedianaVector(y1);
            DesviacionExtTemp = Stats.DesviacionNewton(VarianzaInsesgadaExtTemp);
            Pearson1, r1 = Curva.RegresionLinealHTML(y1, VarianzaInsesgadaExtTemp)
            PercExtTemp = Stats.Percentil(y1, Percentiles);
            figHistExtTemp.patch.set_alpha(0.0);  x1HistExtTemp.patch.set_alpha(0.0);
            XlimInf2 = y1[0];    XlimSup2 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
            x1HistExtTemp.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = '#91122B',color ="#E84163",linewidth=4.0, alpha=0.6)
            x1HistExtTemp.set_xticks([XlimInf2,PercExtTemp[0],PercExtTemp[1],PercExtTemp[2],XlimSup2])
            x1HistExtTemp.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtTemp[0]:.0f}°C',f'{PercExtTemp[1]:.0f}°C',f'{PercExtTemp[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color="#000000", fontsize=14, fontname=fuente)
            x1HistExtTemp.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercExtTemp,ColorPerc):
                x1HistExtTemp.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistExtTemp = io.BytesIO()
            plt.savefig(bufHistExtTemp, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistExtTemp)
            src_hist_ext_temp = f"data:image/png;base64,{base64.b64encode(bufHistExtTemp.getvalue()).decode('utf-8')}"
            BloqueHistExteriorTemp = html.Div([
                html.Img(src=src_hist_ext_temp, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ext-temp',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Temperatura °C']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{Media1:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaExtTemp:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaExtTemp:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionExtTemp:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza1:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionExtTempNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha: {Fechas[IndiceMaxExtTemp + Pos1]}',f', : {Fechas[IndiceMinExtTemp + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxExtTemp:.0f}%',f',: {DatoMinExtTemp:.0f}%',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa1:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Bulbo Húmedo: CD:{Pearson1:.4f}',f',CC:{r1:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercExtTemp[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtTemp[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtTemp[2]:.0f}°C'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma de humedad exterior
            figHistExtHum, x2HistExtHum = plt.subplots(figsize=(10, 6));    y2 = VectorExtTempHum[3];
            Media2,VarianzaInsesgadaExtHum,Varianza2,DesviacionExtHumNM,DatoMaxExtHum,IndiceMaxExtHum,DatoMinExtHum,IndiceMinExtHum,DatoModa2 = Curva.DatosHTML(y2)
            Stats.timsort(y2);      MedianaExtHum = Stats.MedianaVector(y2);
            DesviacionExtHum = Stats.DesviacionNewton(VarianzaInsesgadaExtHum);
            Pearson2, r2 = Curva.RegresionLinealHTML(y2, VarianzaInsesgadaExtHum)
            PercExtHum = Stats.Percentil(y2, Percentiles);
            figHistExtHum.patch.set_alpha(0.0);  x2HistExtHum.patch.set_alpha(0.0);
            XlimInf2 = y2[0];    XlimSup2 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(len(y2) - 1))
            x2HistExtHum.hist(y2, bins=Rango2,rwidth = 1.2, edgecolor = '#060047',color ="#1B08FF",linewidth=4.0, alpha=0.6)
            x2HistExtHum.set_xticks([XlimInf2,PercExtHum[0],PercExtHum[1],PercExtHum[2],XlimSup2])
            x2HistExtHum.set_xticklabels([f'{XlimInf2:.2f}%',f'{PercExtHum[0]:.0f}%',f'{PercExtHum[1]:.0f}%',f'{PercExtHum[2]:.0f}%',f'{XlimSup2:.2f}%'], color="#000000", fontsize=14, fontname=fuente)
            x2HistExtHum.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercExtHum,ColorPerc):
                x2HistExtHum.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistExtTemp = io.BytesIO()
            plt.savefig(bufHistExtTemp, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistExtHum)
            src_hist_ext_hum = f"data:image/png;base64,{base64.b64encode(bufHistExtTemp.getvalue()).decode('utf-8')}"
            BloqueHistExteriorHum = html.Div([
                html.Img(src=src_hist_ext_hum, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ext-hum',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Humedad (%)']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{Media2:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaExtHum:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaExtHum:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionExtHum:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza2:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionExtHumNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxExtHum + Pos1]}',f', : {Fechas[IndiceMinExtHum + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxExtHum:.0f}%',f',: {DatoMinExtHum:.0f}%',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa2:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para Maximas: CD:{Pearson2:.4f}',f',CC:{r2:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercExtHum[0]:.0f}%',f'\tP{Percentiles[1]}: {PercExtHum[1]:.0f}%',f'\tP{Percentiles[2]}: {PercExtHum[2]:.0f}%'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histrograma Temperaturas exteriores
            y2 = VectorExtTempHum[1];  y3 = VectorExtTempHum[2]
            Media2,VarianzaInsesgadaExtTempMax,Varianza2,DesviacionExtTempMaxNM,DatoMaxExtTempMax,IndiceMaxExtTempMax,DatoMinExtTempMax,IndiceMinExtTempMax,DatoModa2 = Curva.DatosHTML(y2)
            Media3,VarianzaInsesgadaExtTempMin,Varianza3,DesviacionExtTempMinNM,DatoMaxExtTempMin,IndiceMaxExtTempMin,DatoMinExtTempMin,IndiceMinExtTempMin,DatoModa3 = Curva.DatosHTML(y3)
            Stats.timsort(y2);                      Stats.timsort(y3);
            Mediana2 = Stats.MedianaVector(y2);     Mediana3 = Stats.MedianaVector(y3);
            DesviacionExtTempMax = Stats.DesviacionNewton(VarianzaInsesgadaExtTempMax);
            DesviacionExtTempMin = Stats.DesviacionNewton(VarianzaInsesgadaExtTempMin);
            Pearson2, r2 = Curva.RegresionLinealHTML(y2, VarianzaInsesgadaExtTempMax)
            Pearson3, r3 = Curva.RegresionLinealHTML(y3, VarianzaInsesgadaExtTempMin)
            PercExtTempMax = Stats.Percentil(y2, Percentiles);
            PercExtTempMin = Stats.Percentil(y3, Percentiles);
            figHistExtTempMaxMin, xHistExtTempMaxMin = plt.subplots(figsize=(10, 6));
            figHistExtTempMaxMin.patch.set_alpha(0.0);  xHistExtTempMaxMin.patch.set_alpha(0.0);
            XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(len(y2) - 1))
            xHistExtTempMaxMin.hist(y2, bins=Rango,rwidth = 1.2, color = '#9D061F',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistExtTempMaxMin.hist(y3, bins=Rango,rwidth = 1.2, color = '#45020E',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistExtTempMaxMin.set_xticks([XlimInf2,PercExtTempMax[0],PercExtTempMax[1],PercExtTempMax[2],PercExtTempMin[0],PercExtTempMin[1],PercExtTempMin[2],XlimSup2])
            xHistExtTempMaxMin.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtTempMax[0]:.0f}°C',f'{PercExtTempMax[1]:.0f}°C',f'{PercExtTempMax[2]:.0f}°C',f'{PercExtTempMin[0]:.0f}°C',f'{PercExtTempMin[1]:.0f}°C',f'{PercExtTempMin[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color="#000000", fontsize=14, fontname=fuente)
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
                html.Img(src=src_hist_ext_temp_max_min, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ext-temp-max-min',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Temperaturas °C']),
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
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxExtTempMax + Pos1]}',f', : {Fechas[IndiceMinExtTempMax + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxExtTempMax:.0f}°C',f',: {DatoMinExtTempMax:.0f}°C',html.Br(),
                    f'Fecha Minimos: {Fechas[IndiceMaxExtTempMin + Pos1]}',f', : {Fechas[IndiceMinExtTempMin + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxExtTempMin:.0f}°C',f',: {DatoMinExtTempMin:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para maximas: {DatoModa2:.0f}',f'\tPara Minimos: {DatoModa3:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para Maximas: CD:{Pearson2:.4f}',f',CC:{r2:.4f}',html.Br(),
                    f'Para Minimas: CD:{Pearson3:.4f}',f',CC:{r3:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Maximas: P{Percentiles[0]}: {PercExtTempMax[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtTempMax[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtTempMax[2]:.0f}°C',html.Br(),
                    f'Minimas: P{Percentiles[0]}: {PercExtTempMin[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtTempMin[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtTempMin[2]:.0f}°C'
                ],style={'textAlign': 'center'})  
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histrograma Humedades
            y2 = VectorExtTempHum[4];  y3 = VectorExtTempHum[5]
            Media2,VarianzaInsesgadaExtHumMax,Varianza2,DesviacionExtHumMaxNM,DatoMaxExtHumMax,IndiceMaxExtHumMax,DatoMinExtHumMax,IndiceMinExtHumMax,DatoModa2 = Curva.DatosHTML(y2)
            Media3,VarianzaInsesgadaExtHumMin,Varianza3,DesviacionExtHumMinNM,DatoMaxExtHumMin,IndiceMaxExtHumMin,DatoMinExtHumMin,IndiceMinExtHumMin,DatoModa3 = Curva.DatosHTML(y3)
            Stats.timsort(y2);                      Stats.timsort(y3);
            Mediana2 = Stats.MedianaVector(y2);     Mediana3 = Stats.MedianaVector(y3);
            DesviacionExtHumMax = Stats.DesviacionNewton(VarianzaInsesgadaExtHumMax);
            DesviacionExtHumMin = Stats.DesviacionNewton(VarianzaInsesgadaExtHumMin);
            Pearson2, r2 = Curva.RegresionLinealHTML(y2, VarianzaInsesgadaExtHumMax)
            Pearson3, r3 = Curva.RegresionLinealHTML(y3, VarianzaInsesgadaExtHumMin)
            PercExtHumMax = Stats.Percentil(y2, Percentiles);
            PercExtHumMin = Stats.Percentil(y3, Percentiles);
            figHistExtHumMaxMin, xHistExtHumMaxMin = plt.subplots(figsize=(10, 6));
            figHistExtHumMaxMin.patch.set_alpha(0.0);  xHistExtHumMaxMin.patch.set_alpha(0.0);
            XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(len(y2) - 1));
            xHistExtHumMaxMin.hist(y2, bins=Rango,rwidth = 1.2, color = '#2900A1',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistExtHumMaxMin.hist(y3, bins=Rango,rwidth = 1.2, color = '#120047',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistExtHumMaxMin.set_xticks([XlimInf2,PercExtHumMax[0],PercExtHumMax[1],PercExtHumMax[2],PercExtHumMin[0],PercExtHumMin[1],PercExtHumMin[2],XlimSup2])
            xHistExtHumMaxMin.set_xticklabels([f'{XlimInf2:.2f} %',f'{PercExtHumMax[0]:.0f}°C',f'{PercExtHumMax[1]:.0f}°C',f'{PercExtHumMax[2]:.0f}°C',f'{PercExtHumMin[0]:.0f}°C',f'{PercExtHumMin[1]:.0f}°C',f'{PercExtHumMin[2]:.0f}°C',f'{XlimSup2:.2f} %'], color="#000000", fontsize=14, fontname=fuente)
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
                html.Img(src=src_hist_ext_hum_max_min, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ext-hum-max-min',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Humedades (%)']),
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
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxExtHumMax + Pos1]}',f', : {Fechas[IndiceMinExtHumMax + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxExtHumMax:.0f}%',f',: {DatoMinExtHumMax:.0f}%',html.Br(),
                    f'Fecha Minimos: {Fechas[IndiceMaxExtHumMin + Pos1]}',f', : {Fechas[IndiceMinExtHumMin + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxExtHumMin:.0f}%',f',: {DatoMinExtHumMin:.0f}%',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para maximas: {DatoModa2:.0f}',f'\tPara Minimos: {DatoModa3:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para Maximas: CD:{Pearson2:.4f}',f',CC:{r2:.4f}',html.Br(),
                    f'Para Minimas: CD:{Pearson3:.4f}',f',CC:{r3:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Maximas: P{Percentiles[0]}: {PercExtHumMax[0]:.0f}%',f'\tP{Percentiles[1]}: {PercExtHumMax[1]:.0f}%',f'\tP{Percentiles[2]}: {PercExtHumMax[2]:.0f}%',html.Br(),
                    f'Minimas: P{Percentiles[0]}: {PercExtHumMin[0]:.0f}%',f'\tP{Percentiles[1]}: {PercExtHumMin[1]:.0f}%',f'\tP{Percentiles[2]}: {PercExtHumMin[2]:.0f}%'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma de punto de rocio
            figHistExtD, x1HistExtD = plt.subplots(figsize=(10, 6));        y1 = VectorExtDewWet[0];
            Media1,VarianzaInsesgadaExtD,Varianza1,DesviacionExtDNM,DatoMaxExtDMax,IndiceMaxExtDMax,DatoMinExtDMax,IndiceMinExtDMax,DatoModa1 = Curva.DatosHTML(y1)
            Stats.timsort(y1);  DatoModa1 = Stats.ModaVectorValor(y1); MedianaExtD = Stats.MedianaVector(y1);
            DesviacionExtD = Stats.DesviacionNewton(VarianzaInsesgadaExtD);
            Pearson1, r1 = Curva.RegresionLinealHTML(y1, VarianzaInsesgadaExtD)
            PercExtD = Stats.Percentil(y1, Percentiles);
            figHistExtD.patch.set_alpha(0.0);  x1HistExtD.patch.set_alpha(0.0);
            XlimInf2 = y1[0];    XlimSup2 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
            x1HistExtD.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = '#0A7563',color ="#00DBB7",linewidth=4.0, alpha=0.6)
            x1HistExtD.set_xticks([XlimInf2,PercExtD[0],PercExtD[1],PercExtD[2],XlimSup2])
            x1HistExtD.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtD[0]:.0f}°C',f'{PercExtD[1]:.0f}°C',f'{PercExtD[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color="#000000", fontsize=14, fontname=fuente)
            x1HistExtD.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercExtD,ColorPerc):
                x1HistExtD.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistExtD = io.BytesIO()
            plt.savefig(bufHistExtD, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistExtD)
            src_hist_ext_d = f"data:image/png;base64,{base64.b64encode(bufHistExtD.getvalue()).decode('utf-8')}"
            BloqueHistExteriorDew = html.Div([
                html.Img(src=src_hist_ext_d, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ext-d',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Punto de Rocio °C']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{Media1:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaExtD:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaExtD:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionExtD:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza1:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionExtDNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxExtDMax + Pos1]}',f', : {Fechas[IndiceMinExtDMax + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxExtDMax:.0f}°C',f',: {DatoMinExtDMax:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa1:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Bulbo Húmedo: CD:{Pearson1:.4f}',f',CC:{r1:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercExtD[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtD[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtD[2]:.0f}°C'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma de bulbo húmedo
            figHistExtW, x1HistExtW = plt.subplots(figsize=(10, 6));        y2 = VectorExtDewWet[3];
            Media2,VarianzaInsesgadaExtW,Varianza2,DesviacionExtWNM,DatoMaxExtWMax,IndiceMaxExtWMax,DatoMinExtWMax,IndiceMinExtWMax,DatoModa2 = Curva.DatosHTML(y2)
            Stats.timsort(y2);  MedianaExtW = Stats.MedianaVector(y2);
            DesviacionExtW = Stats.DesviacionNewton(VarianzaInsesgadaExtW);
            Pearson2, r2 = Curva.RegresionLinealHTML(y2, VarianzaInsesgadaExtW)
            PercExtW = Stats.Percentil(y2, Percentiles);
            figHistExtW.patch.set_alpha(0.0);  x1HistExtW.patch.set_alpha(0.0);
            XlimInf2 = y2[0];    XlimSup2 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(len(y2) - 1))
            x1HistExtW.hist(y2, bins=Rango2,rwidth = 1.2, edgecolor = '#0C4574',color ="#008CFF",linewidth=4.0, alpha=0.6)
            x1HistExtW.set_xticks([XlimInf2,PercExtW[0],PercExtW[1],PercExtW[2],XlimSup2])
            x1HistExtW.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtW[0]:.0f}°C',f'{PercExtW[1]:.0f}°C',f'{PercExtW[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color="#000000", fontsize=14, fontname=fuente)
            x1HistExtW.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercExtW,ColorPerc):
                x1HistExtW.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistExtW = io.BytesIO()
            plt.savefig(bufHistExtW, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistExtW)
            src_hist_ext_w = f"data:image/png;base64,{base64.b64encode(bufHistExtW.getvalue()).decode('utf-8')}"
            BloqueHistExteriorWet = html.Div([
                html.Img(src=src_hist_ext_w, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ext-w',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Bulbo Húmedo °C']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{Media2:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaExtW:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaExtW:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionExtW:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza2:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionExtWNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxExtWMax + Pos1]}',f', : {Fechas[IndiceMinExtWMax + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxExtWMax:.0f}°C',f',: {DatoMinExtWMax:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa2:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Bulbo Húmedo: CD:{Pearson2:.4f}',f',CC:{r2:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercExtW[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtW[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtW[2]:.0f}°C'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histrograma Punto de Rocio Maximos y Minimos exteriores
            y2 = VectorExtDewWet[1];  y3 = VectorExtDewWet[2]
            Media2,VarianzaInsesgadaExtDMax,Varianza2,DesviacionExtDMaxNM,DatoMaxExtDMax,IndiceMaxExtDMax,DatoMinExtDMax,IndiceMinExtDMax,DatoModa2 = Curva.DatosHTML(y2)
            Media3,VarianzaInsesgadaExtDMin,Varianza3,DesviacionExtDMinNM,DatoMaxExtDMin,IndiceMaxExtDMin,DatoMinExtDMin,IndiceMinExtDMin,DatoModa3 = Curva.DatosHTML(y3)
            Stats.timsort(y2);                      Stats.timsort(y3);
            Mediana2 = Stats.MedianaVector(y2);     Mediana3 = Stats.MedianaVector(y3);
            DesviacionExtDMax = Stats.DesviacionNewton(VarianzaInsesgadaExtDMax);
            DesviacionExtDMin = Stats.DesviacionNewton(VarianzaInsesgadaExtDMin);
            Pearson2, r2 = Curva.RegresionLinealHTML(y2, VarianzaInsesgadaExtDMax)
            Pearson3, r3 = Curva.RegresionLinealHTML(y3, VarianzaInsesgadaExtDMin)
            PercExtDMax = Stats.Percentil(y2, Percentiles);
            PercExtDMin = Stats.Percentil(y3, Percentiles);
            figHistExtDMaxMin, xHistExtDMaxMin = plt.subplots(figsize=(10, 6));
            figHistExtDMaxMin.patch.set_alpha(0.0);  xHistExtDMaxMin.patch.set_alpha(0.0);
            XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(len(y2) - 1))
            xHistExtDMaxMin.hist(y2, bins=Rango,rwidth = 1.2, color = "#33059E",linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistExtDMaxMin.hist(y3, bins=Rango,rwidth = 1.2, color = '#6F34F9',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistExtDMaxMin.set_xticks([XlimInf2,PercExtDMax[0],PercExtDMax[1],PercExtDMax[2],PercExtDMin[0],PercExtDMin[1],PercExtDMin[2],XlimSup2])
            xHistExtDMaxMin.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtDMax[0]:.0f}°C',f'{PercExtDMax[1]:.0f}°C',f'{PercExtDMax[2]:.0f}°C',f'{PercExtDMin[0]:.0f}°C',f'{PercExtDMin[1]:.0f}°C',f'{PercExtDMin[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color="#000000", fontsize=14, fontname=fuente)
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
                html.Img(src=src_hist_ext_dew_max_min, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ext-dew-max-min',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Maximos y Minimos Rocio °C']),
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
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxExtDMax + Pos1]}',f', : {Fechas[IndiceMinExtDMax + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxExtDMax:.0f}°C',f',: {DatoMinExtDMax:.0f}°C',html.Br(),
                    f'Fecha Minimos: {Fechas[IndiceMaxExtDMin + Pos1]}',f', : {Fechas[IndiceMinExtDMin + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxExtDMin:.0f}°C',f',: {DatoMinExtDMin:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para maximas: {DatoModa2:.0f}',f'\tPara Minimos: {DatoModa3:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para Maximas: CD:{Pearson2:.4f}',f',CC:{r2:.4f}',html.Br(),
                    f'Para Minimas: CD:{Pearson3:.4f}',f',CC:{r3:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Maximas: P{Percentiles[0]}: {PercExtDMax[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtDMax[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtDMax[2]:.0f}°C',html.Br(),
                    f'Minimas: P{Percentiles[0]}: {PercExtDMin[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtDMin[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtDMin[2]:.0f}°C'
                ],style={'textAlign': 'center'})  
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histrograma Bulbo Humedo Maximos y Minimos exteriores
            y2 = VectorExtDewWet[4];  y3 = VectorExtDewWet[5]
            Media2,VarianzaInsesgadaExtWMax,Varianza2,DesviacionExtWMaxNM,DatoMaxExtWMax,IndiceMaxExtWMax,DatoMinExtWMax,IndiceMinExtWMax,DatoModa2 = Curva.DatosHTML(y2)
            Media3,VarianzaInsesgadaExtWMin,Varianza3,DesviacionExtWMinNM,DatoMaxExtWMin,IndiceMaxExtWMin,DatoMinExtWMin,IndiceMinExtWMin,DatoModa3 = Curva.DatosHTML(y3)
            Stats.timsort(y2);                      Stats.timsort(y3);
            Mediana2 = Stats.MedianaVector(y2);     Mediana3 = Stats.MedianaVector(y3);
            DesviacionExtWMax = Stats.DesviacionNewton(VarianzaInsesgadaExtWMax);
            DesviacionExtWMin = Stats.DesviacionNewton(VarianzaInsesgadaExtWMin);
            Pearson2, r2 = Curva.RegresionLinealHTML(y2, VarianzaInsesgadaExtWMax)
            Pearson3, r3 = Curva.RegresionLinealHTML(y3, VarianzaInsesgadaExtWMin)
            PercExtWMax = Stats.Percentil(y2, Percentiles);
            PercExtWMin = Stats.Percentil(y3, Percentiles);
            figHistExtWMaxMin, xHistExtWMaxMin = plt.subplots(figsize=(10, 6));
            figHistExtWMaxMin.patch.set_alpha(0.0);  xHistExtWMaxMin.patch.set_alpha(0.0);
            XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(len(y2) - 1))
            xHistExtWMaxMin.hist(y2, bins=Rango,rwidth = 1.2, color = '#6A0472',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistExtWMaxMin.hist(y3, bins=Rango,rwidth = 1.2, color = '#D007DE',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistExtWMaxMin.set_xticks([XlimInf2,PercExtWMax[0],PercExtWMax[1],PercExtWMax[2],PercExtWMin[0],PercExtWMin[1],PercExtWMin[2],XlimSup2])
            xHistExtWMaxMin.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtWMax[0]:.0f}°C',f'{PercExtWMax[1]:.0f}°C',f'{PercExtWMax[2]:.0f}°C',f'{PercExtWMin[0]:.0f}°C',f'{PercExtWMin[1]:.0f}°C',f'{PercExtWMin[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color="#000000", fontsize=14, fontname=fuente)
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
                html.Img(src=src_hist_ext_wet_max_min, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ext-wet-max-min',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Maximos y Minimos Bulbo °C']),
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
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxExtWMax + Pos1]}',f', : {Fechas[IndiceMinExtWMax + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxExtWMax:.0f}°C',f',: {DatoMinExtWMax:.0f}°C',html.Br(),
                    f'Fecha Minimos: {Fechas[IndiceMaxExtWMin + Pos1]}',f', : {Fechas[IndiceMinExtWMin + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxExtWMin:.0f}°C',f',: {DatoMinExtWMin:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para maximas: {DatoModa2:.0f}',f'\tPara Minimos: {DatoModa3:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para Maximas: CD:{Pearson2:.4f}',f',CC:{r2:.4f}',html.Br(),
                    f'Para Minimas: CD:{Pearson3:.4f}',f',CC:{r3:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Maximas: P{Percentiles[0]}: {PercExtWMax[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtWMax[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtWMax[2]:.0f}°C',html.Br(),
                    f'Minimas: P{Percentiles[0]}: {PercExtWMin[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtWMin[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtWMin[2]:.0f}°C'
                ],style={'textAlign': 'center'})  
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            return BloqueExtTempHum,BloqueExtTempMaxMin,BloqueExtHumMaxMin, BloqueHistExteriorTemp,BloqueHistExteriorHum,BloqueHistExteriorTempMaxMin,BloqueHistExteriorHumMaxMin, BloqueExtDewWetM,BloqueExtDewMaxMin,BloqueExtWetMaxMin, BloqueHistExteriorDew,BloqueHistExteriorWet,BloqueHistExteriorDewMaxMin,BloqueHistExteriorWetMaxMin
        #Presiones
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

            IndiceBarrasPbar = [f"PbarMin",f"PbarProm",f"PbarMax"]
            figPbar = go.Figure()
            figPbar.add_trace(go.Bar(x=[IndiceBarrasPbar[0]],y=[VectorPbar[0]],
                name='Dew',marker=dict(color='#88D3C9',line=dict(color='#20564E', width=2.5)),
                opacity=0.9,text=[f"{VectorPbar[0]:.1f}mb"],textposition='outside',textfont=dict(color="#88D3C9", size=12, weight='bold')))
            figPbar.add_trace(go.Bar(x=[IndiceBarrasPbar[1]],y=[VectorPbar[1]],
                name='Wet',marker=dict(color='#57B1EB',line=dict(color='#204256', width=2.5)),
                opacity=0.9,text=[f"{VectorPbar[1]:.1f}mb"],textposition='outside',textfont=dict(color="#57B1EB", size=12, weight='bold')))
            figPbar.add_trace(go.Bar(x=[IndiceBarrasPbar[2]],y=[VectorPbar[2]],
                name='Heat',marker=dict(color='#E535A4',line=dict(color='#680D47', width=2.5)),
                opacity=0.9,text=[f"{VectorPbar[2]:.1f}mb"],textposition='outside',textfont=dict(color='#E535A4', size=12, weight='bold')))
            figPbar.update_layout(width=480,height=320,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(range=[950, 1150],tickvals=[950, 975, 1000, 1025, 1050, 1075, 1100, 1125, 1150],ticktext=['950mb', '975mb', '1000mb', '1025mb', '1050mb', '1075mb', '1100mb', '1125mb', '1150mb'],
                tickfont=dict(color="#000000", size=14),showgrid=False),
                xaxis=dict(tickfont=dict(color="#000000", size=11),showgrid=False),
                margin=dict(l=45, r=15, t=30, b=40),showlegend=False)
            BloquePbar = html.Div([
                html.Label(id='input-titulo-pbar-max-min',style={'color': "#000000", 'fontSize': '16px'}, children=["Maximos, Promedios y Minimos de la Presion mb"]),
                dcc.Graph(id='grafico-pbar-max-min',figure=figPbar,config={'displayModeBar': False},style={'margin': '0 auto', 'display': 'block'})
            ], style={'width': '500px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
    
            #############################################
            ###                                       ###
            ###         Grafica Pbar vs Pabs          ###
            ###                                       ###
            #############################################

            figPbarabs = go.Figure()
            y1 = VectorPbarabs[0]; y2 = VectorPbarabs[1];  x = list(range(len(VectorPbarabs[0])))
            figPbarabs.add_trace(go.Scatter(x=x, y=y2,mode='lines',line=dict(color='#EC067B'),opacity=0.4,name='P barometrica mb'))
            figPbarabs.add_trace(go.Scatter(x=x, y=y1,mode='lines',line=dict(color='#06EC75'),opacity=0.4,name='P absoluta mb'))
            XlimInf = x[0]; XlimSup = x[len(x)-1];  YlimInf = Stats.DatoMinimoVector(y1); YlimSup = Stats.DatoMaximoVector(y2);
            tickvals_x = [XlimInf + (i * 0.1 * (XlimSup - XlimInf)) for i in range(11)]
            ticktext_x = [f'{val:.0f}' for val in tickvals_x]
            figPbarabs.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    range=[XlimInf, XlimSup],tickvals=tickvals_x,ticktext=ticktext_x,tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                yaxis=dict(range=[YlimInf - 0.5, YlimSup + 0.5],tickvals=[YlimInf, YlimSup],ticktext=[f'{YlimInf:.0f}mb', f'{YlimSup:.0f}mb'],
                    tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                margin=dict(l=40, r=40, t=20, b=40),showlegend=False,width=480,height=320
            )
            BloquePbarabs = html.Div([
                html.Label(id='input-titulo-pbar-pabs',style={'color': "#000000", 'fontSize': '16px'}, children=['Presion Barometrica vs Presion Absoluta mb']),
                dcc.Graph(id='grafico-pbar-pabs',figure=figPbarabs,config={'displayModeBar': True})   
            ], style={'width': '500px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})

            #Histograma de presion barometrica
            figHisPbar, xHistPbar = plt.subplots(figsize=(10, 6));      y1 = VectorPbarabs[0];
            Media1,VarianzaInsesgadaPbar,Varianza1,DesviacionPbarNM,DatoMaxPbar,IndiceMaxPbar,DatoMinPbar,IndiceMinPbar,DatoModa1 = Curva.DatosHTML(y1)
            Stats.timsort(y1);      MedianaPbar = Stats.MedianaVector(y1);
            DesviacionPbar = Stats.DesviacionNewton(VarianzaInsesgadaPbar);
            Pearson1, r1 = Curva.RegresionLinealHTML(y1, VarianzaInsesgadaPbar)
            PercPbar = Stats.Percentil(y1, Percentiles);
            figHisPbar.patch.set_alpha(0.0);  xHistPbar.patch.set_alpha(0.0);
            XlimInf2 = y1[0];    XlimSup2 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
            xHistPbar.hist(y1, bins=Rango1, rwidth = 1.2, edgecolor = "#7C0E47",color ="#EC067B",linewidth=4.0, alpha=0.6)
            xHistPbar.set_xticks([XlimInf2,PercPbar[0],PercPbar[1],PercPbar[2],XlimSup2])
            xHistPbar.set_xticklabels([f'{XlimInf2:.2f}mb',f'{PercPbar[0]:.0f}mb',f'{PercPbar[1]:.0f}mb',f'{PercPbar[2]:.0f}mb',f'{XlimSup2:.2f}mb'], color="#000000", fontsize=14, fontname=fuente)
            xHistPbar.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercPbar,ColorPerc):
                xHistPbar.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistPbar = io.BytesIO()
            plt.savefig(bufHistPbar, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHisPbar)
            src_hist_p_bar = f"data:image/png;base64,{base64.b64encode(bufHistPbar.getvalue()).decode('utf-8')}"
            BloqueHistPBar = html.Div([
                html.Img(src=src_hist_p_bar, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_p-bar',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Presión barometrica mb']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{Media1:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaPbar:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaPbar:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionPbar:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza1:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionPbarNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxPbar + Pos1]}',f', : {Fechas[IndiceMinPbar + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxPbar:.0f}mb',f',: {DatoMinPbar:.0f}mb',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa1:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'P bar: CD:{Pearson1:.4f}',f',CC:{r1:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercPbar[0]:.0f}mb',f'\tP{Percentiles[1]}: {PercPbar[1]:.0f}mb',f'\tP{Percentiles[2]}: {PercPbar[2]:.0f}mb'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma de presion barometrica maxima
            figHisPbarMax, xHistPbarMax = plt.subplots(figsize=(10, 6));        y3 = VectorPbarMaxMin[0];
            Media3,VarianzaInsesgadaPbarMax,Varianza3,DesviacionPbarMaxNM,DatoMaxPbarMax,IndiceMaxPbarMax,DatoMinPbarMax,IndiceMinPbarMax,DatoModa3 = Curva.DatosHTML(y3)
            Stats.timsort(y3);      MedianaPbarMax = Stats.MedianaVector(y3);
            DesviacionPbarMax = Stats.DesviacionNewton(VarianzaInsesgadaPbarMax);
            Pearson3, r3 = Curva.RegresionLinealHTML(y3, VarianzaInsesgadaPbarMax)
            PercPbarMax = Stats.Percentil(y3, Percentiles);
            figHisPbarMax.patch.set_alpha(0.0);  xHistPbarMax.patch.set_alpha(0.0);
            XlimInf2 = y3[0];    XlimSup3 = y3[len(y3) - 1];  Rango3 = int(RegladeSturges(len(y3) - 1))
            xHistPbarMax.hist(y3, bins=Rango3, rwidth = 1.2, edgecolor = "black",color ="#7A8490",linewidth=4.0, alpha=0.6)
            xHistPbarMax.set_xticks([XlimInf2,PercPbarMax[0],PercPbarMax[1],PercPbarMax[2],XlimSup2])
            xHistPbarMax.set_xticklabels([f'{XlimInf2:.2f}mb',f'{PercPbarMax[0]:.0f}mb',f'{PercPbarMax[1]:.0f}mb',f'{PercPbarMax[2]:.0f}mb',f'{XlimSup2:.2f}mb'], color="#000000", fontsize=14, fontname=fuente)
            xHistPbarMax.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercPbarMax,ColorPerc):
                xHistPbarMax.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistPbarMax = io.BytesIO()
            plt.savefig(bufHistPbarMax, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHisPbarMax)
            src_hist_p_bar_max = f"data:image/png;base64,{base64.b64encode(bufHistPbarMax.getvalue()).decode('utf-8')}"
            BloqueHistPBarMax = html.Div([
                html.Img(src=src_hist_p_bar_max, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_p-bar-max',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Presión barometrica maxima mb']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{Media3:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaPbarMax:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaPbarMax:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionPbarMax:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza3:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionPbarMaxNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxPbarMax + Pos1]}',f', : {Fechas[IndiceMinPbarMax + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxPbarMax:.0f}mb',f',: {DatoMinPbarMax:.0f}mb',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa3:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'P bar max: CD:{Pearson3:.4f}',f',CC:{r3:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercPbarMax[0]:.0f}mb',f'\tP{Percentiles[1]}: {PercPbarMax[1]:.0f}mb',f'\tP{Percentiles[2]}: {PercPbarMax[2]:.0f}mb'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma de presion barometrica minima
            figHisPbarMin, xHistPbarMin = plt.subplots(figsize=(10, 6));        y4 = VectorPbarMaxMin[1];
            Media4,VarianzaInsesgadaPbarMin,Varianza4,DesviacionPbarMinNM,DatoMaxPbarMin,IndiceMaxPbarMin,DatoMinPbarMin,IndiceMinPbarMin,DatoModa4 = Curva.DatosHTML(y4)
            Stats.timsort(y4);      MedianaPbarMin = Stats.MedianaVector(y4);
            DesviacionPbarMin = Stats.DesviacionNewton(VarianzaInsesgadaPbarMin);
            Pearson4, r4 = Curva.RegresionLinealHTML(y4, VarianzaInsesgadaPbarMin)
            PercPbarMin = Stats.Percentil(y4, Percentiles);
            figHisPbarMin.patch.set_alpha(0.0);  xHistPbarMin.patch.set_alpha(0.0);
            XlimInf2 = y4[0];    XlimSup2 = y4[len(y4) - 1];  Rango4 = int(RegladeSturges(len(y4) - 1))
            xHistPbarMin.hist(y4, bins=Rango4, rwidth = 1.2, edgecolor = "black",color ="#BBC7D1",linewidth=4.0, alpha=0.6)
            xHistPbarMin.set_xticks([XlimInf2,PercPbarMin[0],PercPbarMin[1],PercPbarMin[2],XlimSup2])
            xHistPbarMin.set_xticklabels([f'{XlimInf2:.2f}mb',f'{PercPbarMin[0]:.0f}mb',f'{PercPbarMin[1]:.0f}mb',f'{PercPbarMin[2]:.0f}mb',f'{XlimSup2:.2f}mb'], color="#000000", fontsize=14, fontname=fuente)
            xHistPbarMin.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercPbarMin,ColorPerc):
                xHistPbarMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistPbarMin = io.BytesIO()
            plt.savefig(bufHistPbarMin, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHisPbarMin)
            src_hist_p_bar_min = f"data:image/png;base64,{base64.b64encode(bufHistPbarMin.getvalue()).decode('utf-8')}"
            BloqueHistPBarMin = html.Div([
                html.Img(src=src_hist_p_bar_min, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_p-bar-min',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Presión barometrica minima mb']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{VectorPbar[2]:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaPbarMin:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaPbarMin:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionPbarMin:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza4:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionPbarMinNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxPbarMin + Pos1]}',f', : {Fechas[IndiceMinPbarMin + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxPbarMin:.0f}mb',f',: {DatoMinPbarMin:.0f}mb',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa4:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'P bar min: CD:{Pearson4:.4f}',f',CC:{r4:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercPbarMin[0]:.0f}mb',f'\tP{Percentiles[1]}: {PercPbarMin[1]:.0f}mb',f'\tP{Percentiles[2]}: {PercPbarMin[2]:.0f}mb'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma de presion absoluta
            figHisPabs, xHistPabs = plt.subplots(figsize=(10, 6));      y2 = VectorPbarabs[1];
            Media2,VarianzaInsesgadaPabs,Varianza2,DesviacionPabsNM,DatoMaxPabs,IndiceMaxPabs,DatoMinPabs,IndiceMinPabs,DatoModa2 = Curva.DatosHTML(y2)
            Stats.timsort(y2);      MedianaPabs = Stats.MedianaVector(y2);
            DesviacionPabs = Stats.DesviacionNewton(VarianzaInsesgadaPabs);
            Pearson2, r2 = Curva.RegresionLinealHTML(y2, VarianzaInsesgadaPabs)
            PercPabs = Stats.Percentil(y2, Percentiles);
            figHisPabs.patch.set_alpha(0.0);  xHistPabs.patch.set_alpha(0.0);
            XlimInf2 = y2[0];    XlimSup2 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(len(y2) - 1))
            xHistPabs.hist(y2, bins=Rango2, rwidth = 1.2, edgecolor = "#02552A",color ="#06EC75",linewidth=4.0, alpha=0.6)
            xHistPabs.set_xticks([XlimInf2,PercPabs[0],PercPabs[1],PercPabs[2],XlimSup2])
            xHistPabs.set_xticklabels([f'{XlimInf2:.2f}mb',f'{PercPabs[0]:.0f}mb',f'{PercPabs[1]:.0f}mb',f'{PercPabs[2]:.0f}mb',f'{XlimSup2:.2f}mb'], color="#000000", fontsize=14, fontname=fuente)
            xHistPabs.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercPabs,ColorPerc):
                xHistPabs.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistPabs = io.BytesIO()
            plt.savefig(bufHistPabs, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHisPabs)
            src_hist_p_abs = f"data:image/png;base64,{base64.b64encode(bufHistPabs.getvalue()).decode('utf-8')}"
            BloqueHistPAbs = html.Div([
                html.Img(src=src_hist_p_abs, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_p-bar',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Presion Absoluta mb']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{MediaPabs:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaPabs:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaPabs:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionPabs:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza2:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionPabsNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxPabs + Pos1]}',f', : {Fechas[IndiceMinPabs + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxPabs:.0f}mb',f',: {DatoMinPabs:.0f}mb',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa1:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'P abs: CD:{Pearson2:.4f}',f',CC:{r2:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercPbar[0]:.0f}mb',f'\tP{Percentiles[1]}: {PercPbar[1]:.0f}mb',f'\tP{Percentiles[2]}: {PercPbar[2]:.0f}mb'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            return BloquePbar,BloquePbarabs,None, BloqueHistPBar,BloqueHistPBarMax,BloqueHistPBarMin,BloqueHistPAbs, None,None,None, None,None,None,None
        #Viento y su direccion
        if opcion == "Vientos":
            print("Registro Viento y su direccion")
            #Indices
            i = AvgWindSpeed; Ante = HighWindDir;
            #Vectores
            VectorVelWind = [];
            Vector0_3 = [];    Vector3_6 = [];   Vector6_10 = [];   Vector10_13 = [];    Vector13_16 = [];   Vector16_32 = [];  Vector32 = [];
            VectorDirection = []
            vector8 = 0;
            plt.rcParams['axes.edgecolor'] = "#000000"    
            plt.rcParams['axes.linewidth'] = 3.0
            while(i <= Ante):
                #Datos de la fila del Mes seleccionado
                DatosFilas = df.iloc[Pos1:Pos2, i].tolist()
                #Datos de la columna del rango de filas
                Datos = [x.item() if hasattr(x, 'item') else x for x in DatosFilas]
                #Direcciones del grafico
                Direcciones = ['E','ENE','NE','NNE','N','NNW','NW','WNW','W','WSW','SW','SSW','S','SSE','SE','ESE']
                if(i == AvgWindSpeed):
                    Indice = list(range(0, len(Datos)))                             #Indice
                    Curva.InterpolacionLinealNoGraph(Datos, Indice, len(Datos))     #Verificacion de los datos
                    Datos = [float(i) for i in Datos]                               #Convertir Datos a float
                    VectorVelWind.append(Datos)                                     #Obtener los datos
                    i = i + 1;
                elif(i == PrevalentDir or i == AverageDir):
                    if(i == PrevalentDir):
                        Vector0_3,Vector3_6,Vector6_10,Vector10_13,Vector13_16,Vector16_32,Vector32,vector8 = DireccionesGrados(Datos,VectorVelWind[0])
                        VectorDirection.append(Vector0_3);  VectorDirection.append(Vector3_6);  VectorDirection.append(Vector6_10)
                        VectorDirection.append(Vector10_13);  VectorDirection.append(Vector13_16);  VectorDirection.append(Vector16_32);  VectorDirection.append(Vector32)
                    if(i == AverageDir):
                        Vector0_3,Vector3_6,Vector6_10,Vector10_13,Vector13_16,Vector16_32,Vector32,vector8 = DireccionesGrados(Datos,VectorVelWind[0])
                        VectorDirection.append(Vector0_3);  VectorDirection.append(Vector3_6);  VectorDirection.append(Vector6_10)
                        VectorDirection.append(Vector10_13);  VectorDirection.append(Vector13_16);  VectorDirection.append(Vector16_32);  VectorDirection.append(Vector32)
                    i = i + 1;
                elif(i == WindRun):
                    Indice = list(range(0, len(Datos)))                             #Indice
                    Curva.InterpolacionLinealNoGraph(Datos, Indice, len(Datos))     #Verificacion de los datos
                    Datos = [float(i) for i in Datos]                               #Convertir Datos a float
                    VectorVelWind.append(Datos)    
                    i = i + 1
                elif(i == HighWindSpeed):
                    Indice = list(range(0, len(Datos)))                             #Indice
                    Curva.InterpolacionLinealNoGraph(Datos, Indice, len(Datos))     #Verificacion de los datos
                    Datos = [float(i) for i in Datos]                               #Convertir Datos a float
                    VectorVelWind.append(Datos)                                     #Obtener los datos
                    i = i + 1
                elif(i == HighWindDir):
                    Vector0_3,Vector3_6,Vector6_10,Vector10_13,Vector13_16,Vector16_32,Vector32,vector8 = DireccionesGrados(Datos,VectorVelWind[2])
                    VectorDirection.append(Vector0_3);  VectorDirection.append(Vector3_6);  VectorDirection.append(Vector6_10)
                    VectorDirection.append(Vector10_13);  VectorDirection.append(Vector13_16);  VectorDirection.append(Vector16_32);  VectorDirection.append(Vector32)
                    i = i + 1;
            #Vector de "ceros"
            VectorBottom = [0] * 16
            p = log(0.8) / log(0.4)         # El 40% de los datos se mostrara en el 80% del grafico: (0.4)^p = 0.8  ->  p = log(0.8) / log(0.4)
            #Funcio transformacion a Logaritmica
            def EscalaRosa(ValorTotal, MaximoDelVector):
                Porcentaje = [y / MaximoDelVector for y in ValorTotal]
                Expresion = [y**p for y in Porcentaje]
                return Expresion
            #Etiquetas para el texto y Colores de las barras
            Etiquetas = ['0 - 3 km','3 - 6 km','6 - 10 km','10 - 13 km','13 - 16 km','16 - 32 km','32 > km']
            Colores = ["#046360", "#003A31",'#0070AD','#D4068A','#FFBA00','#FF5500','#0026FF']
            #Numeros del 0 a 2pi
            theta = np.linspace(0.0, 2*np.pi, 16, endpoint=False)
            #Ancho de las barras para simular triangulos
            Width = 2 * np.pi / 16
    
            ##############################################################
            ###                                                        ###
            ###     Grafica de la direccion de viento predominante     ###
            ###                                                        ###
            ##############################################################
    
            #Vectores Barras
            y1 = VectorDirection[0];    y2 = VectorDirection[1];    y3 = VectorDirection[2];
            y4 = VectorDirection[3];    y5 = VectorDirection[4];    y6 = VectorDirection[5];    y7 = VectorDirection[6];
            #Sumar las iteraciones de cada vector
            SumaVectores = [x1 + x2 + x3 + x4 + x5 + x6 + x7 for x1, x2, x3, x4, x5, x6, x7 in zip(y1, y2, y3, y4, y5, y6, y7)]
            MaximoVectores = Stats.DatoMaximoVector(SumaVectores)
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
            #Codificacion
            bufPrevWind = io.BytesIO() 
            plt.savefig(bufPrevWind, format="png", bbox_inches='tight', transparent=True)
            plt.close(figPrevWind)
            src_prev_wind = f"data:image/png;base64,{base64.b64encode(bufPrevWind.getvalue()).decode('utf-8')}"
            BloquePrevWind = html.Div([
                html.Label(
                    id='input-prev-wind',
                    style={'textAlign': 'center'},
                    children=[
                        'Direccion del viento prevalescente'
                        ]
                    ),
                html.Img(src=src_prev_wind, style={'width': '350px', 'height': '350px'})
                ], style={'width': '380px','height': '400px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            
            #Vector de "ceros"
            VectorBottom = [0] * 16
    
            ##########################################################
            ###                                                    ###
            ###     Grafica de la direccion de viento promedio     ###
            ###                                                    ###
            ##########################################################
    
            #Vectores Barras
            y1 = VectorDirection[7];    y2 = VectorDirection[8];    y3 = VectorDirection[9];
            y4 = VectorDirection[10];    y5 = VectorDirection[11];    y6 = VectorDirection[12];    y7 = VectorDirection[13];
            #Sumar las iteraciones de cada vector
            SumaVectores = [x1 + x2 + x3 + x4 + x5 + x6 + x7 for x1, x2, x3, x4, x5, x6, x7 in zip(y1, y2, y3, y4, y5, y6, y7)]
            MaximoVectores = Stats.DatoMaximoVector(SumaVectores)
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
            #Codificacion
            bufAvgWind = io.BytesIO() 
            plt.savefig(bufAvgWind, format="png", bbox_inches='tight', transparent=True)
            plt.close(figAvgWind)
            src_avg_wind = f"data:image/png;base64,{base64.b64encode(bufAvgWind.getvalue()).decode('utf-8')}"
            BloqueAvgWind = html.Div([
                html.Label(
                    style={'textAlign': 'center'},
                    children=[
                        'Direccion del viento promedio'
                        ]
                    ),
                html.Img(src=src_avg_wind, style={'width': '350px', 'height': '350px'})
                ], style={'width': '380px','height': '400px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
    
            #Vector de "ceros"
            VectorBottom = [0] * 16
    
            #############################################################
            ###                                                       ###
            ###     Grafica de la direccion de viento proveniente     ###
            ###                                                       ###
            #############################################################
    
            #Vectores Barras
            y1 = VectorDirection[14];    y2 = VectorDirection[15];    y3 = VectorDirection[16];
            y4 = VectorDirection[17];    y5 = VectorDirection[18];    y6 = VectorDirection[19];    y7 = VectorDirection[20];
            #Sumar las iteraciones de cada vector
            SumaVectores = [x1 + x2 + x3 + x4 + x5 + x6 + x7 for x1, x2, x3, x4, x5, x6, x7 in zip(y1, y2, y3, y4, y5, y6, y7)]
            MaximoVectores = Stats.DatoMaximoVector(SumaVectores)
            MatrizDatos = [y1, y2, y3, y4, y5, y6, y7]
            figProWind, xProWind = plt.subplots(subplot_kw={"projection": "polar"})
            xProWind.set_axisbelow(True)
            for PrevWindVector, Color in zip(MatrizDatos, Colores):
                VectorInf = EscalaRosa(VectorBottom, MaximoVectores)
                VectorBottom = [x1 + x2 for x1,x2 in zip(VectorBottom , PrevWindVector)]
                VectorSup = EscalaRosa(VectorBottom, MaximoVectores)
                VectorAltura = [y1 - y2 for y1,y2 in zip(VectorSup , VectorInf)]
                xProWind.bar(theta,VectorAltura,bottom=VectorInf, color = Color,width=Width, linewidth=2, edgecolor='k', alpha=0.9)
            xProWind.set_xticks(theta)
            xProWind.set_xticklabels(Direcciones)
            plt.ylim(0, 1.1)
            #Codificacion
            bufProWind = io.BytesIO() 
            plt.savefig(bufProWind, format="png", bbox_inches='tight', transparent=True)
            plt.close(figProWind)
            src_pro_wind = f"data:image/png;base64,{base64.b64encode(bufProWind.getvalue()).decode('utf-8')}"
            BloqueProWind = html.Div([
                html.Label(
                    style={'textAlign': 'center'},
                    children=[
                        'Direccion del viento proveniente'
                        ]
                    ),
                html.Img(src=src_pro_wind, style={'width': '350px', 'height': '350px'})
                ], style={'width': '380px','height': '400px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            BloqueWindText = html.Div(
                [
                html.Label(
                    id='input-label-prev-wind',
                    style={'textAlign': 'center'},
                    children=['Velocidad del Viento']
                ),
                html.Div(
                    [
                        html.P(style={"marginTop": "15px","fontSize": "14px","color": Colores[0],"fontFamily": "sans-serif",},children=[ '0 - 3 km/h']),
                        html.P(style={"marginTop": "15px","fontSize": "14px","color": Colores[1],"fontFamily": "sans-serif",},children=[ '3 - 6 km/h']),
                        html.P(style={"marginTop": "15px","fontSize": "14px","color": Colores[2],"fontFamily": "sans-serif",},children=[ '6 - 10 km/h']),
                        html.P(style={"marginTop": "15px","fontSize": "14px","color": Colores[3],"fontFamily": "sans-serif",},children=[ '10 - 13 km/h']),
                        html.P(style={"marginTop": "15px","fontSize": "14px","color": Colores[4],"fontFamily": "sans-serif",},children=[ '13 - 16 km/h']),
                        html.P(style={"marginTop": "15px","fontSize": "14px","color": Colores[5],"fontFamily": "sans-serif",},children=[ '16 - 32 km/h']),
                        html.P(style={"marginTop": "15px","fontSize": "14px","color": Colores[6],"fontFamily": "sans-serif",},children=[ '32 > km/h'])
                    ],
                    style={"width": "100%",'textAlign': 'center'}
                ),
            ], style={'width': '200px','height': '400px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
    
            ###########################
            ###                     ###
            ###     Histogramas     ###
            ###                     ###
            ###########################
    
            #Histograma de viento promedio
            figHistAvgSpd, xHistAvgSpd = plt.subplots(figsize=(10, 6));     y1 = VectorVelWind[0];
            Media1,VarianzaInsesgadaAvgSpd,Varianza1,DesviacionAvgSpdNM,DatoMaxAvgSpd,IndiceMaxAvgSpd,DatoMinAvgSpd,IndiceMinAvgSpd,DatoModa1 = Curva.DatosHTML(y1)
            Stats.timsort(y1);      MediaAvgSpd = Stats.MediaVector(y1); MedianaAvgSpd = Stats.MedianaVector(y1);
            DesviacionAvgSpd = Stats.DesviacionNewton(VarianzaInsesgadaAvgSpd);
            Pearson1, r1 = Curva.RegresionLinealHTML(y1, VarianzaInsesgadaAvgSpd)
            PercAvgSpd = Stats.Percentil(y1, Percentiles);
            figHistAvgSpd.patch.set_alpha(0.0);  xHistAvgSpd.patch.set_alpha(0.0);
            XlimInf2 = y1[0];    XlimSup2 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
            xHistAvgSpd.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = "#006C53",color ="#00B188",linewidth=4.0, alpha=0.6)
            xHistAvgSpd.set_xticks([XlimInf2,PercAvgSpd[0],PercAvgSpd[1],PercAvgSpd[2],XlimSup2])
            xHistAvgSpd.set_xticklabels([f'{XlimInf2:.2f}km/h',f'{PercAvgSpd[0]:.0f}km/h',f'{PercAvgSpd[1]:.0f}km/h',f'{PercAvgSpd[2]:.0f}km/h',f'{XlimSup2:.2f}km/h'], color="#000000", fontsize=14, fontname=fuente)
            xHistAvgSpd.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercAvgSpd,ColorPerc):
                xHistAvgSpd.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistAvgSpd = io.BytesIO()
            plt.savefig(bufHistAvgSpd, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistAvgSpd)
            src_hist_avg_spd = f"data:image/png;base64,{base64.b64encode(bufHistAvgSpd.getvalue()).decode('utf-8')}"
            BloqueHistAverageSpeed = html.Div([
                html.Img(src=src_hist_avg_spd, style={'width': '100%', 'height': '300px'}),
                html.Label(id='input-hist_avg-spd',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Velocidad promedio del viento km/h']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{MediaAvgSpd:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaAvgSpd:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaAvgSpd:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionAvgSpd:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza1:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionAvgSpdNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxAvgSpd + Pos1]}',f', : {Fechas[IndiceMinAvgSpd + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxAvgSpd:.0f}km/h',f',: {DatoMinAvgSpd:.0f}km/h',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa1:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Avg Speed: CD:{Pearson1:.4f}',f',CC:{r1:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercAvgSpd[0]:.0f}km/h',f'\tP{Percentiles[1]}: {PercAvgSpd[1]:.0f}km/h',f'\tP{Percentiles[2]}: {PercAvgSpd[2]:.0f}km/h'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma de la longitud de paso del viento
            figHistWindRun, xHistWindRun = plt.subplots(figsize=(10, 6));   y2 = VectorVelWind[1];
            MediaWindRun,VarianzaInsesgadaWindRun,Varianza2,DesviacionWindRunNM,DatoMaxWindRun,IndiceMaxWindRun,DatoMinWindRun,IndiceMinWindRun,DatoModa2 = Curva.DatosHTML(y2)
            Stats.timsort(y2);      MedianaWindRun = Stats.MedianaVector(y2);
            DesviacionWindRun = Stats.DesviacionNewton(VarianzaInsesgadaWindRun);
            Pearson2, r2 = Curva.RegresionLinealHTML(y2, VarianzaInsesgadaWindRun)
            PercWindRun = Stats.Percentil(y2, Percentiles);
            figHistWindRun.patch.set_alpha(0.0);  xHistWindRun.patch.set_alpha(0.0);
            XlimInf2 = y2[0];    XlimSup2 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(len(y2) - 1))
            xHistWindRun.hist(y2, bins=Rango2,rwidth = 1.2, edgecolor = '#060047',color ="#1B08FF",linewidth=4.0, alpha=0.6)
            xHistWindRun.set_xticks([XlimInf2,PercWindRun[0],PercWindRun[1],PercWindRun[2],XlimSup2])
            xHistWindRun.set_xticklabels([f'{XlimInf2:.2f}km',f'{PercWindRun[0]:.0f}km',f'{PercWindRun[1]:.0f}km',f'{PercWindRun[2]:.0f}km',f'{XlimSup2:.2f}km'], color="#000000", fontsize=14, fontname=fuente)
            xHistWindRun.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercWindRun,ColorPerc):
                xHistWindRun.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistWindRun = io.BytesIO()
            plt.savefig(bufHistWindRun, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistWindRun)
            src_hist_wind_run = f"data:image/png;base64,{base64.b64encode(bufHistWindRun.getvalue()).decode('utf-8')}"
            BloqueHistWindRun = html.Div([
                html.Img(src=src_hist_wind_run, style={'width': '100%', 'height': '300px'}),
                html.Label(id='input-hist_wind-run',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Longitud del paso de viento km']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{MediaWindRun:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaWindRun:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaWindRun:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionWindRun:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza2:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionWindRunNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxWindRun + Pos1]}',f', : {Fechas[IndiceMinWindRun + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxWindRun:.0f}km/h',f',: {DatoMinWindRun:.0f}km/h',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa2:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Run Wind: CD:{Pearson2:.4f}',f',CC:{r2:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercWindRun[0]:.0f}km',f'\tP{Percentiles[1]}: {PercWindRun[1]:.0f}km',f'\tP{Percentiles[2]}: {PercWindRun[2]:.0f}km'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma de vientos de alta velocidad
            figHistHighSpd, xHistHighSpd = plt.subplots(figsize=(10, 6));       y3 = VectorVelWind[2];
            MediaHighSpd,VarianzaInsesgadaHighSpd,Varianza3,DesviacionHighSpdNM,DatoMaxHighSpd,IndiceMaxHighSpd,DatoMinHighSpd,IndiceMinHighSpd,DatoModa3 = Curva.DatosHTML(y3)
            Stats.timsort(y3);      MedianaHighSpd = Stats.MedianaVector(y3);
            DesviacionHighSpd = Stats.DesviacionNewton(VarianzaInsesgadaHighSpd);
            Pearson3, r3 = Curva.RegresionLinealHTML(y3, VarianzaInsesgadaHighSpd)
            PercHighSpd = Stats.Percentil(y3, Percentiles);
            figHistHighSpd.patch.set_alpha(0.0);  xHistHighSpd.patch.set_alpha(0.0);
            XlimInf2 = y3[0];    XlimSup2 = y3[len(y3) - 1];  Rango3 = int(RegladeSturges(len(y3) - 1))
            xHistHighSpd.hist(y3, bins=Rango3,rwidth = 1.2, edgecolor = "#006C53",color ="#00B188",linewidth=4.0, alpha=0.6)
            xHistHighSpd.set_xticks([XlimInf2,PercHighSpd[0],PercHighSpd[1],PercHighSpd[2],XlimSup2])
            xHistHighSpd.set_xticklabels([f'{XlimInf2:.2f}km/h',f'{PercHighSpd[0]:.0f}km/h',f'{PercHighSpd[1]:.0f}km/h',f'{PercHighSpd[2]:.0f}km/h',f'{XlimSup2:.2f}km/h'], color="#000000", fontsize=14, fontname=fuente)
            xHistHighSpd.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercHighSpd,ColorPerc):
                xHistHighSpd.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistHighSpd = io.BytesIO()
            plt.savefig(bufHistHighSpd, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistHighSpd)
            src_hist_high_spd = f"data:image/png;base64,{base64.b64encode(bufHistHighSpd.getvalue()).decode('utf-8')}"
            BloqueHistHighWindSpeed = html.Div([
                html.Img(src=src_hist_high_spd, style={'width': '100%', 'height': '300px'}),
                html.Label(id='input-hist_avg-spd',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Velocidad maxima de la rafaga de viento km/h']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{MediaHighSpd:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaHighSpd:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaHighSpd:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionHighSpd:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza3:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionHighSpdNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximos: {Fechas[IndiceMaxHighSpd + Pos1]}',f', : {Fechas[IndiceMinHighSpd + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxHighSpd:.0f}km/h',f',: {DatoMinHighSpd:.0f}km/h',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa3:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'P abs: CD:{Pearson3:.4f}',f',CC:{r3:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercHighSpd[0]:.0f}km/h',f'\tP{Percentiles[1]}: {PercHighSpd[1]:.0f}km/h',f'\tP{Percentiles[2]}: {PercHighSpd[2]:.0f}km/h'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            return None,None,None, BloqueWindText,BloquePrevWind,BloqueAvgWind,BloqueProWind, BloqueHistAverageSpeed,BloqueHistWindRun,BloqueHistHighWindSpeed, None,None,None,None
        #Sensaciones termicas del ambiente
        if opcion == "Sensaciones":
            print("Sensaciones Termicas")
            VectorWindC = [];   VectorHeat = [];    VectorTWH = [];     VectorTHSW = [];
            i = WindChill;  Ante = MinimoTHSWIndex;
            while(i <= Ante):
                #Datos de la fila del Mes seleccionado
                DatosFilas = df.iloc[Pos1:Pos2, i].tolist()
                #Datos de la columna del rango de filas
                Datos = [x.item() if hasattr(x, 'item') else x for x in DatosFilas]
                Indice = list(range(0, len(Datos)))                             #Indice
                Curva.InterpolacionLinealNoGraph(Datos, Indice, len(Datos))     #Verificacion de los datos
                Datos = [float(i) for i in Datos]
                if(i == WindChill or i == MinimoWindChill):
                    VectorWindC.append(Datos)
                    i = i + 1;
                elif(i == HeatIndex or i == HighHeatIndex):
                    VectorHeat.append(Datos)
                    i = i + 1;
                elif(i == THWIndex or i == MaximoTHWIndex or i == MinimoTHWIndex):
                    VectorTWH.append(Datos)
                    i = i + 1;
                elif(i == THSWIndex or i == MaximoTHSWIndex or i == MinimoTHSWIndex):
                    VectorTHSW.append(Datos)
                    i = i + 1;
    
            ##########################################################
            ###                                                    ###
            ###     Grafica de barra de Wind, Heat, THW, THSW      ###
            ###                                                    ###
            ##########################################################

            MediaWind = Stats.MediaVector(VectorWindC[0]);  MediaHeat = Stats.MediaVector(VectorHeat[0]);
            MediaTHW = Stats.MediaVector(VectorTWH[0]);     MediaTHSW = Stats.MediaVector(VectorTHSW[0]);
            IndiceBarrasWHTT = [f"Wind Chill",f"Heat Index",f"THW",f"THSW"]
            figPbar = go.Figure()
            figPbar.add_trace(go.Bar(x=[IndiceBarrasWHTT[0]],y=[MediaWind],
                name='Wind',marker=dict(color='#00FFF7',line=dict(color='#00716E', width=2.5)),
                opacity=0.9,text=[f"{MediaWind:.2f}mb"],textposition='outside',textfont=dict(color="#00FFF7", size=12, weight='bold')))
            figPbar.add_trace(go.Bar(x=[IndiceBarrasWHTT[1]],y=[MediaHeat],
                name='Heat',marker=dict(color='#FF6F00',line=dict(color='#B04E04', width=2.5)),
                opacity=0.9,text=[f"{MediaHeat:.2f}mb"],textposition='outside',textfont=dict(color="#FF6F00", size=12, weight='bold')))
            figPbar.add_trace(go.Bar(x=[IndiceBarrasWHTT[2]],y=[MediaTHW],
                name='THW',marker=dict(color='#4F9BFF',line=dict(color='#083E83', width=2.5)),
                opacity=0.9,text=[f"{MediaTHW:.2f}mb"],textposition='outside',textfont=dict(color='#4F9BFF', size=12, weight='bold')))
            figPbar.add_trace(go.Bar(x=[IndiceBarrasWHTT[3]],y=[MediaTHSW],
                name='THSW',marker=dict(color='#9309D3',line=dict(color='#7A0DA6', width=2.5)),
                opacity=0.9,text=[f"{MediaTHSW:.2f}mb"],textposition='outside',textfont=dict(color='#9309D3', size=12, weight='bold')))
            figPbar.update_layout(width=560,height=320,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(range=[0, 40],tickvals=[0, 5, 10, 15, 20, 25, 30, 35, 40],ticktext=["0°C", "5°C", "10°C", "15°C", "20°C", "25°C", "30°C", "35°C", "40°C"],
                tickfont=dict(color="#000000", size=14),showgrid=False),
                xaxis=dict(tickfont=dict(color="#000000", size=11),showgrid=False),
                margin=dict(l=45, r=15, t=30, b=40),showlegend=False)
            BloqueW_H_THW = html.Div([
                html.Label(id='input-titulo-w-h-twh-thsw',style={'color': "#000000", 'fontSize': '16px'}, children=["'Enfriamiento Eólico °C' 'Indice de Calor °C' 'THW °C' 'THSW °C'"]),
                dcc.Graph(id='grafico-w-h-twh-thsw',figure=figPbar,config={'displayModeBar': False},style={'margin': '0 auto', 'display': 'block'})
            ], style={'width': '590px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})

            ############################################################
            ###                                                      ###
            ###     Grafica de Wind, Wind Low, Heat, Heat High       ###
            ###                                                      ###
            ############################################################

            figPbarabs = go.Figure()
            y1 = VectorWindC[0];  y2 = VectorWindC[1];  y3 = VectorHeat[0];  y4 = VectorHeat[1];    x = list(range(len(VectorWindC[0])))
            figPbarabs.add_trace(go.Scatter(x=x, y=y1,mode='lines',line=dict(color='#00FFF7'),opacity=0.4,name='Wind Chill °C'))
            figPbarabs.add_trace(go.Scatter(x=x, y=y2,mode='lines',line=dict(color='#00716E'),opacity=0.4,name='Low Wind Chill °C'))
            figPbarabs.add_trace(go.Scatter(x=x, y=y3,mode='lines',line=dict(color='#FF6F00'),opacity=0.4,name='Heat Index °C'))
            figPbarabs.add_trace(go.Scatter(x=x, y=y4,mode='lines',line=dict(color='#B04E04'),opacity=0.4,name='High Heat Index °C'))
            XlimInf = x[0]; XlimSup = x[len(x)-1];  YlimInf = Stats.DatoMinimoVector(y4); YlimSup = Stats.DatoMaximoVector(y3);
            tickvals_x = [XlimInf + (i * 0.1 * (XlimSup - XlimInf)) for i in range(11)]
            ticktext_x = [f'{val:.0f}' for val in tickvals_x]
            figPbarabs.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    range=[XlimInf, XlimSup],tickvals=tickvals_x,ticktext=ticktext_x,tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                yaxis=dict(range=[YlimInf - 0.5, YlimSup + 0.5],tickvals=[YlimInf, YlimSup],ticktext=[f'{YlimInf:.0f} °C', f'{YlimSup:.0f}°C'],
                    tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                margin=dict(l=40, r=40, t=20, b=40),showlegend=False,width=480,height=320
            )
            BloqueWWLHHH = html.Div([
                html.Label(id='input-titulo-w-wl-h-hl',style={'color': "#000000", 'fontSize': '16px'}, children=['Maximos y minimos del enfriamiento y calor °C']),
                dcc.Graph(id='grafico-w-wl-h-hl',figure=figPbarabs,config={'displayModeBar': True})   
            ], style={'width': '500px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
    
            ##################################################
            ###                                            ###
            ###     Grafica de TWH, TWH Max, TWH Min       ###
            ###                                            ###
            ##################################################
    
            MediaTHWMax = Stats.MediaVector(VectorTWH[1]);      MediaTHWMin = Stats.MediaVector(VectorTWH[2])               
            Etiquetas = ['',f'Max: {MediaTHWMax:.4f}',f'{MediaTHW:.4f}',f'Min: {MediaTHWMin:.4f}',''];
            ValoresTWH = [23.478875,MediaTHWMax,MediaTHW,MediaTHWMin,(23.478875+MediaTHWMax+MediaTHW+MediaTHWMin)]
            ColoresTWH = ['#ffffff', '#002fff', '#ff9999','#c60202','none'];
            figTHW, xTHW = plt.subplots(figsize=(6, 3.2))
            #figTHW.patch.set_alpha(0.0);  #xTHW.patch.set_alpha(0.0)
            xTHW.pie(ValoresTWH, labels=Etiquetas,colors=ColoresTWH,startangle=0,textprops={'fontsize': 11, 'weight': 'bold'})
            Dona = plt.Circle((0, 0), 0.70, fc='white')
            xTHW.add_artist(Dona);  xTHW.set_ylim(0, 1.1);  xTHW.set_xlim(-1.1, 1.1)
            plt.tight_layout()
            #codificar
            bufTHW = io.BytesIO()
            plt.savefig(bufTHW, format="png", bbox_inches='tight', transparent=True)
            plt.close(figTHW)
            bufTHW.seek(0)
            imagen_base64 = base64.b64encode(bufTHW.read()).decode('utf-8')
            url_imagen = f"data:image/png;base64,{imagen_base64}"
            #src_twh = f"data:image/png;base64,{base64.b64encode(bufTHW.getvalue()).decode('utf-8')}"
            BloqueTHW = html.Div(
                [
                    html.Label(id='input-twh',style={'color': "#000000", 'fontSize': '16px'},children=['Sensacion Termica °C']),
                    html.Img(src=url_imagen, style={'width': '300px', 'height': '600px'})
                ], style={'width': '340px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
    
            #####################################################
            ###                                               ###
            ###     Grafica de TWSH, TWSH Max, TWSH Min       ###
            ###                                               ###
            #####################################################
            
            MediaTHSWMax = Stats.MediaVector(VectorTHSW[1]);      MediaTHSWMin = Stats.MediaVector(VectorTHSW[2])               
            Etiquetas = ['',f'Max: {MediaTHSWMax:.4f}',f'{MediaTHSW:.4f}',f'Min: {MediaTHSWMin:.4f}',''];
            ValoresTWH = [23.478875,MediaTHSWMax,MediaTHSW,MediaTHSWMin,(23.478875+MediaTHSWMax+MediaTHSW+MediaTHSWMin)]
            ColoresTWH = ['#ffffff', "#00b512", "#300D64",'#c60202','none'];
            figTHSW, xTHSW = plt.subplots(figsize=(6, 3.2))
            #figTHW.patch.set_alpha(0.0);  #xTHW.patch.set_alpha(0.0)
            xTHSW.pie(ValoresTWH, labels=Etiquetas,colors=ColoresTWH,startangle=0,textprops={'fontsize': 11, 'weight': 'bold'})
            Dona = plt.Circle((0, 0), 0.70, fc='white')
            xTHSW.add_artist(Dona);  xTHSW.set_ylim(0, 1.1);  xTHSW.set_xlim(-1.1, 1.1)
            plt.tight_layout()
            #codificar
            bufTHSW = io.BytesIO()
            plt.savefig(bufTHSW, format="png", bbox_inches='tight', transparent=True)
            plt.close(figTHSW)
            bufTHSW.seek(0)
            imagen_base64 = base64.b64encode(bufTHSW.read()).decode('utf-8')
            url_imagen = f"data:image/png;base64,{imagen_base64}"
            #src_twh = f"data:image/png;base64,{base64.b64encode(bufTHW.getvalue()).decode('utf-8')}"
            BloqueTHSW = html.Div(
                [
                    html.Label(id='input-twsh',style={'color': "#000000", 'fontSize': '16px'},children=['Sensacion Termica Radiada°C']),
                    html.Img(src=url_imagen, style={'width': '300px', 'height': '600px'})
                ], style={'width': '340px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
    
            ###########################
            ###                     ###
            ###     Histogramas     ###
            ###                     ###
            ###########################

            #Histrograma Enfriamento eolico
            Media1,VarianzaInsesgadaWindC,Varianza1,DesviacionWindCNM,DatoMaxWindC,IndiceMaxWindC,DatoMinWindC,IndiceMinWindC,DatoModa1 = Curva.DatosHTML(y1)
            Media2,VarianzaInsesgadaWindCMin,Varianza2,DesviacionWindCMinNM,DatoMaxWindCMin,IndiceMaxWindCMin,DatoMinWindCMin,IndiceMinWindCMin,DatoModa2 = Curva.DatosHTML(y2)
            Stats.timsort(y1);                      Stats.timsort(y2);
            Mediana1 = Stats.MedianaVector(y1);     Mediana2 = Stats.MedianaVector(y2);
            DesviacionWindC = Stats.DesviacionNewton(VarianzaInsesgadaWindC);
            DesviacionWindCMin = Stats.DesviacionNewton(VarianzaInsesgadaWindCMin);
            Pearson1, r1 = Curva.RegresionLinealHTML(y1, VarianzaInsesgadaWindC)
            Pearson2, r2 = Curva.RegresionLinealHTML(y2, VarianzaInsesgadaWindCMin)
            PercExtWindC = Stats.Percentil(y1, Percentiles);
            PercExtWindCMin = Stats.Percentil(y2, Percentiles);
            figHistWindCWindCMin, xHistWindCWindCMin = plt.subplots(figsize=(10, 6));
            figHistWindCWindCMin.patch.set_alpha(0.0);  xHistWindCWindCMin.patch.set_alpha(0.0);
            XlimInf2 = y2[0];    XlimSup2 = y1[len(y1) - 1];  Rango = int(RegladeSturges(len(y1) - 1));
            xHistWindCWindCMin.hist(y1, bins=Rango,rwidth = 1.2, color = '#00FFF7',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistWindCWindCMin.hist(y2, bins=Rango,rwidth = 1.2, color = '#00716E',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistWindCWindCMin.set_xticks([XlimInf2,PercExtWindC[0],PercExtWindC[1],PercExtWindC[2],PercExtWindCMin[0],PercExtWindCMin[1],PercExtWindCMin[2],XlimSup2])
            xHistWindCWindCMin.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtWindC[0]:.0f}°C',f'{PercExtWindC[1]:.0f}°C',f'{PercExtWindC[2]:.0f}°C',f'{PercExtWindCMin[0]:.0f}°C',f'{PercExtWindCMin[1]:.0f}°C',f'{PercExtWindCMin[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color="#0A0000", fontsize=14, fontname=fuente)
            xHistWindCWindCMin.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercExtWindC,ColorPerc):
                xHistWindCWindCMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            for p, val, col in zip(Percentiles,PercExtWindCMin,ColorPerc):
                xHistWindCWindCMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistWindCWindCMin = io.BytesIO()
            plt.savefig(bufHistWindCWindCMin, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistWindCWindCMin)
            src_hist_wind_c_wind_c_min = f"data:image/png;base64,{base64.b64encode(bufHistWindCWindCMin.getvalue()).decode('utf-8')}"
            BloqueHistWindCWindCMin = html.Div([
                html.Img(src=src_hist_wind_c_wind_c_min, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_wind_c_wind_c_min',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Enfriamiento Eólico °C']),
                html.P([
                    html.Strong('Medias Aritméticas'),html.Br(),
                    f'Para medios: {Media1:.4f}',f'\tPara Minimos: {Media2:.4f}',html.Br(),
                    html.Strong('Medianas'),html.Br(),
                    f'Para medios: {Mediana1:.0f}',f'\tPara Minimos: {Mediana2:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'Para medios: {VarianzaInsesgadaWindC:.4f}',f'\tPara Minimos: {VarianzaInsesgadaWindCMin:.4f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'Para medios: {DesviacionWindC:.4f}',f'\tPara Minimos: {DesviacionWindCMin:.4f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'Para medios: {Varianza1:.4f}',f'\tPara Minimos: {Varianza2:.4f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'Para medios: {DesviacionWindCNM:.4f}',f'\tPara Minimos: {DesviacionWindCMinNM:.4f}',html.Br(),
                    html.Strong('Valores y Minimos'),html.Br(),
                    f'Fecha Medios: {Fechas[IndiceMaxWindC + Pos1]}',f', : {Fechas[IndiceMinWindC + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxWindC:.0f}°C',f',: {DatoMinWindC:.0f}°C',html.Br(),
                    f'Fecha Minimos: {Fechas[IndiceMaxWindCMin + Pos1]}',f', : {Fechas[IndiceMinWindCMin + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxWindCMin:.0f}°C',f',: {DatoMinWindCMin:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para medios: {DatoModa1:.0f}',f'\tPara Minimos: {DatoModa2:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para Medios: CD:{Pearson1:.4f}',f',CC:{r1:.4f}',html.Br(),
                    f'Para Minimas: CD:{Pearson2:.4f}',f',CC:{r2:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Medios: P{Percentiles[0]}: {PercExtWindC[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtWindC[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtWindC[2]:.0f}°C',html.Br(),
                    f'Minimas: P{Percentiles[0]}: {PercExtWindCMin[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtWindCMin[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtWindCMin[2]:.0f}°C'
                ],style={'textAlign': 'center'})
                ], style={'width': '340px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            
            #Histrograma Indice de Calor
            Media3,VarianzaInsesgadaHeatI,Varianza3,DesviacionHeatINM,DatoMaxHeatI,IndiceMaxHeatI,DatoMinHeatI,IndiceMinHeatI,DatoModa3 = Curva.DatosHTML(y3)
            Media4,VarianzaInsesgadaHHeatI,Varianza4,DesviacionHHeatINM,DatoMaxHHeatI,IndiceMaxHHeatI,DatoMinHHeatI,IndiceMinHHeatI,DatoModa4 = Curva.DatosHTML(y4)
            Stats.timsort(y3);                      Stats.timsort(y4);
            Mediana3 = Stats.MedianaVector(y3);     Mediana4 = Stats.MedianaVector(y4);
            DesviacionHeatI = Stats.DesviacionNewton(VarianzaInsesgadaHeatI);
            DesviacionHHeatI = Stats.DesviacionNewton(VarianzaInsesgadaHHeatI);
            Pearson3, r3 = Curva.RegresionLinealHTML(y3, VarianzaInsesgadaWindC)
            Pearson4, r4 = Curva.RegresionLinealHTML(y4, VarianzaInsesgadaWindCMin)
            PercExtHeatI = Stats.Percentil(y3, Percentiles);
            PercExtHHeatI = Stats.Percentil(y4, Percentiles);
            figHistH_HeatI, xHistH_HeatI = plt.subplots(figsize=(10, 6));
            figHistH_HeatI.patch.set_alpha(0.0);  xHistH_HeatI.patch.set_alpha(0.0);
            XlimInf2 = y4[0];    XlimSup2 = y3[len(y3) - 1];  Rango = int(RegladeSturges(len(y3) - 1));
            xHistH_HeatI.hist(y3, bins=Rango,rwidth = 1.2, color = '#FF6F00',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistH_HeatI.hist(y4, bins=Rango,rwidth = 1.2, color = '#B04E04',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistH_HeatI.set_xticks([XlimInf2,PercExtHeatI[0],PercExtHeatI[1],PercExtHeatI[2],PercExtHHeatI[0],PercExtHHeatI[1],PercExtHHeatI[2],XlimSup2])
            xHistH_HeatI.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtHeatI[0]:.0f}°C',f'{PercExtHeatI[1]:.0f}°C',f'{PercExtHeatI[2]:.0f}°C',f'{PercExtHHeatI[0]:.0f}°C',f'{PercExtHHeatI[1]:.0f}°C',f'{PercExtHHeatI[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color="#050000", fontsize=14, fontname=fuente)
            xHistH_HeatI.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercExtHeatI,ColorPerc):
                xHistH_HeatI.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            for p, val, col in zip(Percentiles,PercExtHHeatI,ColorPerc):
                xHistH_HeatI.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistH_HeatI = io.BytesIO()
            plt.savefig(bufHistH_HeatI, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistH_HeatI)
            src_hist_high_heat_index = f"data:image/png;base64,{base64.b64encode(bufHistH_HeatI.getvalue()).decode('utf-8')}"
            BloqueHistHighHeatIndex = html.Div([
                html.Img(src=src_hist_high_heat_index, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_high_heat_index',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Calentamiento °C']),
                html.P([
                    html.Strong('Medias Aritméticas'),html.Br(),
                    f'Para maximas: {Media3:.4f}',f'\tPara Minimos: {Media4:.4f}',html.Br(),
                    html.Strong('Medianas'),html.Br(),
                    f'Para maximas: {Mediana3:.0f}',f'\tPara Minimos: {Mediana4:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'Para maximas: {VarianzaInsesgadaHeatI:.4f}',f'\tPara Minimos: {VarianzaInsesgadaHHeatI:.4f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'Para maximas: {DesviacionHeatI:.4f}',f'\tPara Minimos: {DesviacionHHeatI:.4f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'Para maximas: {Varianza3:.4f}',f'\tPara Minimos: {Varianza4:.4f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'Para maximas: {DesviacionHeatINM:.4f}',f'\tPara Minimos: {DesviacionHHeatINM:.4f}',html.Br(),
                    html.Strong('Valores y Minimos'),html.Br(),
                    f'Fecha Medios: {Fechas[IndiceMaxHeatI + Pos1]}',f', : {Fechas[IndiceMinHeatI + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxHeatI:.0f}°C',f',: {DatoMinHeatI:.0f}°C',html.Br(),
                    f'Fecha Minimos: {Fechas[IndiceMaxHHeatI + Pos1]}',f', : {Fechas[IndiceMinHHeatI + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxHHeatI:.0f}°C',f',: {DatoMinHHeatI:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para maximas: {DatoModa3:.0f}',f'\tPara Minimos: {DatoModa4:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para Medios: CD:{Pearson3:.4f}',f',CC:{r3:.4f}',html.Br(),
                    f'Para Minimas: CD:{Pearson4:.4f}',f',CC:{r4:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Maximas: P{Percentiles[0]}: {PercExtHeatI[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtHeatI[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtHeatI[2]:.0f}°C',html.Br(),
                    f'Minimas: P{Percentiles[0]}: {PercExtHHeatI[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtHHeatI[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtHHeatI[2]:.0f}°C'
                ],style={'textAlign': 'center'})
                ], style={'width': '340px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma TWH
            figHistInsideTWH, xHistInsideTWH = plt.subplots(figsize=(10, 6));   y5 = VectorTWH[0];
            Media5,VarianzaInsesgadaTHW,Varianza5,DesviacionTHWNM,DatoMaxInsideTWH,IndiceMaxInsideTWH,DatoMinInsideTWH,IndiceMinInsideTWH,DatoModa5 = Curva.DatosHTML(y5)
            Stats.timsort(y5);      MedianaTHW = Stats.MedianaVector(y5);
            DesviacionTHW = Stats.DesviacionNewton(VarianzaInsesgadaTHW);
            Pearson5, r5 = Curva.RegresionLinealHTML(y5, VarianzaInsesgadaTHW)
            PercTHW = Stats.Percentil(y5, Percentiles);
            figHistInsideTWH.patch.set_alpha(0.0);  xHistInsideTWH.patch.set_alpha(0.0);
            XlimInf1 = y5[0];    XlimSup1 = y5[len(y5) - 1];  Rango5 = int(RegladeSturges(len(y1) - 1))
            xHistInsideTWH.hist(y5, bins=Rango5,rwidth = 1.2, edgecolor = 'black', color="#4F9BFF",linewidth=4.0, alpha=0.6)
            xHistInsideTWH.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
            xHistInsideTWH.set_xticks([XlimInf1,PercTHW[0],PercTHW[1],PercTHW[2],XlimSup1])
            xHistInsideTWH.set_xticklabels([f'{XlimInf1:.2f}°C',f'{PercTHW[0]:.0f}°C',f'{PercTHW[1]:.0f}°C',f'{PercTHW[2]:.0f}°C',f'{XlimSup1:.2f}°C'], color="#000000", fontsize=14, fontname=fuente)
            for p, val, col in zip(Percentiles,PercTHW,ColorPerc):
                xHistInsideTWH.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistTWH = io.BytesIO()
            plt.savefig(bufHistTWH, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistInsideTWH)
            src_hist_t_w_h = f"data:image/png;base64,{base64.b64encode(bufHistTWH.getvalue()).decode('utf-8')}"
            BloqueHistTWH = html.Div([
                html.Img(src=src_hist_t_w_h, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_ins-temp-hum',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Sensación de calor °C']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{Media5:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaTHW:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaTHW:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionTHW:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza5:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionTHWNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Medios: {Fechas[IndiceMaxInsideTWH + Pos1]}',f', : {Fechas[IndiceMinInsideTWH + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxInsideTWH:.0f}°C',f',: {DatoMinInsideTWH:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa5:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'THW: CD:{Pearson5:.4f}',f',CC:{r5:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercTHW[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercTHW[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercTHW[2]:.0f}°C'
                ],style={'textAlign': 'center'})
                ], style={'width': '340px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma THSW
            figHistInsideTHSW, xHistInsideTHSW = plt.subplots(figsize=(10, 6));     y8 = VectorTHSW[0];
            Media8,VarianzaInsesgadaTHSW,Varianza8,DesviacionTHSWNM,DatoMaxTHSW,IndiceMaxTHSW,DatoMinTHSW,IndiceMinTHSW,DatoModa8 = Curva.DatosHTML(y8)
            Stats.timsort(y8);  DatoModa8 = Stats.ModaVectorValor(y8);  MedianaTHSW = Stats.MedianaVector(y8);
            DesviacionTHSW = Stats.DesviacionNewton(VarianzaInsesgadaTHSW);
            Pearson8, r8 = Curva.RegresionLinealHTML(y8, VarianzaInsesgadaTHSW)
            PercTHSW = Stats.Percentil(y8, Percentiles);
            figHistInsideTHSW.patch.set_alpha(0.0);  xHistInsideTHSW.patch.set_alpha(0.0);
            XlimInf1 = y8[0];    XlimSup1 = y8[len(y8) - 1];  Rango8 = int(RegladeSturges(len(y8) - 1))
            xHistInsideTHSW.hist(y8, bins=Rango8,rwidth = 1.2, edgecolor = 'black', color="#9309D3",linewidth=4.0, alpha=0.6)
            xHistInsideTHSW.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
            xHistInsideTHSW.set_xticks([XlimInf1,PercTHSW[0],PercTHSW[1],PercTHSW[2],XlimSup1])
            xHistInsideTHSW.set_xticklabels([f'{XlimInf1:.2f}°C',f'{PercTHSW[0]:.0f}°C',f'{PercTHSW[1]:.0f}°C',f'{PercTHSW[2]:.0f}°C',f'{XlimSup1:.2f}°C'], color="#000000", fontsize=14, fontname=fuente)
            for p, val, col in zip(Percentiles,PercTHSW,ColorPerc):
                xHistInsideTHSW.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistTHSW = io.BytesIO()
            plt.savefig(bufHistTHSW, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistInsideTHSW)
            src_hist_t_h_s_w = f"data:image/png;base64,{base64.b64encode(bufHistTHSW.getvalue()).decode('utf-8')}"
            BloqueHistTHSW = html.Div([
                html.Img(src=src_hist_t_h_s_w, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_t-h-s-w',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Sensacion de calor radiada °C']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{MediaTHSW:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaTHSW:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaTHSW:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionTHSW:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza8:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionTHSWNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fechas: {Fechas[IndiceMaxTHSW + Pos1]}',f', : {Fechas[IndiceMinTHSW + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxTHSW:.0f}°C',f',: {DatoMinTHSW:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa8:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'THSW: CD:{Pearson8:.4f}',f',CC:{r8:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercTHSW[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercTHSW[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercTHSW[2]:.0f}°C'
                ],style={'textAlign': 'center'})
                ], style={'width': '340px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histrograma THW Maximos y Minimos
            y6 = VectorTWH[1];  y7 = VectorTWH[2]
            Media6,VarianzaInsesgadaTHWMax,Varianza6,DesviacionTHWMaxNM,DatoMaxTHWMax,IndiceMaxTHWMax,DatoMinTHWMax,IndiceMinTHWMax,DatoModa6 = Curva.DatosHTML(y6)
            Media7,VarianzaInsesgadaTHWMin,Varianza7,DesviacionTHWMinNM,DatoMaxTHWMin,IndiceMaxTHWMin,DatoMinTHWMin,IndiceMinTHWMin,DatoModa7 = Curva.DatosHTML(y7)
            Stats.timsort(y6);                      Stats.timsort(y7);
            Mediana6 = Stats.MedianaVector(y6);     Mediana7 = Stats.MedianaVector(y7);
            DesviacionTHWMax = Stats.DesviacionNewton(VarianzaInsesgadaTHWMax);
            DesviacionTHWMin = Stats.DesviacionNewton(VarianzaInsesgadaTHWMin);
            Pearson6, r6 = Curva.RegresionLinealHTML(y6, VarianzaInsesgadaTHWMax)
            Pearson7, r7 = Curva.RegresionLinealHTML(y7, VarianzaInsesgadaTHWMin)
            PercTHWMax = Stats.Percentil(y6, Percentiles);
            PercTHWMin = Stats.Percentil(y7, Percentiles);
            figHistTHWMaxMin, xHistTHWMaxMin = plt.subplots(figsize=(10, 6));
            figHistTHWMaxMin.patch.set_alpha(0.0);  xHistTHWMaxMin.patch.set_alpha(0.0);
            XlimInf2 = y7[0];    XlimSup2 = y6[len(y6) - 1];  Rango = int(RegladeSturges(len(y7) - 1))
            xHistTHWMaxMin.hist(y6, bins=Rango,rwidth = 1.2, color = "#002fff",linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistTHWMaxMin.hist(y7, bins=Rango,rwidth = 1.2, color = "#c60202",linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistTHWMaxMin.set_xticks([XlimInf2,PercTHWMin[0],PercTHWMin[1],PercTHWMin[2],PercTHWMax[0],PercTHWMax[1],PercTHWMax[2],XlimSup2])
            xHistTHWMaxMin.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercTHWMin[0]:.0f}°C',f'{PercTHWMin[1]:.0f}°C',f'{PercTHWMin[2]:.0f}°C',f'{PercTHWMax[0]:.0f}°C',f'{PercTHWMax[1]:.0f}°C',f'{PercTHWMax[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
            xHistTHWMaxMin.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercTHWMax,ColorPerc):
                xHistTHWMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            for p, val, col in zip(Percentiles,PercTHWMin,ColorPerc):
                xHistTHWMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistTHWMaxMin = io.BytesIO()
            plt.savefig(bufHistTHWMaxMin, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistTHWMaxMin)
            src_hist_thw_max_min = f"data:image/png;base64,{base64.b64encode(bufHistTHWMaxMin.getvalue()).decode('utf-8')}"
            BloqueHistTHWMaxMin = html.Div([
                html.Img(src=src_hist_thw_max_min, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_thw-max-min',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Sensaciones Termicas °C']),
                html.P([
                    html.Strong('Medias Aritméticas'),html.Br(),
                    f'Para maximas: {Media6:.4f}',f'\tPara Minimos: {Media7:.4f}',html.Br(),
                    html.Strong('Medianas'),html.Br(),
                    f'Para maximas: {Mediana6:.0f}',f'\tPara Minimos: {Mediana7:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'Para maximas: {VarianzaInsesgadaTHWMax:.4f}',f'\tPara Minimos: {VarianzaInsesgadaTHWMin:.4f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'Para maximas: {DesviacionTHWMax:.4f}',f'\tPara Minimos: {DesviacionTHWMin:.4f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'Para maximas: {Varianza6:.4f}',f'\tPara Minimos: {Varianza7:.4f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'Para maximas: {DesviacionTHWMaxNM:.4f}',f'\tPara Minimos: {DesviacionTHWMinNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Medios: {Fechas[IndiceMaxTHWMax + Pos1]}',f', : {Fechas[IndiceMinTHWMax + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxTHWMax:.0f}°C',f',: {DatoMinTHWMax:.0f}°C',html.Br(),
                    f'Fecha Minimos: {Fechas[IndiceMaxTHWMin + Pos1]}',f', : {Fechas[IndiceMinTHWMin + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxTHWMin:.0f}°C',f',: {DatoMinTHWMin:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para maximas: {DatoModa6:.0f}',f'\tPara Minimos: {DatoModa7:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para Medios: CD:{Pearson6:.4f}',f',CC:{r6:.4f}',html.Br(),
                    f'Para Minimas: CD:{Pearson7:.4f}',f',CC:{r7:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Maximas: P{Percentiles[0]}: {PercTHWMax[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercTHWMax[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercTHWMax[2]:.0f}°C',html.Br(),
                    f'Minimas: P{Percentiles[0]}: {PercTHWMin[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercTHWMin[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercTHWMin[2]:.0f}°C'
                ],style={'textAlign': 'center'})  
                ], style={'width': '340px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histrograma THSW Maximos y Minimos
            y6 = VectorTHSW[1];  y7 = VectorTHSW[2]
            Media6,VarianzaInsesgadaTHSWMax,Varianza6,DesviacionTHSWMaxNM,DatoMaxTHSWMax,IndiceMaxTHSWMax,DatoMinTHSWMax,IndiceMinTHSWMax,DatoModa6 = Curva.DatosHTML(y6)
            Media7,VarianzaInsesgadaTHSWMin,Varianza7,DesviacionTHSWMinNM,DatoMaxTHSWMin,IndiceMaxTHSWMin,DatoMinTHSWMin,IndiceMinTHSWMin,DatoModa7 = Curva.DatosHTML(y7)
            Stats.timsort(y6);                      Stats.timsort(y7);
            Mediana6 = Stats.MedianaVector(y6);     Mediana7 = Stats.MedianaVector(y7);
            DesviacionTHSWMax = Stats.DesviacionNewton(VarianzaInsesgadaTHSWMax);
            DesviacionTHSWMin = Stats.DesviacionNewton(VarianzaInsesgadaTHSWMin);
            Pearson6, r6 = Curva.RegresionLinealHTML(y6, VarianzaInsesgadaTHSWMax)
            Pearson7, r7 = Curva.RegresionLinealHTML(y7, VarianzaInsesgadaTHSWMin)
            PercTHSWMax = Stats.Percentil(y6, Percentiles);
            PercTHSWMin = Stats.Percentil(y7, Percentiles);
            figHistTHSWMaxMin, xHistTHSWMaxMin = plt.subplots(figsize=(10, 6));
            figHistTHSWMaxMin.patch.set_alpha(0.0);  xHistTHSWMaxMin.patch.set_alpha(0.0);
            XlimInf2 = y6[0];    XlimSup2 = y7[len(y7) - 1];  Rango = int(RegladeSturges(len(y7) - 1))
            xHistTHSWMaxMin.hist(y6, bins=Rango,rwidth = 1.2, color = "#00b512",linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistTHSWMaxMin.hist(y7, bins=Rango,rwidth = 1.2, color = "#c60202",linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistTHSWMaxMin.set_xticks([XlimInf2,PercTHSWMin[0],PercTHSWMin[1],PercTHSWMin[2],PercTHSWMax[0],PercTHSWMax[1],PercTHSWMax[2],XlimSup2])
            xHistTHSWMaxMin.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercTHSWMin[0]:.0f}°C',f'{PercTHSWMin[1]:.0f}°C',f'{PercTHSWMin[2]:.0f}°C',f'{PercTHSWMax[0]:.0f}°C',f'{PercTHSWMax[1]:.0f}°C',f'{PercTHSWMax[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
            xHistTHSWMaxMin.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercTHSWMax,ColorPerc):
                xHistTHSWMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            for p, val, col in zip(Percentiles,PercTHSWMin,ColorPerc):
                xHistTHSWMaxMin.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistTHSWMaxMin = io.BytesIO()
            plt.savefig(bufHistTHSWMaxMin, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistTHSWMaxMin)
            src_hist_thsw_max_min = f"data:image/png;base64,{base64.b64encode(bufHistTHSWMaxMin.getvalue()).decode('utf-8')}"
            BloqueHistTHSWMaxMin = html.Div([
                html.Img(src=src_hist_thsw_max_min, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_thsw-max-min',style={'color': "#000000",'textAlign': 'center','fontSize': '16px'},children=['Sensaciones Termicas °C']),
                html.P([
                    html.Strong('Medias Aritméticas'),html.Br(),
                    f'Para maximas: {Media6:.4f}',f'\tPara Minimos: {Media7:.4f}',html.Br(),
                    html.Strong('Medianas'),html.Br(),
                    f'Para maximas: {Mediana6:.0f}',f'\tPara Minimos: {Mediana7:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'Para maximas: {VarianzaInsesgadaTHSWMax:.4f}',f'\tPara Minimos: {VarianzaInsesgadaTHSWMin:.4f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'Para maximas: {DesviacionTHSWMax:.4f}',f'\tPara Minimos: {DesviacionTHSWMin:.4f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'Para maximas: {Varianza6:.4f}',f'\tPara Minimos: {Varianza7:.4f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'Para maximas: {DesviacionTHSWMaxNM:.4f}',f'\tPara Minimos: {DesviacionTHSWMinNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Medios: {Fechas[IndiceMaxTHSWMax + Pos1]}',f', : {Fechas[IndiceMinTHSWMax + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxTHSWMax:.0f}°C',f',: {DatoMinTHSWMax:.0f}°C',html.Br(),
                    f'Fecha Minimos: {Fechas[IndiceMaxTHSWMin + Pos1]}',f', : {Fechas[IndiceMinTHSWMin + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxTHSWMin:.0f}°C',f',: {DatoMinTHSWMin:.0f}°C',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para maximas: {DatoModa6:.0f}',f'\tPara Minimos: {DatoModa7:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para Medios: CD:{Pearson6:.4f}',f',CC:{r6:.4f}',html.Br(),
                    f'Para Minimas: CD:{Pearson7:.4f}',f',CC:{r7:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Maximas: P{Percentiles[0]}: {PercTHSWMax[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercTHSWMax[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercTHSWMax[2]:.0f}°C',html.Br(),
                    f'Minimas: P{Percentiles[0]}: {PercTHSWMin[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercTHSWMin[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercTHSWMin[2]:.0f}°C'
                ],style={'textAlign': 'center'})  
                ], style={'width': '340px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            return BloqueW_H_THW,None,BloqueWWLHHH, BloqueHistWindCWindCMin,BloqueHistHighHeatIndex,BloqueHistTWH,BloqueHistTHSW, None,None,None, BloqueTHW,BloqueHistTHWMaxMin,BloqueHistTHSWMaxMin,BloqueTHSW
            
        if opcion == "DatosLluvia":
            print("Datos de la lluvia")
            #Vectores Temperatura Exterior
            VectorETRain = [];  VectorETRainM = [];
            #Inicio y Final del indice
            i = ETpot; Ante = HighRain;
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
                if(i == ETpot):
                    VectorETRain.append(Datos)
                    VectorETRainM.append(Stats.MediaVector(Datos))
                    i = i + 1;
                elif(i == Rain):
                    VectorETRain.append(Datos)
                    VectorETRainM.append(Stats.MediaVector(Datos))
                    i = i + 1;
                #Temperatura vs Humedad Minimas
                elif(i == HighRain):
                    VectorETRain.append(Datos)
                    VectorETRainM.append(Stats.MediaVector(Datos))
                    i = i + 1;
            
            ##########################################################################
            ###                                                                    ###
            ###     Grafica de medias de la Evotranspiracion, Lluvia y Maximos     ###
            ###                                                                    ###
            ##########################################################################
            
            IndiceBarrasDobleAxial = ["ET","Rain","RainHigh"]
            figETRain = go.Figure()
            figETRain.add_trace(go.Bar(x=[IndiceBarrasDobleAxial[0]],y=[VectorETRainM[0]],
                name='Evapotranspiracion',marker=dict(color='#5EF956',line=dict(color='#005A06', width=6)),
                opacity=0.9,text=[f"{VectorETRainM[0]:.1f}mm"],  # Equivalente a bar_label
                textposition='outside',textfont=dict(color="#5EF956", size=12, family='sans-serif')
            ))
            figETRain.add_trace(go.Bar(x=[IndiceBarrasDobleAxial[1]],y=[VectorETRainM[1]],
                name='Humedad',yaxis='y2',marker=dict(color="#0026B0",line=dict(color="#0404CE", width=6)),
                opacity=0.9,text=[f"{VectorETRainM[1]:.1f}mm"],
                textposition='outside',textfont=dict(color="#0026B0", size=12, family='sans-serif')
            ))
            figETRain.add_trace(go.Bar(x=[IndiceBarrasDobleAxial[2]],y=[VectorETRainM[2]],
                name='Humedad',yaxis='y2',marker=dict(color='#001CD0',line=dict(color="#0700D0", width=6)),
                opacity=0.9,text=[f"{VectorETRainM[2]:.1f}mm"],
                textposition='outside',textfont=dict(color="#001CD0", size=12, family='sans-serif')
            ))
            figETRain.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    title=dict(text="ET | Precipitacion Pluvial",font=dict(color="#000000", size=16)),
                    tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                yaxis=dict(
                    title=dict(text='Evapotranspiracion mm',font=dict(color="#000000", size=16)),range=[0, 40],
                    tickvals=[0, 5, 10, 15, 20, 25, 30, 35, 40],ticktext=["0 mm", "5 mm", "10 mm", "15 mm", "20 mm", "25 mm", "30 mm", "35 mm", "40 mm"],
                    tickfont=dict(color='#F76A25', size=14),showgrid=False
                ),
                yaxis2=dict(
                    title=dict(text='Precipitacion mm',font=dict(color="#000000", size=16)),range=[0, 1.5],
                    tickvals=[0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00, 1.10, 1.20, 1.30, 1.40, 1.50],ticktext=['0.10 mm', '0.20 mm', '0.30 mm', '0.40 mm', '0.50 mm', '0.60 mm', '0.70 mm', '0.80 mm', '0.90 mm', '1.00 mm', '1.10 mm', '1.20 mm', '1.30 mm', '1.40 mm', '1.50 mm'],
                    tickfont=dict(color='#01476B', size=14),overlaying='y',side='right',showgrid=False
                ),
                margin=dict(l=60, r=60, t=30, b=60),showlegend=False,width=480,height=320
            )
            BloqueETRain = html.Div([
                html.Label(id='input-et-rain-high',style={'color': "#000000", 'fontSize': '16px'},children=['Precipitacion Pluvial']),
                dcc.Graph(id='grafico-et-rain-high',figure=figETRain,config={'displayModeBar': False})
            ], style={'width': '500px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})

            #################################################################
            ###                                                           ###
            ###     Grafica de maximos y medicion de la precipitacion     ###
            ###                                                           ###
            #################################################################

            figPbarabs = go.Figure()
            y1 = VectorETRain[1];  y2 = VectorETRain[2];    x = list(range(len(VectorETRain[1])))
            figPbarabs.add_trace(go.Scatter(x=x, y=y1,mode='lines',line=dict(color='#74E1FF'),opacity=0.4,name='Rain mm'))
            figPbarabs.add_trace(go.Scatter(x=x, y=y2,mode='lines',line=dict(color='#1A37AB'),opacity=0.4,name='High Rain mm'))
            XlimInf = x[0]; XlimSup = x[len(x)-1];  YlimInf = Stats.DatoMinimoVector(y1); YlimSup = Stats.DatoMaximoVector(y2);
            tickvals_x = [XlimInf + (i * 0.1 * (XlimSup - XlimInf)) for i in range(11)]
            ticktext_x = [f'{val:.0f}' for val in tickvals_x]
            figPbarabs.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    range=[XlimInf, XlimSup],tickvals=tickvals_x,ticktext=ticktext_x,tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                yaxis=dict(range=[YlimInf - 0.5, YlimSup + 0.5],tickvals=[YlimInf, YlimSup],ticktext=[f'{YlimInf:.0f} mm', f'{YlimSup:.0f} mm'],
                    tickfont=dict(color="#000000", size=14),showgrid=False
                ),
                margin=dict(l=40, r=40, t=20, b=40),showlegend=False,width=480,height=320
            )
            BloqueRainRainHigh = html.Div([
                html.Label(id='input-titulo-rain-rain-high',style={'color': "#000000", 'fontSize': '16px'}, children=['Precipitación y maximos']),
                dcc.Graph(id='grafico-rain-rain-high',figure=figPbarabs,config={'displayModeBar': True})   
            ], style={'width': '500px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})

            ###########################
            ###                     ###
            ###     Histogramas     ###
            ###                     ###
            ###########################

            #Histograma ET
            figET, xET = plt.subplots(figsize=(10, 6));     y1 = VectorETRain[0];
            Media1,VarianzaInsesgadaET,Varianza1,DesviacionETNM,DatoMaxET,IndiceMaxET,DatoMinET,IndiceMinET,DatoModa1 = Curva.DatosHTML(y1)
            Stats.timsort(y1);      MedianaET = Stats.MedianaVector(y1);
            DesviacionET = Stats.DesviacionNewton(VarianzaInsesgadaET);
            Pearson1, r1 = Curva.RegresionLinealHTML(y1, VarianzaInsesgadaET)
            PercET = Stats.Percentil(y1, Percentiles);
            figET.patch.set_alpha(0.0);  xET.patch.set_alpha(0.0);
            XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
            xET.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = 'black', color="#5EF956",linewidth=4.0, alpha=0.6)
            xET.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
            xET.set_xticks([XlimInf1,PercET[0],PercET[1],PercET[2],XlimSup1])
            xET.set_xticklabels([f'{XlimInf1:.2f}mm',f'{PercET[0]:.0f}mm',f'{PercET[1]:.0f}mm',f'{PercET[2]:.0f}mm',f'{XlimSup1:.2f}mm'], color="#000000", fontsize=14, fontname=fuente)
            for p, val, col in zip(Percentiles,PercET,ColorPerc):
                xET.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufET = io.BytesIO()
            plt.savefig(bufET, format="png", bbox_inches="tight", transparent=True)
            plt.close(figET)
            src_hist_ET = f"data:image/png;base64,{base64.b64encode(bufET.getvalue()).decode('utf-8')}"
            BloqueET = html.Div([
                html.Img(src=src_hist_ET, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-et',style={'color': "#000000", 'fontSize': '16px'},children=['Evapotranspiracion mm']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{VectorETRainM[0]:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaET:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaET:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionET:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza1:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionETNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Medios: {Fechas[IndiceMaxET + Pos1]}',f', : {Fechas[IndiceMinET + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxET:.0f}mm',f',: {DatoMinET:.0f}mm',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa1:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para Medios: CD:{Pearson1:.4f}',f',CC:{r1:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercET[0]:.0f}mm',f'\tP{Percentiles[1]}: {PercET[1]:.0f}mm',f'\tP{Percentiles[2]}: {PercET[2]:.0f}mm'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma Rain
            figRain, xRain = plt.subplots(figsize=(10, 6));     y2 = VectorETRain[1];
            Media2,VarianzaInsesgadaRain,Varianza2,DesviacionRainNM,DatoMaxRain,IndiceMaxRain,DatoMinRain,IndiceMinRain,DatoModa2 = Curva.DatosHTML(y2)
            Stats.timsort(y2);      MedianaRain = Stats.MedianaVector(y2);
            DesviacionRain = Stats.DesviacionNewton(VarianzaInsesgadaRain);
            Pearson2, r2 = Curva.RegresionLinealHTML(y2, VarianzaInsesgadaRain)
            PercRain = Stats.Percentil(y2, Percentiles);
            figRain.patch.set_alpha(0.0);  xRain.patch.set_alpha(0.0);
            XlimInf1 = y2[0];    XlimSup1 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(len(y2) - 1))
            xRain.hist(y2, bins=Rango2,rwidth = 1.2, edgecolor = 'black', color="#8ED7FB",linewidth=4.0, alpha=0.6)
            xRain.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
            xRain.set_xticks([XlimInf1,PercRain[0],PercRain[1],PercRain[2],XlimSup1])
            xRain.set_xticklabels([f'{XlimInf1:.2f}mm',f'{PercRain[0]:.0f}mm',f'{PercRain[1]:.0f}mm',f'{PercRain[2]:.0f}mm',f'{XlimSup1:.2f}mm'], color="#000000", fontsize=14, fontname=fuente)
            for p, val, col in zip(Percentiles,PercRain,ColorPerc):
                xRain.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufRain = io.BytesIO()
            plt.savefig(bufRain, format="png", bbox_inches="tight", transparent=True)
            plt.close(figRain)
            src_hist_Rain = f"data:image/png;base64,{base64.b64encode(bufRain.getvalue()).decode('utf-8')}"
            BloqueRain = html.Div([
                html.Img(src=src_hist_Rain, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_rain',style={'color': "#000000", 'fontSize': '16px'},children=['Precipitacion Pluvial mm']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{VectorETRainM[1]:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaRain:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaRain:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionRain:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza2:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionRainNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Medios: {Fechas[IndiceMaxRain + Pos1]}',f', : {Fechas[IndiceMinRain + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxRain:.0f}mm',f',: {DatoMinRain:.0f}mm',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa2:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para Medios: CD:{Pearson2:.4f}',f',CC:{r2:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercRain[0]:.0f}mm',f'\tP{Percentiles[1]}: {PercRain[1]:.0f}mm',f'\tP{Percentiles[2]}: {PercRain[2]:.0f}mm'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            #Histograma High Rain
            figRainHigh, xRainHigh = plt.subplots(figsize=(10, 6));     y1 = VectorETRain[2];
            Media1,VarianzaInsesgadaRainHigh,Varianza1,DesviacionRainHighNM,DatoMaxRainHigh,IndiceMaxRainHigh,DatoMinRainHigh,IndiceMinRainHigh,DatoModa1 = Curva.DatosHTML(y1)
            Stats.timsort(y1);      MedianaRainHigh = Stats.MedianaVector(y1);
            DesviacionRainHigh = Stats.DesviacionNewton(VarianzaInsesgadaRainHigh);
            Pearson1, r1 = Curva.RegresionLinealHTML(y1, VarianzaInsesgadaRainHigh)
            PercRainHigh = Stats.Percentil(y1, Percentiles);
            figRainHigh.patch.set_alpha(0.0);  xRainHigh.patch.set_alpha(0.0);
            XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
            xRainHigh.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = 'black', color="#001CD0",linewidth=4.0, alpha=0.6)
            xRainHigh.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
            xRainHigh.set_xticks([XlimInf1,PercRainHigh[0],PercRainHigh[1],PercRainHigh[2],XlimSup1])
            xRainHigh.set_xticklabels([f'{XlimInf1:.2f}mm',f'{PercRainHigh[0]:.0f}mm',f'{PercRainHigh[1]:.0f}mm',f'{PercRainHigh[2]:.0f}mm',f'{XlimSup1:.2f}mm'], color="#000000", fontsize=14, fontname=fuente)
            for p, val, col in zip(Percentiles,PercRainHigh,ColorPerc):
                xRainHigh.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufRainHigh = io.BytesIO()
            plt.savefig(bufRainHigh, format="png", bbox_inches="tight", transparent=True)
            plt.close(figRainHigh)
            src_hist_rain_high = f"data:image/png;base64,{base64.b64encode(bufRainHigh.getvalue()).decode('utf-8')}"
            BloqueRainHigh = html.Div([
                html.Img(src=src_hist_rain_high, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_rain_high',style={'color': "#000000", 'fontSize': '16px'},children=['Precipitacion Pluvial Maxima mm']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{VectorETRainM[2]:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaRainHigh:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaRainHigh:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionRainHigh:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza1:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionRainHighNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Medios: {Fechas[IndiceMaxRainHigh + Pos1]}',f', : {Fechas[IndiceMinRainHigh + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxRainHigh:.0f}mm',f',: {DatoMinRainHigh:.0f}mm',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa1:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para Medios: CD:{Pearson1:.4f}',f',CC:{r1:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercRainHigh[0]:.0f}mm',f'\tP{Percentiles[1]}: {PercRainHigh[1]:.0f}mm',f'\tP{Percentiles[2]}: {PercRainHigh[2]:.0f}mm'
                ],style={'textAlign': 'center'})
                ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            return BloqueETRain,None,BloqueRainRainHigh, BloqueET,None,BloqueRain,BloqueRainHigh, None,None,None, None,None,None,None
        
        if (opcion == "DatosSol"):
            SolarRad = 46;  HighSolarRad = 47;
            SolarE = 48;    UVIndex = 49;   HighUVIndex = 50;   UVDose = 51;
            HeatD = 52;     CoolD = 53;

            VectorSolarRad = [];  VectorSolarEnergy = [];   VectorDegree = [];  VectorUVIndex = []
            #Inicio y Final del indice
            i = SolarRad; Ante = CoolD;
            #Marcos color plata y bordes gruesos
            plt.rcParams['axes.edgecolor'] = "#000000"    
            plt.rcParams['axes.linewidth'] = 3.0
            while(i <= Ante):
                #Datos de la fila del Mes seleccionado
                DatosFilas = df.iloc[Pos1:Pos2, i].tolist()
                #Datos de la columna del rango de filas
                Datos = [x.item() if hasattr(x, 'item') else x for x in DatosFilas]
                #Verificar integridad de los datos
                Indice = list(range(0, len(Datos)))
                if(i == SolarRad or i == HighSolarRad):
                    Curva.InterpolacionLinealNoGraph(Datos, Indice, len(Datos))
                    Datos = [float(i) for i in Datos]
                    VectorSolarRad.append(Datos)
                    i = i + 1;
                elif(i == SolarE):
                    Curva.InterpolacionLinealNoGraph(Datos, Indice, len(Datos))
                    Datos = [float(i) for i in Datos]
                    VectorSolarEnergy.append(Datos)
                    i = i + 1;
                #Temperatura vs Humedad Minimas
                elif(i == UVIndex or i == HighUVIndex):
                    VectorUVIndex.append(Datos)
                    i = i + 1;
                elif(i == UVDose):
                    i = i + 1;
                elif(i == HeatD or i == CoolD):
                    VectorDegree.append(Datos)
                    i = i + 1;

            ############################################
            ###                                      ###
            ###     Grafica de la Radiacion Solar    ###
            ###                                      ###
            ############################################

            IndiceBarrasSolar = [f"Solar Rad",f"Solar Rad High"]
            MediaSolarRad = Stats.MediaVector(VectorSolarRad[0]);    MediaSolarRadHigh = Stats.MediaVector(VectorSolarRad[1])
            figSolarRad = go.Figure()
            figSolarRad.add_trace(go.Bar(x=[IndiceBarrasSolar[0]],y=[MediaSolarRad],
                name='Solar Rad',marker=dict(color='#F6FF00',line=dict(color='#B5B521', width=2.5)),
                opacity=0.9,text=[f"{MediaSolarRad:.1f}W/m2"],textposition='outside',textfont=dict(color="#F6FF00", size=12, weight='bold')))
            figSolarRad.add_trace(go.Bar(x=[IndiceBarrasSolar[1]],y=[MediaSolarRadHigh],
                name='Solar Rad High',marker=dict(color='#FE7B00',line=dict(color='#905D0C', width=2.5)),
                opacity=0.9,text=[f"{MediaSolarRadHigh:.1f}W/m2"],textposition='outside',textfont=dict(color="#FE7B00", size=12, weight='bold')))
            figSolarRad.update_layout(width=420,height=320,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(range=[0, 250],tickvals=[0, 50, 100, 150, 200, 250],ticktext=['0 W/m2', '50 W/m2', '100 W/m2', '150 W/m2', '200 W/m2', '250 W/m2'],
                tickfont=dict(color="#000000", size=14),showgrid=False),
                xaxis=dict(tickfont=dict(color="#000000", size=11),showgrid=False),
                margin=dict(l=45, r=15, t=30, b=40),showlegend=False)
            BloqueSolarSolarRad = html.Div([
                html.Label(id='input-titulo-solar-solar-rad-high',style={'color': "#000000", 'fontSize': '16px'}, children=['Radiacion Solar y picos W/m2']),
                dcc.Graph(id='grafico-solar-solar-rad-high',figure=figSolarRad,config={'displayModeBar': False},style={'margin': '0 auto', 'display': 'block'})
            ], style={'width': '440px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            
            ##########################################
            ###                                    ###
            ###     Grafica de la Energia Solar    ###
            ###                                    ###
            ##########################################

            IndiceBarrasSolar = [f"Solar Energy"]
            MediaSolarE = Stats.MediaVector(VectorSolarEnergy[0]);
            figSolarE = go.Figure()
            figSolarE.add_trace(go.Bar(x=[IndiceBarrasSolar[0]],y=[MediaSolarE],
                name='Solar Energy',marker=dict(color='#FF4400',line=dict(color='#B52121', width=2.5)),
                opacity=0.9,text=[f"{MediaSolarRad:.1f}W/m2"],textposition='outside',textfont=dict(color="#FF4400", size=12, weight='bold')))
            figSolarE.update_layout(width=420,height=320,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(range=[1.1, 1.9],tickvals=[1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9],ticktext=['1.1Ly', '1.2Ly', '1.3Ly', '1.4Ly', '1.5Ly', '1.6Ly', '1.7Ly', '1.8Ly', '1.9Ly'],
                tickfont=dict(color="#000000", size=14),showgrid=False),
                xaxis=dict(tickfont=dict(color="#000000", size=11),showgrid=False),
                margin=dict(l=45, r=15, t=30, b=40),showlegend=False)
            BloqueSolarEnergy = html.Div([
                html.Label(id='input-titulo-solar-energy',style={'color': "#000000", 'fontSize': '16px'}, children=['Radiacion Solar y picos W/m2']),
                dcc.Graph(id='grafico-solar-energy',figure=figSolarE,config={'displayModeBar': False},style={'margin': '0 auto', 'display': 'block'})
            ], style={'width': '440px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})

            ###########################
            ###                     ###
            ###     Histogramas     ###
            ###                     ###
            ###########################

            #Histrograma Radiacion Solar
            y3 = VectorSolarRad[0];         y4 = VectorSolarRad[1];
            Media3,VarianzaInsesgadaSolarRad,Varianza3,DesviacionSolarRadNM,DatoMaxSolarRad,IndiceMaxSolarRad,DatoMinSolarRad,IndiceMinSolarRad,DatoModa3 = Curva.DatosHTML(y3)
            Media4,VarianzaInsesgadaSolarRadHigh,Varianza4,DesviacionSolarRadHighNM,DatoMaxSolarRadHigh,IndiceMaxSolarRadHigh,DatoMinSolarRadHigh,IndiceMinSolarRadHigh,DatoModa4 = Curva.DatosHTML(y4)
            Stats.timsort(y3);                      Stats.timsort(y4);
            Mediana3 = Stats.MedianaVector(y3);     Mediana4 = Stats.MedianaVector(y4);
            DesviacionSolarRad = Stats.DesviacionNewton(VarianzaInsesgadaSolarRad);
            DesviacionSolarRadHigh = Stats.DesviacionNewton(VarianzaInsesgadaSolarRadHigh);
            Pearson3, r3 = Curva.RegresionLinealHTML(y3, VarianzaInsesgadaSolarRadHigh)
            Pearson4, r4 = Curva.RegresionLinealHTML(y4, VarianzaInsesgadaSolarRadHigh)
            PercExtSolarRad = Stats.Percentil(y3, Percentiles);
            PercExtSolarRadHigh = Stats.Percentil(y4, Percentiles);
            figHist_SolarRad, xHist_SolarRad = plt.subplots(figsize=(10, 6));
            figHist_SolarRad.patch.set_alpha(0.0);  xHist_SolarRad.patch.set_alpha(0.0);
            XlimInf2 = y3[0];    XlimSup2 = y4[len(y4) - 1];  Rango = int(RegladeSturges(len(y3) - 1));
            xHist_SolarRad.hist(y3, bins=Rango,rwidth = 1.2, color = '#F6FF00',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHist_SolarRad.hist(y4, bins=Rango,rwidth = 1.2, color = '#FE7B00',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHist_SolarRad.set_xticks([XlimInf2,PercExtSolarRad[0],PercExtSolarRad[1],PercExtSolarRad[2],PercExtSolarRadHigh[0],PercExtSolarRadHigh[1],PercExtSolarRadHigh[2],XlimSup2])
            xHist_SolarRad.set_xticklabels([f'{XlimInf2:.2f}W/m2',f'{PercExtSolarRad[0]:.0f}W/m2',f'{PercExtSolarRad[1]:.0f}W/m2',f'{PercExtSolarRad[2]:.0f}W/m2',f'{PercExtSolarRadHigh[0]:.0f}W/m2',f'{PercExtSolarRadHigh[1]:.0f}W/m2',f'{PercExtSolarRadHigh[2]:.0f}W/m2',f'{XlimSup2:.2f}W/m2'], color="#000000", fontsize=14, fontname=fuente)
            xHist_SolarRad.set_xlim(XlimInf2 - 1, XlimSup2 + 1)
            for p, val, col in zip(Percentiles,PercExtSolarRad,ColorPerc):
                xHist_SolarRad.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            for p, val, col in zip(Percentiles,PercExtSolarRadHigh,ColorPerc):
                xHist_SolarRad.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistSolarRad = io.BytesIO()
            plt.savefig(bufHistSolarRad, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHist_SolarRad)
            src_hist_solar_high_rad = f"data:image/png;base64,{base64.b64encode(bufHistSolarRad.getvalue()).decode('utf-8')}"
            BloqueSolarRadHigh = html.Div([
                html.Img(src=src_hist_solar_high_rad, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-hist_solar_rad_high',style={'color': "#000000", 'fontSize': '16px'},children=['Radiación Solar W/m2']),
                html.P([
                    html.Strong('Medias Aritméticas'),html.Br(),
                    f'Para medias: {Media3:.4f}',f'\tPara maximas: {Media4:.4f}',html.Br(),
                    html.Strong('Medianas'),html.Br(),
                    f'Para medias: {Mediana3:.0f}',f'\tPara maximas: {Mediana4:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'Para medias: {VarianzaInsesgadaSolarRad:.4f}',f'\tPara maximas: {VarianzaInsesgadaSolarRadHigh:.4f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'Para medias: {DesviacionSolarRad:.4f}',f'\tPara maximas: {DesviacionSolarRadHigh:.4f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'Para medias: {Varianza3:.4f}',f'\tPara maximas: {Varianza4:.4f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'Para medias: {DesviacionSolarRadNM:.4f}',f'\tPara maximas: {DesviacionSolarRadHighNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Maximas: {Fechas[IndiceMaxSolarRad + Pos1]}',f', : {Fechas[IndiceMinSolarRad + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxSolarRad:.0f}W/m2',f',: {DatoMinSolarRad:.0f}W/m2',html.Br(),
                    f'Fecha Minimos: {Fechas[IndiceMaxSolarRadHigh + Pos1]}',f', : {Fechas[IndiceMinSolarRadHigh + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxSolarRadHigh:.0f}W/m2',f',: {DatoMinSolarRadHigh:.0f}W/m2',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para medias: {DatoModa3:.0f}',f'\tPara maximas: {DatoModa4:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para Medios: CD:{Pearson3:.4f}',f',CC:{r3:.4f}',html.Br(),
                    f'Para Minimas: CD:{Pearson4:.4f}',f',CC:{r4:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Medias: P{Percentiles[0]}: {PercExtSolarRad[0]:.0f}W/m2',f'\tP{Percentiles[1]}: {PercExtSolarRad[1]:.0f}W/m2',f'\tP{Percentiles[2]}: {PercExtSolarRad[2]:.0f}W/m2',html.Br(),
                    f'Maximas: P{Percentiles[0]}: {PercExtSolarRadHigh[0]:.0f}W/m2',f'\tP{Percentiles[1]}: {PercExtSolarRadHigh[1]:.0f}W/m2',f'\tP{Percentiles[2]}: {PercExtSolarRadHigh[2]:.0f}W/m2'
                ])
                ], style={'width': '420px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})

            #Histograma Solar Energy
            figHistSolarEnergy, xHistSolarEnergy = plt.subplots(figsize=(10, 6));   y1 = VectorSolarEnergy[0];
            Media1,VarianzaInsesgadaHistSolarEnergy,Varianza1,DesviacionHistSolarEnergyNM,DatoMaxSolarEnergy,IndiceMaxSolarEnergy,DatoMinSolarEnergy,IndiceMinSolarEnergy,DatoModa1 = Curva.DatosHTML(y1)
            Stats.timsort(y1);  MedianaHistSolarEnergy = Stats.MedianaVector(y1);
            DesviacionHistSolarEnergy = Stats.DesviacionNewton(VarianzaInsesgadaHistSolarEnergy);
            Pearson1, r1 = Curva.RegresionLinealHTML(y1, VarianzaInsesgadaHistSolarEnergy)
            PercHistSolarEnergy = Stats.Percentil(y1, Percentiles);
            figHistSolarEnergy.patch.set_alpha(0.0);  xHistSolarEnergy.patch.set_alpha(0.0);
            XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
            xHistSolarEnergy.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = 'black', color="#FF4400",linewidth=4.0, alpha=0.6)
            xHistSolarEnergy.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
            xHistSolarEnergy.set_xticks([XlimInf1,PercHistSolarEnergy[0],PercHistSolarEnergy[1],PercHistSolarEnergy[2],XlimSup1])
            xHistSolarEnergy.set_xticklabels([f'{XlimInf1:.2f}Ly',f'{PercHistSolarEnergy[0]:.0f}Ly',f'{PercHistSolarEnergy[1]:.0f}Ly',f'{PercHistSolarEnergy[2]:.0f}Ly',f'{XlimSup1:.2f}Ly'], color="#000000", fontsize=14, fontname=fuente)
            for p, val, col in zip(Percentiles,PercHistSolarEnergy,ColorPerc):
                xHistSolarEnergy.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistSolarEnergy = io.BytesIO()
            plt.savefig(bufHistSolarEnergy, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistSolarEnergy)
            src_hist_solar_energy = f"data:image/png;base64,{base64.b64encode(bufHistSolarEnergy.getvalue()).decode('utf-8')}"
            BloqueHistSolarEnergy = html.Div([
                html.Img(src=src_hist_solar_energy, style={'width': '300px', 'height': '300px'}),
                html.Label(id='input-solar-energy',style={'color': "#000000", 'fontSize': '16px'},children=['Energia Solar Ly']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{MediaSolarE:.4f}',html.Br(),
                    html.Strong('Mediana'),html.Br(),
                    f'{MedianaHistSolarEnergy:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'{VarianzaInsesgadaHistSolarEnergy:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'{DesviacionHistSolarEnergy:.8f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'{Varianza1:.8f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'{DesviacionHistSolarEnergyNM:.4f}',html.Br(),
                    html.Strong('Valores Maximos y Minimos'),html.Br(),
                    f'Fecha Medios: {Fechas[IndiceMaxSolarEnergy + Pos1]}',f', : {Fechas[IndiceMinSolarEnergy + Pos1]}',html.Br(),
                    f'Datos: {DatoMaxSolarEnergy:.0f}Ly',f',: {DatoMinSolarEnergy:.0f}Ly',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa1:.0f}',html.Br(),
                    html.Strong('Coeficientes'),html.Br(),
                    f'Para Medios: CD:{Pearson1:.4f}',f',CC:{r1:.4f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercHistSolarEnergy[0]:.0f}Ly',f'\tP{Percentiles[1]}: {PercHistSolarEnergy[1]:.0f}Ly',f'\tP{Percentiles[2]}: {PercHistSolarEnergy[2]:.0f}Ly'
                ])
                ], style={'width': '420px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
            if(estacion == '0'):
                
                ########################################
                ###                                  ###
                ###     Grafica de los grados-dia    ###
                ###                                  ###
                ########################################

                Curva.InterpolacionLinealNoGraph(VectorDegree[0], Indice, len(VectorDegree[0]))
                VectorDegree[0] = [float(i) for i in VectorDegree[0]]
                Curva.InterpolacionLinealNoGraph(VectorDegree[1], Indice, len(VectorDegree[1]))
                VectorDegree[1] = [float(i) for i in VectorDegree[1]]
                MediaDegreeHeat = Stats.MediaVector(VectorDegree[0]);    MediaDegreeCool = Stats.MediaVector(VectorDegree[1])
                IndiceBarrasDobleAxial = ["Calefación","Refrigeración"]
                figDegree = go.Figure()
                figDegree.add_trace(go.Bar(x=[IndiceBarrasDobleAxial[0]],y=[MediaDegreeHeat],
                    name='Calefacion',marker=dict(color='#F99462',line=dict(color='#F76A25', width=6)),
                    opacity=0.9,text=[f"{MediaDegreeCool}"],
                    textposition='outside',textfont=dict(color="#F76A25", size=12, family='sans-serif')
                ))
                figDegree.add_trace(go.Bar(x=[IndiceBarrasDobleAxial[1]],y=[MediaDegreeCool],
                    name='Refrigeración',yaxis='y2',marker=dict(color='#8ED7FB',line=dict(color="#01476B", width=6)),
                    opacity=0.9,text=[f"{MediaDegreeCool}"],
                    textposition='outside',textfont=dict(color="#01476B", size=12, family='sans-serif')
                ))
                figDegree.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(
                        title=dict(text="Temperatura | Humedad",font=dict(color="#000000", size=16)),
                        tickfont=dict(color="#000000", size=14),showgrid=False
                    ),
                    yaxis=dict(
                        title=dict(text='Temperatura Interior (°C)',font=dict(color="#000000", size=16)),range=[0, 35],
                        tickvals=[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15],ticktext=['0.010', '0.020', '0.030', '0.040', '0.050', '0.060', '0.070', '0.080', '0.090', '0.100', '0.110', '0.120', '0.130', '0.140', '0.150'],
                        tickfont=dict(color='#F76A25', size=14),showgrid=False
                    ),
                    yaxis2=dict(
                        title=dict(text='Humedad Interior (%)',font=dict(color="#000000", size=16)),range=[0, 100],
                        tickvals=[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15],ticktext=['0.010', '0.020', '0.030', '0.040', '0.050', '0.060', '0.070', '0.080', '0.090', '0.100', '0.110', '0.120', '0.130', '0.140', '0.150'],
                        tickfont=dict(color='#01476B', size=14),overlaying='y',side='right',showgrid=False
                    ),
                    margin=dict(l=60, r=60, t=30, b=60),showlegend=False,width=280,height=320
                )
                BloqueDegree = html.Div([
                    html.Label(id='input-titulo-degree-heat-cool',style={'color': "#000000", 'fontSize': '16px'},children=['Grados-día']),
                    dcc.Graph(id='grafico-degree-heat-cool',figure=figDegree,config={'displayModeBar': False})
                ], style={'width': '360px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                    'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})

                #Histograma Degree Calefaccion
                figHistDegreeHeat, xHistDegreeHeat = plt.subplots(figsize=(10, 6));     y1 = VectorDegree[0];
                Media1,VarianzaInsesgadaHistDegreeHeat,Varianza1,DesviacionHistDegreeHeatNM,DatoMaxDegreeHeat,IndiceMaxDegreeHeat,DatoMinDegreeHeat,IndiceMinDegreeHeat,DatoModa1 = Curva.DatosHTML(y1)
                Stats.timsort(y1);  MedianaHistDegreeHeat = Stats.MedianaVector(y1);
                DesviacionHistDegreeHeat = Stats.DesviacionNewton(VarianzaInsesgadaHistDegreeHeat);
                #Pearson1, r1 = Curva.RegresionLinealHTML(y1, VarianzaInsesgadaHistDegreeHeat)
                PercHistDegreeHeat = Stats.Percentil(y1, Percentiles);
                figHistDegreeHeat.patch.set_alpha(0.0);  xHistDegreeHeat.patch.set_alpha(0.0);
                XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
                xHistDegreeHeat.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = 'black', color="#EA8D00",linewidth=4.0, alpha=0.6)
                xHistDegreeHeat.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
                xHistDegreeHeat.set_xticks([XlimInf1,PercHistDegreeHeat[0],PercHistDegreeHeat[1],PercHistDegreeHeat[2],XlimSup1])
                xHistDegreeHeat.set_xticklabels([f'{XlimInf1:.2f}',f'{PercHistDegreeHeat[0]:.0f}',f'{PercHistDegreeHeat[1]:.0f}',f'{PercHistDegreeHeat[2]:.0f}',f'{XlimSup1:.2f}'], color="#000000", fontsize=14, fontname=fuente)
                for p, val, col in zip(Percentiles,PercHistDegreeHeat,ColorPerc):
                    xHistDegreeHeat.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
                #Codificar
                bufHistDegreeHeat = io.BytesIO()
                plt.savefig(bufHistDegreeHeat, format="png", bbox_inches="tight", transparent=True)
                plt.close(figHistDegreeHeat)
                src_hist_degree_heat = f"data:image/png;base64,{base64.b64encode(bufHistDegreeHeat.getvalue()).decode('utf-8')}"
                BloqueHistDegreeHeat = html.Div([
                    html.Img(src=src_hist_degree_heat, style={'width': '300px', 'height': '300px'}),
                    html.Label(id='input-hist_degree-heat',style={'color': "#000000", 'fontSize': '16px'},children=['Calefacción']),
                    html.P([
                        html.Strong('Media Aritmética'),html.Br(),
                        f'{MediaDegreeHeat:.4f}',html.Br(),
                        html.Strong('Mediana'),html.Br(),
                        f'{MedianaHistDegreeHeat:.0f}',html.Br(),
                        html.Strong('Varianza Insesgada'),html.Br(),
                        f'{VarianzaInsesgadaHistDegreeHeat:.8f}',html.Br(),
                        html.Strong('Desviacion Estandar'),html.Br(),
                        f'{DesviacionHistDegreeHeat:.8f}',html.Br(),
                        html.Strong('Varianza Sesgada'),html.Br(),
                        f'{Varianza1:.8f}',html.Br(),
                        html.Strong('Desviacion Estandar sin Media'),html.Br(),
                        f'{DesviacionHistDegreeHeatNM:.4f}',html.Br(),
                        html.Strong('Valores Maximos y Minimos'),html.Br(),
                        f'Fecha Medios: {Fechas[IndiceMaxDegreeHeat + Pos1]}',f', : {Fechas[IndiceMinDegreeHeat + Pos1]}',html.Br(),
                        f'Datos: {DatoMaxDegreeHeat:.0f}Ly',f',: {DatoMinDegreeHeat:.0f}Ly',html.Br(),
                        html.Strong('Moda de los datos'),html.Br(),
                        f'{DatoModa1:.0f}',html.Br(),
                        #html.Strong('Coeficientes'),html.Br(),
                        #f'Para Medios: CD:{Pearson1:.4f}',f',CC:{r1:.4f}',html.Br(),
                        html.Strong('Percentiles'),html.Br(),
                        f'P{Percentiles[0]}: {PercHistDegreeHeat[0]:.0f}',f'\tP{Percentiles[1]}: {PercHistDegreeHeat[1]:.0f}',f'\tP{Percentiles[2]}: {PercHistDegreeHeat[2]:.0f}'
                    ],style={'textAlign': 'center'})
                    ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                    'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
                #Histograma Degree Refrigeration
                figHistDegreeCool, xHistDegreeCool = plt.subplots(figsize=(10, 6));     y1 = VectorDegree[1];
                Media1,VarianzaInsesgadaHistDegreeCool,Varianza1,DesviacionHistDegreeCoolNM,DatoMaxDegreeCool,IndiceMaxDegreeCool,DatoMinDegreeCool,IndiceMinDegreeCool,DatoModa1 = Curva.DatosHTML(y1)
                Stats.timsort(y1);      MedianaHistDegreeCool = Stats.MedianaVector(y1);
                DesviacionHistDegreeCool = Stats.DesviacionNewton(VarianzaInsesgadaHistDegreeCool);
                #Pearson1, r1 = Curva.RegresionLinealHTML(y1, VarianzaInsesgadaHistDegreeHeat)
                PercHistDegreeCool = Stats.Percentil(y1, Percentiles);
                figHistDegreeCool.patch.set_alpha(0.0);  xHistDegreeCool.patch.set_alpha(0.0);
                XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
                xHistDegreeCool.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = 'black', color="#8ED7FB",linewidth=4.0, alpha=0.6)
                xHistDegreeCool.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
                xHistDegreeCool.set_xticks([XlimInf1,PercHistDegreeCool[0],PercHistDegreeCool[1],PercHistDegreeCool[2],XlimSup1])
                xHistDegreeCool.set_xticklabels([f'{XlimInf1:.2f}',f'{PercHistDegreeCool[0]:.0f}',f'{PercHistDegreeCool[1]:.0f}',f'{PercHistDegreeCool[2]:.0f}',f'{XlimSup1:.2f}'], color="#000000", fontsize=14, fontname=fuente)
                for p, val, col in zip(Percentiles,PercHistDegreeCool,ColorPerc):
                    xHistDegreeCool.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
                #Codificar
                bufHistDegreeCool = io.BytesIO()
                plt.savefig(bufHistDegreeCool, format="png", bbox_inches="tight", transparent=True)
                plt.close(figHistDegreeCool)
                src_hist_degree_cool = f"data:image/png;base64,{base64.b64encode(bufHistDegreeCool.getvalue()).decode('utf-8')}"
                BloqueHistDegreeCool = html.Div([
                    html.Img(src=src_hist_degree_cool, style={'width': '300px', 'height': '300px'}),
                    html.Label(id='input-hist_degree-cool',style={'color': "#000000", 'fontSize': '16px'},children=['Refrigeracion']),
                    html.P([
                        html.Strong('Media Aritmética'),html.Br(),
                        f'{MediaDegreeCool:.4f}',html.Br(),
                        html.Strong('Mediana'),html.Br(),
                        f'{MedianaHistDegreeCool:.0f}',html.Br(),
                        html.Strong('Varianza Insesgada'),html.Br(),
                        f'{VarianzaInsesgadaHistDegreeCool:.8f}',html.Br(),
                        html.Strong('Desviacion Estandar'),html.Br(),
                        f'{DesviacionHistDegreeCool:.8f}',html.Br(),
                        html.Strong('Varianza Sesgada'),html.Br(),
                        f'{Varianza1:.8f}',html.Br(),
                        html.Strong('Desviacion Estandar sin Media'),html.Br(),
                        f'{DesviacionHistDegreeCoolNM:.4f}',html.Br(),
                        html.Strong('Valores Maximos y Minimos'),html.Br(),
                        f'Fecha Medios: {Fechas[IndiceMaxDegreeCool + Pos1]}',f', : {Fechas[IndiceMinDegreeCool + Pos1]}',html.Br(),
                        f'Datos: {DatoMaxDegreeCool:.0f}Ly',f',: {DatoMinDegreeCool:.0f}Ly',html.Br(),
                        html.Strong('Moda de los datos'),html.Br(),
                        f'{DatoModa1:.0f}',html.Br(),
                        #html.Strong('Coeficientes'),html.Br(),
                        #f'Para Medios: CD:{Pearson1:.4f}',f',CC:{r1:.4f}',html.Br(),
                        html.Strong('Percentiles'),html.Br(),
                        f'P{Percentiles[0]}: {PercHistDegreeCool[0]:.0f}',f'\tP{Percentiles[1]}: {PercHistDegreeCool[1]:.0f}',f'\tP{Percentiles[2]}: {PercHistDegreeCool[2]:.0f}'
                    ],style={'textAlign': 'center'})
                    ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                    'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
                return BloqueSolarSolarRad,BloqueSolarEnergy,BloqueDegree, BloqueSolarRadHigh,BloqueHistSolarEnergy,BloqueHistDegreeHeat,BloqueHistDegreeCool, None,None,None, None,None,None,None
            elif(estacion == '1'):

                ##################################
                ###                            ###
                ###     Grafica de rayos UV    ###
                ###                            ###
                ##################################

                Curva.InterpolacionLinealNoGraph(VectorUVIndex[0], Indice, len(VectorUVIndex[0]))
                VectorUVIndex[0] = [float(i) for i in VectorUVIndex[0]]
                Curva.InterpolacionLinealNoGraph(VectorUVIndex[1], Indice, len(VectorUVIndex[1]))
                VectorUVIndex[1] = [float(i) for i in VectorUVIndex[1]]
                IndiceBarrasDobleAxial = ["UV Index","UV High Index"]
                MediaUVIndex = Stats.MediaVector(VectorUVIndex[0]);    MediaHighUVIndex = Stats.MediaVector(VectorUVIndex[1])

                figDegree = go.Figure()
                figDegree.add_trace(go.Bar(x=[IndiceBarrasDobleAxial[0]],y=[MediaUVIndex],
                    name='UV Index',marker=dict(color='#F99462',line=dict(color='#F76A25', width=6)),
                    opacity=0.9,text=[f"{MediaUVIndex}"],
                    textposition='outside',textfont=dict(color="#F76A25", size=12, family='sans-serif')
                ))
                figDegree.add_trace(go.Bar(x=[IndiceBarrasDobleAxial[1]],y=[MediaHighUVIndex],
                    name='UV Index High',yaxis='y2',marker=dict(color='#8ED7FB',line=dict(color="#01476B", width=6)),
                    opacity=0.9,text=[f"{MediaHighUVIndex}"],
                    textposition='outside',textfont=dict(color="#01476B", size=12, family='sans-serif')
                ))
                figDegree.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(
                        title=dict(text="UV Index",font=dict(color="#000000", size=16)),
                        tickfont=dict(color="#000000", size=14),showgrid=False
                    ),
                    yaxis=dict(
                        title=dict(text='Radiacion Ultravioleta',font=dict(color="#000000", size=16)),
                        #tickvals=[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15],ticktext=['0.010', '0.020', '0.030', '0.040', '0.050', '0.060', '0.070', '0.080', '0.090', '0.100', '0.110', '0.120', '0.130', '0.140', '0.150'],
                        tickfont=dict(color='#F76A25', size=14),showgrid=False
                    ),
                    yaxis2=dict(
                        title=dict(text='Radiacion Ultravioleta Pico',font=dict(color="#000000", size=16)),
                        #tickvals=[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15],ticktext=['0.010', '0.020', '0.030', '0.040', '0.050', '0.060', '0.070', '0.080', '0.090', '0.100', '0.110', '0.120', '0.130', '0.140', '0.150'],
                        tickfont=dict(color='#01476B', size=14),overlaying='y',side='right',showgrid=False
                    ),
                    margin=dict(l=60, r=60, t=30, b=60),showlegend=False,width=280,height=320
                )
                BloqueUVIndex = html.Div([
                    html.Label(id='input-titulo-uv-index',style={'color': "#000000", 'fontSize': '16px'},children=['Radiación Ultravioleta entrante']),
                    dcc.Graph(id='grafico-uv-index',figure=figDegree,config={'displayModeBar': False})
                ], style={'width': '300px','height': '380px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                    'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
                
                #Histograma UVIndex
                figUVIndex, xUVIndex = plt.subplots(figsize=(10, 6));       y1 = VectorUVIndex[0];
                Media1,VarianzaInsesgadaHistUVIndex,Varianza1,DesviacionHistUVIndexNM,DatoMaxUVIndex,IndiceMaxUVIndex,DatoMinUVIndex,IndiceMinUVIndex,DatoModa1 = Curva.DatosHTML(y1)
                Stats.timsort(y1);      MedianaHistUVIndex = Stats.MedianaVector(y1);
                DesviacionHistUVIndex = Stats.DesviacionNewton(VarianzaInsesgadaHistUVIndex);
                #Pearson1, r1 = Curva.RegresionLinealHTML(y1, VarianzaInsesgadaHistUVIndex)
                PercHistUVIndex = Stats.Percentil(y1, Percentiles);
                figUVIndex.patch.set_alpha(0.0);  xUVIndex.patch.set_alpha(0.0);
                XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
                xUVIndex.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = 'black', color="#8ED7FB",linewidth=4.0, alpha=0.6)
                xUVIndex.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
                xUVIndex.set_xticks([XlimInf1,PercHistUVIndex[0],PercHistUVIndex[1],PercHistUVIndex[2],XlimSup1])
                xUVIndex.set_xticklabels([f'{XlimInf1:.2f}',f'{PercHistUVIndex[0]:.0f}',f'{PercHistUVIndex[1]:.0f}',f'{PercHistUVIndex[2]:.0f}',f'{XlimSup1:.2f}'], color="#000000", fontsize=14, fontname=fuente)
                for p, val, col in zip(Percentiles,PercHistUVIndex,ColorPerc):
                    xUVIndex.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
                #Codificar
                bufHistUVIndex = io.BytesIO()
                plt.savefig(bufHistUVIndex, format="png", bbox_inches="tight", transparent=True)
                plt.close(figUVIndex)
                src_hist_uv_index = f"data:image/png;base64,{base64.b64encode(bufHistUVIndex.getvalue()).decode('utf-8')}"
                BloqueHistUVIndex = html.Div([
                    html.Img(src=src_hist_uv_index, style={'width': '100%', 'height': '300px'}),
                    html.Label(id='input-hist_uv-index',style={'color': "#000000", 'fontSize': '16px'},children=['Radiacion Ultravioleta']),
                    html.P([
                        html.Strong('Media Aritmética'),html.Br(),
                        f'{MediaUVIndex:.4f}',html.Br(),
                        html.Strong('Mediana'),html.Br(),
                        f'{MedianaHistUVIndex:.0f}',html.Br(),
                        html.Strong('Varianza Insesgada'),html.Br(),
                        f'{VarianzaInsesgadaHistUVIndex:.8f}',html.Br(),
                        html.Strong('Desviacion Estandar'),html.Br(),
                        f'{DesviacionHistUVIndex:.8f}',html.Br(),
                        html.Strong('Varianza Sesgada'),html.Br(),
                        f'{Varianza1:.8f}',html.Br(),
                        html.Strong('Desviacion Estandar sin Media'),html.Br(),
                        f'{DesviacionHistUVIndexNM:.4f}',html.Br(),
                        html.Strong('Valores Maximos y Minimos'),html.Br(),
                        f'Fecha Medios: {Fechas[IndiceMaxUVIndex + Pos1]}',f', : {Fechas[IndiceMinUVIndex + Pos1]}',html.Br(),
                        f'Datos: {DatoMaxUVIndex:.0f}',f',: {DatoMinUVIndex:.0f}',html.Br(),
                        html.Strong('Moda de los datos'),html.Br(),
                        f'{DatoModa1:.0f}',html.Br(),
                        #html.Strong('Coeficientes'),html.Br(),
                        #f'Para Medios: CD:{Pearson1:.4f}',f',CC:{r1:.4f}',html.Br(),
                        html.Strong('Percentiles'),html.Br(),
                        f'P{Percentiles[0]}: {PercHistUVIndex[0]:.0f}',f'\tP{Percentiles[1]}: {PercHistUVIndex[1]:.0f}',f'\tP{Percentiles[2]}: {PercHistUVIndex[2]:.0f}'
                    ],style={'textAlign': 'center'})
                    ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                    'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
                #Histograma UV Index High
                figUVIndexHigh, xUVIndexHigh = plt.subplots(figsize=(10, 6));       y1 = VectorUVIndex[1];
                Media1,VarianzaInsesgadaHistUVIndexHigh,Varianza1,DesviacionHistUVIndexHighNM,DatoMaxUVIndexHigh,IndiceMaxUVIndexHigh,DatoMinUVIndexHigh,IndiceMinUVIndexHigh,DatoModa1 = Curva.DatosHTML(y1)
                Stats.timsort(y1);      MedianaHistUVIndexHigh = Stats.MedianaVector(y1);
                DesviacionHistUVIndexHigh = Stats.DesviacionNewton(VarianzaInsesgadaHistUVIndexHigh);
                #Pearson1, r1 = Curva.RegresionLinealHTML(y1, VarianzaInsesgadaHistUVIndexHigh)
                PercHistUVIndexHigh = Stats.Percentil(y1, Percentiles);
                figUVIndexHigh.patch.set_alpha(0.0);  xUVIndexHigh.patch.set_alpha(0.0);
                XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
                xUVIndexHigh.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = 'black', color="#8ED7FB",linewidth=4.0, alpha=0.6)
                xUVIndexHigh.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
                xUVIndexHigh.set_xticks([XlimInf1,PercHistUVIndexHigh[0],PercHistUVIndexHigh[1],PercHistUVIndexHigh[2],XlimSup1])
                xUVIndexHigh.set_xticklabels([f'{XlimInf1:.2f}',f'{PercHistUVIndexHigh[0]:.0f}',f'{PercHistUVIndexHigh[1]:.0f}',f'{PercHistUVIndexHigh[2]:.0f}',f'{XlimSup1:.2f}'], color="#000000", fontsize=14, fontname=fuente)
                for p, val, col in zip(Percentiles,PercHistUVIndex,ColorPerc):
                    xUVIndex.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
                #Codificar
                bufHistUVIndexHigh = io.BytesIO()
                plt.savefig(bufHistUVIndexHigh, format="png", bbox_inches="tight", transparent=True)
                plt.close(figUVIndexHigh)
                src_hist_uv_index_high = f"data:image/png;base64,{base64.b64encode(bufHistUVIndexHigh.getvalue()).decode('utf-8')}"
                BloqueHistUVIndexHigh = html.Div([
                    html.Img(src=src_hist_uv_index_high, style={'width': '100%', 'height': '300px'}),
                    html.Label(id='input-hist_uv-index',style={'color': "#000000", 'fontSize': '16px'},children=['Maximos de la Radiacion Ultravioleta']),
                    html.P([
                        html.Strong('Media Aritmética'),html.Br(),
                        f'{MediaHighUVIndex:.4f}',html.Br(),
                        html.Strong('Mediana'),html.Br(),
                        f'{MedianaHistUVIndexHigh:.0f}',html.Br(),
                        html.Strong('Varianza Insesgada'),html.Br(),
                        f'{VarianzaInsesgadaHistUVIndexHigh:.8f}',html.Br(),
                        html.Strong('Desviacion Estandar'),html.Br(),
                        f'{DesviacionHistUVIndexHigh:.8f}',html.Br(),
                        html.Strong('Varianza Sesgada'),html.Br(),
                        f'{Varianza1:.8f}',html.Br(),
                        html.Strong('Desviacion Estandar sin Media'),html.Br(),
                        f'{DesviacionHistUVIndexHighNM:.4f}',html.Br(),
                        html.Strong('Valores Maximos y Minimos'),html.Br(),
                        f'Fecha Medios: {Fechas[IndiceMaxUVIndexHigh + Pos1]}',f', : {Fechas[IndiceMinUVIndexHigh + Pos1]}',html.Br(),
                        f'Datos: {DatoMaxUVIndexHigh:.0f}',f',: {DatoMinUVIndexHigh:.0f}',html.Br(),
                        html.Strong('Moda de los datos'),html.Br(),
                        f'{DatoModa1:.0f}',html.Br(),
                        #html.Strong('Coeficientes'),html.Br(),
                        #f'Para Medios: CD:{Pearson1:.4f}',f',CC:{r1:.4f}',html.Br(),
                        html.Strong('Percentiles'),html.Br(),
                        f'P{Percentiles[0]}: {PercHistUVIndexHigh[0]:.0f}',f'\tP{Percentiles[1]}: {PercHistUVIndexHigh[1]:.0f}',f'\tP{Percentiles[2]}: {PercHistUVIndexHigh[2]:.0f}'
                    ],style={'textAlign': 'center'})
                    ], style={'width': '360px','height': '780px','border': '2px solid #DBDBDB','borderRadius': '8px','padding': '10px','boxSizing': 'border-box',
                    'display': 'inline-flex','flexDirection': 'column','alignItems': 'center','border': '2px solid #000000','justifyContent': 'center','margin': '10px'})
                return BloqueSolarSolarRad,BloqueSolarEnergy,BloqueUVIndex, BloqueSolarRadHigh,BloqueHistSolarEnergy,BloqueHistUVIndex,BloqueHistUVIndexHigh, None,None,None, None,None,None,None
        else:
            return None,None,None, None,None,None,None, None,None,None, None,None,None,None
    

#if __name__ == '__main__':
#    appEstacion.run(debug=True)
if __name__ == '__main__':
    appEstacion.run_server(debug=True)