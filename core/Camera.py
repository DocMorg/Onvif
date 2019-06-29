import io
import os
import re
import time
from time import sleep
import string
from random import choice
from onvif import ONVIFCamera, exceptions
import requests
import rtsp
from tests import Tests

gen_timestamp = lambda: time.strftime("_%d-%m-%Y_%H:%M:%S", time.localtime())


class Camera(ONVIFCamera):
    def __init__(self, ip, port, user='admin', password='Supervisor'):
        super(Camera, self).__init__(ip, port, user, password)
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.test_types = [
            'analytics',
            'device',
            'deviceio',
            'events',
            'imaging',
            'media',
            'ptz',
            'pullpoint',
            'recording',
            'replay',
            'search'
        ]


    # TODO: make it json fomatted
    def get_capabilities(self):
        return self.devicemgmt.GetCapabilities()


    def get_device_info(self):
        device_info = self.devicemgmt.GetDeviceInformation()
        return {
            'Manufacturer': device_info.Manufacturer,
            'Model': device_info.Model,
            'Firmware Version': device_info.FirmwareVersion,
            'Serial Number': device_info.SerialNumber,
            'Hardware ID': device_info.HardwareId,
            'Supported Services': self.get_supported_services(),
            'avaliable_tests': self.get_available_tests(),
            'private_snapshot_url': self.get_private_snapshot_url(),
            'private_stream_url': self.get_private_stream_url(),
            'snapshot_url': self.get_public_snapshot_url(),
            'stream_url': self.get_public_stream_url(),
            'ip': self.ip,
            'port': self.port,
            'username': self.user,
            'password': self.password
        }


    def get_private_snapshot_url(self):
        uri = None
        media_service = self.create_media_service()
        token = media_service.GetProfiles()[0]._token

        try:
            uri = media_service.GetSnapshotUri({'ProfileToken': token}).Uri
        except Exception as e:
            pass

        return uri


    def get_private_stream_url(self):
        uri = None
        media_service = self.create_media_service()
        token = media_service.GetProfiles()[0]._token

        obj = media_service.create_type('GetStreamUri')
        obj.ProfileToken = token
        obj.StreamSetup = {
            'Stream': 'RTP-Unicast',
            'Transport': {'Protocol': 'RTSP'}
        }

        try:
            uri = media_service.GetStreamUri(obj).Uri
            if len(self.user + self.password) > 0:
                uri = uri[:7] + self.user + ':' + self.password + "@" + uri[7:]

        except Exception as e:
            pass

        return uri


    def get_public_snapshot_url(self):
        # make sure that snapshots folder is exists
        if not os.path.isdir('snapshots'):
            os.makedirs('snapshots')

        private_uri = self.get_private_snapshot_url()
        if private_uri is not None:
            try:
                r = requests.get(private_uri, auth=(self.user, self.password))

                if r.ok:
                    filename = 'snapshots/' + self.ip + ":" + str(self.port) + gen_timestamp() + '.jpg'
                    with open(filename, 'wb') as snapshot:
                        snapshot.write(r.content)
                    return "/" + filename
            except Exception as e:
                print('get_public_snapshot_url: request error: ', e)


        # try to get snapshot from stream
        private_stream_url = self.get_private_stream_url()

        if private_stream_url is not None:
            client = rtsp.Client(rtsp_server_uri=private_stream_url, verbose=False)
            image = client.read()

            if image is not None:
                imgByteArr = io.BytesIO()
                image.save(imgByteArr, format='jpeg')
                image = imgByteArr.getvalue()

            client.close()
            filename = 'snapshots/' + self.ip + ":" + str(self.port) + gen_timestamp() + '.jpg'

            with open(filename, 'wb') as snapshot:
                snapshot.write(image)

            return "/" + filename

        return None


    def get_public_stream_url(self):
        if self.get_private_stream_url() is not None:
            return '/livestream?ip='+self.ip+"&port="+str(self.port)
        return None


    def get_supported_services(self):
        services = list(dict.fromkeys(map(lambda x: x.Namespace.split('/')[-2].lower(), self.devicemgmt.GetServices({'IncludeCapability': False}))))
        return [item for item in services if item in self.test_types]


    def get_available_tests(self):
        test = Tests(self)
        return test.avaliable_tests()['response']

    def get_snapshots_list(self):
        credentials = self.ip + ':' + str(self.port)
        print credentials
        snapshots = []
        if os.path.isdir('snapshots'):
            for snapshot in os.listdir("snapshots"):
                if re.search(credentials, snapshot):
                    print snapshot
                    date = re.findall('_(.*)_(.*)\.jpg', snapshot)
                    snapshots.append({'url': '/snapshots/' + snapshot, 'datetime': date[0][0] + ' ' + date[0][1], 'camera': credentials})
        return snapshots

    def returnpos(self, ptz, token):
        try:
            pos = ptz.GetStatus({"ProfileToken": token}).Position
        except AttributeError:
            return False
        try:
            pos.x_z = pos.Zoom._x
        except AttributeError:
                pos.x_z = False
        try:
            pos.x = pos.PanTilt._x
            pos.y = pos.PanTilt._y
        except AttributeError:
            pos.x = False
            pos.y = False
        return pos

    def left(self, req_move, req_stop, ptz, token):
        sleep(0.3)
        self.ptz.Stop(req_stop)
        req_move.Velocity.Zoom._x = 0.0
        req_move.Velocity.PanTilt._x = -0.5
        req_move.Velocity.PanTilt._y = 0.0
        self.ptz.ContinuousMove(req_move)
        sleep(1)
        self.ptz.Stop(req_stop)
        sleep(0.3)


    def right(self, req_move, req_stop, ptz, token):
        sleep(0.3)
        self.ptz.Stop(req_stop)
        req_move.Velocity.Zoom._x = 0.0
        req_move.Velocity.PanTilt._x = 0.5
        req_move.Velocity.PanTilt._y = 0.0
        self.ptz.ContinuousMove(req_move)
        sleep(1)
        self.ptz.Stop(req_stop)
        sleep(0.3)

    def zoom_in(self, req_move, req_stop, ptz, token):
        sleep(0.3)
        self.ptz.Stop(req_stop)
        req_move.Velocity.PanTilt._x = 0.0
        req_move.Velocity.PanTilt._y = 0.0
        req_move.Velocity.Zoom._x = 0.1
        self.ptz.ContinuousMove(req_move)
        sleep(1)
        self.ptz.Stop(req_stop)
        sleep(0.3)

    def zoom_out(self, req_move, req_stop, ptz, token):
        sleep(0.3)
        self.ptz.Stop(req_stop)
        req_move.Velocity.PanTilt._x = 0.0
        req_move.Velocity.PanTilt._y = 0.0
        req_move.Velocity.Zoom._x = -0.1
        self.ptz.ContinuousMove(req_move)
        sleep(1)
        self.ptz.Stop(req_stop)
        sleep(0.3)

    def genpass(self, length=8, chars=string.ascii_letters + string.digits):
        return ''.join([choice(chars) for k in range(length)])

    def genchar(self, length=8, chars=string.ascii_letters):
        return ''.join([choice(chars) for k in range(length)])

    def gendigits(self, length=8, chars=string.digits):
        return ''.join([choice(chars) for k in range(length)])

    def genhardpass(self, length=8, chars=string.ascii_letters + string.digits + string.punctuation):
        return ''.join([choice(chars) for k in range(length)])

    def maxminpass(self, a):
        i = 4
        k = 1000
        z = 0
        while i < 50:
            try:
                name = self.genpass(7)
                if a == 'chars':
                    self.devicemgmt.CreateUsers({'User': {'Username': name, 'Password': self.genchar(i), 'UserLevel': 'User'}})
                    sleep(0.3)
                elif a == 'digits':
                    self.devicemgmt.CreateUsers({'User': {'Username': name, 'Password': self.gendigits(i), 'UserLevel': 'User'}})
                    sleep(0.3)
                elif a == 'chars+digits':
                    self.devicemgmt.CreateUsers({'User': {'Username': name, 'Password': self.genpass(i), 'UserLevel': 'User'}})
                    sleep(0.3)
                elif a == 'chars+digits+symbols':
                    self.devicemgmt.CreateUsers({'User': {'Username': name, 'Password': self.genhardpass(i),'UserLevel': 'User'}})
                    sleep(0.3)
                if self.devicemgmt.GetUsers()[-1].Username == name:
                    if i < k:
                        k = i
                    if i > z:
                        z = i
                    self.devicemgmt.DeleteUsers({'Username': name})
                    sleep(0.5)
                    i += 1
                else:
                    break
            except exceptions.ONVIFError:
                i += 1
        if k != 1000 and z != 0:
            return 'The range for password length is from ' + str(k) + ' to ' + str(z) + ' for ' + a
        else:
            return 'No user has been created. Password with ' + str(a) + ' does not work'

    def maxminpass(self):
        result = []
        for m in ['chars', 'digits', 'chars+digits', 'chars+digits+symbols']:
            result.append(self.test(m))
        return result

    def maxminuser(self):
        i = 1
        k = 100
        z = 0
        while i < 32:
            try:
                name = self.genpass(i)
                self.devicemgmt.CreateUsers({'User': {'Username': name, 'Password': self.genpass(9), 'UserLevel': 'User'}})
                sleep(0.3)
                if self.devicemgmt.GetUsers()[-1].Username == name:
                    if i < k:
                        k = i
                    if i > z:
                        z = i
                # print self.cam.devicemgmt.GetUsers()[-1].Username, name
                self.devicemgmt.DeleteUsers({'Username': name})
                sleep(0.5)
                i += 1
            except exceptions.ONVIFError:
                i += 1
        if k != 1000 and z != 0:
            return 'The range for username length is from ' + str(k) + ' to ' + str(z)
        else:
            return 'No user has been created. Something is wrong'

    def maxusers(self):
        k = []
        n, z, i, max1 = 1, 1, 1, 0
        for item in self.devicemgmt.GetUsers():
            max1 += 1
        while i <= 100:
            k += [self.genpass(8)]
            i += 1
        while n < i-1:
            try:
                self.devicemgmt.CreateUsers({'User': {'Username': k[n], 'Password': self.genpass(), 'UserLevel': 'User'}})
                sleep(0.3)
                if self.devicemgmt.GetUsers()[-1].Username == k[n]:
                    n += 1
                    max1 += 1
                else:
                    break
            except exceptions.ONVIFError:
                break
        if n == i:
            return 'No user has been created. Something is wrong'
        # print self.cam.devicemgmt.GetUsers()
        while z < n:
            self.devicemgmt.DeleteUsers({'Username': k[z]})
            sleep(0.5)
            z += 1
        if n != 1:
            return 'Camera supports ' + str(max1) + ' max users'
        else:
            return 'No user has been created. Something is wrong'
