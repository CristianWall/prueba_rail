#!/usr/bin/env python3
"""
Script para instalar dependencias de manera más robusta
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Ejecutar comando y manejar errores"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"Salida de error: {e.stderr}")
        return False

def install_dependencies():
    """Instalar dependencias de manera incremental"""
    print("🚀 Iniciando instalación de dependencias...")
    
    # Actualizar pip primero
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Actualizando pip"):
        return False
    
    # Instalar dependencias básicas primero
    basic_deps = [
        "Flask==3.1.0",
        "gunicorn==23.0.0",
        "Werkzeug==3.1.3",
        "Jinja2==3.1.5",
        "MarkupSafe==3.0.2",
        "itsdangerous==2.2.0",
        "click==8.1.8",
        "blinker==1.9.0"
    ]
    
    for dep in basic_deps:
        if not run_command(f"{sys.executable} -m pip install {dep}", f"Instalando {dep}"):
            print(f"⚠️  Continuando sin {dep}")
    
    # Instalar numpy con versión específica
    if not run_command(f"{sys.executable} -m pip install 'numpy>=1.26.0,<2.0.0'", "Instalando numpy"):
        print("⚠️  Intentando instalar numpy sin restricciones de versión...")
        run_command(f"{sys.executable} -m pip install numpy", "Instalando numpy (sin restricciones)")
    
    # Instalar Pillow
    if not run_command(f"{sys.executable} -m pip install 'Pillow>=10.0.0,<11.0.0'", "Instalando Pillow"):
        print("⚠️  Intentando instalar Pillow sin restricciones de versión...")
        run_command(f"{sys.executable} -m pip install Pillow", "Instalando Pillow (sin restricciones)")
    
    # Instalar OpenCV (versión headless para mejor compatibilidad)
    if not run_command(f"{sys.executable} -m pip install opencv-python-headless==4.10.0.84", "Instalando OpenCV"):
        print("⚠️  Intentando instalar OpenCV sin versión específica...")
        run_command(f"{sys.executable} -m pip install opencv-python-headless", "Instalando OpenCV (sin restricciones)")
    
    # Instalar dependencias adicionales
    additional_deps = ["colorama==0.4.6", "packaging==24.2"]
    for dep in additional_deps:
        run_command(f"{sys.executable} -m pip install {dep}", f"Instalando {dep}")
    
    print("🎉 Instalación de dependencias completada")
    return True

def test_imports():
    """Probar que las importaciones funcionan"""
    print("🧪 Probando importaciones...")
    
    try:
        import flask
        print("✅ Flask importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Flask: {e}")
        return False
    
    try:
        import cv2
        print("✅ OpenCV importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando OpenCV: {e}")
        return False
    
    try:
        import numpy
        print("✅ NumPy importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando NumPy: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Pillow: {e}")
        return False
    
    print("🎉 Todas las importaciones funcionan correctamente")
    return True

if __name__ == "__main__":
    print("🔧 Instalador de dependencias para detección de caras")
    print("=" * 50)
    
    if install_dependencies():
        if test_imports():
            print("\n🎉 ¡Instalación exitosa! Todas las dependencias están funcionando.")
        else:
            print("\n⚠️  Instalación completada pero algunas importaciones fallaron.")
    else:
        print("\n❌ La instalación falló. Revisa los errores anteriores.")
        sys.exit(1)
