from flask import Flask, render_template, Response
import os
import cv2
import numpy as np

app = Flask(__name__)

# Variable global para la cámara
camera = None

def get_camera():
    """Obtener la cámara"""
    global camera
    if camera is None:
        try:
            camera = cv2.VideoCapture(0)
            # Probar si la cámara funciona
            success, frame = camera.read()
            if not success:
                camera = None
        except:
            camera = None
    return camera

def create_demo_frame():
    """Crear un frame de demostración cuando no hay cámara"""
    # Crear un frame de 640x480 con un patrón
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Agregar un patrón de colores
    for i in range(0, 480, 20):
        for j in range(0, 640, 20):
            color = (i + j) % 255
            frame[i:i+20, j:j+20] = [color, (color + 50) % 255, (color + 100) % 255]
    
    # Agregar texto
    cv2.putText(frame, "Cámara no disponible en Railway", (50, 240), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, "Demo Frame - Funciona localmente", (50, 280), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
    
    return frame

def generate_frames():
    """Generar frames para el stream de video"""
    camera = get_camera()
    
    if camera is None:
        # En Railway no hay cámara, mostrar frame de demo
        while True:
            demo_frame = create_demo_frame()
            ret, buffer = cv2.imencode('.jpg', demo_frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    else:
        # Cámara disponible (desarrollo local)
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
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
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)