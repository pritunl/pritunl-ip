import os
import json
import flask
import cherrypy.wsgiserver

PORT = int(os.getenv('PORT', 8080))
NOTIFICATIONS = {
    '1009': {
        'www': 'ok',
        'vpn': 'ok',
        'message': 'Update available, please use your distributions ' +
            'package management system to update to the latest version.',
    },
    '1010': {
        'www': 'ok',
        'vpn': 'ok',
        'message': 'Update available, please use your distributions ' +
            'package management system to update to the latest version.',
    },
    '1011': {
        'www': 'ok',
        'vpn': 'ok',
        'message': '',
    },
}

app = flask.Flask('pritunl_ip')

def get_remote_addr():
    if 'X-Forwarded-For' in flask.request.headers:
        return flask.request.headers.getlist('X-Forwarded-For')[0]
    if 'X-Real-Ip' in flask.request.headers:
        return flask.request.headers.getlist('X-Real-Ip')[0]
    return flask.request.remote_addr

def jsonify(data=None, status_code=None):
    if not isinstance(data, basestring):
        data = json.dumps(data)
    response = flask.Response(response=data, mimetype='application/json')
    response.headers.add('Cache-Control',
        'no-cache, no-store, must-revalidate')
    response.headers.add('Pragma', 'no-cache')
    if status_code is not None:
        response.status_code = status_code
    return response

@app.route('/', methods=['GET'])
@app.route('/json', methods=['GET'])
def json_get():
    ip_addr = get_remote_addr()
    return jsonify({
        'ip': ip_addr,
    })

@app.route('/notification/<ver>', methods=['GET'])
def notification_get(ver):
    notification = NOTIFICATIONS.get(ver)
    if not notification:
        return flask.abort(404)
    return jsonify(notification)

server = cherrypy.wsgiserver.CherryPyWSGIServer(('0.0.0.0', PORT), app)
try:
    server.start()
except (KeyboardInterrupt, SystemExit), exc:
    server.stop()
