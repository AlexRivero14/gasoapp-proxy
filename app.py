from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Referer': 'https://geoportalgasolineras.es/',
    'Origin': 'https://geoportalgasolineras.es',
}

@app.route('/api')
def proxy():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL'}), 400
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        data = r.json()
        response = jsonify(data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
