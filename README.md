👋 ¡Hola! Soy un administrador de sistemas con experiencia en la automatización de tareas y el despliegue de infraestructuras eficientes y seguras.

🔧 Trabajo con entornos virtualizados basados en **Proxmox VE**, gestionando clústeres, alta disponibilidad y optimización de recursos para entornos empresariales.

📜 Me apasiona la **automatización** con **PowerShell**, **Bash** y **Power Automate**, desarrollando scripts para la administración de usuarios en **Active Directory**, **Azure AD**, tareas programadas, backups, y más.

📡 También tengo experiencia integrando herramientas como **pfSense**, **NetBox**, y **Snipe-IT** en entornos corporativos, enfocándome en la documentación, la seguridad y la eficiencia operativa.

🚀 Actualmente estoy desarrollando un proyecto de red corporativa virtualizada como parte de mi formación en Administración de Sistemas, simulando un entorno empresarial completo.

📂 En mis repositorios encontrarás configuraciones reales, scripts reutilizables y documentación técnica pensada para administradores de sistemas.

# 📋 Snipe IT PDF Report Generator

API REST que genera reportes PDF de recursos informáticos desde Snipe IT basado en el correo electrónico del usuario.

## 🚀 Características

- **Integración con Snipe IT**: Conecta con la API de Snipe IT para obtener datos de usuarios y activos
- **Generación de PDF**: Crea reportes en formato PDF con la estructura de "Acta de Control de Recursos Informáticos"
- **API REST**: Endpoints HTTP simples para generar reportes
- **Validación de datos**: Verificación de emails y manejo de errores
- **Configuración flexible**: Variables de entorno para diferentes instalaciones

## 📝 Estructura del Reporte PDF

El PDF generado incluye:

1. **Encabezado**: Título del documento y código de formulario
2. **Información básica**: Código de acta, empresa, fecha, tipo de movimiento
3. **Datos del trabajador**: Nombres, DNI, gerencia, área, cargo
4. **Recursos informáticos**: Detalles de los activos asignados
   - Tipo, línea, marca
   - Modelo/nombre, número de serie, código de inventario
   - Características técnicas (MAC, memoria, procesador, etc.)
5. **Términos y condiciones**: Texto legal de responsabilidades

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd snipe-it-pdf-generator
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copiar el archivo de ejemplo y configurar:

```bash
cp .env.example .env
```

Editar `.env` con tus datos:

```env
SNIPE_IT_URL=https://tu-snipe-it-domain.com
SNIPE_IT_TOKEN=tu-api-token-aqui
FLASK_PORT=5000
FLASK_DEBUG=True
```

### 4. Obtener el Token de API de Snipe IT

1. Accede a tu instalación de Snipe IT
2. Ve a **Account Settings** > **API Keys**
3. Genera un nuevo token de API
4. Copia el token y ponlo en la variable `SNIPE_IT_TOKEN`

## 🚀 Uso

### Iniciar el servidor

```bash
python app.py
```

El servidor se iniciará en `http://localhost:5000`

### Endpoints disponibles

#### 1. Health Check
```http
GET /health
```

Respuesta:
```json
{
  "status": "healthy",
  "timestamp": "2023-12-07T10:30:00",
  "service": "Snipe IT PDF Report Generator"
}
```

#### 2. Generar reporte PDF
```http
POST /api/user-report
Content-Type: application/json

{
  "email": "usuario@ejemplo.com"
}
```

Respuesta: Archivo PDF descargable

#### 3. Obtener información del usuario (debug)
```http
POST /api/user-info
Content-Type: application/json

{
  "email": "usuario@ejemplo.com"
}
```

Respuesta:
```json
{
  "user": {
    "id": 123,
    "first_name": "Juan",
    "last_name": "Pérez",
    "email": "juan.perez@ejemplo.com",
    "employee_num": "EMP001",
    "job_title": "Analista de Sistemas",
    "department": "IT",
    "location": "Oficina Principal",
    "company": "Mi Empresa"
  },
  "assets_count": 2,
  "assets": [
    {
      "id": 456,
      "asset_tag": "LAP001",
      "serial": "SN123456789",
      "model": "Dell Latitude 5520",
      "status": "Deployed"
    }
  ]
}
```

## 💻 Ejemplos de uso

### Con cURL

```bash
# Generar reporte PDF
curl -X POST http://localhost:5000/api/user-report \
     -H 'Content-Type: application/json' \
     -d '{"email": "usuario@ejemplo.com"}' \
     --output reporte.pdf

# Obtener información del usuario
curl -X POST http://localhost:5000/api/user-info \
     -H 'Content-Type: application/json' \
     -d '{"email": "usuario@ejemplo.com"}'
```

### Con Python requests

```python
import requests

# Generar reporte PDF
response = requests.post(
    'http://localhost:5000/api/user-report',
    json={'email': 'usuario@ejemplo.com'}
)

if response.status_code == 200:
    with open('reporte.pdf', 'wb') as f:
        f.write(response.content)
    print("Reporte generado: reporte.pdf")
else:
    print(f"Error: {response.json()}")
```

### Con JavaScript/Fetch

```javascript
// Generar reporte PDF
async function generateReport(email) {
    try {
        const response = await fetch('http://localhost:5000/api/user-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'reporte.pdf';
            a.click();
        } else {
            const error = await response.json();
            console.error('Error:', error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Uso
generateReport('usuario@ejemplo.com');
```

## 🔧 Configuración avanzada

### Variables de entorno disponibles

| Variable | Descripción | Requerido | Ejemplo |
|----------|-------------|-----------|---------|
| `SNIPE_IT_URL` | URL de tu instalación Snipe IT | ✅ | `https://assets.empresa.com` |
| `SNIPE_IT_TOKEN` | Token de API de Snipe IT | ✅ | `Bearer eyJ0eXAiOiJKV1Q...` |
| `FLASK_PORT` | Puerto del servidor Flask | ❌ | `5000` |
| `FLASK_DEBUG` | Modo debug de Flask | ❌ | `True` |

### Personalización del PDF

Para personalizar el formato del PDF, edita el archivo `pdf_generator.py`:

- Modificar estilos en `__init__`
- Cambiar estructura en los métodos `_build_*`
- Añadir nuevos campos desde Snipe IT

## 🐛 Troubleshooting

### Error: "SNIPE_IT_URL is required"
- Verifica que el archivo `.env` existe y contiene la variable `SNIPE_IT_URL`

### Error: "User not found"
- Confirma que el email existe en Snipe IT
- Verifica que el token de API tiene permisos de lectura

### Error de conexión a Snipe IT
- Verifica que la URL de Snipe IT es correcta
- Confirma que el token de API es válido
- Revisa que no hay firewall bloqueando la conexión

### PDF vacío o con datos faltantes
- Verifica que el usuario tiene activos asignados en Snipe IT
- Revisa los campos personalizados en tu instalación de Snipe IT

## 🏗️ Arquitectura

```
snipe-it-pdf-generator/
├── app.py              # Aplicación Flask principal
├── config.py           # Configuración y variables de entorno
├── snipe_client.py     # Cliente API de Snipe IT
├── pdf_generator.py    # Generador de PDFs
├── requirements.txt    # Dependencias Python
├── .env.example       # Plantilla de variables de entorno
└── README.md          # Documentación
```

## 🛡️ Seguridad

- Nunca commitees el archivo `.env` al repositorio
- Usa tokens de API con permisos mínimos necesarios
- Considera usar HTTPS en producción
- Implementa rate limiting si es necesario

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

👨‍💻 **Desarrollado para la gestión eficiente de recursos informáticos con Snipe IT**

