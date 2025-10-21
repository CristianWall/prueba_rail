#!/usr/bin/env python3
"""
Healthcheck específico para Railway
Verifica que la aplicación esté funcionando correctamente
"""

import requests
import time
import sys

def healthcheck():
    """Verificar el estado de la aplicación"""
    try:
        # Intentar conectar a la aplicación
        response = requests.get('http://localhost:5000/health', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Healthcheck exitoso: {data}")
            return True
        else:
            print(f"❌ Healthcheck falló: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar a la aplicación")
        return False
    except Exception as e:
        print(f"❌ Error en healthcheck: {e}")
        return False

def wait_for_app(max_attempts=30, delay=2):
    """Esperar a que la aplicación esté lista"""
    print("⏳ Esperando a que la aplicación esté lista...")
    
    for attempt in range(max_attempts):
        if healthcheck():
            print("🎉 Aplicación lista")
            return True
        
        print(f"⏳ Intento {attempt + 1}/{max_attempts} - Esperando {delay}s...")
        time.sleep(delay)
    
    print("❌ La aplicación no respondió en el tiempo esperado")
    return False

if __name__ == "__main__":
    if wait_for_app():
        sys.exit(0)
    else:
        sys.exit(1)
