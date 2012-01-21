module(..., package.seeall);

--local socket=require("socket")

local bobot_baseboard = require("bobot_baseboard")

local my_path = debug.getinfo(1, "S").source:match[[^@?(.*[\/])[^\/]-$]]
assert(package.loadlib(my_path .. "lua_serialcomm.so","luaopen_serialcomm"))()

local serial_handler 

--executes s on the console and returns the output
local function run_shell (s) 
	local f = io.popen(s) -- runs command
	local l = f:read("*a") -- read output of command
	f:close()
	return l
end

local function split_words(s)
	words={}
	for p in string.gmatch(s, "%S+") do
		words[#words+1]=p
	end
	return words
end


function send(endpoint, data, timeout)
	--parameters sanity check
	assert(type(serial_handler)=="number")
	--assert(type(endpoint)=="number")
	assert(type(data)=="string")
	assert(type(timeout)=="number")

	--local tini=socket.gettime()
	local ret =  serialcomm.send_msg(serial_handler, data)
	--print ('%%%%%%%%%%%%%%%% comms serial send',socket.gettime()-tini)
	return ret
end

function read(endpoint, len, timeout)
	--parameters sanity check
	assert(type(serial_handler)=="number")
	--assert(type(endpoint)=="number")
      --assert(type(len)=="number")
	--assert(type(timeout)=="number")

	return serialcomm.read_msg(serial_handler, len, timeout)
end
    

function init(baseboards)
	--parameters sanity check
	assert(type(baseboards)=="table")

	--FIXME leer ttyusbs...
	local tty_s=run_shell("ls /dev/ttyUSB*")
	local tty_t=split_words(tty_s)  
	local tty
	local err
	if (#tty_t == 0) then
		return 0,"no ttyUSB found"
	end

	--    tty="/dev/ttyUSB0"
	--for i=1, #tty_t do 
	for _, ttyI in ipairs(tty_t) do
		print ("Trying to connect to", ttyI)
		serial_handler, err = serialcomm.init(ttyI, 115200) 
		if serial_handler then 
			tty=ttyI
			break
		else
			print("Error connecting:", err)
		end
	end
	if not serial_handler then
		print("cs:", "no ttyUSB could be open")
		return 0, err
	end
	print ("cs:", tty)
	local bb = bobot_baseboard.BaseBoard:new({idBoard=tty, comms=comms_serial})
	baseboards[tty]=bb

	return 1
end

