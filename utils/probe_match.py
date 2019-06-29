from wsdiscovery import WSDiscovery

def probe_match():
    wsd = WSDiscovery()
    wsd.start()
    ret = wsd.searchServices()
    wsd.stop()
