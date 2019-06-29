def parse_cam_from_request(request):
    if request.method == "GET":
        ip = request.args.get('ip', None)
        port = request.args.get('port', None)
    else:
        ip = request.form.get('ip', None)
        port = request.form.get('port', None)

    if ip is None:
        return (None, None)

    if port is not None and port.isdigit():
        port = int(port)
    else:
        port = 80

    return (ip, port)
