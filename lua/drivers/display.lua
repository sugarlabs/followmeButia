local device = _G
local RD_VERSION = string.char(0x00)
local ESCRIBIR = string.char(0x01)
local PRUEBA = string.char(0x02)
local BORRAR = string.char(0x03)
local INICIAR = string.char(0x04)
local PRENDER_BKL = string.char(0x08)
local APAGAR_BKL = string.char(0x09)
local AGENDAR_MSG = string.char(0x0A)
local ESPACIO	= string.char (0x20)

api={}
api.read_version = {}
api.read_version.parameters = {} --no parameters
api.read_version.returns = {[1]={rname="version", rtype="number"}} --one return
api.read_version.call = function ()
	local get_read_version = RD_VERSION 
	device:send(get_read_version)
	local version_response = device:read(2) 
	local raw_val = string.byte(temperature_response, 2) 
	--print("rawval, deg_temp: ", raw_val, deg_temp)
	return raw_val
end

api.escribir = {}
api.escribir.parameters = {[1]={rname="message", rtype="string"}}
api.escribir.returns = {}
api.escribir.call = function (str)
	local msg = ESCRIBIR .. str
	device:send(msg)
	device:read()
end

api.prueba = {}
api.prueba.parameters = {} --no parameters
api.prueba.returns = {} --no return
api.prueba.call = function ()
	device:send(PRUEBA)
end

api.borrar = {}
api.borrar.parameters = {} --no parameters
api.borrar.returns = {} --no return
api.borrar.call = function ()
	device:send(BORRAR)
end

api.iniciar = {}
api.iniciar.parameters = {} --no parameters
api.iniciar.returns = {} --no return
api.iniciar.call = function ()
	device:send(INICIAR)
end

api.prender_bkl = {}
api.prender_bkl.parameters = {} --no parameters
api.prender_bkl.returns = {} --no return
api.prender_bkl.call = function ()
	device:send(PRENDER_BKL)
end

api.apagar_bkl = {}
api.apagar_bkl.parameters = {} --no parameters
api.apagar_bkl.returns = {} --no return
api.apagar_bkl.call = function ()
        device:send(APAGAR_BKL)
end

api.agendar_msg = {}
api.agendar_msg.parameters = {[1]={rname="message", rtype="string"}, [2]={rname="isCiclic", rtype="numeric"}} -- first parameter is the message, second is 1 in case of a ciclic message 0 elsewere
api.agendar_msg.returns = {[1]={rname="isFull", rtype="boolean"}}  --If it is no more space in the event buffer returns true, false elsewere
api.agendar_msg.call = function (str, isCiclic)
    	device:send(AGENDAR_MSG .. string.char(32) .. string.char(1) .. string.char(isCiclic) .. str)
end
