local device = _G
local RD_VERSION = string.char(0x02) -- lee la versión del firmware de la placa
local GET_VOLT = string.char(0x03) -- obtiene el voltage de la batería

api={}
api.read_ver = {}
api.read_ver.parameters = {[1]={rname="data", rtype="number"}}
api.read_ver.returns = {[1]={rname="data", rtype="string"}}
api.read_ver.call = function (data)
	local rd_ver = RD_VERSION
	device:send(rd_ver)
	local ret = device:read(2)
	local devolver = string.byte(ret , 2) --leo el segundo byte obtenido que tiene la versión (el primero tiene el opcode)
	return devolver	
end

api.get_volt = {}
api.get_volt.parameters = {} -- no se envian parámetros
api.get_volt.returns = {[1]={rname="data", rtype="string"}} --nos devuelve el voltaje de las baterías
api.get_volt.call = function ()
	local get_volt = GET_VOLT
	device:send(get_volt) --envío el código de operación
	local data_in = device:read(2) --leo 2 bytes, primero el código de operación y segundo el voltaje
	local voltaje = string.byte(data_in , 2) --leo el segundo byte obtenido que es el que tiene el voltaje
	--local resultado = string.char(math.floor(voltNum / 10),".",tonumber(volNum) % 256, " volts")	
	return voltaje
end


function bytesToString(data)
    local data_hex = ""
    for i=1, string.len(data) do
            data_hex = data_hex .. string.format('%02X', (string.byte(data, i)))
    end
    return data_hex
end

