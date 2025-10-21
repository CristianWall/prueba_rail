from flask import Flask, render_template, jsonify
import os
import sys
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading template: {str(e)}", 500

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.now().isoformat(),
        'message': 'Aplicación Flask funcionando correctamente',
        'port': os.getenv("PORT", "5000")
    })

@app.route('/api/info')
def info():
    return jsonify({
        'app_name': 'Prueba de Despliegue Railway',
        'version': '1.0.0',
        'framework': 'Flask',
        'deployment': 'Railway',
        'python_version': sys.version,
        'port': os.getenv("PORT", "5000")
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    print(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
