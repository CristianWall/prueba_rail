from flask import Flask, render_template, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.now().isoformat(),
        'message': 'Aplicación Flask funcionando correctamente'
    })

@app.route('/api/info')
def info():
    return jsonify({
        'app_name': 'Prueba de Despliegue Railway',
        'version': '1.0.0',
        'framework': 'Flask',
        'deployment': 'Railway',
        'python_version': os.sys.version
    })

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
