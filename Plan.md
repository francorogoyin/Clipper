# Plan: Highlighter — App web para resaltados

## Visión del producto

Highlighter es una app web para procesar resaltados
de libros digitales y exportarlos a múltiples
formatos. Apunta a público general: tiene que ser
intuitivo, guiado y completo.

El usuario sube su archivo, configura cómo quiere
los highlights, y exporta. Sus highlights se guardan
en su cuenta para volver a editarlos y re-exportar.

---

## Decisiones de producto

- **App web completa** (no desktop)
- **Cuentas con OAuth** (Google y Notion)
- **Público general**: wizard paso a paso, tooltips
- **Highlights persistentes** en la cuenta
- **Ayuda externa** (videos YouTube) aspiracional;
  por ahora tooltips internos

---

## Formatos de entrada

### Kindle TXT (MVP)

El archivo `My Clippings.txt` que genera Kindle.
Cada highlight trae: autor, libro, página, fecha,
texto resaltado.

### DOCX/DOC con marcas de formato (Fase 2)

Documentos donde el usuario marca highlights con
prefijos tipo Markdown que definen su **tipo
semántico**:

- `###` → heading
- `>` → quote
- `!` → callout
- `~` → toggle
- Sin prefijo → paragraph

Las marcas son **predefinidas + personalizables**.
El usuario configura sus reglas en la app (sección
de configuración con tabla: marca → tipo semántico).

### Otros e-readers (futuro)

Kobo, Apple Books, etc. La arquitectura de parsers
se diseña extensible desde el día 1.

---

## Modelo de datos

Cada highlight tiene:

- **Texto**: el contenido resaltado
- **Autor**: quién escribió el libro
- **Libro**: de dónde se extrajo
- **Página**: ubicación en el libro
- **Fecha**: cuándo se hizo el subrayado
- **Tipo semántico**: paragraph, heading, callout,
  quote o toggle (derivado de marcas en DOCX o
  configurado manualmente)

Tipos semánticos iniciales (5):

| Tipo | Notion | PDF | Obsidian | DOCX |
| --- | --- | --- | --- | --- |
| paragraph | paragraph | texto normal | texto | párrafo |
| heading | heading | título grande | ## | Heading |
| callout | callout | caja color | > [!note] | text box |
| quote | quote | itálica + barra | > | cita |
| toggle | toggle | recuadro | details | colapsable |

CSV/XLSX: columna "Tipo" con el valor semántico.

---

## Pipeline (5 pantallas) — Flujo detallado

### P_Start — Pantalla de inicio

**Subir archivo:**

- Campo para subir TXT o DOCX.
- Si el formato es inválido: **modal** explicando
  el problema con ejemplo visual de cómo debe ser
  el formato del archivo.

**Formato de salida:**

- Dropdown: PDF, DOCX, DOC, ODT, CSV, XLSX, XLS,
  TXT, Notion, Obsidian (Markdown).
- Si no registrado: PDF por defecto.
- Si registrado: el preferido del usuario.

**Partición:**

- Checkbox "Guardar en archivos separados".
- Si tildado: dropdown con UN criterio:
  Author, Book, Year, Month, Day.
- Extensible a combinaciones en el futuro.

**Ruta de guardado:**

- Muestra ubicación por defecto.
- Botón "Guardar en" abre selector de carpeta.

**Opciones de estilo** (solo si el formato lo soporta:
PDF, DOCX, DOC, ODT — ocultas para CSV/XLSX/TXT):

- Estilo de Block (6 opciones, ver sección Estilos).
- Para Highlight y Sub_Line por separado:
  - Formato: Normal, Negrita, Cursiva, N+C.
  - Fuente.
  - Color.
  - Tamaño de fuente.
  - Alineación: izquierda, derecha, centro, justif.

**Sub_Line configurable:**

- El usuario elige qué campos mostrar: autor, libro,
  ambos, fecha, página, o combinación libre.

**Otros:**

- Casilla: usar config de P_Display por defecto.
- Casilla: usar config de P_Processing por defecto.
- Campo: nombre del archivo de salida.
- Tooltips y links de ayuda (aspiracional).
- Botón **"Get Highlights"**.

---

### P_Display — Pantalla de bloques

**No aparece** si el usuario tildó "usar config de
P_Display por defecto" en P_Start.

**Tabla de highlights:**

- Columnas: Autor, Libro, Página, Fecha, Highlight
  (truncado).
- **Paginación** (20-50 highlights por página).
- Ordenar por: Author, Book, Date.
- Agrupar en Clippings por: Author, Book,
  Day_Of_Week, Date, Month, Year.

**Selección de bloques:**

- Checkbox por fila + Shift/Ctrl para selección
  rápida (tipo explorador de archivos).

**Operaciones:**

- **Combinar** F_Blocks → C_Block:
  - Se rechaza si son de distinto Author-Book.
  - Se pregunta qué Date mantener.
  - Confirmación antes de ejecutar.
- **Dividir** F_Block → varios C_Blocks:
  - Confirmación antes de ejecutar.
- **Eliminar** F_Blocks:
  - Confirmación antes de ejecutar.
- **Renombrar** Clippings (default: Author/Book/etc.)
- **Eliminar** Clippings (con confirmación).
- **Deshacer** última operación.

**Confirmación final:**

- Botón "Proceder con el F_Order".
- Se muestra **preview completo**: vista de cómo
  quedará el archivo exportado con el estilo
  elegido aplicado.
- Confirmación (con opción "no volver a preguntar",
  guardada permanentemente en la cuenta, reseteable
  desde Configuración).
- Opción de guardar config de P_Display por defecto.

---

### P_Processing — Procesamiento de texto

**No aparece** si el usuario tildó "usar config de
P_Processing por defecto" en P_Start.
Sí aparece si algún Clipping no tiene config guardada.

**Lista de Clippings** desplegables, cada uno con:

- Checkboxes (tildados por defecto según config):
  - Cambiar primera letra a mayúscula.
  - Borrar caracteres específicos (campo de texto).
  - Cambiar primer carácter "Letra" a mayúscula.
  - Agregar signos faltantes (', ", <, (, ¿, ¡, «).
- **Vista previa en tiempo real**: al tildar/destildar,
  un highlight de ejemplo se actualiza al instante.
- Botón: repetir patrón en todos los Clippings.
- Botón: guardar config para este Clipping.

**Otros:**

- Botón: aplicar H_Processing por defecto a todos.
  (con confirmación que explica qué pasa).
- Tooltips de ayuda (aspiracional).
- Botón "Acepto el H_Processing".
- Confirmación + opción de guardar config.

---

### P_Notion — Configuración de Notion

**Solo aparece** si el formato de salida es Notion.
**Wizard paso a paso** (una cosa a la vez con
botón Siguiente):

**Paso 1 — Conexión:**

- a) Ya configuró N_Account: pantalla con opciones
  "Cambiar ubicación" o "Seguir".
- b) Primera vez: inicia OAuth con Notion, pide
  permisos, abre N_Explorer para elegir N_Database.

**Paso 2 — Matcheo:**

- Matcheo automático **configurable**: el usuario
  define qué campo del Clipping se matchea con qué
  propiedad de la N_Page.
- Lista de N_Match con indicadores de color:
  - Verde: matcheado correctamente.
  - Rojo: no se pudo matchear.
- Por cada Clipping, botones:
  - "Crear nueva N_Page" (elegir emoji + título).
  - "Seleccionar ubicación" (abre N_Explorer).
  - Opción de guardar este match para el futuro.

**N_Explorer:**

- Tree view (como sidebar de Notion) + buscador
  de páginas arriba para filtrar rápido.

**Paso 3 — Posición de paste:**

- Opciones: Final, Principio, N_Block específico.
- Si "específico": abre N_Explorer para elegir el
  N_Block dentro de la N_Page.

**Paso 4 — Formato del N_Block:**

- Tipo: callout, paragraph, quote.
- Estilo: negrita, cursiva, subrayado, tachado.
- Fuente, color, tamaño, alineación.
- Color de fondo del N_Block.
- Si callout: elegir emoji.
- Vista previa del N_Block final.
- Aplicar a todos los N_Blocks de este Clipping.
- Aplicar a todos los Clippings.
- Importar/exportar config de N_Block.

**Confirmación:**

- Si hay N_Match en rojo: advertencia, opción de
  volver atrás.
- Confirmación de que los N_Match son correctos.
- Botón "Aceptar destinos de Highlights".

---

### P_End — Pantalla final

- Resumen de toda la configuración (desplegable).
- Opción: guardar configuración actual.
- Botón **"Finalizar"** (con confirmación).
- Barra de progreso durante exportación.
- Al completar: mensaje de éxito con opciones:
  - **Descargar** el archivo generado.
  - **Ir a biblioteca** de highlights guardados.

---

## Estilos de Block

6 estilos que definen cómo se presenta un highlight
en formatos de archivo (PDF, DOCX, etc.).

La **Sub_Line** es configurable: el usuario elige
qué campos mostrar (autor, libro, ambos, fecha,
página, o combinación libre).

### 1. Clásico

Highlight arriba, Sub_Line en cursiva abajo,
separados por línea fina horizontal.

```
«No es que tengamos poco tiempo,
sino que perdemos mucho.»

─────────────────────────────────
  Séneca — Sobre la brevedad
  de la vida
```

### 2. Cita

Barra lateral izquierda tipo blockquote.
Sub_Line al final con guión largo.

```
  │ No es que tengamos poco
  │ tiempo, sino que perdemos
  │ mucho.
  │
  │ — Séneca, Sobre la brevedad
  │   de la vida
```

### 3. Tarjeta

Recuadro completo alrededor del highlight.
Sub_Line fuera del recuadro.

```
┌───────────────────────────────┐
│ No es que tengamos poco       │
│ tiempo, sino que perdemos     │
│ mucho.                        │
└───────────────────────────────┘
  Séneca — Sobre la brevedad
  de la vida
```

### 4. Minimalista

Highlight centrado, Sub_Line pequeña debajo.
Sin separadores ni adornos.

```
   No es que tengamos poco
   tiempo, sino que perdemos
   mucho.

         Séneca
   Sobre la brevedad de la vida
```

### 5. Numerado

Número secuencial a la izquierda del highlight.
Sub_Line alineada a la derecha.

```
  1.  No es que tengamos poco
      tiempo, sino que
      perdemos mucho.
                    Séneca —
          Sobre la brevedad
               de la vida
```

### 6. Destacado

Fondo sombreado en el highlight (como un
resaltador real). Sub_Line normal debajo.

```
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▓ No es que tengamos poco   ▓
  ▓ tiempo, sino que perdemos ▓
  ▓ mucho.                    ▓
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  Séneca — Sobre la brevedad
  de la vida
```

---

## Reglas de marcas de formato (DOCX)

### Concepto

Cuando el usuario sube un DOCX en vez de un TXT,
los highlights pueden tener **prefijos tipo
Markdown** que determinan su tipo semántico.

### Marcas predefinidas

| Marca | Tipo semántico | Ejemplo en DOCX |
| --- | --- | --- |
| (sin marca) | paragraph | Texto normal |
| `###` | heading | ### Título del highlight |
| `>` | quote | > Frase citada |
| `!` | callout | ! Nota importante |
| `~` | toggle | ~ Contenido colapsable |

### Reglas personalizables

En Configuración de la cuenta, sección
"Reglas de marcas":

- Tabla editable: Marca → Tipo semántico.
- El usuario puede agregar, editar o eliminar
  reglas.
- Las reglas personalizadas tienen prioridad
  sobre las predefinidas.
- Se pueden resetear a las predefinidas.

### Parseo

1. Cada línea del DOCX se analiza buscando
   prefijo al inicio.
2. Si se encuentra una marca conocida, se asigna
   el tipo semántico correspondiente.
3. Si no hay marca, se asigna "paragraph".
4. El prefijo se elimina del texto del highlight.

---

## Pantallas adicionales

### Landing page (simple)

- Hero con propuesta de valor.
- 3-4 features destacadas.
- Sección pricing (free vs premium).
- CTA de registro.
- Footer.

### Biblioteca de highlights

Dos vistas alternables:

- **Por archivo**: lista de archivos subidos como
  cards (nombre, fecha, cantidad de highlights).
  Click para ver highlights de ese archivo.
- **Vista unificada**: todos los highlights del
  usuario en una tabla filtrable por autor, libro,
  fecha. Click para abrir y re-exportar.

### Configuración de cuenta

- **Perfil**: nickname, avatar, email (solo lectura).
- **Suscripción**: plan actual + botón upgrade.
- **Apariencia**: tema claro/oscuro, idioma.
- **Exportación por defecto**: formato preferido,
  estilo de block, config de Highlight y Sub_Line.
- **Reglas de marcas**: tabla editable
  marca → tipo semántico + resetear a predefinidas.
- **Notion**: estado de conexión, config N_Block
  por defecto, botón desconectar.
- **Confirmaciones**: lista de silenciadas +
  botón resetear todas.
- **Conexiones OAuth**: estado Google y Notion.

---

## Configuración del usuario

- Perfil: nickname, avatar, mail.
- Suscripción: free (50 highlights) / premium
  (ilimitado).
- Highlights guardados con sus configs.
- H_Processing por defecto por Clipping.
- N_Block por defecto.
- Formato de salida preferido.
- Reglas de marcas personalizadas (DOCX).
- Confirmaciones silenciadas (reseteable).
- Tema visual: claro / oscuro.
- Idioma.

---

## Stack técnico

### Frontend

- **React** con Vite.
- **shadcn/ui** (Radix + Tailwind): moderna,
  liviana, muy customizable. Ideal para wizard.
- **TanStack Query** para estado del servidor.
- **Zustand** para estado del wizard del pipeline.

### Backend

- **FastAPI** (Python):
  ligero, async, tipado, docs automática.
- **SQLAlchemy** + **PostgreSQL**.
- **Celery** + **Redis** para tareas async
  (exportación, paste a Notion).
- **OAuth**: Google + Notion (authlib).
- **Cookies httpOnly** para sesión JWT
  (más seguro contra XSS que localStorage).
- **S3 / Cloudflare R2** para archivos
  (subidos y exportados).

### Hosting

- **Railway**: web + worker Celery + Redis +
  PostgreSQL en un mismo proyecto.
- Dominio: flexible, sin definir aún.

### Dependencias backend

- fastapi, uvicorn
- sqlalchemy, alembic, asyncpg
- celery, redis
- authlib, python-jose
- boto3 (S3/R2)
- fpdf2 (PDF)
- python-docx (DOCX)
- pypandoc (DOC, ODT)
- openpyxl (XLSX)
- pandas
- notion-client

### Estructura monorepo

```
Highlighter/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── stores/
│   │   ├── api/
│   │   └── lib/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── files.py
│   │   │   ├── highlights.py
│   │   │   ├── clippings.py
│   │   │   ├── processing.py
│   │   │   ├── export.py
│   │   │   ├── notion.py
│   │   │   └── rules.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── parsers/
│   │   ├── exporters/
│   │   ├── tasks/
│   │   └── core/
│   ├── alembic/
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── railway.toml
└── README.md
```

---

## Modelo de base de datos

### Users

```
Id_Usuario              UUID PK
Email                   VARCHAR(255) UNIQUE NOT NULL
Nickname                VARCHAR(100)
Avatar_Url              VARCHAR(500)
Idioma                  VARCHAR(10) DEFAULT 'es'
Tema_Visual             VARCHAR(10) DEFAULT 'claro'
Tipo_Suscripcion        VARCHAR(10) DEFAULT 'free'
Formato_Preferido       VARCHAR(20) DEFAULT 'pdf'
Estilo_Block            INTEGER DEFAULT 1 (1..6)
Confirmaciones_Silenciadas  JSONB DEFAULT '{}'
Config_P_Display_Defecto    BOOLEAN DEFAULT false
Config_P_Processing_Defecto BOOLEAN DEFAULT false
Fecha_Creacion          TIMESTAMPTZ
Fecha_Actualizacion     TIMESTAMPTZ
```

### Conexiones_Oauth

```
Id_Conexion             UUID PK
Id_Usuario              UUID FK → Users
Proveedor               VARCHAR(20) ('google'|'notion')
Access_Token            TEXT (encriptado)
Refresh_Token           TEXT (encriptado)
Token_Expira_En         TIMESTAMPTZ
Id_Externo              VARCHAR(255)
UNIQUE(Id_Usuario, Proveedor)
```

### Archivos_Subidos

```
Id_Archivo              UUID PK
Id_Usuario              UUID FK → Users
Nombre_Original         VARCHAR(500)
Tipo_Archivo            VARCHAR(10) ('txt'|'docx')
Tamano_Bytes            INTEGER
Ruta_Almacenamiento     VARCHAR(500) (ruta en S3)
Cantidad_Highlights     INTEGER DEFAULT 0
Fecha_Subida            TIMESTAMPTZ
```

### Highlights

```
Id_Highlight            UUID PK
Id_Usuario              UUID FK → Users
Id_Archivo              UUID FK → Archivos_Subidos
Texto                   TEXT NOT NULL
Autor                   VARCHAR(300)
Libro                   VARCHAR(500)
Pagina                  VARCHAR(50)
Fecha_Subrayado         TIMESTAMPTZ
Tipo_Semantico          VARCHAR(20) DEFAULT 'paragraph'
Orden_Original          INTEGER (O_Order)
Fecha_Creacion          TIMESTAMPTZ
```

### Clippings

```
Id_Clipping             UUID PK
Id_Usuario              UUID FK → Users
Nombre                  VARCHAR(300)
Fecha_Creacion          TIMESTAMPTZ
Fecha_Actualizacion     TIMESTAMPTZ
```

### Clipping_Highlights (N:M)

```
Id_Clipping_Highlight   UUID PK
Id_Clipping             UUID FK → Clippings CASCADE
Id_Highlight            UUID FK → Highlights CASCADE
Orden_En_Clipping       INTEGER (F_Order)
UNIQUE(Id_Clipping, Id_Highlight)
```

### Config_H_Processing

```
Id_Config_Processing    UUID PK
Id_Clipping             UUID FK → Clippings UNIQUE
Primera_Letra_Mayuscula     BOOLEAN DEFAULT true
Borrar_Caracteres           BOOLEAN DEFAULT false
Caracteres_A_Borrar         VARCHAR(100) DEFAULT ''
Primer_Caracter_Letra_Mayus BOOLEAN DEFAULT true
Agregar_Signos_Faltantes    BOOLEAN DEFAULT true
```

### Config_Exportacion

```
Id_Config_Exportacion   UUID PK
Id_Usuario              UUID FK → Users UNIQUE
Estilo_Block            INTEGER DEFAULT 1
Sub_Line_Campos         JSONB DEFAULT '["autor","libro"]'
Highlight_Formato       VARCHAR(10) DEFAULT 'normal'
Highlight_Fuente        VARCHAR(100) DEFAULT 'Arial'
Highlight_Color         VARCHAR(7) DEFAULT '#000000'
Highlight_Tamano        INTEGER DEFAULT 12
Highlight_Alineacion    VARCHAR(15) DEFAULT 'izquierda'
Sub_Line_Formato        VARCHAR(10) DEFAULT 'cursiva'
Sub_Line_Fuente         VARCHAR(100) DEFAULT 'Arial'
Sub_Line_Color          VARCHAR(7) DEFAULT '#666666'
Sub_Line_Tamano         INTEGER DEFAULT 10
Sub_Line_Alineacion     VARCHAR(15) DEFAULT 'izquierda'
```

### Reglas_Marcas

```
Id_Regla                UUID PK
Id_Usuario              UUID FK → Users
Marca                   VARCHAR(20)
Tipo_Semantico          VARCHAR(20)
Es_Predefinida          BOOLEAN DEFAULT false
Prioridad               INTEGER DEFAULT 0
UNIQUE(Id_Usuario, Marca)
```

### Config_Notion

```
Id_Config_Notion        UUID PK
Id_Usuario              UUID FK → Users UNIQUE
Id_N_Database           VARCHAR(255)
Titulo_N_Database       VARCHAR(500)
Campo_Matcheo_Clipping  VARCHAR(50) DEFAULT 'nombre'
Propiedad_Matcheo_N_Page VARCHAR(100) DEFAULT 'title'
N_Block_Tipo            VARCHAR(20) DEFAULT 'paragraph'
N_Block_Formato         VARCHAR(20) DEFAULT 'normal'
N_Block_Color           VARCHAR(30) DEFAULT 'default'
N_Block_Color_Fondo     VARCHAR(30) DEFAULT 'default'
N_Block_Alineacion      VARCHAR(15) DEFAULT 'izquierda'
N_Block_Emoji           VARCHAR(10)
```

### N_Matches

```
Id_N_Match              UUID PK
Id_Usuario              UUID FK → Users
Id_Clipping             UUID FK → Clippings
N_Page_Id               VARCHAR(255)
N_Page_Titulo           VARCHAR(500)
Posicion_Paste          VARCHAR(20) DEFAULT 'final'
N_Block_Especifico_Id   VARCHAR(255)
Guardado_Permanente     BOOLEAN DEFAULT false
UNIQUE(Id_Clipping, N_Page_Id)
```

### Relaciones

- Users 1:N Conexiones_Oauth
- Users 1:N Archivos_Subidos
- Users 1:N Highlights
- Archivos_Subidos 1:N Highlights
- Users 1:N Clippings
- Clippings N:M Highlights (via Clipping_Highlights)
- Clippings 1:1 Config_H_Processing
- Users 1:1 Config_Exportacion
- Users 1:N Reglas_Marcas
- Users 1:1 Config_Notion
- Users 1:N N_Matches

### Notas

- Límite free: COUNT(Highlights WHERE Id_Usuario)
  <= 50. Sin columna extra.
- Tokens OAuth encriptados con Fernet.
- Soft delete con Eliminado_En en Highlights y
  Clippings para soportar deshacer.

---

## API endpoints

### Auth — /api/auth

- `GET /auth/google/login` →
  Redirect a Google OAuth.
- `GET /auth/google/callback` →
  { Token_Acceso, Usuario }.
- `GET /auth/notion/login` →
  Redirect a Notion OAuth.
- `GET /auth/notion/callback` →
  { Token_Acceso, Usuario }.
- `POST /auth/logout` →
  Invalida sesión.
- `GET /auth/me` →
  { Usuario autenticado }.
- `POST /auth/refresh` →
  { Token_Acceso nuevo }.

### Users — /api/users

- `GET /users/perfil` →
  { Nickname, Avatar, Email, Suscripcion, ... }.
- `PATCH /users/perfil` →
  Actualizar nickname, avatar, idioma, tema.
- `GET /users/config` →
  { Config_Exportacion, Confirmaciones, ... }.
- `PATCH /users/config` →
  Actualizar campos parciales.
- `POST /users/confirmaciones/reset` →
  Resetear confirmaciones silenciadas.
- `GET /users/suscripcion` →
  { Tipo, Limite, Highlights_Usados }.

### Files — /api/files

- `POST /files/upload` (multipart) →
  { Id_Archivo, Cantidad, Highlights[] }.
  Valida formato. Verifica límite free.
- `GET /files` →
  { Archivos[], Total }. Paginado.
- `GET /files/{id}` →
  { Archivo con metadata }.
- `DELETE /files/{id}` →
  Elimina archivo y sus highlights.

### Highlights — /api/highlights

- `GET /highlights` →
  { Highlights[], Total }. Filtros: autor,
  libro, id_archivo. Paginado y ordenable.
- `GET /highlights/{id}` →
  { Highlight }.
- `PATCH /highlights/{id}` →
  Editar texto, tipo semántico.
- `DELETE /highlights/{id}` →
  Soft delete.
- `POST /highlights/combinar` →
  { Ids[], Fecha_A_Mantener } →
  { Highlight_Combinado }.
- `POST /highlights/dividir/{id}` →
  { Puntos_De_Corte[] } →
  { Highlights_Resultantes[] }.
- `DELETE /highlights/lote` →
  { Ids[] } → { Cantidad_Eliminada }.

### Clippings — /api/clippings

- `GET /clippings` →
  { Clippings[], Total }. Paginado.
- `POST /clippings` →
  { Nombre, Ids_Highlights[] } →
  { Clipping }.
- `POST /clippings/agrupar` →
  { Criterio, Ids_Highlights[] } →
  { Clippings[] }. Criterio: autor, libro,
  dia, mes, ano.
- `GET /clippings/{id}` →
  { Clipping con Highlights ordenados }.
- `PATCH /clippings/{id}` →
  Renombrar.
- `DELETE /clippings/{id}` →
  Soft delete.
- `PATCH /clippings/{id}/orden` →
  { Orden: [{ Id, Posicion }] } →
  Reordena highlights dentro del clipping.

### Processing — /api/processing

- `POST /processing/preview` →
  { Texto, Config } → { Texto_Procesado }.
  Para preview en tiempo real (debounce 300ms).
- `POST /processing/aplicar/{id_clipping}` →
  Aplica H_Processing a un clipping.
- `POST /processing/aplicar-todos` →
  Aplica H_Processing a todos los clippings.
- `GET /processing/config/{id_clipping}` →
  { Config_H_Processing }.
- `PUT /processing/config/{id_clipping}` →
  Guarda config de processing.

### Export — /api/export

- `POST /export/generar` →
  { Formato, Ids_Clippings, Config_Estilo,
  Particion? } → { Id_Tarea } (async Celery).
- `GET /export/estado/{id_tarea}` →
  { Estado, Progreso%, Url_Descarga? }.
- `GET /export/descargar/{id_tarea}` →
  Archivo binario desde S3.
- `POST /export/preview` →
  { Preview_Html } del archivo final.
- `GET /export/config` →
  { Config_Exportacion del usuario }.
- `PUT /export/config` →
  Guarda config de exportación.

### Notion — /api/notion

- `GET /notion/paginas` →
  { Paginas[] }. Query: id_padre, busqueda.
  Para N_Explorer (tree lazy-loaded + búsqueda).
- `GET /notion/paginas/{id}/bloques` →
  { Bloques[] }. Para posición específica.
- `POST /notion/match/auto` →
  { Ids_Clippings, Campo, Propiedad } →
  { Matches[], Sin_Match[] }.
- `POST /notion/match/manual` →
  { Id_Clipping, N_Page_Id, Guardar? } →
  { N_Match }.
- `DELETE /notion/match/{id}` →
  Eliminar match.
- `GET /notion/matches` →
  { N_Matches[] }.
- `POST /notion/paginas` →
  { Titulo, Emoji, Id_Padre } →
  { N_Page creada }.
- `POST /notion/paste` →
  { Matches_Con_Config[] } →
  { Id_Tarea } (async Celery, rate limited).
- `GET /notion/paste/estado/{id_tarea}` →
  { Estado, Progreso, Errores? }.
- `GET /notion/config` →
  { Config_Notion }.
- `PUT /notion/config` →
  Guarda config de N_Block por defecto.

### Rules — /api/rules

- `GET /rules` →
  { Reglas[] } (incluye predefinidas).
- `POST /rules` →
  { Marca, Tipo_Semantico } → { Regla }.
- `PATCH /rules/{id}` →
  Editar regla.
- `DELETE /rules/{id}` →
  Eliminar regla personalizada.
- `POST /rules/reset` →
  Resetear a predefinidas.

### Notas de la API

- Todas las rutas excepto /auth/* requieren
  cookie httpOnly con JWT.
- Paginación: pagina (default 1), limite
  (default 20, max 100). Respuesta con Total.
- Errores: { Detalle, Codigo } + HTTP status.
- Exportación y paste son async via Celery.
  Frontend hace polling con estado/{id_tarea}.
- POST /files/upload verifica límite free (50).
  Devuelve 403 si se excede.

---

## Componentes React

### Árbol de páginas

```
App
├── Proveedores
│   (AuthProvider, ThemeProvider,
│    QueryClientProvider)
│
├── Layout_Publico
│   ├── Pagina_Landing
│   │   ├── Hero_Section
│   │   ├── Seccion_Caracteristicas
│   │   ├── Seccion_Precios
│   │   └── Footer
│   └── Pagina_Login
│       ├── Boton_Login_Google
│       └── Boton_Login_Notion
│
└── Layout_Privado (sidebar + auth guard)
    ├── Pagina_Pipeline (wizard 5 pasos)
    ├── Pagina_Biblioteca
    └── Pagina_Configuracion
```

### Pipeline — Wizard

```
Pagina_Pipeline
├── Barra_Progreso_Wizard (1-5)
│
├── Paso_P_Start
│   ├── Campo_Upload_Archivo (drag & drop)
│   │   └── Modal_Error_Formato
│   ├── Selector_Formato_Salida
│   ├── Config_Particion
│   ├── Selector_Ruta_Guardado
│   ├── Panel_Opciones_Estilo (condicional)
│   │   ├── Selector_Estilo_Block (6 opciones)
│   │   ├── Style_Config (para Highlight)
│   │   └── Style_Config (para Sub_Line)
│   ├── Config_Sub_Line_Campos
│   ├── Checkboxes (P_Display/P_Processing)
│   ├── Campo_Nombre_Archivo
│   └── Boton_Get_Highlights
│
├── Paso_P_Display (condicional)
│   ├── Barra_Herramientas
│   │   ├── Selector_Orden
│   │   ├── Selector_Agrupacion
│   │   └── Botones operaciones
│   ├── Tabla_Highlights (paginada)
│   │   └── Filas con checkbox + Shift/Ctrl
│   ├── Panel_Clippings (lateral)
│   ├── Preview_Completo (modal)
│   └── Boton_Proceder + Confirm_Dialog
│
├── Paso_P_Processing (condicional)
│   ├── Lista_Clippings_Desplegable
│   │   └── Item_Clipping_Processing
│   │       ├── Checkboxes de procesamiento
│   │       ├── Preview_Tiempo_Real
│   │       └── Botones guardar/repetir
│   └── Boton_Aceptar
│
├── Paso_P_Notion (condicional, sub-wizard)
│   ├── Sub_Paso_Conexion
│   ├── Sub_Paso_Matcheo
│   │   ├── Config_Matcheo_Automatico
│   │   ├── Lista_N_Matches (verde/rojo)
│   │   └── N_Explorer (para match manual)
│   ├── Sub_Paso_Posicion_Paste
│   └── Sub_Paso_Formato_N_Block
│       ├── Style_Config (extendido)
│       ├── Selector_Emoji
│       └── Preview_N_Block
│
└── Paso_P_End
    ├── Resumen_Desplegable
    ├── Boton_Finalizar
    ├── Barra_Progreso_Exportacion
    └── Panel_Resultado
        ├── Boton_Descargar
        └── Link_Ir_A_Biblioteca
```

### Biblioteca

```
Pagina_Biblioteca
├── Tabs (por archivo / unificada)
├── Vista_Por_Archivo
│   ├── Lista cards de archivos
│   └── Tabla_Highlights del seleccionado
└── Vista_Unificada
    └── Tabla_Highlights (filtrable)
```

### Configuración

```
Pagina_Configuracion
├── Seccion_Perfil
├── Seccion_Suscripcion
├── Seccion_Apariencia (tema, idioma)
├── Seccion_Exportacion_Defecto
│   └── Style_Config (reutilizable)
├── Seccion_Reglas_Marcas
│   └── Tabla editable
├── Seccion_Notion
├── Seccion_Confirmaciones
└── Seccion_Conexiones_OAuth
```

### Componentes reutilizables

| Componente | Usado en |
| --- | --- |
| N_Explorer (tree + buscador) | P_Notion, Config |
| Style_Config (fuente/color/tamaño/alineación) | P_Start, P_Notion, Config |
| Confirm_Dialog (con "no volver a preguntar") | P_Display, P_Processing, P_Notion, P_End |
| Highlight_Preview (renderiza estilos) | P_Display, P_Processing, P_End |
| Campo_Upload_Archivo (drag & drop) | P_Start |
| Tabla_Highlights (paginada, seleccionable) | P_Display, Biblioteca |
| Selector_Emoji | P_Notion |
| Barra_Progreso_Wizard | Pipeline, P_Notion |

### Routing

```
/                    → Landing
/login               → Login
/pipeline            → Pipeline wizard
/pipeline?paso=1..5  → Paso específico
/biblioteca          → Biblioteca
/biblioteca/:id      → Filtrado por archivo
/configuracion       → Configuración cuenta
```

### Gestión de estado

- **TanStack Query**: datos del servidor
  (highlights, clippings, configs). Cache +
  revalidación automática.
- **Zustand**: estado del wizard del pipeline
  (paso actual, datos acumulados, selecciones).
- **Estado local**: checkboxes de tabla,
  formularios antes de confirmar.

### Componentes shadcn/ui que se usan

Dialog, Table, Tabs, Accordion, Select,
Combobox, Checkbox, Input, Button, Progress,
DropdownMenu, Command (buscador N_Explorer),
Sheet (panel lateral preview), Toast.

---

## Terminología

| Término | Definición |
| --- | --- |
| Block | Highlight + metadata (autor, libro, etc.) |
| Highlight | Frase resaltada del libro |
| Sub_Line | Línea debajo del highlight (configurable) |
| F_Block | Block sobre el que se opera |
| C_Block | Block resultante de una operación |
| Clipping | Grupo de Blocks |
| B_Sort | Reordenar/agrupar/dividir/unir Blocks |
| H_Processing | Procesamiento del texto |
| Paste | Pegado en el formato de salida |
| N_Block | Bloque de Notion |
| N_Page | Página de Notion |
| N_Match | Conexión Clipping ↔ N_Page |
| N_Database | Página principal con N_Pages hijas |
| N_Explorer | Navegador Notion (tree + búsqueda) |
| O_Order | Orden original del archivo |
| F_Order | Orden final elegido por el usuario |
| Tipo semántico | Naturaleza del highlight |

---

## Fases de implementación

### Fase 0 — Setup del monorepo

- Crear monorepo: frontend/ + backend/.
- Setup React + Vite + shadcn/ui + Tailwind.
- Setup FastAPI + SQLAlchemy + Alembic.
- PostgreSQL + Redis en Railway.
- Docker compose para desarrollo local.
- Implementar OAuth Google + Notion.
- Modelo de Users + Conexiones_Oauth.
- Deploy inicial en Railway.

### Fase 1 — Parseo y core del backend

- Parser de Kindle TXT (regex robusto).
- Modelos: Highlights, Archivos_Subidos,
  Clippings, Clipping_Highlights.
- Endpoints: /files/upload, /highlights,
  /clippings, /clippings/agrupar.
- Upload de archivos a S3/R2.
- Límite free (50 highlights).
- Tests del parser y endpoints.

### Fase 2 — Frontend: Landing + Auth + P_Start

- Pagina_Landing (hero, features, pricing).
- Pagina_Login (OAuth Google + Notion).
- Layout_Privado con sidebar.
- Paso_P_Start completo con upload,
  formato, partición, estilos.
- Conexión frontend ↔ backend.

### Fase 3 — Frontend: P_Display + P_Processing

- Paso_P_Display: tabla paginada,
  operaciones de bloques, preview completo.
- Endpoints: combinar, dividir, reordenar.
- Paso_P_Processing: checkboxes, preview
  en tiempo real (debounce 300ms).
- Endpoints: /processing/preview, /aplicar.

### Fase 4 — Exportadores + P_End

- Todos los exportadores server-side:
  PDF, DOCX, DOC, ODT, CSV, XLSX, XLS,
  TXT, Obsidian (Markdown).
- Tasks Celery para exportación async.
- Paso_P_End: resumen, progreso, descarga.
- Descarga desde S3.

### Fase 5 — Notion completo

- Crear integración OAuth pública en Notion.
- N_Explorer (tree lazy-loaded + buscador).
- Matcheo configurable + manual.
- Sub-wizard de 4 pasos en P_Notion.
- Exportador Notion (Celery, rate limited).
- Config_Notion + N_Matches en DB.

### Fase 6 — Biblioteca + Config + DOCX

- Pagina_Biblioteca (dos vistas).
- Pagina_Configuracion completa.
- Parser DOCX con marcas de formato.
- Sistema de reglas personalizables.
- Implementar los 6 estilos de Block.

### Fase 7 — Pulido y testing

- Tema claro/oscuro.
- Tooltips de ayuda.
- Responsive (mobile).
- Tests end-to-end.
- Manejo de errores y edge cases.
- Performance y optimización.

---

## Verificación

1. Subir TXT Kindle → highlights correctos.
2. Subir DOCX con marcas → tipos semánticos ok.
3. Recorrer las 5 pantallas del wizard.
4. Exportar a cada uno de los 10 formatos.
5. Conectar Notion y subir highlights.
6. Crear cuenta, cerrar sesión, volver y ver
   highlights guardados en la biblioteca.
7. Probar en Chrome, Firefox, Safari.
8. Probar responsive en mobile.
9. Verificar límite de 50 highlights en free.
10. Verificar tema claro/oscuro.
