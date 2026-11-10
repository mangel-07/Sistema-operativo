Simulador de organizacion de archivos (CRUD)

Instalar:   pip install -r requirements.txt   (en Fedora tambien: sudo dnf install python3-tkinter y Arch Linux: sudo pacman -S tk)
EJECUTAR:   python main.py        <-- este es el unico archivo que se ejecuta

modelo/          registro.py (campos, longitudes, bytes) y almacenamiento.py (archivo binario fijo, busqueda binaria)
organizaciones/  base.py (clase base CRUD), serial.py, secuencial.py, indexado.py, hash_directo.py
vista/           app.py (interfaz grafica)
datos/           se crea solo; aqui quedan los archivos .dat / .idx
