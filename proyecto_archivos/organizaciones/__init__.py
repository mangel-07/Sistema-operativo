"""Organizaciones de archivo disponibles."""
from organizaciones.serial import ArchivoSerial
from organizaciones.secuencial import ArchivoSecuencial
from organizaciones.indexado import ArchivoIndexado
from organizaciones.hash_directo import ArchivoHash

ORGS = {c.nombre: c for c in (ArchivoSerial, ArchivoSecuencial, ArchivoIndexado, ArchivoHash)}
