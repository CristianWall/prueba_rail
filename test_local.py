#!/usr/bin/env python3
"""
Script para probar la aplicación Flask localmente
"""

import requests
import subprocess
import time
import os
import signal
import sys

def test_app():
    """Prueba la aplicación Flask localmente"""
    print("🚀 Iniciando prueba de la aplicación...")
    
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
            
        print("🔍 Probando endpoint de salud...")
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Endpoint de salud funcionando correctamente")
            print(f"📊 Respuesta: {response.json()}")
        else:
            print(f"❌ Error en endpoint de salud: {response.status_code}")
            
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        
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

if __name__ == "__main__":
    test_app()
