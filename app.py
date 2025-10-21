from flask import Flask, render_template, Response, jsonify
import os
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Inicializar el detector de caras
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Variable global para la cámara
camera = None

def get_camera():
    """Obtener o inicializar la cámara"""
    global camera
    if camera is None:
        try:
            camera = cv2.VideoCapture(0)
            if not camera.isOpened():
                # Intentar con diferentes índices de cámara
                for i in range(1, 5):
                    camera = cv2.VideoCapture(i)
                    if camera.isOpened():
                        break
                else:
                    camera = None
                    return None
            
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        except Exception as e:
            print(f"Error inicializando cámara: {e}")
            camera = None
            return None
    return camera

def detect_faces(frame):
    """Detectar caras en el frame"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, 'Cara Detectada', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    
    return frame, len(faces)

def generate_frames():
    """Generar frames para el stream de video"""
    camera = get_camera()
    if camera is None:
        # Generar frame de error si no hay cámara
        error_frame = create_error_frame("Cámara no disponible")
        while True:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + error_frame + b'\r\n')
    
    while True:
        try:
            success, frame = camera.read()
            if not success:
                # Generar frame de error
                error_frame = create_error_frame("Error capturando video")
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + error_frame + b'\r\n')
                break
            else:
                # Detectar caras
                frame_with_faces, face_count = detect_faces(frame)
                
                # Codificar frame como JPEG
                ret, buffer = cv2.imencode('.jpg', frame_with_faces)
                frame_bytes = buffer.tobytes()
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        except Exception as e:
            print(f"Error en generate_frames: {e}")
            error_frame = create_error_frame(f"Error: {str(e)}")
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + error_frame + b'\r\n')
            break

def create_error_frame(message):
    """Crear un frame de error cuando la cámara no está disponible"""
    import numpy as np
    
    # Crear frame negro
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Agregar texto de error
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (0, 0, 255)  # Rojo
    thickness = 2
    
    # Calcular posición del texto (centrado)
    text_size = cv2.getTextSize(message, font, font_scale, thickness)[0]
    x = (640 - text_size[0]) // 2
    y = (480 + text_size[1]) // 2
    
    cv2.putText(frame, message, (x, y), font, font_scale, color, thickness)
    cv2.putText(frame, "Verifica que la camara este conectada", (x-50, y+40), font, 0.7, (255, 255, 255), 1)
    
    # Codificar como JPEG
    _, buffer = cv2.imencode('.jpg', frame)
    return buffer.tobytes()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

@app.route("/camera")
def camera_page():
    return render_template("camera.html")

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/detect_face", methods=['POST'])
def detect_face():
    """Endpoint para detección de cara desde imagen"""
    try:
        camera = get_camera()
        if camera is None:
            return jsonify({
                "success": False, 
                "error": "Cámara no disponible. Verifica que esté conectada y no esté siendo usada por otra aplicación."
            })
        
        success, frame = camera.read()
        if success:
            frame_with_faces, face_count = detect_faces(frame)
            
            # Convertir a base64 para enviar como JSON
            _, buffer = cv2.imencode('.jpg', frame_with_faces)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return jsonify({
                "success": True,
                "face_count": face_count,
                "image": img_base64
            })
        else:
            return jsonify({
                "success": False, 
                "error": "No se pudo capturar imagen de la cámara"
            })
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": f"Error en detección: {str(e)}"
        })

@app.route("/camera_status")
def camera_status():
    """Verificar estado de la cámara"""
    try:
        camera = get_camera()
        success, frame = camera.read()
        return jsonify({
            "camera_available": success,
            "message": "Cámara funcionando" if success else "Cámara no disponible"
        })
    except Exception as e:
        return jsonify({
            "camera_available": False,
            "message": f"Error: {str(e)}"
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)