from wsdiscovery import WSDiscovery
import re


def discovery():
    cameras = []

    wsd = WSDiscovery()
    wsd.start()
    ret = wsd.searchServices()

    for index, service in enumerate(ret):
        address = service.getXAddrs()[0]

        if 'onvif' not in address:
            continue

        res = re.findall(r'[0-9.]+|(?<=:)\d+', address)
        cam = {
            'ip': res[0],
            'port': int(res[1]) if len(res) > 1 else 80,
            'online': True
        }

        #Exclude devices on local Server Network
        if(cam['ip'] != '10.0.3.229' and cam['ip'] != '192.168.13.247'):
            cameras.append(cam)

    wsd.stop()
    cameras.sort(key=lambda x: x['ip'])
    return cameras
