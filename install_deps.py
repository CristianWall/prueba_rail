#!/usr/bin/env python3
"""
Script para instalar dependencias de manera segura en Railway
"""
import subprocess
import sys
import os

def run_command(cmd):
    """Ejecutar comando y manejar errores"""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {cmd}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {cmd}: {e}")
        print(f"stderr: {e.stderr}")
        return False

def install_dependencies():
    """Instalar dependencias paso a paso"""
    print("🚀 Instalando dependencias para Railway...")
    
    # Actualizar pip
    if not run_command("pip install --upgrade pip"):
        return False
    
    # Instalar dependencias básicas primero
    basic_deps = [
        "Flask==3.1.0",
        "gunicorn==23.0.0",
        "numpy==1.26.4",
        "Pillow==10.4.0",
        "requests==2.31.0"
    ]
    
    for dep in basic_deps:
        if not run_command(f"pip install {dep}"):
            print(f"⚠️  Falló instalación de {dep}, continuando...")
    
    # Instalar PyTorch CPU (más ligero)
    if not run_command("pip install torch==2.4.0+cpu torchvision==0.19.0+cpu --index-url https://download.pytorch.org/whl/cpu"):
        print("⚠️  Falló instalación de PyTorch CPU, intentando versión normal...")
        run_command("pip install torch==2.4.0 torchvision==0.19.0")
    
    # Instalar OpenCV
    if not run_command("pip install opencv-python-headless==4.10.0.84"):
        print("⚠️  Falló instalación de OpenCV, intentando versión más reciente...")
        run_command("pip install opencv-python-headless")
    
    # Instalar Ultralytics
    if not run_command("pip install ultralytics==8.3.0"):
        print("⚠️  Falló instalación de Ultralytics, intentando versión más reciente...")
        run_command("pip install ultralytics")
    
    print("✅ Instalación completada")
    return True

if __name__ == "__main__":
    success = install_dependencies()
    sys.exit(0 if success else 1)