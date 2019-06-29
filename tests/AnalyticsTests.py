from onvif import ONVIFCamera


class AnalyticsTests:
    def __init__(self, cam):
        self.cam = cam
        self.media = self.cam.create_media_service()
        self.analytics = self.cam.create_analytics_service()
        self.analytics_rules = self.cam.create_analytics_rules_service()
        self.vactoken = self.media.GetProfiles()[0].VideoAnalyticsConfiguration._token

    def GetServiceCapabilities(self):
        try:
            response = self.analytics.GetServiceCapabilities()
            report = ''
            try:
                response._AnalyticsModuleSupport
                report1 = 'Device supports analytics rules interface and the rules syntax\n' if response._AnalyticsModuleSupport == True else 'Device does not support analytics rules interface and the rules syntax\n'
            except:
                report1 = ''

            try:
                response._RuleSupport
                report2 = 'Device supports the scene analytics module interface\n' if response._RuleSupport == True else 'Device does not support the scene analytics module interface\n'
            except:
                report2 = ''
            try:
                response._CellBasedSceneDescriptionSupported
                report3 = 'Device produces the cell based scene description\n' if response._CellBasedSceneDescriptionSupported == True else 'Device does not produce the cell based scene description\n'
            except:
                report3 = ''
            try:
                response._RuleOptionsSupported
                report4 = 'Device supports the GetRuleOptions operation on the rules interface\n' if response._RuleOptionsSupported == True else 'Device does not support the GetRuleOptions operation on the rules interface\n'
            except:
                report4 = 'Device does not support the GetRuleOptions operation on the rules interface\n'
            try:
                response._AnalyticsModuleOptionsSupported
                report5 = 'Device supports the GetAnalyticsModuleOptions operation on the analytics interface' if response._AnalyticsModuleOptionsSupported == True else 'Device does not support the GetAnalyticsModuleOptions operation on the analytics interface'
            except:
                report5 = 'Device does not support the GetAnalyticsModuleOptions operation on the analytics interface'
            report += report1
            report += report2
            report += report3
            report += report4
            report += report5
            if ((response is None) or (len(response) == 0)):
                return {'name': 'GetServiceCapabilities', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Analytics Service capabilities',
                'extension': 'The DUT did not send GetServiceCapabilitiesResponse message',
                'response': str(response), 'report': 'Not Supported' }}
            else:
                return {'name': 'GetServiceCapabilities', 'service': 'Analytics',
                'result': {'supported': True,
                'report_name': 'Analytics Service capabilities',
                'extension': None,
                'response': str(response), 'report': report}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetServiceCapabilities', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Analytics Service capabilities',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetServiceCapabilities', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Analytics Service capabilities',
                'extension': str(e), 'response': "",
                'report': 'Not Supported' }}

    def GetSupportedAnalyticsModules(self):
        try:
            report = ''
            supported_modules = self.analytics.GetSupportedAnalyticsModules({'ConfigurationToken': self.vactoken})
            if ((supported_modules is None) or (len(supported_modules) == 0)):
                return {'name': 'GetSupportedAnalyticsModules', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Supported analytics modules',
                'extension': 'The DUT did not send GetSupportedAnalyticsModulesResponse message',
                'response': str(supported_modules), 'report': 'Not Supported'}}
            else:
                for count, modules in enumerate(supported_modules.AnalyticsModuleDescription):
                    report = report + modules._Name+ '\n'
                report = "Device has {} analytics modules that are supported by the given VideoAnalyticsConfiguration\n".format(count + 1) + report[:-1]
                return {'name': 'GetSupportedAnalyticsModules', 'service': 'Analytics',
                'result': {'supported': True,
                'report_name': 'Supported analytics modules',
                'extension': None,
                'response': str(supported_modules), 'report': report}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetSupportedAnalyticsModules', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Supported analytics modules',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetSupportedAnalyticsModules', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Supported analytics modules',
                'extension': str(e), 'response': "",
                'report': 'Not Supported'}}

    def GetAnalyticsModules(self):
        try:
            report = ''
            analytics_modules = self.analytics.GetAnalyticsModules({'ConfigurationToken': self.vactoken})
            if ((analytics_modules is None) or (len(analytics_modules) == 0)):
                return {'name': 'GetAnalyticsModules', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Running analytics modules',
                'extension': 'The DUT did not send GetAnalyticsModulesResponse message',
                'response': str(analytics_modules), 'report': 'Not Supported'}}
            else:
                for count, modules in enumerate(analytics_modules):
                    report = report + modules._Name+ '\n'
                report = "Device has {} currently assigned set of analytics modules of a VideoAnalyticsConfiguration\n".format(count + 1) + report[:-1]
                return {'name': 'GetAnalyticsModules',
                'service': 'Analytics',
                'result': {'supported': True, 'report_name': 'Running analytics modules',
                'extension': None,
                'response': str(analytics_modules), 'report': report}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetAnalyticsModules', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Running analytics modules',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetAnalyticsModules', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Running analytics modules',
                'extension': str(e), 'response': "",
                'report': 'Not Supported' }}

    def GetSupportedRules(self):
        try:
            report = ''
            supported_rules = self.analytics_rules.GetSupportedRules({'ConfigurationToken': self.vactoken})
            if ((supported_rules is None) or (len(supported_rules) == 0)):
                return {'name': 'GetSupportedRules', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Supported analytics rules',
                'extension': 'The DUT did not send GetSupportedAnalyticsModulesResponse message',
                'response': str(supported_rules), 'report': 'Not Supported'}}
            else:
                for count, rules in enumerate(supported_rules.RuleDescription):
                    report = report + rules._Name + ' Rule'+ '\n'
                report = "Device has {} rules that are supported by the given VideoAnalyticsConfiguration\n".format(count + 1) + report[:-1]
                return {'name': 'GetSupportedRules', 'service': 'Analytics',
                'result': {'supported': True,
                'report_name': 'Supported analytics rules',
                'extension': None,
                'response': str(supported_rules), 'report': report}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetSupportedRules', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Supported analytics rules',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetSupportedRules', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Supported analytics rules',
                'extension': str(e), 'response': "",
                'report': 'Not Supported'}}

    def GetRules(self):
        try:
            report = ''
            rules_list = self.analytics_rules.GetRules({'ConfigurationToken': self.vactoken})
            if ((rules_list is None) or (len(rules_list) == 0)):
                return {'name': 'GetRules', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Currently assigned analytics rules',
                'extension': 'The DUT did not send GetAnalyticsModulesResponse message',
                'response': str(rules_list), 'report': 'Not Supported'}}
            else:
                for count, rules in enumerate(rules_list):
                    report = report + rules._Name + '\n'
                report = "Device has {} currently assigned set of rules of a VideoAnalyticsConfiguration\n".format(count + 1) + report[:-1]
                return {'name': 'GetRules', 'service': 'Analytics',
                'result': {'supported': True,
                'report_name': 'Currently assigned analytics rules',
                'extension': None,
                'response': str(rules_list), 'report': report}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetRules', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Currently assigned analytics rules',
                'extension': 'Optional Action Not Implemented', 
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetRules', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Currently assigned analytics rules',
                'extension': str(e), 
                'response': "", 'report': 'Not Supported' }}

    def DeleteRules(self):
        try:
            rules = self.analytics_rules.DeleteRules({'ConfigurationToken': self.vactoken, 'RuleName': 'MyLineDetector4'})
            if ((rules is None) or (len(rules) == 0)):
                return {'name': 'DeleteRules', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Delete rules support',
                'extension': 'The DUT did not delete Rule MyLineDetector4',
                'response': str(rules), 'report': 'Not Supported'}}
            else:
                return {'name': 'DeleteRules', 'service': 'Analytics',
                'result': {'supported': True,
                'report_name': 'Delete rules support',
                'extension': None,
                'response': str(rules), 'report': 'Supported'}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'DeleteRules', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Delete rules support',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'DeleteRules', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Delete rules support',
                'extension': str(e),
                'response': "", 'report': 'Not Supported' }}

    def GetTamperDetector(self):
        try:
            supported_modules = self.analytics.GetSupportedAnalyticsModules({'ConfigurationToken': self.vactoken})
            supported_rules = self.analytics_rules.GetSupportedRules({'ConfigurationToken': self.vactoken})
            items = []
            for modules in supported_modules.AnalyticsModuleDescription:
                items.append(modules._Name)
            for rules in supported_rules.RuleDescription:
                items.append(rules._Name)
            for item in items:
                if 'tamper' in item.lower():
                    report =  'Tamper detector is supported'
                    break
                else:
                    report =  'Tamper detector is not supported'
                    break
            if ((items is None) or (len(items) == 0)):
                return {'name': 'GetTamperDetector', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Tamper detector',
                'extension': '',
                'response': str(items), 'report': 'Not Supported'}}
            else:
                return {'name': 'GetTamperDetector', 'service': 'Analytics',
                'result': {'supported': True,
                'report_name': 'Tamper detector',
                'extension': None,
                'response': str(items), 'report': report }}
        except Exception as e:
            return {'name': 'GetTamperDetector', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Tamper detector',
                'extension': str(e),
                'response': "", 'report': 'Not Supported' }}

    def GetMotionDetector(self):
        try:
            supported_modules = self.analytics.GetSupportedAnalyticsModules({'ConfigurationToken': self.vactoken})
            supported_rules = self.analytics_rules.GetSupportedRules({'ConfigurationToken': self.vactoken})
            items = []
            for modules in supported_modules.AnalyticsModuleDescription:
                items.append(modules._Name)
            for rules in supported_rules.RuleDescription:
                items.append(rules._Name)
            for item in items:
                if 'motion' in item.lower():
                    report =  'Motion detector is supported'
                    break
                else:
                    report =  'Motion detector is not supported'
                    break
            if ((items is None) or (len(items) == 0)):
                return {'name': 'GetMotionDetector', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Motion detector',
                'extension': '',
                'response': str(items), 'report': 'Not Supported'}}
            else:
                return {'name': 'GetMotionDetector', 'service': 'Analytics',
                'result': {'supported': True,
                'report_name': 'Motion detector',
                'extension': None,
                'response': str(items), 'report': report }}
        except Exception as e:
            return {'name': 'GetMotionDetector', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Motion detector',
                'extension': str(e),
                'response': "", 'report': 'Not Supported' }}

    def GetVehicleDetector(self):
        try:
            supported_modules = self.analytics.GetSupportedAnalyticsModules({'ConfigurationToken': self.vactoken})
            supported_rules = self.analytics_rules.GetSupportedRules({'ConfigurationToken': self.vactoken})
            items = []
            for modules in supported_modules.AnalyticsModuleDescription:
                items.append(modules._Name)
            for rules in supported_rules.RuleDescription:
                items.append(rules._Name)
            for item in items:
                if 'vehicle' in item.lower():
                    report =  'Vehicle detector is supported'
                    break
                else:
                    report =  'Vehicle detector is not supported'
                    break
            if ((items is None) or (len(items) == 0)):
                return {'name': 'GetVehicleDetector', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Vehicle detector',
                'extension': '',
                'response': str(items), 'report': 'Not Supported'}}
            else:
                return {'name': 'GetVehicleDetector', 'service': 'Analytics',
                'result': {'supported': True,
                'report_name': 'Vehicle detector',
                'extension': None,
                'response': str(items), 'report': report }}
        except Exception as e:
            return {'name': 'GetVehicleDetector', 'service': 'Analytics',
                'result': {'supported': False,
                'report_name': 'Vehicle detector',
                'extension': str(e),
                'response': "", 'report': 'Not Supported' }}

