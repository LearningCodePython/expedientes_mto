# Historial de Lanzamientos y Crecimiento (`release.md`)

Este documento detalla la evolución, hitos y crecimiento del proyecto **Plantilla de Mantenimiento de Racks (`plantilla_mto`)**.

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
