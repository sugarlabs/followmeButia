module(..., package.seeall);

local socket=require('socket')

local comms_usb=require('comms_usb')
local comms_serial=require('comms_serial')


--baseboards[iSerial] = BaseBoard
baseboards={}

--Returns number of baseboards detected.
function init ()
	local n_boards_usb, n_boards_serial, n_boards = 0,0,0

	repeat 
		print ("Initializing bobot...")
		local n_boards_usb = comms_usb.init(baseboards)
		local n_boards_serial = comms_serial.init(baseboards)
		print ("Found boards:", n_boards_usb, "usb,", n_boards_serial, "serial" )
		n_boards = n_boards_usb + n_boards_serial
		if n_boards == 0 then socket.sleep(2) end
	until n_boards > 0    
	return n_boards
end

init()
