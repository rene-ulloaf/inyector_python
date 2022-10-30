#-------------------------------------------------------------------------------
# Name:         inyector
# Purpose:      Realiza la carga de archivos a una bd luego de validarlos
#
# Author:       Rene Ulloa
#
# Created:      19/10/2011
# Copyright:    (c) Rene Ulloa 2011
# Licence:      GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys

sys.path.append("./clases")
from clsInyector import clsInyector

def main():
    i = clsInyector("inyector.cfg")
    archs = i.ArchivosaProcesar()

    if(len(archs) > 0):
        print "archivos con datos a inyectar:\n"
        for a in archs:
            print "\t -" ,a

        resp = raw_input("Desea procesar los archivos [S/N]")
        if(resp == "S" or resp == "s"):
            print "Inicio Proceso\n\n"
            i.LeeArchivos(archs)
        else:
            resp = raw_input("Desea buscar nuevamente los archivos [S/N]")
            if(resp == "S" or resp == "s"):
                resp = ""
                main()
            else:
                print "Saliendo..."
    else:
        print "No existen archivos a procesar"

if __name__ == '__main__':
    main()