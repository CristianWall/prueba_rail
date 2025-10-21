# Sistema de Detección de Chalecos de Seguridad

Aplicación web para detectar chalecos de seguridad en tiempo real usando YOLO.

## Características

- ✅ Detección automática de chalecos de seguridad
- ✅ Clasificación: CON chaleco vs SIN chaleco  
- ✅ Análisis en tiempo real con cámara web
- ✅ Interfaz web moderna y responsive

## Despliegue en Railway

Esta aplicación está configurada para desplegarse automáticamente en Railway.

### Estructura del proyecto

```
prueba_despliegue/
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias Python
├── Procfile              # Configuración para Railway
├── nixpacks.toml         # Configuración de build
├── templates/            # Plantillas HTML
│   ├── index.html
│   └── camera.html
├── static/               # Archivos estáticos
│   ├── css/
│   └── images/
└── modelo_entrenado/     # Modelo YOLO entrenado
    └── chaleco_detection/
        └── weights/
            └── best.pt
```

### Funcionalidades

1. **Página principal** (`/`): Información del sistema
2. **Detección en tiempo real** (`/camera`): Stream de video con detección
3. **API de salud** (`/health`): Estado del sistema para Railway
4. **Detección de imágenes** (`/detect_vest`): Upload de imágenes para análisis

### Requisitos

- Python 3.8+
- PyTorch 2.4.0
- Ultralytics YOLO 8.3.0
- OpenCV
- Flask

La aplicación funciona tanto con cámara como sin ella, adaptándose automáticamente al entorno.
