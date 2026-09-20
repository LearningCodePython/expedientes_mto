# Historial de Lanzamientos y Crecimiento (`release.md`)

Este documento detalla la evolución, hitos y crecimiento del proyecto **Plantilla de Mantenimiento de Racks (`plantilla_mto`)**.

---

## v0.7.0 - Contenedor Docker y Preparación para Despliegue con Coolify (Marzo 2026)

### Hitos Principales
- **Dockerfile optimizado**: Imagen ligera basada en Python 3.10-slim con instalación de dependencias y ejecución expuesta en el puerto interno `5001`.
- **Docker Compose (`docker-compose.yml`)**: Configuración para desarrollo y pruebas locales con persistencia de volúmenes para la base de datos SQLite (`racks.db`) y directorio de subidas (`uploads/`).
- **Fichero `.dockerignore`**: Exclusión de artefactos innecesarios para optimizar el tamaño de compilación de la imagen.
- **Soporte para Coolify**: Preparado para despliegue automático en producción en `https://expedientes.cremheda.online` gestionando SSL en el proxy inverso (puerto 443) y enrutando al puerto interno `5001`.

---

## v0.6.0 - Sistema de Autenticación de Usuario y Contraseña (Marzo 2026)

### Hitos Principales
- **Sistema de Autenticación por Sesión Flask**: Endpoints `/api/login`, `/api/logout`, `/api/check-auth` y `/api/change-password` con cifrado seguro de contraseñas (`werkzeug.security`) y control de acceso mediante decorador `@login_required`.
- **Base de Datos de Usuarios (`users`)**: Tabla en SQLite con cuenta predeterminada (`admin` / `admin123`) inicializada automáticamente.
- **Modal de Inicio de Sesión y Badge de Usuario**: Interfaz modal responsiva en Tailwind CSS para autenticación y indicador visual con opción de cierre de sesión en la cabecera superior.
- **Modificación de Contraseña**: Funcionalidad para que el usuario autenticado (admin) pueda cambiar su contraseña desde el panel superior con verificación de contraseña actual y nueva contraseña cifrada.
- **Protección de API y Vistas**: Restricción de acceso a datos y operaciones de guardado/subida únicamente a usuarios autenticados con redirección automática ante códigos 401.

---

## v0.5.0 - Subida Manual de QR, Rediseño de Vista Móvil y Corrección de PDF (Marzo 2026)

### Hitos Principales
- **Subida Manual de Códigos QR (JPG)**: Componente de carga manual asociado al ID del rack mediante el endpoint `/upload`.
- **Rediseño de la Sección "App Móvil"**: Imagen QR ampliada al ancho completo del box (`w-full aspect-square`) con etiqueta inferior.
- **Optimización de Exportación a PDF (Multi-página)**: Impresión automatizada de todos los expedientes en páginas A4 exactas sin páginas en blanco mediante eventos de impresión y CSS estricto.
- **Simplificación de Interfaz**: Actualización de etiqueta a "Editor de Expediente".

---

## v0.4.0 - Vista Resumen Uno a Uno y Vista Detalle de Electrónica de Red (Marzo 2026)

### Hitos Principales
- **Renombramiento a Vista Resumen**: Presentación de expedientes de racks de forma individual (uno a uno), eliminando el desplazamiento vertical continuo de múltiples páginas.
- **Selector y Botones de Navegación DB**: Adición de botones de avance/retroceso y menú desplegable selector para saltar ágilmente entre los diferentes racks de la base de datos SQLite.
- **Creación de Vista Detalle de Electrónica de Red**: Ficha dedicada para inventario y detalle de componentes de red en el rack activo, incluyendo ID, Marca, Modelo, Número de Serie y Dirección MAC.
- **Consistencia de Marca**: Preservación de la cabecera corporativa y pie de página en ambas vistas.

## v0.3.0 - Rediseño de Vistas Fotográficas y Esquema de Rack 42U por Columnas (Marzo 2026)

### Hitos Principales
- **Esquema de Rack 42U por Columnas**: Ordenación de las 42 unidades en 6 columnas verticales de 7 unidades cada una (desde la primera columna con U42→U36 a la sexta con U7→U1).
- **Renombramiento de Sección**: Actualización del título a "Esquema de Rack 42U".
- **Reorganización de Secciones Principales**: Posicionamiento del esquema 42U en la parte inferior, debajo de la cuadrícula superior que agrupa la **Vista Frontal**, **Vista Trasera**, **Código QR** y **Verificación**.
- **Formato Vertical 9:16 para Fotografías**: Contenedores 9:16 para vistas frontal y trasera.
- **Gestión de Exclusiones de Git (`.gitignore`)**: Creación e integración del fichero `.gitignore`.
- **Actualización de Directrices (`AGENTS.md`)**: Optimización de directrices para OpenCode.

## v0.2.0 - Modo Plantilla de Campo y Diferenciación DB / PDF (Marzo 2026)

### Hitos Principales
- **Selector de Modo (DB vs Plantilla de Campo)**: Interfaz en la barra superior para alternar entre la vista de registros de base de datos y la plantilla de campo para trabajos in situ.
- **Plantilla de Campo para Anotaciones Manuales**:
  - Checklist de verificación con casillas desmarcadas listas para marcar a mano.
  - Sección de notas y observaciones del técnico en blanco con líneas horizontales punteadas hasta el final de la página.
  - Campos de fecha y técnico en blanco para registro manuscrito.
- **Combinación de Inventario y Relleno de Campo**: Conserva el esquema de 42U del rack desde la base de datos para que el técnico conozca los equipos instalados al llegar a la ubicación.

## v0.1.0 - Versión Operativa Inicial con Backend SQLite (Marzo 2026)

### Hitos Principales
- **Definición de Especificaciones (`AGENTS.md`)**: Documentación técnica del stack (Python Flask + SQLite en puerto 5001).
- **Backend Python Flask (`app.py`) & Base de Datos SQLite (`racks.db`)**: Migración de la persistencia fuera del navegador a una base de datos externa robusta, almacenando la configuración de la empresa mantenedora y todos los expedientes de racks (fotos, checklists, notas y esquemas 42U).
- **Interfaz Web Responsiva (`index.html`)**: UI basada en Tailwind CSS con comunicación REST API (`/api/data`) y soporte completo de impresión y exportación a PDF.

### Funcionalidades Implementadas
1. **Branding Corporativo Global**:
   - Panel de configuración único para establecer el nombre de la empresa, eslogan (tagline) y logotipo corporativo aplicado consistentemente en todas las páginas y exportaciones.
2. **Gestión Completa de Racks**:
   - Creación, navegación, edición y eliminación de múltiples expedientes de racks.
3. **Activos Multimedia y Base de Datos**:
   - Almacenamiento persistente en SQLite de fotografías frontal y trasera (Base64) y códigos QR de la App móvil.
4. **Esquema de Rack 42U y Checklist de Verificación**:
   - Editor de unidades (1U-42U) y puntos críticos de verificación (cableado, alimentación, temperatura, etiquetado y puesta a tierra).
5. **Exportación a PDF**:
   - Estilos CSS `@media print` optimizados para formato A4 con saltos de página por rack.
6. **Puerto de Ejecución Asignado**:
   - Servidor configurado para arrancar en el puerto `5001` (`python3 app.py`).
