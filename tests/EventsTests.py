from onvif import ONVIFCamera
import random
import string
import datetime
import requests


class EventsTests:
    
    def __init__(self, cam):
        self.cam = cam
        self.event_service = self.cam.create_events_service()

    def GetEventProperties(self):
        try:
            properties = self.event_service.GetEventProperties()
            topic = str(properties.TopicNamespaceLocation[0])
            status_code = requests.get(topic).status_code
            if(len(properties) > 0):
                return {'name': 'GetEventProperties', 'service': 'Events',
                'result': {'supported': True,
                'report_name': 'Event properties',
                'extension': None, 'response': str(properties),
                'report': 'Supported'}}
            elif((len(properties) > 0) and (status_code != 200)):
                return {'name': 'GetEventProperties', 'service': 'Events',
                'result': {'supported': True,
                'report_name': 'Event properties',
                'extension': 'DUT does not return a valid topic namespace. Status Code != 200',
                'response': str(properties),
                'report': 'Supported'}}
            elif((len(properties) > 0) and (len(properties.TopicExpressionDialect) < 2)):
                return {'name': 'GetEventProperties', 'service': 'Events',
                'result': {'supported': True,
                'report_name': 'Event properties',
                'extension': 'None or only one Mandatory TopicExpressionDialects are supported by the DUT',
                'response': str(properties),
                'report': 'Supported'}}
            elif((len(properties) > 0) and (len(properties.TopicExpressionDialect) < 2) and (status_code != 200)):
                return {'name': 'GetEventProperties', 'service': 'Events',
                'result': {'supported': True,
                'report_name': 'Event properties',
                'extension': 'None or only one Mandatory TopicExpressionDialects are supported by the DUT. DUT does not return a valid topic namespace.',
                'response': str(properties),
                'report': 'Supported'}}
            elif((len(properties) > 0) and (len(properties.MessageContentFilterDialect) < 1)):
                return {'name': 'GetEventProperties', 'service': 'Events',
                'result': {'supported': True,
                'report_name': 'Event properties',
                'extension': 'Mandatory MessageContentFilterDialect is not supported by the DUT. None or only one Mandatory TopicExpressionDialects are supported by the DUT.',
                'response': str(properties),
                'report': 'Supported'}}
            elif((len(properties) > 0) and (len(properties.MessageContentFilterDialect) < 1) and (status_code != 200)):
                return {'name': 'GetEventProperties', 'service': 'Events',
                'result': {'supported': True,
                'report_name': 'Event properties',
                'extension': 'Mandatory MessageContentFilterDialect is not supported by the DUT. None or only one Mandatory TopicExpressionDialects are supported by the DUT. DUT does not return a valid topic namespace.',
                'response': str(properties),
                'report': 'Supported'}}
            elif((len(properties) > 0) and (len(properties.MessageContentFilterDialect) < 1) and (len(properties.TopicExpressionDialect) < 2)):
                return {'name': 'GetEventProperties', 'service': 'Events',
                'result': {'supported': True,
                'report_name': 'Event properties',
                'extension': 'Mandatory MessageContentFilterDialect is not supported by the DUT',
                'response': str(properties),
                'report': 'Supported'}}
            elif((len(properties) > 0) and (len(properties.MessageContentFilterDialect)) < 1 and (len(properties.TopicExpressionDialect)) < 2 and (status_code != 200)):
                return {'name': 'GetEventProperties', 'service': 'Events',
                'result': {'supported': True,
                'report_name': 'Event properties',
                'extension': 'Mandatory MessageContentFilterDialect is not supported by the DUT. DUT does not return a valid topic namespace.',
                'response': str(properties),
                'report': 'Supported'}}
            else:
                return {'name': 'GetEventProperties', 'service': 'Events',
                'result': {'supported': False,
                'report_name': 'Event properties',
                'extension': 'The DUT did not send a GetEventPropertiesResponse message',
                'response': str(properties), 'report': 'Not Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'name': 'GetEventProperties', 'service': 'Events',
                'result': {'supported': False,
                'report_name': 'Event properties',
                'extension': 'Optional Action Not Implemented',
				'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetEventProperties', 'service': 'Events',
                'result': {'supported': False,
                'report_name': 'Event properties',
                'extension': str(e), 'response': "", 'report': 'Not Supported' }}

    def CreatePullPointSubscription(self):
        try:
            subs = self.event_service.CreatePullPointSubscription()
            curr = subs.CurrentTime
            term = subs.TerminationTime
            delt = int((term - curr).total_seconds())
            if(subs != []):
                if (delt >= 10):
                    return {'name': 'CreatePullPointSubscription', 'service': 'Events',
                    'result': {'supported': True,
                    'report_name': 'PullPoint subscription',
                    'extension': 'Valid values for SubscriptionReference CurrentTime and TerminationTime are returned(TerminationTime >= CurrentTime + InitialTerminationTime)',
                    'response': str(subs), 'report': 'Supported\nValid values for SubscriptionReference CurrentTime and TerminationTime are returned(TerminationTime >= CurrentTime + InitialTerminationTime)'}}
                else:
                    return {'name': 'CreatePullPointSubscription', 'service': 'Events',
                    'result': {'supported': False,
                    'report_name': 'PullPoint subscription',
                    'extension': 'Returned response with TerminationTime < CurrentTime + InitialTerminationTime).', 'response': str(subs),
                    'report': 'Not Supported\nReturned response with TerminationTime < CurrentTime + InitialTerminationTime)'}}
            else:
                return {'name': 'CreatePullPointSubscription', 'service': 'Events',
                'result': {'supported': False,
                'report_name': 'PullPoint subscription',
                'extension': 'The DUT did not send CreatePullPointSubscriptionResponse message',
                'response': str(subs), 'report': 'Not Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'name': 'CreatePullPointSubscription', 'service': 'Events',
                'result': {'supported': False,
                'report_name': 'PullPoint subscription',
                'extension': 'Optional Action Not Implemented',
				'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'CreatePullPointSubscription', 'service': 'Events',
                'result': {'supported': False,
                'report_name': 'PullPoint subscription',
                'extension': str(e), 'response': "",
                'report': 'Not Supported' }}
			

    def GetServiceCapabilities(self):
        try:
            capabilities = self.event_service.GetServiceCapabilities()
            if (len(capabilities) > 0):
                return {'name': 'GetServiceCapabilities', 'service': 'Events',
                'result': {'supported': True,
                'report_name': 'Events service capabilities',
                'extension': None, 'response': str(capabilities), 'report': 'Supported'}}
            else:
                return {'name': 'GetServiceCapabilities', 'service': 'Events',
                'result': {'supported': False,
                'report_name': 'Events service capabilities',
                'extension': 'The DUT did not send valid GetServiceCapabilitiesResponse message',
                'response': str(capabilities), 'report': 'Not Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'name': 'GetServiceCapabilities', 'service': 'Events',
                'result': {'supported': False,
                'report_name': 'Events service capabilities',
                'extension': 'Optional Action Not Implemented',
				'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetServiceCapabilities', 'service': 'Events',
                'result': {'supported': False,
                'report_name': 'Events service capabilities',
                'extension': str(e), 'response': "",
                'report': 'Not Supported' }}

    # def PullMessages(self):
    #     self.cam.create_pullpoint_service()
    #     service = self.cam.pullpoint.zeep_client._get_service('EventService')
    #     port = self.cam.pullpoint.zeep_client._get_port(service, 'PullPointSubscription')
    #     port.binding_options['address'] = onvif_camera.xaddrs['http://www.onvif.org/ver10/events/wsdl/PullPointSubscription']
    #     plp = onvif_camera.pullpoint.zeep_client.bind('EventService', 'PullPointSubscription')
    #     response = plp.PullMessages(Timeout = timedelta(seconds = 20), MessageLimit = 100)
    #     return response
