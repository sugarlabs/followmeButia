module(..., package.seeall);

--local socket=require("socket")

local bobot_baseboard = require("bobot_baseboard")

local my_path = debug.getinfo(1, "S").source:match[[^@?(.*[\/])[^\/]-$]]
assert(package.loadlib(my_path .. "/lua_serialcomm.so","luaopen_serialcomm"))()

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
    local tty=tty_t[1]
    print ("cs:", tty)
    if not tty then
        return 0,"no ttyUSB found"
    end

--    tty="/dev/ttyUSB0"

	serial_handler, err = serialcomm.init(tty, 115200)
    if not serial_handler then
        return 0, err
    end

	local bb = bobot_baseboard.BaseBoard:new({idBoard=tty, comms=comms_serial})
	baseboards[tty]=bb

	return 1
end

