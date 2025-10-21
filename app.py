from flask import Flask, render_template, request, jsonify, Response
import os
import cv2
import numpy as np
from ultralytics import YOLO
import threading
import time
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Cargar el modelo YOLO entrenado
model_path = os.path.join('modelo_entrenado', 'chaleco_detection', 'weights', 'best.pt')
model = None
camera = None
camera_lock = threading.Lock()

def load_model():
    """Cargar el modelo YOLO de detección de chalecos"""
    global model
    try:
        if os.path.exists(model_path):
            model = YOLO(model_path)
            print(f"✅ Modelo cargado exitosamente desde: {model_path}")
            return True
        else:
            print(f"❌ No se encontró el modelo en: {model_path}")
            return False
    except Exception as e:
        print(f"❌ Error cargando el modelo: {e}")
        return False

def init_camera():
    """Inicializar la cámara"""
    global camera
    try:
        # En Railway, la cámara puede no estar disponible
        camera = cv2.VideoCapture(0)
        if camera.isOpened():
            print("✅ Cámara inicializada correctamente")
            return True
        else:
            print("⚠️  Cámara no disponible (normal en Railway)")
            camera = None
            return False
    except Exception as e:
        print(f"⚠️  Cámara no disponible: {e}")
        camera = None
        return False

def detect_vests(frame):
    """Detectar chalecos de seguridad en un frame"""
    if model is None:
        return frame, []
    
    try:
        # Realizar detección
        results = model(frame, conf=0.5)  # Umbral de confianza 0.5
        
        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # Obtener coordenadas y confianza
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = box.conf[0].cpu().numpy()
                    class_id = int(box.cls[0].cpu().numpy())
                    
                    # Obtener nombre de la clase
                    class_name = model.names[class_id]
                    
                    # Dibujar bounding box
                    color = (0, 255, 0) if class_name == 'con_chaleco' else (0, 0, 255)
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                    
                    # Agregar etiqueta
                    label = f"{class_name}: {confidence:.2f}"
                    cv2.putText(frame, label, (int(x1), int(y1)-10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    
                    detections.append({
                        'class': class_name,
                        'confidence': float(confidence),
                        'bbox': [int(x1), int(y1), int(x2), int(y2)]
                    })
        
        return frame, detections
    except Exception as e:
        print(f"Error en detección: {e}")
        return frame, []

def generate_frames():
    """Generar frames para el stream de video"""
    global camera
    while True:
        with camera_lock:
            if camera is None or not camera.isOpened():
                # Crear frame de error
                error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(error_frame, "Camara no disponible", (50, 240), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                ret, buffer = cv2.imencode('.jpg', error_frame)
                if ret:
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                time.sleep(0.1)
                continue
            
            success, frame = camera.read()
            if not success:
                continue
            
            # Detectar chalecos
            frame_with_detections, detections = detect_vests(frame)
            
            # Codificar frame
            ret, buffer = cv2.imencode('.jpg', frame_with_detections)
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/camera")
def camera_page():
    return render_template("camera.html")

@app.route("/video_feed")
def video_feed():
    """Stream de video con detección de chalecos"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/camera_status")
def camera_status():
    """Verificar estado de la cámara"""
    global camera
    try:
        if camera is not None and camera.isOpened():
            return jsonify({
                'camera_available': True,
                'message': 'Cámara funcionando correctamente'
            })
        else:
            return jsonify({
                'camera_available': False,
                'message': 'Cámara no disponible'
            })
    except Exception as e:
        return jsonify({
            'camera_available': False,
            'message': f'Error: {str(e)}'
        })

@app.route("/detect_vest", methods=['POST'])
def detect_vest():
    """Detectar chalecos en una imagen"""
    global model
    try:
        if model is None:
            return jsonify({
                'success': False,
                'error': 'Modelo no cargado'
            })
        
        # Obtener imagen del request
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó imagen'
            })
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Archivo vacío'
            })
        
        # Leer imagen
        image_bytes = file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Detectar chalecos
        frame_with_detections, detections = detect_vests(image)
        
        # Convertir resultado a base64
        _, buffer = cv2.imencode('.jpg', frame_with_detections)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'success': True,
            'detections': detections,
            'image_with_detections': img_base64,
            'total_detections': len(detections)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route("/health")
def health():
    """Endpoint de salud"""
    model_status = "loaded" if model is not None else "not_loaded"
    camera_status = "available" if camera is not None and camera.isOpened() else "not_available"
    
    return jsonify({
        'status': 'healthy',
        'model': model_status,
        'camera': camera_status,
        'timestamp': time.time()
    })

# Inicializar modelo y cámara al importar
print("🚀 Iniciando aplicación de detección de chalecos...")

# Cargar modelo
if load_model():
    print("✅ Modelo de detección de chalecos cargado")
else:
    print("⚠️  Modelo no disponible - la aplicación funcionará sin detección")

# Inicializar cámara
if init_camera():
    print("✅ Cámara inicializada")
else:
    print("⚠️  Cámara no disponible - la aplicación funcionará sin cámara")

# Inicializar modelo y cámara al arrancar
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Iniciando servidor en puerto {port}")
    app.run(host="0.0.0.0", port=port, debug=False)