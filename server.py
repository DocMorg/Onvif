import time
import os
import sys
import utils
from core import Camera
from tests import CoreTests, EventsTests, AnalyticsTests, ImagingTests, Tests
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json
from pprint import pprint
from utils.generate_report import *
from database import db, User, TestResults, Device

import jinja2


from flask import (
    Flask, request, jsonify, redirect,
    send_from_directory, Response, render_template, g, make_response)

from flask_login import LoginManager, login_user, logout_user, login_required, current_user


from urlparse import urlparse, urljoin
from flask import request, url_for, flash


IS_PROD = '--prod' in sys.argv
if IS_PROD:
    CORS_VALUE = 'http://onvif.auditory.ru'
else:
    CORS_VALUE = 'http://localhost:3000'

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc



app = Flask(__name__,
 static_folder = 'templates/build/static',
 template_folder="templates/build")

app.config.from_object('config')
db.init_app(app)
app.app_context().push()
db.create_all()
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('templates/'),
])
app.jinja_loader = my_loader


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id==int(user_id)).one_or_none()


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    remember_me = False

    if 'remember_me' in request.form:
        remember_me = True

    registered_user = User.query.filter_by(email=email).first()
    if registered_user is None:
        flash('Username is invalid' , 'error')
        return redirect(url_for('login'))

    if not registered_user.check_password(password):
        flash('Password is invalid','error')
        return redirect(url_for('login'))

    login_user(registered_user, remember = remember_me)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) 

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    surname = request.form.get('surname')

    user = User(email=email, name=name, surname=surname)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)


@app.before_request
def before_request():
    g.user = current_user

@app.route('/info')
def apiinfo():
    return jsonify(api_avaliable_routes=[
        '/api/<test_type>_test/<method_name>',
        '/api/tests',
        '/api/devices',
        '/api/device',
        '/snapshots/<path:filename>',
        '/livestream'
    ])


@app.route('/api/<test_type>_test/<method_name>', methods=['POST'])
@utils.cam_required
def run_test(*args, **kwargs):
    cam = kwargs['ctx']['cam']
    test_type = kwargs['test_type']
    method_name = kwargs['method_name']
    test = Tests(cam)
    return jsonify(test.service_test(test_type, method_name))


@app.route('/api/tests')
@utils.cam_required
def tests(*args, **kwargs):
    cam = kwargs['ctx']['cam']
    test = Tests(cam)
    return jsonify(test.avaliable_tests())


@app.route('/api/report', methods=['GET', 'POST'])
def report():
    tested_data = json.loads(request.data)
    url = generate_report(tested_data)

    ip = str(tested_data['camInfo']['ip'])
    port = str(tested_data['camInfo']['port'])

    device = Device.query.filter(Device.ip==ip, Device.port==port).first()
    if device is None:
        device = Device(ip=ip, port=port, type='device', name='%s:%s'%(ip, port))
        db.session.add(device)

    dbreport = TestResults(device=device, user=g.user, url=url, rawText=json.dumps(tested_data))
    db.session.add(dbreport)
    db.session.commit()

    return jsonify(response=url)


@app.route('/api/reports')
@login_required
def return_report_files_list():
    results = TestResults.query.filter(User.id==int(g.user.get_id())).all()
    return jsonify([r.get_json() for r in results])


@app.route('/api/user')
@login_required
def return_user():
    return jsonify(g.user.get_json())



@app.route('/reports/<path:filename>')
def return_report_file(filename):
    return send_from_directory('reports', filename)

'''
Devices API
'''
@app.route('/api/devices')
def get_devices_list():
    cameras = utils.discovery()
    saved_cameras = list(map(lambda d: dict(ip=d.ip, port=d.port, online=False), Device.query.all()))
    ips = [c['ip'] for c in cameras]
    for sc in saved_cameras:
        if sc['ip'] not in ips:
            cameras.append(sc)

    cameras.sort(key=lambda x: x['ip'])
    for i in range(len(cameras)):
        cameras[i]['id'] = i+1

    return jsonify(cameras)


@app.route('/api/device')
@utils.cam_required
def get_device_info(*args, **kwargs):
    cam = kwargs['ctx']['cam']
    ip = cam.ip
    port = str(cam.port)


    device_info = cam.get_device_info()
    return jsonify(device_info)


'''
Serving data from device
'''
@app.route('/snapshots/<path:filename>')
def get_snapshot(filename):
    return send_from_directory(
        app.config['SNAPSHOTS_STATIC_PATH'], filename)


@app.route('/api/get_snapshots')
@utils.cam_required
def get_snapshots(*args, **kwargs):
    cam = kwargs['ctx']['cam']
    return jsonify(cam.get_snapshots_list())


@app.route('/api/current_snapshot')
@utils.cam_required
def get_current_snapshot(*args, **kwargs):
    cam = kwargs['ctx']['cam']
    return jsonify({
        'camera': cam.ip + ':' + str(cam.port),
        'datetime': time.strftime("%d-%m-%Y %H:%M:%S", time.localtime()),
        'url': cam.get_public_snapshot_url()
    })


@app.route('/livestream')
@utils.cam_required
def livestream(*args, **kwargs):
    cam = kwargs['ctx']['cam']
    url = cam.get_private_stream_url()
    playlist_name = ("%s%d.m3u8" % (cam.ip.replace('.', ''), cam.port))

    print utils.stream.check_stream(cam.ip, cam.port)

    if len(utils.stream.check_stream(cam.ip, cam.port)) <= 2:
        utils.stream.start_stream(url, './streams', playlist_name)

    # make sure the stream was created
    while not os.path.exists(os.path.join('./streams', playlist_name)) or len(utils.stream.check_stream(cam.ip, cam.port)) <= 2:
        time.sleep(1)

    return redirect("/%s" % playlist_name, code=302)


@app.route('/api/stop_stream')
@utils.cam_required
def kill_stream(*args, **kwargs):
    cam = kwargs['ctx']['cam']
    # utils.stream.stop_stream(cam.ip, cam.port)
    return 'ok'


@app.route('/<name>.m3u8')
def streaming_stuff1(name):
    response = make_response(send_from_directory('streams', name+'.m3u8'))
    response.headers['Access-Control-Allow-Origin'] = CORS_VALUE
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    # response.headers['Expires'] = 'Tue, 03 Jul 2001 06:00:00 GMT'
    # response.headers['Last-Modified'] = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime())
    # response.headers['Cache-Control'] = 'max-age=0, no-cache, must-revalidate, proxy-revalidate'
    return response


@app.route('/<name>.ts')
def streaming_stuff2(name):
    response = make_response(send_from_directory('streams', name+'.ts'))
    response.headers['Access-Control-Allow-Origin'] = CORS_VALUE
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@login_required
def index(path):
    return render_template('index.html')


if __name__ == '__main__':
    if '--prod' in sys.argv:
        app.run('10.0.3.91', 5000, debug=True)
    else:
        app.run(debug=True)
