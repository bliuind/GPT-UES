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
        'backgroundImage': 'url("/assets/fondo_sol.jpg")',  #Imagen De Fondo
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
                            id='dropdown-estacion',
                            options=[
                                {'label': 'Pagina Principal', 'value': '-1'},                           #Opcion 1
                                {'label': 'Estación Metereológica 7GT-EEP', 'value': '0'},              #Opcion 2
                                {'label': 'Estación Metereológica 7GT-UES', 'value': '1'},              #Opcion 3
                            ],
                            value='-1',      # Valor inicial por defecto
                            clearable=False,            # Evita que el usuario deje el menú vacío
                            style={ 'width': '20%', 'color': '#0E94B5' }
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
                                {'label': 'Radiacion Solar', 'value': 'DatosSol'}                           #Opcion 7
                            ],
                            value='TemperaturasI',      # Valor inicial por defecto
                            clearable=False,            # Evita que el usuario deje el menú vacío
                            style={ 'width': '30%', 'color': '#0E94B5' }
                        ),
                        dcc.Dropdown(
                            id='drop-años',
                            options=[{'label': 'Elegir Estacion', 'value': '-1'}],
                            value='-1',      # Valor inicial por defecto
                            clearable=False,            # Evita que el usuario deje el menú vacío
                            style={ 'width': '10%', 'color': '#0E94B5' }
                        ),
                        dcc.Dropdown(
                            id='drop-meses',
                            options=[
                                {'label': 'Escoger Estación', 'value': '-1'}
                            ],
                            value='-1', clearable=False,
                            style={ 'width': '20%', 'color': "#0E94B5" }
                        ),
                        dcc.Dropdown(
                            id='drop-dias',
                            options=[
                                {'label': 'Escoger Estación', 'value': '-1'}
                            ],
                            value='-1', clearable=False,
                            style={ 'width': '20%', 'color': "#0E94B5" }
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
    
            #Grafica de Barras Temperatura
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
            XlimInf = x[0]; XlimSup = x[len(x)-1];     YlimInf = Stats.DatoMinimoVector(y1); YlimSup = Stats.DatoMaximoVector(y1);
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
            XlimInf = x[0]; XlimSup = x[len(x)-1];
            YlimInf = Stats.DatoMinimoVector(y1); YlimSup = Stats.DatoMaximoVector(y1);
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
            XlimInf = x[0]; XlimSup = x[len(x)-1];
            YlimInf = Stats.DatoMinimoVector(y1); YlimSup = Stats.DatoMaximoVector(y1);
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
            XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
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
            XlimInf2 = y2[0];    XlimSup2 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(len(y2) - 1))
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
                    f'{VectorInsTempHum[1]:.4f}',html.Br(),
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
            XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(len(y2) - 1))
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
            XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(len(y2) - 1));
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
            XlimInf2 = y4[0];    XlimSup2 = y4[len(y4) - 1];  Rango4 = int(RegladeSturges(len(y4) - 1))
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
                    f'{VectorInsDewWetHeat[0]:.4f}',html.Br(),
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
            XlimInf2 = y5[0];    XlimSup2 = y5[len(y5) - 1];  Rango5 = int(RegladeSturges(len(y5) - 1))
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
                    f'{VectorInsDewWetHeat[1]:.4f}',html.Br(),
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
            XlimInf2 = y6[0];    XlimSup2 = y6[len(y6) - 1];  Rango6 = int(RegladeSturges(len(y6) - 1))
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
                    f'{VectorInsDewWetHeat[2]:.4f}',html.Br(),
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
            XlimInf2 = y7[0];    XlimSup2 = y7[len(y7) - 1];  Rango7 = int(RegladeSturges(len(y7) - 1))
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
            XlimInf = x[0]; XlimSup = x[len(x)-1];
            YlimInf = Stats.DatoMinimoVector(y1); YlimSup = Stats.DatoMaximoVector(y1);
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
            XlimInf = x[0]; XlimSup = x[len(x)-1];
            YlimInf = Stats.DatoMinimoVector(y1); YlimSup = Stats.DatoMaximoVector(y1);
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
                html.Label(id='input-titulo-dew-wet-ext',style=label_style,children=['Punto de Rocio y Bulbo Humedo °C']),
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
            XlimInf = x[0]; XlimSup = x[len(x)-1];     YlimInf = Stats.DatoMinimoVector(y1); YlimSup = Stats.DatoMaximoVector(y1);
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
            XlimInf = x[0]; XlimSup = x[len(x)-1];     YlimInf = Stats.DatoMinimoVector(y1); YlimSup = Stats.DatoMaximoVector(y1);
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
            XlimInf2 = y1[0];    XlimSup2 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
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
                    f'{VectorExtTempHumM[0]:.4f}',html.Br(),
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
            XlimInf2 = y2[0];    XlimSup2 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(len(y2) - 1))
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
                    f'{VectorExtTempHumM[1]:.4f}',html.Br(),
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
            XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(len(y2) - 1))
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
            XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(len(y2) - 1));
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
            XlimInf2 = y1[0];    XlimSup2 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
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
                    f'{VectorExtDewWetM[0]:.4f}',html.Br(),
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
            XlimInf2 = y2[0];    XlimSup2 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(len(y2) - 1))
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
                    f'{VectorExtDewWetM[1]:.4f}',html.Br(),
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
            XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(len(y2) - 1))
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
            XlimInf2 = y2[0];    XlimSup2 = y3[len(y2) - 1];  Rango = int(RegladeSturges(len(y2) - 1))
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
            XlimInf = x[0]; XlimSup = x[len(x)-1];
            YlimInf = Stats.DatoMinimoVector(y2); YlimSup = Stats.DatoMaximoVector(y1);
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
            XlimInf2 = y1[0];    XlimSup2 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
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
                    f'{VectorPbar[0]:.4f}',html.Br(),
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
            XlimInf2 = y3[0];    XlimSup3 = y3[len(y3) - 1];  Rango3 = int(RegladeSturges(len(y3) - 1))
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
                    f'{VectorPbar[1]:.4f}',html.Br(),
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
            XlimInf2 = y4[0];    XlimSup2 = y4[len(y4) - 1];  Rango4 = int(RegladeSturges(len(y4) - 1))
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
            XlimInf2 = y2[0];    XlimSup2 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(len(y2) - 1))
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
            Colores = ['#3EB1AE', '#0A9E85','#0070AD','#D4068A','#FFBA00','#FF5500','#0026FF']
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
                    style={'width': '50%','backgroundColor':'transparent','border': '3px solid #b5b5b5','margin': '0 auto 40px auto','borderRadius': '10px','fontWeight': 'bold','backgroundImage': 'linear-gradient(135deg, #777 0%, #ccc 25%, #fff 50%, #ccc 75%, #555 100%)',
                           'display': 'inline-block','backgroundClip': 'text','WebkitBackgroundClip': 'text','color': 'transparent','WebkitTextFillColor': 'transparent'},
                    children=[
                        'Direccion del viento prevalescente'
                        ]
                    ),
                html.Img(src=src_prev_wind, style={'width': '300px', 'height': '300px'})
                ],
                style={"width": "100%",'textAlign': 'center'}
            )
            
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
                    style={'width': '50%','backgroundColor':'transparent','border': '3px solid #b5b5b5','margin': '0 auto 40px auto','borderRadius': '10px','fontWeight': 'bold','backgroundImage': 'linear-gradient(135deg, #777 0%, #ccc 25%, #fff 50%, #ccc 75%, #555 100%)',
                           'display': 'inline-block','backgroundClip': 'text','WebkitBackgroundClip': 'text','color': 'transparent','WebkitTextFillColor': 'transparent'},
                    children=[
                        'Direccion del viento promedio'
                        ]
                    ),
                html.Img(src=src_avg_wind, style={'width': '300px', 'height': '300px'})
                ],
                style={"width": "100%",'textAlign': 'center'}
            )
    
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
                    style={'width': '50%','backgroundColor':'transparent','border': '3px solid #b5b5b5','margin': '0 auto 40px auto','borderRadius': '10px','fontWeight': 'bold','backgroundImage': 'linear-gradient(135deg, #777 0%, #ccc 25%, #fff 50%, #ccc 75%, #555 100%)',
                           'display': 'inline-block','backgroundClip': 'text','WebkitBackgroundClip': 'text','color': 'transparent','WebkitTextFillColor': 'transparent'},
                    children=[
                        'Direccion del viento proveniente'
                        ]
                    ),
                html.Img(src=src_pro_wind, style={'width': '300px', 'height': '300px'})
                ],
                style={"width": "100%",'textAlign': 'center'}
            )
            BloqueWindText = html.Div(
                [
                html.Label(
                    id='input-label-prev-wind',
                    style={'width': '100%','backgroundColor':'transparent','border': '3px solid #b5b5b5','margin': '0 auto 40px auto','borderRadius': '10px','fontWeight': 'bold','backgroundImage': 'linear-gradient(135deg, #777 0%, #ccc 25%, #fff 50%, #ccc 75%, #555 100%)',
                           'display': 'inline-block','backgroundClip': 'text','WebkitBackgroundClip': 'text','color': 'transparent','WebkitTextFillColor': 'transparent'},
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
            ],
            style={"width": "100%",'textAlign': 'center','paddingTop': '20px'}
            )
    
            ###########################
            ###                     ###
            ###     Histogramas     ###
            ###                     ###
            ###########################
    
            #Histograma de viento promedio
            figHistAvgSpd, xHistAvgSpd = plt.subplots(figsize=(10, 6))
            y1 = VectorVelWind[0];      Stats.timsort(y1);  DatoModa1 = Stats.ModaVectorValor(y1); MediaAvgSpd = Stats.MediaVector(y1); MedianaAvgSpd = Stats.MedianaVector(y1);
            VarianzaInsesgadaAvgSpd = Stats.DesviacionMediaVector(y1, MediaAvgSpd);
            DesviacionAvgSpd = Stats.DesviacionNewton(VarianzaInsesgadaAvgSpd);
            Varianza1 = Stats.VarianzaVector(y1);
            DesviacionAvgSpdNM = Stats.DesviacionNewton(Varianza1);
            PercAvgSpd = Stats.Percentil(y1, Percentiles);
            figHistAvgSpd.patch.set_alpha(0.0);  xHistAvgSpd.patch.set_alpha(0.0);
            XlimInf2 = y1[0];    XlimSup2 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
            xHistAvgSpd.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = "#006C53",color ="#00B188",linewidth=4.0, alpha=0.6)
            xHistAvgSpd.set_xticks([XlimInf2,PercAvgSpd[0],PercAvgSpd[1],PercAvgSpd[2],XlimSup2])
            xHistAvgSpd.set_xticklabels([f'{XlimInf2:.2f}km/h',f'{PercAvgSpd[0]:.0f}km/h',f'{PercAvgSpd[1]:.0f}km/h',f'{PercAvgSpd[2]:.0f}km/h',f'{XlimSup2:.2f}km/h'], color='#DBDBDB', fontsize=14, fontname=fuente)
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
                html.Label(id='input-hist_avg-spd',style=label_style,children=['Velocidad promedio del viento km/h']),
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
                    html.Strong('Valores Minimos y Maximos'),html.Br(),
                    f'Minimo: {y1[0]:.0f}',f'\tMaximo: {y1[len(y1) - 1]:.0f}',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa1:.0f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercAvgSpd[0]:.0f}km/h',f'\tP{Percentiles[1]}: {PercAvgSpd[1]:.0f}km/h',f'\tP{Percentiles[2]}: {PercAvgSpd[2]:.0f}km/h'
                ])
                ],  
                style={'width': '100%','textAlign': 'center'}
            )
            #Histograma de la longitud de paso del viento
            figHistWindRun, xHistWindRun = plt.subplots(figsize=(10, 6))
            y2 = VectorVelWind[1];      Stats.timsort(y2);  DatoModa2 = Stats.ModaVectorValor(y2); MediaWindRun = Stats.MediaVector(y2); MedianaWindRun = Stats.MedianaVector(y2);
            VarianzaInsesgadaWindRun = Stats.DesviacionMediaVector(y2, MediaWindRun);
            DesviacionWindRun = Stats.DesviacionNewton(VarianzaInsesgadaWindRun);
            Varianza2 = Stats.VarianzaVector(y2);
            DesviacionWindRunNM = Stats.DesviacionNewton(Varianza2);
            PercWindRun = Stats.Percentil(y2, Percentiles);
            figHistWindRun.patch.set_alpha(0.0);  xHistWindRun.patch.set_alpha(0.0);
            XlimInf2 = y2[0];    XlimSup2 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(len(y2) - 1))
            xHistWindRun.hist(y2, bins=Rango2,rwidth = 1.2, edgecolor = '#060047',color ="#1B08FF",linewidth=4.0, alpha=0.6)
            xHistWindRun.set_xticks([XlimInf2,PercWindRun[0],PercWindRun[1],PercWindRun[2],XlimSup2])
            xHistWindRun.set_xticklabels([f'{XlimInf2:.2f}km',f'{PercWindRun[0]:.0f}km',f'{PercWindRun[1]:.0f}km',f'{PercWindRun[2]:.0f}km',f'{XlimSup2:.2f}km'], color='#DBDBDB', fontsize=14, fontname=fuente)
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
                html.Label(id='input-hist_wind-run',style=label_style,children=['Longitud del paso de viento km']),
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
                    html.Strong('Valores Minimos y Maximos'),html.Br(),
                    f'Minimo: {y2[0]:.0f}',f'\tMaximo: {y2[len(y2) - 1]:.0f}',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa2:.0f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercWindRun[0]:.0f}km',f'\tP{Percentiles[1]}: {PercWindRun[1]:.0f}km',f'\tP{Percentiles[2]}: {PercWindRun[2]:.0f}km'
                ])
                ],  
                style={'width': '100%','textAlign': 'center'}
            )
            #Histograma de vientos de alta velocidad
            figHistHighSpd, xHistHighSpd = plt.subplots(figsize=(10, 6))
            y3 = VectorVelWind[2];      Stats.timsort(y3);  DatoModa3 = Stats.ModaVectorValor(y3); MediaHighSpd = Stats.MediaVector(y3); MedianaHighSpd = Stats.MedianaVector(y3);
            VarianzaInsesgadaHighSpd = Stats.DesviacionMediaVector(y2, MediaHighSpd);
            DesviacionHighSpd = Stats.DesviacionNewton(VarianzaInsesgadaHighSpd);
            Varianza3 = Stats.VarianzaVector(y3);
            DesviacionHighSpdNM = Stats.DesviacionNewton(Varianza3);
            PercHighSpd = Stats.Percentil(y3, Percentiles);
            figHistHighSpd.patch.set_alpha(0.0);  xHistHighSpd.patch.set_alpha(0.0);
            XlimInf2 = y3[0];    XlimSup2 = y3[len(y3) - 1];  Rango3 = int(RegladeSturges(len(y3) - 1))
            xHistHighSpd.hist(y3, bins=Rango3,rwidth = 1.2, edgecolor = "#006C53",color ="#00B188",linewidth=4.0, alpha=0.6)
            xHistHighSpd.set_xticks([XlimInf2,PercHighSpd[0],PercHighSpd[1],PercHighSpd[2],XlimSup2])
            xHistHighSpd.set_xticklabels([f'{XlimInf2:.2f}km/h',f'{PercHighSpd[0]:.0f}km/h',f'{PercHighSpd[1]:.0f}km/h',f'{PercHighSpd[2]:.0f}km/h',f'{XlimSup2:.2f}km/h'], color='#DBDBDB', fontsize=14, fontname=fuente)
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
                html.Label(id='input-hist_avg-spd',style=label_style,children=['Velocidad maxima de la rafaga de viento km/h']),
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
                    html.Strong('Valores Minimos y Maximos'),html.Br(),
                    f'Minimo: {y3[0]:.0f}',f'\tMaximo: {y3[len(y3) - 1]:.0f}',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa3:.0f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercHighSpd[0]:.0f}km/h',f'\tP{Percentiles[1]}: {PercHighSpd[1]:.0f}km/h',f'\tP{Percentiles[2]}: {PercHighSpd[2]:.0f}km/h'
                ])
                ],  
                style={'width': '100%','textAlign': 'center'}
            )
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
            IndiceBarrasWHTHW = [f"Wind C.: {MediaWind:.4f}",f"Heat I.: {MediaHeat:.4f}",f"THW: {MediaTHW:.4f}",f"THSW: {MediaTHSW:.4f}"]
            figWHTHW, xWHTHW = plt.subplots(figsize=(10, 6))
            figWHTHW.patch.set_alpha(0.0); xWHTHW.patch.set_alpha(0.0);
            barrasx01 = xWHTHW.bar(IndiceBarrasWHTHW[0], MediaWind,edgecolor = "#00716E",linewidth=2.5,color="#00FFF7", alpha=0.9)
            barrasx02 = xWHTHW.bar(IndiceBarrasWHTHW[1], MediaHeat,edgecolor = "#B04E04",linewidth=2.5,color="#FF6F00", alpha=0.9)
            barrasx03 = xWHTHW.bar(IndiceBarrasWHTHW[2], MediaTHW,edgecolor = "#083E83",linewidth=2.5,color="#4F9BFF", alpha=0.9)
            barrasx04 = xWHTHW.bar(IndiceBarrasWHTHW[3], MediaTHSW,edgecolor = "#7A0DA6",linewidth=2.5,color="#9309D3", alpha=0.9)
            xWHTHW.set_yticks([0, 5, 10, 15, 20, 25, 30, 35, 40])
            xWHTHW.set_yticklabels(["0°C", "5°C", "10°C", "15°C", "20°C", "25°C", "30°C", "35°C", "40°C"], color='#DBDBDB', fontsize=14, fontname=fuente)
            xWHTHW.bar_label(barrasx01, color='#00FFF7', fontsize=12, fontweight='bold')
            xWHTHW.bar_label(barrasx02, color='#FF6F00', fontsize=12, fontweight='bold')
            xWHTHW.bar_label(barrasx03, color='#4F9BFF', fontsize=12, fontweight='bold')
            xWHTHW.bar_label(barrasx04, color='#9309D3', fontsize=12, fontweight='bold')
            #Codificar
            bufWHTHW = io.BytesIO()
            plt.savefig(bufWHTHW, format="png", bbox_inches="tight", transparent=True)
            plt.close(figWHTHW)
            #Crear Objeto Doble Axial
            src_w_h_thw = f"data:image/png;base64,{base64.b64encode(bufWHTHW.getvalue()).decode('utf-8')}"
            BloqueW_H_THW = html.Div([
                html.Label(id='input-w-h-twh',style=label_style_minus,children=["'Enfriamiento Eólico °C' 'Indice de Calor °C' 'THW °C' 'THSW °C'"]),
                html.Img(src=src_w_h_thw, style={'width': '60%', 'height': '300px'})
                ],
                style={'width': '100','textAlign': 'center'}
            )
    
            ############################################################
            ###                                                      ###
            ###     Grafica de Wind, Wind Low, Heat, Heat High       ###
            ###                                                      ###
            ############################################################
    
            #Grafica x,y de Wind, Heat
            y1 = VectorWindC[0];  y2 = VectorWindC[1];  y3 = VectorHeat[0];  y4 = VectorHeat[1]
            x = list(range(len(VectorWindC[0])))
            figWWLHHH, xWWLHHH = plt.subplots(figsize=(10, 6))
            figWWLHHH.patch.set_alpha(0.0);  xWWLHHH.patch.set_alpha(0.0)
            XlimInf = x[0]; XlimSup = x[len(x)-1];     YlimInf = Stats.DatoMinimoVector(y4); YlimSup = Stats.DatoMaximoVector(y3);
            plt.xlim(XlimInf, XlimSup);             plt.ylim(YlimInf-1, YlimSup+1)
            xWWLHHH.plot(x, y1, color = '#00FFF7', alpha=0.9, linewidth=3.0)
            xWWLHHH.plot(x, y2, color = '#00716E', alpha=0.9, linewidth=3.0)
            xWWLHHH.plot(x, y3, color = '#FF6F00', alpha=0.9, linewidth=3.0)
            xWWLHHH.plot(x, y4, color = '#B04E04', alpha=0.9, linewidth=3.0)
            VectorNum = []; VectorLetter = []
            for i in range(11):
                factor = (i)*0.1
                VectorNum.append(((XlimSup - XlimInf)*factor)+XlimInf)
                VectorLetter.append(f'{((XlimSup - XlimInf)*factor)+XlimInf:.0f}')
            xWWLHHH.set_xticks(VectorNum)
            xWWLHHH.set_xticklabels(VectorLetter, color='#DBDBDB', fontsize=14, fontname=fuente)
            xWWLHHH.set_yticks([YlimInf, YlimSup])
            xWWLHHH.set_yticklabels([f'{YlimInf:.0f}°C', f'{YlimSup:.0f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
            #codificar
            bufxWWLHHH = io.BytesIO()
            plt.savefig(bufxWWLHHH, format="png", bbox_inches='tight', transparent=True)
            plt.close(figWWLHHH)
            #Crear Objeto Temperaturas
            src_w_wl_h_hh = f"data:image/png;base64,{base64.b64encode(bufxWWLHHH.getvalue()).decode('utf-8')}"
            BloqueWWLHHH = html.Div(
                [
                    html.Label(id='input-w-wl-h-hl',style=label_style,children=['Maximos y minimos del enfriamiento y calor °C']),
                    html.Img(src=src_w_wl_h_hh, style={'width': '60%', 'height': '300px'})
                ],
                style={'width': '100%','textAlign': 'center'}
            )
    
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
                    html.Label(id='input-twh',style=label_style,children=['Sensacion Termica °C']),
                    html.Img(src=url_imagen, style={'width': '100%','height': 'auto'})
                ],
                style={'width': '100%','textAlign': 'center'}
            )
    
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
                    html.Label(id='input-twsh',style=label_style,children=['Sensacion Termica Radiada°C']),
                    html.Img(src=url_imagen, style={'width': '100%','height': 'auto'})
                ],
                style={'width': '100%','textAlign': 'center'}
            )
    
            ###########################
            ###                     ###
            ###     Histogramas     ###
            ###                     ###
            ###########################
    
            #Histrograma Enfriamento eolico
            Stats.timsort(y1);                      Stats.timsort(y2);
            Media1 = Stats.MediaVector(y1);         Media2 = Stats.MediaVector(y2);
            Mediana1 = Stats.MedianaVector(y1);     Mediana2 = Stats.MedianaVector(y2);
            VarianzaInsesgadaWindC = Stats.DesviacionMediaVector(y1, Media1);
            DesviacionWindC = Stats.DesviacionNewton(VarianzaInsesgadaWindC);
            VarianzaInsesgadaWindCMin = Stats.DesviacionMediaVector(y2, Media2);
            DesviacionWindCMin = Stats.DesviacionNewton(VarianzaInsesgadaWindCMin);
            DatoModa1 = Stats.ModaVectorValor(y1);  DatoModa2 = Stats.ModaVectorValor(y2);
            Varianza1 = Stats.VarianzaVector(y1);   Varianza2 = Stats.VarianzaVector(y2);
            DesviacionWindCNM = Stats.DesviacionNewton(Varianza1);
            DesviacionWindCMinNM = Stats.DesviacionNewton(Varianza2);
            PercExtWindC = Stats.Percentil(y1, Percentiles);
            PercExtWindCMin = Stats.Percentil(y2, Percentiles);
            figHistWindCWindCMin, xHistWindCWindCMin = plt.subplots(figsize=(10, 6));
            figHistWindCWindCMin.patch.set_alpha(0.0);  xHistWindCWindCMin.patch.set_alpha(0.0);
            XlimInf2 = y2[0];    XlimSup2 = y1[len(y1) - 1];  Rango = int(RegladeSturges(len(y1) - 1));
            xHistWindCWindCMin.hist(y1, bins=Rango,rwidth = 1.2, color = '#00FFF7',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistWindCWindCMin.hist(y2, bins=Rango,rwidth = 1.2, color = '#00716E',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistWindCWindCMin.set_xticks([XlimInf2,PercExtWindC[0],PercExtWindC[1],PercExtWindC[2],PercExtWindCMin[0],PercExtWindCMin[1],PercExtWindCMin[2],XlimSup2])
            xHistWindCWindCMin.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtWindC[0]:.0f}°C',f'{PercExtWindC[1]:.0f}°C',f'{PercExtWindC[2]:.0f}°C',f'{PercExtWindCMin[0]:.0f}°C',f'{PercExtWindCMin[1]:.0f}°C',f'{PercExtWindCMin[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
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
                html.Img(src=src_hist_wind_c_wind_c_min, style={'width': '100%', 'height': '300px'}),
                html.Label(id='input-hist_wind_c_wind_c_min',style=label_style,children=['Enfriamiento Eólico °C']),
                html.P([
                    html.Strong('Medias Aritméticas'),html.Br(),
                    f'Para maximas: {Media1:.4f}',f'\tPara Minimos: {Media2:.4f}',html.Br(),
                    html.Strong('Medianas'),html.Br(),
                    f'Para maximas: {Mediana1:.0f}',f'\tPara Minimos: {Mediana2:.0f}',html.Br(),
                    html.Strong('Varianza Insesgada'),html.Br(),
                    f'Para maximas: {VarianzaInsesgadaWindC:.4f}',f'\tPara Minimos: {VarianzaInsesgadaWindCMin:.4f}',html.Br(),
                    html.Strong('Desviacion Estandar'),html.Br(),
                    f'Para maximas: {DesviacionWindC:.4f}',f'\tPara Minimos: {DesviacionWindCMin:.4f}',html.Br(),
                    html.Strong('Varianza Sesgada'),html.Br(),
                    f'Para maximas: {Varianza1:.4f}',f'\tPara Minimos: {Varianza2:.4f}',html.Br(),
                    html.Strong('Desviacion Estandar sin Media'),html.Br(),
                    f'Para maximas: {DesviacionWindCNM:.4f}',f'\tPara Minimos: {DesviacionWindCMinNM:.4f}',html.Br(),
                    html.Strong('Valores Minimos y Maximos'),html.Br(),
                    f'Para maximas: {y1[0]:.0f}',f',{y1[len(y1) - 1]:.0f}',f'\tPara Minimos: {y2[0]:.0f}',f' {y2[len(y2) - 1]:.0f}',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para maximas: {DatoModa1:.0f}',f'\tPara Minimos: {DatoModa2:.0f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Maximas: P{Percentiles[0]}: {PercExtWindC[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtWindC[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtWindC[2]:.0f}°C',html.Br(),
                    f'Minimas: P{Percentiles[0]}: {PercExtWindCMin[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtWindCMin[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtWindCMin[2]:.0f}°C'
                ])
                ],  
                style={'width': '100%','textAlign': 'center'}
            )
            #Histrograma Indice de Calor
            Stats.timsort(y3);                      Stats.timsort(y4);
            Media3 = Stats.MediaVector(y3);         Media4 = Stats.MediaVector(y4);
            Mediana3 = Stats.MedianaVector(y3);     Mediana4 = Stats.MedianaVector(y4);
            VarianzaInsesgadaHeatI = Stats.DesviacionMediaVector(y3, Media3);
            DesviacionHeatI = Stats.DesviacionNewton(VarianzaInsesgadaHeatI);
            VarianzaInsesgadaHHeatI = Stats.DesviacionMediaVector(y4, Media4);
            DesviacionHHeatI = Stats.DesviacionNewton(VarianzaInsesgadaHHeatI);
            DatoModa3 = Stats.ModaVectorValor(y3);  DatoModa4 = Stats.ModaVectorValor(y4);
            Varianza3 = Stats.VarianzaVector(y3);   Varianza4 = Stats.VarianzaVector(y4);
            DesviacionHeatINM = Stats.DesviacionNewton(Varianza3);
            DesviacionHHeatINM = Stats.DesviacionNewton(Varianza4);
            PercExtHeatI = Stats.Percentil(y3, Percentiles);
            PercExtHHeatI = Stats.Percentil(y4, Percentiles);
            figHistH_HeatI, xHistH_HeatI = plt.subplots(figsize=(10, 6));
            figHistH_HeatI.patch.set_alpha(0.0);  xHistH_HeatI.patch.set_alpha(0.0);
            XlimInf2 = y4[0];    XlimSup2 = y3[len(y3) - 1];  Rango = int(RegladeSturges(len(y3) - 1));
            xHistH_HeatI.hist(y3, bins=Rango,rwidth = 1.2, color = '#FF6F00',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistH_HeatI.hist(y4, bins=Rango,rwidth = 1.2, color = '#B04E04',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHistH_HeatI.set_xticks([XlimInf2,PercExtHeatI[0],PercExtHeatI[1],PercExtHeatI[2],PercExtHHeatI[0],PercExtHHeatI[1],PercExtHHeatI[2],XlimSup2])
            xHistH_HeatI.set_xticklabels([f'{XlimInf2:.2f}°C',f'{PercExtHeatI[0]:.0f}°C',f'{PercExtHeatI[1]:.0f}°C',f'{PercExtHeatI[2]:.0f}°C',f'{PercExtHHeatI[0]:.0f}°C',f'{PercExtHHeatI[1]:.0f}°C',f'{PercExtHHeatI[2]:.0f}°C',f'{XlimSup2:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
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
                html.Img(src=src_hist_high_heat_index, style={'width': '100%', 'height': '300px'}),
                html.Label(id='input-hist_high_heat_index',style=label_style,children=['Calentamiento °C']),
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
                    html.Strong('Valores Minimos y Maximos'),html.Br(),
                    f'Para maximas: {y3[0]:.0f}',f',{y3[len(y3) - 1]:.0f}',f'\tPara Minimos: {y4[0]:.0f}',f' {y4[len(y4) - 1]:.0f}',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para maximas: {DatoModa3:.0f}',f'\tPara Minimos: {DatoModa4:.0f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Maximas: P{Percentiles[0]}: {PercExtHeatI[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtHeatI[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtHeatI[2]:.0f}°C',html.Br(),
                    f'Minimas: P{Percentiles[0]}: {PercExtHHeatI[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercExtHHeatI[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercExtHHeatI[2]:.0f}°C'
                ])
                ],  
                style={'width': '100%','textAlign': 'center'}
            )
            #Histograma TWH
            figHistInsideTWH, xHistInsideTWH = plt.subplots(figsize=(10, 6))
            y5 = VectorTWH[0];      Stats.timsort(y5);  DatoModa5 = Stats.ModaVectorValor(y5);  MedianaTHW = Stats.MedianaVector(y5);
            VarianzaInsesgadaTHW = Stats.DesviacionMediaVector(y5, MediaTHW);
            DesviacionTHW = Stats.DesviacionNewton(VarianzaInsesgadaTHW);
            Varianza5 = Stats.VarianzaVector(y5);
            DesviacionTHWNM = Stats.DesviacionNewton(Varianza5);
            PercTHW = Stats.Percentil(y5, Percentiles);
            figHistInsideTWH.patch.set_alpha(0.0);  xHistInsideTWH.patch.set_alpha(0.0);
            XlimInf1 = y5[0];    XlimSup1 = y5[len(y5) - 1];  Rango5 = int(RegladeSturges(len(y1) - 1))
            xHistInsideTWH.hist(y5, bins=Rango5,rwidth = 1.2, edgecolor = 'black', color="#4F9BFF",linewidth=4.0, alpha=0.6)
            xHistInsideTWH.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
            xHistInsideTWH.set_xticks([XlimInf1,PercTHW[0],PercTHW[1],PercTHW[2],XlimSup1])
            xHistInsideTWH.set_xticklabels([f'{XlimInf1:.2f}°C',f'{PercTHW[0]:.0f}°C',f'{PercTHW[1]:.0f}°C',f'{PercTHW[2]:.0f}°C',f'{XlimSup1:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
            for p, val, col in zip(Percentiles,PercTHW,ColorPerc):
                xHistInsideTWH.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistTWH = io.BytesIO()
            plt.savefig(bufHistTWH, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistInsideTWH)
            src_hist_t_w_h = f"data:image/png;base64,{base64.b64encode(bufHistTWH.getvalue()).decode('utf-8')}"
            BloqueHistTWH = html.Div([
                html.Img(src=src_hist_t_w_h, style={'width': '100%', 'height': '300px'}),
                html.Label(id='input-hist_ins-temp-hum',style=label_style,children=['Sensación de calor °C']),
                html.P([
                    html.Strong('Media Aritmética'),html.Br(),
                    f'{MediaTHW:.4f}',html.Br(),
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
                    html.Strong('Valores Minimos y Maximos'),html.Br(),
                    f'Minimo: {y5[0]:.0f}',f'\tMaximo: {y5[len(y5) - 1]:.0f}',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa5:.0f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercTHW[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercTHW[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercTHW[2]:.0f}°C'
                ])
                ],
                style={'width': '100%','textAlign': 'center'}
            )
            #Histograma THSW
            figHistInsideTHSW, xHistInsideTHSW = plt.subplots(figsize=(10, 6))
            y8 = VectorTHSW[0];      Stats.timsort(y8);  DatoModa8 = Stats.ModaVectorValor(y8);  MedianaTHSW = Stats.MedianaVector(y8);
            VarianzaInsesgadaTHSW = Stats.DesviacionMediaVector(y8, MediaTHSW);
            DesviacionTHSW = Stats.DesviacionNewton(VarianzaInsesgadaTHSW);
            Varianza8 = Stats.VarianzaVector(y8);
            DesviacionTHSWNM = Stats.DesviacionNewton(Varianza8);
            PercTHSW = Stats.Percentil(y8, Percentiles);
            figHistInsideTHSW.patch.set_alpha(0.0);  xHistInsideTHSW.patch.set_alpha(0.0);
            XlimInf1 = y8[0];    XlimSup1 = y8[len(y8) - 1];  Rango8 = int(RegladeSturges(len(y8) - 1))
            xHistInsideTHSW.hist(y8, bins=Rango8,rwidth = 1.2, edgecolor = 'black', color="#9309D3",linewidth=4.0, alpha=0.6)
            xHistInsideTHSW.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
            xHistInsideTHSW.set_xticks([XlimInf1,PercTHSW[0],PercTHSW[1],PercTHSW[2],XlimSup1])
            xHistInsideTHSW.set_xticklabels([f'{XlimInf1:.2f}°C',f'{PercTHSW[0]:.0f}°C',f'{PercTHSW[1]:.0f}°C',f'{PercTHSW[2]:.0f}°C',f'{XlimSup1:.2f}°C'], color='#DBDBDB', fontsize=14, fontname=fuente)
            for p, val, col in zip(Percentiles,PercTHSW,ColorPerc):
                xHistInsideTHSW.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistTHSW = io.BytesIO()
            plt.savefig(bufHistTHSW, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistInsideTHSW)
            src_hist_t_h_s_w = f"data:image/png;base64,{base64.b64encode(bufHistTHSW.getvalue()).decode('utf-8')}"
            BloqueHistTHSW = html.Div([
                html.Img(src=src_hist_t_h_s_w, style={'width': '100%', 'height': '300px'}),
                html.Label(id='input-hist_t-h-s-w',style=label_style,children=['Sensacion de calor radiada °C']),
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
                    html.Strong('Valores Minimos y Maximos'),html.Br(),
                    f'Minimo: {y8[0]:.0f}',f'\tMaximo: {y8[len(y8) - 1]:.0f}',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa8:.0f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercTHSW[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercTHSW[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercTHSW[2]:.0f}°C'
                ])
                ],
                style={'width': '100%','textAlign': 'center'}
            )
            #Histrograma THW Maximos y Minimos
            y6 = VectorTWH[1];  y7 = VectorTWH[2]
            Stats.timsort(y6);                      Stats.timsort(y7);
            Media6 = Stats.MediaVector(y6);         Media7= Stats.MediaVector(y7);
            Mediana6 = Stats.MedianaVector(y6);     Mediana7 = Stats.MedianaVector(y7);
            VarianzaInsesgadaTHWMax = Stats.DesviacionMediaVector(y6, Media6);
            DesviacionTHWMax = Stats.DesviacionNewton(VarianzaInsesgadaTHWMax);
            VarianzaInsesgadaTHWMin = Stats.DesviacionMediaVector(y7, Media7);
            DesviacionTHWMin = Stats.DesviacionNewton(VarianzaInsesgadaTHWMin);
            Moda6 = Stats.ModaVector(y6);           DatoModa6 = Stats.ModaVectorValor(y6);
            Moda7 = Stats.ModaVector(y7);           DatoModa7 = Stats.ModaVectorValor(y7);
            Varianza6 = Stats.VarianzaVector(y2);   Varianza7 = Stats.VarianzaVector(y3);
            DesviacionTHWMaxNM = Stats.DesviacionNewton(Varianza6);
            DesviacionTHWMinNM = Stats.DesviacionNewton(Varianza7);
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
                html.Img(src=src_hist_thw_max_min, style={'width': '100%', 'height': '300px'}),
                html.Label(id='input-hist_thw-max-min',style=label_style,children=['Sensaciones Termicas °C']),
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
                    html.Strong('Valores Minimos y Maximos'),html.Br(),
                    f'Para maximas: {y6[0]:.0f}',f',{y6[len(y6) - 1]:.0f}',f'\tPara Minimos: {y7[0]:.0f}',f' {y7[len(y7) - 1]:.0f}',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para maximas: {DatoModa6:.0f}',f'\tPara Minimos: {DatoModa7:.0f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Maximas: P{Percentiles[0]}: {PercTHWMax[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercTHWMax[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercTHWMax[2]:.0f}°C',html.Br(),
                    f'Minimas: P{Percentiles[0]}: {PercTHWMin[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercTHWMin[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercTHWMin[2]:.0f}°C'
                ])  
                ],  
                style={'width': '100%','textAlign': 'center'}
            )
            #Histrograma THW Maximos y Minimos
            y6 = VectorTHSW[1];  y7 = VectorTHSW[2]
            Stats.timsort(y6);                      Stats.timsort(y7);
            Media6 = Stats.MediaVector(y6);         Media7= Stats.MediaVector(y7);
            Mediana6 = Stats.MedianaVector(y6);     Mediana7 = Stats.MedianaVector(y7);
            VarianzaInsesgadaTHSWMax = Stats.DesviacionMediaVector(y6, Media6);
            DesviacionTHSWMax = Stats.DesviacionNewton(VarianzaInsesgadaTHSWMax);
            VarianzaInsesgadaTHSWMin = Stats.DesviacionMediaVector(y7, Media7);
            DesviacionTHSWMin = Stats.DesviacionNewton(VarianzaInsesgadaTHSWMin);
            Moda6 = Stats.ModaVector(y6);           DatoModa6 = Stats.ModaVectorValor(y6);
            Moda7 = Stats.ModaVector(y7);           DatoModa7 = Stats.ModaVectorValor(y7);
            Varianza6 = Stats.VarianzaVector(y2);   Varianza7 = Stats.VarianzaVector(y3);
            DesviacionTHSWMaxNM = Stats.DesviacionNewton(Varianza6);
            DesviacionTHSWMinNM = Stats.DesviacionNewton(Varianza7);
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
                html.Img(src=src_hist_thsw_max_min, style={'width': '100%', 'height': '300px'}),
                html.Label(id='input-hist_thsw-max-min',style=label_style,children=['Sensaciones Termicas °C']),
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
                    html.Strong('Valores Minimos y Maximos'),html.Br(),
                    f'Para maximas: {y6[0]:.0f}',f',{y6[len(y6) - 1]:.0f}',f'\tPara Minimos: {y7[0]:.0f}',f' {y7[len(y7) - 1]:.0f}',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para maximas: {DatoModa6:.0f}',f'\tPara Minimos: {DatoModa7:.0f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Maximas: P{Percentiles[0]}: {PercTHSWMax[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercTHSWMax[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercTHSWMax[2]:.0f}°C',html.Br(),
                    f'Minimas: P{Percentiles[0]}: {PercTHSWMin[0]:.0f}°C',f'\tP{Percentiles[1]}: {PercTHSWMin[1]:.0f}°C',f'\tP{Percentiles[2]}: {PercTHSWMin[2]:.0f}°C'
                ])  
                ],  
                style={'width': '100%','textAlign': 'center'}
            )
            return BloqueW_H_THW,BloqueWWLHHH,None, BloqueHistWindCWindCMin,BloqueHistHighHeatIndex,BloqueHistTWH,BloqueHistTHSW, None,None,None, BloqueTHW,BloqueHistTHWMaxMin,BloqueHistTHSWMaxMin,BloqueTHSW
            
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
    
            IndiceBarras = [f"ET: {VectorETRainM[0]:.4f}",f"Rain: {VectorETRainM[1]:.4f}",f"RainGigh: {VectorETRainM[2]:.4f}"]
            figETRain, xETRain1 = plt.subplots(figsize=(10, 6))
            figETRain.patch.set_alpha(0.0);  xETRain1.patch.set_alpha(0.0)
            barrasx1 = xETRain1.bar(IndiceBarras[0], VectorETRainM[0],edgecolor = "#005A06",linewidth=6.0, color="#5EF956", alpha=0.9)
            xETRain1.bar_label(barrasx1, color='#5EF956', fontsize=12, fontweight='bold')
            xETRain1.set_ylabel('Evapotranspiracion', color='#DBDBDB', fontname=fuente, fontsize=16, fontweight='bold')
            xETRain1.tick_params(axis='y', labelcolor='blue')
            xETRain1.set_yticks([0, 5, 10, 15, 20, 25, 30, 35, 40])
            xETRain1.set_yticklabels(["0 mm", "5 mm", "10 mm", "15 mm", "20 mm", "25 mm", "30 mm", "35 mm", "40 mm"], color='#DBDBDB', fontsize=14, fontname=fuente)
            xETRain2 = xETRain1.twinx()
            barrasx2 = xETRain2.bar(IndiceBarras[1], VectorETRainM[1],edgecolor = "#25B1F7",linewidth=6.0,color ="#8ED7FB", alpha=0.9)
            barrasx3 = xETRain2.bar(IndiceBarras[2], VectorETRainM[2],edgecolor = "#0700D0",linewidth=6.0,color ="#001CD0", alpha=0.9)
            xETRain2.bar_label(barrasx2, color='#8ED7FB', fontsize=12, fontweight='bold')
            xETRain2.bar_label(barrasx3, color='#001CD0', fontsize=12, fontweight='bold')
            xETRain2.set_ylabel('Precipitacion', color='#DBDBDB', fontname=fuente, fontsize=16, fontweight='bold')
            xETRain2.set_yticks([0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00, 1.10, 1.20, 1.30, 1.40, 1.50]) 
            xETRain2.set_yticklabels(['0.10 mm', '0.20 mm', '0.30 mm', '0.40 mm', '0.50 mm', '0.60 mm', '0.70 mm', '0.80 mm', '0.90 mm', '1.00 mm', '1.10 mm', '1.20 mm', '1.30 mm', '1.40 mm', '1.50 mm'], color='#DBDBDB', fontsize=14, fontname=fuente)
            xETRain2.set_xlabel("Evapotranspiracion - - - Precipitación Pluvial", color='#FFFFFF', fontname=fuente, fontsize=16, fontweight='bold')
            #Codificar
            bufETRain = io.BytesIO()
            plt.savefig(bufETRain, format="png", bbox_inches="tight", transparent=True)
            plt.close(figETRain)
            #Crear Objeto Doble Axial
            src_et_rain_high = f"data:image/png;base64,{base64.b64encode(bufETRain.getvalue()).decode('utf-8')}"
            BloqueETRain = html.Div([
                html.Label(id='input-et-rain-high',style=label_style,children=['Evapotranspitacion y Precipitacion']),
                html.Img(src=src_et_rain_high, style={'width': '100%', 'height': '300px'})
                ],  
                style={'width': '100%','textAlign': 'center'}
            )

            #################################################################
            ###                                                           ###
            ###     Grafica de maximos y medicion de la precipitacion     ###
            ###                                                           ###
            #################################################################

            y1 = VectorETRain[1];  y2 = VectorETRain[2];
            x = list(range(len(VectorETRain[0])))
            figRainHigh, xRainHigh = plt.subplots(figsize=(10, 6))
            figRainHigh.patch.set_alpha(0.0);  xRainHigh.patch.set_alpha(0.0)
            XlimInf = x[0]; XlimSup = x[len(x)-1];     YlimInf = Stats.DatoMinimoVector(y1); YlimSup = Stats.DatoMaximoVector(y2);
            plt.xlim(XlimInf, XlimSup);             plt.ylim(YlimInf-0.5, YlimSup+0.5)
            xRainHigh.plot(x, y1, color = "#74E1FF", alpha=0.4)
            xRainHigh.plot(x, y2, color = "#1A37AB", alpha=0.4)
            VectorNum = []; VectorLetter = []
            for i in range(11):
                factor = (i)*0.1
                VectorNum.append(((XlimSup - XlimInf)*factor)+XlimInf)
                VectorLetter.append(f'{((XlimSup - XlimInf)*factor)+XlimInf:.0f}')
            xRainHigh.set_xticks(VectorNum)
            xRainHigh.set_xticklabels(VectorLetter, color='#DBDBDB', fontsize=14, fontname=fuente)
            xRainHigh.set_yticks([YlimInf, YlimSup])
            xRainHigh.set_yticklabels([f'{YlimInf:.0f} mm', f'{YlimSup:.0f} mm'], color='#DBDBDB', fontsize=14, fontname=fuente)
            #Guardar imagen de MatplotLib
            bufRainHigh = io.BytesIO()
            plt.savefig(bufRainHigh, format="png", bbox_inches='tight', transparent=True)
            plt.close(figRainHigh)
            #Crear Objeto Temperaturas
            src_rain_high = f"data:image/png;base64,{base64.b64encode(bufRainHigh.getvalue()).decode('utf-8')}"
            BloqueRainRainHigh = html.Div(
                [
                    html.Label(id='input-rain-rain-high',style=label_style,children=['Precipitación y maximos']),
                    html.Img(src=src_rain_high, style={'width': '100%', 'height': '300px'})
                ],
                style={'width': '100%','textAlign': 'center'}
            )

            ###########################
            ###                     ###
            ###     Histogramas     ###
            ###                     ###
            ###########################

            #Histograma ET
            figET, xET = plt.subplots(figsize=(10, 6))
            y1 = VectorETRain[0];      Stats.timsort(y1);  DatoModa1 = Stats.ModaVectorValor(y1);  MedianaET = Stats.MedianaVector(y1);
            VarianzaInsesgadaET = Stats.DesviacionMediaVector(y1, VectorETRainM[0]);
            DesviacionET = Stats.DesviacionNewton(VarianzaInsesgadaET);
            Varianza1 = Stats.VarianzaVector(y1);
            DesviacionETNM = Stats.DesviacionNewton(Varianza1);
            PercET = Stats.Percentil(y1, Percentiles);
            figET.patch.set_alpha(0.0);  xET.patch.set_alpha(0.0);
            XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
            xET.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = 'black', color="#5EF956",linewidth=4.0, alpha=0.6)
            xET.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
            xET.set_xticks([XlimInf1,PercET[0],PercET[1],PercET[2],XlimSup1])
            xET.set_xticklabels([f'{XlimInf1:.2f}mm',f'{PercET[0]:.0f}mm',f'{PercET[1]:.0f}mm',f'{PercET[2]:.0f}mm',f'{XlimSup1:.2f}mm'], color='#DBDBDB', fontsize=14, fontname=fuente)
            for p, val, col in zip(Percentiles,PercET,ColorPerc):
                xET.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufET = io.BytesIO()
            plt.savefig(bufET, format="png", bbox_inches="tight", transparent=True)
            plt.close(figET)
            src_hist_ET = f"data:image/png;base64,{base64.b64encode(bufET.getvalue()).decode('utf-8')}"
            BloqueET = html.Div([
                html.Img(src=src_hist_ET, style={'width': '100%', 'height': '300px'}),
                html.Label(id='input-et',style=label_style,children=['Evapotranspiracion mm']),
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
                    html.Strong('Valores Minimos y Maximos'),html.Br(),
                    f'Minimo: {y1[0]:.0f}',f'\tMaximo: {y1[len(y1) - 1]:.0f}',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa1:.0f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercET[0]:.0f}mm',f'\tP{Percentiles[1]}: {PercET[1]:.0f}mm',f'\tP{Percentiles[2]}: {PercET[2]:.0f}mm'
                ])
                ],
                style={'width': '100%','textAlign': 'center'}
            )
            #Histograma Rain
            figRain, xRain = plt.subplots(figsize=(10, 6))
            y2 = VectorETRain[1];      Stats.timsort(y2);  DatoModa2 = Stats.ModaVectorValor(y2);  MedianaRain = Stats.MedianaVector(y2);
            VarianzaInsesgadaRain = Stats.DesviacionMediaVector(y2, VectorETRainM[1]);
            DesviacionRain = Stats.DesviacionNewton(VarianzaInsesgadaRain);
            Varianza2 = Stats.VarianzaVector(y2);
            DesviacionRainNM = Stats.DesviacionNewton(Varianza2);
            PercRain = Stats.Percentil(y2, Percentiles);
            figRain.patch.set_alpha(0.0);  xRain.patch.set_alpha(0.0);
            XlimInf1 = y2[0];    XlimSup1 = y2[len(y2) - 1];  Rango2 = int(RegladeSturges(len(y2) - 1))
            xRain.hist(y2, bins=Rango2,rwidth = 1.2, edgecolor = 'black', color="#8ED7FB",linewidth=4.0, alpha=0.6)
            xRain.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
            xRain.set_xticks([XlimInf1,PercRain[0],PercRain[1],PercRain[2],XlimSup1])
            xRain.set_xticklabels([f'{XlimInf1:.2f}mm',f'{PercRain[0]:.0f}mm',f'{PercRain[1]:.0f}mm',f'{PercRain[2]:.0f}mm',f'{XlimSup1:.2f}mm'], color='#DBDBDB', fontsize=14, fontname=fuente)
            for p, val, col in zip(Percentiles,PercRain,ColorPerc):
                xRain.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufRain = io.BytesIO()
            plt.savefig(bufRain, format="png", bbox_inches="tight", transparent=True)
            plt.close(figRain)
            src_hist_Rain = f"data:image/png;base64,{base64.b64encode(bufRain.getvalue()).decode('utf-8')}"
            BloqueRain = html.Div([
                html.Img(src=src_hist_Rain, style={'width': '100%', 'height': '300px'}),
                html.Label(id='input-hist_rain',style=label_style,children=['Precipitacion Pluvial mm']),
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
                    html.Strong('Valores Minimos y Maximos'),html.Br(),
                    f'Minimo: {y1[0]:.0f}',f'\tMaximo: {y2[len(y2) - 1]:.0f}',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa2:.0f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercRain[0]:.0f}mm',f'\tP{Percentiles[1]}: {PercRain[1]:.0f}mm',f'\tP{Percentiles[2]}: {PercRain[2]:.0f}mm'
                ])
                ],
                style={'width': '100%','textAlign': 'center'}
            )
            #Histograma High Rain
            figRainHigh, xRainHigh = plt.subplots(figsize=(10, 6))
            y1 = VectorETRain[2];      Stats.timsort(y1);  DatoModa1 = Stats.ModaVectorValor(y1);  MedianaRainHigh = Stats.MedianaVector(y1);
            VarianzaInsesgadaRainHigh = Stats.DesviacionMediaVector(y1, VectorETRainM[2]);
            DesviacionRainHigh = Stats.DesviacionNewton(VarianzaInsesgadaRainHigh);
            Varianza1 = Stats.VarianzaVector(y1);
            DesviacionRainHighNM = Stats.DesviacionNewton(Varianza1);
            PercRainHigh = Stats.Percentil(y1, Percentiles);
            figRainHigh.patch.set_alpha(0.0);  xRainHigh.patch.set_alpha(0.0);
            XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
            xRainHigh.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = 'black', color="#001CD0",linewidth=4.0, alpha=0.6)
            xRainHigh.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
            xRainHigh.set_xticks([XlimInf1,PercRainHigh[0],PercRainHigh[1],PercRainHigh[2],XlimSup1])
            xRainHigh.set_xticklabels([f'{XlimInf1:.2f}mm',f'{PercRainHigh[0]:.0f}mm',f'{PercRainHigh[1]:.0f}mm',f'{PercRainHigh[2]:.0f}mm',f'{XlimSup1:.2f}mm'], color='#DBDBDB', fontsize=14, fontname=fuente)
            for p, val, col in zip(Percentiles,PercRainHigh,ColorPerc):
                xRainHigh.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufRainHigh = io.BytesIO()
            plt.savefig(bufRainHigh, format="png", bbox_inches="tight", transparent=True)
            plt.close(figRainHigh)
            src_hist_rain_high = f"data:image/png;base64,{base64.b64encode(bufRainHigh.getvalue()).decode('utf-8')}"
            BloqueRainHigh = html.Div([
                html.Img(src=src_hist_rain_high, style={'width': '100%', 'height': '300px'}),
                html.Label(id='input-hist_rain_high',style=label_style,children=['Precipitacion Pluvial mm']),
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
                    html.Strong('Valores Minimos y Maximos'),html.Br(),
                    f'Minimo: {y1[0]:.0f}',f'\tMaximo: {y1[len(y1) - 1]:.0f}',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa1:.0f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercRainHigh[0]:.0f}mm',f'\tP{Percentiles[1]}: {PercRainHigh[1]:.0f}mm',f'\tP{Percentiles[2]}: {PercRainHigh[2]:.0f}mm'
                ])
                ],
                style={'width': '100%','textAlign': 'center'}
            )
            return BloqueETRain,None,BloqueRainRainHigh, BloqueET,None,BloqueRain,BloqueRainHigh, None,None,None, None,None,None,None
        
        if (opcion == "DatosSol"):
            SolarRad = 46;  HighSolarRad = 47;
            SolarE = 48;    UVIndex = 49;   HighUVIndex = 50;   UVDose = 51;
            HeatD = 52;     CoolD = 53;

            VectorSolarRad = [];  VectorSolarEnergy = [];   VectorDegree = [];  VectorUVIndex = []
            #Inicio y Final del indice
            i = SolarRad; Ante = CoolD;
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

            MediaSolarRad = Stats.MediaVector(VectorSolarRad[0]);    MediaSolarRadHigh = Stats.MediaVector(VectorSolarRad[1])
            IndiceBarras = [f"Solar Rad: {MediaSolarRad:.4f}",f"Solar Rad High: {MediaSolarRadHigh:.4f}"]
            figSolarRad, xSolarRad = plt.subplots(figsize=(10, 6))
            figSolarRad.patch.set_alpha(0.0);  xSolarRad.patch.set_alpha(0.0)
            barrasx1 = xSolarRad.bar(IndiceBarras[0], MediaSolarRad,edgecolor = "#B5B521",linewidth=6.0, color="#F6FF00", alpha=0.9)
            barrasx2 = xSolarRad.bar(IndiceBarras[1], MediaSolarRadHigh,edgecolor = "#905D0C",linewidth=6.0, color="#FE7B00", alpha=0.9)
            xSolarRad.bar_label(barrasx1, color='#F6FF00', fontsize=12, fontweight='bold')
            xSolarRad.bar_label(barrasx2, color='#FE7B00', fontsize=12, fontweight='bold')
            xSolarRad.set_ylabel('Radiacion Solar y picos', color='#DBDBDB', fontname=fuente, fontsize=16, fontweight='bold')
            xSolarRad.tick_params(axis='y', labelcolor='blue')
            xSolarRad.set_yticks([0, 50, 100, 150, 200, 250])
            xSolarRad.set_yticklabels(['0 W/m2', '50 W/m2', '100 W/m2', '150 W/m2', '200 W/m2', '250 W/m2'], color='#DBDBDB', fontsize=14, fontname=fuente)
            #Codificar
            bufSolarRadSolarRadHigh = io.BytesIO()
            plt.savefig(bufSolarRadSolarRadHigh, format="png", bbox_inches="tight", transparent=True)
            plt.close(figSolarRad)
            #Crear Objeto Doble Axial
            src_et_solar_solar_rad_high = f"data:image/png;base64,{base64.b64encode(bufSolarRadSolarRadHigh.getvalue()).decode('utf-8')}"
            BloqueSolarSolarRad = html.Div([
                html.Label(id='input-solar-solar-rad-high',style=label_style,children=['Radiacion Solar y picos W/m2']),
                html.Img(src=src_et_solar_solar_rad_high, style={'width': '100%', 'height': '300px'})
                ],  
                style={'width': '100%','textAlign': 'center'}
            )

            ##########################################
            ###                                    ###
            ###     Grafica de la Energia Solar    ###
            ###                                    ###
            ##########################################

            MediaSolarE = Stats.MediaVector(VectorSolarEnergy[0]);
            IndiceBarras = [f"Solar Energy: {MediaSolarE:.4f}"]
            figSolarE, xSolarE = plt.subplots(figsize=(10, 6))
            figSolarE.patch.set_alpha(0.0);  xSolarE.patch.set_alpha(0.0)
            barrasx1 = xSolarE.bar(IndiceBarras[0], MediaSolarE,edgecolor = "#B52121",linewidth=6.0, color="#FF4400", alpha=0.9)
            xSolarE.bar_label(barrasx1, color="#FF4400", fontsize=12, fontweight='bold')
            xSolarE.set_ylabel('Energia Solar', color='#DBDBDB', fontname=fuente, fontsize=16, fontweight='bold')
            xSolarE.tick_params(axis='y', labelcolor='blue')
            xSolarE.set_yticks([1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9])
            xSolarE.set_yticklabels(['1.1Ly', '1.2Ly', '1.3Ly', '1.4Ly', '1.5Ly', '1.6Ly', '1.7Ly', '1.8Ly', '1.9Ly'], color='#DBDBDB', fontsize=14, fontname=fuente)
            #Codificar
            bufSolarE = io.BytesIO()
            plt.savefig(bufSolarE, format="png", bbox_inches="tight", transparent=True)
            plt.close(figSolarE)
            #Crear Objeto Doble Axial
            src_solar_energy = f"data:image/png;base64,{base64.b64encode(bufSolarE.getvalue()).decode('utf-8')}"
            BloqueSolarEnergy = html.Div([
                html.Label(id='input-solar-energy',style=label_style,children=['Energia Solar Ly']),
                html.Img(src=src_solar_energy, style={'width': '100%', 'height': '300px'})
                ],  
                style={'width': '100%','textAlign': 'center'}
            )

            ###########################
            ###                     ###
            ###     Histogramas     ###
            ###                     ###
            ###########################

            #Histrograma Radiacion Solar
            y3 = VectorSolarRad[0];         y4 = VectorSolarRad[1]; 
            Stats.timsort(y3);                      Stats.timsort(y4);
            Media3 = Stats.MediaVector(y3);         Media4 = Stats.MediaVector(y4);
            Mediana3 = Stats.MedianaVector(y3);     Mediana4 = Stats.MedianaVector(y4);
            VarianzaInsesgadaSolarRad = Stats.DesviacionMediaVector(y3, Media3);
            DesviacionSolarRad = Stats.DesviacionNewton(VarianzaInsesgadaSolarRad);
            VarianzaInsesgadaSolarRadHigh = Stats.DesviacionMediaVector(y4, Media4);
            DesviacionSolarRadHigh = Stats.DesviacionNewton(VarianzaInsesgadaSolarRadHigh);
            DatoModa3 = Stats.ModaVectorValor(y3);  DatoModa4 = Stats.ModaVectorValor(y4);
            Varianza3 = Stats.VarianzaVector(y3);   Varianza4 = Stats.VarianzaVector(y4);
            DesviacionSolarRadNM = Stats.DesviacionNewton(Varianza3);
            DesviacionSolarRadHighNM = Stats.DesviacionNewton(Varianza4);
            PercExtSolarRad = Stats.Percentil(y3, Percentiles);
            PercExtSolarRadHigh = Stats.Percentil(y4, Percentiles);
            figHist_SolarRad, xHist_SolarRad = plt.subplots(figsize=(10, 6));
            figHist_SolarRad.patch.set_alpha(0.0);  xHist_SolarRad.patch.set_alpha(0.0);
            XlimInf2 = y3[0];    XlimSup2 = y4[len(y4) - 1];  Rango = int(RegladeSturges(len(y3) - 1));
            xHist_SolarRad.hist(y3, bins=Rango,rwidth = 1.2, color = '#F6FF00',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHist_SolarRad.hist(y4, bins=Rango,rwidth = 1.2, color = '#FE7B00',linewidth=4.0, edgecolor = 'black', alpha=0.3)
            xHist_SolarRad.set_xticks([XlimInf2,PercExtSolarRad[0],PercExtSolarRad[1],PercExtSolarRad[2],PercExtSolarRadHigh[0],PercExtSolarRadHigh[1],PercExtSolarRadHigh[2],XlimSup2])
            xHist_SolarRad.set_xticklabels([f'{XlimInf2:.2f}W/m2',f'{PercExtSolarRad[0]:.0f}W/m2',f'{PercExtSolarRad[1]:.0f}W/m2',f'{PercExtSolarRad[2]:.0f}W/m2',f'{PercExtSolarRadHigh[0]:.0f}W/m2',f'{PercExtSolarRadHigh[1]:.0f}W/m2',f'{PercExtSolarRadHigh[2]:.0f}W/m2',f'{XlimSup2:.2f}W/m2'], color='#DBDBDB', fontsize=14, fontname=fuente)
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
                html.Img(src=src_hist_solar_high_rad, style={'width': '100%', 'height': '300px'}),
                html.Label(id='input-hist_solar_rad_high',style=label_style,children=['Radiación Solar W/m2']),
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
                    html.Strong('Valores Minimos y Maximos'),html.Br(),
                    f'Para medias: {y3[0]:.0f}',f',{y3[len(y3) - 1]:.0f}',f'\tPara maximas: {y4[0]:.0f}',f' {y4[len(y4) - 1]:.0f}',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'Para medias: {DatoModa3:.0f}',f'\tPara maximas: {DatoModa4:.0f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'Medias: P{Percentiles[0]}: {PercExtSolarRad[0]:.0f}W/m2',f'\tP{Percentiles[1]}: {PercExtSolarRad[1]:.0f}W/m2',f'\tP{Percentiles[2]}: {PercExtSolarRad[2]:.0f}W/m2',html.Br(),
                    f'Maximas: P{Percentiles[0]}: {PercExtSolarRadHigh[0]:.0f}W/m2',f'\tP{Percentiles[1]}: {PercExtSolarRadHigh[1]:.0f}W/m2',f'\tP{Percentiles[2]}: {PercExtSolarRadHigh[2]:.0f}W/m2'
                ])
                ],  
                style={'width': '100%','textAlign': 'center'}
            )

            #Histograma Solar Energy
            figHistSolarEnergy, xHistSolarEnergy = plt.subplots(figsize=(10, 6))
            y1 = VectorSolarEnergy[0];      Stats.timsort(y1);  DatoModa1 = Stats.ModaVectorValor(y1);  MedianaHistSolarEnergy = Stats.MedianaVector(y1);
            VarianzaInsesgadaHistSolarEnergy = Stats.DesviacionMediaVector(y1, MediaSolarE);
            DesviacionHistSolarEnergy = Stats.DesviacionNewton(VarianzaInsesgadaHistSolarEnergy);
            Varianza1 = Stats.VarianzaVector(y1);
            DesviacionHistSolarEnergyNM = Stats.DesviacionNewton(Varianza1);
            PercHistSolarEnergy = Stats.Percentil(y1, Percentiles);
            figHistSolarEnergy.patch.set_alpha(0.0);  xHistSolarEnergy.patch.set_alpha(0.0);
            XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
            xHistSolarEnergy.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = 'black', color="#FF4400",linewidth=4.0, alpha=0.6)
            xHistSolarEnergy.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
            xHistSolarEnergy.set_xticks([XlimInf1,PercHistSolarEnergy[0],PercHistSolarEnergy[1],PercHistSolarEnergy[2],XlimSup1])
            xHistSolarEnergy.set_xticklabels([f'{XlimInf1:.2f}Ly',f'{PercHistSolarEnergy[0]:.0f}Ly',f'{PercHistSolarEnergy[1]:.0f}Ly',f'{PercHistSolarEnergy[2]:.0f}Ly',f'{XlimSup1:.2f}Ly'], color='#DBDBDB', fontsize=14, fontname=fuente)
            for p, val, col in zip(Percentiles,PercHistSolarEnergy,ColorPerc):
                xHistSolarEnergy.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
            #Codificar
            bufHistSolarEnergy = io.BytesIO()
            plt.savefig(bufHistSolarEnergy, format="png", bbox_inches="tight", transparent=True)
            plt.close(figHistSolarEnergy)
            src_hist_solar_energy = f"data:image/png;base64,{base64.b64encode(bufHistSolarEnergy.getvalue()).decode('utf-8')}"
            BloqueHistSolarEnergy = html.Div([
                html.Img(src=src_hist_solar_energy, style={'width': '100%', 'height': '300px'}),
                html.Label(id='input-solar-energy',style=label_style,children=['Energia Solar Ly']),
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
                    html.Strong('Valores Minimos y Maximos'),html.Br(),
                    f'Minimo: {y1[0]:.0f}',f'\tMaximo: {y1[len(y1) - 1]:.0f}',html.Br(),
                    html.Strong('Moda de los datos'),html.Br(),
                    f'{DatoModa1:.0f}',html.Br(),
                    html.Strong('Percentiles'),html.Br(),
                    f'P{Percentiles[0]}: {PercHistSolarEnergy[0]:.0f}Ly',f'\tP{Percentiles[1]}: {PercHistSolarEnergy[1]:.0f}Ly',f'\tP{Percentiles[2]}: {PercHistSolarEnergy[2]:.0f}Ly'
                ])
                ],
                style={'width': '100%','textAlign': 'center'}
            )
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
                IndiceDegree = [f"Calefacción: {MediaDegreeHeat}",f"Refrigeración: {MediaDegreeCool}"]
                figDegree, xHeat = plt.subplots(figsize=(10, 6))
                figDegree.patch.set_alpha(0.0);  xHeat.patch.set_alpha(0.0)
                barrasx1 = xHeat.bar(IndiceDegree[0], MediaDegreeHeat,edgecolor = "#D63702",linewidth=6.0, color="#EA8D00", alpha=0.9)
                xHeat.bar_label(barrasx1, color='#EA8D00', fontsize=12, fontweight='bold')
                xHeat.set_ylabel('Calefacción', color='#DBDBDB', fontname=fuente, fontsize=16, fontweight='bold')
                xHeat.tick_params(axis='y', labelcolor='blue')
                xHeat.set_yticks([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15])
                xHeat.set_yticklabels(['0.010', '0.020', '0.030', '0.040', '0.050', '0.060', '0.070', '0.080', '0.090', '0.100', '0.110', '0.120', '0.130', '0.140', '0.150'], color='#DBDBDB', fontsize=14, fontname=fuente)
                xCool = xHeat.twinx()
                barrasx2 = xCool.bar(IndiceDegree[1], MediaDegreeCool,edgecolor = "#25B1F7",linewidth=6.0,color ="#8ED7FB", alpha=0.9)
                xCool.bar_label(barrasx2, color='#8ED7FB', fontsize=12, fontweight='bold')
                xCool.set_ylabel('Refrigeración', color='#DBDBDB', fontname=fuente, fontsize=16, fontweight='bold')
                xCool.set_yticks([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15]) 
                xCool.set_yticklabels(['0.010', '0.020', '0.030', '0.040', '0.050', '0.060', '0.070', '0.080', '0.090', '0.100', '0.110', '0.120', '0.130', '0.140', '0.150'], color='#DBDBDB', fontsize=14, fontname=fuente)
                #Codificar
                bufDegree = io.BytesIO()
                plt.savefig(bufDegree, format="png", bbox_inches="tight", transparent=True)
                plt.close(figDegree)
                #Crear Objeto Doble Axial
                src_degree_heat_cool = f"data:image/png;base64,{base64.b64encode(bufDegree.getvalue()).decode('utf-8')}"
                BloqueDegree = html.Div([
                    html.Label(id='input-degree-heat-cool',style=label_style,children=['Indicador Energetico']),
                    html.Img(src=src_degree_heat_cool, style={'width': '100%', 'height': '300px'})
                    ],  
                    style={'width': '100%','textAlign': 'center'}
                )
                #Histograma Degree Calefaccion
                figHistDegreeHeat, xHistDegreeHeat = plt.subplots(figsize=(10, 6))
                y1 = VectorDegree[0];      Stats.timsort(y1);  DatoModa1 = Stats.ModaVectorValor(y1);  MedianaHistDegreeHeat = Stats.MedianaVector(y1);
                VarianzaInsesgadaHistDegreeHeat = Stats.DesviacionMediaVector(y1, MediaDegreeHeat);
                DesviacionHistDegreeHeat = Stats.DesviacionNewton(VarianzaInsesgadaHistDegreeHeat);
                Varianza1 = Stats.VarianzaVector(y1);
                DesviacionHistDegreeHeatNM = Stats.DesviacionNewton(Varianza1);
                PercHistDegreeHeat = Stats.Percentil(y1, Percentiles);
                figHistDegreeHeat.patch.set_alpha(0.0);  xHistDegreeHeat.patch.set_alpha(0.0);
                XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
                xHistDegreeHeat.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = 'black', color="#EA8D00",linewidth=4.0, alpha=0.6)
                xHistDegreeHeat.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
                xHistDegreeHeat.set_xticks([XlimInf1,PercHistDegreeHeat[0],PercHistDegreeHeat[1],PercHistDegreeHeat[2],XlimSup1])
                xHistDegreeHeat.set_xticklabels([f'{XlimInf1:.2f}',f'{PercHistDegreeHeat[0]:.0f}',f'{PercHistDegreeHeat[1]:.0f}',f'{PercHistDegreeHeat[2]:.0f}',f'{XlimSup1:.2f}'], color='#DBDBDB', fontsize=14, fontname=fuente)
                for p, val, col in zip(Percentiles,PercHistDegreeHeat,ColorPerc):
                    xHistDegreeHeat.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
                #Codificar
                bufHistDegreeHeat = io.BytesIO()
                plt.savefig(bufHistDegreeHeat, format="png", bbox_inches="tight", transparent=True)
                plt.close(figHistDegreeHeat)
                src_hist_degree_heat = f"data:image/png;base64,{base64.b64encode(bufHistDegreeHeat.getvalue()).decode('utf-8')}"
                BloqueHistDegreeHeat = html.Div([
                    html.Img(src=src_hist_degree_heat, style={'width': '100%', 'height': '300px'}),
                    html.Label(id='input-hist_degree-heat',style=label_style,children=['Calefacción']),
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
                        html.Strong('Valores Minimos y Maximos'),html.Br(),
                        f'Minimo: {y1[0]:.0f}',f'\tMaximo: {y1[len(y1) - 1]:.0f}',html.Br(),
                        html.Strong('Moda de los datos'),html.Br(),
                        f'{DatoModa1:.0f}',html.Br(),
                        html.Strong('Percentiles'),html.Br(),
                        f'P{Percentiles[0]}: {PercHistDegreeHeat[0]:.0f}',f'\tP{Percentiles[1]}: {PercHistDegreeHeat[1]:.0f}',f'\tP{Percentiles[2]}: {PercHistDegreeHeat[2]:.0f}'
                    ])
                    ],
                    style={'width': '100%','textAlign': 'center'}
                )
                #Histograma Degree Refrigeration
                figHistDegreeCool, xHistDegreeCool = plt.subplots(figsize=(10, 6))
                y1 = VectorDegree[1];      Stats.timsort(y1);  DatoModa1 = Stats.ModaVectorValor(y1);  MedianaHistDegreeCool = Stats.MedianaVector(y1);
                VarianzaInsesgadaHistDegreeCool = Stats.DesviacionMediaVector(y1, MediaDegreeCool);
                DesviacionHistDegreeCool = Stats.DesviacionNewton(VarianzaInsesgadaHistDegreeCool);
                Varianza1 = Stats.VarianzaVector(y1);
                DesviacionHistDegreeCoolNM = Stats.DesviacionNewton(Varianza1);
                PercHistDegreeCool = Stats.Percentil(y1, Percentiles);
                figHistDegreeCool.patch.set_alpha(0.0);  xHistDegreeCool.patch.set_alpha(0.0);
                XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
                xHistDegreeCool.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = 'black', color="#8ED7FB",linewidth=4.0, alpha=0.6)
                xHistDegreeCool.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
                xHistDegreeCool.set_xticks([XlimInf1,PercHistDegreeCool[0],PercHistDegreeCool[1],PercHistDegreeCool[2],XlimSup1])
                xHistDegreeCool.set_xticklabels([f'{XlimInf1:.2f}',f'{PercHistDegreeCool[0]:.0f}',f'{PercHistDegreeCool[1]:.0f}',f'{PercHistDegreeCool[2]:.0f}',f'{XlimSup1:.2f}'], color='#DBDBDB', fontsize=14, fontname=fuente)
                for p, val, col in zip(Percentiles,PercHistDegreeCool,ColorPerc):
                    xHistDegreeCool.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
                #Codificar
                bufHistDegreeCool = io.BytesIO()
                plt.savefig(bufHistDegreeCool, format="png", bbox_inches="tight", transparent=True)
                plt.close(figHistDegreeCool)
                src_hist_degree_cool = f"data:image/png;base64,{base64.b64encode(bufHistDegreeCool.getvalue()).decode('utf-8')}"
                BloqueHistDegreeCool = html.Div([
                    html.Img(src=src_hist_degree_cool, style={'width': '100%', 'height': '300px'}),
                    html.Label(id='input-hist_degree-cool',style=label_style,children=['Refrigeracion']),
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
                        html.Strong('Valores Minimos y Maximos'),html.Br(),
                        f'Minimo: {y1[0]:.0f}',f'\tMaximo: {y1[len(y1) - 1]:.0f}',html.Br(),
                        html.Strong('Moda de los datos'),html.Br(),
                        f'{DatoModa1:.0f}',html.Br(),
                        html.Strong('Percentiles'),html.Br(),
                        f'P{Percentiles[0]}: {PercHistDegreeCool[0]:.0f}',f'\tP{Percentiles[1]}: {PercHistDegreeCool[1]:.0f}',f'\tP{Percentiles[2]}: {PercHistDegreeCool[2]:.0f}'
                    ])
                    ],
                    style={'width': '100%','textAlign': 'center'}
                )
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
                MediaUVIndex = Stats.MediaVector(VectorUVIndex[0]);    MediaHighUVIndex = Stats.MediaVector(VectorUVIndex[1])
                IndiceMediaUVIndex = [f"Radiación Ultravioleta: {MediaUVIndex}",f"Radiacion UV maxima: {MediaHighUVIndex}"]
                figUVIndex, xUVIndex = plt.subplots(figsize=(10, 6))
                figUVIndex.patch.set_alpha(0.0);  xUVIndex.patch.set_alpha(0.0)
                barrasx1 = xUVIndex.bar(IndiceMediaUVIndex[0], MediaUVIndex,edgecolor = "#D63702",linewidth=6.0, color="#EA8D00", alpha=0.9)
                xUVIndex.bar_label(barrasx1, color='#EA8D00', fontsize=12, fontweight='bold')
                xUVIndex.set_ylabel('Radiacion Ultravioleta', color='#DBDBDB', fontname=fuente, fontsize=16, fontweight='bold')
                xUVIndex.tick_params(axis='y', labelcolor='blue')
                #xUVIndex.set_yticks([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15])
                #xUVIndex.set_yticklabels(['0.010', '0.020', '0.030', '0.040', '0.050', '0.060', '0.070', '0.080', '0.090', '0.100', '0.110', '0.120', '0.130', '0.140', '0.150'], color='#DBDBDB', fontsize=14, fontname=fuente)
                xUVIndexHigh = xUVIndex.twinx()
                barrasx2 = xUVIndexHigh.bar(IndiceMediaUVIndex[1], MediaHighUVIndex,edgecolor = "#25B1F7",linewidth=6.0,color ="#8ED7FB", alpha=0.9)
                xUVIndexHigh.bar_label(barrasx2, color='#8ED7FB', fontsize=12, fontweight='bold')
                xUVIndexHigh.set_ylabel('Radiacion Ultravioleta Pico', color='#DBDBDB', fontname=fuente, fontsize=16, fontweight='bold')
                #xUVIndexHigh.set_yticks([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15]) 
                #xUVIndexHigh.set_yticklabels(['0.010', '0.020', '0.030', '0.040', '0.050', '0.060', '0.070', '0.080', '0.090', '0.100', '0.110', '0.120', '0.130', '0.140', '0.150'], color='#DBDBDB', fontsize=14, fontname=fuente)
                #Codificar
                bufUVIndex = io.BytesIO()
                plt.savefig(bufUVIndex, format="png", bbox_inches="tight", transparent=True)
                plt.close(figUVIndex)
                #Crear Objeto Doble Axial
                src_uvindex_uvindexhigh = f"data:image/png;base64,{base64.b64encode(bufUVIndex.getvalue()).decode('utf-8')}"
                BloqueUVIndex = html.Div([
                    html.Label(id='input-degree-heat-cool',style=label_style,children=['Indicador Energetico']),
                    html.Img(src=src_uvindex_uvindexhigh, style={'width': '100%', 'height': '300px'})
                    ],  
                    style={'width': '100%','textAlign': 'center'}
                )
                #Histograma Degree Refrigeration
                figUVIndex, xUVIndex = plt.subplots(figsize=(10, 6))
                y1 = VectorUVIndex[0];      Stats.timsort(y1);  DatoModa1 = Stats.ModaVectorValor(y1);  MedianaHistUVIndex = Stats.MedianaVector(y1);
                VarianzaInsesgadaHistUVIndex = Stats.DesviacionMediaVector(y1, MediaUVIndex);
                DesviacionHistUVIndex = Stats.DesviacionNewton(VarianzaInsesgadaHistUVIndex);
                Varianza1 = Stats.VarianzaVector(y1);
                DesviacionHistUVIndexNM = Stats.DesviacionNewton(Varianza1);
                PercHistUVIndex = Stats.Percentil(y1, Percentiles);
                figUVIndex.patch.set_alpha(0.0);  xUVIndex.patch.set_alpha(0.0);
                XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
                xUVIndex.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = 'black', color="#8ED7FB",linewidth=4.0, alpha=0.6)
                xUVIndex.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
                xUVIndex.set_xticks([XlimInf1,PercHistUVIndex[0],PercHistUVIndex[1],PercHistUVIndex[2],XlimSup1])
                xUVIndex.set_xticklabels([f'{XlimInf1:.2f}',f'{PercHistUVIndex[0]:.0f}',f'{PercHistUVIndex[1]:.0f}',f'{PercHistUVIndex[2]:.0f}',f'{XlimSup1:.2f}'], color='#DBDBDB', fontsize=14, fontname=fuente)
                for p, val, col in zip(Percentiles,PercHistUVIndex,ColorPerc):
                    xUVIndex.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
                #Codificar
                bufHistUVIndex = io.BytesIO()
                plt.savefig(bufHistUVIndex, format="png", bbox_inches="tight", transparent=True)
                plt.close(figUVIndex)
                src_hist_uv_index = f"data:image/png;base64,{base64.b64encode(bufHistUVIndex.getvalue()).decode('utf-8')}"
                BloqueHistUVIndex = html.Div([
                    html.Img(src=src_hist_uv_index, style={'width': '100%', 'height': '300px'}),
                    html.Label(id='input-hist_uv-index',style=label_style,children=['Radiacion Ultravioleta']),
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
                        html.Strong('Valores Minimos y Maximos'),html.Br(),
                        f'Minimo: {y1[0]:.0f}',f'\tMaximo: {y1[len(y1) - 1]:.0f}',html.Br(),
                        html.Strong('Moda de los datos'),html.Br(),
                        f'{DatoModa1:.0f}',html.Br(),
                        html.Strong('Percentiles'),html.Br(),
                        f'P{Percentiles[0]}: {PercHistUVIndex[0]:.0f}',f'\tP{Percentiles[1]}: {PercHistUVIndex[1]:.0f}',f'\tP{Percentiles[2]}: {PercHistUVIndex[2]:.0f}'
                    ])
                    ],
                    style={'width': '100%','textAlign': 'center'}
                )
                #Histograma Degree Refrigeration
                figUVIndexHigh, xUVIndexHigh = plt.subplots(figsize=(10, 6))
                y1 = VectorUVIndex[1];      Stats.timsort(y1);  DatoModa1 = Stats.ModaVectorValor(y1);  MedianaHistUVIndexHigh = Stats.MedianaVector(y1);
                VarianzaInsesgadaHistUVIndexHigh = Stats.DesviacionMediaVector(y1, MediaHighUVIndex);
                DesviacionHistUVIndexHigh = Stats.DesviacionNewton(VarianzaInsesgadaHistUVIndexHigh);
                Varianza1 = Stats.VarianzaVector(y1);
                DesviacionHistUVIndexHighNM = Stats.DesviacionNewton(Varianza1);
                PercHistUVIndexHigh = Stats.Percentil(y1, Percentiles);
                figUVIndexHigh.patch.set_alpha(0.0);  xUVIndexHigh.patch.set_alpha(0.0);
                XlimInf1 = y1[0];    XlimSup1 = y1[len(y1) - 1];  Rango1 = int(RegladeSturges(len(y1) - 1))
                xUVIndexHigh.hist(y1, bins=Rango1,rwidth = 1.2, edgecolor = 'black', color="#8ED7FB",linewidth=4.0, alpha=0.6)
                xUVIndexHigh.set_xlim(XlimInf1 - 1, XlimSup1 + 1);
                xUVIndexHigh.set_xticks([XlimInf1,PercHistUVIndexHigh[0],PercHistUVIndexHigh[1],PercHistUVIndexHigh[2],XlimSup1])
                xUVIndexHigh.set_xticklabels([f'{XlimInf1:.2f}',f'{PercHistUVIndexHigh[0]:.0f}',f'{PercHistUVIndexHigh[1]:.0f}',f'{PercHistUVIndexHigh[2]:.0f}',f'{XlimSup1:.2f}'], color='#DBDBDB', fontsize=14, fontname=fuente)
                for p, val, col in zip(Percentiles,PercHistUVIndex,ColorPerc):
                    xUVIndex.axvline(val, color=col, linestyle='--', linewidth=2,label=f'P{p}: {val:.2f}')
                #Codificar
                bufHistUVIndexHigh = io.BytesIO()
                plt.savefig(bufHistUVIndexHigh, format="png", bbox_inches="tight", transparent=True)
                plt.close(figUVIndexHigh)
                src_hist_uv_index_high = f"data:image/png;base64,{base64.b64encode(bufHistUVIndexHigh.getvalue()).decode('utf-8')}"
                BloqueHistUVIndexHigh = html.Div([
                    html.Img(src=src_hist_uv_index_high, style={'width': '100%', 'height': '300px'}),
                    html.Label(id='input-hist_uv-index',style=label_style,children=['Maximos de la Radiacion Ultravioleta']),
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
                        html.Strong('Valores Minimos y Maximos'),html.Br(),
                        f'Minimo: {y1[0]:.0f}',f'\tMaximo: {y1[len(y1) - 1]:.0f}',html.Br(),
                        html.Strong('Moda de los datos'),html.Br(),
                        f'{DatoModa1:.0f}',html.Br(),
                        html.Strong('Percentiles'),html.Br(),
                        f'P{Percentiles[0]}: {PercHistUVIndexHigh[0]:.0f}',f'\tP{Percentiles[1]}: {PercHistUVIndexHigh[1]:.0f}',f'\tP{Percentiles[2]}: {PercHistUVIndexHigh[2]:.0f}'
                    ])
                    ],
                    style={'width': '100%','textAlign': 'center'}
                )
                return BloqueSolarSolarRad,BloqueSolarEnergy,BloqueUVIndex, BloqueSolarRadHigh,BloqueHistSolarEnergy,BloqueHistUVIndex,BloqueHistUVIndexHigh, None,None,None, None,None,None,None
            


        else:
            return None,None,None, None,None,None,None, None,None,None, None,None,None,None
    

#if __name__ == '__main__':
#    appEstacion.run(debug=True)
if __name__ == '__main__':
    app.run_server(debug=True)