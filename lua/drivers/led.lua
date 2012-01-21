local device = _G


api={}
api.setLight = {}
api.setLight.parameters = {[1]={rname="message", rtype="string"}} 
api.setLight.returns = {} 
api.setLight.call = function (intensidad)
	local msg = string.char(0x00) .. string.char(math.floor(intensidad)) -- entre 0 y 255
	device:send(msg)	
	local version_response = device:read() 	
end
