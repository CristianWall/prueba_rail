# 🚀 Prueba de Despliegue Railway

Una aplicación Flask simple para probar el despliegue automático en Railway conectado a GitHub.

## 📋 Características

- ✅ Aplicación Flask básica
- ✅ Interfaz web moderna y responsiva
- ✅ API endpoints para verificar estado
- ✅ Despliegue automático desde GitHub
- ✅ Configuración optimizada para Railway

## 🛠️ Estructura del Proyecto

```
prueba_despliegue/
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias de Python
├── Procfile             # Configuración para Railway
├── templates/
│   └── index.html       # Página principal
└── README.md           # Este archivo
```

## 🚀 Instrucciones de Despliegue

### 1. Preparar el Repositorio

1. Sube esta carpeta `prueba_despliegue` a tu repositorio de GitHub
2. Asegúrate de que esté en la raíz del repositorio o en una carpeta específica

### 2. Configurar Railway

1. Ve a [Railway.app](https://railway.app)
2. Inicia sesión con tu cuenta de GitHub
3. Haz clic en "New Project"
4. Selecciona "Deploy from GitHub repo"
5. Elige tu repositorio
6. Railway detectará automáticamente que es una aplicación Python/Flask

### 3. Configuración Automática

Railway detectará automáticamente:
- ✅ `requirements.txt` para instalar dependencias
- ✅ `Procfile` para ejecutar la aplicación
- ✅ Puerto dinámico (Railway asignará automáticamente)

### 4. Variables de Entorno (Opcional)

Si necesitas configurar variables de entorno:
- Ve a tu proyecto en Railway
- Selecciona "Variables"
- Agrega las variables necesarias

## 🔧 Endpoints Disponibles

- **`/`** - Página principal con interfaz web
- **`/api/status`** - Estado de la aplicación (JSON)
- **`/api/info`** - Información técnica (JSON)

## 📱 Características de la Interfaz

- 🎨 Diseño moderno con gradientes
- 📱 Totalmente responsiva
- ⚡ Actualización automática del estado
- 🔄 Indicadores de estado en tiempo real

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
- Verifica que `requirements.txt` esté en la raíz del proyecto
- Railway debería instalar automáticamente las dependencias

### Error: "Port already in use"
- Railway maneja automáticamente el puerto
- El código ya está configurado para usar `PORT` de variables de entorno

### Error: "Template not found"
- Verifica que la carpeta `templates` esté en la misma ubicación que `app.py`

## 🔄 Despliegue Automático

Una vez configurado:
1. Haz push a tu repositorio de GitHub
2. Railway detectará los cambios automáticamente
3. Desplegará la nueva versión sin intervención manual

## 📊 Monitoreo

Railway proporciona:
- 📈 Métricas de uso
- 📋 Logs en tiempo real
- 🔄 Estado del servicio
- 💰 Información de facturación

## 🎯 Próximos Pasos

Una vez que funcione esta prueba:
1. Puedes integrar tu modelo YOLO
2. Agregar más funcionalidades
3. Configurar dominios personalizados
4. Implementar CI/CD más avanzado

---

**¡Listo para desplegar! 🚀**

Simplemente sube este código a GitHub y conéctalo con Railway para un despliegue automático.
