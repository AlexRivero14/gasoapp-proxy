from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Referer': 'https://geoportalgasolineras.es/',
}

@app.route('/api')
def proxy():
    url = request.args.get('url')
    if not url:
        resp = jsonify({'error': 'No URL'})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, 400
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        resp = Response(r.text, status=r.status_code, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = '*'
        return resp
    except Exception as e:
        resp = jsonify({'error': str(e)})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, 500

@app.route('/api', methods=['OPTIONS'])
def proxy_options():
    resp = Response('')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

if __name__ == '__main__':
    app.run()
