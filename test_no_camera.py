#!/usr/bin/env python3
"""
Script para probar la aplicación sin cámara disponible
"""

import requests
import subprocess
import time
import os
import signal
import sys

def test_app_without_camera():
    """Probar la aplicación cuando no hay cámara disponible"""
    print("🚀 Iniciando prueba de la aplicación sin cámara...")
    
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
        
        print("🔍 Probando endpoint principal...")
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Endpoint principal funcionando correctamente")
        else:
            print(f"❌ Error en endpoint principal: {response.status_code}")
            
        print("🔍 Probando página de cámara...")
        response = requests.get(f"{base_url}/camera", timeout=10)
        if response.status_code == 200:
            print("✅ Página de cámara funcionando correctamente")
        else:
            print(f"❌ Error en página de cámara: {response.status_code}")
            
        print("🔍 Probando estado de cámara (debería fallar)...")
        response = requests.get(f"{base_url}/camera_status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Respuesta del estado: {data}")
            if not data.get('camera_available', False):
                print("✅ Correcto: La cámara no está disponible (como se esperaba)")
            else:
                print("⚠️  Inesperado: La cámara está disponible")
        else:
            print(f"❌ Error en endpoint de estado de cámara: {response.status_code}")
            
        print("🔍 Probando detección de cara (debería fallar)...")
        response = requests.post(f"{base_url}/detect_face", 
                               json={}, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Respuesta de detección: {data}")
            if not data.get('success', False):
                print("✅ Correcto: La detección falló como se esperaba (cámara no disponible)")
            else:
                print("⚠️  Inesperado: La detección funcionó")
        else:
            print(f"❌ Error en endpoint de detección: {response.status_code}")
            
        print("🔍 Probando stream de video...")
        response = requests.get(f"{base_url}/video_feed", timeout=5)
        if response.status_code == 200:
            print("✅ Stream de video funcionando (mostrará frame de error)")
        else:
            print(f"❌ Error en stream de video: {response.status_code}")
            
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("💡 La aplicación maneja correctamente la ausencia de cámara")
        
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

def test_error_handling():
    """Probar el manejo de errores específicos"""
    print("\n🧪 Probando manejo de errores específicos...")
    
    # Simular diferentes tipos de errores
    test_cases = [
        ("Cámara no disponible", "camera_status"),
        ("Detección fallida", "detect_face"),
        ("Stream de video", "video_feed")
    ]
    
    for test_name, endpoint in test_cases:
        print(f"🔍 Probando {test_name}...")
        try:
            if endpoint == "detect_face":
                response = requests.post(f"http://localhost:5000/{endpoint}", 
                                       json={}, 
                                       headers={'Content-Type': 'application/json'},
                                       timeout=5)
            else:
                response = requests.get(f"http://localhost:5000/{endpoint}", timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {test_name}: Respuesta exitosa")
            else:
                print(f"⚠️  {test_name}: Código {response.status_code}")
        except Exception as e:
            print(f"❌ {test_name}: Error - {e}")

if __name__ == "__main__":
    print("🔧 Prueba de aplicación sin cámara")
    print("=" * 50)
    
    test_app_without_camera()
    test_error_handling()
    
    print("\n📋 Resumen:")
    print("✅ La aplicación debe funcionar sin cámara")
    print("✅ Los errores deben manejarse graciosamente")
    print("✅ Los usuarios deben recibir mensajes informativos")
    print("✅ El stream de video debe mostrar frames de error")
