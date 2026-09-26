# Guía de Transición de SQLite a PostgreSQL (`POSTGRES_MIGRATION.md`)

Esta guía detalla los pasos necesarios para migrar la persistencia de la **Plantilla de Mantenimiento de Racks (`plantilla_mto`)** desde SQLite (por defecto) hacia **PostgreSQL**, aprovechando la capa de abstracción de base de datos introducida en la versión **v0.19.0**.

---

## 1. Prerrequisitos y Dependencias

Para permitir que la aplicación Flask se conecte a una base de datos PostgreSQL, es necesario instalar el adaptador de Python `psycopg2-binary`.

Añade `psycopg2-binary` a tu fichero `requirements.txt` o instálalo directamente en el entorno de producción:

```bash
pip3 install psycopg2-binary
```

---

## 2. Configuración de Variables de Entorno

La aplicación detecta automáticamente el motor de base de datos a través de las siguientes variables de entorno:

- **`DB_TYPE`**: Debe configurarse como `postgres` o `postgresql`.
- **`DATABASE_URL`**: Cadena de conexión completa de PostgreSQL con el siguiente formato:
  ```env
  DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_base_datos
  ```

### Ejemplo de fichero `.env` para producción con PostgreSQL:
```env
PORT=5001
DEBUG=False
SECRET_KEY=tu-clave-secreta-segura
DB_TYPE=postgres
DATABASE_URL=postgresql://soportia_user:secure_password@db.internal:5432/racks_prod
```

---

## 3. Inicialización Automática del Esquema

Al arrancar la aplicación por primera vez (`python3 app.py` o mediante el contenedor Docker/Coolify) con `DB_TYPE=postgres` y `DATABASE_URL` configurados:
1. El sistema se conectará a tu instancia de PostgreSQL.
2. Ejecutará la función `init_db()` la cual creará automáticamente las tablas necesarias (`users`, `company`, `racks`) utilizando sintaxis compatible con PostgreSQL.
3. Insertará por defecto las credenciales iniciales de administrador (`admin` / `admin123`), la configuración de la empresa y el rack de ejemplo inicial (`RACK-HQ-01`).

---

## 4. Migración de Datos Existentes (Opcional)

Si deseas migrar los datos existentes en tu base de datos SQLite local (`data/racks.db`) hacia PostgreSQL:

1. **Exportar datos de SQLite a JSON**:
   Puedes exportar los registros de las tablas `company` y `racks` mediante un script Python o herramientas de consulta.
2. **Importar en PostgreSQL**:
   Inserta los registros volcados en las tablas correspondientes de PostgreSQL manteniendo la estructura JSON de los campos `checklist`, `units` y `electronics`.

---

## 5. Despliegue en Coolify con PostgreSQL

1. **Crear base de datos PostgreSQL en Coolify**:
   - Despliega un servicio o recurso de base de datos PostgreSQL en tu panel de Coolify.
   - Copia la URL de conexión interna (Internal Connection URL).
2. **Configurar las Variables de Entorno en el Servicio de la Aplicación**:
   - `DB_TYPE` = `postgres`
   - `DATABASE_URL` = `[Pega aquí la URL interna de PostgreSQL]`
3. **Desplegar**:
   - Realiza el despliegue del repositorio. La aplicación inicializará el esquema y conectará de forma transparente con tu base de datos PostgreSQL gestionada.
