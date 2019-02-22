import csv
from flask import jsonify
from onvif import ONVIFCamera
from Naked.toolshed.shell import execute_js

class Core_Test:
	def __init__(self,ip,port,user,passw):
		self.ip = ip
		self.port = port
		self.user = user
		self.passw = passw
		self.cam = ONVIFCamera(self.ip, self.port, self.user, self.passw)

	def GetCapabilities(self):
		capabilities = self.cam.devicemgmt.GetCapabilities()
		if (len(capabilities) > 0):
			return 'GetCapabilities works', capabilities
		else:
			return 'GetCapabilities does not work', capabilities

	def GetDiscoveryMode(self):
		request = self.cam.devicemgmt.GetDiscoveryMode()
		if (request):
			 return request + ' GetDiscoveryMode works', request
		else:
			return 'GetDiscoveryMode does not work', request

	def SetDiscoveryMode(self):
		get1 = self.cam.devicemgmt.GetDiscoveryMode()
		if (get1 == 'Discoverable'):
			set1 = self.cam.devicemgmt.SetDiscoveryMode({'DiscoveryMode': 'NonDiscoverable'})
			get2 = self.cam.devicemgmt.GetDiscoveryMode()
			self.cam.devicemgmt.SetDiscoveryMode({'DiscoveryMode': get1})
			if (get1 != get2 ):
				return 'Left Discoverable, SetDiscoveryMode works', set1
			else:
				return 'SetDiscoveryMode does not work', set1
		elif (get1 == 'NonDiscoverable'):
			set1 = self.cam.devicemgmt.SetDiscoveryMode({'DiscoveryMode': 'Discoverable'})
			get2 = self.cam.devicemgmt.GetDiscoveryMode()
			self.cam.devicemgmt.SetDiscoveryMode({'DiscoveryMode': get1})
			if (get1 != get2):
				return 'left Nondiscoverable, SetDiscoveryMode works', set1
			else:
				return 'SetDiscoveryMode does not work', set1
		else:
			return 'It seems GetDiscoveryMode does not work', get1
		

	def GetScopes(self):
		response = self.cam.devicemgmt.GetScopes()
		if (len(response) > 0):
			return 'GetScopes works', response
		else:
			return 'GetScopes does not work', response

	def AddScopes(self):
		item = "onvif://www.onvif.org/type/test"
		add = self.cam.devicemgmt.AddScopes({'ScopeItem': item})
		# execute_js('start_probe.js')
		gett = self.cam.devicemgmt.GetScopes()
		if (gett != []):
			gett = self.cam.devicemgmt.GetScopes()[-1].ScopeItem
		# execute_js('start_probe.js')
		self.cam.devicemgmt.RemoveScopes({'ScopeItem': item})
		if (item == gett):
			return 'AddScopes works', add
		else:
			return 'AddScopes does not work', add

	def RemoveScopes(self):
		item = "onvif://www.onvif.org/type/test"
		add = self.cam.devicemgmt.AddScopes({'ScopeItem': item})
		# execute_js('start_probe.js')
		remove = self.cam.devicemgmt.RemoveScopes({'ScopeItem': item})
		# execute_js('start_probe.js')
		gett = self.cam.devicemgmt.GetScopes()
		if (gett != []):
			gett = self.cam.devicemgmt.GetScopes()[-1].ScopeItem	
		if (item != gett):
			return 'RemoveScopes works', remove
		else:
			return 'RemoveScopes does not work', remove

	def GetHostname(self):
		name = self.cam.devicemgmt.GetHostname()
		if (name):
			return 'GetHostname works', name,
		else:
			return 'GetHostname does not work', name

	def SetHostname(self):
		get1 = self.cam.devicemgmt.GetHostname().Name
		name = "Onviftest1"
		set1 = self.cam.devicemgmt.SetHostname({'Name': name})
		get2 = self.cam.devicemgmt.GetHostname().Name
		self.cam.devicemgmt.SetHostname({'Name': get1})
		if (get1 != get2):
			return 'SetHostname works', set1
		else:
			return 'SetHostname does not work', set1

	def GetNetworkInterfaces(self):
		interfaces = self.cam.devicemgmt.GetNetworkInterfaces()
		if (interfaces != []):
			return 'GetNetworkInterfaces works', interfaces
		else:
			return 'GetNetworkInterfaces does not work', interfaces

	def GetDNS(self):
		dns = self.cam.devicemgmt.GetDNS()
		if (dns != []):
			return 'GetDNS works', dns
		else:
			return 'GetDNS does not work', dns

	def GetNetworkProtocols(self):
		protocols = self.cam.devicemgmt.GetNetworkProtocols()
		if (protocols != []):
			return 'GetNetworkProtocols works', protocols
		else:
			return 'GeetNetworkProtocols does not work', protocols

	def GetNetworkDefaultGateway(self):
		gateways = self.cam.devicemgmt.GetNetworkDefaultGateway()
		if (gateways != []):
			return 'GetNetworkDefaultGateway works', gateways
		else:
			return 'GetNetworkDefaultGateway does not work', gateways

	def SetNetworkDefaultGateway(self): #"192.168.11.1"
		default = str(self.cam.devicemgmt.GetNetworkDefaultGateway().IPv4Address[0])
		#print default
		new = '10.1.0.1'
		set1 = self.cam.devicemgmt.SetNetworkDefaultGateway({'IPv4Address': new})
		# execute_js('start_probe.js')
		get1 = str(self.cam.devicemgmt.GetNetworkDefaultGateway().IPv4Address[0])
		# execute_js('start_probe.js')
		self.cam.devicemgmt.SetNetworkDefaultGateway({'IPv4Address': default})
		if (get1 == new):
			return 'SetNetworkDefaultGateway works', set1
		else:
			return 'SetNetworkDefaultGateway does not work', set1
		

	def GetDeviceInformation(self):
		info = self.cam.devicemgmt.GetDeviceInformation()
		if (info != []):
			return 'GetDeviceInformation works', info
		else:
			return 'GetDeviceInformation does not work', info

	def GetUsers(self):
		users = self.cam.devicemgmt.GetUsers()
		if (users != []):
			return 'GetUsers works', users
		else:
			return 'GetUsers does not work', users

	def DeleteUsers(self):
		set1 = self.cam.devicemgmt.CreateUsers({'Username': 'lalalal', 'Password': 'lalala', 'UserLevel': 'User'})
		delete = self.cam.devicemgmt.DeleteUsers({'Username':'lalalal'})
		if (delete != []):
			return 'DeleteUsers works', delete
		else:
			return 'DeleteUsers does not work', delete

	def GetNTP(self):
		ntp = self.cam.devicemgmt.GetNTP()
		if (ntp != []):
			return 'GetNTP works', ntp
		else:
			return 'GetNTP does not work', ntp

	def GetServices(self):
		services = self.cam.devicemgmt.GetServices()
		if (services != []):
			return 'GetServices works', services
		else:
			return 'GetServices does not work', services

	def GetSystemDateAndTime(self):
		datetime = self.cam.devicemgmt.GetSystemDateAndTime()
		if (datetime != []):
			return 'GetSystemDateAndTime works', datetime
		else: 	
			return 'GetSystemDateAndTime does not work', datetime

	def GetSystemUris(self):
		uri = self.cam.devicemgmt.GetSystemUris()
		if (uri != []):
			return 'GetSystemUris works', uri
		else:
			return 'GetSystemUris does not work', uri
	'''def CreateUsers(self):
		get1 = self.cam.devicemgmt.GetUsers()
		set1 = self.cam.devicemgmt.CreateUsers({'User':{'Username': 'lalalal', 'Password': 'lalala', 'UserLevel': 'User'}})
		execute_js('start_probe.js')
		get2 = self.cam.GetUsers().User.Username
		if get2 
		print set1
		print self.cam.devicemgmt.GetUsers()
	def SetNetworkInterfaces(self):
		get1 = self.cam.devicemgmt.GetNetworkInterfaces()
		print get1
		params = self.cam.devicemgmt.create_type('SetNetworkInterfaces')
		params.InterfaceToken='net'
		params.NetworkInterface.Enabled	= True
		params.NetworkInterface.IPv4.Enabled = True
		params.NetworkInterface.IPv4.DHCP = True
		params.NetworkInterface.IPv6.Enabled = True
		set1 = self.cam.devicemgmt.SetNetworkInterfaces(params)
		print set1
		get2 = self.cam.devicemgmt.GetNetworkInterfaces()
		print get2'''