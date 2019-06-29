from onvif import ONVIFCamera
from PTZTests import PTZTests
from time import sleep

class ImagingTests:

    def __init__(self, cam):
        self.cam = cam
        self.media = self.cam.create_media_service()
        self.ptz = self.cam.create_ptz_service()
        self.imaging = self.cam.create_imaging_service()
        self.vstoken = self.media.GetVideoSources()[0]._token

    def GetImagingSettings(self):
        try:
            response = self.imaging.GetImagingSettings({'VideoSourceToken': self.vstoken})
            if ((response is None) or (len(response) == 0)):
                return {'name': 'GetImagingSettings', 'service': 'Imaging',
                'result': {'supported': False,
                'report_name': 'Imaging settings',
                'extension': 'The DUT did not send GetImagingSettingsResponse message',
                'response': str(response), 
                'report': 'Imaging settings are not supported\nThe device did not send GetImagingSettingsResponse message'}}
            else:
                return {'name': 'GetImagingSettings', 'service': 'Imaging',
                'result': {'supported': True,
                'report_name': 'Imaging settings',
                'extension': None,
                'response': str(response),
                'report': 'Imaging Settings Report'}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetImagingSettings', 'service': 'Imaging',
                'result': {'supported': False,
                'report_name': 'Imaging settings',
                'extension': 'Optional Action Not Implemented',
                'response': "", 'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetImagingSettings', 'service': 'Imaging',
                'result': {'supported': False,
                'report_name': 'Imaging settings',
                'extension': str(e),
                'response': "",
                'report': 'Not Supported'}}

    def AbsoluteImagingMoveInteractive(self):
        try:
            token = self.media.GetProfiles()[0]._token
            req_move = self.ptz.create_type('ContinuousMove')
            req_move.ProfileToken = token
            req_stop = self.ptz.create_type('Stop')
            req_stop.ProfileToken = token

            options = self.imaging.GetMoveOptions({'VideoSourceToken': self.vstoken})
            self.imaging.create_type('Move')
            self.imaging.SetImagingSettings({'VideoSourceToken': self.vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'MANUAL'}}})
            self.imaging.Stop({'VideoSourceToken': self.vstoken})
            x0 = round(self.imaging.GetStatus({'VideoSourceToken': self.vstoken}).FocusStatus20.Position, 2)
            max_x = options.Absolute.Position.Max
            if x0 + (max_x/2) < max_x:
                x1 = x0 + max_x/2
            else:
                x1 = x0 - max_x/2

            self.imaging.Move({'VideoSourceToken': self.vstoken, 'Focus': {'Absolute': {'Position': x1, 'Speed': 0.8}}})
            sleep(2)
            self.imaging.Stop({'VideoSourceToken': self.vstoken})
            x2 = round(imaging.GetStatus({'VideoSourceToken': self.vstoken}).FocusStatus20.Position, 2)
            if abs(x1-x2) == 0 and not x0 == x2 == 0:
                self.imaging.SetImagingSettings(
                    {'VideoSourceToken': self.vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
                self.cam.left(req_move, req_stop, self.ptz, token)
                self.cam.right(req_move, req_stop, self.ptz, token)
                self.cam.zoom_in(req_move, req_stop, self.ptz, token)
                self.cam.zoom_out(req_move, req_stop, self.ptz, token)
                return {'name': 'AbsoluteImagingMoveInteractive', 'service': 'Imaging',
                'result': {'supported': True,
                'report_name': 'Absolute Focus move',
                'extension': 'Absolute Imaging Move is supported',
                'response': "Absolute Imaging Move is supported",
                'report': 'Absolute Focus move is supported, current coordinates: {}'.format(x2)}}
            else:
                self.imaging.SetImagingSettings(
                    {'VideoSourceToken': self.vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
                self.cam.left(req_move, req_stop, self.ptz, token)
                self.cam.right(req_move, req_stop, self.ptz, token)
                self.cam.zoom_in(req_move, req_stop, self.ptz, token)
                self.cam.zoom_out(req_move, req_stop, self.ptz, token)
                return {'name': 'AbsoluteImagingMoveInteractive', 'service': 'Imaging',
                'result': {'supported': True,
                'report_name': 'Absolute Focus move',
                'extension': 'Absolute Imaging Move is supported, but it cannot be checked.\nPotential error with coordinates from GetStatus(), current coordinates: {}'.format(x2),
                'response': 'Absolute Imaging Move is supported, but it cannot be checked.\nPotential error with coordinates from GetStatus(), current coordinates: {}'.format(x2),
                'report': 'Absolute Imaging Move is supported, but it cannot be checked.\nPotential error with coordinates from GetStatus(), current coordinates: {}'.format(x2)}}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'AbsoluteImagingMoveInteractive', 'service': 'Imaging',
                'result': {'supported': False,
                'report_name': 'Absolute Focus move',
                'extension': 'Optional Action Not Implemented',
                'response': "Optional Action Not Implemented",
                'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'AbsoluteImagingMoveInteractive', 'service': 'Imaging',
                'result': {'supported': False,
                'report_name': 'Absolute Focus move',
                'extension': str(e),
                'response': "Not Supported", 'report': 'Not Supported'}}

    def ContinuousImagingMoveInteractive(self):
        try:
            options = self.imaging.GetMoveOptions({'VideoSourceToken': self.vstoken})
            token = self.media.GetProfiles()[0]._token
            req_move = self.ptz.create_type('ContinuousMove')
            req_move.ProfileToken = token
            req_stop = self.ptz.create_type('Stop')
            req_stop.ProfileToken = token
            self.imaging.create_type('Move')
            try:
                options.Continuous
            except AttributeError:
                return {'name': 'ContinuousImagingMoveInteractive', 'service': 'Imaging',
                'result': {'supported': False,
                'report_name': 'Continuous Focus move',
                'extension': 'Continuous Focus Move is not supported',
                'response': "Continuous Focus Move is not supported",
                'report': 'Continuous Focus move is not supported' }}

            max_speed = options.Continuous.Speed.Max

            self.imaging.SetImagingSettings(
                {'VideoSourceToken': self.vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'MANUAL'}}})
            self.imaging.Stop({'VideoSourceToken': self.vstoken})
            x0 = round(self.imaging.GetStatus({'VideoSourceToken': self.vstoken}).FocusStatus20.Position, 2)
            if x0 + (max_speed / 2) < max_speed:
                x1 = x0 + max_speed / 2
            else:
                x1 = x0 - max_speed / 2
            self.imaging.Move({'VideoSourceToken': self.vstoken, 'Focus': {'Continuous': {'Speed': x1}}})
            sleep(1)
            self.imaging.Stop({'VideoSourceToken': self.vstoken})
            x2 = round(self.imaging.GetStatus({'VideoSourceToken': self.vstoken}).FocusStatus20.Position, 2)
            # print 'x0 ', x0, ' x1 ', x1, ' x2 ', x2
            if abs(x1 - x2) == 0 and not x0 == x2 == 0:
                self.imaging.SetImagingSettings(
                    {'VideoSourceToken': self.vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
                self.cam.left(req_move, req_stop, self.ptz, token)
                self.cam.right(req_move, req_stop, self.ptz, token)
                self.cam.zoom_in(req_move, req_stop, self.ptz, token)
                self.cam.zoom_out(req_move, req_stop, self.ptz, token)
                return {'name': 'ContinuousImagingMoveInteractive', 'service': 'Imaging',
                'result': {'supported': True,
                'report_name': 'Continuous Focus move',
                'extension': 'Continuous Focus move is supported current coordinates: {}'.format(x2),
                'response': 'Continuous Focus move is supported current coordinates: {}'.format(x2),
                'report': 'Continuous Focus move is supported current coordinates: {}'.format(x2) }}
            else:
                self.imaging.SetImagingSettings(
                    {'VideoSourceToken': self.vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
                self.cam.left(req_move, req_stop, self.ptz, token)
                self.cam.right(req_move, req_stop, self.ptz, token)
                self.cam.zoom_in(req_move, req_stop, self.ptz, token)
                self.cam.zoom_out(req_move, req_stop, self.ptz, token)
                return {'name': 'ContinuousImagingMoveInteractive', 'service': 'Imaging',
                'result': {'supported': True,
                'report_name': 'Continuous Focus move',
                'extension': 'Continuous Focus move is supported, but it cannot be checked.\nPotential error with coordinates from GetStatus(), current coordinates: {}.Invalid coordinates.'.format(x2),
                'response': 'Continuous Focus move is supported, but it cannot be checked.\nPotential error with coordinates from GetStatus(), current coordinates: {}.Invalid coordinates.'.format(x2),
                'report': 'Continuous Focus move is supported, but it cannot be checked.\nPotential error with coordinates from GetStatus(), current coordinates: {}.Invalid coordinates.'.format(x2) }}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'ContinuousImagingMoveInteractive', 'service': 'Imaging',
                'result': {'supported': False,
                'report_name': 'Continuous Focus move',
                'extension': 'Optional Action Not Implemented',
                'response': "Optional Action Not Implemented",
                'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'ContinuousImagingMoveInteractive', 'service': 'Imaging',
                'result': {'supported': False,
                'report_name': 'Continuous Focus move',
                'extension': str(e),
                'response': "Not Supported", 'report': 'Not Supported'}}

    def RelativeImagingMoveInteractive(self):
        try:
            options = self.imaging.GetMoveOptions({'VideoSourceToken': self.vstoken})
            token = self.media.GetProfiles()[0]._token
            req_move = self.ptz.create_type('ContinuousMove')
            req_move.ProfileToken = token
            req_stop = self.ptz.create_type('Stop')
            req_stop.ProfileToken = token
            self.imaging.create_type('Move')
            try:
                options.Relative
            except AttributeError:
                return {'name': 'RelativeImagingMoveInteractive', 'service': 'Imaging',
                'result': {'supported': False,
                'report_name': 'Relative Focus move',
                'extension': 'Relative Focus Move is not supported',
                'response': "Relative Focus Move is not supported",
                'report': 'Relative Focus move is not supported' }}
            self.imaging.SetImagingSettings(
                {'VideoSourceToken': self.vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'MANUAL'}}})
            self.imaging.Stop({'VideoSourceToken': self.vstoken})
            x0 = round(imaging.GetStatus({'VideoSourceToken': self.vstoken}).FocusStatus20.Position, 2)
            max_x = options.Relative.Distance.Max
            if x0 + (max_x / 2) < max_x:
                x1 = x0 + max_x / 2
            else:
                x1 = x0 - max_x / 2
            self.imaging.Move({'VideoSourceToken': self.vstoken, 'Focus': {'Relative': {'Distance': x1, 'Speed': 0.8}}})
            sleep(2)  # waiting
            self.imaging.Stop({'VideoSourceToken': self.vstoken})  # stopping imaging
            x2 = round(self.imaging.GetStatus({'VideoSourceToken': self.vstoken}).FocusStatus20.Position, 2)
            # print 'x0 ', x0, ' x1 ', x1, ' x2 ', x2
            if abs(x1 - x2) == 0 and not x0 == x2 == 0:
                self.imaging.SetImagingSettings(
                    {'VideoSourceToken': self.vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
                self.cam.left(req_move, req_stop, self.ptz, token)
                self.cam.right(req_move, req_stop, self.ptz, token)
                self.cam.zoom_in(req_move, req_stop, self.ptz, token)
                self.cam.zoom_out(req_move, req_stop, self.ptz, token)
                return {'name': 'RelativeImagingMoveInteractive', 'service': 'Imaging',
                'result': {'supported': True,
                'report_name': 'Relative Focus move',
                'extension': 'Relative Focus move is supported current coordinates: {}'.format(x2),
                'response': 'Relative Focus move is supported current coordinates: {}'.format(x2),
                'report': 'Relative Focus move is supported current coordinates: {}'.format(x2) }}
            else:
                self.imaging.SetImagingSettings(
                    {'VideoSourceToken': self.vstoken, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
                self.cam.left(req_move, req_stop, self.ptz, token)
                self.cam.right(req_move, req_stop, self.ptz, token)
                self.cam.zoom_in(req_move, req_stop, self.ptz, token)
                self.cam.zoom_out(req_move, req_stop, self.ptz, token)
                return {'name': 'RelativeImagingMoveInteractive', 'service': 'Imaging',
                'result': {'supported': True,
                'report_name': 'Relative Focus move',
                'extension': 'Relative Focus move is supported, but it cannot be checked.\nPotential error with coordinates from GetStatus(), current coordinates: {}.Invalid coordinates.'.format(x2),
                'response': 'Relative Focus move is supported, but it cannot be checked.\nPotential error with coordinates from GetStatus(), current coordinates: {}.Invalid coordinates.'.format(x2),
                'report': 'Relative Focus move is supported, but it cannot be checked.\nPotential error with coordinates from GetStatus(), current coordinates: {}.Invalid coordinates.'.format(x2) }}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'RelativeImagingMoveInteractive', 'service': 'Imaging',
                'result': {'supported': False,
                'report_name': 'Relative Focus move',
                'extension': 'Optional Action Not Implemented',
                'response': "Optional Action Not Implemented",
                'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'RelativeImagingMoveInteractive', 'service': 'Imaging',
                'result': {'supported': False,
                'report_name': 'Relative Focus move',
                'extension': str(e),
                'response': "Not Supported", 'report': 'Not Supported'}}

    def GetBrightness(self):
        try:
            f1 = True
            f2 = True
            settings = self.imaging.GetImagingSettings({'VideoSourceToken': self.vstoken})
            options = self.imaging.GetOptions({'VideoSourceToken': self.vstoken})
            try:
                Min = options.Brightness.Min
                Max = options.Brightness.Max
            except AttributeError:
                f1 = False
            try:
                Curr = settings.Brightness
            except AttributeError:
                f2 = False
            if f1 and f2:
                statement1 = 'Min: ' + str(Min) + ' Curr: ' + str(Curr) + ' Max: ' + str(Max)
                return {'name': 'GetBrightness', 'service': 'Imaging',
                'result': {'supported': True,
                'report_name': 'Brightness',
                'extension': str(statement1),
                'response': "Supported", 'report': statement1}}
            elif f1 and not f2:
                statement2 = 'Min: ' + str(Min) + ' Curr: ' + 'NULL' + ' Max: ' + str(Max)
            elif not f1:
                return {'name': 'GetBrightness', 'service': 'Imaging',
                'result': {'supported': True,
                'report_name': 'Brightness',
                'extension': statement2,
                'response': statement2, 'report': statement2 }}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'GetBrightness', 'service': 'Imaging',
                'result': {'supported': False,
                'report_name': 'Brightness',
                'extension': 'Optional Action Not Implemented',
                'response': "Optional Action Not Implemented",
                'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'GetBrightness', 'service': 'Imaging',
                'result': {'supported': False,
                'report_name': 'Brightness',
                'extension': str(e),
                'response': "Not Supported", 'report': 'Not Supported'}}

    def SetBrightnessInteractive(self):
        try:
            options = self.imaging.GetOptions({'VideoSourceToken': self.vstoken})
            get0 = self.imaging.GetImagingSettings({'VideoSourceToken': self.vstoken})
            try:
                Min = options.Brightness.Min
                Max = options.Brightness.Max
                br0 = get0.Brightness
                value = br0 - 10
                if Min < value < Max:
                    self.imaging.SetImagingSettings({'VideoSourceToken': self.vstoken, 'ImagingSettings': {'Brightness': value}})
                    sleep(1)
                get1 = self.imaging.GetImagingSettings({'VideoSourceToken': self.vstoken})
                sleep(1)
                self.imaging.SetImagingSettings({'VideoSourceToken': self.vstoken, 'ImagingSettings': {'Brightness': br0}})
                br1 = get1.Brightness
                if br1 == value:
                    statement1 = 'Set Brightness is supported. Current value: ' + str(br1)
                    return {'name': 'SetBrightnessInteractive', 'service': 'Imaging',
                    'result': {'supported': True,
                    'report_name': 'Set Brightness settings',
                    'extension': '',
                    'response': statement1, 'report': statement1}}
                else:
                    statement2 =  'Set Brightness is not supported'
                    return {'name': 'SetBrightnessInteractive', 'service': 'Imaging',
                    'result': {'supported': True,
                    'report_name': 'Set Brightness settings',
                    'extension': '',
                    'response': statement2, 'report': statement2 }}
            except AttributeError:
                statement3 =  'Set Brightness is not supported'
                return {'name': 'SetBrightnessInteractive', 'service': 'Imaging',
                'result': {'supported': True,
                'report_name': 'Set Brightness settings',
                'extension': '',
                'response': statement3, 'report': statement3 }}
        except Exception as e:
            if ((str(e) == 'Optional Action Not Implemented') or (str(e) == 'This optional method is not implemented')):
                return {'name': 'SetBrightnessInteractive', 'service': 'Imaging',
                'result': {'supported': False,
                'report_name': 'Set Brightness settings',
                'extension': 'Optional Action Not Implemented',
                'response': "Optional Action Not Implemented",
                'report': 'Optional Action Not Implemented' }}
            else:
                return {'name': 'SetBrightnessInteractive', 'service': 'Imaging',
                'result': {'supported': False,
                'report_name': 'Set Brightness settings',
                'extension': str(e),
                'response': "Not Supported", 'report': 'Not Supported'}}

