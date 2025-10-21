#!/usr/bin/env python3
"""
Script de configuración específico para Railway
Maneja la instalación y configuración de dependencias
"""

import os
import sys
import subprocess

def install_dependencies():
    """Instalar dependencias específicas para Railway"""
    print("📦 Instalando dependencias para Railway...")
    
    # Dependencias básicas
    basic_deps = [
        "Flask==3.1.0",
        "gunicorn==23.0.0",
        "opencv-python-headless==4.10.0.84",
        "numpy==1.24.3",
        "Pillow==10.0.0"
    ]
    
    for dep in basic_deps:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
            print(f"✅ {dep} instalado")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando {dep}: {e}")
    
    # Dependencias de YOLO (versiones ligeras)
    yolo_deps = [
        "ultralytics==8.0.196",
        "torch==2.0.1",
        "torchvision==0.15.2"
    ]
    
    for dep in yolo_deps:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
            print(f"✅ {dep} instalado")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  {dep} no se pudo instalar: {e}")

def configure_environment():
    """Configurar variables de entorno para Railway"""
    print("🔧 Configurando entorno para Railway...")
    
    # Variables de entorno para Railway
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ.setdefault('PYTHONUNBUFFERED', '1')
    os.environ.setdefault('OPENCV_VIDEOIO_PRIORITY_MSMF', '0')
    
    print("✅ Variables de entorno configuradas")

def verify_setup():
    """Verificar que la configuración esté correcta"""
    print("🧪 Verificando configuración...")
    
    try:
        import flask
        print("✅ Flask disponible")
    except ImportError:
        print("❌ Flask no disponible")
        return False
    
    try:
        import cv2
        print("✅ OpenCV disponible")
    except ImportError:
        print("❌ OpenCV no disponible")
        return False
    
    try:
        import numpy
        print("✅ NumPy disponible")
    except ImportError:
        print("❌ NumPy no disponible")
        return False
    
    try:
        from ultralytics import YOLO
        print("✅ YOLO disponible")
    except ImportError:
        print("❌ YOLO no disponible")
        return False
    
    print("✅ Configuración verificada")
    return True

if __name__ == "__main__":
    print("🚀 Configurando aplicación para Railway...")
    
    configure_environment()
    install_dependencies()
    
    if verify_setup():
        print("🎉 Configuración completada exitosamente")
    else:
        print("❌ Error en la configuración")
        sys.exit(1)
