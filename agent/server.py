from flask import Flask, request, jsonify, render_template, send_file
import json
import subprocess
import sys
import os

app = Flask(__name__)

PROJECT_DIR = '/app'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        result = subprocess.run(
            [sys.executable, 'runner.py', json.dumps(data)],
            capture_output=True,
            text=True,
            cwd=PROJECT_DIR
        )
        if result.returncode != 0:
            return jsonify({"status": "error", "message": result.stderr})
        return jsonify(json.loads(result.stdout))
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/report', methods=['GET'])
def get_report():
    try:
        path = request.args.get('path')
        full_path = os.path.join(PROJECT_DIR, path)
        return open(full_path).read(), 200, {'Content-Type': 'text/plain'}
    except Exception as e:
        return str(e), 404

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.json
        report_path = data.get('report_path')
        full_path = os.path.join(PROJECT_DIR, report_path)
        return send_file(full_path, as_attachment=True, download_name='report.md')
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))