
# Simple Scraper

Script de scraping de propósito general desarrollado en Python 3. 

Recibe la URL de una página que contiene una tabla de contenidos HTML, recorre sus enlaces y guarda el contenido de cada entrada en un archivo Markdown (`.md`) independiente.

Puede utilizarse para extraer documentación técnica, manuales, libros en línea y colecciones de artículos.

La documentación incluye:
- Descripción y propósito del scraper.
- Creación del proyecto e instalación de dependencias con uv.
- Ejemplos de ejecución y parámetros disponibles.
- Descripción de cada función del script.
- Estructura y nomenclatura de los archivos .md.
- Tratamiento de errores y mensajes de ejecución.
- Limitaciones de extracción y conservación del formato Markdown.
- Posibles mejoras futuras.



## Requisitos

- Python 3.
- [uv](https://docs.astral.sh/uv/).
- Acceso HTTP(S) a las páginas que se desean procesar.

## Instalación

Crear el proyecto:

```bash
uv init simple_scraper
cd simple_scraper
```

Instalar las dependencias:

```bash
uv add requests beautifulsoup4 trafilatura
```

Copiar `simple_scraper.py` al directorio del proyecto.

Si el proyecto ya existe, verificar que `pyproject.toml` tenga el nombre correcto:

```toml
[project]
name = "simple_scraper"
version = "0.1.0"
```

Actualizar las dependencias:

```bash
uv lock
uv sync
```

## Uso

El script recibe como argumento la URL de la tabla de contenidos.

**Ejemplo de uso:** el libro [Site Reliability Engineering de Google](https://sre.google/sre-book/table-of-contents/). 
El script no depende de este sitio y puede utilizarse con otras URLs que contengan una tabla de contenidos accesible mediante HTML.

### Ejemplo con Google SRE

```bash
uv run simple_scraper.py "https://sre.google/sre-book/table-of-contents/"
```

### Ejemplo genérico

```bash
uv run simple_scraper.py "https://example.com/contents/"
```

### Especificar el selector CSS

Permite limitar la búsqueda a los enlaces contenidos en un elemento HTML determinado:

```bash
uv run simple_scraper.py "https://example.com/contents/" --selector "#table-of-contents"
```

### Configurar la pausa entre solicitudes

```bash
uv run simple_scraper.py "https://example.com/contents/" --delay 2
```

### Ayuda

```bash
uv run simple_scraper.py --help
```

## Parámetros

| Parámetro | Descripción | Valor predeterminado |
|---|---|---|
| `url` | URL de la tabla de contenidos | Obligatorio |
| `--selector` | Selector CSS de la tabla | Toda la página |
| `--delay` | Pausa entre solicitudes, en segundos | `1.0` |

## Archivos generados

Cada entrada del índice que pueda extraerse genera un archivo Markdown en el directorio de ejecución.

Ejemplo:

```text
simple_scraper/
├── pyproject.toml
├── uv.lock
├── README.md
├── simple_scraper.py
├── 01-Foreword.md
├── 02-Preface.md
├── 03-Introduction.md
├── 04-The Production Environment at Google.md
└── ...
```

Los archivos se numeran siguiendo el orden de los enlaces detectados.

El contenido sigue esta estructura:

```markdown
# Título de la entrada

**Source:** https://example.com/chapter/

---

Contenido extraído en Markdown.
```

Los nombres se normalizan para eliminar caracteres incompatibles con los sistemas de archivos. Los archivos existentes con el mismo nombre pueden sobrescribirse.

## Funcionamiento interno

### `fetch_page()`

Descarga el HTML utilizando `requests`, una sesión HTTP y un timeout de 30 segundos.

### `get_toc_links()`

Analiza el HTML mediante Beautiful Soup y obtiene los enlaces de la tabla de contenidos.

- Convierte enlaces relativos en absolutos.
- Descarta enlaces duplicados.
- Elimina fragmentos de URL.
- Filtra enlaces según el host y el prefijo de ruta del índice.
- Permite limitar la búsqueda mediante un selector CSS.

### `extract_content()`

Utiliza Trafilatura para identificar el contenido principal y convertirlo a Markdown.

Configuración:

```python
output_format='markdown'
include_tables=True
include_links=True
include_images=True
include_comments=False
favor_recall=True
```

### `sanitize_filename()`

Normaliza los títulos para utilizarlos como nombres de archivo y limita su longitud.

### `scrape()`

Coordina el proceso completo: descarga del índice, identificación de enlaces, extracción, numeración y escritura de archivos.

## Formato Markdown

El script intenta conservar:

- Encabezados y subtítulos.
- Párrafos.
- Listas numeradas y viñetas.
- Tablas.
- Enlaces.
- Referencias a imágenes.

La fidelidad depende de la estructura HTML original. Las imágenes se referencian, pero no se descargan.

Los bloques de código, tablas complejas y ecuaciones pueden perder parte de su formato.

## Mensajes de ejecución

Ejemplo ilustrativo:

```text
Index: https://sre.google/sre-book/table-of-contents/
Output: /ruta/al/proyecto
Found N entries

[1/N] Foreword
  SAVED: 01-Foreword.md

Completed: X/N files saved
```

Mensajes posibles:

- `SAVED`: archivo generado.
- `SKIP: No content found`: no se pudo extraer contenido.
- `ERROR`: error de red o escritura.
- `CSS selector not found`: el selector no coincide con ningún elemento.

## Limitaciones

1. El script no identifica automáticamente cuál es la tabla de contenidos. Sin `--selector`, examina los enlaces de toda la página que superan los filtros de URL.
2. No ejecuta JavaScript. Algunos sitios con contenido dinámico pueden no funcionar.
3. No descarga imágenes ni otros archivos binarios.
4. No sigue índices anidados de manera recursiva.
5. Solo incluye enlaces del mismo host y bajo el prefijo de ruta determinado por la URL inicial.
6. No implementa reintentos automáticos ni tratamiento específico de errores HTTP 429.
7. No comprueba automáticamente `robots.txt` ni los términos de uso del sitio.
8. La conversión a Markdown no garantiza preservar íntegramente el formato original.

Se recomienda revisar las condiciones de acceso del sitio y utilizar `--delay` para evitar solicitudes excesivas.

## Dependencias

| Biblioteca | Propósito |
|---|---|
| `requests` | Solicitudes HTTP |
| `beautifulsoup4` | Análisis de HTML |
| `trafilatura` | Extracción y conversión a Markdown |

## Mejoras futuras

- Agregar `--output-dir` para configurar el directorio de salida.
- Implementar reintentos con backoff.
- Incorporar detección automática de tablas de contenidos.
- Generar un manifiesto con títulos, URLs y estado de extracción.
- Mejorar la conservación de bloques de código, ecuaciones y tablas complejas.
- Agregar filtros para incluir o excluir determinadas URLs.

