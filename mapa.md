# Mapa de Superficie de Ataque — Figma Inc.

- **Organización:** Figma Inc. (`figma.com`)
- **Fecha de consolidación:** 2 de noviembre de 2026
- **Auditor/a:** Alumno 20
- **Ámbito:** `*.figma.com`, `weavy.ai`, `!www.designsystems.com` (Programa público HackerOne)

---

## 1. Resumen Ejecutivo (en 5 líneas)

Figma Inc. opera una plataforma SaaS de diseño colaborativo alojada íntegramente en la infraestructura elástica de **Amazon Web Services (AWS)** con despliegues redundantes en EE. UU. y Europa. Su perímetro público está altamente blindado mediante **AWS CloudFront y AWS WAF**, exponiendo únicamente los puertos estándar HTTP/S (80 y 443). La autenticación corporativa y de usuarios se encuentra centralizada mediante **Okta (SSO/MFA)** y las comunicaciones de correo delegadas en **Google Workspace**. No se han identificado credenciales expuestas ni puertos de administración accesibles de forma directa, pero sí una amplia superficie de microservicios, APIs y entornos de pre-producción/staging indexados públicamente.

---

## 2. Dominios y Subdominios Relevantes

De los **100 subdominios descubiertos** durante la fase de reconocimiento pasivo mediante `subfinder` y certificados SSL, se destacan los activos más representativos agrupados por su criticidad e impacto:

| Subdominio | Dirección IP / Hostname | En Alcance (In Scope) | Función Estimada / Rol en la Superficie |
| :--- | :--- | :--- | :--- |
| `www.figma.com` | `3.174.170.42` (CloudFront) | **Sí** | Portal web principal, documentación y entrada a la aplicación. |
| `api.figma.com` | `3.174.170.3` (AWS ALB) | **Sí** | API REST y GraphQL consumida por clientes web, desktop y plugins. |
| `staging-admin.figma.com` | AWS Edge Cluster | **Sí** | Panel de administración en entorno de pruebas pre-producción. |
| `artifactory.staging.figma.com` | AWS Cloud Cluster | **Sí** | Repositorio de artefactos y binarios en fase de desarrollo. |
| `cortex-trace-viewer-dev.staging.figma.com` | AWS Cloud Cluster | **Sí** | Visor de trazas y depuración interna para desarrolladores. |
| `status.figma.com` | Servidor externo (Statuspage) | **Sí** (Informativo) | Monitor de estado del servicio y registro de incidentes pasados. |
| `static.figma.com` | Amazon S3 / CloudFront | **Sí** | Servidor de subida de ficheros y contenidos estáticos públicos (PDFs). |
| `weavy.ai` | Clúster Cloud dedicado | **Sí** | Plataforma de tejido y colaboración inteligente integrada en Figma. |
| `www.designsystems.com` | Host externo | **NO (Excluido)** | Blog / comunidad sobre sistemas de diseño marcada como fuera de alcance en HackerOne. |

---

## 3. Infraestructura y Servicios de Red

| Capa | Proveedor / Tecnología | Detalle Técnico |
| :--- | :--- | :--- |
| **Hosting Cloud** | Amazon Web Services (AWS) | Regiones activas: `US West`, `US East`, `EU Central` (Frankfurt) y `EU West` (Irlanda). |
| **CDN / Perímetro** | AWS CloudFront / Envoy | Terminación TLS, compresión HTTP/2 y HTTP/3 (`h2,h3`), balanceo con ALB. |
| **Puertos Expuestos** | `80/TCP` (HTTP), `443/TCP` (HTTPS) | Verificado vía Shodan InternetDB. Cero puertos de gestión (SSH/RDP) abiertos. |
| **Servidores DNS** | Amazon Route 53 | `awsdns-26.org`, `awsdns-15.co.uk`, `awsdns-40.com`, `awsdns-50.net`. |
| **Tecnologías Web** | Next.js, Netlify, WebGPU/Wasm | Frontend reactivo de alto rendimiento; compresión gzip/brotli. |
| **Almacenamiento** | AWS S3 & Amazon RDS | Base de datos relacional sobre Linux; S3 para assets y ficheros. |
| **Servicio de Correo** | Google Workspace | Registros MX autorizados: `aspmx.l.google.com`. |

---

## 4. Correos y Factor Humano

- **Patrón de Correo Corporativo:** `{first}.{last}@figma.com` (deducido y verificado a través de estructuras de contacto en soporte y auditorías).
- **Servicios de Envío Autorizados (SPF DNS):**
  - **Google Workspace** (`include:_spf.google.com`): Comunicaciones directas de los trabajadores.
  - **Zendesk** (`include:mail.zendesk.com`): Plataforma oficial de tickets y atención técnica a usuarios.
  - **Greenhouse** (`include:mg-spf.greenhouse.io`): Plataforma de gestión y selección de recursos humanos (HR).
- **Política Antisuplantación:** Configuración estricta `-all` (Hard Fail), lo que mitiga el riesgo de ataques de *Email Spoofing* directo sobre el dominio principal.
- **Identidad Interna:** Toda la plantilla opera bajo autenticación multifactor obligatoria gestionada mediante **Okta** y **Perma Security (Opal)** para asignación de privilegios de mínimo acceso.

---

## 5. Puntos de Interés Prioritarios (Fase Activa)

Si el alcance permitiera avanzar hacia una fase activa autorizada (Pentesting / Explotación), los **tres vectores prioritarios** a investigar serían:

### 1. Auditoría de Seguridad sobre la API (`api.figma.com`)
- **Por qué:** Al estar blindado el perímetro de red a nivel de puertos por AWS, el vector más plausible reside en la **lógica de negocio de la aplicación**.
- **Qué probar:** Pruebas de autorización horizontal y vertical (**BOLA / IDOR** en OWASP API Top 10), validación de tokens de sesión OAuth y límites de peticiones (Rate Limiting) en endpoints que interactúan con archivos de diseño.

### 2. Entornos de Staging y Pre-producción (`staging-admin.figma.com`, `*.staging.figma.com`)
- **Por qué:** Los entornos de desarrollo y staging frecuentemente cuentan con controles de seguridad más relajados que producción (mensajes de depuración detallados, librerías sin actualizar o paneles de acceso provisionales).
- **Qué probar:** Comprobación de autenticación en paneles administrativos, exposición de endpoints de trazabilidad (`cortex-trace-viewer`) y posibles fugas de información técnica en respuestas de error.

### 3. Fugas de Información en Almacenamiento Estático (`static.figma.com/uploads/`)
- **Por qué:** La búsqueda mediante Google Dorks demostró que este subdominio indexa documentación interna de auditoría y certificación.
- **Qué probar:** Enumeración pasiva/activa de rutas y nombres de ficheros en el bucket para detectar documentos no vinculados, borradores de políticas o ficheros de configuración olvidados por desarrolladores.

---

*Nota metodológica: Cada dato incluido en este informe se encuentra debidamente respaldado por su correspondiente registro cronológico y evidencia gráfica en `cuaderno.md`.*
