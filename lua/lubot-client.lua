#!/usr/bin/lua

local socket = require("socket")

--local host, port = "192.168.10.1", 2009
local host, port = "localhost", 2009

local client = assert(socket.connect(host, port))
client:settimeout(nil) --blocking
--client:settimeout(1)

local function send(s)
	print("sending", s)
	client:send(s.."\n")
	local ret = client:receive()
	print("ret:", ret)
	return ret
end
send("LIST")
-- send("RESET")
-- Motor SUMBOT
--send("CALL stmtr t0cfg 254 254") --quedo medio a ojardi esto, hay que estudiarlo un poco
--send("CALL stmtr speed 127 127")
--socket.sleep(5)
--send("CALL stmtr speed 100 100")
--socket.sleep(5)
--send("CALL stmtr speed 50 50")
--socket.sleep(5)
--send("CALL stmtr speed 10 10")

--[[
while true do
	local v=127
	send("CALL stmtr speed "..v.." "..v)
	socket.sleep(10)
	local v=-v
	send("CALL stmtr speed "..v.." "..v)
	socket.sleep(10)
end
--]]

socket.sleep(1)
send("OPEN lback")
socket.sleep(1)
---[[
while true do
	--print ('Timing...\n\n\n')

	local tini=socket.gettime()
	send("CALL lback send ping!".. socket.gettime())
	print ('#################### call send', socket.gettime()-tini)
	--socket.sleep(1)
	local tini=socket.gettime()
	send("CALL lback read")
	print ('#################### call read', socket.gettime()-tini)
	--socket.sleep(1)

end
--]]


--[[
while true do
	send("CALL temp get_temperature")
	--send("CALL pote get_value")
	socket.sleep(1)
end
--]]

-- Motor a interrupciones simple
--send("CALL motorin speed 6536")
--send("CALL motorin steps 05")
--send("CALL motorin on 1")

-- Motor simple
--send("CALL motor speed 1")
--send("CALL motor steps 05")
--send("CALL motor on 1")

-- Sensor de temperatura
--send("CALL temp get_temperature")
--send("CALL boot reset")
--send("CALL boot reset")
--send("RESET")
--send("CALL temp get_temperature")

