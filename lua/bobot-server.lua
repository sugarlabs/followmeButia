#!/usr/bin/lua

local socket = require("socket")
local bobot = require("bobot")

--tcp listening address
local ADDRESS = "*"
local PORT = 2009


local server = assert(socket.bind(ADDRESS, PORT))

local recvt={[1]=server}

local baseboards = bobot.baseboards

local devices = {}

local function get_device_name(n)
	if not devices[n] then
		return n
	end

	local i=2
	local nn=n.."#"..i
	while devices[nn] do
		i=i+1
		nn=n.."#"..i
	end

	return nn
end

local function read_devices_list()
print("=Listing Devices")
	local bfound
	devices={}
	for b_name, bb in pairs(baseboards) do
print("===board", b_name)
		for d_name,d in pairs(bb.devices) do
			local regname = get_device_name(d_name)
			devices[regname]=d
print("=====d_name", d_name, "regname", regname)
		end
		bfound = true
	end
	if not bfound then print ("ls:WARN: No Baseboard found.") end
end

local function check_open_device(d, ep1, ep2)
	if not d then return end
	if d.handler then
		--print ("ls:Already open", d.name, d.handler)
		return true
	else
        -- if the device is not open, then open the device
		print ("ls:Opening", d.name, d.handler)
		return d:open(ep1 or 1, ep2 or 1) --TODO asignacion de ep?
	end
end

local process = {}
process["LIST"] = function ()
	local ret,comma = "", ""
	for d_name, _ in pairs(devices) do
		ret = ret .. comma .. d_name
		comma=","
	end
	return ret
end
process["OPEN"] = function (parameters)
	local d  = parameters[2]
	local ep1= tonumber(parameters[3])
	local ep2= tonumber(parameters[4])

	if not d then
		print("ls:Missing 'device' parameter")
		return
	end
	
	local device = devices[d]
	if check_open_device(device, ep1, ep2) then	
		return "ok"
	else
		return "fail"
	end
end
process["DESCRIBE"] = function (parameters)
	local d  = parameters[2]
	local ep1= tonumber(parameters[3])
	local ep2= tonumber(parameters[4])

	if not d then
		print("ls:Missing \"device\" parameter")
		return
	end
	
	local device = devices[d]
	if not check_open_device(device, ep1, ep2) then	
		return "fail"
	end

	local ret = "{"
	for fname, fdef in pairs(device.api) do
		ret = ret .. fname .. "={"
		ret = ret .. " parameters={"
		for i,pars in ipairs(fdef.parameters) do
			ret = ret .. "[" ..i.."]={"
			for k, v in pairs(pars) do
				ret = ret .."[".. k .."]='"..tostring(v).."',"
			end
			ret = ret .. "},"
		end
		ret = ret .. "}, returns={"
		for i,rets in ipairs(fdef.returns) do
			ret = ret .. "[" ..i.."]={"
			for k, v in pairs(rets) do
				ret = ret .."[".. k .."]='"..tostring(v).."',"
			end
			ret = ret .. "},"
		end
		ret = ret .. "}}," 
	end
	ret=ret.."}"

	return ret
end
process["CALL"] = function (parameters)
	local d  = parameters[2]
	local call  = parameters[3]

	if not (d and call) then
		print("ls:Missing parameters", d, call)
		return
	end

	local device = devices[d]
	if not check_open_device(device, nil, nil) then	
		return "fail"
	end

	local api_call=device.api[call];	 if not api_call then return end
	
	if api_call.call then
		--local tini=socket.gettime()
		local ret = api_call.call(unpack(parameters,4))
		--print ('%%%%%%%%%%%%%%%% bobot-server',socket.gettime()-tini)
		return ret
	end
end
process["CLOSEALL"] = function ()
	if baseboards then
		for _, bb in pairs(baseboards) do
			---bb:close_all()
			bb:force_close_all() --modif andrew
		end
	end
	return "ok"
end

local function split_words(s)
	words={}

	for p in string.gmatch(s, "%S+") do
		words[#words+1	]=p
	end
	
	return words
end

read_devices_list()
print ("Listening...")
-- loop forever waiting for clients

while 1 do
	local recvt_ready, _, err=socket.select(recvt, nil, 1)
	if err~='timeout' then
		--ready to accept new tcp connection
		local client=recvt_ready[1]
		if client == server then
			local client, err=server:accept()
			if client then
				print ("bs:New client", client, client:getpeername())
				table.insert(recvt,client)			
			end
		elseif client then
			local line,err = client:receive()
			if err=='closed' then
				print ("bs:Closing client", client)
				for k, v in ipairs(recvt) do 
					if client==v then 
						table.remove(recvt,k) 
						break
					end
				end
			end
			if line then
				--local command, parameters = string.match(line, "^(%S+)%s*(.*)$")
				local words=split_words(line)
				local command=words[1]
				if not command then
					print("ls:Error parsing line:", line, command)
				else
					if not process[command] then
						print("ls:Command not supported:", command)
					else
						print ('=====', line)
						local ret = process[command](words) or ""
						--print("returning", ret)
						client:send(ret .."\n")
					end
				end
			end
		end
	end
end



