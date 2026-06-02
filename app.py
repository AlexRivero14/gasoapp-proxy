from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Referer': 'https://geoportalgasolineras.es/',
}

def cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

@app.route('/api')
def proxy():
    url = request.args.get('url')
    if not url:
        return cors(jsonify({'error': 'No URL'})), 400
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        # Si la respuesta es HTML, devolver lista vacía
        content_type = r.headers.get('Content-Type', '')
        if 'html' in content_type or r.text.strip().startswith('<'):
            resp = Response('{"ListaEESSPrecio":[]}', status=200, mimetype='application/json')
            return cors(resp)
        resp = Response(r.text, status=r.status_code, mimetype='application/json')
        return cors(resp)
    except Exception as e:
        return cors(jsonify({'error': str(e)})), 500

@app.route('/api', methods=['OPTIONS'])
def proxy_options():
    return cors(Response(''))

if __name__ == '__main__':
    app.run()
