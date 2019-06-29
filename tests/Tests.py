from . import *
from flask import jsonify


class Tests(object):
    def __init__(self, cam):
        self.cam = cam
        self.test_types = {
            'analytics': AnalyticsTests,
            'device': CoreTests,
            'deviceio': DeviceIOTests,
            'events': EventsTests,
            'imaging': ImagingTests,
            'media': MediaTests,
            'ptz': PTZTests,
            'pullpoint': PullpointTests,
            'recording': RecordingTests,
            'replay': ReplayTests,
            'search': SearchTests
        }

    def service_test(self, test_type, method_name):

        if test_type in self.test_types:
            test = self.test_types[test_type](self.cam)
        else:
            return dict(response = 'Sorry, Service with name {} does not exist.'.format(test_type))

        try:
            method = getattr(test, method_name)

        except AttributeError:
            return dict(response = 'Sorry, method with name ' + method_name + ' does not exist.')

        except Exception as e:
            return dict(response = 'ONVIFError, ' + method_name + ' method is not supported, ' + e)

        return dict(response = method())

    def avaliable_tests(self):
        test_descriptions = []
        supported_test_types = self.cam.get_supported_services()

        for test_type in supported_test_types:
            if test_type in self.test_types:
                test = self.test_types[test_type]
                listing = list(filter(lambda func: not func.startswith("__") and callable(getattr(test, func)), dir(test)))

                test_descriptions.append({
                    'service': test_type,
                    'available_tests': listing
                })

        return dict(response=test_descriptions)
