#!/usr/bin/env python3
"""
Script simple para probar la aplicación localmente
"""

import requests
import time

def test_app():
    """Probar la aplicación"""
    print("🧪 Probando aplicación de detección de chalecos...")
    
    base_url = "http://localhost:5000"
    
    try:
        # Probar endpoint de salud
        print("1. Probando endpoint de salud...")
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check OK: {data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
        
        # Probar página principal
        print("2. Probando página principal...")
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Página principal OK")
        else:
            print(f"❌ Página principal failed: {response.status_code}")
        
        # Probar página de cámara
        print("3. Probando página de cámara...")
        response = requests.get(f"{base_url}/camera", timeout=10)
        if response.status_code == 200:
            print("✅ Página de cámara OK")
        else:
            print(f"❌ Página de cámara failed: {response.status_code}")
        
        # Probar estado de cámara
        print("4. Probando estado de cámara...")
        response = requests.get(f"{base_url}/camera_status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Estado de cámara: {data}")
        else:
            print(f"❌ Estado de cámara failed: {response.status_code}")
        
        print("\n🎉 Todas las pruebas completadas!")
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a la aplicación. ¿Está ejecutándose en localhost:5000?")
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")

if __name__ == "__main__":
    test_app()
