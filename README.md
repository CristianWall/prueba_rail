# 🎥 Aplicación Flask - Cámara en Vivo

Esta es una aplicación Flask que permite mostrar el feed de video de una cámara web en tiempo real, optimizada para desplegarse en Railway.

## 🚀 Características

- **Streaming en tiempo real**: Muestra el feed de video de la cámara web
- **Interfaz web moderna**: Diseño responsive con controles intuitivos
- **Control de cámara**: Botones para iniciar/detener la cámara
- **Estado en tiempo real**: Verificación del estado de la cámara
- **Optimizado para Railway**: Configuración lista para desplegar
- **Modo demostración**: Funciona sin cámara real usando animaciones

## ⚠️ Solución de Problemas de OpenCV

Si encuentras errores de OpenCV como `libGL.so.1: cannot open shared object file`, la aplicación incluye dos versiones:

### Versión Simple (Recomendada para Railway)
- **Archivo**: `app_simple.py`
- **Características**: Modo demostración con animaciones
- **Ventajas**: Sin dependencias de OpenCV, funciona en cualquier entorno
- **Uso**: Cambia `Procfile` para usar `python app_simple.py`

### Versión Completa (Con OpenCV)
- **Archivo**: `app.py`
- **Características**: Cámara real con OpenCV
- **Ventajas**: Funcionalidad completa de cámara
- **Requisitos**: Dockerfile con dependencias del sistema

## 📁 Estructura del Proyecto

```
prueba_despliegue/
├── app.py              # Aplicación Flask principal
├── templates/
│   └── index.html      # Interfaz web
├── requirements.txt    # Dependencias Python
├── Procfile           # Configuración para Railway
├── railway.toml       # Configuración específica de Railway
├── runtime.txt        # Versión de Python
└── README.md          # Este archivo
```

## 🛠️ Instalación Local

1. **Clonar o navegar al directorio:**
   ```bash
   cd prueba_despliegue
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```

4. **Abrir en el navegador:**
   ```
   http://localhost:5000
   ```

## 🚀 Despliegue en Railway

### Método 1: Desde GitHub
1. Sube este proyecto a un repositorio de GitHub
2. Conecta tu repositorio a Railway
3. Railway detectará automáticamente la configuración

### Método 2: Desde Railway CLI
1. Instala Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Inicia sesión:
   ```bash
   railway login
   ```

3. Despliega:
   ```bash
   railway up
   ```

## 🔧 Configuración

### Variables de Entorno
- `PORT`: Puerto donde correrá la aplicación (por defecto: 5000)

### Endpoints de la API
- `GET /`: Página principal
- `GET /video_feed`: Stream de video
- `GET /start_camera`: Inicia la cámara
- `GET /stop_camera`: Detiene la cámara
- `GET /camera_status`: Estado de la cámara
- `GET /health`: Health check para Railway

## 📱 Uso

1. **Iniciar la aplicación**: La aplicación se ejecutará automáticamente
2. **Activar la cámara**: Haz clic en "Iniciar Cámara"
3. **Ver el stream**: El video aparecerá en la página
4. **Controlar la cámara**: Usa los botones para iniciar/detener
5. **Verificar estado**: Usa el botón "Estado" para verificar el estado

## ⚠️ Notas Importantes

- **Cámara web**: La aplicación requiere una cámara web conectada
- **Permisos**: Asegúrate de que la aplicación tenga permisos para acceder a la cámara
- **Navegador**: Funciona mejor en navegadores modernos (Chrome, Firefox, Safari)
- **HTTPS**: En producción, se recomienda usar HTTPS para acceder a la cámara

## 🐛 Solución de Problemas

### La cámara no se inicia
- Verifica que la cámara esté conectada
- Asegúrate de que no esté siendo usada por otra aplicación
- Revisa los permisos del navegador

### Error de streaming
- Verifica la conexión a internet
- Revisa los logs de la aplicación
- Intenta recargar la página

### Problemas de despliegue
- Verifica que todas las dependencias estén en `requirements.txt`
- Revisa la configuración de Railway
- Consulta los logs de Railway

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs de la aplicación
2. Verifica la configuración de Railway
3. Asegúrate de que todas las dependencias estén instaladas

## 🔄 Actualizaciones

Para actualizar la aplicación:
1. Modifica el código según sea necesario
2. Actualiza las dependencias en `requirements.txt` si es necesario
3. Redespliega en Railway

---

**Desarrollado para Railway** 🚂
