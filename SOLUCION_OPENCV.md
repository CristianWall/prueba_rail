# 🔧 Solución para Error de OpenCV en Railway

## ❌ Problema Actual
```
ImportError: libGL.so.1: cannot open shared object file: No such file or directory
```

## ✅ Soluciones Disponibles

### Opción 1: Usar app_simple.py (Recomendada)
La aplicación ya está configurada para usar `app_simple.py` que NO requiere OpenCV.

**Archivos configurados:**
- ✅ `Procfile`: `web: python app_simple.py`
- ✅ `nixpacks.toml`: Configurado para usar app_simple.py
- ✅ `app_simple.py`: Versión sin OpenCV con animaciones

### Opción 2: Forzar uso de Docker
Si Railway sigue ejecutando `app.py`, cambia la configuración:

1. **Renombrar archivos:**
   ```bash
   mv railway.toml railway_original.toml
   mv railway_docker.toml railway.toml
   mv Dockerfile Dockerfile_original
   mv Dockerfile.simple Dockerfile
   ```

2. **O cambiar manualmente en Railway:**
   - Ve a Settings > Build
   - Cambia el builder a "Dockerfile"
   - Usa el Dockerfile.simple

### Opción 3: app.py con manejo de errores
El archivo `app.py` ya está modificado para manejar errores de OpenCV automáticamente.

## 🚀 Pasos para Solucionar

### Método 1: Verificar configuración actual
1. Asegúrate de que `Procfile` contenga: `web: python app_simple.py`
2. Redespliega en Railway
3. La aplicación debería funcionar sin errores

### Método 2: Si sigue fallando
1. En Railway, ve a Settings > Build
2. Cambia el builder a "Dockerfile"
3. Usa el `Dockerfile.simple` (sin OpenCV)
4. Redespliega

### Método 3: Configuración manual
1. En Railway, ve a Settings > Deploy
2. Cambia el comando de inicio a: `python app_simple.py`
3. Guarda y redespliega

## 📁 Archivos de Configuración

- `app_simple.py` - Aplicación sin OpenCV (RECOMENDADA)
- `app.py` - Aplicación con manejo de errores de OpenCV
- `Dockerfile.simple` - Docker sin OpenCV
- `nixpacks.toml` - Configuración Nixpacks
- `railway_docker.toml` - Configuración Docker

## 🎯 Resultado Esperado

Después de aplicar cualquiera de las soluciones:
- ✅ Sin errores de OpenCV
- ✅ Aplicación funcionando
- ✅ Interfaz web con animaciones
- ✅ Health check funcionando

## 🔍 Verificación

Para verificar que funciona:
1. Ve a la URL de tu aplicación
2. Deberías ver la interfaz web
3. Haz clic en "Iniciar Cámara"
4. Deberías ver animaciones (modo demostración)

## 📞 Si el problema persiste

1. Verifica que Railway esté usando `app_simple.py`
2. Revisa los logs de Railway
3. Asegúrate de que no haya archivos `app.py` en el directorio raíz
4. Usa el Dockerfile.simple si es necesario
