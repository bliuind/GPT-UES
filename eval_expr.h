/* eval_expr.c
   lee una expresión en forma de cadena y un valor de x por línea de
   comandos, luego imprime el resultado. 
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#ifndef M_PI
    #define M_PI 3.1415926535897932384
#endif
#ifndef M_E
    #define M_E 2.7182818284590452353
#endif

/* prototipos del parser */
double eval(const char *expr, double x);
static const char *ep;
static void skip_spaces(void){ while(*ep==' '||*ep=='\t') ep++; }
static double parse_expr(double x);
static double parse_term(double x);
static double parse_pow(double x);
static double parse_factor(double x);

/*definiciones de las funciones de análisis */
static double parse_expr(double x){
    /*
    expr ::= term { ('+'|'-') term }

    */
    double v = parse_term(x);
    for(;;){
        skip_spaces();
        if(*ep == '+'){ ep++; v += parse_term(x); }
        else if(*ep == '-'){ ep++; v -= parse_term(x); }
        else break;
    }
    return v;
}
static double parse_term(double x){
    /*
    term ::= pow { ('*'|'/') pow }
    */
    double v = parse_pow(x);
    for(;;){
        skip_spaces();
        if(*ep == '*'){ ep++; v *= parse_pow(x); }
        else if(*ep == '/'){ ep++; v /= parse_pow(x); }
        else break;
    }
    return v;
}
static double parse_pow(double x){
    /*
    pow ::= factor { '^' factor }
    */
    double v = parse_factor(x);
    skip_spaces();
    if(*ep == '^'){ ep++; double rhs = parse_pow(x); v = pow(v, rhs); }
    return v;
}
static double parse_factor(double x){
    /*
    factor ::= ('+'|'-') factor | number | 'x' | '(' expr ')' | constant | function
    */

    skip_spaces();
    double v = 0.0;
    if(*ep=='x' || *ep=='X'){ 
        v = x; 
        ep++; 
    }
    else if(*ep=='('){ 
        ep++; 
        v = parse_expr(x); 
        if(*ep==')') ep++; 
    }
    else if((*ep=='e' || *ep=='E') &&
            (*(ep+1)<'a' || *(ep+1)>'z') &&
            (*(ep+1)<'A' || *(ep+1)>'Z')){
        /* constant e */
        v = M_E;
        ep++;
    }
    else if((*ep=='p' || *ep=='P') &&
            (*(ep+1)=='i' || *(ep+1)=='I')){
        /* constant pi */
        v = M_PI;
        ep += 2;
    }
    else if(isalpha((unsigned char)*ep)){
        /* simple function names: exp, sin, cos, log, etc. */
        char func[16]; int i=0;
        while(isalpha((unsigned char)*ep) && i < (int)sizeof(func)-1)
            func[i++] = *ep++;
        func[i] = '\0';
        if(*ep=='('){
            ep++; /* skip '(' */
            double arg = parse_expr(x);
            if(*ep==')') ep++;
            if(strcmp(func, "exp") == 0) v = exp(arg);
            else if(strcmp(func, "sin") == 0) v = sin(arg);
            else if(strcmp(func, "cos") == 0) v = cos(arg);
            else if(strcmp(func, "tan") == 0) v = tan(arg);
            else if(strcmp(func, "asin") == 0) v = asin(arg);
            else if(strcmp(func, "acos") == 0) v = acos(arg);
            else if(strcmp(func, "atan") == 0) v = atan(arg);
            else if(strcmp(func, "sinh") == 0) v = sinh(arg);
            else if(strcmp(func, "cosh") == 0) v = cosh(arg);
            else if(strcmp(func, "tanh") == 0) v = tanh(arg);
            else if(strcmp(func, "sec") == 0) v = 1.0 / cos(arg);
            else if(strcmp(func, "csc") == 0) v = 1.0 / sin(arg);
            else if(strcmp(func, "cot") == 0) v = 1.0 / tan(arg);
            else if(strcmp(func, "log") == 0) v = log(arg);
            else if(strcmp(func, "log10") == 0) v = log10(arg);
            else if(strcmp(func, "sqrt") == 0) v = sqrt(arg);
            else if(strcmp(func, "abs") == 0) v = fabs(arg);
            else if(strcmp(func, "floor") == 0) v = floor(arg);
            else if(strcmp(func, "ceil") == 0) v = ceil(arg);
            else {
                /* unknown function, treat as zero */
                v = 0.0;
            }
        } else {
            /* unknown identifier, treat as zero */
            v = 0.0;
        }
    }
    else {
        char *end;
        v = strtod(ep, &end);
        ep = end;
    }
    skip_spaces();
    return v;
}
double eval(const char *expr, double x){
    /*
    eval ::= expr
    */
    ep = expr;
    return parse_expr(x);
}


/*

int main(int argc, char *argv[]){
    if(argc != 3){
        fprintf(stderr, "uso: %s \"<expresion>\" <x>\n", argv[0]);
        return 1;
    }
    const char *expr = argv[1];
    double x = atof(argv[2]);
    double y = eval(expr, x);
    printf("f(x) = %s\nx = %g\nresultado = %g\n", expr, x, y);
    return 0;
}
*/
