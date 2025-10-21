# 🚀 Guía de Despliegue en Railway

## 📋 Pasos para Desplegar

### 1. Preparar el Proyecto
```bash
# Navegar a la carpeta
cd prueba_despliegue

# Verificar que todos los archivos estén presentes
ls -la
```

### 2. Configurar Railway
1. **Crear proyecto en Railway**
2. **Conectar repositorio Git**
3. **Configurar variables de entorno**:
   - `FLASK_ENV=production`
   - `PYTHONUNBUFFERED=1`

### 3. Archivos de Configuración
- `railway.json` - Configuración de Railway
- `Procfile` - Comando de inicio
- `requirements-railway.txt` - Dependencias optimizadas
- `railway_setup.py` - Script de configuración

### 4. Comandos de Despliegue
```bash
# Usar requirements optimizados
cp requirements-railway.txt requirements.txt

# Desplegar
git add .
git commit -m "Deploy vest detection system"
git push
```

## 🔧 Configuración Específica

### Railway.json
```json
{
  "deploy": {
    "startCommand": "gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --preload app:app",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 30
  }
}
```

### Procfile
```
web: gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --preload app:app
```

## 🐛 Solución de Problemas

### Error: Healthcheck Failure
1. **Verificar puerto**: Asegurar que la app use `$PORT`
2. **Verificar endpoint**: Usar `/health` en lugar de `/`
3. **Verificar timeout**: Aumentar a 120 segundos

### Error: Dependencias
1. **Usar requirements-railway.txt**
2. **Verificar versiones**: Usar versiones específicas
3. **Verificar memoria**: Railway tiene límites de memoria

### Error: Modelo no carga
1. **Verificar ruta**: `modelo_entrenado/chaleco_detection/weights/best.pt`
2. **Verificar tamaño**: El modelo puede ser muy grande
3. **Verificar permisos**: Archivos deben ser accesibles

## 📊 Monitoreo

### Logs de Railway
```bash
# Ver logs en tiempo real
railway logs

# Ver logs específicos
railway logs --service web
```

### Healthcheck Manual
```bash
# Verificar estado
curl https://tu-app.railway.app/health

# Verificar cámara
curl https://tu-app.railway.app/camera_status
```

## 🚀 Optimizaciones

### 1. Reducir Tamaño del Modelo
- Usar modelo más pequeño si es posible
- Comprimir el modelo
- Usar modelo cuantizado

### 2. Optimizar Dependencias
- Usar versiones específicas
- Eliminar dependencias innecesarias
- Usar dependencias ligeras

### 3. Configurar Gunicorn
- Usar 1 worker (Railway tiene límites)
- Configurar timeout apropiado
- Usar preload para mejor rendimiento

## 📈 Métricas de Despliegue

### Tiempo de Inicio
- **Objetivo**: < 60 segundos
- **Realidad**: ~ 2-3 minutos (debido al modelo)

### Uso de Memoria
- **Límite Railway**: 1GB
- **Uso estimado**: ~ 800MB

### CPU
- **Límite Railway**: 1 vCPU
- **Uso estimado**: ~ 70%

## 🔄 Actualizaciones

### Despliegue Automático
1. **Push a main**: Despliegue automático
2. **Verificar logs**: Revisar errores
3. **Probar endpoints**: Verificar funcionalidad

### Rollback
1. **Revertir commit**: `git revert`
2. **Push cambios**: Despliegue automático
3. **Verificar funcionamiento**: Probar endpoints

---

*Guía específica para despliegue de detección de chalecos en Railway*
