---
name: prospector
description: "Scrapes local business leads from Google Maps using Apify and creates an Airtable base with all relevant data and a WhatsApp URL field per lead. Use when the user says /prospector, wants to prospect leads, scrape businesses into Airtable, or build a lead database. Requires: Apify API key, Airtable personal access token, niche and zone."
---

# Skill: Prospector

Scrapes Google Maps leads via Apify → crea una base Airtable `Leads [Nicho] [Zona]` con datos relevantes y un campo WhatsApp con link directo por lead.

## Inputs requeridos

Pedí al usuario lo que falte antes de ejecutar:

| Input | Cómo obtenerlo |
|---|---|
| `APIFY_KEY` | apify.com → Account → Integrations → API token |
| `AIRTABLE_TOKEN` | airtable.com/create/tokens — scopes: `schema.bases:write`, `data.records:write`, `schema.bases:read` |
| `niche` | Ej: "clínicas dentales", "restaurantes", "inmobiliarias" |
| `zone` | Ej: "Madrid", "Buenos Aires", "Miami" |
| `max_results` | Opcional, default 200 |
| `workspace_id` | Opcional — auto-detectado; si falla, abrí cualquier base en Airtable y mirá la URL |

## Ejecución

1. Instalar dependencia: `pip3 install requests -q`
2. Escribir el script a `/tmp/prospector.py` (ver sección "Script" al final de este archivo)
3. Correr:

```bash
python3 /tmp/prospector.py \
  --apify-key "APIFY_KEY" \
  --airtable-token "AIRTABLE_TOKEN" \
  --niche "NICHE" \
  --zone "ZONE" \
  --max-results 200
```

4. Si falla con `workspace_id not found`, agregar `--workspace-id "wspXXXXXXXX"`.

### Requisitos de red

El script necesita salida HTTPS hacia `api.apify.com`, `api.airtable.com` y
`nominatim.openstreetmap.org`. En entornos con política de egress restringida
(por ejemplo Claude Code en la web) esos hosts pueden estar bloqueados y el
proxy responde `403` al CONNECT. En ese caso, ejecutá la skill en local.

### Cobertura geográfica

El script geocodifica `zone` y le pasa a Apify `zoom: 12`, que cubre
aproximadamente el radio de una ciudad. Para una provincia o región amplia,
corré una vez por ciudad en lugar de usar el nombre de la provincia, y
consolidá las bases después.

## Campos que crea en Airtable

| Campo | Tipo |
|---|---|
| Empresa | Texto |
| Teléfono | Teléfono |
| Rating | Número (1 decimal) |
| Reseñas | Número |
| Categoría | Texto |
| Dirección | Texto |
| Ciudad | Texto |
| Web | URL |
| Google Maps | URL |
| WhatsApp | Fórmula URL (clickeable) |

### Fórmula del campo WhatsApp

```
"https://wa.me/" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE({Teléfono}, "+", ""), " ", ""), "-", ""), "(", "") & "?text=Hola%2C%20hablo%20con%20" & SUBSTITUTE({Empresa}, " ", "%20") & "%3F"
```

## Botón WhatsApp verde (paso manual — 30 seg)

La API de Airtable no soporta crear campos Button programáticamente. El script crea el campo WhatsApp como fórmula URL funcional. Para convertirlo en botón verde visual:

1. Abrí la base → click en **+** al final de las columnas
2. Tipo: **Button** · Nombre: `WhatsApp` · Label: `WhatsApp` · Color: verde
3. Action: **Open URL** → activar fórmula → pegar la fórmula de arriba
4. Save

## Manejo de errores

| Error | Causa | Solución |
|---|---|---|
| Apify 401 | API key inválida | Verificar en apify.com |
| Apify FAILED / 0 resultados | Scraper falló o término sin resultados | Reintentar con nicho más genérico |
| Airtable 403 | Token sin permisos | Agregar scopes `schema.bases:write`, `data.records:write`, `schema.bases:read` |
| workspace_id not found | Sin bases existentes para auto-detectar | Crear una base vacía en Airtable primero, o pasar `--workspace-id` |
| ProxyError / 403 al CONNECT | Host bloqueado por la política de red del entorno | Ejecutar en local (ver "Requisitos de red") |

---

## Script

Cuando el usuario pida ejecutar el skill, escribí el contenido de
[`prospector.py`](prospector.py) en `/tmp/prospector.py` usando la herramienta
Write o Bash, y luego ejecutalo con los parámetros provistos.
