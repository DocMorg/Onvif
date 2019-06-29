from onvif import ONVIFCamera


class SearchTests:
    def __init__(self, cam):
        self.cam = cam
        self.search = self.cam.create_search_service()

    def GetServiceCapabilities(self):
        try:
            capabilities = self.search.GetServiceCapabilities()
            report = ''
            metadata = 'Metadata search is supported by the device\n' if capabilities._MetadataSearch == True else 'Metadata search is not supported by the device\n'
            events = 'General virtual property events in the FindEvents method is supported' if capabilities._GeneralStartEvents == True else 'General virtual property events in the FindEvents method is not supported'
            report += metadata
            report += events
            if ((capabilities is None) or (len(capabilities) == 0)):
                return {'name': 'GetServiceCapabilities', 'service': 'Search',
                'result': {'supported': False,
                'report_name': 'Search Service capabilities',
                'extension': 'The DUT did not send GetServiceCapabilitiesResponse message',
                'response': str(capabilities),
                'report': 'Not Supported' }}
            else:
                return {'name': 'GetServiceCapabilities', 'service': 'Search',
                'result': {'supported': True,
                'report_name': 'Search Service capabilities',
                'extension': None,
                'response': str(capabilities), 'report': report }}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetServiceCapabilities', 'service': 'Search',
                'result': {'supported': False,
                'report_name': 'Search Service capabilities',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetServiceCapabilities', 'service': 'Search',
                'result': {'supported': False,
                'report_name': 'Search Service capabilities',
                'extension': str(e), 'response': "",
                'report': 'Not Supported'}}