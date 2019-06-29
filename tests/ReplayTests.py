from onvif import ONVIFCamera


class ReplayTests:
    def __init__(self, cam):
        self.cam = cam
        self.replay = self.cam.create_replay_service()

    def GetServiceCapabilities(self):
        try:
            replays = self.replay.GetServiceCapabilities()
            report = ''
            rtp = 'RTP/RTSP/TCP are supported by the Replay service\n' if replays._RTP_RTSP_TCP == True else 'RTP/RTSP/TCP are not supported by the Replay service\n'
            reverse = 'Device supports reverse playback as defined in the ONVIF Streaming Specification\n' if replays._ReversePlayback == True else 'Device do not support reverse playback as defined in the ONVIF Streaming Specification\n'
            session = 'Minimum and Maximum valid values supported as session timeout in seconds: {}'.format(replays._SessionTimeoutRange) if hasattr(replays,'_SessionTimeoutRange') else 'Minimum and Maximum valid values supported as session are not specified'
            report += rtp
            report += reverse
            report += session
            if ((replays is None) or (len(replays) == 0)):
                return {'name': 'GetServiceCapabilities', 'service': 'Replay',
                'result': {'supported': False,
                'report_name': 'Replay Service capabilities',
                'extension': 'The DUT did not send GetServiceCapabilitiesResponse message',
                'response': str(replays),
                'report': 'Not Supported'}}
            else:
                return {'name': 'GetServiceCapabilities', 'service': 'Replay',
                'result': {'supported': True,
                'report_name': 'Replay Service capabilities',
                'extension': None,
                'response': str(replays),
                'report': report}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetServiceCapabilities', 'service': 'Replay',
                'result': {'supported': False,
                'report_name': 'Replay Service capabilities',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetServiceCapabilities', 'service': 'Replay',
                'result': {'supported': False,
                'report_name': 'Replay Service capabilities',
                'extension': str(e), 'response': "",
                'report': 'Not Supported'}}

    def GetReplayConfiguration(self):
        try:
            configuration = self.replay.GetReplayConfiguration()
            report = ''
            session = 'RTSP session timeout in seconds: {}'.format(configuration.SessionTimeout) if configuration.SessionTimeout else 'RTSP session timeout is not specified'
            report += session
            if ((configuration is None) or (len(configuration) == 0)):
                return {'name': 'GetReplayConfiguration', 'service': 'Replay',
                'result': {'supported': False,
                'report_name': 'Replay configuraton',
                'extension': 'The DUT did not send Mandatory GetReplayConfigurationResponse message',
                'response': str(configuration),
                'report': 'Not Supported'}}
            else:
                return {'name': 'GetReplayConfiguration', 'service': 'Replay',
                'result': {'supported': True,
                'report_name': 'Replay configuraton',
                'extension': None,
                'response': str(configuration),
                'report': report}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetReplayConfiguration', 'service': 'Replay',
                'result': {'supported': False,
                'report_name': 'Replay configuraton',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetReplayConfiguration', 'service': 'Replay',
                'result': {'supported': False,
                'report_name': 'Replay configuraton',
                'extension': str(e), 'response': "",
                'report': 'Not Supported'}}

    def SetReplayConfiguration(self):
        try:
            timeout1 = self.replay.GetReplayConfiguration().SessionTimeout
            response = self.replay.SetReplayConfiguration({'Configuration': {'SessionTimeout': 'PT25S'}})
            timeout2 = self.replay.GetReplayConfiguration().SessionTimeout
            back = self.replay.SetReplayConfiguration({'Configuration': {'SessionTimeout': timeout1}})
            timeout3 = self.replay.GetReplayConfiguration().SessionTimeout
            if (timeout2 == timeout1):
			    return {'name': 'SetReplayConfiguration', 'service': 'Replay',
                'result': {'supported': False,
                'report_name': 'Set Replay configuraton support',
                'extension': 'The DUT did not set SetReplayConfiguration SessionTimeout to PT25S',
                'response': 'Response: '+ str(response) + 'Set Timeout failed, ' + str(timeout2),
                'report': 'Manual Replay configuration setting is not supported\nThe device did not set Replay configuration Session Timeout to 25s'}}        
            elif ((timeout2 != timeout1) and (response is None)):
                return {'name': 'SetReplayConfiguration', 'service': 'Replay',
                'result': {'supported': True,
                'report_name': 'Set Replay configuraton support',
                'extension': 'The DUT SetReplayConfiguration SessionTimeout to PT25S, but did not send valid SetReplayConfigurationResponse message',
                'report': 'Manual Replay configuration setting is supported\nSet timeout to {}, returned back to {}, but device did not send valid SetReplayConfigurationResponse message'.format(str(timeout2), str(timeout3)),
                'response': 'Response: '+ str(response) + ', set Timeout to ' + str(timeout2) + ', returned back to ' + str(timeout3)}}
            elif ((timeout2 != timeout1) and (response is not None)):
                return {'name': 'SetReplayConfiguration', 'service': 'Replay',
                'result': {'supported': True,
                'report_name': 'Set Replay configuraton support',
                'extension': None,
                'response': 'Response: '+ str(response) + ', set Timeout to ' + str(timeout2) + ', returned back to ' + str(timeout3),
                'report': 'Manual Replay configuration setting is supported\nSet timeout to {}, returned back to {}'.format(str(timeout2), str(timeout3))}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'SetReplayConfiguration', 'service': 'Replay',
                'result': {'supported': False,
                'report_name': 'Set Replay configuraton support',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented'}}
            else:
                return {'name': 'SetReplayConfiguration', 'service': 'Replay',
                'result': {'supported': False,
                'report_name': 'Set Replay configuraton support',
                'extension': str(e), 'response': "",
                'report': 'Not Supported'}}