from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api')
def proxy():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL'}), 400
    try:
        r = requests.get(url, timeout=15)
        data = r.json()
        response = jsonify(data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
