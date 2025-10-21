#!/usr/bin/env python3
"""
Script para probar las correcciones de manejo de cámara
"""

import requests
import subprocess
import time
import os
import signal
import sys

def test_camera_handling():
    """Probar el manejo de cámara mejorado"""
    print("🚀 Iniciando prueba de manejo de cámara...")
    
    # Configurar variables de entorno
    os.environ['PORT'] = '5000'
    
    try:
        # Iniciar la aplicación en segundo plano
        print("📦 Iniciando servidor Flask...")
        process = subprocess.Popen([
            sys.executable, 'app.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar a que el servidor se inicie
        print("⏳ Esperando a que el servidor se inicie...")
        time.sleep(3)
        
        # Probar endpoints
        base_url = "http://localhost:5000"
        
        print("🔍 Probando estado de cámara...")
        response = requests.get(f"{base_url}/camera_status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Respuesta del estado: {data}")
            
            if data.get('camera_available', False):
                print("✅ Cámara disponible - probando detección...")
                test_face_detection(base_url)
            else:
                print("⚠️  Cámara no disponible - probando manejo de errores...")
                test_error_handling(base_url)
        else:
            print(f"❌ Error en endpoint de estado: {response.status_code}")
            
        print("🔍 Probando stream de video...")
        try:
            response = requests.get(f"{base_url}/video_feed", timeout=5)
            if response.status_code == 200:
                print("✅ Stream de video funcionando (puede mostrar frame de error)")
            else:
                print(f"❌ Error en stream de video: {response.status_code}")
        except requests.exceptions.Timeout:
            print("⚠️  Stream de video timeout (normal para streams largos)")
            
        print("🎉 ¡Pruebas completadas!")
        
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor. Verifica que la aplicación esté ejecutándose.")
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
    finally:
        # Terminar el proceso
        if 'process' in locals():
            process.terminate()
            process.wait()
            print("🛑 Servidor detenido")

def test_face_detection(base_url):
    """Probar detección de caras cuando la cámara está disponible"""
    print("🔍 Probando detección de caras...")
    try:
        response = requests.post(f"{base_url}/detect_face", 
                               json={}, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Respuesta de detección: {data}")
            if data.get('success', False):
                print("✅ Detección funcionando correctamente")
            else:
                print(f"⚠️  Detección falló: {data.get('error', 'Error desconocido')}")
        else:
            print(f"❌ Error en detección: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en detección: {e}")

def test_error_handling(base_url):
    """Probar manejo de errores cuando no hay cámara"""
    print("🔍 Probando manejo de errores...")
    try:
        response = requests.post(f"{base_url}/detect_face", 
                               json={}, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Respuesta de detección: {data}")
            if not data.get('success', False) and not data.get('camera_available', True):
                print("✅ Manejo de errores funcionando correctamente")
            else:
                print("⚠️  Manejo de errores inesperado")
        else:
            print(f"❌ Error en detección: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en detección: {e}")

def test_endpoints():
    """Probar todos los endpoints básicos"""
    print("\n🧪 Probando endpoints básicos...")
    
    endpoints = [
        ("/", "Página principal"),
        ("/health", "Endpoint de salud"),
        ("/camera", "Página de cámara"),
        ("/camera_status", "Estado de cámara")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"http://localhost:5000{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {description}: OK")
            else:
                print(f"⚠️  {description}: Código {response.status_code}")
        except Exception as e:
            print(f"❌ {description}: Error - {e}")

if __name__ == "__main__":
    print("🔧 Prueba de correcciones de cámara")
    print("=" * 50)
    
    test_camera_handling()
    test_endpoints()
    
    print("\n📋 Resumen:")
    print("✅ La aplicación debe manejar correctamente la ausencia de cámara")
    print("✅ Los errores deben ser informativos y no causar crashes")
    print("✅ El stream de video debe mostrar frames de error cuando no hay cámara")
    print("✅ Los endpoints deben responder correctamente en todos los casos")
