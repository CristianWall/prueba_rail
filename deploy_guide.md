# Guía de Despliegue - Detección de Caras

## 🚨 Problema de Dependencias Resuelto

El error que experimentaste se debe a incompatibilidades entre las versiones de las dependencias y Python 3.13. He creado varias soluciones:

## 📋 Opciones de Solución

### Opción 1: Usar requirements-stable.txt (Recomendado)
```bash
# En lugar de requirements.txt, usa:
pip install -r requirements-stable.txt
```

### Opción 2: Instalación Manual
```bash
# Instalar dependencias básicas primero
pip install Flask==3.1.0 gunicorn==23.0.0

# Luego las dependencias de visión
pip install opencv-python-headless numpy Pillow
```

### Opción 3: Usar el Script de Instalación
```bash
python install_deps.py
```

## 🔧 Cambios Realizados

### 1. **requirements.txt** - Versión corregida
- Cambié `opencv-python` por `opencv-python-headless` (mejor para servidores)
- Actualicé las versiones de numpy y Pillow para compatibilidad con Python 3.13
- Agregué rangos de versiones más flexibles

### 2. **requirements-stable.txt** - Versión sin restricciones
- Versiones sin fijar para máxima compatibilidad
- Ideal para entornos de despliegue

### 3. **install_deps.py** - Script de instalación robusta
- Instalación incremental de dependencias
- Manejo de errores y fallbacks
- Pruebas de importación automáticas

### 4. **Dockerfile.alternative** - Para contenedores
- Usa Python 3.11 (más estable)
- Instala dependencias del sistema necesarias
- Configuración optimizada para OpenCV

## 🚀 Para Desplegar

### Railway/Heroku:
```bash
# Usar requirements-stable.txt en lugar de requirements.txt
# O cambiar el nombre del archivo:
mv requirements-stable.txt requirements.txt
```

### Docker:
```bash
# Usar el Dockerfile alternativo:
docker build -f Dockerfile.alternative -t face-detection-app .
docker run -p 8080:8080 face-detection-app
```

### Local:
```bash
# Opción 1: Script automático
python install_deps.py

# Opción 2: Manual
pip install -r requirements-stable.txt
python app.py
```

## ✅ Verificación

Después de la instalación, verifica que funciona:
```bash
python test_local.py
```

## 🎯 Funcionalidades Disponibles

- ✅ Detección de caras en tiempo real
- ✅ Stream de video en vivo
- ✅ API endpoints para detección
- ✅ Interfaz web moderna
- ✅ Compatible con despliegue en la nube

## 📞 Si Aún Hay Problemas

1. **Usa Python 3.11** en lugar de 3.13
2. **Usa requirements-stable.txt**
3. **Ejecuta install_deps.py** para instalación robusta
4. **Verifica que la cámara esté disponible** en el entorno de despliegue
