#!/usr/bin/env python3
"""
Script para solucionar problemas específicos de Railway
Maneja la carga del modelo y configuración del entorno
"""

import os
import sys
import torch

def fix_torch_loading():
    """Solucionar problemas de carga de PyTorch en Railway"""
    print("🔧 Configurando PyTorch para Railway...")
    
    try:
        # Configurar torch para cargar modelos de manera segura
        torch.serialization.add_safe_globals([
            'ultralytics.nn.tasks.DetectionModel',
            'ultralytics.nn.modules.block.C2f',
            'ultralytics.nn.modules.block.Bottleneck',
            'ultralytics.nn.modules.block.SPPF',
            'ultralytics.nn.modules.conv.Conv',
            'ultralytics.nn.modules.head.Detect'
        ])
        print("✅ PyTorch configurado para Railway")
        return True
    except Exception as e:
        print(f"❌ Error configurando PyTorch: {e}")
        return False

def configure_environment():
    """Configurar variables de entorno para Railway"""
    print("🔧 Configurando entorno para Railway...")
    
    # Variables de entorno para Railway
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ.setdefault('PYTHONUNBUFFERED', '1')
    os.environ.setdefault('OPENCV_VIDEOIO_PRIORITY_MSMF', '0')
    
    # Configurar PyTorch para Railway
    os.environ.setdefault('TORCH_HOME', '/tmp/torch')
    os.environ.setdefault('TORCH_MODEL_ZOO', '/tmp/torch/models')
    
    print("✅ Variables de entorno configuradas")

def test_model_loading():
    """Probar la carga del modelo con configuración de Railway"""
    print("🧪 Probando carga del modelo...")
    
    try:
        from ultralytics import YOLO
        
        model_path = os.path.join('modelo_entrenado', 'chaleco_detection', 'weights', 'best.pt')
        
        if os.path.exists(model_path):
            print(f"📁 Modelo encontrado en: {model_path}")
            
            # Cargar modelo con configuración de Railway
            model = YOLO(model_path)
            print("✅ Modelo cargado exitosamente")
            
            # Verificar clases del modelo
            if hasattr(model, 'names'):
                print(f"📊 Clases del modelo: {model.names}")
            
            return True
        else:
            print(f"❌ No se encontró el modelo en: {model_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error cargando el modelo: {e}")
        return False

def optimize_for_railway():
    """Optimizar la aplicación para Railway"""
    print("⚡ Optimizando para Railway...")
    
    # Reducir el uso de memoria
    import gc
    gc.collect()
    
    # Configurar threading para Railway
    import threading
    threading.stack_size(65536)
    
    # Configurar logging para Railway
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("✅ Optimizaciones aplicadas")

if __name__ == "__main__":
    print("🚀 Configurando aplicación para Railway...")
    
    configure_environment()
    fix_torch_loading()
    optimize_for_railway()
    
    if test_model_loading():
        print("🎉 Configuración completada exitosamente")
    else:
        print("⚠️  Configuración completada con advertencias")
        print("💡 La aplicación funcionará sin detección si el modelo no se puede cargar")
