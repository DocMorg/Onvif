from onvif import ONVIFCamera

class RecordingTests:    
    def __init__(self, cam):
        self.cam = cam
        self.recording = self.cam.create_recording_service()
    

    def GetServiceCapabilities(self):
        try:
            recordings = self.recording.GetServiceCapabilities()
            report = ''
            dyn_recordings = 'Device supports Dynamic creation and deletion of recordings\n' if recordings._DynamicRecordings == True else 'Device does not support Dynamic creation and deletion of recordings\n'
            dyn_tracks = 'Device supports Dynamic creation and deletion of tracks\n' if recordings._DynamicTracks == True else 'Device does not support Dynamic creation and deletion of tracks\n'
            encodings = 'Encodings that are supported for recording: {}\n'.format(str(recordings._Encoding)) if recordings._Encoding else 'Encodings that are supported for recording are not specified\n'
            max_recordings = 'Maximum number of recordings supported: {}\n'.format(int(recordings._MaxRecordings)) if recordings._MaxRecordings else 'Maximum number of recordings supported is not specified\n'
            max_totalrate = 'Maximum supported bitrate for all recordings in kBit/s: {}\n'.format(recordings._MaxTotalRate) if recordings._MaxTotalRate else 'Maximum supported bitrate for all recordings is not specified\n'
            max_rate = 'Maximum supported bitrate for all tracks of a recording in kBit/s: {}\n'.format(recordings._MaxRate) if recordings._MaxRate else 'Maximum supported bitrate for all tracks of a recording is not specified'
            report += max_recordings
            report += encodings
            report += dyn_recordings
            report += dyn_tracks
            report += max_totalrate
            report += max_rate
            if ((recordings is None) or (len(recordings) == 0)):
                return {'name': 'GetServiceCapabilities', 'service': 'Recording',
                'result': {'supported': False,
                'report_name': 'Recording Service capabilities',
                'extension': 'The DUT did not send GetServiceCapabilitiesResponse message',
                'response': str(recordings),
                'report': 'Not Supported'}}
            else:
                return {'name': 'GetServiceCapabilities', 'service': 'Recording',
                'result': {'supported': True,
                'report_name': 'Recording Service capabilities',
                'extension': None,
                'response': str(recordings),
                'report': report}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetServiceCapabilities', 'service': 'Recording',
                'result': {'supported': False,
                'report_name': 'Recording Service capabilities',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetServiceCapabilities', 'service': 'Recording',
                'result': {'supported': False,
                'report_name': 'Recording Service capabilities',
                'extension': str(e), 'response': "",
                'report': 'Not Supported'}}
