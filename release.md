# Historial de Lanzamientos y Crecimiento (`release.md`)

Este documento detalla la evolución, hitos y crecimiento del proyecto **Plantilla de Mantenimiento de Racks (`plantilla_mto`)**.

---

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
