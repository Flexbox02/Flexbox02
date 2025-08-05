# 🖥️ Snipe IT PDF Generator - Aplicación GUI para Windows

Aplicación de escritorio con interfaz gráfica que permite generar reportes PDF de recursos informáticos desde Snipe IT de manera fácil e intuitiva.

## 🎯 Características

- **Interfaz gráfica intuitiva** con Tkinter
- **Configuración fácil** del servidor Snipe IT y API Token
- **Búsqueda de usuarios** por correo electrónico
- **Visualización de activos** en tabla interactiva
- **Generación de PDF** con formato profesional
- **Exportación a CSV** de los datos
- **Instalación sencilla** para Windows

## 📋 Requisitos del Sistema

- **Windows 10/11** (recomendado)
- **Python 3.8+** (solo para desarrollo)
- **Conexión a internet** para acceder a Snipe IT
- **Token de API** válido de Snipe IT

## 🚀 Instalación

### Para Usuarios Finales

1. **Descargar** el paquete ZIP desde las releases
2. **Extraer** todos los archivos en una carpeta
3. **Ejecutar** `install.bat` como administrador
4. **Buscar** el acceso directo en el escritorio

### Para Desarrolladores

```bash
# Clonar el repositorio
git clone <repository-url>
cd snipe-it-pdf-generator

# Instalar dependencias
pip install -r requirements_gui.txt

# Ejecutar aplicación
python main_gui.py

# Ejecutar pruebas
python gui_test.py

# Construir instalador
python build_installer.py
```

## 🔧 Configuración Inicial

### 1. Obtener Token de API de Snipe IT

1. Inicie sesión en su instalación de Snipe IT
2. Vaya a **Account Settings** → **API Keys**
3. Haga clic en **"Create New Token"**
4. Asigne un nombre (ej: "PDF Generator")
5. **Copie el token** generado

### 2. Configurar la Aplicación

1. **Abra la aplicación**
2. Haga clic en **"Configurar"**
3. Ingrese la **URL de su servidor** Snipe IT
4. Ingrese su **token de API**
5. Haga clic en **"Probar Conexión"**
6. **Guarde la configuración**

## 💻 Uso de la Aplicación

### Pantalla Principal

La aplicación consta de las siguientes secciones:

#### 🔍 Sección de Búsqueda
- **Campo Email**: Ingrese el correo del usuario
- **Botón Buscar**: Inicia la búsqueda
- **Botón Limpiar**: Limpia los resultados

#### 📊 Sección de Resultados
- **Información del usuario**: Nombre, cargo, departamento
- **Tabla de activos**: Lista todos los recursos asignados
- **Botones de acción**: Generar PDF y exportar CSV

#### 📄 Tipos de Activos Mostrados
- **Equipos**: Laptops, desktops, servidores, etc.
- **Accesorios**: Mouse, teclados, cables, etc.
- **Licencias**: Software asignado al usuario

### Generar Reporte PDF

1. **Busque un usuario** por email
2. **Revise los activos** en la tabla
3. Haga clic en **"Generar Reporte PDF"**
4. **Seleccione ubicación** para guardar
5. El PDF se abrirá automáticamente

### Exportar a CSV

1. **Busque un usuario** por email
2. Haga clic en **"Exportar CSV"**
3. **Seleccione ubicación** para guardar
4. Abra el archivo en Excel o similar

## 📁 Estructura del Proyecto

```
snipe-it-pdf-generator/
├── 📄 main_gui.py              # Aplicación principal
├── 📄 gui_config.py            # Gestión de configuración
├── 📄 gui_config_window.py     # Ventana de configuración
├── 📄 gui_snipe_client.py      # Cliente API de Snipe IT
├── 📄 pdf_generator.py         # Generador de PDF
├── 📄 build_installer.py       # Constructor de instalador
├── 📄 gui_test.py             # Pruebas automatizadas
├── 📄 requirements_gui.txt     # Dependencias GUI
└── 📄 README_GUI.md           # Esta documentación
```

## 🎨 Capturas de Pantalla

### Pantalla de Configuración
- Campo para URL del servidor
- Campo para token de API (oculto)
- Botón "Probar Conexión"
- Ayuda para obtener token

### Pantalla Principal
- Estado de conexión
- Búsqueda por email
- Tabla de activos asignados
- Botones de acción

### Reporte PDF Generado
- Header con información de la empresa
- Datos del trabajador
- Lista detallada de recursos
- Términos y condiciones

## 🔨 Desarrollo

### Arquitectura

La aplicación utiliza el patrón **MVC (Model-View-Controller)**:

- **Model**: `gui_config.py`, `gui_snipe_client.py`
- **View**: `main_gui.py`, `gui_config_window.py`
- **Controller**: Lógica de negocio en las clases GUI

### Componentes Principales

#### 1. GUIConfig
```python
# Gestiona configuración local
config = GUIConfig()
config.save_config(url, token)
is_configured = config.is_configured()
```

#### 2. GUISnipeITClient
```python
# Cliente API para Snipe IT
client = GUISnipeITClient(config)
result = client.get_user_complete_data(email)
```

#### 3. MainGUI
```python
# Interfaz principal
app = MainGUI()
app.run()
```

### Pruebas

```bash
# Ejecutar suite de pruebas
python gui_test.py

# Pruebas incluidas:
# - Importaciones
# - Configuración
# - Generación PDF
# - Creación GUI
# - Cliente Snipe IT
# - Prueba interactiva
```

### Construcción del Instalador

```bash
# Construir ejecutable para Windows
python build_installer.py

# Archivos generados:
# - dist/SnipeIT_PDF_Generator.exe
# - SnipeIT_PDF_Generator_v1.0.0_YYYYMMDD_HHMMSS.zip
```

## 🐛 Solución de Problemas

### Error: "No configurado"
- **Causa**: No se ha configurado la URL o token
- **Solución**: Ir a Archivo → Configuración

### Error: "No se pudo conectar"
- **Causa**: URL incorrecta o servidor no disponible
- **Solución**: Verificar URL y conectividad

### Error: "Error de autenticación"
- **Causa**: Token de API inválido o expirado
- **Solución**: Generar nuevo token en Snipe IT

### Error: "Usuario no encontrado"
- **Causa**: Email no existe en Snipe IT
- **Solución**: Verificar ortografía del email

### La aplicación no inicia
- **Causa**: Dependencias faltantes
- **Solución**: Reinstalar o usar el instalador oficial

### PDF no se genera
- **Causa**: Permisos de escritura o datos corruptos
- **Solución**: Ejecutar como administrador

## 📧 Soporte

### Logs de Error

Los errores se muestran en:
- Mensajes de la aplicación
- Barra de estado
- Ventanas emergentes

### Archivos de Configuración

- **Ubicación**: `C:\Users\[Usuario]\snipe_it_config.json`
- **Contenido**: URL y token (cifrado)

### Información del Sistema

Para reportar errores, incluya:
- Versión de Windows
- Versión de la aplicación
- Mensaje de error completo
- Pasos para reproducir

## 🔄 Actualizaciones

### Versión 1.0.0
- ✅ Interfaz gráfica inicial
- ✅ Configuración de conexión
- ✅ Búsqueda de usuarios
- ✅ Generación de PDF
- ✅ Exportación CSV
- ✅ Instalador para Windows

### Próximas Versiones
- 🔄 Búsqueda avanzada
- 🔄 Reportes personalizados
- 🔄 Múltiples usuarios
- 🔄 Programación automática
- 🔄 Integración con AD

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 🤝 Contribuciones

1. **Fork** el repositorio
2. **Cree** una rama para su feature
3. **Implemente** los cambios
4. **Pruebe** con `gui_test.py`
5. **Envíe** un Pull Request

---

**Desarrollado para facilitar la gestión de recursos informáticos con Snipe IT** 🚀