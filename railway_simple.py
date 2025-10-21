#!/usr/bin/env python3
"""
Versión simplificada para Railway
Maneja la carga del modelo de manera más robusta
"""

import os
import sys
import torch

def simple_model_loading():
    """Cargar modelo de manera simplificada para Railway"""
    print("🔧 Cargando modelo de manera simplificada...")
    
    try:
        from ultralytics import YOLO
        
        model_path = os.path.join('modelo_entrenado', 'chaleco_detection', 'weights', 'best.pt')
        
        if os.path.exists(model_path):
            print(f"📁 Modelo encontrado en: {model_path}")
            
            # Configurar torch para cargar el modelo
            torch.serialization.add_safe_globals([
                'ultralytics.nn.tasks.DetectionModel',
                'ultralytics.nn.modules.block.C2f',
                'ultralytics.nn.modules.block.Bottleneck',
                'ultralytics.nn.modules.block.SPPF',
                'ultralytics.nn.modules.conv.Conv',
                'ultralytics.nn.modules.head.Detect'
            ])
            
            # Cargar modelo
            model = YOLO(model_path)
            print("✅ Modelo cargado exitosamente")
            
            # Verificar clases del modelo
            if hasattr(model, 'names'):
                print(f"📊 Clases del modelo: {model.names}")
            
            return model
        else:
            print(f"❌ No se encontró el modelo en: {model_path}")
            return None
            
    except Exception as e:
        print(f"❌ Error cargando el modelo: {e}")
        return None

def configure_railway():
    """Configurar entorno para Railway"""
    print("🔧 Configurando entorno para Railway...")
    
    # Variables de entorno para Railway
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ.setdefault('PYTHONUNBUFFERED', '1')
    os.environ.setdefault('OPENCV_VIDEOIO_PRIORITY_MSMF', '0')
    
    print("✅ Variables de entorno configuradas")

if __name__ == "__main__":
    print("🚀 Configurando aplicación simplificada para Railway...")
    
    configure_railway()
    model = simple_model_loading()
    
    if model:
        print("🎉 Configuración completada exitosamente")
    else:
        print("⚠️  Configuración completada con advertencias")
        print("💡 La aplicación funcionará sin detección si el modelo no se puede cargar")
