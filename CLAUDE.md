# Highlighter

App web para procesar resaltados de libros digitales
y exportarlos a múltiples formatos. Público general.

## Stack

### Frontend

- React (Vite o Next.js)
- Librería de componentes UI (a definir)

### Backend

- FastAPI (Python)
- SQLAlchemy + PostgreSQL
- OAuth (Google + Notion)

### Dependencias de exportación

- fpdf2 (PDF)
- python-docx (DOCX)
- pypandoc (DOC, ODT)
- openpyxl (XLSX)
- pandas (CSV, XLSX, procesamiento)
- notion-client (Notion API)

### Hosting

- Vercel / Railway / Render (tier gratuito)

## Pipeline (5 pantallas)

1. P_Start: subir archivo + configuración
2. P_Display: ordenar, agrupar, editar bloques
3. P_Processing: limpiar y normalizar texto
4. P_Notion: matchear con Notion (si aplica)
5. P_End: exportar al formato elegido

## Formatos de entrada

- Kindle TXT (MVP)
- DOCX/DOC con marcas de formato (Fase 2)
- Otros e-readers (futuro)

## Formatos de salida

PDF, DOCX, DOC, ODT, CSV, XLSX, XLS, TXT,
Notion, Obsidian (Markdown)

## Módulos externos

Los módulos en `../Modulio/` son librerías propias
reutilizables. Se pueden modificar si hace falta:
Highpy, Frampy, Stringpy, Listpy, Graphpy, Notpy

## Terminología

- **Block**: highlight + metadata (autor, libro, etc.)
- **Highlight**: frase resaltada del libro
- **Sub_Line**: línea debajo del highlight (autor/libro)
- **F_Block**: block sobre el que se opera
- **C_Block**: block resultante de una operación
- **Clipping**: grupo de blocks
- **B_Sort**: reordenar/agrupar/dividir/unir blocks
- **H_Processing**: procesamiento del texto
- **Paste**: pegado en el formato de salida
- **N_Block / N_Page / N_Match / N_Database**:
  entidades de Notion
- **Tipo semántico**: naturaleza del highlight
  (toggle, callout, quote, etc.)
- **O_Order**: orden original del archivo
- **F_Order**: orden final elegido por el usuario
