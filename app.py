from flask import Flask, render_template, Response, jsonify
import cv2
import threading
import time
import os

app = Flask(__name__)

# Variable global para la cámara
camera = None
camera_lock = threading.Lock()

def get_camera():
    """Obtiene la instancia de la cámara de forma thread-safe"""
    global camera
    with camera_lock:
        if camera is None:
            try:
                camera = cv2.VideoCapture(0)
                camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                camera.set(cv2.CAP_PROP_FPS, 30)
            except Exception as e:
                print(f"Error al inicializar la cámara: {e}")
                return None
        return camera

def release_camera():
    """Libera la cámara de forma thread-safe"""
    global camera
    with camera_lock:
        if camera is not None:
            camera.release()
            camera = None

def generate_frames():
    """Genera frames de la cámara para streaming"""
    while True:
        cam = get_camera()
        if cam is None:
            # Si no hay cámara disponible, enviamos un frame negro
            frame = cv2.imread('static/no_camera.jpg')
            if frame is None:
                # Crear un frame negro si no hay imagen de respaldo
                frame = cv2.zeros((480, 640, 3), dtype=cv2.uint8)
                cv2.putText(frame, "Camara no disponible", (50, 240), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        else:
            success, frame = cam.read()
            if not success:
                # Frame negro si no se puede leer de la cámara
                frame = cv2.zeros((480, 640, 3), dtype=cv2.uint8)
                cv2.putText(frame, "Error al leer camara", (50, 240), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Codificar el frame como JPEG
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Endpoint para el streaming de video"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_camera')
def start_camera():
    """Inicia la cámara"""
    try:
        cam = get_camera()
        if cam is not None and cam.isOpened():
            return jsonify({'status': 'success', 'message': 'Cámara iniciada correctamente'})
        else:
            return jsonify({'status': 'error', 'message': 'No se pudo iniciar la cámara'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error: {str(e)}'})

@app.route('/stop_camera')
def stop_camera():
    """Detiene la cámara"""
    try:
        release_camera()
        return jsonify({'status': 'success', 'message': 'Cámara detenida correctamente'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error: {str(e)}'})

@app.route('/camera_status')
def camera_status():
    """Verifica el estado de la cámara"""
    try:
        cam = get_camera()
        if cam is not None and cam.isOpened():
            return jsonify({'status': 'active', 'message': 'Cámara activa'})
        else:
            return jsonify({'status': 'inactive', 'message': 'Cámara inactiva'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error: {str(e)}'})

@app.route('/health')
def health():
    """Endpoint de salud para Railway"""
    return jsonify({'status': 'healthy', 'message': 'Aplicación funcionando correctamente'})

if __name__ == '__main__':
    # Crear directorio para archivos estáticos si no existe
    os.makedirs('static', exist_ok=True)
    
    # Obtener puerto de Railway o usar 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    
    print(f"Iniciando aplicación en puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
