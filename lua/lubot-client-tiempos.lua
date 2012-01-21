#!/usr/bin/lua

local socket = require("socket")

-- Convierte un caracter hexadecimal a su valor numérico.
function charToByte(c_valua)

    if (type(c_valua) == "string") then
        c_valua = string.byte(c_valua)
    end

    local value = 0
    if (string.byte("0") <= c_valua and c_valua <= string.byte("9")) then
        value = c_valua - string.byte("0")
    else
        if (string.byte("A") <= c_valua and c_valua <= string.byte("F")) then
            value = c_valua - string.byte("A") + 10
        else
            print("charToByte("..c_valua..") ERROR: me pasaste verdura")
        end
    end
    return value
end

local function stringToBytes(data)
    local data_hex = ""
    for i=1, (string.len(data) / 2) do
        local value_h = string.byte(data,i*2-1)
        local value_l = string.byte(data,i*2)
        local value = charToByte(value_h) * 0x10 + charToByte(value_l)
        data_hex = data_hex .. string.char(value)
    end
    return data_hex
end

--local host, port = "192.168.10.1", 2009
local host, port = "localhost", 2009

local client = assert(socket.connect(host, port))
client:settimeout(nil) --blocking
--client:settimeout(1)

local function send(s)
	--print("sending", s)
	client:send(s.."\n")
	local ret = client:receive()
	--print("ret:", ret)
	return ret
end

send("LIST")
socket.sleep(1)
send("OPEN lback")
socket.sleep(1)
---[[
while true do
	--print ('\n\n\nTiming...')

	local tini=socket.gettime()
    local data="ping!".. socket.gettime()
	send("CALL lback send ".. data)
	--print ('#################### call send', socket.gettime()-tini)
	--socket.sleep(1)
	--local tini=socket.gettime()
	local ret=send("CALL lback read")
    if ret~=data then print ("!", string.byte(ret,1,#ret)) end
	--print ('#################### call read', socket.gettime()-tini)
	--socket.sleep(1)

end
--]]

