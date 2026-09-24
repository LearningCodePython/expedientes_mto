# Historial de Lanzamientos y Crecimiento (`release.md`)

Este documento detalla la evolución, hitos y crecimiento del proyecto **Plantilla de Mantenimiento de Racks (`plantilla_mto`)**.

---

## v0.16.0 - Esquema de Rack Dinámico y Selección de Tamaños (9U a 42U) (Marzo 2026)

### Hitos Principales
- **Selector de Tamaño de Rack Estándar**: Incorporación de un selector en el editor de expedientes para elegir la altura del rack entre medidas estándar corporativas (`9U`, `12U`, `16U`, `22U`, `24U`, `32U`, `36U`, `42U`).
- **Renderizado Dinámico y Adaptativo**: Distribución flexible de unidades y columnas en la interfaz interactiva y en el visor/PDF de impresión.
- **Persistencia en Base de Datos**: Actualización del backend Flask y esquema SQLite (`total_units`) para almacenar y recuperar la configuración de unidades de cada rack de forma persistente.

---

## v0.15.0 - Ampliación de Escala de Fotografías en PDF (Marzo 2026)

### Hitos Principales
- **Aumento de Altura Máxima de Imágenes en PDF**: Actualización de los estilos de impresión en `index.html` para incrementar la `max-height` de las fotografías de Vista Frontal y Vista Trasera a `220px` (Escala 3), manteniendo estrictamente la relación de aspecto `9:16` para mayor legibilidad de los expedientes en papel y exportaciones PDF.
- **Actualización de Guías de Agentes**: Mejora y compactación del fichero `AGENTS.md` con directrices precisas y de alta señal para futuras sesiones de OpenCode.

---

## v0.14.0 - Corrección de Proporción 9:16 en Fotografías para PDF (Marzo 2026)

### Hitos Principales
- **Preservación de Relación de Aspecto 9:16**: Actualización de los estilos de impresión (`@media print`) en `index.html` para los contenedores de Vista Frontal y Vista Trasera, eliminando la altura fija de 100px y restaurando `aspect-ratio: 9 / 16 !important` con altura automática. Esto evita que las imágenes aparezcan recortadas o deformadas en el PDF, manteniéndose idénticas a la visualización en pantalla.

---

## v0.13.0 - Limpieza de Base de Datos en el Repositorio Git (Marzo 2026)

### Hitos Principales
- **Desindexación de `racks.db`**: Eliminación definitiva del fichero de base de datos del índice de Git (`git rm --cached racks.db`) para impedir que Coolify o cualquier despliegue remoto reemplace la base de datos persistente del volumen por una versión por defecto al clonar el repositorio.

---

## v0.12.0 - Corrección Definitiva de Persistencia en Contenedores Docker y Coolify (Marzo 2026)

### Hitos Principales
- **Ruta Estricta de Base de Datos (`data/racks.db`)**: Configuración en `app.py` para que `DB_PATH` apunte obligatoriamente al directorio persistente `/app/data/racks.db`, evitando cualquier dependencia de bases de datos efímeras en la raíz del contenedor.
- **Actualización de `.dockerignore`**: Exclusión explícita de ficheros de bases de datos (`*.db`), directorios `data/` y `uploads/` para evitar que se empaqueten bases de datos antiguas o vacías dentro de las imágenes Docker al compilar en Coolify.

---

## v0.11.0 - Separación Inteligente de Exportación PDF según Vista Activa (Marzo 2026)

### Hitos Principales
- **Exportación en Modo Plantilla de Campo**: Al hacer clic en PDF estando en la **Vista Plantilla**, el sistema genera exclusivamente las **plantillas de campo en blanco** optimizadas para anotaciones manuales del técnico in situ (respetando el filtro de cliente activo y numeración de página independiente).
- **Exportación en Modo Resumen / Detalle**: Al estar en las vistas de gestión o detalle, se mantiene la exportación del **Libro de Mantenimiento Completo** con Portada, Índice, Resumen y Detalle de Electrónica de Red.

---

## v0.10.0 - Libro de Mantenimiento Integral por Cliente con Portada e Índice (Marzo 2026)

### Hitos Principales
- **Selector de Libro por Cliente**: Desplegable en la barra superior para alternar entre "Todos los Clientes (Libro Global)" o filtrar por un cliente/área específica.
- **Portada de Dossier Técnico (Cover Page)**: Generación automática de una página de portada oficial al exportar a PDF, incluyendo branding corporativo, datos del cliente e **Índice de Racks** con ubicaciones, fechas y técnicos asignados.
- **Dossier Secuencial Completo**: Cada rack seleccionado incluye de forma automatizada tanto su **Página de Resumen / Expediente** como su **Página de Vista Detalle de Electrónica de Red**.
- **Paginación Dinámica Global**: Numeración exacta de páginas calculada automáticamente en todo el libro (ej. *Página 3 de 7*).

---

## v0.9.0 - Agrupación por Cliente/Área y Sistema de Búsqueda Rápida (Marzo 2026)

### Hitos Principales
- **Agrupación Jerárquica en Selector**: Organización de los expedientes mediante `<optgroup>` agrupados por **Cliente / Área**, conteniendo en su interior los identificadores ID de los racks correspondientes.
- **Campo de Búsqueda Integrado**: Incorporación de un campo de búsqueda en la barra de navegación superior para filtrar expedientes instantáneamente por cliente, ubicación o ID de rack.

---

## v0.8.0 - Optimización Estricta de Impresión y Exportación a PDF A4 (Marzo 2026)

### Hitos Principales
- **Corrección de Margen de Impresión A4**: Anulación del layout de pantalla (padding de contenedores, flex y min-height) en `@media print` para asegurar que cada `.rack-page` comience exactamente en la esquina superior de la hoja.
- **Ajuste de Altura y Padding**: Definición precisa de `296.5mm` de altura y `5mm 8mm` de padding por página para evitar páginas en blanco o desbordamientos accidentales.
- **Evitar Página en Blanco Final**: Configuración de `.rack-page:last-child` para desactivar el salto de página forzado en el último rack del informe.
- **Compactación Adaptativa**: Escalado automático de elementos internos (fotografías y celdas de esquema 42U) durante la impresión para garantizar que todo el contenido encaje perfectamente en una sola página A4.

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
