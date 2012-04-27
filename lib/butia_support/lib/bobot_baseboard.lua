#!/usr/bin/lua

--module(..., package.seeall);

local bobot_device = require("bobot_device")
local bobot = require("bobot")

local NULL_BYTE				                    = string.char(0x00)
local DEFAULT_PACKET_SIZE    	          	    = 0x04
local GET_USER_MODULES_SIZE_COMMAND           	= string.char(0x05)
local GET_USER_MODULE_LINE_COMMAND		        = string.char(0x06)
local GET_LINES_RESPONSE_PACKET_SIZE 	        = 6
local GET_LINE_RESPONSE_PACKET_SIZE 	        = 12
local ADMIN_HANDLER_SEND_COMMAND 		        = string.char(0x00)
local ADMIN_MODULE_IN_ENDPOINT		            = 0x01
local ADMIN_MODULE_OUT_ENDPOINT        	        = 0x81
local GET_USER_MODULE_LINE_PACKET_SIZE 	        = 0x05
local CLOSEALL_BASE_BOARD_COMMAND             	= string.char(0x07) 
local CLOSEALL_BASE_BOARD_RESPONSE_PACKET_SIZE	= 5
local TIMEOUT	                                = 250 --ms
local MAX_RETRY 				                = 20

local BaseBoard = {}

--Instantiates BaseBoard object.
--Loads list of modules installed on baseboard
function BaseBoard:new(bb)
	--parameters sanity check
	assert(type(bb)=="table")
	assert(type(bb.comms)=="table")

	--OO boilerplate
   	setmetatable(bb, self)
	self.__index = self

	local retry = 0
	bb.devices = {}
	--read modules list
	local n_modules=bb:get_user_modules_size()
	while(n_modules == nil and retry < MAX_RETRY)do
		n_modules=bb:get_user_modules_size()
		bobot.debugprint("u4b:new:the module list size returned a nil value, trying to recover...")
		retry = retry+1
	end
	retry=0
	bobot.debugprint ("Reading modules:", n_modules)
	for i=1, n_modules do
		local name=bb:get_user_module_line(i)
		while(name == nil and retry < MAX_RETRY) do
			name=bb:get_user_module_line(i)
			bobot.debugprint("u4b:new:the module name returned a nil value, trying to recover...")
			retry = retry+1
		end
		if(name) then
			local d = bobot_device:new({name=name, baseboard=bb}) -- in_endpoint=0x01, out_endpoint=0x01})
			bb.devices[name]=d
		end
	end	
--bobot.debugprint ('----------------')
	bb:force_close_all()
--bobot.debugprint ('================')
	return bb
end

--Closes all modules opened on baseboard
function BaseBoard:close()
	--state sanity check
	assert(type(self.devices)=="table")

	for _,d in pairs(self.devices) do
		if type(d.handler)=="number" then
			bobot.debugprint ("closing", d.name, d.handler)
			d:close()
		end
	end

	--TODO actually close the baseboard
end

--returns number of modules present on baseboard
function BaseBoard:get_user_modules_size()
	--state sanity check
	assert(type(self.comms)=="table")

	local comms=self.comms

	-- In case of get_user_modules_size command is atended by admin module in handler 0 and send operation is 000

	local handler_packet = ADMIN_HANDLER_SEND_COMMAND .. string.char(DEFAULT_PACKET_SIZE) .. NULL_BYTE
	local admin_packet = GET_USER_MODULES_SIZE_COMMAND
	local get_user_modules_size_packet  = handler_packet .. admin_packet    

	local write_res = comms.send(ADMIN_MODULE_IN_ENDPOINT, get_user_modules_size_packet, TIMEOUT)
	if write_res then
         	local data, err = comms.read(ADMIN_MODULE_OUT_ENDPOINT, GET_LINES_RESPONSE_PACKET_SIZE, TIMEOUT)
		if not data then
			bobot.debugprint("u4b:get_user_modules_size:comunication with I/O board read error", err)
			return 0
		else
			local user_modules_size = string.byte(data, 5)	
			return user_modules_size
		end
	else	
	local retry = 0
        while(write_res == nil and retry < MAX_RETRY) do
			write_res = comms.send(ADMIN_MODULE_IN_ENDPOINT, get_user_modules_size_packet, TIMEOUT)
			bobot.debugprint("u4b:get_user_modules_size:comunication with I/O board write error", write_res)
			retry = retry+1
		end
		return 0
   	end
end

--returns thename of a given (by a 1-based index)module 
function BaseBoard:get_user_module_line(index)
	--state & parameter sanity check
	assert(type(index)=="number")
	assert(index>0)	
	assert(type(self.comms)=="table")


	local comms=self.comms

	-- In case of get_user_module_line command is atended by admin module in handler 0 and send operation is 000
	local get_user_module_line_packet_length = string.char(GET_USER_MODULE_LINE_PACKET_SIZE)
	local handler_packet = ADMIN_HANDLER_SEND_COMMAND .. get_user_module_line_packet_length .. NULL_BYTE
	local admin_packet = GET_USER_MODULE_LINE_COMMAND .. string.char(index-1)
	local get_user_module_line_packet  = handler_packet .. admin_packet

	local write_res = comms.send(ADMIN_MODULE_IN_ENDPOINT, get_user_module_line_packet, TIMEOUT)
    	if write_res then
		local data, err = comms.read(ADMIN_MODULE_OUT_ENDPOINT, GET_LINE_RESPONSE_PACKET_SIZE, TIMEOUT)
		if not data then
			bobot.debugprint("u4b:get_user_modules_line:comunication with I/O board read error", err)
			return
		end
		--the name is between a header and a null
		local end_mark = string.find(data, "\000", GET_USER_MODULE_LINE_PACKET_SIZE, true)
		if not end_mark then
			bobot.debugprint ("u4b:get_user_module_line:Error parsing module name")
			return
		end
		local module_name = string.sub(data, GET_USER_MODULE_LINE_PACKET_SIZE, end_mark-1)
		return module_name
	else	
		bobot.debugprint("u4b:get_user_module_line:comunication with I/O board write error", write_res)
	end
end

-- resets the baseboard, after this operation the baseboard will claim reenumeration to the operative system
-- this function is deprecated by force_close_all
function BaseBoard:close_all()
	for d_name,d in pairs(self.devices) do
		--bobot.debugprint ("===", d.name,d.handler)
		if d.handler then d:close() end
	end
end

function BaseBoard:reset()
	--state & parameter sanity check
	assert(type(self.comms)=="table")
	
	local comms=self.comms
	-- In case of reset_base_board command is atended by admin module in handler 0 and send operation is 000
	local handler_packet = ADMIN_HANDLER_SEND_COMMAND .. string.char(DEFAULT_PACKET_SIZE) .. NULL_BYTE
	local admin_packet = string.char(0xFF)  --CLOSEALL_BASE_BOARD_COMMAND
	local reset_base_board_packet  = handler_packet .. admin_packet

	local write_res = comms.send(ADMIN_MODULE_IN_ENDPOINT, reset_base_board_packet, TIMEOUT)
    	if write_res then
		-- no tego que leer respuesta porque se reseteo
		--libusb.close(libusb_handler)
		--self.libusb_handler=nil
		--for d_name,d in pairs(self.devices) do
			--bobot.debugprint ("===", d.name,d.handler)
		--	d.handler=nil
		--end
	else	
		bobot.debugprint("u4b:reset:comunication with I/O board write error", write_res)
	end
end

function BaseBoard:force_close_all()
	--state & parameter sanity check
	assert(type(self.comms)=="table")
	
	local comms=self.comms
	-- In case of reset_base_board command is atended by admin module in handler 0 and send operation is 000
	local handler_packet = ADMIN_HANDLER_SEND_COMMAND .. string.char(DEFAULT_PACKET_SIZE) .. NULL_BYTE
	local admin_packet = CLOSEALL_BASE_BOARD_COMMAND
	local reset_base_board_packet  = handler_packet .. admin_packet

--bobot.debugprint ('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
	local write_res = comms.send(ADMIN_MODULE_IN_ENDPOINT, reset_base_board_packet, TIMEOUT)
--bobot.debugprint ('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    	if write_res then
		local data, err = comms.read(ADMIN_MODULE_OUT_ENDPOINT,	CLOSEALL_BASE_BOARD_RESPONSE_PACKET_SIZE, TIMEOUT)
		if err then
			bobot.debugprint("u4b:force_close_all:comunication with I/O board read error",err)
		else
			--bobot.debugprint("u4b:force_close_all:libusb read",string.byte(data,1,string.len(data)))
		end
		for d_name,d in pairs(self.devices) do
			--bobot.debugprint ("===", d.name,d.handler)
			d.handler=nil
		end
	else	
		bobot.debugprint("u4b:force_close_all:comunication with I/O board write error", write_res)
	end
end

return BaseBoard
