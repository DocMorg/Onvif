from flask import request, jsonify
from core import Camera
from . import parse_cam_from_request
from . import status
from onvif import ONVIFError


def cam_required_decorator(fn):
    def wrapper(*args, **kwargs):
        ip, port = parse_cam_from_request(request)
        error_msg = ""
        cam = None

        if ip is not None:
            try:
                cam = Camera(ip, port)
            except ONVIFError as e:
                print "utils.cam_required_decorator: ONVIFError: %s" % e 
                error_msg = "Ip or port are incorrect"
        else:
            error_msg = "Please provide correct camera ip and port"

        if error_msg == "" and cam is not None:
            kwargs['ctx'] = {"cam": cam}
            return fn(*args, **kwargs)

        return jsonify({
            "error": error_msg,
            "params": [
                    {"param": "ip", "value": ip, "required": True},
                    {"param": "port", "value": port, "required": True},
                ]}), status.HTTP_400_BAD_REQUEST


    wrapper.func_name = fn.func_name
    return wrapper
