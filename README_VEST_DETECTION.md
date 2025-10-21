# 🦺 Sistema de Detección de Chalecos de Seguridad

## 📋 Descripción

Sistema de detección automática de chalecos de seguridad en tiempo real utilizando YOLOv8 y Flask. El sistema puede identificar si una persona lleva chaleco de seguridad o no, con visualización en tiempo real y métricas de confianza.

## 🚀 Características

- ✅ **Detección en Tiempo Real**: Análisis continuo del video de la cámara
- ✅ **Clasificación Binaria**: CON chaleco vs SIN chaleco
- ✅ **Interfaz Web Moderna**: Dashboard responsive con visualización en vivo
- ✅ **Métricas de Confianza**: Nivel de certeza para cada detección
- ✅ **Manejo de Errores**: Funciona sin cámara o modelo
- ✅ **API RESTful**: Endpoints para integración con otros sistemas
- ✅ **Despliegue en la Nube**: Compatible con Railway, Heroku, etc.

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cámara Web    │───▶│   Flask App     │───▶│   YOLO Model    │
│                 │    │                 │    │   (Chalecos)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Web Browser   │
                       │   (Frontend)    │
                       └─────────────────┘
```

## 📁 Estructura del Proyecto

```
prueba_despliegue/
├── app.py                          # Aplicación Flask principal
├── requirements.txt                 # Dependencias básicas
├── requirements-stable.txt         # Dependencias estables
├── modelo_entrenado/
│   └── chaleco_detection/
│       ├── weights/
│       │   └── best.pt            # Modelo YOLO entrenado
│       └── data.yaml              # Configuración del modelo
├── templates/
│   ├── index.html                 # Página principal
│   └── camera.html                # Página de detección
├── static/
│   ├── css/styles.css             # Estilos
│   └── images/                    # Imágenes estáticas
├── test_vest_detection.py          # Script de pruebas
└── README_VEST_DETECTION.md        # Este archivo
```

## 🔧 Instalación

### Opción 1: Instalación Rápida
```bash
# Instalar dependencias
pip install -r requirements-stable.txt

# Ejecutar la aplicación
python app.py
```

### Opción 2: Instalación Robusta
```bash
# Usar el script de instalación
python install_deps.py

# Ejecutar la aplicación
python app.py
```

### Opción 3: Instalación Manual
```bash
# Dependencias básicas
pip install Flask==3.1.0 gunicorn==23.0.0

# Dependencias de visión
pip install ultralytics torch torchvision
pip install opencv-python-headless numpy Pillow

# Ejecutar la aplicación
python app.py
```

## 🚀 Uso

### 1. Iniciar la Aplicación
```bash
python app.py
```

### 2. Acceder a la Interfaz
- Abrir navegador en: `http://localhost:5000`
- Hacer clic en "🦺 Detección de Chalecos en Tiempo Real"
- Permitir acceso a la cámara cuando se solicite

### 3. Usar la Detección
- Hacer clic en "📹 Iniciar Detección"
- El sistema comenzará a analizar el video en tiempo real
- Las detecciones aparecerán con:
  - **Verde**: Persona CON chaleco de seguridad
  - **Rojo**: Persona SIN chaleco de seguridad

## 🔌 API Endpoints

### GET `/`
Página principal del sistema

### GET `/camera`
Página de detección en tiempo real

### GET `/video_feed`
Stream de video con detecciones (MJPEG)

### GET `/camera_status`
Estado de la cámara
```json
{
  "camera_available": true,
  "message": "Cámara funcionando correctamente"
}
```

### GET `/health`
Estado del sistema
```json
{
  "status": "healthy",
  "model": "loaded",
  "camera": "available",
  "timestamp": 1699123456.789
}
```

### POST `/detect_vest`
Detectar chalecos en una imagen
```json
{
  "success": true,
  "detections": [
    {
      "class": "con_chaleco",
      "confidence": 0.85,
      "bbox": [100, 150, 200, 300]
    }
  ],
  "total_detections": 1
}
```

## 🧪 Pruebas

### Ejecutar Pruebas Completas
```bash
python test_vest_detection.py
```

### Pruebas Específicas
```bash
# Probar sin cámara
python test_no_camera.py

# Probar correcciones de cámara
python test_camera_fixes.py

# Probar localmente
python test_local.py
```

## 📊 Modelo YOLO

### Características del Modelo
- **Arquitectura**: YOLOv8n (nano)
- **Clases**: 2 (sin_chaleco, con_chaleco)
- **Tamaño de imagen**: 416x416 píxeles
- **Umbral de confianza**: 0.5
- **Métricas de entrenamiento**:
  - Precisión: ~75%
  - Recall: ~66%
  - mAP50: ~70%

### Uso del Modelo
```python
from ultralytics import YOLO

# Cargar modelo
model = YOLO('modelo_entrenado/chaleco_detection/weights/best.pt')

# Realizar detección
results = model('imagen.jpg', conf=0.5)

# Procesar resultados
for result in results:
    boxes = result.boxes
    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            confidence = box.conf[0]
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
```

## 🚀 Despliegue

### Railway
```bash
# Usar requirements-stable.txt
# Configurar Procfile
# Desplegar automáticamente
```

### Heroku
```bash
# Crear Procfile
# Configurar buildpacks
# Desplegar con Git
```

### Docker
```bash
# Usar Dockerfile.alternative
docker build -f Dockerfile.alternative -t vest-detection .
docker run -p 8080:8080 vest-detection
```

## 🔧 Configuración

### Variables de Entorno
- `PORT`: Puerto del servidor (default: 5000)
- `DEBUG`: Modo debug (default: False)

### Parámetros del Modelo
- `conf`: Umbral de confianza (default: 0.5)
- `imgsz`: Tamaño de imagen (default: 416)

## 🐛 Solución de Problemas

### Error: "Modelo no cargado"
- Verificar que `best.pt` existe en la ruta correcta
- Revisar permisos de archivos
- Verificar que ultralytics está instalado

### Error: "Cámara no disponible"
- Verificar que la cámara esté conectada
- Revisar permisos de acceso a la cámara
- Probar con `cv2.VideoCapture(0)` en Python

### Error: "Dependencias faltantes"
```bash
# Reinstalar dependencias
pip install -r requirements-stable.txt

# O usar el script de instalación
python install_deps.py
```

## 📈 Mejoras Futuras

- [ ] Detección de múltiples personas
- [ ] Almacenamiento de detecciones en base de datos
- [ ] Notificaciones en tiempo real
- [ ] Dashboard de estadísticas
- [ ] Integración con sistemas de seguridad
- [ ] Detección de otros EPIs (cascos, guantes, etc.)

## 📞 Soporte

Para problemas o preguntas:
1. Revisar los logs de la aplicación
2. Ejecutar `python test_vest_detection.py`
3. Verificar que todas las dependencias estén instaladas
4. Comprobar que el modelo esté en la ruta correcta

---

*Sistema desarrollado con YOLOv8, Flask y OpenCV para detección de chalecos de seguridad en tiempo real.*
