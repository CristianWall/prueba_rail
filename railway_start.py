#!/usr/bin/env python3
"""
Script de inicio optimizado para Railway
Maneja la carga del modelo de manera más eficiente
"""

import os
import sys
import time
from app import app, load_model, init_camera

def startup_sequence():
    """Secuencia de inicio optimizada para Railway"""
    print("🚀 Iniciando aplicación de detección de chalecos en Railway...")
    
    # Configurar variables de entorno
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Puerto configurado: {port}")
    
    # Cargar modelo de manera asíncrona
    print("📦 Cargando modelo de detección...")
    model_loaded = load_model()
    
    if model_loaded:
        print("✅ Modelo de detección de chalecos cargado")
    else:
        print("⚠️  Modelo no disponible - la aplicación funcionará sin detección")
    
    # Inicializar cámara (puede fallar en Railway)
    print("📹 Inicializando cámara...")
    camera_loaded = init_camera()
    
    if camera_loaded:
        print("✅ Cámara inicializada")
    else:
        print("⚠️  Cámara no disponible - la aplicación funcionará sin cámara")
    
    print("🎉 Aplicación lista para recibir requests")
    return port

if __name__ == "__main__":
    try:
        port = startup_sequence()
        print(f"🚀 Iniciando servidor en puerto {port}")
        app.run(host="0.0.0.0", port=port, debug=False)
    except Exception as e:
        print(f"❌ Error durante el inicio: {e}")
        sys.exit(1)
