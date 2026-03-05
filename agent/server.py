from flask import Flask, request, jsonify, render_template, Response
from flask_cloudflared import run_with_cloudflared
import json, subprocess, sys, os
import requests as req
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, template_folder='templates')
run_with_cloudflared(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        company = data.get('company', '')
        serper_data, guardian_data, alpha_data = {}, {}, {}
        try:
            serper_data = req.post('https://google.serper.dev/search',
                headers={'X-API-KEY': os.getenv('SERPER_API_KEY'), 'Content-Type': 'application/json'},
                json={'q': company + ' company financial news 2025'}).json()
        except: pass
        try:
            guardian_data = req.get('https://content.guardianapis.com/search',
                params={'q': company, 'api-key': os.getenv('GUARDIAN_API_KEY'), 'show-fields': 'bodyText', 'page-size': 5}).json()
        except: pass
        try:
            alpha_data = req.get('https://www.alphavantage.co/query',
                params={'function': 'OVERVIEW', 'symbol': company[:4].upper(), 'apikey': os.getenv('ALPHA_VANTAGE_API_KEY')}).json()
        except: pass
        bundle = {'serper': serper_data, 'guardian': guardian_data, 'alpha_vantage': alpha_data}
        payload = json.dumps({'company': company, 'research_bundle': bundle})
        result = subprocess.run([sys.executable, 'runner.py', payload],
            capture_output=True, text=True,
            cwd='/Users/kindafaisalhotmail.com/Desktop/week5/project ')
        return jsonify(json.loads(result.stdout))
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/report', methods=['GET'])
def report():
    try:
        full_path = os.path.join('/Users/kindafaisalhotmail.com/Desktop/week5/project ', request.args.get('path'))
        return Response(open(full_path).read(), mimetype='text/plain')
    except Exception as e:        return Response('Error', status=500)

@app.route('/research', methods=['POST'])
def research():
    try:
        data = request.json
        result = subprocess.run([sys.executable, 'runner.py', json.dumps(data)],
            capture_output=True, text=True,
            cwd='/Users/kindafaisalhotmail.com/Desktop/week5/project ')
        return jsonify(json.loads(result.stdout))
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
