#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Butia 2010, 2011
# This is a part of program to use with the robot Butia.
# Butia is a project from Facultad de Ingenieria - Uruguay
# Facultad de Ingenieria web site: <http://www.fing.edu.uy/>
# Butia project web site: <http://www.fing.edu.uy/inco/proyectos/butia/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# version 2_0 //agrega funcionalidades para manejar nuevos drivers 

import socket


ADDRESS = "localhost"
PUERTO  = 2009
	
	
class robot:
	cliente = None
	   
	def __init__(self):
		#print "creando clase butiaAPI"
		# abrir la conexion en socket
		try:
			self.cliente = socket.socket()
			self.cliente.connect((ADDRESS, PUERTO))  
		except:
			print "Connection error..."
			#return -1
		
	def cerrar(self):
		#print "cerrando comunicacion..."	
		# cerrar comunicacion con servidor lubot
		try:
			self.cliente.close() # FIXME verificar q esta operacion no da error
		except:
			return -1	
		
	#Operaciones solicitadas al sistema modulo principal
	
	#listar modulos: devuelve la lista de los modulos disponibles en el firmware de la placa
	def listarModulos(self):
		ret = -1
		try:
			#print "Listar modulos"
			msg = "LIST\n"
			#print msg
			self.cliente.send(msg)  # FIXME -- controlar que no de error el socket
			ret = self.cliente.recv(256) 			
		except:	
			print "Error listing modules"
		finally:
			return ret	
		
	def abrirLback(self):
		ret = -1
		try:
			msg = "OPEN lback\n"
			#print msg
			self.cliente.send(msg)  # FIXME -- controlar que no de error el socket
			ret = self.cliente.recv(256) 
			return ret	
		except:
			return -1	
			
		
	#loopBack: envia un mensaje a la placa y espera recibir exactamente lo que fue enviado
	def loopBack(self, data):
		ret = -1
		try:
			#print "Loop back"
			msg = "CALL lback send " + data  + "\n"
			#print msg
			self.cliente.send(msg) # FIXME -- controlar que no de error el socket
			ret = self.cliente.recv(256) # ver q hacer con esta respuesta
			self.cliente.send("CALL lback read\n")# FIXME -- controlar que no de error el socket
			ret = self.cliente.recv(256) 
		except:
			print "Operation error"
		finally:	
			return ret				
	 
	#Operaciones solicidatas al driver motores.lua	
	 
	def abrirMotores(self):
		ret = -1
		try:
			#print "Abrir modulo"
			msg = "OPEN motores\n"
			#print msg
			self.cliente.send(msg)  # FIXME -- controlar que no de error el socket
			ret = self.cliente.recv(256) 
		except:
			print "Operation error"
		finally:	
			return ret	
		
	def setVelocidadMotores(self, sentidoIzq = "0", velIzq = "0", sentidoDer = "0", velDer = "0"):
		ret = -1
		try:
			#print "setVelocidadMotores"
			msg = "CALL motores setvel2mtr " + sentidoIzq + " " + velIzq + " " + sentidoDer + " " + velDer + "\n"
			#print msg
			self.cliente.send(msg)
			ret = self.cliente.recv(256)
		except:
			print "Operation error"
		finally:	
			return ret
	 
	def setVelMotor(self, idMotor = "0", sentido = "0", vel = "0"):
		ret = -1
		try:
			#print "setVelMotor"
			msg = "CALL motores setvelmtr " + idMotor + " " + sentido + " " + vel + "\n"
			#print msg
			self.cliente.send(msg)
			ret = self.cliente.recv(256)
		except:
			print "Operation error"
		finally:	
			return ret
	 
	
	#Operaciones solicitadas al driver de los sensores
	def abrirSensor(self):
		ret = -1
		try:
			#print "Abrir modulo"
			msg = "OPEN sensor\n"
			#print msg
			self.cliente.send(msg)  # FIXME -- controlar que no de error el socket
			ret = self.cliente.recv(256) 
		except:
			print "Operation error"
		finally:	
			return ret
		
	def getValSenAnalog(self, pinAnalog = "0"):
		ret = -1
		try:
			#print "getValSenAnalog"
			msg = "CALL sensor senanl " + pinAnalog + "\n"
			#print msg
			self.cliente.send(msg)
			ret = self.cliente.recv(256) 
		except:
			print "Operation error"
		finally:	
			return ret
		
	def getValSenDigital(self, pinDig = "0"):
		ret = -1
		try:
			#print "getValSenDig"
			msg = "CALL sensor sendig " + pinDig + "\n" 
			#print msg
			self.cliente.send(msg)
			ret = self.cliente.recv(256) 
		except:
			print "Operation error"
		finally:	
			return ret
		
	#Operaciones solicitadas al modulo de la placa, driver butia.lua
	#siempre de debe abrir el modulo antes de solicitar cualquier otra operacion
	def abrirButia(self):
		ret = -1
		try:
			#print "Abrir modulo"
			msg = "OPEN butia\n"
			#print msg
			self.cliente.send(msg)  
			ret = self.cliente.recv(256) 
		except:
			print "Operation error"
		finally:
			return ret
		
	def ping(self):
		try:
			#print "ping"
			msg = "CALL placa ping"
			#print msg
			self.cliente.send(msg)
		except:
			print "Operation error"
			return -1
		
	# esta operacion nos devuelve la carga aproximada del pack de pilas del robot con un error de 1 volt.	
	def getCargaBateria(self):
		ret = -1
		try:
			#print "getCargaBateria"
			msg = "CALL butia get_volt\n"
			#print msg
			self.cliente.send(msg)
			ret = self.cliente.recv(256)
		except:
			print "Operation error"
		finally:
			return ret
	 
	#esta operacion nos devuelve la version del firmware de la placa con el que estamos trabajando 
	def getVersion(self):
		ret = -1
		try:
			#print "getVersion"
			msg = "CALL butia read_ver\n"
			#print msg
			self.cliente.send(msg)
			ret = self.cliente.recv(256)
		except:
			print "Operation error"
		finally:
			return ret
		
	def setVelocidad3(self,velIzq = 0, velDer = 0):
		try:
			#print "setVelocidad en ambas ruedas" 
			msg = "CALL placa setVelocidad " +  str(velIzq) + " " + str(velDer)
			#print msg
			self.cliente.send(msg)
		except:
			print "Operation error"
			return -1
		
	def setPosicion(self, idMotor = 0, angulo = 0):
		try:
			#print "setPosicion"
			msg = "CALL placa setPosicion "  + str(idMotor) + " " + str(angulo)
			#print msg
			self.cliente.send(msg)
		except:
			print "Operation error"	
			return -1

    #Operaciones solicitadas al driver boton4
	def abrirBoton4(self):
		ret = -1
		try:
			#print "Abrir modulo"
			msg = "OPEN boton4\n"
			#print msg
			self.cliente.send(msg)  # FIXME -- controlar que no de error el socket
			ret = self.cliente.recv(256) 
		except:
			print "Operation error"
		finally:			
			return ret
		
	def getBoton(self):
		ret = -1
		try:
			#print "getValSenDig"
			msg = "CALL boton getBoton\n"
			#print msg
			self.cliente.send(msg)
			ret = self.cliente.recv(256) 
		except:
			print "Operation error"
		finally:	
			return ret