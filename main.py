#!/usr/bin/env python3
"""
Simulador de la instrucción LDA para SIC/XE

Este programa lee dos archivos:
  - memoria.txt: cada línea contiene "Dirección Valor_cargador" (en hexadecimal)
  - banderas_dir.txt: cada línea contiene "nixbpe dirección", donde:
      • nixbpe: bits (n, i, x, b, p, e) que determinan el modo de direccionamiento
      • dirección: campo de dirección de la instrucción LDA

La salida se imprime con el formato:
   nixbpe dirección Modo Salida
"""

def cargar_memoria(nombre_archivo):
    """
    Lee el archivo de memoria y retorna un diccionario con:
      clave: dirección (entero)
      valor: contenido (entero)
    """
    memoria = {}  # Diccionario vacío
    with open(nombre_archivo, 'r') as f:
        for linTA in f:
            linTA = linTA.strip()
            if not linTA:
                continue
            partes = linTA.split()
            if len(partes) < 2:
                continue
            direccion_str, valor_str = partes[0], partes[1]
            direccion = int(direccion_str, 16)
            valor = int(valor_str, 16)
            memoria[direccion] = valor
    return memoria

def simular_LDA(memoria, banderas_dir_file):
    """
    Simula la ejecución de la instrucción LDA para cada línea del archivo banderas_dir.txt.
    Imprime una línea de salida con el formato:
       nixbpe dirección Modo Salida
    donde "Modo" puede ser Inmediato, Base, PC, Extendido, Indirecto o Directo.
    """
    # Valores fijos
    PC = 2              # Para direccionamiento PC-relativo
    Base = 0xA          # Registro Base, establecido a 000A (hexadecimal)
    X = 0               # Registro X (se asume 0)

        # Imprimir la cabecera de la tabla
    print("-" * 42)
    print(f"{'nixbpe':<8} {'Dirección':<10} {'Modo':<12} {'Salida':<8}")
    print("-" * 42)

    with open(banderas_dir_file, 'r') as f:
        for linTA in f:
            linTA = linTA.strip()
            if not linTA:
                continue
            partes = linTA.split()
            if len(partes) < 2:
                continue
            banderas = partes[0]      # Cadena de 6 bits: n i x b p e
            operando = partes[1]      # Campo de dirección (en hexadecimal)
            
            # Convertir el operando a entero (valor inmediato o desplazamiento)
            hex_decimal_op = int(operando, 16)
            
            # Extraer cada bit (orden: n, i, x, b, p, e)
            n = banderas[0]
            i = banderas[1]
            x_flag = banderas[2]  # No se utiliza en este ejercicio (X = 0)
            b_flag = banderas[3]
            p_flag = banderas[4]
            e_flag = banderas[5]
            
            # Inicializamos TA (dirección efectiva) y determinamos el modo
            if n == '0' and i == '1':
                # Modo inmediato: se usa el valor inmediato directamente
                modo = "Inmediato"
                TA = None  # No se utiliza TA en inmediato
                A = hex_decimal_op
            elif n == '1' and i == '0':
                # Modo indirecto: se obtiene un puntero en memoria[TA] y luego se carga el valor en memoria[puntero]
                modo = "Indirecto"
                TA = hex_decimal_op
                puntero = memoria.get(TA, 0)
                A = memoria.get(puntero, 0)
            else:
                # Para los demás casos se calcula TA según otros bits
                if e_flag == '1':
                    modo = "Extendido"
                    TA = hex_decimal_op
                elif p_flag == '1':
                    modo = "PC"
                    TA = PC + hex_decimal_op
                elif b_flag == '1':
                    modo = "Base"
                    TA = Base + hex_decimal_op
                else:
                    modo = "Directo"
                    TA = hex_decimal_op
                
                # Aplicar el modo indexado si x_flag es '1'
                if x_flag == '1':
                    TA = TA + X

                A = memoria.get(TA, 0)
            
            # Imprimir el resultado con el formato: nixbpe dirección modo salida
            print(f"{banderas:<8} {operando:<10} {modo:<12} {A:04X}")

def main():
    memoria = cargar_memoria("memoria.txt")
    simular_LDA(memoria, "banderas_dir.txt")

if __name__ == "__main__":
    main()
