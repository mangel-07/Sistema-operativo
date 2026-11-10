# Simulador de reemplazo de páginas

Aplicación de escritorio en Python con CustomTkinter y arquitectura MVC para
visualizar FIFO, LRU, Óptimo, Clock y Segunda oportunidad mejorada (bits R/M).

## Instalación y ejecución

Desde esta carpeta, crea un entorno virtual, instala la dependencia y ejecuta
la aplicación:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

El sistema debe tener Tk instalado para abrir ventanas (en Arch Linux:
`sudo pacman -S tk`).

La tabla muestra una columna por referencia y una fila por marco. Las columnas
con fallos se resaltan en tono pastel; la última fila marca cada fallo y el
resumen indica el total y los tiempos en que ocurrió.

## Entradas

Escribe referencias separadas por comas, por ejemplo `7, 0, 1, 2, 0`, y el
número de marcos. Para indicar lectura o escritura, usa `R` o `W`, por ejemplo:
`2:R, 4:W, 2:R`. Si no se especifica la operación, se asume lectura.
