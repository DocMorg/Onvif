from onvif import ONVIFCamera


class DeviceIOTests:
    def __init__(self, cam):
        self.cam = cam
        self.media = self.cam.create_media_service()
        self.io = self.cam.create_deviceio_service()

    def GetServiceCapabilities(self):
        try:
            capabilities = self.io.GetServiceCapabilities()
            items = []
            report = 'Device has:\n'
            for item in capabilities:
                items.append('{} {}'.format(item[1], item[0][1:]))
            report += (', ').join(items)
            if ((capabilities is None) or (len(capabilities) == 0)):
                return {'name': 'GetServiceCapabilities', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Device Input Output service capabilities',
                'extension': 'The DUT did not send GetServiceCapabilitiesResponse message',
                'response': str(capabilities),
                'report': 'Not Supported\nThe device did not send GetServiceCapabilitiesResponse message'}}
            else:
                return {'name': 'GetServiceCapabilities', 'service': 'deviceio',
                'result': {'supported': True,
                'report_name': 'Device Input Output service capabilities',
                'extension': None,
                'response': str(capabilities), 'report': report}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetServiceCapabilities', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Device Input Output service capabilities',
                'extension': 'Optional Action Not Implemented',
				'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetServiceCapabilities', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Device Input Output service capabilities',
                'extension': str(e), 'response': "",
                'report': 'Not Supported'}}

    def GetAudioSourceConfiguration(self):
        try:
            asctoken = self.media.GetProfiles()[0].AudioSourceConfiguration._token
            response = self.io.GetAudioSourceConfiguration({'AudioSourceToken': asctoken})
            if ((response is None) or (len(response) == 0)):
                return {'name': 'GetAudioSourceConfiguration', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Audio source configuration',
                'extension': 'The DUT did not send GetAudioSourceConfigurationResponse message',
                'response': str(response),
                'report': 'Not Supported'}}
            else:
                return {'name': 'GetAudioSourceConfiguration', 'service': 'deviceio',
                'result': {'supported': True,
                'report_name': 'Audio source configuration',
                'extension': None,
                'response': str(response), 'report': 'Supported'}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetAudioSourceConfiguration', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Audio source configuration',
                'extension': 'Optional Action Not Implemented',
				'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetAudioSourceConfiguration', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Audio source configuration',
                'extension': str(e), 'response': "",
                'report': 'Not Supported'}}

    def GetAudioSourceConfigurationOptions(self):
        try:
            asctoken = self.media.GetProfiles()[0].AudioSourceConfiguration._token
            response = self.io.GetAudioSourceConfiguration({'AudioSourceToken': asctoken})
            if ((response is None) or (len(response) == 0)):
                return {'name': 'GetAudioSourceConfigurationOptions', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Audio source configuration options',
                'extension': 'The DUT did not send GetAudioSourceConfigurationOptionsResponse message',
                'response': str(response), 'report': 'Not Supported'}}
            else:
                return {'name': 'GetAudioSourceConfigurationOptions', 'service': 'deviceio',
                'result': {'supported': True,
                'report_name': 'Audio source configuration options',
                'extension': None,
                'response': str(response), 'report': 'Supported'}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetAudioSourceConfigurationOptions', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Audio source configuration options',
                'extension': 'Optional Action Not Implemented',
				'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetAudioSourceConfigurationOptions', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Audio source configuration options',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioSources(self):
        try:
            response = self.io.GetAudioSources()
            if ((response is None) or (len(response) == 0)):
                return {'name': 'GetAudioSources', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Audio sources settings',
                'extension': 'The DUT did not send GetAudioSourcesResponse message',
                'response': str(response), 'report': 'Not Supported'}}
            else:
                return {'name': 'GetAudioSources', 'service': 'deviceio',
                'result': {'supported': True,
                'report_name': 'Audio sources settings',
                'extension': None,
                'response': str(response), 'report': 'Supported'}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetAudioSources', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Audio sources settings',
                'extension': 'Optional Action Not Implemented',
				'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetAudioSources', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Audio sources settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetDigitalInputs(self):
        try:
            response = self.io.GetDigitalInputs()
            inputs = []
            report = ''
            for item in response:
                inputs.append(item._token)
            if len(inputs) == 1:
                report += 'Device has 1 Digital input, with token {}'.format(('').join(inputs))
            elif len(inputs) > 1:
                report += 'Device has {} Digital inputs, with tokens: {}'.format(int(len(inputs)), (', ').join(inputs))
            if ((response is None) or (len(response) == 0)):
                return {'name': 'GetDigitalInputs', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Digital inputs',
                'extension': 'The DUT did not send GetDigitalInputsResponse message',
                'response': str(response),
                'report': 'Not Supported'}}
            else:
                return {'name': 'GetDigitalInputs', 'service': 'deviceio',
                'result': {'supported': True,
                'report_name': 'Digital inputs',
                'extension': None,
                'response': str(response), 'report': report}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetDigitalInputs', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Digital inputs',
                'extension': 'Optional Action Not Implemented',
				'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetDigitalInputs', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Digital inputs',
                'extension': str(e), 'response': "",
                'report': 'Not Supported'}}

    def GetRelayOutputs(self):
        try:
            response = self.io.GetRelayOutputs()
            report = 'Device Relay output settings:\n'
            try:
                token = response[0]._token
                token_report = 'Relay unique token is: {}\n'.format(token) if token else 'Relay unique token is not specified\n'
            except:
                token_report = ''
            try:
                mode = response[0].Properties.Mode
                mode_report = 'Relay mode is Bistable: After setting the state, the relay remains in this state\n' if mode == 'Bistable' else 'Relay mode is Monostable: After setting the state, the relay returns to its idle state after the specified time\n'
            except:
                mode_report = ''
            try:
                delay = response[0].Properties.DelayTime
                delay_report = 'Time after which the relay returns to its idle state if it is in monostable mode is: {}\n'.format(delay) if delay else 'Time after which the relay returns to its idle state if it is in monostable mode is not specified\n'
            except:
                delay_report = ''
            try:
                idle = response[0].Properties.IdleState
                idle_report = 'Relay state currently is: {}\n'.format(idle)
            except:
                idle_report = ''
            report += token_report
            report += mode_report
            report += delay_report
            report += idle_report
            if ((response is None) or (len(response) == 0)):
                return {'name': 'GetRelayOutputs', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Relay status',
                'extension': 'The DUT did not send GetRelayOutputsResponse message',
                'response': str(response),
                'report': 'Not Supported\nThe device did not send GetRelayOutputsResponse message'}}
            else:
                return {'name': 'GetRelayOutputs', 'service': 'deviceio',
                'result': {'supported': True,
                'report_name': 'Relay status',
                'extension': None,
                'response': str(response),
                'report': report }}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetRelayOutputs', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Relay status',
                'extension': 'Optional Action Not Implemented',
				'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetRelayOutputs', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Relay status',
                'extension': str(e), 'response': "",
                'report': 'Not Supported'}}

    def GetSerialPorts(self):
        try:
            response = self.io.GetSerialPorts()
            ports = []
            report = ''
            for item in response:
                ports.append(item._token)
            if len(ports) == 1:
                report += 'Device has 1 Serial port, with token {}'.format(('').join(ports))
            elif len(ports) > 1:
                report += 'Device has {} Serial ports, with tokens: {}'.format(int(len(ports)), (', ').join(ports))
            if ((response is None) or (len(response) == 0)):
                return {'name': 'GetSerialPorts', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Serial ports',
                'extension': 'The DUT did not send GetSerialPortsResponse message',
                'response': str(response), 'report': 'Not Supported'}}
            else:
               return {'name': 'GetSerialPorts', 'service': 'deviceio',
               'result': {'supported': True,
               'report_name': 'Serial ports',
               'extension': None,
               'response': str(response), 'report': report}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetSerialPorts', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Serial ports',
                'extension': 'Optional Action Not Implemented',
				'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                 return {'name': 'GetSerialPorts', 'service': 'deviceio',
                 'result': {'supported': False,
                 'report_name': 'Serial ports',
                 'extension': str(e),
				 'response': "", 'report': 'Not Supported'}}

    def GetVideoOutputs(self):
        try:
            response = self.io.GetVideoOutputs()
            if ((response is None) or (len(response) == 0)):
                return {'name': 'GetVideoOutputs', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Video outputs settings',
                'extension': 'The DUT did not send GetVideoOutputsResponse message',
                'response': str(response), 'report': 'Not Supported'}}
            else:
                return {'name': 'GetVideoOutputs', 'service': 'deviceio',
                'result': {'supported': True,
                'report_name': 'Video outputs settings',
                'extension': None,
                'response': str(response), 'report': 'Supported'}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetVideoOutputs', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Video outputs settings',
                'extension': 'Optional Action Not Implemented',
				'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetVideoOutputs', 'service': 'deviceio',
                'result': {'supported': False,
                'report_name': 'Video outputs settings',
                'extension': str(e), 'response': "",
                'report': 'Not Supported'}}
