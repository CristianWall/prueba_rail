from flask import Flask, render_template, Response, jsonify
import threading
import time
import os
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests

app = Flask(__name__)

# Variable global para el estado de la cámara
camera_active = False
camera_lock = threading.Lock()

# Intentar importar OpenCV, si falla usar alternativa
try:
    import cv2
    OPENCV_AVAILABLE = True
    print("OpenCV disponible")
except ImportError as e:
    OPENCV_AVAILABLE = False
    print(f"OpenCV no disponible: {e}")
except Exception as e:
    OPENCV_AVAILABLE = False
    print(f"Error al importar OpenCV: {e}")
    print("Usando modo demostración sin OpenCV")

def get_camera():
    """Obtiene la instancia de la cámara de forma thread-safe"""
    global camera_active
    if not OPENCV_AVAILABLE:
        return None
    
    try:
        camera = cv2.VideoCapture(0)
        if camera.isOpened():
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            camera.set(cv2.CAP_PROP_FPS, 30)
            return camera
        else:
            return None
    except Exception as e:
        print(f"Error al inicializar la cámara: {e}")
        return None

def release_camera():
    """Libera la cámara de forma thread-safe"""
    global camera_active
    with camera_lock:
        camera_active = False

def create_placeholder_frame(message="Cámara no disponible"):
    """Crea un frame de placeholder usando PIL"""
    # Crear una imagen de 640x480
    img = Image.new('RGB', (640, 480), color='black')
    draw = ImageDraw.Draw(img)
    
    # Intentar usar una fuente, si no está disponible usar la por defecto
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
    
    # Obtener el tamaño del texto
    bbox = draw.textbbox((0, 0), message, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Centrar el texto
    x = (640 - text_width) // 2
    y = (480 - text_height) // 2
    
    draw.text((x, y), message, fill='white', font=font)
    
    # Convertir a bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG', quality=80)
    img_bytes.seek(0)
    return img_bytes.getvalue()

def create_demo_frame(message="Demo - Cámara Simulada", frame_count=0):
    """Crea un frame de demostración usando PIL"""
    # Crear una imagen de 640x480
    img = Image.new('RGB', (640, 480), color=(20, 20, 40))
    draw = ImageDraw.Draw(img)
    
    # Crear un patrón de fondo animado
    for i in range(0, 640, 20):
        for j in range(0, 480, 20):
            color_intensity = int(50 + 30 * (i + j + frame_count) % 100 / 100)
            draw.rectangle([i, j, i+19, j+19], fill=(color_intensity, color_intensity//2, color_intensity//3))
    
    # Intentar usar una fuente, si no está disponible usar la por defecto
    try:
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Dibujar el mensaje principal
    bbox = draw.textbbox((0, 0), message, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (640 - text_width) // 2
    y = (480 - text_height) // 2 - 30
    
    draw.text((x, y), message, fill='white', font=font_large)
    
    # Dibujar información adicional
    info_text = f"Frame: {frame_count} | Tiempo: {time.strftime('%H:%M:%S')}"
    bbox_info = draw.textbbox((0, 0), info_text, font=font_small)
    info_width = bbox_info[2] - bbox_info[0]
    info_x = (640 - info_width) // 2
    info_y = y + text_height + 20
    
    draw.text((info_x, info_y), info_text, fill='lightblue', font=font_small)
    
    # Dibujar un círculo animado
    circle_x = 320 + int(100 * (frame_count % 60) / 60)
    circle_y = 200 + int(50 * (frame_count % 40) / 40)
    draw.ellipse([circle_x-20, circle_y-20, circle_x+20, circle_y+20], fill='red', outline='white', width=2)
    
    # Convertir a bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG', quality=80)
    img_bytes.seek(0)
    return img_bytes.getvalue()

def generate_frames():
    """Genera frames de la cámara para streaming"""
    frame_count = 0
    while True:
        if not OPENCV_AVAILABLE:
            # Si OpenCV no está disponible, crear frame de demostración
            frame_bytes = create_demo_frame("Modo Demostración - Sin OpenCV", frame_count)
        else:
            cam = get_camera()
            if cam is None or not cam.isOpened():
                frame_bytes = create_demo_frame("Cámara no disponible", frame_count)
            else:
                try:
                    success, frame = cam.read()
                    if not success:
                        frame_bytes = create_demo_frame("Error al leer cámara", frame_count)
                    else:
                        # Codificar el frame como JPEG
                        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                        if not ret:
                            frame_bytes = create_demo_frame("Error al codificar frame", frame_count)
                        else:
                            frame_bytes = buffer.tobytes()
                except Exception as e:
                    print(f"Error en generate_frames: {e}")
                    frame_bytes = create_demo_frame(f"Error: {str(e)}", frame_count)
        
        frame_count += 1
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        # Pequeña pausa para simular FPS
        time.sleep(0.033)  # ~30 FPS

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
    global camera_active
    try:
        if not OPENCV_AVAILABLE:
            return jsonify({
                'status': 'warning', 
                'message': 'OpenCV no disponible. Usando modo simulación.'
            })
        
        with camera_lock:
            camera_active = True
        
        cam = get_camera()
        if cam is not None and cam.isOpened():
            return jsonify({'status': 'success', 'message': 'Cámara iniciada correctamente'})
        else:
            return jsonify({'status': 'warning', 'message': 'Cámara no disponible, usando modo simulación'})
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
        if not OPENCV_AVAILABLE:
            return jsonify({
                'status': 'simulation', 
                'message': 'Modo simulación - OpenCV no disponible'
            })
        
        with camera_lock:
            if camera_active:
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
