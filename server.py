import os
import json
import flask
import cherrypy.wsgiserver

app = flask.Flask('pritunl_ip')

def get_remote_addr():
    if 'X-Forwarded-For' in flask.request.headers:
        return flask.request.headers.getlist('X-Forwarded-For')[0]
    if 'X-Real-Ip' in flask.request.headers:
        return flask.request.headers.getlist('X-Real-Ip')[0]
    return flask.request.remote_addr

@app.route('/', methods=['GET'])
@app.route('/json', methods=['GET'])
def json_get():
    data = json.dumps({
        'ip': get_remote_addr(),
    })
    callback = flask.request.args.get('callback', False)
    if callback:
        data = '%s(%s)' % (callback, data)
        mimetype = 'application/javascript'
    else:
        mimetype = 'application/json'
    response = flask.Response(response=data, mimetype=mimetype)
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Cache-Control',
        'private, no-cache, no-cache=Set-Cookie, proxy-revalidate')
    response.headers.set('Pragma', 'no-cache')
    return response

server = cherrypy.wsgiserver.CherryPyWSGIServer(
    ('0.0.0.0', int(os.getenv('PORT', 8080))), app)
try:
    server.start()
except (KeyboardInterrupt, SystemExit), exc:
    server.stop()
