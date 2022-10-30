#-------------------------------------------------------------------------------
# Name:         clsInyector
# Purpose:      clase que realiza la carga de datos a una bd
#
# Author:       Rene Ulloa
#
# Created:      19/10/2011
# Copyright:    (c) Rene Ulloa 2011
# Licence:      GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys
import os
import shutil
import datetime
import time

from clsUtilidades import clsUtil

class clsInyector:
    __companias = {}
    __con = ""
    __host = ""
    __user = ""
    __pass = ""
    __bd = ""

    __dir_procesar = ""
    __dir_procesados = ""
    __dir_error = ""

    #__cant_datos_arch = ""
    #__cant_num_cel = ""
    #__monto_min_recarga = ""
    #__monto_max_recarga = ""

    __fecha_format = ""
    __fecha_com_format = ""

    __cant_a_inyectar = 0
    __cant_inyectadas = 0
    __cant_err = 0

    def __init__(self,dir_cfg):
        self.__U = clsUtil()
        self.__DatosCFG(dir_cfg)

        fecha = datetime.date.today()
        fecha_com = datetime.datetime.today()

        self.__con = self.__U.coneccion(self.__host, self.__user, self.__pass, self.__bd)
        self.__ObtenerCia()
        self.__fecha_format =  fecha.strftime("%Y%m%d")
        self.__fecha_com_format = fecha_com.strftime("%Y%m%d%H%M%S")

        if not os.path.isdir(self.__dir_procesar):
            os.mkdir(self.__dir_procesar)

        if not os.path.isdir(self.__dir_procesados):
            os.mkdir(self.__dir_procesados)

        if not os.path.isdir(self.__dir_error):
            os.mkdir(self.__dir_error)

    def ArchivosaProcesar(self):
        arch=[]
        archs = os.listdir(self.__dir_procesar)

        for f in archs:
            if os.path.isfile(os.path.join(self.__dir_procesar,f)):
                if os.path.splitext(f)[1] == ".txt":
                    arch.append(f)
        return arch

    def LeeArchivos(self,archivos):
        for a in archivos:
            print "procesando ",os.path.splitext(a)[0],"\n"

            nuevo_arch = self.__CopiaArchProc(a)
            f = open(os.path.join(self.__dir_procesados,nuevo_arch))

            for lineas in f.readlines():
                try:
                    self.__cant_a_inyectar += 1
                    d = lineas.split(";")

                    if len(d) == int( self.__cant_datos_arch):
                        resp = self.__Inyector(d[0],d[1],d[2],d[3],d[4],d[5])
                        if resp == "":
                            self.__cant_inyectadas += 1
                        else:
                            self.__GuardaError(nuevo_arch,lineas,resp)
                    else:
                        self.__GuardaError(nuevo_arch,lineas,"formato de datos no valido")
                except:
                    #print sys.exc_info()[1]
                    self.__GuardaError(nuevo_arch,lineas, sys.exc_info()[1])

            f.close()
            self.__DatosInyeccion()
            self.__LimpiaDatosInyeccion()
            print "\n\n"

        print "Inyeccion Terminada\n\n"

    def __Inyector(self,cod_empresa,cia,nro,monto,sucursal,fecha_arch):
        fecha = ""
        hora = ""

        if fecha_arch.find(" ") > 0:
            fecha = fecha_arch.split(" ")[0]
            hora = fecha_arch.split(" ")[1]
        else:
            fecha = fecha_arch

        if fecha.find("-") > 0:
            fecha = fecha.replace("-","")
        elif fecha.find("/") > 0:
            fecha = fecha.replace("/","")

        if hora == "":
            hora = "000000"
        else:
            if hora.find(":") > 0:
                hora = hora.replace(":","")

        resp = self.__ValidaDatos(cod_empresa, cia, nro, monto, sucursal, fecha, hora)

        if resp == "":
            if not self.__GuardaDatos(cia, cod_empresa, nro, monto, sucursal, fecha, hora):
                resp = "Erro al guardar los datos"

        return resp


    def __ValidaDatos(self,cod_empresa,cia,nro,monto,sucursal,fecha, hora):
        msg_err = ""

        if cod_empresa == "":
            msg_err += "Codigo de la empresa es obligatorio - "

        if cia == "":
            msg_err += "Compania de telefono es obligatorio - "
        elif not self.__companias.has_key(cia):
            msg_err += "Compania de telefono no existe - "

        if nro == "":
            msg_err += "Numero de telefono es obligatorio - "
        elif not nro.isdigit() :
            msg_err += "Numero de telefono debe ser numerico - "
        elif len(nro) <> int(self.__cant_num_cel):
            msg_err += "Numero de telefono invalido - "
        elif not self.__ExisteNro(nro):
            msg_err += "Numero de telefono no esta registrado - "
        elif not self.__ExisteNroCia(cia, nro):
            msg_err += "Numero de telefono no pertenece a la compania - "

        if monto == "":
            msg_err += "Monto es obligatorio - "
        elif not monto.isdigit():
            msg_err += "Monto debe ser numerico - "
        elif monto < self.__monto_min_recarga:
            msg_err += "El monto no debe ser menor a (" + self.__monto_min_recarga + ") - "
        elif monto > self.__monto_max_recarga:
            msg_err += "El monto excede la recarga maxima (" + self.__monto_max_recarga + ") - "

        if sucursal == "":
            msg_err += "Sucursal es obligatoria - "
        elif not self.__ExisteSucursal(sucursal):
            msg_err += "Sucursal no esta registrada - "
        elif not self.__ExisteSucursalCia(cia, sucursal):
            msg_err += "Sucursal no pertenece a la compania - "

        if not self.__U.ValidaFecha(fecha.replace("\n","")):
            msg_err += "Fecha invalida - "

        if not self.__U.ValidaHora(hora.replace("\n","")):
            msg_err += "Hora invalida - "

        if msg_err <> "":
            msg_err = msg_err[0:len(msg_err)-3]

        return msg_err

    def __ExisteNro(self, nro):
        con_cur = self.__con.cursor()

        sql_query = "SELECT count(id_telefono) FROM telefono WHERE numero = '" + nro + "' AND vigente = 1;"
        con_cur.execute(sql_query)
        reg = con_cur.fetchone()

        if reg <> None:
            if reg[0] > 0:
                return True
            else:
                return False
        else:
            return False

    def __ExisteNroCia(self, cia, nro):
        con_cur = self.__con.cursor()

        if self.__companias.has_key(cia):
            idCia = self.__companias[cia]

            sql_query = "SELECT count(id_telefono) FROM telefono WHERE numero = '" + nro + "' AND id_cia = " + str(idCia) + " AND vigente = 1;"
            con_cur.execute(sql_query)
            reg = con_cur.fetchone()

        if reg <> None:
            if reg[0] > 0:
                return True
            else:
                return False
        else:
            return False

    def __ExisteSucursal(self, suc):
        con_cur = self.__con.cursor()

        sql_query = "SELECT count(id_sucursal) FROM sucursal WHERE upper(nombre) = upper('" + suc + "') AND vigente = 1;"
        con_cur.execute(sql_query)
        reg = con_cur.fetchone()

        if reg <> None:
            if reg[0] > 0:
                return True
            else:
                return False
        else:
            return False

    def __ExisteSucursalCia(self, cia, suc):
        con_cur = self.__con.cursor()

        if self.__companias.has_key(cia):
            idCia = self.__companias[cia]

            sql_query = "SELECT count(id_sucursal) FROM sucursal WHERE upper(nombre) = upper('" + suc + "') AND id_cia = " + str(idCia) + " AND vigente = 1;"
            con_cur.execute(sql_query)
            reg = con_cur.fetchone()

        if reg <> None:
            if reg[0] > 0:
                return True
            else:
                return False
        else:
            return False

    def __GuardaDatos(self, cia, cod_cia, nro, monto, sucursal, fecha, hora):
        id_telefono = 0
        id_recarga = 0
        id_sucursal = 0

        con_cur = self.__con.cursor()

        con_cur.execute("SELECT id_telefono FROM telefono WHERE numero = '" + nro + "';")
        reg = con_cur.fetchone()

        if reg <> None:
            id_telefono = reg[0]

        if id_telefono <> 0:
            sql_query = "INSERT INTO recargas("
            sql_query += "id_cia"
            sql_query += ",cod_cia"
            sql_query += ",id_telefono"
            sql_query += ",monto"
            sql_query += ",fecha_recarga"
            sql_query += ",hora_recarga"
            sql_query += ")VALUES("
            sql_query += str(self.__companias[cia])
            sql_query += ",'" + str(cod_cia) + "'"
            sql_query += "," + str(id_telefono) + ""
            sql_query += "," + monto
            sql_query += ",'" + fecha + "'"
            sql_query += ",'" + hora + "'"
            sql_query += ")"

            if con_cur.execute(sql_query) == 1:
                #self.__con.commit()
                error = False
            else:
                error = True
        else:
            error = True

        if not error:
            con_cur.execute("select last_insert_id();")
            reg = con_cur.fetchone()

            if reg <> None:
                id_recarga = reg[0]

        if id_recarga <> 0:
            con_cur.execute("SELECT id_sucursal FROM sucursal WHERE upper(nombre) = upper('" + sucursal + "');")
            reg = con_cur.fetchone()

            if reg <> None:
                id_sucursal = reg[0]
        else:
            error = True

        if id_sucursal <> 0:
            sql_query = "INSERT INTO suc_reg(id_recarga, id_sucursal)VALUES(" + str(id_recarga) + "," + str(id_sucursal) + ");"

            if con_cur.execute(sql_query) == 1:
                #self.__con.commit()
                error = False
            else:
                error = True
        else:
            error = True

        if error:
            self.__con.rollback()
            return False
        else:
            self.__con.commit()
            return True

    def __DatosInyeccion(self):
        print "Detalle Inyeccion:\n"
        print "cantidad de datos a inyectar: ", self.__cant_a_inyectar
        print "\ncantidad de datos inyectados: ", self.__cant_inyectadas
        print "\ncantidad de datos erroneos: ", self.__cant_err

    def __LimpiaDatosInyeccion(self):
        self.__cant_a_inyectar = 0
        self.__cant_inyectadas = 0
        self.__cant_err = 0

    def __CopiaArchProc(self,arch):
        aux = True
        proc = 1

        while aux == True:
            if proc < 10:
                proceso = "0" + str(proc)
            else:
                proceso = str(proc)

            nuevo_nombre = os.path.splitext(arch)[0] + "_proc" + proceso + os.path.splitext(arch)[1]

            if os.path.isfile(os.path.join(self.__dir_procesados,nuevo_nombre)) == True:
                proc += 1
            else:
                aux = False

        shutil.copy2(os.path.join(self.__dir_procesar,arch),os.path.join(self.__dir_procesados,nuevo_nombre))
        os.remove(os.path.join(self.__dir_procesar,arch))

        return nuevo_nombre

    def __GuardaError(self,arch,linea,error):
        f = open(os.path.join(self.__dir_error,"error_" + os.path.splitext(arch)[0] + self.__fecha_com_format + ".txt"),"a")
        datos = linea.replace("\n","") + " | " + str(error) + "\n"
        f.write(datos)
        f.close()
        self.__cant_err += 1

    def __ObtenerCia(self):
        con_cur = self.__con.cursor()
        sql_query = "SELECT id_cia, nombre FROM cia WHERE vigente = 1;"

        con_cur.execute(sql_query)
        resultados = con_cur.fetchall()

        for registro in resultados:
            self.__companias[registro[1].lower()] = registro[0]

    def __DatosCFG(self,dir_cfg):
        datos=[]
        datos = self.__U.leerCFG(dir_cfg)

        for dat in datos:
            d = dat.split("|")

            if d[0] == "host":
                self.__host = d[1]

            if d[0] == "user":
                self.__user = d[1]

            if d[0] == "pass":
                self.__pass = d[1]


            if d[0] == "bd":
                self.__bd = d[1]

            if d[0] == "cfg_dir_procesar":
                self.__dir_procesar = d[1]

            if d[0] == "cfg_dir_procesados":
                self.__dir_procesados = d[1]

            if d[0] == "cfg_dir_error":
                self.__dir_error = d[1]

            if d[0] == "cant_datos_arch":
                self.__cant_datos_arch = d[1]

            if d[0] == "cant_num_cel":
                self.__cant_num_cel = d[1]

            if d[0] == "monto_min_recarga":
                self.__monto_min_recarga = d[1]

            if d[0] == "monto_max_recarga":
                self.__monto_max_recarga = d[1]