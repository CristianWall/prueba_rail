#!/usr/bin/env python3
"""
Configuración específica para Railway
Optimiza el rendimiento y maneja errores de despliegue
"""

import os
import sys

def configure_railway():
    """Configurar variables de entorno para Railway"""
    
    # Configurar variables de entorno para Railway
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ.setdefault('PYTHONUNBUFFERED', '1')
    
    # Configurar logging
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Configurar OpenCV para Railway
    os.environ.setdefault('OPENCV_VIDEOIO_PRIORITY_MSMF', '0')
    
    print("🔧 Configuración de Railway aplicada")

def check_dependencies():
    """Verificar que las dependencias críticas estén disponibles"""
    critical_deps = ['flask', 'cv2', 'numpy', 'ultralytics']
    
    for dep in critical_deps:
        try:
            if dep == 'cv2':
                import cv2
            else:
                __import__(dep)
            print(f"✅ {dep} disponible")
        except ImportError as e:
            print(f"❌ {dep} no disponible: {e}")
            return False
    
    return True

def optimize_for_railway():
    """Optimizar la aplicación para Railway"""
    
    # Reducir el uso de memoria
    import gc
    gc.collect()
    
    # Configurar threading para Railway
    import threading
    threading.stack_size(65536)
    
    print("⚡ Optimizaciones para Railway aplicadas")

if __name__ == "__main__":
    configure_railway()
    check_dependencies()
    optimize_for_railway()
