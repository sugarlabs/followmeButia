# ButiaAPI
# Copyright 2009-2010 Mina @ Facultad de Ingenieria UDELAR
#
# Implementa una capa de abstraccion para la comunicacion con el bobot-server
# version 3_0 //reorganiza el codigo pa mas legible y menos codigo repetido
# version 2_0 //agrega funcionalidades para manejar nuevos drivers 
#
# This program is free software.....
# TODO Poner la licencia que corresponde
# 

import socket
import string
import math 


	
class robot:
	cliente = None
	fcliente = None

	#Init de la clase robot
	def __init__(self, address = "localhost" , port = 2009):
		self.reconnect(address, port)

	# Connecta o Reconnecta al bobot en address:port
	def reconnect(self, address, port):
		self.cerrar()
		try:
			self.cliente = socket.socket()
			self.cliente.connect((address, port))  
			self.fcliente = self.cliente.makefile()
			msg = "INIT\n"
			self.cliente.send(msg) #bobot server instance is running, but we have to check for new or remove hardware
			self.fcliente.readline()
		except:
			return -1
		return 0


	# Cierra la comunicacion con servidor lubot
	def cerrar(self):
		#print "cerrando comunicacion..."	
		try:
			if self.fcliente != None:
				self.fcliente.close()
				self.fcliente = None
			if self.cliente != None:
				self.cliente.close()
				self.cliente = None
		except:
			return -1
		return 0

	#######################################################################
	### Operaciones solicitadas al sistema modulo principal
	#######################################################################

	#listar modulos: devuelve la lista de los modulos disponibles en el firmware de la placa
	def listarModulos(self):
		ret = -1
		msg = "LIST\n"
		try:
			self.cliente.send(msg)		# FIXME -- controlar que no de error el socket -- Guille: No esta controlado con el "try"?
			ret = self.fcliente.readline()
		except:	
			return -1
		ret = ret[:len(ret) -1]		# le borro el \n
		return ret
	

	#abrirModulo: apertura de modulos, habre el modulo "moduloname"
	def abrirModulo(self, moduloname):
		ret = -1
		msg = "OPEN " + moduloname  + "\n"
		try:
			self.cliente.send(msg)  # FIXME -- controlar que no de error el socket
			ret = self.fcliente.readline()
		except:
			return -1
		ret = ret[:len(ret) -1]		# le borro el \n
		return ret


	#llamarModulo: Operacion de llamada de una funcion de un modulo (CALL)
	def llamarModulo(self, modulename, function , params = ""):
		ret = -1
		msg = "CALL " + modulename + " " + function
		if params != "" :
			msg += " " + params
		msg += "\n"
		try:
			self.cliente.send(msg) # FIXME -- controlar que no de error el socket
			ret = self.fcliente.readline()
		except:
			return -1
		ret = ret[:len(ret) -1]		# le borro el \n
		return ret



	#######################################################################
	### Funciones utiles
	####################################################################### 


	#retorna si esta presente el modulo
	def isPresent(self, modulename):
		ret = self.listarModulos()
		# TODO : habria que hacer un buffer para guardar el listademodulos
		# ya que las subsecuentes llamadas a esta funcion para chequear por
		# muchos modulos seria ineficiente.
		if ret == -1 :
			return False
		listamodulos = string.split(ret,',')
		for modulo in listamodulos:
			if modulo == modulename:
				return True
		return False

	#loopBack: modulo de ayuda presente en el butia (open)
	def abrirLback(self):
		return self.abrirModulo("lback")

	#loopBack: envia un mensaje a la placa y espera recibir exactamente lo que fue enviado
	def loopBack(self, data):
		ret = self.llamarModulo("lback", "send", data)
		if ret == -1 :
			return -1
		return self.llamarModulo("lback", "read" )


	#######################################################
	### Operaciones solicidatas al driver motores.lua	
	######################################################

	def abrirMotores(self):
		return self.abrirModulo("motores")

	def setVelocidadMotores(self, sentidoIzq = "0", velIzq = "0", sentidoDer = "0", velDer = "0"):
		msg = sentidoIzq + " " + velIzq + " " + sentidoDer + " " + velDer
		return self.llamarModulo("motores", "setvel2mtr", msg )
	 
	def setVelMotor(self, idMotor = "0", sentido = "0", vel = "0"):
		msg = idMotor + " " + sentido + " " + vel
		return self.llamarModulo("motores", "setvelmtr", msg )

	
	#### Operaciones solicitadas al driver de los sensores

	def abrirSensor(self):
		return self.abrirModulo("sensor")

	def getValSenAnalog(self, pinAnalog = "0"):
		return self.llamarModulo("sensor", "senanl", pinAnalog )

	def getValSenDigital(self, pinDig = "0"):
		return self.llamarModulo("sensor", "sendig", pinDig )

		
	#### Operaciones solicitadas al modulo de la placa, driver butia.lua

	def abrirButia(self):
		return self.abrirModulo("butia")
		
	def ping(self):
		return self.llamarModulo("placa", "ping" )

		
	# esta operacion nos devuelve la carga aproximada del pack de pilas del robot con un error de 1 volt.	
	def getCargaBateria(self):
		return self.llamarModulo("butia", "get_volt" )
	 
	#esta operacion nos devuelve la version del firmware de la placa con el que estamos trabajando 
	def getVersion(self):
		return self.llamarModulo("butia", "read_ver" )
		
	def setVelocidad3(self,velIzq = 0, velDer = 0):
		msg = str(velIzq) + " " + str(velDer)
		return self.llamarModulo("placa", "setVelocidad" , msg )

	def setPosicion(self, idMotor = 0, angulo = 0):
		msg = str(idMotor) + " " + str(angulo)
		return self.llamarModulo("placa", "setPosicion" , msg )


	#### Operaciones solicitadas al driver boton4

	def abrirBoton(self):
		return self.abrirModulo("boton")
		
	def getBoton(self):
		return self.llamarModulo("boton", "getBoton" )
	
	def getLuzAmbiente(self):
		return self.llamarModulo("luz", "getLuz" )

	def getDistancia(self):
		return self.llamarModulo("dist", "getDistancia" )
	
	def getEscalaGris(self):
		return self.llamarModulo("grises", "getLevel" )

	def getTemperature(self):
		return self.llamarModulo("temp", "getTemp" )

	def getVibration(self):
		return self.llamarModulo("vibra", "getVibra" )

	def getTilt(self):
		return self.llamarModulo("tilt", "getTilt" )

	def getContactoCapacitivo(self):
		return self.llamarModulo("capaci", "getCap" )

	def getInduccionMagnetica(self):
		return self.llamarModulo("magnet", "getCampo" )

	def setLed(self, nivel = 255):
		return self.llamarModulo("led", "setLight" , str(math.trunc(nivel)) )


