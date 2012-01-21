local device = _G

api={}
api.getLevel = {}
api.getLevel.parameters = {} -- -- no input parameters
api.getLevel.returns = {[1]={rname="par1", rtype="int"}} 
api.getLevel.call = function ()
	device:send(string.char(0x00)) -- codigo de operacion 0
	local sen_anl_response = device:read(3) 
	local raw_val	
	if not sen_anl_response or string.byte(sen_anl_response or "00000000", 2) == nil or string.byte(sen_anl_response or "00000000", 3) == nil
	then 
		raw_val = "nil value"
	else
		raw_val = string.byte(sen_anl_response, 2)* 256 + string.byte(sen_anl_response, 3) 
	end	
	return raw_val 
	
end
