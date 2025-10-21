from flask import Flask, render_template, Response
import os
import cv2

app = Flask(__name__)

# Variable global para la cámara
camera = None

def get_camera():
    """Obtener la cámara"""
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
    return camera

def generate_frames():
    """Generar frames para el stream de video"""
    camera = get_camera()
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Codificar frame como JPEG
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