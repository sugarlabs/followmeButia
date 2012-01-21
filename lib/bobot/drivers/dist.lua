local device = _G

local char00=string.char(0x00)

api={}
api.getDistancia = {}
api.getDistancia.parameters = {} -- -- no input parameters
api.getDistancia.returns = {[1]={rname="par1", rtype="int"}} 
api.getDistancia.call = function ()
	device:send(char00) -- codigo de operacion 0
	local sen_anl_response = device:read(3) 
	local raw_val	
	if not sen_anl_response or string.byte(sen_anl_response or "00000000", 2) == nil or string.byte(sen_anl_response or "00000000", 3) == nil
	then 
		raw_val = "nil value"
	else
		raw_val = string.byte(sen_anl_response, 2)* 256 + string.byte(sen_anl_response, 3) 
		raw_val = 1024 - raw_val

	end	
	return raw_val  
	
end
