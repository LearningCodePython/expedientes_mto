# Plantilla de Mantenimiento de Racks (`plantilla_mto`)

Sistema web profesional para la gestión, inventario, verificación y certificación de mantenimiento de Racks de comunicaciones y centros de datos.

## 🚀 Arquitectura y Tecnologías
- **Backend**: Python Flask (`app.py`) ejecutándose en el puerto `5001`. Inicializa automáticamente la base de datos SQLite (`racks.db`) con datos de prueba al arrancar.
- **Base de Datos**: SQLite (`racks.db`) para persistencia de configuración corporativa, expedientes de racks, esquemas de unidades 42U, inventario de electrónica de red, checklists de verificación y credenciales de usuario.
- **Frontend**: Interfaz responsiva de archivo único (`index.html`) construida con Tailwind CSS, FontAwesome y comunicación REST API (`/api/data`, `/upload`, autenticación).
- **Seguridad**: Sistema de autenticación por sesión con cifrado de contraseñas (`werkzeug.security`) y capacidad de modificación de credenciales por el usuario administrador.

---

## 📋 Funcionalidades Principales
1. **Branding Corporativo Global**: Configuración de nombre, eslogan y logotipo aplicados consistentemente en la interfaz y reportes.
2. **Editor de Expedientes de Racks**: Gestión completa de múltiples racks con fotos en formato 9:16, códigos QR, notas del técnico y checklists críticos (cableado, alimentación, temperatura, etiquetado y puesta a tierra).
3. **Esquema de Rack 42U**: Distribución detallada en 6 columnas verticales de 7 unidades.
4. **Vista Detalle de Electrónica de Red**: Inventario de dispositivos con ID, Marca, Modelo, Número de Serie y Dirección MAC.
5. **Modo Plantilla de Campo**: Vista optimizada para anotaciones manuscritas in situ durante el mantenimiento.
6. **Exportación a PDF Multi-página**: Diseñado con estilos estrictos `@media print` para impresión y exportación en formato A4 exacto.

---

## 🛠️ Guía de Ejecución y Despliegue

### 1. Ejecución Local (Python Directo)
```bash
# Instalar dependencias
pip3 install -r requirements.txt

# Iniciar servidor Flask (Puerto 5001)
python3 app.py
```
Accede en tu navegador a: `http://localhost:5001`  
*Credenciales por defecto*: `admin` / `admin123`

---

### 2. Ejecución Local con Docker (Desarrollo y Pruebas)
Puedes levantar la aplicación encapsulada en un contenedor Docker con persistencia local de volúmenes:
```bash
# Construir y arrancar con Docker Compose
docker-compose up --build
```
La aplicación estará disponible en `http://localhost:5001`.

---

### 3. Despliegue en Producción con Coolify
La aplicación está completamente preparada para despliegues automatizados mediante Coolify:

1. **Crear Servicio / Recurso en Coolify**:
   - Selecciona **Public Repository** o despliega desde tu repositorio Git.
   - Detectará automáticamente el `Dockerfile`.
2. **Configuración del Contenedor**:
   - **Puerto interno**: `5001`
3. **Dominio y SSL**:
   - Asigna tu dominio público (ej. `https://expedientes.cremheda.online`).
   - Coolify gestionará automáticamente el proxy inverso con HTTPS (puerto 443) y redirigirá el tráfico al puerto interno `5001` del contenedor.
4. **Volúmenes Persistentes (Recomendado en Coolify)**:
   - Configura un volumen persistente montado en `/app/racks.db` para conservar la base de datos ante actualizaciones de imagen.
   - Configura un volumen para el directorio `/app/uploads` para preservar las imágenes subidas.
