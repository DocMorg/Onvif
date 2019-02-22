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

	    def GetServiceCapabilities(self):
        imaging = self.cam.create_imaging_service()
        return imaging.GetServiceCapabilities()

	#rework Imaging Tests, focus, etc
    def GetImagingSettings(self):
        media = self.cam.create_media_service()
        imaging = self.cam.create_imaging_service()
        vstoken = media.GetVideoSources()[0]._token
        return imaging.GetImagingSettings({'VideoSourceToken': vstoken})

    def GetMoveOptions(self):
        media = self.cam.create_media_service()
        imaging = self.cam.create_imaging_service()
        vstoken = media.GetVideoSources()[0]._token
        return imaging.GetMoveOptions({'VideoSourceToken': vstoken})

    def GetStatus(self):
        media = self.cam.create_media_service()
        imaging = self.cam.create_imaging_service()
        vstoken = media.GetVideoSources()[0]._token
        return imaging.GetStatus({'VideoSourceToken': vstoken})

	def GetSnapshotUri(self):
		media_service = self.cam.create_media_service()
		token = media_service.GetProfiles()[0]._token
		return media_service.GetSnapshotUri({'ProfileToken': token}).Uri