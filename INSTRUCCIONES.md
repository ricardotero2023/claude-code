# Zona Informática Pontevedra – Sitio Web

Sitio web estático para **Informática de Zona S.L.** (Zona Informática Pontevedra), preparado para justificación del **Kit Digital** – categoría *Sitio web y presencia básica en internet*.

---

## Estructura de archivos

```
/
├── index.html              ← Página principal (Homepage)
├── servicios.html          ← Página de servicios (6 servicios detallados)
├── sobre-nosotros.html     ← Página sobre la empresa
├── contacto.html           ← Formulario de contacto + mapa
├── aviso-legal.html        ← Aviso legal (LSSICE)
├── politica-privacidad.html ← Política de privacidad (RGPD + LOPDGDD)
├── politica-cookies.html   ← Política de cookies + tabla de cookies
├── robots.txt              ← Directrices para buscadores
├── sitemap.xml             ← Mapa del sitio para SEO
├── css/
│   └── style.css           ← Hoja de estilos (responsive, accesible)
├── js/
│   └── main.js             ← JavaScript (menú móvil, cookies, formulario, animaciones)
└── img/
    └── logo.png            ← ⚠️ DEBES AÑADIR EL LOGO AQUÍ
```

---

## Pasos para poner en marcha

### 1. Añadir el logo
Descarga el logo desde Facebook o usa el archivo proporcionado y guárdalo en:
```
img/logo.png
```
Tamaño recomendado: 200×200 px mínimo, fondo transparente (PNG).

### 2. Actualizar datos de contacto
Busca y reemplaza en todos los archivos HTML:
- `986 000 000` → número de teléfono real
- `info@zonagalicia.com` → email real
- `Pontevedra, Galicia` → dirección completa real
- `B-XXXXXXXX` → CIF real de Informática de Zona S.L.

### 3. Actualizar el mapa (contacto.html)
En `contacto.html`, reemplaza el iframe de Google Maps con el código embed real de la ubicación de la tienda.

### 4. Configurar el formulario de contacto
El formulario en `contacto.html` tiene un submit simulado (JavaScript). Para que funcione de verdad, elige una de estas opciones:
- **WordPress + Contact Form 7** (recomendado si usas WP)
- **Formspree** (https://formspree.io): cambia el `action` del form por el endpoint de Formspree
- **PHP propio**: crea un `procesar-contacto.php` en el servidor

---

## Implementación en WordPress

Para subir a WordPress mantén la estructura visual usando el **tema hijo** o un **constructor de páginas** (Elementor, Gutenberg con bloques de código HTML):

1. Crea las páginas en WP: Inicio, Servicios, Sobre nosotros, Contacto
2. Para cada página: pega el contenido del `<main>` del HTML correspondiente en un bloque **HTML personalizado**
3. Sube el `style.css` como **tema hijo** o añádelo mediante *Personalizar → CSS adicional*
4. Sube el `main.js` mediante un plugin (e.g. *Insert Headers and Footers*) o el theme
5. Para el formulario: usa **Contact Form 7** o **WPForms**
6. Para las cookies: usa **Complianz** o **CookieYes** (plugin)
7. Configura el **plugin Yoast SEO** con los mismos meta title y description

---

## Requisitos Kit Digital cubiertos ✅

| Requisito | Estado |
|-----------|--------|
| Dominio propio (zonagalicia.com) | ✅ (ya tienen el dominio) |
| Diseño responsive (móvil/tablet/escritorio) | ✅ |
| Accesibilidad WCAG 2.1 nivel AA | ✅ (landmarks, aria, skip-link, focus-visible) |
| SEO on-page (title, meta, H1, alt, canonical) | ✅ |
| Structured data (Schema.org LocalBusiness) | ✅ |
| Mínimo 3 páginas indexadas | ✅ (7 páginas) |
| Formulario de contacto | ✅ |
| Aviso legal | ✅ |
| Política de privacidad (RGPD) | ✅ |
| Política de cookies + banner | ✅ |
| Redes sociales vinculadas (Facebook) | ✅ |
| Sitemap XML | ✅ |
| robots.txt | ✅ |
| HTTPS | ✅ (depende del hosting) |

---

## Notas para justificación Kit Digital

- El sitio web está desarrollado con **tecnología web estándar** (HTML5, CSS3, JavaScript ES6)
- Es apto para migración a **WordPress** u otro CMS para facilitar la gestión
- Cumple los requisitos mínimos de la **Resolución de 30 de noviembre de 2021** de Red.es para la categoría *Sitio web y presencia básica en internet*
- La dirección de correo y datos fiscales del Aviso Legal deben completarse antes de la publicación

---

*Desarrollado para Informática de Zona S.L. — Kit Digital 2025*
