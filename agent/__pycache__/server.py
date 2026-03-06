from flask import Flask, request, jsonify, render_template, send_file
from flask_cloudflared import run_with_cloudflared
import json
import subprocess
import sys
import os

app = Flask(__name__)
run_with_cloudflared(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/research', methods=['POST'])
def research():
    try:
        data = request.json
        result = subprocess.run(
            [sys.executable, 'runner.py', json.dumps(data)],
            capture_output=True,
            text=True,
            cwd='/Users/kindafaisalhotmail.com/Desktop/week5/project '
        )
        return jsonify(json.loads(result.stdout))
    e