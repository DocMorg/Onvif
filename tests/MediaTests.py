from onvif import ONVIFCamera, exceptions
from time import sleep

class MediaTests:
    def __init__(self, cam):
        self.cam = cam
        self.media = self.cam.create_media_service()

    def CreateProfile(self):
        try:
            token = self.media.GetProfiles()[0]._token
            token1 = self.media.GetProfiles()[-1]._token
            create = self.media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
            sleep(1)
            token2 = self.media.GetProfiles()[-1]._token
            if (token1 == token2):
                sleep(1)
                delete = self.media.DeleteProfile({'ProfileToken': token2})
                return {'test_id': 2, 'name': 'CreateProfile', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'Create Media profile',
                'extension': 'The DUT did not create Media profile with Name - Test',
                'response': str(create), 'report': 'The device did not create Media profile with name - Test'}}
            else:
                return {'test_id': 2, 'name': 'CreateProfile', 'service': 'Media',
                'result': {'supported': True,
                'report_name': 'Create Media profile',
                'extension': 'The DUT created Media profile with Name - Test',
                'response': str(create), 'report': 'The device successfully created Media profile with name - Test'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 2, 'name': 'CreateProfile', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'Create Media profile',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 2, 'name': 'CreateProfile', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'Create Media profile',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetProfiles(self):
        try:
            media = self.cam.create_media_service()
            profiles = self.media.GetProfiles()
            if ((profiles is None) or (len(profiles) == 0)):
                return {'test_id': 3, 'name': 'GetProfiles', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'Media profiles(GetProfiles)',
                'extension': 'The DUT did not returned GetProfilesResponse message',
                'response': str(profiles), 'report': 'Not Supported'}}
            else:
                return {'test_id': 3, 'name': 'GetProfiles', 'service': 'Media',
                'result': {'supported': True, 
                'report_name': 'Media profiles(GetProfiles)',
                'extension': None, 'response': str(profiles), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 3, 'name': 'GetProfiles', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'Media profiles(GetProfiles)',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 3, 'name': 'GetProfiles', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'Media profiles(GetProfiles)',
                'extension': str(e),'response': "", 'report': 'Not Supported'}}

    def GetSnapshotUri(self):
        try:
            report = 'Device shapshot URI is:\n'
            token = self.media.GetProfiles()[0]._token
            uri = self.media.GetSnapshotUri({'ProfileToken': token})
            report += uri.Uri
            if ((uri is None) or (len(uri) == 0)):
                return {'test_id': 4, 'name': 'GetSnapshotUri', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'Image snapshot',
                'extension': 'The DUT did not returned GetSnapshotUriResponse message',
                'response': str(uri), 'report': 'Not Supported\nThe device did not return GetSnapshotUriResponse message'}}
            else:
                return {'test_id': 4, 'name': 'GetSnapshotUri', 'service': 'Media',
                'result': {'supported': True,
                'report_name': 'Image snapshot',
                'extension': None, 'response': str(uri), 'report': report}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 4, 'name': 'GetSnapshotUri', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'Image snapshot',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 4, 'name': 'GetSnapshotUri', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'Image snapshot',
                'extension': str(e), 'response': "", 'report': 'Not Supported' }}


    # def AddAudioDecoderConfiguration(self):
    #     try:
    #         token = self.media.GetProfiles()[0]._token
    #         create = self.media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
    #         sleep(1)
    #         token = self.media.GetProfiles()[-1]._token
    #         audio_token = self.media.GetProfiles()[0].AudioDecoderConfiguration._token
    #         add_config = self.media.AddAudioDecoderConfiguration({'ProfileToken': token, 'ConfigurationToken': audio_token})
    #         sleep(1)
    #         audio_token2 = self.media.GetProfiles()[-1].AudioDecoderConfiguration._token
    #         sleep(1)
    #         delete = self.media.DeleteProfile({'ProfileToken': token})
    #         if (audio_token != audio_token2):
    #             return {'test_id': 5, 'name': 'AddAudioDecoderConfiguration', 'service': 'Media',
    #             'result': {'supported': False,
    #             'extension': 'The DUT did not add new AddAudioDecoderConfiguration',
    #             'response': str(add_config)}}
    #         else:
    #             return {'test_id': 5, 'name': 'AddAudioDecoderConfiguration', 'service': 'Media',
    #             'result': {'supported': True, 'extension': None, 'response': str(add_config)}}
    #     except AttributeError:
    #         return {'test_id': 5, 'name': 'AddAudioDecoderConfiguration', 'service': 'Media',
    #         'result': {'supported': False,
    #         'extension': 'AddAudioDecoderConfiguration does not work, AttributeError',
    #         'response': ""}}
    #     except Exception as e:
    #         if str(e) == 'Optional Action Not Implemented':
    #             return {'test_id': 5, 'name': 'AddAudioDecoderConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': 'Optional Action Not Implemented',
    #             'response': "", 'report': 'Optional Action Not Implemented' }}
    #         else:
    #             return {'test_id': 5, 'name': 'AddAudioDecoderConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': str(e), 'response': ""}}

    # def AddAudioEncoderConfiguration(self):
    #     try:
    #         token = self.media.GetProfiles()[0]._token
    #         create = self.media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
    #         sleep(1)
    #         token = self.media.GetProfiles()[-1]._token
    #         audio_token = self.media.GetProfiles()[0].AudioEncoderConfiguration._token
    #         add_config = self.media.AddAudioEncoderConfiguration({'ProfileToken': token, 'ConfigurationToken': audio_token})
    #         sleep(1)
    #         audio_token2 = self.media.GetProfiles()[-1].AudioEncoderConfiguration._token
    #         sleep(1)
    #         delete = self.media.DeleteProfile({'ProfileToken': token})
    #         if (audio_token != audio_token2):
    #             return {'test_id': 6, 'name': 'AddAudioEncoderConfiguration', 'service': 'Media',
    #             'result': {'supported': False,
    #             'extension': 'The DUT did not add new AddAudioEncoderConfiguration',
    #             'response': str(add_config)}}
    #         else:
    #             return {'test_id': 6, 'name': 'AddAudioEncoderConfiguration', 'service': 'Media',
    #             'result': {'supported': True, 'extension': None, 'response': str(add_config)}}
    #     except AttributeError:
    #         return {'test_id': 6, 'name': 'AddAudioEncoderConfiguration', 'service': 'Media',
    #         'result': {'supported': False,
    #         'extension': 'AddAudioEncoderConfiguration does not work, AttributeError',
    #         'response': "" }}
    #     except Exception as e:
    #         if str(e) == 'Optional Action Not Implemented':
    #             return {'test_id': 6, 'name': 'AddAudioEncoderConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': 'Optional Action Not Implemented',
    #             'response': "", 'report': 'Optional Action Not Implemented' }}
    #         else:
    #             return {'test_id': 6, 'name': 'AddAudioEncoderConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': str(e), 'response': ""}}

    # def AddAudioOutputConfiguration(self):
    #     try:
    #         token = self.media.GetProfiles()[0]._token
    #         create = self.media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
    #         sleep(1)
    #         token = self.media.GetProfiles()[-1]._token
    #         audio_token = self.media.GetProfiles()[0].AudioOutputConfiguration._token
    #         add_config = self.media.AddAudioOutputConfiguration({'ProfileToken': token, 'ConfigurationToken': audio_token})
    #         sleep(1)
    #         audio_token2 = self.media.GetProfiles()[-1].AudioOutputConfiguration._token
    #         sleep(1)
    #         delete = self.media.DeleteProfile({'ProfileToken': token})
    #         if (audio_token != audio_token2):
    #             return {'test_id': 7, 'name': 'AddAudioOutputConfiguration', 'service': 'Media',
    #             'result': {'supported': False,
    #             'extension': 'The DUT did not add new AddAudioOutputConfiguration',
    #             'response': str(add_config)}}
    #         else:
    #             return {'test_id': 7, 'name': 'AddAudioOutputConfiguration', 'service': 'Media',
    #             'result': {'supported': True, 'extension': None, 'response': str(add_config)}}
    #     except AttributeError:
    #         return {'test_id': 7, 'name': 'AddAudioOutputConfiguration', 'service': 'Media',
    #         'result': {'supported': False,
    #         'extension': 'AddAudioOutputConfiguration does not work, AttributeError',
    #         'response': "" }}
    #     except Exception as e:
    #         if str(e) == 'Optional Action Not Implemented':
    #             return {'test_id': 7, 'name': 'AddAudioOutputConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': 'Optional Action Not Implemented',
    #             'response': "", 'report': 'Optional Action Not Implemented' }}
    #         else:
    #             return {'test_id': 7, 'name': 'AddAudioOutputConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': str(e), 'response': ""}}

    # def AddAudioSourceConfiguration(self):
    #     try:
    #         token = self.media.GetProfiles()[0]._token
    #         create = self.media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
    #         sleep(1)
    #         token = self.media.GetProfiles()[-1]._token
    #         audio_token = self.media.GetProfiles()[0].AudioSourceConfiguration._token
    #         add_config = self.media.AddAudioSourceConfiguration({'ProfileToken': token, 'ConfigurationToken': audio_token})
    #         sleep(1)
    #         audio_token2 = self.media.GetProfiles()[-1].AudioSourceConfiguration._token
    #         sleep(1)
    #         delete = self.media.DeleteProfile({'ProfileToken': token})
    #         if (audio_token != audio_token2):
    #             return {'test_id': 8, 'name': 'AddAudioSourceConfiguration', 'service': 'Media',
    #             'result': {'supported': False,
    #             'extension': 'The DUT did not add new AddAudioSourceConfiguration',
    #             'response': str(add_config)}}
    #         else:
    #             return {'test_id': 8, 'name': 'AddAudioSourceConfiguration', 'service': 'Media',
    #             'result': {'supported': True, 'extension': None, 'response': str(add_config)}}
    #     except AttributeError:
    #         return {'test_id': 8, 'name': 'AddAudioSourceConfiguration', 'service': 'Media',
    #         'result': {'supported': False,
    #         'extension': 'AddAudioSourceConfiguration does not work, AttributeError',
    #         'response': "" }}
    #     except Exception as e:
    #         if str(e) == 'Optional Action Not Implemented':
    #             return {'test_id': 8, 'name': 'AddAudioSourceConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': 'Optional Action Not Implemented',
    #             'response': "", 'report': 'Optional Action Not Implemented' }}
    #         else:
    #             return {'test_id': 8, 'name': 'AddAudioSourceConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': str(e), 'response': ""}}

    # def AddMetadataConfiguration(self):
    #     try:
    #         token = self.media.GetProfiles()[0]._token
    #         create = self.media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
    #         sleep(1)
    #         token = self.media.GetProfiles()[-1]._token
    #         metadata_token = self.media.GetMetadataConfigurations()[0]._token
    #         add_config = self.media.AddMetadataConfiguration({'ProfileToken': token, 'ConfigurationToken': metadata_token})
    #         sleep(1)
    #         metadata_token2 = self.media.GetProfiles()[-1].MetadataConfiguration._token
    #         sleep(1)
    #         delete = self.media.DeleteProfile({'ProfileToken': token})
    #         if (metadata_token != metadata_token2):
    #             return {'test_id': 9, 'name': 'AddMetadataConfiguration', 'service': 'Media',
    #             'result': {'supported': False,
    #             'extension': 'The DUT did not add new AddMetadataConfiguration',
    #             'response': str(add_config)}}
    #         else:
    #             return {'test_id': 9, 'name': 'AddMetadataConfiguration', 'service': 'Media',
    #             'result': {'supported': True, 'extension': None, 'response': str(add_config)}}
    #     except AttributeError:
    #         return {'test_id': 9, 'name': 'AddMetadataConfiguration', 'service': 'Media',
    #         'result': {'supported': False,
    #         'extension': 'AddMetadataConfiguration does not work, AttributeError',
    #         'response': "" }}
    #     except Exception as e:
    #         if str(e) == 'Optional Action Not Implemented':
    #             return {'test_id': 9, 'name': 'AddMetadataConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': 'Optional Action Not Implemented',
    #             'response': "", 'report': 'Optional Action Not Implemented' }}
    #         else:
    #             return {'test_id': 9, 'name': 'AddMetadataConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': str(e), 'response': ""}}

    # def AddPTZConfiguration(self):
    #     try:
    #         token = self.media.GetProfiles()[0]._token
    #         create = self.media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
    #         sleep(1)
    #         token = self.media.GetProfiles()[-1]._token
    #         ptz_token = self.media.GetProfiles()[0].PTZConfiguration._token
    #         add_config = self.media.AddPTZConfiguration({'ProfileToken': token, 'ConfigurationToken': ptz_token})
    #         sleep(1)
    #         ptz_token2 = self.media.GetProfiles()[-1].PTZConfiguration._token
    #         sleep(1)
    #         delete = self.media.DeleteProfile({'ProfileToken': token})
    #         if (ptz_token != ptz_token2):
    #             return {'test_id': 10, 'name': 'AddPTZConfiguration', 'service': 'Media',
    #             'result': {'supported': False,
    #             'extension': 'The DUT did not add new AddPTZConfiguration',
    #             'response': str(add_config)}}
    #         else:
    #             return {'test_id': 10, 'name': 'AddPTZConfiguration', 'service': 'Media',
    #             'result': {'supported': True, 'extension': None, 'response': str(add_config)}}
    #     except AttributeError:
    #         return {'test_id': 10, 'name': 'AddPTZConfiguration', 'service': 'Media',
    #         'result': {'supported': False,
    #         'extension': 'AddPTZConfiguration does not work, AttributeError',
    #         'response': "" }}
    #     except Exception as e:
    #         if str(e) == 'Optional Action Not Implemented':
    #             return {'test_id': 10, 'name': 'AddPTZConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': 'Optional Action Not Implemented',
    #             'response': "", 'report': 'Optional Action Not Implemented' }}
    #         else:
    #             return {'test_id': 10, 'name': 'AddPTZConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': str(e), 'response': ""}}

    # def AddVideoAnalyticsConfiguration(self):
    #     try:
    #         token = self.media.GetProfiles()[0]._token
    #         create = self.media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
    #         sleep(1)
    #         token = self.media.GetProfiles()[-1]._token
    #         vid_token = self.media.GetProfiles()[0].VideoAnalyticsConfiguration._token
    #         add_config = self.media.AddVideoAnalyticsConfiguration({'ProfileToken': token, 'ConfigurationToken': vid_token})
    #         sleep(1)
    #         vid_token2 = self.media.GetProfiles()[-1].VideoAnalyticsConfiguration._token
    #         sleep(1)
    #         delete = self.media.DeleteProfile({'ProfileToken': token})
    #         if (vid_token != vid_token2):
    #             return {'test_id': 11, 'name': 'AddVideoAnalyticsConfiguration', 'service': 'Media',
    #             'result': {'supported': False,
    #             'extension': 'The DUT did not add new AddVideoAnalyticsConfiguration',
    #             'response': str(add_config)}}
    #         else:
    #             return {'test_id': 11, 'name': 'AddVideoAnalyticsConfiguration', 'service': 'Media',
    #             'result': {'supported': True, 'extension': None, 'response': str(add_config)}}
    #     except AttributeError:
    #         return {'test_id': 11, 'name': 'AddVideoAnalyticsConfiguration', 'service': 'Media',
    #         'result': {'supported': False,
    #         'extension': 'AddVideoAnalyticsConfiguration does not work, AttributeError',
    #         'response': "" }}
    #     except Exception as e:
    #         if str(e) == 'Optional Action Not Implemented':
    #             return {'test_id': 11, 'name': 'AddVideoAnalyticsConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': 'Optional Action Not Implemented',
    #             'response': "", 'report': 'Optional Action Not Implemented' }}
    #         else:
    #             return {'test_id': 11, 'name': 'AddVideoAnalyticsConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': str(e), 'response': ""}}

    # def AddVideoEncoderConfiguration(self):
    #     try:
    #         token = self.media.GetProfiles()[0]._token
    #         create = self.media.CreateProfile({'Name': 'Test', 'ProfileToken': token})
    #         sleep(1)
    #         token = self.media.GetProfiles()[-1]._token
    #         vid_token = self.media.GetProfiles()[0].VideoEncoderConfiguration._token
    #         add_config = self.media.AddVideoEncoderConfiguration({'ProfileToken': token, 'ConfigurationToken': vid_token})
    #         sleep(1)
    #         vid_token2 = self.media.GetProfiles()[-1].VideoEncoderConfiguration._token
    #         sleep(1)
    #         delete = self.media.DeleteProfile({'ProfileToken': token})
    #         if (vid_token != vid_token2):
    #             return {'test_id': 12, 'name': 'AddVideoEncoderConfiguration', 'service': 'Media',
    #             'result': {'supported': False,
    #             'extension': 'The DUT did not add new AddVideoEncoderConfiguration',
    #             'response': str(add_config)}}
    #         else:
    #             return {'test_id': 12, 'name': 'AddVideoEncoderConfiguration', 'service': 'Media',
    #             'result': {'supported': True, 'extension': None, 'response': str(add_config)}}
    #     except AttributeError:
    #         return {'test_id': 12, 'name': 'AddVideoEncoderConfiguration', 'service': 'Media',
    #         'result': {'supported': False,
    #         'extension': 'AddVideoSourceConfiguration does not work, AttributeError',
    #         'response': "" }}
    #     except Exception as e:
    #         if str(e) == 'Optional Action Not Implemented':
    #             return {'test_id': 12, 'name': 'AddVideoEncoderConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': 'Optional Action Not Implemented',
    #             'response': "", 'report': 'Optional Action Not Implemented' }}
    #         else:
    #             return {'test_id': 12, 'name': 'AddVideoEncoderConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': str(e), 'response': ""}}

    # def AddVideoSourceConfiguration(self):
    #     try:
    #         token0 = self.media.GetProfiles()[0]._token
    #         create = self.media.CreateProfile({'Name': 'Test', 'ProfileToken': token0})
    #         sleep(1)
    #         token = self.media.GetProfiles()[-1]._token
    #         source_token = self.media.GetProfiles()[0].VideoSourceConfiguration._token
    #         addvid = self.media.AddVideoSourceConfiguration({'ProfileToken': token, 'ConfigurationToken': source_token})
    #         sleep(1)
    #         source_token2 = self.media.GetProfiles()[-1].VideoSourceConfiguration._token
    #         sleep(1)
    #         delete = self.media.DeleteProfile({'ProfileToken': token})
    #         if (source_token != source_token2):
    #             return {'test_id': 13, 'name': 'AddVideoSourceConfiguration', 'service': 'Media',
    #             'result': {'supported': False,
    #             'extension': 'The DUT did not add new AddVideoSourceConfiguration',
    #             'response': str(addvid)}}
    #         else:
    #             return {'test_id': 13, 'name': 'AddVideoSourceConfiguration', 'service': 'Media',
    #             'result': {'supported': True, 'extension': None, 'response': str(addvid)}}
    #     except AttributeError:
    #         return {'test_id': 13, 'name': 'AddVideoSourceConfiguration', 'service': 'Media',
    #         'result': {'supported': False,
    #         'extension': 'AddVideoSourceConfiguration does not work, AttributeError',
    #         'response': "" }}
    #     except Exception as e:
    #         if str(e) == 'Optional Action Not Implemented':
    #             return {'test_id': 13, 'name': 'AddVideoSourceConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': 'Optional Action Not Implemented',
    #             'response': "", 'report': 'Optional Action Not Implemented' }}
    #         else:
    #             return {'test_id': 13, 'name': 'AddVideoSourceConfiguration', 'service': 'Media',
    #             'result': {'supported': False, 'extension': str(e), 'response': ""}}

    def GetVideoSourceConfiguration(self):
        try:
            config_token = self.media.GetProfiles()[0].VideoSourceConfiguration._token
            config = self.media.GetVideoSourceConfiguration({'ConfigurationToken': config_token})
            if ((config is None) or (len(config) == 0)):
                return {'test_id': 14, 'name': 'GetVideoSourceConfiguration', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetVideoSourceConfiguration settings',
                'extension': 'The DUT did not send GetVideoSourceConfigurationResponse message',
                'response': str(config), 'report': 'Not Supported'}}
            else:
                return {'test_id': 14, 'name': 'GetVideoSourceConfiguration', 'service': 'Media',
                'result': {'supported': True,
                'report_name': 'GetVideoSourceConfiguration settings',
                'extension': None, 'response': str(config), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 14, 'name': 'GetVideoSourceConfiguration', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetVideoSourceConfiguration settings',
            'extension': 'GetVideoSourceConfiguration does not work, AttributeError',
            'response': "", 'report': 'Not Supported' }}
        except IndexError:
            return {'test_id': 14, 'name': 'GetVideoSourceConfiguration', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetVideoSourceConfiguration settings',
            'extension': 'GetVideoSourceConfiguration may be working, but there is no VideoSourceConfigurations availible',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 14, 'name': 'GetVideoSourceConfiguration', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetVideoSourceConfiguration settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 14, 'name': 'GetVideoSourceConfiguration', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetVideoSourceConfiguration settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioOutputConfigurations(self):
        try:
            configs = self.media.GetAudioOutputConfigurations()
            token = configs[0]._token
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 15, 'name': 'GetAudioOutputConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioOutputConfigurations settings',
                'extension': 'The DUT did not send GetAudioOutputConfigurationsResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 15, 'name': 'GetAudioOutputConfigurations', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetAudioOutputConfigurations settings',
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 15, 'name': 'GetAudioOutputConfigurations', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioOutputConfigurations settings',
            'extension': 'GetAudioOutputConfigurations does not work, AttributeError',
            'response': "", 'report': 'Not Supported' }}
        except IndexError:
            return {'test_id': 15, 'name': 'GetAudioOutputConfigurations', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioOutputConfigurations settings',
            'extension': 'GetAudioOutputConfigurations may be working, but there is no AudioOutputConfigurations availible',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 15, 'name': 'GetAudioOutputConfigurations', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioOutputConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 15, 'name': 'GetAudioOutputConfigurations', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioOutputConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioDecoderConfigurations(self):
        try:
            configs = self.media.GetAudioDecoderConfigurations()
            token = configs[0]._token
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 16, 'name': 'GetAudioDecoderConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioDecoderConfigurations settings',
                'extension': 'The DUT did not send GetAudioDecoderConfigurationsResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 16, 'name': 'GetAudioDecoderConfigurations', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetAudioDecoderConfigurations settings',
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 16, 'name': 'GetAudioDecoderConfigurations', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioDecoderConfigurations settings',
            'extension': 'GetAudioDecoderConfigurations does not work, AttributeError',
            'response': "", 'report': 'Not Supported' }}
        except IndexError:
            return {'test_id': 16, 'name': 'GetAudioDecoderConfigurations', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioDecoderConfigurations settings',
            'extension': 'GetAudioDecoderConfigurations may be working, but there is no AudioDecoderConfigurations availible',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 16, 'name': 'GetAudioDecoderConfigurations', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioDecoderConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 16, 'name': 'GetAudioDecoderConfigurations', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioDecoderConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioDecoderConfigurationOptions(self):
        try:
            token = self.media.GetProfiles()[0]._token
            config_token = self.media.GetAudioDecoderConfigurations()[0]._token
            options = self.media.GetAudioDecoderConfigurationOptions({'ConfigurationToken': config_token, 'ProfileToken': token})
            if ((options is None) or (len(options) == 0)):
                return {'test_id': 17, 'name': 'GetAudioDecoderConfigurationOptions', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioDecoderConfigurationOptions settings',
                'extension': 'The DUT did not send GetAudioDecoderConfigurationOptionsResponse message',
                'response': str(options), 'report': 'Not Supported'}}
            else:
                return {'test_id': 17, 'name': 'GetAudioDecoderConfigurationOptions', 'service': 'Media',
                'result': {'supported': True,
                'report_name': 'GetAudioDecoderConfigurationOptions settings',
                'extension': None, 'response': str(options), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 17, 'name': 'GetAudioDecoderConfigurationOptions', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioDecoderConfigurationOptions settings',
            'extension': 'GetAudioDecoderConfigurationOptions does not work, AttributeError',
            'response': "", 'report': 'Not Supported' }}
        except IndexError:
            return {'test_id': 17, 'name': 'GetAudioDecoderConfigurationOptions', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioDecoderConfigurationOptions settings',
            'extension': 'GetAudioDecoderConfigurationOptions may be working, but there is no AudioDecoderConfigurations availible',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 17, 'name': 'GetAudioDecoderConfigurationOptions', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioDecoderConfigurationOptions settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 17, 'name': 'GetAudioDecoderConfigurationOptions', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioDecoderConfigurationOptions settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioDecoderConfiguration(self):
        try:
            config_token = self.media.GetAudioDecoderConfigurations()[0]._token
            config = self.media.GetAudioDecoderConfiguration({'ConfigurationToken': config_token})
            if ((config is None) or (len(config) == 0)):
                return {'test_id': 18, 'name': 'GetAudioDecoderConfiguration', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioDecoderConfiguration settings',
                'extension': 'The DUT did not send GetAudioDecoderConfigurationResponse message',
                'response': str(config), 'report': 'Not Supported'}}
            else:
                return {'test_id': 18, 'name': 'GetAudioDecoderConfiguration', 'service': 'Media',
                'result': {'supported': True,
                'report_name': 'GetAudioDecoderConfiguration settings',
                'extension': None, 'response': str(config), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 18, 'name': 'GetAudioDecoderConfiguration', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioDecoderConfiguration settings',
            'extension': 'GetAudioDecoderConfiguration does not work, AttributeError',
            'response': "", 'report': 'Not Supported' }}
        except IndexError:
            return {'test_id': 18, 'name': 'GetAudioDecoderConfiguration', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioDecoderConfiguration settings',
            'extension': 'GetAudioDecoderConfiguration may be working, but there is no AudioDecoderConfigurations availible',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 18, 'name': 'GetAudioDecoderConfiguration', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioDecoderConfiguration settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 18, 'name': 'GetAudioDecoderConfiguration', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioDecoderConfiguration settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioEncoderConfigurations(self):
        try:
            configs = self.media.GetAudioEncoderConfigurations()
            token = configs[0]._token
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 19, 'name': 'GetAudioEncoderConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioEncoderConfigurations settings',
                'extension': 'The DUT did not send GetAudioEncoderConfigurationsResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 19, 'name': 'GetAudioEncoderConfigurations', 'service': 'Media',
                'result': {'supported': True,
                'report_name': 'GetAudioEncoderConfigurations settings',
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 19, 'name': 'GetAudioEncoderConfigurations', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioEncoderConfigurations settings',
            'extension': 'GetAudioEncoderConfigurations does not work, AttributeError',
            'response': "", 'report': 'Not Supported' }}
        except IndexError:
            return {'test_id': 19, 'name': 'GetAudioEncoderConfigurations', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioEncoderConfigurations settings',
            'extension': 'GetAudioEncoderConfigurations may be working, but there is no AudioEncoderConfigurations availible',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 19, 'name': 'GetAudioEncoderConfigurations', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioEncoderConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 19, 'name': 'GetAudioEncoderConfigurations', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioEncoderConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioEncoderConfigurationOptions(self):
        try:
            def handleBrackets(string):
                return str(string)[str(string).find('[') + 1:str(string).find(']')]

            report = "Avaliable Audio encodings:\n"
            aCodecs = []
            token = self.media.GetProfiles()[0]._token
            config_token = self.media.GetAudioEncoderConfigurations()[0]._token
            options = self.media.GetAudioEncoderConfigurationOptions({'ConfigurationToken': config_token, 'ProfileToken': token})
            if ((options is None) or (len(options) == 0)):
                return {'test_id': 20, 'name': 'GetAudioEncoderConfigurationOptions', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'Audio encoders',
                'extension': 'The DUT did not send GetAudioEncoderConfigurationOptionsResponse message',
                'response': str(options), 'report': 'Device did not send GetAudioEncoderConfigurationOptionsResponse message'}}
            else:
                for encoder in options.Options:
                    aCodecs.append({'Encoding': encoder.Encoding, 'BitrateList': encoder.BitrateList.Items,
                                    'SampleRateList': encoder.SampleRateList.Items})
                for codec in aCodecs:
                    report = report + codec['Encoding'] + ', Avaliable bitrate(kbps): {}\n'.format(handleBrackets(codec['BitrateList'])) + 'Avaliable sample rate(kHz): {}\n'.format(handleBrackets(codec['SampleRateList']))                
                return {'test_id': 20, 'name': 'GetAudioEncoderConfigurationOptions', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'Audio encoders',
                'extension': None, 'response': str(options),
                'report': report }}
        except AttributeError:
            return {'test_id': 20, 'name': 'GetAudioEncoderConfigurationOptions', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'Audio encoders',
            'extension': 'GetAudioEncoderConfigurationOptions does not work, AttributeError',
            'response': "", 'report': 'Not Supported' }}
        except IndexError:
            return {'test_id': 20, 'name': 'GetAudioEncoderConfigurationOptions', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'Audio encoders',
            'extension': 'GetAudioEncoderConfigurationOptions may be working, but there is no AudioEncoderConfigurations availible',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 20, 'name': 'GetAudioEncoderConfigurationOptions', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'Audio encoders', 'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 20, 'name': 'GetAudioEncoderConfigurationOptions', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'Audio encoders',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioEncoderConfiguration(self):
        try:
            config_token = self.media.GetAudioEncoderConfigurations()[0]._token
            config = self.media.GetAudioEncoderConfiguration({'ConfigurationToken': config_token})
            if ((config is None) or (len(config) == 0)):
                return {'test_id': 21, 'name': 'GetAudioEncoderConfiguration', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioEncoderConfiguration settings',
                'extension': 'The DUT did not send GetAudioEncoderConfigurationResponse message',
                'response': str(config), 'report': 'Not Supported'}}
            else:
                return {'test_id': 21, 'name': 'GetAudioEncoderConfiguration', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetAudioEncoderConfiguration settings',
                'extension': None, 'response': str(config), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 21, 'name': 'GetAudioEncoderConfiguration', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioEncoderConfiguration settings',
            'extension': 'GetAudioEncoderConfiguration does not work, AttributeError',
            'response': "", 'report': 'Not Supported' }}
        except IndexError:
            return {'test_id': 21, 'name': 'GetAudioEncoderConfiguration', 'service': 'Media',
            'result': {'supported': False,  'report_name': 'GetAudioEncoderConfiguration settings',
            'extension': 'GetAudioEncoderConfiguration may be working, but there is no AudioEncoderConfigurations availible',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 21, 'name': 'GetAudioEncoderConfiguration', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioEncoderConfiguration settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 21, 'name': 'GetAudioEncoderConfiguration', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioEncoderConfiguration settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioOutputConfigurations(self):
        try:
            configs = self.media.GetAudioOutputConfigurations()
            token = configs[0]._token
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 22, 'name': 'GetAudioOutputConfigurations', 'service': 'Media',
                'result': {'supported': False,  'report_name': 'GetAudioOutputConfigurations settings',
                'extension': 'The DUT did not send GetAudioOutputConfigurationsResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 22, 'name': 'GetAudioOutputConfigurations', 'service': 'Media',
                'result': {'supported': True,
                'report_name': 'GetAudioOutputConfigurations settings',
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 22, 'name': 'GetAudioOutputConfigurations', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioOutputConfigurations settings',
            'extension': 'GetAudioOutputConfigurations does not work, AttributeError',
            'response': "", 'report': 'Not Supported' }}
        except IndexError:
            return {'test_id': 22, 'name': 'GetAudioOutputConfigurations', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioOutputConfigurations settings',
            'extension': 'GetAudioOutputConfigurations may be working, but there is no AudioOutputConfigurations availible',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 22, 'name': 'GetAudioOutputConfigurations', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioOutputConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 22, 'name': 'GetAudioOutputConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioOutputConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioOutputConfigurationOptions(self):
        try:
            token = self.media.GetProfiles()[0]._token
            config_token = self.media.GetAudioOutputConfigurations()[0]._token
            options = self.media.GetAudioOutputConfigurationOptions({'ConfigurationToken': config_token, 'ProfileToken': token})
            if ((options is None) or (len(options) == 0)):
                return {'test_id': 23, 'name': 'GetAudioOutputConfigurationOptions', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioOutputConfigurationOptions settings',
                'extension': 'The DUT did not send GetAudioOutputConfigurationOptionsResponse message',
                'response': str(options), 'report': 'Not Supported'}}
            else:
                return {'test_id': 23, 'name': 'GetAudioOutputConfigurationOptions', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetAudioOutputConfigurationOptions settings',
                'extension': None, 'response': str(options), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 23, 'name': 'GetAudioOutputConfigurationOptions', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioOutputConfigurationOptions settings',
            'extension': 'GetAudioOutputConfigurationOptions does not work, AttributeError',
            'response': "", 'report': 'Not Supported' }}
        except IndexError:
            return {'test_id': 23, 'name': 'GetAudioOutputConfigurationOptions', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioOutputConfigurationOptions settings',
            'extension': 'GetAudioOutputConfigurationOptions may be working, but there is no AudioOutputConfigurations availible',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 23, 'name': 'GetAudioOutputConfigurationOptions', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioOutputConfigurationOptions settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 23, 'name': 'GetAudioOutputConfigurationOptions', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioOutputConfigurationOptions settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioOutputConfiguration(self):
        try:
            config_token = self.media.GetAudioOutputConfigurations()[0]._token
            config = self.media.GetAudioOutputConfiguration({'ConfigurationToken': config_token})
            if ((config is None) or (len(config) == 0)):
                return {'test_id': 24, 'name': 'GetAudioOutputConfiguration', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioOutputConfiguration settings',
                'extension': 'The DUT did not send GetAudioOutputConfigurationResponse message',
                'response': str(config), 'report': 'Not Supported'}}
            else:
                return {'test_id': 24, 'name': 'GetAudioOutputConfiguration', 'service': 'Media',
                'result': {'supported': True,
                'report_name': 'GetAudioOutputConfiguration settings',
                'extension': None, 'response': str(config), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 24, 'name': 'GetAudioOutputConfiguration', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioOutputConfiguration settings',
            'extension': 'GetAudioOutputConfiguration does not work',
            'response': "", 'report': 'Not Supported' }}
        except IndexError:
            return {'test_id': 24, 'name': 'GetAudioOutputConfiguration', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioOutputConfiguration settings',
            'extension': 'GetAudioOutputConfiguration may be working, but there is no AudioOutputConfigurations availible',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 24, 'name': 'GetAudioOutputConfiguration', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioOutputConfiguration settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 24, 'name': 'GetAudioOutputConfiguration', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioOutputConfiguration settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioOutputs(self):
        try:
            outputs = self.media.GetAudioOutputs()
            token = outputs[0]._token
            if ((outputs is None) or (len(outputs) == 0)):
                return {'test_id': 25, 'name': 'GetAudioOutputs', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioOutputs settings',
                'extension': 'The DUT did not send GetAudioOutputsResponse message',
                'response': str(outputs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 25, 'name': 'GetAudioOutputs', 'service': 'Media',
                'result': {'supported': True,
                'report_name': 'GetAudioOutputs settings',
                'extension': None, 'response': str(outputs), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 25, 'name': 'GetAudioOutputs', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioOutputs settings',
            'extension': 'The DUT did send GetAudioOutputsResponse message. The DUT scope list does not have one or more mandatory scope entry.',
            'response': "", 'report': 'Not Supported' }}
        except IndexError:
            return {'test_id': 25, 'name': 'GetAudioOutputs', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioOutputs settings',
            'extension': 'The DUT did send GetAudioOutputsResponse message, The DUT scope list does not have one or more mandatory scope entry.',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 25, 'name': 'GetAudioOutputs', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioOutputs settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 25, 'name': 'GetAudioOutputs', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioOutputs settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioSourceConfiguration(self):
        try:
            audio_token = self.media.GetProfiles()[0].AudioSourceConfiguration._token
            configs = self.media.GetAudioSourceConfiguration({'ConfigurationToken': audio_token})
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 26, 'name': 'GetAudioSourceConfiguration', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioSourceConfiguration settings',
                'extension': 'The DUT did not send GetAudioSourceConfigurationResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 26, 'name': 'GetAudioSourceConfiguration', 'service': 'Media',
                'result': {'supported': True,
                'report_name': 'GetAudioSourceConfiguration settings',
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 26, 'name': 'GetAudioSourceConfiguration', 'service': 'Media',
            'result': {'supported': False,  'report_name': 'GetAudioSourceConfiguration settings',
            'extension': 'The DUT scope list does not have one or more mandatory scope entry.',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 26, 'name': 'GetAudioSourceConfiguration', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioSourceConfiguration settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 26, 'name': 'GetAudioSourceConfiguration', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioSourceConfiguration settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioSourceConfigurationOptions(self):
        try:
            audio_token = self.media.GetProfiles()[0].AudioSourceConfiguration._token
            configs = self.media.GetAudioSourceConfigurationOptions({'ConfigurationToken': audio_token})
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 27, 'name': 'GetAudioSourceConfigurationOptions', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioSourceConfigurationOptions settings',
                'extension': 'The DUT did not send GetAudioSourceConfigurationOptionsResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 27, 'name': 'GetAudioSourceConfigurationOptions', 'service': 'Media',
                'result': {'supported': True,
                'report_name': 'GetAudioSourceConfigurationOptions settings',
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 27, 'name': 'GetAudioSourceConfigurationOptions', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioSourceConfigurationOptions settings',
            'extension': 'The DUT scope list does not have one or more mandatory scope entry.',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 27, 'name': 'GetAudioSourceConfigurationOptions', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioSourceConfigurationOptions settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 27, 'name': 'GetAudioSourceConfigurationOptions', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioSourceConfigurationOptions settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioSourceConfigurations(self):
        try:
            configs = self.media.GetAudioSourceConfigurations()
            if configs is None or len(configs) == 0:
                return {'test_id': 28, 'name': 'GetAudioSourceConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioSourceConfigurations settings',
                'extension': 'The DUT did not send GetAudioSourceConfigurationsResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 28, 'name': 'GetAudioSourceConfigurations', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetAudioSourceConfigurations settings',
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 28, 'name': 'GetAudioSourceConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioSourceConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 28, 'name': 'GetAudioSourceConfigurations', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioSourceConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetAudioSources(self):
        try:
            sources = self.media.GetAudioSources()
            token = sources[0]._token
            if ((sources is None) or (len(sources) == 0)):
                return {'test_id': 29, 'name': 'GetAudioSources', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetAudioSources settings',
                'extension': 'The DUT did not send GetAudioSourcesResponse message',
                'response': str(sources), 'report': 'Not Supported'}}
            else:
                return {'test_id': 29, 'name': 'GetAudioSources', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetAudioSources settings',
                'extension': None, 'response': str(sources), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 29, 'name': 'GetAudioSources', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioSources settings',
            'extension': 'The DUT did send GetAudioSourcesResponse message. The DUT scope list does not have one or more mandatory scope entry.',
            'response': "", 'report': 'Not Supported' }}
        except IndexError:
            return {'test_id': 29, 'name': 'GetAudioSources', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetAudioSources settings',
            'extension': 'The DUT did send GetAudioSourcesResponse message, The DUT scope list does not have one or more mandatory scope entry.',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 29, 'name': 'GetAudioSources', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioSources settings',
                'extension': 'Optional Action Not Implemented', 
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 29, 'name': 'GetAudioSources', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetAudioSources settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetCompatibleAudioDecoderConfigurations(self):
        try:
            token = self.media.GetProfiles()[0]._token
            sources = self.media.GetCompatibleAudioDecoderConfigurations({'ProfileToken': token})
            if ((sources is None) or (len(sources) == 0)):
                return {'test_id': 30, 'name': 'GetCompatibleAudioDecoderConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleAudioDecoderConfigurations settings',
                'extension': 'The DUT did not send GetCompatibleAudioDecoderConfigurationsResponse message',
                'response': str(sources), 'report': 'Not Supported'}}
            else:
                return {'test_id': 30, 'name': 'GetCompatibleAudioDecoderConfigurations', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetCompatibleAudioDecoderConfigurations settings',
                'extension': None, 'response': str(sources), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 30, 'name': 'GetCompatibleAudioDecoderConfigurations', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetCompatibleAudioDecoderConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 30, 'name': 'GetCompatibleAudioDecoderConfigurations', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetCompatibleAudioDecoderConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetCompatibleAudioOutputConfigurations(self):
        try:
            token = self.media.GetProfiles()[0]._token
            sources = self.media.GetCompatibleAudioOutputConfigurations({'ProfileToken': token})
            if ((sources is None) or (len(sources) == 0)):
                return {'test_id': 31, 'name': 'GetCompatibleAudioOutputConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleAudioOutputConfigurations settings',
                'extension': 'The DUT did not send GetCompatibleAudioOutputConfigurationsResponse message',
                'response': str(sources), 'report': 'Not Supported'}}
            else:
                return {'test_id': 31, 'name': 'GetCompatibleAudioOutputConfigurations', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetCompatibleAudioOutputConfigurations settings',
                'extension': None, 'response': str(sources), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 31, 'name': 'GetCompatibleAudioOutputConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleAudioOutputConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 31, 'name': 'GetCompatibleAudioOutputConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleAudioOutputConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetCompatibleAudioSourceConfigurations(self):
        try:
            token = self.media.GetProfiles()[0]._token
            sources = self.media.GetCompatibleAudioSourceConfigurations({'ProfileToken': token})
            if ((sources is None) or (len(sources) == 0)):
                return {'test_id': 32, 'name': 'GetCompatibleAudioSourceConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleAudioSourceConfigurations settings',
                'extension': 'The DUT did not send GetCompatibleAudioSourceConfigurationsResponse message',
                'response': str(sources), 'report': 'Not Supported'}}
            else:
                return {'test_id': 32, 'name': 'GetCompatibleAudioSourceConfigurations', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetCompatibleAudioSourceConfigurations settings',
                'extension': None, 'response': str(sources), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 32, 'name': 'GetCompatibleAudioSourceConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleAudioSourceConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 32, 'name': 'GetCompatibleAudioSourceConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleAudioSourceConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetCompatibleMetadataConfigurations(self):
        try:
            token = self.media.GetProfiles()[0]._token
            sources = self.media.GetCompatibleMetadataConfigurations({'ProfileToken': token})
            if ((sources is None) or (len(sources) == 0)):
                return {'test_id': 33, 'name': 'GetCompatibleMetadataConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleMetadataConfigurations settings',
                'extension': 'The DUT did not send GetCompatibleMetadataConfigurationsResponse message',
                'response': str(sources), 'report': 'Not Supported'}}
            else:
                return {'test_id': 33, 'name': 'GetCompatibleMetadataConfigurations', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetCompatibleMetadataConfigurations settings',
                'extension': None, 'response': str(sources), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 33, 'name': 'GetCompatibleMetadataConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleMetadataConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 33, 'name': 'GetCompatibleMetadataConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleMetadataConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetCompatibleVideoAnalyticsConfigurations(self):
        try:
            token = self.media.GetProfiles()[0]._token
            sources = self.media.GetCompatibleVideoAnalyticsConfigurations({'ProfileToken': token})
            if ((sources is None) or (len(sources) == 0)):
                return {'test_id': 34, 'name': 'GetCompatibleVideoAnalyticsConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleVideoAnalyticsConfigurations settings',
                'extension': 'The DUT did not send GetCompatibleVideoAnalyticsConfigurationsResponse message',
                'response': str(sources), 'report': 'Not Supported'}}
            else:
                return {'test_id': 34, 'name': 'GetCompatibleVideoAnalyticsConfigurations', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetCompatibleVideoAnalyticsConfigurations settings',
                'extension': None, 'response': str(sources), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 34, 'name': 'GetCompatibleVideoAnalyticsConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleVideoAnalyticsConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 34, 'name': 'GetCompatibleVideoAnalyticsConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleVideoAnalyticsConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetCompatibleVideoEncoderConfigurations(self):
        try:
            token = self.media.GetProfiles()[0]._token
            sources = self.media.GetCompatibleVideoEncoderConfigurations({'ProfileToken': token})
            if ((sources is None) or (len(sources) == 0)):
                return {'test_id': 35, 'name': 'GetCompatibleVideoEncoderConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleVideoEncoderConfigurations settings',
                'extension': 'The DUT did not send GetCompatibleVideoEncoderConfigurationsResponse message',
                'response': str(sources), 'report': 'Not Supported'}}
            else:
                return {'test_id': 35, 'name': 'GetCompatibleVideoEncoderConfigurations', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetCompatibleVideoEncoderConfigurations settings',
                'extension': None, 'response': str(sources), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 35, 'name': 'GetCompatibleVideoEncoderConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleVideoEncoderConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 35, 'name': 'GetCompatibleVideoEncoderConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleVideoEncoderConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetCompatibleVideoSourceConfigurations(self):
        try:
            token = self.media.GetProfiles()[0]._token
            sources = self.media.GetCompatibleVideoSourceConfigurations({'ProfileToken': token})
            if ((sources is None) or (len(sources) == 0)):
                return {'test_id': 36, 'name': 'GetCompatibleVideoSourceConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleVideoSourceConfigurations settings',
                'extension': 'The DUT did not send GetCompatibleVideoSourceConfigurationsResponse message',
                'response': str(sources), 'report': 'Not Supported'}}
            else:
                return {'test_id': 36, 'name': 'GetCompatibleVideoSourceConfigurations', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetCompatibleVideoSourceConfigurations settings',
                'extension': None, 'response': str(sources), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 36, 'name': 'GetCompatibleVideoSourceConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleVideoSourceConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 36, 'name': 'GetCompatibleVideoSourceConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetCompatibleVideoSourceConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetGuaranteedNumberOfVideoEncoderInstances(self):
        try:
            config_token = self.media.GetProfiles()[0].VideoSourceConfiguration._token
            configs = self.media.GetGuaranteedNumberOfVideoEncoderInstances({'ConfigurationToken': config_token})
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 37, 'name': 'GetGuaranteedNumberOfVideoEncoderInstances', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetGuaranteedNumberOfVideoEncoderInstances settings',
                'extension': 'The DUT did not send GetGuaranteedNumberOfVideoEncoderInstancesResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 37, 'name': 'GetGuaranteedNumberOfVideoEncoderInstances', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetGuaranteedNumberOfVideoEncoderInstances settings', 
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 37, 'name': 'GetGuaranteedNumberOfVideoEncoderInstances', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetGuaranteedNumberOfVideoEncoderInstances settings',
            'extension': 'The DUT did send GetGuaranteedNumberOfVideoEncoderInstancesResponse message. The DUT scope list does not have one or more mandatory scope entry.',
            'response': "", 'report': 'Not Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 37, 'name': 'GetGuaranteedNumberOfVideoEncoderInstances', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetGuaranteedNumberOfVideoEncoderInstances settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 37, 'name': 'GetGuaranteedNumberOfVideoEncoderInstances', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetGuaranteedNumberOfVideoEncoderInstances settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetMetadataConfiguration(self):
        try:
            metadata_token = self.media.GetMetadataConfigurations()[0]._token
            configs = self.media.GetMetadataConfiguration({'ConfigurationToken': metadata_token})
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 38, 'name': 'GetMetadataConfiguration', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetMetadataConfiguration settings',
                'extension': 'The DUT did not send GetMetadataConfigurationResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 38, 'name': 'GetMetadataConfiguration', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetMetadataConfiguration settings',
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 38, 'name': 'GetMetadataConfiguration', 'service': 'Media',
            'result': {'supported': False, 'report_name': 'GetMetadataConfiguration settings',
            'extension': 'The DUT did send GetMetadataConfiguration message. The DUT scope list does not have one or more mandatory scope entry.',
            'response': "", 'report': 'Not Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 38, 'name': 'GetMetadataConfiguration', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetMetadataConfiguration settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 38, 'name': 'GetMetadataConfiguration', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetMetadataConfiguration settings',
                'extension': str(e),
                'response': "", 'report': 'Not Supported' }}

    def GetMetadataConfigurationOptions(self):
        try:
            metadata_token = self.media.GetMetadataConfigurations()[0]._token
            configs = self.media.GetMetadataConfigurationOptions({'ConfigurationToken': metadata_token})
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 39, 'name': 'GetMetadataConfigurationOptions', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetMetadataConfigurationOptions settings',
                'extension': 'The DUT did not send GetMetadataConfigurationOptionsResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 39, 'name': 'GetMetadataConfigurationOptions', 'service': 'Media',
                'result': {'supported': True,  'report_name': 'GetMetadataConfigurationOptions settings',
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except AttributeError:
            return {'test_id': 39, 'name': 'GetMetadataConfigurationOptions', 'service': 'Media',
            'result': {'supported': False,  'report_name': 'GetMetadataConfigurationOptions settings',
            'extension': 'The DUT did send GetMetadataConfiguration message. The DUT scope list does not have one or more mandatory scope entry.',
            'response': "", 'report': 'Not Supported' }}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 39, 'name': 'GetMetadataConfigurationOptions', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetMetadataConfigurationOptions settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 39, 'name': 'GetMetadataConfigurationOptions', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetMetadataConfigurationOptions settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetMetadataConfigurations(self):
        try:
            configs = self.media.GetMetadataConfigurations()
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 40, 'name': 'GetMetadataConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetMetadataConfigurations settings',
                'extension': 'The DUT did not send GetMetadataConfigurationsResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 40, 'name': 'GetMetadataConfigurations', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetMetadataConfigurations settings',
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 40, 'name': 'GetMetadataConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetMetadataConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 40, 'name': 'GetMetadataConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetMetadataConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetOSDs(self):
        try:
            source_token = self.media.GetProfiles()[0].VideoSourceConfiguration._token
            osds = self.media.GetOSDs({'ConfigurationToken': source_token})
            if ((osds is None) or (len(osds) == 0)):
                return {'test_id': 41, 'name': 'GetOSDs', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'OSDs settings',
                'extension': 'The DUT did not send GetOSDsResponse message',
                'response': str(osds), 'report': 'Not Supported'}}
            else:
                return {'test_id': 41, 'name': 'GetOSDs', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'OSDs settings',
                'extension': None, 'response': str(osds), 'report': 'OSD is supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 41, 'name': 'GetOSDs', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'OSDs settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 41, 'name': 'GetOSDs', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'OSDs settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetOSD(self):
        try:
            source_token = self.media.GetProfiles()[0].VideoSourceConfiguration._token
            osd_token = self.media.GetOSDs({'ConfigurationToken': source_token})[0]._token
            osd = self.media.GetOSD({'OSDToken': osd_token})
            if ((osd is None) or (len(osd) == 0)):
                return {'test_id': 42, 'name': 'GetOSD', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetOSD settings',
                'extension': 'The DUT did not send GetOSDResponse message',
                'response': str(osd), 'report': 'Not Supported'}}
            else:
                return {'test_id': 42, 'name': 'GetOSD', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetOSD settings',
                'extension': None, 'response': str(osd), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 42, 'name': 'GetOSD', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetOSD settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 42, 'name': 'GetOSD', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetOSD settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetOSDOptions(self):
        try:
            source_token = self.media.GetProfiles()[0].VideoSourceConfiguration._token
            options = self.media.GetOSDOptions({'ConfigurationToken': source_token})
            if ((options is None) or (options == [])):
                return {'test_id': 43, 'name': 'GetOSDOptions', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetOSDOptions settings',
                'extension': 'The DUT did not send GetOSDOptionsResponse message',
                'response': str(options), 'report': 'Not Supported'}}
            else:
                return {'test_id': 43, 'name': 'GetOSDOptions', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetOSDOptions settings',
                'extension': None, 'response': str(options), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 43, 'name': 'GetOSDOptions', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetOSDOptions settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 43, 'name': 'GetOSDOptions', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetOSDOptions settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetProfile(self):
        try:
            token = self.media.GetProfiles()[0]._token
            profile = self.media.GetProfile({'ProfileToken': token})
            if ((profile is None) or (len(profile) == 0)):
                return {'test_id': 44, 'name': 'GetProfile', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetProfile settings',
                'extension': 'The DUT did not send GetProfileResponse message',
                'response': str(profile), 'report': 'Not Supported'}}
            else:
                return {'test_id': 44, 'name': 'GetProfile', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetProfile settings',
                'extension': None, 'response': str(profile), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 44, 'name': 'GetProfile', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetProfile settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 44, 'name': 'GetProfile', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetProfile settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetServiceCapabilities(self):
        try:
            capabilities = self.media.GetServiceCapabilities()
            if ((capabilities is None) or (len(capabilities) == 0)):
                return {'test_id': 45, 'name': 'GetServiceCapabilities', 'service': 'Media',
                        'result': {'supported': False, 'report_name': 'Media Service capabilities',
                        'extension': 'The DUT did not send GetServiceCapabilitiesResponse message',
                        'response': str(capabilities), 'report': 'Not Supported'}}
            else:
                return {'test_id': 45, 'name': 'GetServiceCapabilities', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'Media Service capabilities',
                'extension': None, 'response': str(capabilities), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 45, 'name': 'GetServiceCapabilities', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'Media Service capabilities',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 45, 'name': 'GetServiceCapabilities', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'Media Service capabilities',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}

    def GetStreamUri(self):
        try:
            report = 'RTSP Stream URI is:\n'
            token = self.media.GetProfiles()[0]._token
            uri =  self.media.GetStreamUri({'StreamSetup': {'Stream': 'RTP_unicast', 'Transport' : {'Protocol': 'UDP'}} , 'ProfileToken': token})
            report += uri.Uri
            if ((uri is None) or (len(uri) == 0)):
                return {'test_id': 46, 'name': 'GetStreamUri', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'RTSP Stream URI',
                'extension': 'The DUT did not send GetStreamUriResponse message',
                'response': str(uri), 'report': 'Not Supported'}}
            else:
                return {'test_id': 46, 'name': 'GetStreamUri', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'RTSP Stream URI',
                'extension': None, 'response': str(uri), 'report': report}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 46, 'name': 'GetStreamUri', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'RTSP Stream URI',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 46, 'name': 'GetStreamUri', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'RTSP Stream URI',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetVideoAnalyticsConfiguration(self):
        try:
            vid_token = self.media.GetProfiles()[0].VideoAnalyticsConfiguration._token
            configs = self.media.GetVideoAnalyticsConfiguration({'ConfigurationToken': vid_token})
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 47, 'name': 'GetVideoAnalyticsConfiguration', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoAnalyticsConfiguration settings',
                'extension': 'The DUT did not send GetVideoAnalyticsConfigurationResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 47, 'name': 'GetVideoAnalyticsConfiguration', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetVideoAnalyticsConfiguration settings',
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 47, 'name': 'GetVideoAnalyticsConfiguration', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetVideoAnalyticsConfiguration settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 47, 'name': 'GetVideoAnalyticsConfiguration', 'service': 'Media',
                'result': {'supported': False,
                'report_name': 'GetVideoAnalyticsConfiguration settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetVideoAnalyticsConfigurations(self):
        try:
            configs = self.media.GetVideoAnalyticsConfigurations()
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 48, 'name': 'GetVideoAnalyticsConfigurations', 'service': 'Media',
                        'result': {'supported': False, 'report_name': 'GetVideoAnalyticsConfigurations settings',
                        'extension': 'The DUT did not send GetVideoAnalyticsConfigurationsResponse message',
                        'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 48, 'name': 'GetVideoAnalyticsConfigurations', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetVideoAnalyticsConfigurations settings',
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 48, 'name': 'GetVideoAnalyticsConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoAnalyticsConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 48, 'name': 'GetVideoAnalyticsConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoAnalyticsConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetVideoEncoderConfiguration(self):
        try:
            enc_token = self.media.GetProfiles()[0].VideoEncoderConfiguration._token
            configs = self.media.GetVideoEncoderConfiguration({'ConfigurationToken': enc_token})
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 49, 'name': 'GetVideoEncoderConfiguration', 'service': 'Media',
                        'result': {'supported': False, 'report_name': 'GetVideoEncoderConfiguration settings',
                        'extension': 'The DUT did not send GetVideoEncoderConfigurationResponse message',
                        'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 49, 'name': 'GetVideoEncoderConfiguration', 'service': 'Media',
                        'result': {'supported': True, 'report_name': 'GetVideoEncoderConfiguration settings',
                        'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 49, 'name': 'GetVideoEncoderConfiguration', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoEncoderConfiguration settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 49, 'name': 'GetVideoEncoderConfiguration', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoEncoderConfiguration settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetVideoEncoderConfigurationOptions(self):
        try:
            enc_token = self.media.GetProfiles()[0].VideoEncoderConfiguration._token
            configs = self.media.GetVideoEncoderConfigurationOptions({'ConfigurationToken': enc_token})
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 50, 'name': 'GetVideoEncoderConfigurationOptions', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoEncoderConfigurationOptions settings',
                'extension': 'The DUT did not send GetVideoEncoderConfigurationOptionsResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 50, 'name': 'GetVideoEncoderConfigurationOptions', 'service': 'Media',
                        'result': {'supported': True, 'report_name': 'GetVideoEncoderConfigurationOptions settings',
                        'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 50, 'name': 'GetVideoEncoderConfigurationOptions', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoEncoderConfigurationOptions settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 50, 'name': 'GetVideoEncoderConfigurationOptions', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoEncoderConfigurationOptions settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetVideoEncoderConfigurations(self):
        try:
            configs = self.media.GetVideoEncoderConfigurations()
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 51, 'name': 'GetVideoEncoderConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoEncoderConfigurations settings',
                'extension': 'The DUT did not send GetVideoEncoderConfigurationsResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 51, 'name': 'GetVideoEncoderConfigurations', 'service': 'Media',
                'result': {'supported': True,  'report_name': 'GetVideoEncoderConfigurations settings',
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 51, 'name': 'GetVideoEncoderConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoEncoderConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 51, 'name': 'GetVideoEncoderConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoEncoderConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetVideoSourceConfiguration(self):
        try:
            source_token = self.media.GetProfiles()[0].VideoSourceConfiguration._token
            configs = self.media.GetVideoSourceConfiguration({'ConfigurationToken': source_token})
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 52, 'name': 'GetVideoSourceConfiguration', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoSourceConfiguration settings',
                'extension': 'The DUT did not send GetVideoSourceConfigurationResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 52, 'name': 'GetVideoSourceConfiguration', 'service': 'Media',
                'result': {'supported': True,  'report_name': 'GetVideoSourceConfiguration settings',
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 52, 'name': 'GetVideoSourceConfiguration', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoSourceConfiguration settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 52, 'name': 'GetVideoSourceConfiguration', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoSourceConfiguration settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetVideoSourceConfigurationOptions(self):
        try:
            source_token = self.media.GetProfiles()[0].VideoSourceConfiguration._token
            configs = self.media.GetVideoSourceConfigurationOptions({'ConfigurationToken': source_token})
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 53, 'name': 'GetVideoSourceConfigurationOptions', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoSourceConfigurationOptions settings',
                'extension': 'The DUT did not send GetVideoSourceConfigurationOptionsResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 53, 'name': 'GetVideoSourceConfigurationOptions', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetVideoSourceConfigurationOptions settings',
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 53, 'name': 'GetVideoSourceConfigurationOptions', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoSourceConfigurationOptions settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 53, 'name': 'GetVideoSourceConfigurationOptions', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoSourceConfigurationOptions settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetVideoSourceConfigurations(self):
        try:
            configs = self.media.GetVideoSourceConfigurations()
            if ((configs is None) or (len(configs) == 0)):
                return {'test_id': 54, 'name': 'GetVideoSourceConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoSourceConfigurations settings',
                'extension': 'The DUT did not send GetVideoSourceConfigurationsResponse message',
                'response': str(configs), 'report': 'Not Supported'}}
            else:
                return {'test_id': 54, 'name': 'GetVideoSourceConfigurations', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetVideoSourceConfigurations settings', 
                'extension': None, 'response': str(configs), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 54, 'name': 'GetVideoSourceConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoSourceConfigurations settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 54, 'name': 'GetVideoSourceConfigurations', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoSourceConfigurations settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
    
    def GetVideoSources(self):
        try:
            sources = self.media.GetVideoSources()
            if ((sources is None) or (len(sources) == 0)):
                return {'test_id': 55, 'name': 'GetVideoSources', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoSources settings',
                'extension': 'The DUT did not send GetVideoSourcesResponse message',
                'response': str(sources), 'report': 'Not Supported'}}
            else:
                return {'test_id': 55, 'name': 'GetVideoSources', 'service': 'Media',
                'result': {'supported': True, 'report_name': 'GetVideoSources settings',
                'extension': None, 'response': str(sources), 'report': 'Supported'}}
        except Exception as e:
            if str(e) == 'Optional Action Not Implemented':
                return {'test_id': 55, 'name': 'GetVideoSources', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoSources settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'test_id': 55, 'name': 'GetVideoSources', 'service': 'Media',
                'result': {'supported': False, 'report_name': 'GetVideoSources settings',
                'extension': str(e), 'response': "", 'report': 'Not Supported'}}
