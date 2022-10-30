#-------------------------------------------------------------------------------
# Name:        clsUtilidades
# Purpose:     utiliddades para cualquier programa
#
# Author:      Rene Ulloa
#
# Created:     30/09/2011
# Copyright:   (c) Rene Ulloa 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import MySQLdb

class clsUtil:
    def leerCFG(self, dir_cfg):
        datos=[]

        f = open(dir_cfg)

        for lineas in f.readlines():
            if lineas.find("#") < 0:
                linea = lineas.split("=")
                datos.append(linea[0].strip() + "|" + linea[1].strip())

        return datos

    def annoBisiesto(self,anio):
        if anio % 4 == 0 and anio % 100 != 0 or anio % 400 == 0:
            return True
        else:
            return False

    def ValidaFecha(self,fecha):
        if fecha == "":
            return False

        if len(fecha) <> 8:
            return False
        else:
            dia = fecha[0:2]
            mes = fecha[2:4]
            anno = fecha[4:8]

        if not fecha.isdigit():
            return False

        if anno < 1900:
            return False

        if mes < 1 and mes > 12:
            return False

        if mes == 2:
            if annoBisiesto(anno):
                if mes < 0 and mes > 29:
                    return False
            else:
                if dia < 0 and dia > 28:
                    return False
        elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
            if dia < 0 and dia > 30:
                return False
        else:
            if dia < 0 and dia > 31:
                return False

        return True

    def ValidaHora(self,hora):
        if hora == "":
            return False

        if len(hora) <> 6:
            return False
        else:
            hor = hora[0:2]
            min = hora[2:4]
            seg = hora[4:6]

        if not hora.isdigit():
            return False

        if hor < 0 and hor > 23:
            return False

        if min < 0 and min > 59:
            return False

        if seg < 0 and seg > 59:
            return False

        return True

    def coneccion(self, p_host, p_user, p_pass, p_db):
        conn = MySQLdb.connect(host=p_host,user=p_user, passwd=p_pass,db=p_db)

        return conn