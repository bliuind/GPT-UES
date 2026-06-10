from math import *
from numpy import *
import numpy as np
import pylab as plt
import ctypes
import csv
import math
import builtins

BookShelf = ctypes.CDLL('./ObjetoANN_lib.so')
BookShelf.eval.argtypes = (ctypes.c_char_p, ctypes.c_double,)
BookShelf.eval.restype  = ctypes.c_double

class Raices:

    def __init__(self):
        pass

    #Definicion del metodo de la Biseccion
    #Funcion, Limite inferior, Limite superior, Error, Iteracciones maximas
    BookShelf.Biseccion.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    BookShelf.Biseccion.restype  = ctypes.c_double

    #Definicion del metodo de la Falsa Posicion
    #Funcion, Limite inferior, Limite superior, Error, Iteracciones maximas
    BookShelf.FalsaPosicion.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    BookShelf.FalsaPosicion.restype  = ctypes.c_double

    #Definicion del metodo del Punto Fijo
    #Funcion F(x), Funcion G(x), Error, Valor inicial, Iteracciones maximas
    BookShelf.PuntoFijo.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    BookShelf.PuntoFijo.restype  = ctypes.c_double

    #Definicion del metodo Newton-Raphson
    #Funcion F(x), Funcion dF(x), Error, Iteraciones maximas, Valor inicial
    BookShelf.NewtonRaphson.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_int, ctypes.c_double]
    BookShelf.NewtonRaphson.restype  = ctypes.c_double

    #Definicion del metodo de la Secante
    #Funcion F(x), Valor i, Valor s, Error, Iteraciones maximas
    BookShelf.Secante.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int]
    BookShelf.Secante.restype  = ctypes.c_double

    def PlotterRoot(self, Function, xli, xls, xr, Titulo, Equation):
        Muestras = 1000;
        Titulo = 'Metodo de' + Titulo;
        plt.title(Titulo)
        x = np.linspace(xli, xls, Muestras)
        y = [BookShelf.eval(Function, xval) for xval in x]
        plt.plot(x, y, color='mediumblue');
        X = xr;
        Y = BookShelf.eval(Function, xr);
        plt.plot(X, Y, 'ro')
        plt.axhline(0, color='darkgrey', linestyle='-');  plt.axvline(0, color='darkgrey', linestyle='-')
        plt.text(xr, BookShelf.eval(Function, xr)+xr*1.2, f'({xr:.4f}, {BookShelf.eval(Function, xr):.4f})', fontsize=10, color='crimson', ha='right')
        plt.text(0.075, 0.99, r'$' +Equation+ r'$', transform=plt.gca().transAxes, fontsize=11, verticalalignment='top',fontweight='bold')
        #plt.annotate(f'x ≈ {xr:.3f}', xy=(xr, 0), xytext=(2 * X, 3 * X),
        #             arrowprops=dict(arrowstyle='->', color='tomato', lw=2),
        #             fontsize=12, color='crimson', fontweight='bold')
        #plt.annotate(f'y ≈ {Y:.3f}', xy=(xr, 0), xytext=(2 * X, -3 * X),
        #             arrowprops=dict(arrowstyle='->', color='tomato', lw=2),
        #             fontsize=12, color='crimson', fontweight='bold')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        plt.show()

    def Biseccion(self, Function, xi, xs, Ea, Iter, FuncionPlot):
        Equation = ctypes.create_string_buffer(Function.encode());
        xr = BookShelf.Biseccion(Equation, xi, xs, Ea, Iter)
        self.PlotterRoot(Equation, -5, 5, xr, ' la Biseccion', FuncionPlot);

    def FalsaPosicion(self, Function, xi, xs, Ea, Iter, FuncionPlot):
        Equation = ctypes.create_string_buffer(Function.encode());
        xr = BookShelf.FalsaPosicion(Equation, xi, xs, Ea, Iter)
        self.PlotterRoot(Equation, -5, 5, xr, ' la Falsa Posicion', FuncionPlot);

    def NewtonRaphson(self, Function, DFunction, Ea, Iter, Vini, FuncionPlot):
        Equation = ctypes.create_string_buffer(Function.encode());
        if DFunction == "":
            DFunction = "0";
            Derivative = ctypes.create_string_buffer(DFunction.encode());
            xr = BookShelf.NewtonRaphson(Equation, Derivative, Ea, Iter, Vini)
        else:
            Derivative = ctypes.create_string_buffer(DFunction.encode());
            xr = BookShelf.NewtonRaphson(Equation, Derivative, Ea, Iter, Vini)
            self.PlotterRoot(Equation, -4, 4, xr, ' Newton-Raphson', FuncionPlot);

    def PuntoFijo(self, Function, GFunction, Ea, Vini, Iter, FuncionPlot):
        Equation = ctypes.create_string_buffer(Function.encode());
        if GFunction == "":
            FunctionG = "0";
            Alternative = ctypes.create_string_buffer(GFunction.encode());
            xr = BookShelf.PuntoFijo(Equation, Alternative, Ea, Vini, Iter)
        else:
            Alternative = ctypes.create_string_buffer(GFunction.encode());
            xr = BookShelf.PuntoFijo(Equation, Alternative, Ea, Vini, Iter)
            self.PlotterRoot(Equation, -5, 5, xr, 'l Punto Fijo', FuncionPlot);

    def Secante(self, Function, xi, xs, EA, Iter, FuncionPlot):
        Equation = ctypes.create_string_buffer(Function.encode());
        xr = BookShelf.Secante(Equation, xi, xs, EA, Iter)
        self.PlotterRoot(Equation, -5, 5, xr, ' la Secante', FuncionPlot);


class ClassCreacionMatrices:

    # Enviar Nombre del Archivo, Tamaño, Salto de Linea | Recibir Fila en Entero
    BookShelf.LeerFilas.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
    BookShelf.LeerFilas.restype = ctypes.c_int

    # Enviar Nombre del Archivo, Tamaño, Salto de Linea | Recibir Columna en Entero
    BookShelf.LeerColumnas.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
    BookShelf.LeerColumnas.restype = ctypes.c_int

    # Enviar Filas, Columnas, Matriz[][] | Imprime la matriz entera
    BookShelf.IMatriz.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_char_p]

    # Enviar Filas, Columnas, Matriz[][] | Imprime la matriz para los metodos de Gauss y GaussJordan
    BookShelf.IMatrizAumentada.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_char_p]
    
    # Enviar Tamaño, Salto de Linea, Nombre del Archivo, Separador | Recibir Matriz
    BookShelf.CrearMatriz.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
    BookShelf.CrearMatriz.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

    # Enviar Tamaño, Salto de Linea, Nombre del Archivo, Separador | Recibir Matriz menos ultima Columna
    BookShelf.CrearMatrizVariables.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
    BookShelf.CrearMatrizVariables.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

    # Enviar Tamaño, Salto de Linea, Nombre del Archivo, Separador | Recibir la ultima Columna como Matriz
    BookShelf.CrearMatrizComplemento.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
    BookShelf.CrearMatrizComplemento.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

    # Enviar Nombre del Archivo, Escribir en consola filas, columnas, y sus elementos
    BookShelf.CrearArchivo.argtypes = [ctypes.c_char_p]

    # Enviar Nombre del Archivo, Escribir en consola filas, columnas, y sus elementos
    BookShelf.CrearArchivoMatriz.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int]

    def __init__(self):
        pass
    
    #Enviar Nombre del archivo, cuantas Lineas Saltar y cuantas Columnas Saltar, la separacion de datos | Recibir numero de Filas
    def LeerFilasArchivo(self, NombreArchivo, SaltoLinea, TamE):
        i = BookShelf.LeerFilas(NombreArchivo.encode(), TamE, SaltoLinea);
        return i;

    #Enviar Nombre del archivo, cuantas Lineas Saltar y cuantas Columnas Saltar, la separacion de datos | Recibir numero de Columnas
    def LeerColumnasArchivo(self, NombreArchivo, SaltoLinea, SaltoColumna, Separador, TamE):
        j = BookShelf.LeerColumnas(NombreArchivo.encode(), SaltoLinea, SaltoColumna, Separador.encode(), TamE);
        return j;

    #Enviar Nombre del archivo, cuantas Lineas Saltar y cuantas Columnas Saltar, la separacion de datos | Recibir una matriz de numeros reales
    def CrearMatrizArchivo(self, NombreArchivo, SaltoLinea, SaltoColumna, Separador, TamE):
        i = BookShelf.LeerFilas(NombreArchivo.encode(), SaltoLinea, TamE);
        j = BookShelf.LeerColumnas(NombreArchivo.encode(), SaltoLinea, SaltoColumna, Separador.encode(), TamE);
        A = BookShelf.CrearMatriz(NombreArchivo.encode(), SaltoLinea, SaltoColumna, Separador.encode(), TamE);
        MatrizA = np.zeros((i, j))
        for m in range(i):
            for n in range(j):
                MatrizA[m, n] = A[m][n]
        np.array(MatrizA)
        return MatrizA;

    #Enviar Nombre del archivo, la separacion de datos, cuantas Lineas Saltar y cuantas Columnas Saltar | Recibir una matriz de caracteres
    def CrearMatrizArchivoString(self, NombreArchivo, Separador, SaltoLinea, SaltoColumna):
        #Crear objeto Matriz
        Matriz = [];
        #Abrir archivo
        with open(NombreArchivo.encode(), mode = 'r', newline='', encoding='utf-8') as CSVfile:
            #Empzar a leer
            Lector = csv.reader(CSVfile, delimiter=Separador)
            for m in range(SaltoLinea):
                next(Lector)
            for row in Lector:
                Filas = [str(Data) for Data in row[SaltoColumna:]]
                Matriz.append(Filas)
        return Matriz
    
    #Enviar Nombre del archivo, la separacion de datos, cuantas Lineas Saltar y cuantas Columnas Saltar | Recibir una matriz de complejos
    def CrearMatrizArchivoFloat(self, NombreArchivo, Separador, SaltoLinea, SaltoColumna):
        #Crear objeto Matriz
        Matriz = [];
        #Abrir archivo
        with open(NombreArchivo.encode(), mode = 'r', newline='', encoding='utf-8') as CSVfile:
            #Empzar a leer
            Lector = csv.reader(CSVfile, delimiter=Separador)
            for m in range(SaltoLinea):
                next(Lector)
            for row in Lector:
                Filas = [float(Data) for Data in row[SaltoColumna:]]
                Matriz.append(Filas)
        return Matriz
    
    #Enviar Nombre del archivo, la separacion de datos, cuantas Lineas Saltar y cuantas Columnas Saltar | Recibir una matriz de complejos
    def CrearMatrizArchivoComplex(self, NombreArchivo, Separador, SaltoLinea, SaltoColumna):
        #Crear objeto Matriz
        Matriz = [];
        #Abrir archivo
        with open(NombreArchivo.encode(), mode = 'r', newline='', encoding='utf-8') as CSVfile:
            #Empzar a leer
            Lector = csv.reader(CSVfile, delimiter=Separador)
            for m in range(SaltoLinea):
                next(Lector)
            for row in Lector:
                Filas = [complex(Data) for Data in row[SaltoColumna:]]
                Matriz.append(Filas)
        return Matriz

    #Enviar Filas, Columnas, la Matriz tipo float, Mensaje que acompañe/identifique la matriz
    def ImprimirMatriz(self, Filas, Columnas, Matriz, Mensaje):
        Filas = len(Matriz); Columnas = len(Matriz[1]);
        Matriz = np.array(Matriz, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        Rows = (DoublePtr * Matriz.shape[0])();
        for i in range(Matriz.shape[0]):
            Rows[i] = Matriz[i].ctypes.data_as(DoublePtr)
        BookShelf.IMatriz(Filas, Columnas, Rows, Mensaje.encode());
    
    #Enviar Filas, Columnas, la Matriz tipo float, Mensaje que acompañe/identifique la matriz 
    def ImprimirMatrizAumentada(self, Filas, Columnas, Matriz, Mensaje):
        Filas = len(Matriz); Columnas = len(Matriz[0]);
        Matriz = np.array(Matriz, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        Rows = (DoublePtr * Matriz.shape[0])();
        for i in range(Matriz.shape[0]):
            Rows[i] = Matriz[i].ctypes.data_as(DoublePtr)
        BookShelf.IMatrizAumentada(Filas, Columnas, Rows, Mensaje.encode());

    #Enviar Nombre del archivo, la separacion de datos, cuantas Lineas Saltar y cuantas Columnas Saltar | Recibir una matriz menos su ultima fila
    def CrearMatrizArchivoVariables(self, NombreArchivo, SaltoLinea, SaltoColumna, Separador, TamE):
        i = BookShelf.LeerFilas(NombreArchivo.encode(), SaltoLinea, TamE);
        j = BookShelf.LeerColumnas(NombreArchivo.encode(), SaltoLinea, SaltoColumna, Separador.encode(), TamE);
        j = j - 1;
        A = BookShelf.CrearMatrizVariables(NombreArchivo.encode(), SaltoLinea, SaltoColumna, Separador.encode(), TamE);
        MatrizA = np.zeros((i, j))
        for m in range(i):
            for n in range(j):
                MatrizA[m, n] = A[m][n]
        np.array(MatrizA)
        return MatrizA;

    #Enviar Matriz | Recibir una matriz menos su ultima fila
    def CrearMatrizVariablesI(self, Matriz):
        Filas = len(Matriz); Columnas = (len(Matriz[0]) - 1);
        MatrizC = [];
        for m in range(Filas):
            Temp = [];
            for n in range(Columnas):
                Variable = Matriz[m][n];
                Temp.append(Variable)
            MatrizC.append(Temp)
        return MatrizC;

    #Enviar Nombre del archivo, la separacion de datos, cuantas Lineas Saltar y cuantas Columnas Saltar | Recibir una matriz pero la ultima fila
    def CrearMatrizArchivoComplemento(self, NombreArchivo, SaltoLinea, SaltoColumna, Separador, TamE):
        i = BookShelf.LeerFilas(NombreArchivo.encode(), SaltoLinea, TamE);
        j = 1
        A = BookShelf.CrearMatrizComplemento(NombreArchivo.encode(), SaltoLinea, SaltoColumna, Separador.encode(), TamE);
        MatrizA = np.zeros((i, j))
        for m in range(i):
            for n in range(j):
                MatrizA[m, n] = A[m][n]
        np.array(MatrizA)
        return MatrizA;

    #Enviar Matriz | Recibir una matriz pero la ultima fila
    def CrearMatrizComplementoI(self, Matriz):
        Filas = len(Matriz); Columnas = len(Matriz[0]);
        MatrizC = [];
        for m in range(Filas):
            Variable = Matriz[m][Columnas - 1];
            MatrizC.append(Variable)
        return MatrizC;

    #Enviar Nombre del archivo para crear matriz mediante inputs y tambien crear el archivo
    def CrearArchivo(self, NombreArchivo):
        BookShelf.CrearArchivo(NombreArchivo.encode())

    #Enviar Matriz y el nombre del archivo en el que se guardara
    def CrearArchivoMatriz(self, NombreArchivo, Matriz):
        Filas = len(Matriz); Columnas = len(Matriz[0]);
        Matriz = np.array(Matriz, dtype=np.float64);    
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        Rows = (DoublePtr * Matriz.shape[0])();
        for i in range(Matriz.shape[0]):
            Rows[i] = Matriz[i].ctypes.data_as(DoublePtr);
        BookShelf.CrearArchivoMatriz(NombreArchivo.encode(), Rows, Filas, Columnas);

    #Enviar la Matriz, El texto que deseas buscar y su Columna | Recibir una matriz con indices y datos utiles
    def CreacionIndice(self, Matriz, TextoBuscar, Columna):
        Fila = len(Matriz); ContadorInicio = 0; ContadorFinal = 1; InicioContador = -1;
        for m in range(Fila):
            if(Matriz[m][Columna] == TextoBuscar):
                if(InicioContador == -1):
                    InicioContador = m;
                else:
                    ContadorInicio = ContadorInicio + 1;
        ContadorFinal = InicioContador + ContadorInicio - 1;
        Indice = [(InicioContador),(ContadorInicio + 1),(ContadorFinal + 2)];
        return Indice;

    #Enviar Matriz, Matriz Indice, Nombre del archivo, en que columnas Inicia y termina, y el separador
    def GuardarMatrizCSV(self, Matriz, MatrizIndice, NombreArchivo, ColumnaInicio, ColumnaFin, Separador):
        FilaInicio = MatrizIndice[0]; FilaFin = MatrizIndice[2];
        print(MatrizIndice[0]); print(MatrizIndice[2]);
        with open(NombreArchivo, mode='w', newline='', encoding='utf-8') as CSVfile:
            Escritor = csv.writer(CSVfile, delimiter=Separador)
            for fila in Matriz[FilaInicio:FilaFin]:
                Escritor.writerow(fila[ColumnaInicio:ColumnaFin])
    
    #Enviar Vector, Cantidad de elementos, Nombre del archivo, por seguridad un separador
    def GuardarVectorCSV(self, Vector, Filas, NombreArchivo, Separador):
        with open(NombreArchivo,mode='w', newline='',encoding='utf-8') as CSVfile:
            Escritor = csv.writer( CSVfile,delimiter=Separador)
            for indice in range(Filas):
                Escritor.writerow([Vector[indice]])

class OperacionReales:

    #MultiplicacionEscalar
    BookShelf.MultiplicacionEscalar.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int, ctypes.c_double]
    BookShelf.MultiplicacionEscalar.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

    # Enviar Matriz A, Matriz B, Filas Matriz A, Columnas Matriz A, Filas Matriz B, Columnas Matriz B || Recibir Matriz R = Matriz A + Matriz B
    BookShelf.SumaMatrices.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    BookShelf.SumaMatrices.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

    # Enviar Matriz A, Matriz B, Filas Matriz A, Columnas Matriz A, Filas Matriz B, Columnas Matriz B || Recibir Matriz R = Matriz A - Matriz B
    BookShelf.RestaMatrices.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    BookShelf.RestaMatrices.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

    # Enviar Matriz A, Matriz B, Filas Matriz A, Columnas Matriz A, Filas Matriz B, Columnas Matriz B || Recibir Matriz R = Matriz A * Matriz B solo si ColumnasA = FilasB
    BookShelf.MultiplicacionMatrices.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    BookShelf.MultiplicacionMatrices.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

    # Enviar Matriz A, Matriz B, Filas Matriz A, Columnas Matriz B || Recibir Matriz R = Matriz A x Matriz B solo si ColumnasA = FilasB
    BookShelf.ProductoSchur.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int]
    BookShelf.ProductoSchur.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

    # Enviar Matriz A, Filas Matriz A, Columnas Matriz A || Recibir A^t solo si Filas = Columnas
    BookShelf.MatrizTraspuesta.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int]
    BookShelf.MatrizTraspuesta.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

    # Enviar Matriz A, Filas Matriz A, Columnas Matriz A || Recibir el determinante solo si Filas = Columnas
    BookShelf.DeterminanteMatrizSarrus.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int]
    BookShelf.DeterminanteMatrizSarrus.restype = ctypes.c_double
    
    # Enviar Matriz A, Filas Matriz A, Columnas Matriz A || Recibir el determinante solo si Filas = Columnas
    BookShelf.DeterminanteMatrizSuperior.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]
    BookShelf.DeterminanteMatrizSuperior.restype = ctypes.c_double

    # Enviar Matriz A, Filas Matriz A, Columnas Matriz A || Recibir el determinante solo si Filas = Columnas
    BookShelf.Inversa.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]

    # Enviar Matriz, Filas Matriz, Columnas Matriz || Metodo de Gauss
    BookShelf.MetodoGauss.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int]
    
    # Enviar Matriz, Filas Matriz, Columnas Matriz || Metodo de Gauss-Gordan
    BookShelf.MetodoGaussJordan.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int]
    
    # Enviar Matriz, Filas Matriz, Columnas Matriz, Iteraciones, Error || Metodo de Gauss
    BookShelf.MetodoGaussSeiden.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double]

    # Enviar Matriz A, Filas Matriz A, Columnas Matriz A || 
    BookShelf.DescomposicionLU.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int]

    def __init__(self):
        pass
    
    #Enviar Matriz y un Escalar | Recibir Matriz * Escalar
    def MultiplicacionEscalar(self, Matriz, Escalar):
        Filas = len(Matriz); Columnas = len(Matriz[0]);
        Matriz = np.array(Matriz, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        Rows = (DoublePtr * Matriz.shape[0])();
        for i in range(Matriz.shape[0]):
            Rows[i] = Matriz[i].ctypes.data_as(DoublePtr);
        MatrizR = BookShelf.MultiplicacionEscalar(Rows, Filas, Columnas, Escalar);
        MatrizResultado = np.zeros((Filas, Columnas));
        for m in range(Filas):
            for n in range(Columnas):
                MatrizResultado[m, n] = MatrizR[m][n]
        np.array(MatrizResultado);
        return MatrizResultado;
    
    #Enviar Dos matrices | Suma de Matrices reales
    def SumaM(self, MatrizA, MatrizB):
        FilasA = len(MatrizA); ColumnasA = len(MatrizA[0]); FilasB = len(MatrizB); ColumnasB = len(MatrizB[0]);
        MatrizA = np.array(MatrizA, dtype=np.float64);
        MatrizB = np.array(MatrizB, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsA = (DoublePtr * MatrizA.shape[0])(); 
        RowsB = (DoublePtr * MatrizB.shape[0])();
        for i in range(MatrizA.shape[0]):
            RowsA[i] = MatrizA[i].ctypes.data_as(DoublePtr);
        for i in range(MatrizB.shape[0]):
            RowsB[i] = MatrizB[i].ctypes.data_as(DoublePtr);
        MatrizC = BookShelf.SumaMatrices(RowsA, RowsB, FilasA, ColumnasA, FilasB, ColumnasB);
        MatrizResultado = np.zeros((FilasA, ColumnasA));
        for a in range(FilasA):
            for b in range(ColumnasA):
                MatrizResultado[a, b] = MatrizC[a][b]
        np.array(MatrizResultado);
        return MatrizResultado;

    #Enviar Dos matrices | Resta de Matrices reales
    def RestaM(self, MatrizA, MatrizB):
        FilasA = len(MatrizA); ColumnasA = len(MatrizA[0]);
        FilasB = len(MatrizB); ColumnasB = len(MatrizB[0]);
        MatrizA = np.array(MatrizA, dtype=np.float64);
        MatrizB = np.array(MatrizB, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsA = (DoublePtr * MatrizA.shape[0])();
        RowsB = (DoublePtr * MatrizB.shape[0])();
        for i in range(MatrizA.shape[0]):
            RowsA[i] = MatrizA[i].ctypes.data_as(DoublePtr)
        for i in range(MatrizB.shape[0]):
            RowsB[i] = MatrizB[i].ctypes.data_as(DoublePtr)
        MatrizC = BookShelf.RestaMatrices(RowsA, RowsB, FilasA, ColumnasA, FilasB, ColumnasB);
        MatrizResultado = np.zeros((FilasA, ColumnasA));
        for a in range(FilasA):
            for b in range(ColumnasA):
                MatrizResultado[a, b] = MatrizC[a][b]
        np.array(MatrizResultado);
        return MatrizResultado;

    #Enviar Dos matrices | Multiplicacion de Matrices reales
    def MultiplicacionM(self, MatrizA, MatrizB):
        FilasA = len(MatrizA); ColumnasA = len(MatrizA[0]);
        FilasB = len(MatrizB); ColumnasB = len(MatrizB[0]);
        MatrizA = np.array(MatrizA, dtype=np.float64);
        MatrizB = np.array(MatrizB, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsA = (DoublePtr * MatrizA.shape[0])();
        RowsB = (DoublePtr * MatrizB.shape[0])();
        for i in range(MatrizA.shape[0]):
            RowsA[i] = MatrizA[i].ctypes.data_as(DoublePtr)
        for i in range(MatrizB.shape[0]):
            RowsB[i] = MatrizB[i].ctypes.data_as(DoublePtr)
        MatrizC = BookShelf.MultiplicacionMatrices(RowsA, RowsB, FilasA, ColumnasA, FilasB, ColumnasB);
        MatrizResultado = np.zeros((FilasA, ColumnasB));
        for a in range(FilasA):
            for b in range(ColumnasB):
                MatrizResultado[a, b] = MatrizC[a][b]
        np.array(MatrizResultado);
        return MatrizResultado;

    #Enviar Dos matrices | Recibir Multiplicacion Elemento por Elemento
    def Hadamard(self, MatrizA, MatrizB):
        FilasA = len(MatrizA); ColumnasA = len(MatrizA[0]);
        FilasB = len(MatrizB); ColumnasB = len(MatrizB[0]);
        if(FilasA != FilasB and ColumnasA != ColumnasB):
            print("Las matrices no son del mismo orden mxn");
        else:
            DoublePtr = ctypes.POINTER(ctypes.c_double);
            RowsA = (DoublePtr * MatrizA.shape[0])();
            RowsB = (DoublePtr * MatrizB.shape[0])();
            for i in range(MatrizA.shape[0]):
                RowsA[i] = MatrizA[i].ctypes.data_as(DoublePtr)
            for i in range(MatrizB.shape[0]):
                RowsB[i] = MatrizB[i].ctypes.data_as(DoublePtr)
            MatrizR = BookShelf.ProductoSchur(RowsA, RowsB, FilasA, ColumnasA, FilasB, ColumnasB);
            MatrizResultado = np.zeros((FilasA, ColumnasB));
            for m in range(FilasA):
                for n in range(ColumnasB):
                    MatrizResultado[m, n] = MatrizR[m][n]
            np.array(MatrizResultado);
            return MatrizResultado;

    #Enviar Matriz | Recibir la traspuesta de una Matriz
    def TraspuestaM(self, T):
        FilasT = len(T); ColumnasT = len(T[0]);
        MatrizT = np.array(T, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsT = (DoublePtr * MatrizT.shape[0])();
        for i in range(MatrizT.shape[0]):
            RowsT[i] = MatrizT[i].ctypes.data_as(DoublePtr)
        MatrizR = BookShelf.MatrizTraspuesta(RowsT, FilasT, ColumnasT);
        MatrizResultado = np.zeros((FilasT, ColumnasT));
        for a in range(FilasT):
            for b in range(ColumnasT):
                MatrizResultado[a, b] = MatrizR[a][b]
        np.array(MatrizResultado);
        return MatrizResultado;

    #Enviar Matriz | Recibir determinante para Matrices 3x3 con el Metodo de Sarrus
    def DetMSarrus(self, D):
        FilasD = len(D); ColumnasD = len(D[0]);
        MatrizD = np.array(D, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsD = (DoublePtr * MatrizD.shape[0])();
        for i in range(MatrizD.shape[0]):
            RowsD[i] = MatrizD[i].ctypes.data_as(DoublePtr)
        Res = BookShelf.DeterminanteMatrizSarrus(RowsD, FilasD, ColumnasD);
        return Res;

    #Enviar Matriz y su Tamaño asumiendo M*M ; Funcion Recursiva | Recibir un numero
    def DetMSuperior(self, D):
        FilasD = len(D); ColumnasD = len(D[0]);
        if(FilasD != ColumnasD):
            print("No es una matriz cuadrada"); print();
        else:
            MatrizD = np.array(D, dtype=np.float64);
            DoublePtr = ctypes.POINTER(ctypes.c_double);
            RowsD = (DoublePtr * MatrizD.shape[0])();
            for i in range(MatrizD.shape[0]):
                RowsD[i] = MatrizD[i].ctypes.data_as(DoublePtr)
            Res = BookShelf.DeterminanteMatrizSuperior(RowsD, FilasD);
            return Res;

    #Enviar Matriz asumiendo M*M
    def MatrizInversa(self, I):
        FilasI = len(I); ColumnasI = len(I[0]);
        if(FilasI != ColumnasI):
            print("No es una matriz cuadrada"); print();
        else:
            MatrizI = np.array(I, dtype=np.float64);
            DoublePtr = ctypes.POINTER(ctypes.c_double);
            RowsI = (DoublePtr * MatrizI.shape[0])();
            for i in range(MatrizI.shape[0]):
                RowsI[i] = MatrizI[i].ctypes.data_as(DoublePtr)
            Res = BookShelf.Inversa(RowsI, FilasI);
            return Res;

    #Enviar Matriz para Metodo de Gauss para Matrices Reales 
    def Gauss(self, G):
        FilasG = len(G); ColumnasG = len(G[0]);
        MatrizG = np.array(G, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsG = (DoublePtr * MatrizG.shape[0])();
        for i in range(MatrizG.shape[0]):
            RowsG[i] = MatrizG[i].ctypes.data_as(DoublePtr)
        Res = BookShelf.MetodoGauss(RowsG, FilasG, ColumnasG);
    
    #Enviar Matriz para Metodo de Gauss-Jordan para Matrices Reales 
    def Jordan(self, J):
        FilasJ = len(J); ColumnasJ = len(J[0]);
        MatrizJ = np.array(J, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsJ = (DoublePtr * MatrizJ.shape[0])();
        for i in range(MatrizJ.shape[0]):
            RowsJ[i] = MatrizJ[i].ctypes.data_as(DoublePtr)
        Res = BookShelf.MetodoGaussJordan(RowsJ, FilasJ, ColumnasJ);

    #Enviar Matriz para Metodo de Gauss-Seidel para Matrices Reales 
    def Seiden(self, S, MaxIter, Error):
        FilasS = len(S); ColumnasS = len(S[0]);
        MatrizS = np.array(S, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsS = (DoublePtr * MatrizS.shape[0])();
        for i in range(MatrizS.shape[0]):
            RowsS[i] = MatrizS[i].ctypes.data_as(DoublePtr)
        Res = BookShelf.MetodoGaussSeiden(RowsS, FilasS, ColumnasS, MaxIter, Error);

    #Enviar Matriz para Metodo de DescomposicionLU para Matrices Reales 
    def Descomposicion(self, D):
        FilasD = len(D); ColumnasD = len(D[0]);
        MatrizD = np.array(D, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsD = (DoublePtr * MatrizD.shape[0])();
        for i in range(MatrizD.shape[0]):
            RowsD[i] = MatrizD[i].ctypes.data_as(DoublePtr)
        Res = BookShelf.DescomposicionLU(RowsD, FilasD, ColumnasD);

class OperacionesImaginarias:

    def __init__(self):
        pass

    #Enviar una matriz y un escalar por el que sera multiplicado | Recibir Matriz * Escalar
    def MultiplicacionEscalarI(self, Matriz, Escalar):
        Filas = len(Matriz); Columnas = len(Matriz[0]);
        print("Multiplicacion de un escalar a una matriz")
        for m in range(Filas):
            for n in range(Columnas):
                    Matriz[m][n] = Escalar * Matriz[m][n];
        return Matriz;

    #Enviar Dos matrices | Suma de Matrices en complejos
    def SumaMComplex(self, MatrizA, MatrizB):
        FilasA = len(MatrizA); ColumnasA = len(MatrizA[0]); FilasB = len(MatrizB); ColumnasB = len(MatrizB[0]);
        if(FilasA != FilasB and ColumnasA != ColumnasB):
            print("Suma Incompatible")
        else:
            print("Suma de Matrices")
            MatrizS = [];
            for m in range(FilasB):
                Temp = [];
                for n in range(ColumnasA):
                    Suma = MatrizA[m][n] + MatrizB[m][n];
                    Temp.append(Suma)
                MatrizS.append(Temp)
            return MatrizS;

    #Enviar Dos matrices | Resta de Matrices en complejos
    def RestaMComplex(self, MatrizA, MatrizB):
        FilasA = len(MatrizA); ColumnasA = len(MatrizA[0]); FilasB = len(MatrizB); ColumnasB = len(MatrizB[0]);
        if(FilasA != FilasB and ColumnasA != ColumnasB):
            print("Resta Incompatible")
        else:
            print("Resta de Matrices")
            MatrizR = [];
            for m in range(FilasB):
                Temp = [];
                for n in range(ColumnasA):
                    Suma = MatrizA[m][n] + MatrizB[m][n];
                    Temp.append(Suma)
                MatrizR.append(Temp)
            return MatrizR;

    #Enviar Dos matrices | Multiplicacion de Matrices en complejos
    def MultiplicacionMI(self, MatrizA, MatrizB):
        FilasA = len(MatrizA); ColumnasA = len(MatrizA[0]); FilasB = len(MatrizB); ColumnasB = len(MatrizB[0]);
        if(ColumnasA != FilasB):
            print("Multiplicacion Incompatible")
        else:
            print("Multiplicacion de Matrices")
            MatrizM = [];
            for p in range(FilasA):
                Temp = [];
                for q in range(ColumnasB):
                    Sum = 0;
                    for r in range(FilasB):
                        Sum = Sum + (MatrizA[p][r] * MatrizB[r][q]);
                    Temp.append(Sum)
                MatrizM.append(Temp)
            return MatrizM;

    #Enviar Dos matrices | Recibir Multiplicacion Elemento por Elemento en complejos
    def HadamardI(self, MatrizA, MatrizB):
        FilasA = len(MatrizA); ColumnasA = len(MatrizA[0]); FilasB = len(MatrizB); ColumnasB = len(MatrizB[0]);
        if(FilasA != FilasB and ColumnasA != ColumnasB):
            print("Operacion Incompatible")
        else:
            print("Producto Shur | Hadamard")
            MatrizH = [];
            for m in range(FilasB):
                Temp = [];
                for n in range(ColumnasA):
                    Suma = MatrizA[m][n] * MatrizB[m][n];
                    Temp.append(Suma)
                MatrizH.append(Temp)
            return MatrizH;
    
    #Enviar Matriz | Recibir la traspuesta de una Matriz
    def TraspuestaMI(self, T):
        FilasT = len(T); ColumnasT = len(T[0]);
        if(FilasT != ColumnasT):
            print("Solo matrices Cuadradas")
        else:
            print("La traspuesta de una matriz")
            MatrizT = [];
            for m in range(FilasT):
                Temp = [];
                for n in range(ColumnasT):
                    Crear = 0;
                    Temp.append(Crear)
                MatrizT.append(Temp)
            for m in range(FilasT):
                for n in range(ColumnasT):
                    MatrizT[m][n] = T[n][m]
            return MatrizT;
    
    #Enviar Matriz y su Tamaño asumiendo M*M ; Funcion Recursiva | Recibir un numero
    def DeterminanteI(self, Matriz, NewSize):
        Determinante = 0; Signo = 1
        SubMatriz = [];
        for m in range(NewSize):
                Temp = [];
                for n in range(NewSize):
                    Crear = 0;
                    Temp.append(Crear)
                SubMatriz.append(Temp)
        if(NewSize == 1):
            return Matriz[0][0];
        if(NewSize == 2):
            return ((Matriz[0][0] * Matriz[1][2]) - (Matriz[0][1] * Matriz[1][0]));
        for r in range(NewSize):
            SubFila = 0;
            for p in range(NewSize):
                SubColumna = 0;
                for q in range(NewSize):
                    if(q == r):
                        continue;
                    SubMatriz[SubFila][SubColumna] = Matriz[p][q];
                    SubColumna = SubColumna + 1
                SubFila = SubFila + 1
            Determinante = Determinante + (Signo * Matriz[0][r] * self.DeterminanteI(SubMatriz, NewSize - 1))
            Signo = Signo * -1;
        return Determinante;

    #Enviar Matriz, Matriz Temp, indice del numero y su Tamaño asumiendo M*M ; Funcion para MatrizInversaI
    def CofactorMatriz(self, Matriz, Temp, p, q, NewSize):
        i = 0; j = 0;
        for NewRows in range(NewSize):
            for NewCol in range(NewSize):
                if(NewRows != p and NewCol != q):
                    j = j + 1
                    Temp[i][j] = Matriz[NewRows][NewCol]
                    if(j == (NewSize - 1)):
                        j = 0;
                        i = i + 1;

    #Enviar Matriz y su Tamaño asumiendo M*M
    def MatrizInversaI(self, Matriz, NewSize):
        print("La inversa de una matriz");
        Adjunta = []; Temp = [];
        for m in range(NewSize):
            NewTemp = [];
            for n in range(NewSize):
                Void = 0;
                NewTemp.append(Void)
            Adjunta.append(NewTemp)
            Temp.append(NewTemp)
        Signo = 1;
        for i in range(NewSize):
            for j in range(NewSize):
                self.CofactorMatriz(Matriz, Temp, i, j, NewSize);
                Signo = 1 if ((i + j) % 2 == 0) else -1;
                Adjunta[j][i] = Signo * self.DeterminanteI(Temp, NewSize - 1);
        Determinante = self.DeterminanteI(Matriz, NewSize)
        print("Determinante: ", Determinante);
        if(Determinante == 0):
            print("Determinante es 0, no posee inversa");
        else:
            Determinante = 1 / Determinante
            for x in range(NewSize):
                for y in range(NewSize):
                    Matriz[x][y] = Matriz[x][y] * Determinante;
            for row in Matriz:
                print(row)

    #Enviar Matriz para Metodo de Gauss para Matrices Imaginarias 
    def GaussI(self, Matriz):
        Filas = len(Matriz); Columnas = len(Matriz[0]); FilasG = Filas; ColumnasG = Columnas - 1;
        print("Metodo de Gauss para matrices"); MatrizGauss = [];
        for m in range(Filas):
            Temp = [];
            for n in range(Columnas):
                Temp.append(Matriz[m][n])
            MatrizGauss.append(Temp)
        for i in range(Filas):
            Divisor = Matriz[i][i]
            for j in range(i, Filas + 1):
                Matriz[i][j] /= Divisor
            for k in range(i + 1, Filas):
                Factor = Matriz[k][i]
                for j in range(i, Filas + 1):
                    Matriz[k][j] -= Factor * Matriz[i][j]
        VectorS = [0] * Filas
        for i in range(Filas - 1, -1, -1):
            VectorS[i] = Matriz[i][Filas]
            for j in range(i + 1, Filas):
                VectorS[i] -= Matriz[i][j] * VectorS[j]
        for a in range(len(VectorS)):
                print(f"Solucion x{a+1}"f"= {VectorS[i]:.8f} ")
        i = 0;
        for row in Matriz:
            print(row);
        for i in range(FilasG):
            Sumatoria = 0;
            for j in range(ColumnasG):
                Sumatoria = Sumatoria + (MatrizGauss[i][j] * VectorS[j])
            Error = (MatrizGauss[i][ColumnasG] - Sumatoria) / MatrizGauss[i][ColumnasG];
            print("Ecuacion",i+1,f"= {Sumatoria:.6f}"f"\tError: {Error:.8f}");
        print("");
    
    #Enviar Matriz para Metodo de Gauss-Jordan para Matrices Imaginarias 
    def GaussJordanI(self, Matriz):
        Filas = len(Matriz); Columnas = len(Matriz[0]); FilasGJ = Filas; ColumnasGJ = Columnas - 1;
        print("Metodo de Gauss-Jordan para matrices");
        MatrizGaussJordan = []; VectorSoluciones = [];
        for m in range(Filas):
            Temp = [];
            for n in range(Columnas):
                Temp.append(Matriz[m][n])
            MatrizGaussJordan.append(Temp)
            VectorSoluciones.append(0)
        for i in range(Filas):
            Divisor = Matriz[i][i]
            for k in range(i, Filas + 1):
                Matriz[i][k] /= Divisor
            for k in range(Filas):
                if k != i:
                    Factor = Matriz[k][i]
                    for j in range(i, Filas + 1):
                        Matriz[k][j] -= Factor * Matriz[i][j]
        for row in Matriz:
            print(row);
        for z in range(len(VectorSoluciones)):
            VectorSoluciones[z] = Matriz[z][ColumnasGJ];
            print("Solucion x",z+1,f":{VectorSoluciones[z]:.12f}")
        for i in range(FilasGJ):
            Sumatoria = 0;
            for j in range(ColumnasGJ):
                Sumatoria = Sumatoria + (MatrizGaussJordan[i][j] * VectorSoluciones[j])
            Error = (MatrizGaussJordan[i][ColumnasGJ] - Sumatoria) / MatrizGaussJordan[i][ColumnasGJ];
            print("Ecuacion",i+1,f"= {Sumatoria:.8f}  "f"\tError: {Error:.8f}");
        print("");

    #Enviar Matriz para Metodo de Gauss-Seidel para Matrices Imaginarias 
    def GaussSeidelI(self, Matriz, MaxIter, Error):
        print("Metodo de Gauss-Seiden para matrices");
        Filas = len(Matriz); Columnas = len(Matriz[0]); FilasH = Filas; ColumnasH = Columnas - 1;
        MatrizSeidel = []; ValorEstimado = []; ValorOld = [];
        for m in range(Filas):
            Temp = [];
            for n in range(Columnas):
                Temp.append(Matriz[m][n])
            MatrizSeidel.append(Temp)
            ValorEstimado.append(0);
            ValorOld.append(0);
        print(MatrizSeidel); print(ValorEstimado); print(ValorOld);
        i = 0; j = 0; Iter = 0; Sumatoria = 0;
        for Iter in range(MaxIter):
            for i in range(Filas):
                Sumatoria = 0;
                for j in range(Columnas - 1):
                    if(i != j):
                        Sumatoria = Sumatoria + (Matriz[i][j] * ValorEstimado[j])
                ValorEstimado[i] = (Matriz[i][Filas] - Sumatoria) / Matriz[i][i];
            MaxDiff = 0; i = 0;
            for i in range(Filas):
                Diff = abs(ValorEstimado[i] - ValorOld[i]);
                if(Diff > MaxDiff):
                    MaxDiff = Diff;
                ValorOld[i] = ValorEstimado[i];
            if(MaxDiff < Error):
                break;
        if(Iter == MaxIter):
            print("Se alcanco el maximo numero de interaciones")
        else:
            print(f"Convergencia alcanzada en {Iter:.0f} iteraciones."); i = 0;
            for i in range(len(ValorEstimado)):
                print("x",i+1,"=",ValorEstimado[i]," ")
            i = 0; j = 0; 
            for i in range(FilasH):
                Sumatoria = 0;
                for j in range(ColumnasH):
                    Sumatoria = Sumatoria + (MatrizSeidel[i][j] * ValorEstimado[j])
                Error = (MatrizSeidel[i][ColumnasH] - Sumatoria) / MatrizSeidel[i][ColumnasH];
                print("Ecuacion",i+1,f"= {Sumatoria:.6f}"f"\tError: {Error:.8f}");

    #Enviar Matriz para Metodo de DescomposicionLU para Matrices Imaginarias 
    def DescomposicionLU(self, Matriz):
        print("Metodo de Descomposicion LU para matrices");
        Filas = len(Matriz); Columnas = len(Matriz[0]); FilasL = Filas; ColumnasL = Columnas - 1;
        MatrizL = []; MatrizU = []; VectorSoluciones = []; VectorHelper = [];
        for p in range(Filas):
            TempL = []; TempU = [];
            for q in range(Columnas):
                if(p == q):
                    TempL.append(1);
                else:
                    TempL.append(0)
                TempU.append(Matriz[p][q]);
            MatrizL.append(TempL)
            MatrizU.append(TempU)
            VectorSoluciones.append(0)
            VectorHelper.append(Matriz[p][ColumnasL])
        for m in range(FilasL):
            Contador = 0; Factor = 0;
            for n in range(ColumnasL):
                if(n < m):
                    FactorSup = complex(MatrizU[m][n]); FactorInf = complex(MatrizU[Contador][n]); Factor = FactorSup / FactorInf;
                    for l in range(ColumnasL):
                        MatrizU[m][l] = MatrizU[m][l] - (Factor * MatrizU[Contador][l]);
                    MatrizL[m][n] = Factor; Contador = Contador + 1;
        print("Matriz D:");
        for g in range(FilasL):
            Sumatoria = 0;
            for h in range(ColumnasL):
                if(g != h):
                    Sumatoria = Sumatoria + (MatrizL[g][h] * VectorHelper[h])
            VectorSoluciones[g] = VectorHelper[g] - Sumatoria; VectorHelper[g] = VectorSoluciones[g];
            print("Elemento",g+1,":",VectorSoluciones[g]);
        print("Matriz L:");
        for row in MatrizL:
            print(row)
        print("");
        print("Matriz U:");
        for row in MatrizU:
            print(row)   
        print("");
        ElementoIJ = 0; i = FilasL - 1; j = ColumnasL - 1;
        while(i >= 0):
            Sumatoria = 0;
            while(j >= 0):
                ElementoIJ = MatrizU[i][i];
                if(j > i):
                    Sumatoria = Sumatoria + (VectorSoluciones[j] * MatrizU[i][j])
                if(j == i):
                    Sumatoria = (VectorSoluciones[j] - Sumatoria) / ElementoIJ;
                j = j - 1;
            VectorSoluciones[i] = Sumatoria;
            print(f"x{i+1:.0f}: "f"{VectorSoluciones[i]:.8f}");
            i = i - 1; j = ColumnasL - 1;

class Estadistica:
    #Enviar Matriz y Tamaño del array | Recibir media
    BookShelf.MediaAritmetica.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]
    BookShelf.MediaAritmetica.restype = ctypes.c_double

    #Enviar Vector y Tamaño del array | Recibir media
    BookShelf.MediaAritmeticaVector.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
    BookShelf.MediaAritmeticaVector.restype = ctypes.c_double

    #Enviar Matriz, Tamaño del array, media | Recibir Desviacion con media
    BookShelf.DesviacionMedia.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_double]
    BookShelf.DesviacionMedia.restype = ctypes.c_double

    #Enviar Vector, Tamaño del array, media | Recibir Desviacion con media
    BookShelf.DesviacionMediaVector.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_double]
    BookShelf.DesviacionMediaVector.restype = ctypes.c_double

    #Enviar Matriz y Tamaño del array | Recibir Desviacion y sin media
    BookShelf.Varianza.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]
    BookShelf.Varianza.restype = ctypes.c_double

    #Enviar Vector y Tamaño del array | Recibir Desviacion y sin media
    BookShelf.VarianzaVector.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
    BookShelf.VarianzaVector.restype = ctypes.c_double

    #Enviar Varianza | Recibir la raiz cuadrada de la Varianza
    BookShelf.DesviacionSinMedia.argtypes = [ctypes.c_double]
    BookShelf.DesviacionSinMedia.restype = ctypes.c_double

    #Enviar Varianza | Recibir la raiz cuadrada de la Varianza con el metodo Newton Raphson
    BookShelf.DesviacionNewton.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_int, ctypes.c_double]
    BookShelf.DesviacionNewton.restype  = ctypes.c_double

    #Enviar Matriz y Tamaño del array | Recibir el Dato Maximo
    BookShelf.DatoMaximo.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]
    BookShelf.DatoMaximo.restype = ctypes.c_double

    #Enviar Matriz y Tamaño del array | Recibir el Dato Minimo
    BookShelf.DatoMinimo.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]
    BookShelf.DatoMinimo.restype = ctypes.c_double

    #Enviar Dato maximo, Dato Minimo | Recibir Rango
    BookShelf.Rango.argtypes = [ctypes.c_double, ctypes.c_double]
    BookShelf.Rango.restype = ctypes.c_double

    #Enviar Dato maximo, Dato Minimo | Recibir Rango
    BookShelf.Mediana.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]
    BookShelf.Mediana.restype = ctypes.c_double

    #Enviar Dato maximo, Dato Minimo | Recibir Rango
    BookShelf.MedianaVector.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
    BookShelf.MedianaVector.restype = ctypes.c_double

    #Enviar Matriz y Rango | Recibir Rango
    BookShelf.Moda.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]

    #Enviar Matriz y Rango | Recibir Rango
    BookShelf.ModaVector.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
    BookShelf.ModaVector.restype = ctypes.c_int

    #Enviar Matriz y Rango | Recibir Rango
    BookShelf.ModaVectorValor.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
    BookShelf.ModaVectorValor.restype = ctypes.c_double

    #Enviar Matriz y Rango, vector y Tamaño | Recibir Rango
    BookShelf.Percentiles.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int]
    BookShelf.Percentiles.restype = ctypes.POINTER(ctypes.c_double)

    BookShelf.IntervaloConfianza.argtypes = [ctypes.c_double, ctypes.c_int, ctypes.c_double, ctypes.c_int]

    #Enviar Matriz, Tamaño del array, Dato Inferior, Dato Superior | Recibir la cantidad de eventos entre el rango
    BookShelf.BusquedaEventosExcluyente.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_double, ctypes.c_double]
    BookShelf.BusquedaEventosExcluyente.restype = ctypes.c_double

    #Enviar Matriz, Tamaño del array, Dato Inferior, Dato Superior | Recibir la cantidad de eventos entre e iguales del rango
    BookShelf.BusquedaEventosIncluyente.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_double, ctypes.c_double]
    BookShelf.BusquedaEventosIncluyente.restype = ctypes.c_double

    def __init__(self):
        pass
    
    #Enviar Matriz | Recibir la media
    def Media(self, Matriz):
        Fila = len(Matriz);
        MatrizDatos = np.array(Matriz, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsDatos = (DoublePtr * MatrizDatos.shape[0])();
        for i in range(MatrizDatos.shape[0]):
            RowsDatos[i] = MatrizDatos[i].ctypes.data_as(DoublePtr)
        Media = BookShelf.MediaAritmetica(RowsDatos, Fila);
        return Media;

    def MediaVector(self, Vector):
        Fila = len(Vector);
        VectorDatos = (ctypes.c_double * len(Vector))(*Vector)
        Media = BookShelf.MediaAritmeticaVector(VectorDatos, Fila);
        return Media;

    #Enviar Matriz y la media | Recibir la Desviacion estandar
    def DesviacionMedia(self, Matriz, Media):
        Fila = len(Matriz);
        MatrizDatos = np.array(Matriz, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsDatos = (DoublePtr * MatrizDatos.shape[0])();
        for i in range(MatrizDatos.shape[0]):
            RowsDatos[i] = MatrizDatos[i].ctypes.data_as(DoublePtr)
        DesviacionM = BookShelf.DesviacionMedia(RowsDatos, Fila, Media);
        return DesviacionM;

    def DesviacionMediaVector(self, Vector, Media):
        Fila = len(Vector);
        VectorDatos = (ctypes.c_double * len(Vector))(*Vector)
        DesviacionM = BookShelf.DesviacionMediaVector(VectorDatos, Fila, Media);
        return DesviacionM;

    #Enviar Matriz | Recibir la Desviacion estandar
    def Varianza(self, Matriz):
        Fila = len(Matriz);
        MatrizDatos = np.array(Matriz, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsDatos = (DoublePtr * MatrizDatos.shape[0])();
        for i in range(MatrizDatos.shape[0]):
            RowsDatos[i] = MatrizDatos[i].ctypes.data_as(DoublePtr)
        Varianza = BookShelf.Varianza(RowsDatos, Fila);
        return Varianza;

    def VarianzaVector(self, Vector):
        Fila = len(Vector);
        VectorDatos = (ctypes.c_double * len(Vector))(*Vector)
        Varianza = BookShelf.VarianzaVector(VectorDatos, Fila);
        return Varianza;

    def DesviacionSinMedia(self, Varianza):
        Desv = BookShelf.DesviacionSinMedia(Varianza)
        return Desv

    def DesviacionNewton(self, Varianza):
        if Varianza <= 0.0:
            return 0.0
        Function = 'x^2-'+f'{Varianza:.8f}'
        DFunction = '2*x'
        Equation = ctypes.create_string_buffer(Function.encode());
        DEquation = ctypes.create_string_buffer(DFunction.encode());
        Ea = 0.0001;  Iter = 100;
        Vini = Varianza if Varianza >= 1.0 else 1.0
        xr = BookShelf.DesviacionNewton(Equation, DEquation, Ea, Iter, Vini)
        return xr;

    #Enviar Matriz | Recibir el dato mas grande
    def DatoMaximo(self, Matriz):
        Fila = len(Matriz);
        MatrizDatos = np.array(Matriz, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsDatos = (DoublePtr * MatrizDatos.shape[0])();
        for i in range(MatrizDatos.shape[0]):
            RowsDatos[i] = MatrizDatos[i].ctypes.data_as(DoublePtr)
        DatoM = BookShelf.DatoMaximo(RowsDatos, Fila);
        return DatoM;

    #Enviar Matriz | Recibir el dato mas pequeño
    def DatoMinimo(self, Matriz):
        Fila = len(Matriz);
        MatrizDatos = np.array(Matriz, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsDatos = (DoublePtr * MatrizDatos.shape[0])();
        for i in range(MatrizDatos.shape[0]):
            RowsDatos[i] = MatrizDatos[i].ctypes.data_as(DoublePtr)
        DatoM = BookShelf.DatoMinimo(RowsDatos, Fila);
        return DatoM;

    def Rango(self, DatMax, DatMin):
        R = BookShelf.Rango(DatMax, DatMin)
        return R;

    def Mediana(self, Matriz):
        Rango = len(Matriz);
        MatrizDatos = np.array(Matriz, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsDatos = (DoublePtr * MatrizDatos.shape[0])();
        for i in range(MatrizDatos.shape[0]):
            RowsDatos[i] = MatrizDatos[i].ctypes.data_as(DoublePtr)
        Mid = BookShelf.Mediana(RowsDatos, Rango);
        return Mid;

    def MedianaVector(self, Vector):
        Rango = len(Vector);
        VectorDatos = (ctypes.c_double * len(Vector))(*Vector)
        Mid = BookShelf.MedianaVector(VectorDatos, Rango);
        return Mid;

    def Moda(self, Matriz):
        Fila = len(Matriz);
        MatrizDatos = np.array(Matriz, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsDatos = (DoublePtr * MatrizDatos.shape[0])();
        for i in range(MatrizDatos.shape[0]):
            RowsDatos[i] = MatrizDatos[i].ctypes.data_as(DoublePtr)
        BookShelf.Moda(RowsDatos, Fila);
    
    def ModaVector(self, Vector):
        Fila = len(Vector);
        VectorDatos = (ctypes.c_double * len(Vector))(*Vector)
        Moda = BookShelf.ModaVector(VectorDatos, Fila);
        return Moda;

    def ModaVectorValor(self, Vector):
        Fila = len(Vector);
        VectorDatos = (ctypes.c_double * len(Vector))(*Vector)
        DatoModa = BookShelf.ModaVectorValor(VectorDatos, Fila);
        return DatoModa;

    def Percentil(self, Matriz, Percentiles):
        Rango = len(Matriz); Tamaño = len(Percentiles)
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        VectorPuntos = (ctypes.c_double * len(Matriz))(*Matriz)
        VectorDatos = (ctypes.c_double * len(Percentiles))(*Percentiles)
        Vector = BookShelf.Percentiles(VectorPuntos, VectorDatos, Rango, Tamaño)
        Perc = np.zeros(Tamaño);
        for a in range(Tamaño):
            Perc[a] = Vector[a]
        return Perc;

    def Interval(self, MatrizPuntos, Intervalo):
        TamañoMuestral = len(MatrizPuntos)
        Media = self.Media(MatrizPuntos)
        Desviacion = self.DesviacionMedia(MatrizPuntos, Media)
        BookShelf.IntervaloConfianza(Desviacion, TamañoMuestral, Media, Intervalo)

    #Enviar Matriz, Dato Rango inferior, Dato Rango Superior | Recibir cantidad de eventos entre el rango
    def BusquedaLlave(self, Matriz, DatoInf, DatoSup):
        Fila = len(Matriz);
        MatrizDatos = np.array(Matriz, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsDatos = (DoublePtr * MatrizDatos.shape[0])();
        for i in range(MatrizDatos.shape[0]):
            RowsDatos[i] = MatrizDatos[i].ctypes.data_as(DoublePtr)
        ConteoDatos = BookShelf.BusquedaEventosExcluyente(RowsDatos, Fila, DatoInf, DatoSup);
        return ConteoDatos;

    #Enviar Matriz, Dato Rango inferior, Dato Rango Superior | Recibir cantidad de eventos entre e iguales al rango
    def BusquedaCorchete(self, Matriz, DatoInf, DatoSup):
        Fila = len(Matriz);
        MatrizDatos = np.array(Matriz, dtype=np.float64);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        RowsDatos = (DoublePtr * MatrizDatos.shape[0])();
        for i in range(MatrizDatos.shape[0]):
            RowsDatos[i] = MatrizDatos[i].ctypes.data_as(DoublePtr)
        ConteoDatos = BookShelf.BusquedaEventosIncluyente(RowsDatos, Fila, DatoInf, DatoSup);
        return ConteoDatos;
    
    #Ordenar Datos | No recomendado
    def Selection_Sort(self, Matriz):
        Tamaño = len(Matriz)
        for i in range(Tamaño - 1):
            # Assume the current position holds
            # the minimum element
            Min_idx = i
            # Iterate through the unsorted portion
            # to find the actual minimum
            for j in range(i + 1, Tamaño):
                if Matriz[j][0] < Matriz[Min_idx][0]:
                    # Update min_idx if a smaller element is found
                    Min_idx = j
            # Move minimum element to its
            # correct position
            Matriz[i][0], Matriz[Min_idx][0] = Matriz[Min_idx][0], Matriz[i][0]
        return Matriz;

    #Funciones necesarias para el metodo de ordenar "Tim Sort"
    #Calcular el alcance minimo de la iteracion
    def calcMinRun(self, n):
        minRUN = 32;
        r = 0
        while n >= minRUN:
            r |= n & 1
            n >>= 1
        return n + r
    
    #Metodo "Insertion Sort" para tamaños pequeños
    def insertionSort(self, arr, left, right):
        for i in range(left + 1, right + 1):
            key = arr[i]
            j = i - 1
            while j >= left and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
    #Une dos Arrays ya ordenados
    def merge(self, arr, l, m, r):
        left = arr[l:m+1]
        right = arr[m+1:r+1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
    #Detecta la iteracion ascendente/descendente
    def findRun(self, arr, start, n):
        end = start + 1
        if end == n: return end
        if arr[end] < arr[start]:
            # descending
            while end < n and arr[end] < arr[end - 1]:
                end += 1
            arr[start:end] = reversed(arr[start:end])
        else:
            # ascending
            while end < n and arr[end] >= arr[end - 1]:
                end += 1
        return end
    # Timsort main function
    def timsort(self, arr):
        n = len(arr)
        minRun = self.calcMinRun(n)
        runs = []
        i = 0
        while i < n:
            runEnd = self.findRun(arr, i, n)
            runLen = runEnd - i
            if runLen < minRun:
                end = builtins.min(i + minRun, n)
                self.insertionSort(arr, i, end - 1)
                runEnd = end
            runs.append((i, runEnd))
            i = runEnd
            while len(runs) > 1:
                l1, r1 = runs[-2]
                l2, r2 = runs[-1]
                len1, len2 = r1 - l1, r2 - l2
                if len1 <= len2:
                    self.merge(arr, l1, r1 - 1, r2 - 1)
                    runs.pop()
                    runs[-1] = (l1, r2)
                else:
                    break
        while len(runs) > 1:
            l1, r1 = runs[-2]
            l2, r2 = runs[-1]
            self.merge(arr, l1, r1 - 1, r2 - 1)
            runs.pop()
            runs[-1] = (l1, r2)
    #Finalizacion del metodo de ordenar "Tim Sort"

    def DatosEstadisticos(self, Matriz, Percentiles, Intervalo):
        print("Datos estadisticos referentes a la Matriz de Datos");
        Media = self.Media(Matriz)
        print(f"La media del conjunto: {Media:.6f}");
        DesvM = self.DesviacionMedia(Matriz, Media)
        print(f"La desviacion estandar del conjunto: {DesvM:.16f}");
        Var = self.Varianza(Matriz)
        print(f"La Varianza del conjunto: {DesvM:.16f}");
        Desv = self.DesviacionSinMedia(Var)
        print(f"La desviacion estandar sin media aritmetica del conjunto: {Desv:.16f}");
        DatMax = self.DatoMaximo(Matriz)
        print(f"El dato mas alto es: {DatMax:.4f}");
        DatMin = self.DatoMinimo(Matriz)
        print(f"El dato mas bajo es: {DatMin:.4f}");
        Rango = self.Rango(DatMax, DatMin)
        print(f"El rango de el conjunto es: {Rango:.2f}");
        Mid = self.Mediana(Matriz)
        print(f"La mediana de el conjunto es: {Mid:.4f}");
        self.Moda(Matriz)
        self.Interval(Matriz, Intervalo)
        X = []; Indice = [0,0,len(Matriz)]
        for i in range(len(Matriz)):
            X.append(Matriz[i][0]);
        x = []; y = []; i = 0; j = 0; Contador = 0;
        while(i < len(X)):
            if(i == 0):
                x.append(X[0])
                i = i + 1;
            if(x[j] == X[i]):
                i = i + 1;
                Contador = Contador + 1;
            if(x[j] != X[i]):
                y.append(Contador)
                Contador = 0;
                j = j + 1;
                x.append(X[i]);
                i = i + 1;
            if(i == len(X)):
                y.append(Contador)
        Perc = self.Percentil(x, Percentiles)
        for i in range(len(Perc)):
            plt.axvline(x=Perc[i], color='red', linestyle='-', linewidth=2)
        #plt.bar(x,y,width=0.8,color='black')
        hist, bin_edges = np.histogram(x, 30)
        n, bins, patches = plt.hist(x, bins=bin_edges, alpha=0.7, edgecolor='black', linewidth=1.2, rwidth=1)
        plt.xticks(bin_edges)
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Intervalos')
        plt.ylabel('Frecuencia')
        plt.title("Histograma de frecuencia")
        plt.show()

class AjusteDeCurvas:

    BookShelf.ST.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]
    BookShelf.ST.restype = ctypes.c_double

    BookShelf.SR.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_double]
    BookShelf.SR.restype = ctypes.c_double

    BookShelf.SRExp.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_double]
    BookShelf.SRExp.restype = ctypes.c_double

    BookShelf.STPot.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]
    BookShelf.STPot.restype = ctypes.c_double

    BookShelf.SRPot.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_double]
    BookShelf.SRPot.restype = ctypes.c_double

    BookShelf.SRLog.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_double]
    BookShelf.SRLog.restype = ctypes.c_double

    BookShelf.RegresionLineal.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]
    BookShelf.RegresionLineal.restype = ctypes.POINTER(ctypes.c_double)


    BookShelf.RegresionPolinomial.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int]
    BookShelf.RegresionPolinomial.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

    BookShelf.RegresionLogaritmica.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]
    BookShelf.RegresionLogaritmica.restype = ctypes.POINTER(ctypes.c_double)

    BookShelf.RegresionExponencial.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]
    BookShelf.RegresionExponencial.restype = ctypes.POINTER(ctypes.c_double)

    BookShelf.RegresionPotencial.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]
    BookShelf.RegresionPotencial.restype = ctypes.POINTER(ctypes.c_double)

    def __init__(self):
        pass

    def ST(self, Matriz):
        Rango = len(Matriz);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        Rows = (DoublePtr * Matriz.shape[0])();
        for i in range(Matriz.shape[0]):
            Rows[i] = Matriz[i].ctypes.data_as(DoublePtr)
        DesviacionC = BookShelf.ST(Rows, Rango);
        return DesviacionC;

    def SR(self, Matriz, Vector):
        Rango = len(Matriz); Grado = len(Vector)
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        VectorPtr = Vector.ctypes.data_as(DoublePtr)
        Rows = (DoublePtr * Matriz.shape[0])();
        for i in range(Matriz.shape[0]):
            Rows[i] = Matriz[i].ctypes.data_as(DoublePtr)
        ErrorE = BookShelf.SR(Rows, VectorPtr, Rango, Grado);
        return ErrorE;

    def SRExp(self, Matriz, Vector):
        Rango = len(Matriz); Grado = len(Vector)
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        VectorPtr = Vector.ctypes.data_as(DoublePtr)
        Rows = (DoublePtr * Matriz.shape[0])();
        for i in range(Matriz.shape[0]):
            Rows[i] = Matriz[i].ctypes.data_as(DoublePtr)
        ErrorE = BookShelf.SRExp(Rows, VectorPtr, Rango, Grado);
        return ErrorE;

    def STPot(self, Matriz):
        Rango = len(Matriz);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        Rows = (DoublePtr * Matriz.shape[0])();
        for i in range(Matriz.shape[0]):
            Rows[i] = Matriz[i].ctypes.data_as(DoublePtr)
        DesviacionC = BookShelf.STPot(Rows, Rango);
        return DesviacionC;

    def SRPot(self, Matriz, Vector):
        Rango = len(Matriz); Grado = len(Vector)
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        VectorPtr = Vector.ctypes.data_as(DoublePtr)
        Rows = (DoublePtr * Matriz.shape[0])();
        for i in range(Matriz.shape[0]):
            Rows[i] = Matriz[i].ctypes.data_as(DoublePtr)
        ErrorE = BookShelf.SRPot(Rows, VectorPtr, Rango, Grado);
        return ErrorE;

    def SRLog(self, Matriz, Vector):
        Rango = len(Matriz); Grado = len(Vector)
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        VectorPtr = Vector.ctypes.data_as(DoublePtr)
        Rows = (DoublePtr * Matriz.shape[0])();
        for i in range(Matriz.shape[0]):
            Rows[i] = Matriz[i].ctypes.data_as(DoublePtr)
        ErrorE = BookShelf.SRLog(Rows, VectorPtr, Rango, Grado);
        return ErrorE;

    def CoeficienteDeterminacion(self, Desviacion, Error):
        CD = (Desviacion - Error) / Desviacion;
        return CD;

    def CoeficienteCorrelacion(self, CoeficienteDeterminacion):
        CC = sqrt(CoeficienteDeterminacion);
        return CC;

    def RegresionL(self, Matriz):
        Rango = len(Matriz);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        Rows = (DoublePtr * Matriz.shape[0])();
        for i in range(Matriz.shape[0]):
            Rows[i] = Matriz[i].ctypes.data_as(DoublePtr)
        Auxiliar = BookShelf.RegresionLineal(Rows, Rango);
        Vector = np.zeros(2);
        for a in range(2):
            Vector[a] = Auxiliar[a]
        return Vector;

    def RegresionP(self, Matriz, Grado):
        Rango = len(Matriz);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        Rows = (DoublePtr * Matriz.shape[0])();
        for i in range(Matriz.shape[0]):
            Rows[i] = Matriz[i].ctypes.data_as(DoublePtr)
        Auxiliar = BookShelf.RegresionPolinomial(Rows, Rango, Grado);
        Filas = Grado + 1; Columnas = Grado + 2;
        Vector = np.zeros(Filas);
        for a in range(Filas):
            Vector[a] = Auxiliar[a][Columnas - 1]
        return Vector;

    def RegresionExp(self, Matriz):
        Rango = len(Matriz);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        Rows = (DoublePtr * Matriz.shape[0])();
        for i in range(Matriz.shape[0]):
            Rows[i] = Matriz[i].ctypes.data_as(DoublePtr)
        Auxiliar = BookShelf.RegresionExponencial(Rows, Rango);
        Vector = np.zeros(2);
        for a in range(2):
            Vector[a] = Auxiliar[a]
        return Vector;

    def RegresionPot(self, Matriz):
        Rango = len(Matriz);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        Rows = (DoublePtr * Matriz.shape[0])();
        for i in range(Matriz.shape[0]):
            Rows[i] = Matriz[i].ctypes.data_as(DoublePtr)
        Auxiliar = BookShelf.RegresionPotencial(Rows, Rango);
        Vector = np.zeros(2);
        for a in range(2):
            Vector[a] = Auxiliar[a]
        return Vector;

    def RegresionLog(self, Matriz):
        Rango = len(Matriz);
        DoublePtr = ctypes.POINTER(ctypes.c_double);
        Rows = (DoublePtr * Matriz.shape[0])();
        for i in range(Matriz.shape[0]):
            Rows[i] = Matriz[i].ctypes.data_as(DoublePtr)
        Auxiliar = BookShelf.RegresionLogaritmica(Rows, Rango);
        Vector = np.zeros(2);
        for a in range(2):
            Vector[a] = Auxiliar[a]
        return Vector;

    def DatosEstadisticosCurvas(self, Matriz, Vector, Metodo):
        Rango = len(Matriz);
        if(Metodo == 'Lineal'):
            print("Metodo de Regresion Lineal");
            ST = self.ST(Matriz)
            SR = self.SR(Matriz, Vector)
            Sy = sqrt(ST / (Rango - 1))
            print(f"Desviacion estandar: {Sy:.8f}");
            Sr = sqrt(SR / (Rango - 2))
            print(f"Error estandar Estimado: {Sr:.8f}");
        if(Metodo == 'Polinomial'):
            print("Metodo de Regresion Polinomial");
            ST = self.ST(Matriz)
            SR = self.SR(Matriz, Vector)
            Grado = len(Vector) - 1;
            Sy = sqrt(SR / (Rango - (Grado + 1)))
            print(f"Error estandar Estimado: {Sy:.8f}");
        if(Metodo == 'Exponencial'):
            print("Metodo de Regresion Exponencial");
            ST = self.STPot(Matriz)
            SR = self.SRExp(Matriz, Vector)
            Vector[0] = exp(Vector[0])
            Vector[1] = exp(Vector[1])
        if(Metodo == 'Potencial'):
            print("Metodo de Regresion Potencial");
            ST = self.STPot(Matriz)
            SR = self.SRPot(Matriz, Vector)
            Vector[0] = exp(Vector[0])
        if(Metodo == 'Logaritmica'):
            print("Metodo de Regresion Logaritmico");
            ST = self.ST(Matriz)
            SR = self.SRLog(Matriz, Vector)
        CD = self.CoeficienteDeterminacion(ST,SR)
        print(f"El coeficiente de Determinacion es de: {CD:.8f}");
        CC = self.CoeficienteCorrelacion(CD)
        print(f"El coeficiente de Correlacion es de: {CC:.8f}");
        self.PlottCurvas(Matriz, Vector, Metodo, CD, CC)

    def ComparacionCurvas(self, Matriz):
        Rango = len(Matriz);
        m = Matriz[:,0]; n = Matriz[:,1];

        #Regresion Lineal
        VectorL = self.RegresionL(Matriz)
        TerminosL = []
        for grado, coef in enumerate(VectorL):
            if coef == 0:
                continue
            if grado == 0:
                txt_termino = f"{coef:.4f}"
            elif grado == 1:
                txt_termino = f"{coef:.4f}*x"
            if coef > 0 and len(TerminosL) > 0:
                txt_termino = f"+{txt_termino}"
            TerminosL.append(txt_termino)
        EcuacionL = "".join(TerminosL)
        print("Regresion Lineal: ", EcuacionL);

        #Regresion Polinomial
        VectorP = self.RegresionP(Matriz, 2)
        TerminosP = []
        for grado, coef in enumerate(VectorP):
            if coef == 0:
                continue
            if grado == 0:
                txt_termino = f"{coef:.4f}"
            elif grado == 1:
                txt_termino = f"{coef:.4f}*x"
            else:
                txt_termino = f"{coef:.4f}*x^{grado}"
            if coef > 0 and len(TerminosP) > 0:
                txt_termino = f"+{txt_termino}"
            TerminosP.append(txt_termino)
        EcuacionP = "".join(TerminosP)
        print("Regresion Polinomial: ", EcuacionP);

        #Regresion Exponencial
        VectorExp = self.RegresionExp(Matriz)
        VectorExp[0] = exp(VectorExp[0])
        VectorExp[1] = exp(VectorExp[1])
        TerminoA0Exp = VectorExp[0] ; TerminoA1Exp = VectorExp[1]
        EcuacionExp = f"{TerminoA0Exp}*"
        if TerminoA1Exp > 0:
            EcuacionExp += f"({TerminoA1Exp}^x)"
        elif TerminoA1Exp < 0:
            EcuacionExp += f"(-{TerminoA1Exp}^x)"
        EcuacionExp += ")"
        print("Regresion Exponencial: ", EcuacionExp);

        #Regresion Potencial
        VectorPot = self.RegresionPot(Matriz)
        VectorPot[0] = exp(VectorPot[0])
        TerminoA0Pot = VectorPot[0] ; TerminoA1Pot = VectorPot[1]
        EcuacionPot = f"{TerminoA0Pot}*(x"
        if TerminoA1Pot > 0:
            EcuacionPot += f"^{TerminoA1Pot}"
        elif TerminoA1Pot < 0:
            EcuacionPot += f"^{TerminoA1Pot}"
        EcuacionPot += ")"
        print("Regresion Potencial: ", EcuacionPot);

        #Regresion Logaritmica
        VectorLog = self.RegresionLog(Matriz)
        TerminoA0Log = VectorLog[0] ; TerminoA1Log = VectorLog[1]
        EcuacionLog = f"{TerminoA0Log}"
        if TerminoA1Log > 0:
            EcuacionLog += f"+{TerminoA1Log}*log(x)"
        elif TerminoA1Log < 0:
            EcuacionLog += f"{TerminoA1Log}*log(x)"
        EcuacionLog += ")"
        print("Regresion Logaritmica: ", EcuacionLog);

        plt.scatter(m, n, color='red', marker='o', s=50, label='Puntos')
        x = np.linspace(min(m), max(m), 1000)
        FunctionL = ctypes.create_string_buffer(EcuacionL.encode());
        y1 = [BookShelf.eval(FunctionL, xval) for xval in x]
        FunctionP = ctypes.create_string_buffer(EcuacionP.encode());
        y2 = [BookShelf.eval(FunctionP, xval) for xval in x]
        FunctionExp = ctypes.create_string_buffer(EcuacionExp.encode());
        y3 = [BookShelf.eval(FunctionExp, xval) for xval in x]
        FunctionPot = ctypes.create_string_buffer(EcuacionPot.encode());
        y4 = [BookShelf.eval(FunctionPot, xval) for xval in x]
        FunctionLog = ctypes.create_string_buffer(EcuacionLog.encode());
        y5 = [BookShelf.eval(FunctionLog, xval) for xval in x]

        Titulo = "Grafica de comparacion de 'regresion'"
        plt.title(Titulo)
        plt.plot(x,y1,label='Lineal')
        plt.plot(x,y2,label='Polinomial')
        plt.plot(x,y3,label='Exponencial')
        plt.plot(x,y4,label='Potencial')
        plt.plot(x,y5,label='Logaritmica')
        plt.axhline(0, color='black', linestyle='-')
        plt.axvline(0, color='black', linestyle='-')
        plt.xlabel('x');   plt.ylabel('y');
        plt.legend()
        plt.xlim(min(m)-2, max(m)+2);   plt.ylim(min(n)-10, max(n)+10)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5);
        plt.show();

    def PlottCurvas(self, Matriz, Vector, Metodo, CD, CC):
        m = Matriz[:,0]; n = Matriz[:,1];
        if(Metodo == 'Lineal'):
            print("Metodo de Regresion Lineal");
            Titulo="Regresion Lineal";
            Terminos = []
            for grado, coef in enumerate(Vector):
                if coef == 0:
                    continue
                if grado == 0:
                    txt_termino = f"{coef:.4f}"
                elif grado == 1:
                    txt_termino = f"{coef:.4f}*x"
                if coef > 0 and len(Terminos) > 0:
                    txt_termino = f"+{txt_termino}"
                Terminos.append(txt_termino)
            Ecuacion = "".join(Terminos)
        if(Metodo == 'Polinomial'):
            print("Metodo de Regresion Polinomial");
            Terminos = []
            Titulo="Regresion Polinomial";
            for grado, coef in enumerate(Vector):
                if coef == 0:
                    continue
                if grado == 0:
                    txt_termino = f"{coef:.4f}"
                elif grado == 1:
                    txt_termino = f"{coef:.4f}*x"
                else:
                    txt_termino = f"{coef:.4f}*x^{grado}"
                if coef > 0 and len(Terminos) > 0:
                    txt_termino = f"+{txt_termino}"
                Terminos.append(txt_termino)
            Ecuacion = "".join(Terminos)
        if(Metodo == 'Exponencial'):
            print("Metodo de Regresion Exponencial");
            Titulo="Regresion Exponencial";
            TerminoA0 = Vector[0] ; TerminoA1 = Vector[1]
            Ecuacion = f"{TerminoA0}*"
            if TerminoA1 > 0:
                Ecuacion += f"({TerminoA1}^x)"
            elif TerminoA1 < 0:
                Ecuacion += f"(-{TerminoA1}^x)"
            Ecuacion += ")"
        if(Metodo == 'Potencial'):
            print("Metodo de Regresion Potencial");
            Titulo="Regresion Potencial";
            TerminoA0 = Vector[0] ; TerminoA1 = Vector[1]
            Ecuacion = f"{TerminoA0}*(x"
            if TerminoA1 > 0:
                Ecuacion += f"^{TerminoA1}"
            elif TerminoA1 < 0:
                Ecuacion += f"^{TerminoA1}"
            Ecuacion += ")"
        if(Metodo == 'Logaritmica'):
            print("Metodo de Regresion Logaritmica");
            Titulo="Regresion Logaritmica";
            TerminoA0 = Vector[0] ; TerminoA1 = Vector[1]
            Ecuacion = f"{TerminoA0}"
            if TerminoA1 > 0:
                Ecuacion += f"+{TerminoA1}*log(x)"
            elif TerminoA1 < 0:
                Ecuacion += f"{TerminoA1}*log(x)"
            Ecuacion += ")"
        Function = ctypes.create_string_buffer(Ecuacion.encode());
        X = len(Matriz)
        x = np.linspace(min(m), max(m), 1000)
        y = [BookShelf.eval(Function, xval) for xval in x]
        plt.title(Titulo.encode())
        plt.scatter(m, n, color='red', marker='o', s=50, label='Puntos')
        plt.plot(x,y,label='Funcion')
        plt.axhline(0, color='black', linestyle='-')
        plt.ylabel('y')
        plt.axvline(0, color='black', linestyle='-')
        plt.legend()
        plt.xlim(min(m)-2, max(m)+2);   plt.ylim(min(n)-10, max(n)+10) 
        Ecuacion = 'f(x)='+Ecuacion
        CoefD = 'Coef. Determinante: '+f'{CD:.4f}'
        CoefC = 'Coef. de Correlacion: '+f'{CC:.4f}'
        plt.text(0.65, 0.23, Ecuacion, transform=plt.gca().transAxes, fontsize=8, verticalalignment='top')
        plt.text(0.65, 0.13, CoefD, transform=plt.gca().transAxes, fontsize=8, verticalalignment='top')
        plt.text(0.65, 0.07, CoefC, transform=plt.gca().transAxes, fontsize=8, verticalalignment='top')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5);
        plt.show();

    def DiferenciasDivididas(self, x, y):
        Rango = len(y);
        coef = np.zeros([Rango, Rango]) 
        coef[:,0] = y 
        for j in range(1, Rango):
            for i in range(Rango - j):
                coef[i][j] = (coef[i+1][j-1] - coef[i][j-1]) / (x[i+j] - x[i])
        return coef[0, :]

    def PolinomioNewton(self, coef, x_data, x):
        n = len(coef) - 1 
        p = coef[n] 
        for k in range(1, n + 1):
            p = coef[n - k] + (x - x_data[n - k]) * p
        return p

    def PolinomioLagrange(self,x, y, valor):
        Suma = 0; Rango = len(x);
        for i in range(Rango):
            producto = y[i]
            for j in range(Rango):
                if i != j:
                    producto *= (valor - x[j]) / (x[i] - x[j])
            Suma += producto
        return Suma 
    
    def PolinomioN(self, MatrizPuntos, Punto, Titulo):
        m = MatrizPuntos[:,0]; n = MatrizPuntos[:,1];
        Titulo = 'Newton'
        Coeficientes = self.DiferenciasDivididas(m, n);
        XGrafica = np.linspace(np.min(m), np.max(m), 100)
        YGrafica = self.PolinomioNewton(Coeficientes, m, XGrafica)
        YEvaluado = self.PolinomioNewton(Coeficientes, m, Punto)
        self.PlotterPolinomios(m, n, Titulo, Punto, Coeficientes, XGrafica, YGrafica, YEvaluado)
    
    def InterpolacionLineal(self, MatrizPuntos, Punto1, Punto2, Punto):
        plt.title('Interpolación de Polinomios Lineal')
        x = MatrizPuntos[:,0]; y = MatrizPuntos[:,1]; MaxY = len(MatrizPuntos)
        ecuacion = f'{MatrizPuntos[Punto1][1]:.2}'
        a = (MatrizPuntos[Punto2][1]-MatrizPuntos[Punto1][1])/(MatrizPuntos[Punto2][0]-MatrizPuntos[Punto1][0])
        ecuacion = ecuacion + f'+{a:.2}'+f'*(x-{MatrizPuntos[Punto1][0]:.2})'
        Ecuation = ctypes.create_string_buffer(ecuacion.encode());
        ecuacion = 'f(x)=' + ecuacion
        XEval = Punto;  YEval = BookShelf.eval(Ecuation, XEval)
        if XEval < min(x):
            XlimInf = XEval;
        else:
            XlimInf = min(x)
        if XEval > max(x):
            XlimSup = XEval;
        else:
            XlimSup = max(x)
            
        if YEval < min(y):
            YlimInf = YEval;
        else:
            YlimInf = min(y)
        if YEval > max(y):
            YlimSup = YEval;
        else:
            YlimSup = max(y)
        plt.xlim(XlimInf-2, XlimSup+2);   plt.ylim(YlimInf-2, YlimSup+2) 
        XGraph = np.linspace(XlimInf-20, XlimSup+20, 1000);  YGraph = [BookShelf.eval(Ecuation, i) for i in XGraph]
        plt.axhline(0, color='black', linestyle='-');   plt.axvline(0, color='black', linestyle='-')
        plt.plot(XGraph, YGraph, label="Linea de Interpolacion")
        plt.plot(x, y, 'ro', label='Datos')
        plt.text(0.5, 0.5, ecuacion, transform=plt.gca().transAxes, fontsize=8, verticalalignment='top')
        plt.scatter(XEval, YEval, color='green' , label=f'Punto evaluado (x={XEval}, y={YEval:.2f})')
        plt.xlabel('x');    plt.ylabel('y')
        plt.legend()
        plt.grid(True, which='both', linestyle='--', linewidth=0.5);
        plt.show()

    def InterpolacionCuadratica(self, MatrizPuntos, Punto1, Punto2, Punto3, Punto):
        plt.title('Interpolación de Polinomios Cuadratica')
        x = MatrizPuntos[:,0]; y = MatrizPuntos[:,1]; MaxY = len(MatrizPuntos)
        ecuacion = f'{MatrizPuntos[Punto1][1]:.2}'
        b1 = (MatrizPuntos[Punto2][1]-MatrizPuntos[Punto1][1])/(MatrizPuntos[Punto2][0]-MatrizPuntos[Punto1][0])
        Term1 = (MatrizPuntos[Punto3][1]-MatrizPuntos[Punto2][1])/(MatrizPuntos[Punto3][0]-MatrizPuntos[Punto2][0])
        Term2 = (MatrizPuntos[Punto2][1]-MatrizPuntos[Punto1][1])/(MatrizPuntos[Punto2][0]-MatrizPuntos[Punto1][0])
        b2 = (Term1 - Term2)/(MatrizPuntos[Punto3][0] - MatrizPuntos[Punto1][0])
        ecuacion = ecuacion + f'+{b1:.2}'+f'*(x-{MatrizPuntos[Punto1][0]:.2})'
        ecuacion = ecuacion + f'+{b2:.2}'+f'*(x-{MatrizPuntos[Punto1][0]:.2})'+f'*(x-{MatrizPuntos[Punto2][0]:.2})'
        Ecuation = ctypes.create_string_buffer(ecuacion.encode());
        ecuacion = 'f(x)=' + ecuacion
        XEval = Punto;  YEval = BookShelf.eval(Ecuation, XEval)
        if XEval < min(x):
            XlimInf = XEval;
        else:
            XlimInf = min(x)
        if XEval > max(x):
            XlimSup = XEval;
        else:
            XlimSup = max(x)
            
        if YEval < min(y):
            YlimInf = YEval;
        else:
            YlimInf = min(y)
        if YEval > max(y):
            YlimSup = YEval;
        else:
            YlimSup = max(y)
        plt.xlim(XlimInf-2, XlimSup+2);   plt.ylim(YlimInf-2, YlimSup+2)
        XGraph = np.linspace(XlimInf-20, XlimSup+20, 1000);  YGraph = [BookShelf.eval(Ecuation, i) for i in XGraph]
        plt.axhline(0, color='black', linestyle='-');   plt.axvline(0, color='black', linestyle='-')
        plt.plot(XGraph, YGraph, label="Linea de Interpolacion")
        plt.plot(x, y, 'ro', label='Datos')
        plt.text(0.5, 0.11, ecuacion, transform=plt.gca().transAxes, fontsize=8, verticalalignment='top')
        plt.scatter(XEval, YEval, color='green' , label=f'Punto evaluado (x={XEval}, y={YEval:.2f})')
        plt.xlabel('x');    plt.ylabel('y')
        plt.legend()
        plt.grid(True, which='both', linestyle='--', linewidth=0.5);
        plt.show()
    
    def PolinomioL(self, MatrizPuntos, Punto, Titulo):
        m = MatrizPuntos[:,0]; n = MatrizPuntos[:,1];
        Coeficientes = self.DiferenciasDivididas(m, n);
        YEvaluado = self.PolinomioLagrange(m, n, Punto)
        XGrafica = np.linspace(min(m), max(m), 100)
        YGrafica = [self.PolinomioLagrange(m, n, i) for i in XGrafica]
        YEvaluado = self.PolinomioLagrange(m, n, Punto)
        self.PlotterPolinomios(m, n, Titulo, Punto, Coeficientes, XGrafica, YGrafica, YEvaluado)

    def PlotterPolinomios(self, m, n, Titulo, XInteres, Coeficientes, XGrafica, YGrafica, YEvaluado):
        plt.plot(XGrafica, YGrafica, label=Titulo)
        plt.plot(m, n, 'ro', label='Datos originales')
        ecuacion = 'f(x) = '
        for i, coef in enumerate(Coeficientes):
            ecuacion += f'{coef:.2f}' 
            for j in range(i):
                ecuacion += f'*(x-{m[j]:.1f})' 
            if i != len(Coeficientes) - 1:
                ecuacion += ' + ' 
        print(f"El valor del polinomio en x = {XInteres} es: {YEvaluado:.2f}")
        plt.title('Interpolación de Polinomios')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.text(0.5, 0.5, ecuacion, transform=plt.gca().transAxes, fontsize=8, verticalalignment='top')
        plt.text(0.5, 0.45, f"El valor del polinomio en x = {XInteres} es: {YEvaluado:.4f}", transform=plt.gca().transAxes, fontsize=8, verticalalignment='top')
        plt.scatter(XInteres, YEvaluado, color='red', label=f'Punto evaluado (x={XInteres}, y={YEvaluado:.2f})')
        plt.scatter(XInteres, math.log(XInteres), color='green', label=f'Punto evaluado (x={XInteres}, y={math.log(XInteres)})')
        plt.show()

    def InterpolacionLinealNoGraph(self, Datos, Indice, Rango):
        i = 0;
        while(i < Rango):
            #Es el inicio del array un elemento "--"
            if(Datos[i] == "--" and i == 0):
                #Tomamos esta posicion
                Posicion1 = i;
                #Mientras asi sea seguira buscando
                while(Datos[i] == "--"):
                    i = i + 1;
                    #LLego al final del array?
                    if(i == (Rango - 1)):   
                        print("Columna vacia por perdida de paquetes")
                        break;
                #Si salio del ciclo while que tome estos valores
                x1 = float(Indice[i])        
                y1 = float(Datos[i])
                #Segunda posicion relevante
                Posicion2 = i;
                i = i + 1;
                #Vuelve a buscar en el array
                while(Datos[i] == "--"):
                    i = i + 1;
                    #LLego al final del array?
                    if(i == (Rango - 1)):   
                        print("Columna vacia por perdida de paquetes")
                        break;
                x2 = float(Indice[i])        
                y2 = float(Datos[i])
                a = (y2-y1)/(x2-x1)
                ecuacion = f'{y1:.2}'
                ecuacion = ecuacion + f'+{a:.2}'+f'*(x-{x1:.2})'
                Ecuation = ctypes.create_string_buffer(ecuacion.encode());
                while(Posicion1 < Posicion2):
                    Datos[Posicion1] = BookShelf.eval(Ecuation, float(Indice[Posicion1]))
                    Posicion1 = Posicion1 + 1;
                while(Posicion2 < i):
                    Datos[Posicion2] = BookShelf.eval(Ecuation, float(Indice[Posicion2]))
                    Posicion2 = Posicion2 + 1;
                continue
            elif(Datos[i] == "--"):
                x1 = float(Indice[i-1])
                y1 = float(Datos[i - 1])
                Posicion = i;
                while(i <= (Rango-1) and Datos[i] == "--" ):
                    i = i + 1;
                if(i == Rango and Datos[Posicion - 1] != "--"):
                    x1 = float(Indice[Posicion-2])
                    y1 = float(Datos[Posicion - 2])
                    x2 = float(Indice[Posicion-1])
                    y2 = float(Datos[Posicion-1])
                    a = (y2-y1)/(x2-x1)
                    ecuacion = f'{y1:.2}'
                    ecuacion = ecuacion + f'+{a:.2}'+f'*(x-{x1:.2})'
                    Ecuation = ctypes.create_string_buffer(ecuacion.encode());
                    while(Posicion < i):
                        Datos[Posicion] = BookShelf.eval(Ecuation, float(Indice[Posicion]))
                        Posicion = Posicion + 1;
                    continue
                x2 = float(Indice[i])
                y2 = float(Datos[i])
                a = (y2-y1)/(x2-x1)
                ecuacion = f'{y1:.2}'
                ecuacion = ecuacion + f'+{a:.2}'+f'*(x-{x1:.2})'
                Ecuation = ctypes.create_string_buffer(ecuacion.encode());
                while(Posicion < i):
                    Datos[Posicion] = BookShelf.eval(Ecuation, float(Indice[Posicion]))
                    Posicion = Posicion + 1;
                continue
            i = i + 1;
