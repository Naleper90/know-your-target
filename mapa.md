# Mapa de Superficie de Ataque — Figma Inc.

- **Organización:** Figma Inc. (`figma.com`)
- **Fecha de consolidación:** 2 de noviembre de 2026
- **Auditor/a:** Natalia Alejo Pérez (Alumno 20)
- **Ámbito oficial:** `www.figma.com`, `api.figma.com`, `weavy.ai`; excluido `www.designsystems.com` (Programa público HackerOne). El comodín `*.figma.com` **no figura** en la tabla oficial (véase [alcance.md](./alcance.md)).

---

## 1. Resumen Ejecutivo (en 5 líneas)

Figma Inc. ofrece una plataforma SaaS de diseño colaborativo. Su acceso público pasa por **Amazon CloudFront** (cabeceras y CPE de Shodan, Entradas 05 y 07) y Route 53 gestiona su DNS (Entrada 06). En la IP consultada solo se vieron los puertos web 80 y 443 (Shodan InternetDB, Entrada 07). Según su informe SOC 3 público, usan AWS, Okta con autenticación multifactor y otras herramientas internas (Entrada 08), y su correo corporativo se apoya en **Google Workspace** (Entradas 02 y 09). No se han detectado contraseñas expuestas ni servicios de administración abiertos, pero `subfinder` descubrió 100 subdominios, entre ellos de staging, que **no figuran en el alcance oficial del programa**.

---

## 2. Dominios y Subdominios Relevantes

De los **100 subdominios descubiertos** durante la fase de reconocimiento pasivo mediante `subfinder` (Entrada 03), se destacan en la siguiente tabla los activos más representativos y críticos para el modelado de amenazas.

> **Nota metodológica y anexo:** El listado completo y sin procesar de los 100 subdominios identificados se encuentra registrado en la **Entrada 03** del [cuaderno.md](./cuaderno.md) y preservado en el fichero de trabajo del entorno del laboratorio (`subdominios.txt`), garantizando la trazabilidad integral de la superficie descubierta.

| Subdominio | Dirección IP / Hostname | En alcance oficial | Función estimada (deducida del nombre, no verificada) |
| :--- | :--- | :--- | :--- |
| `www.figma.com` | `3.174.170.42` (nodo de CloudFront, Entradas 05 y 07) | **Sí** | Portal web principal y entrada a la aplicación. |
| `api.figma.com` | No resuelta en el cuaderno | **Sí** | API consumida por la aplicación. |
| `weavy.ai` | No resuelta en el cuaderno | **Sí** | Figma Weave, listado en la tabla oficial. |
| `staging-admin.figma.com` | No resuelta en el cuaderno | **No** (no figura en la tabla) | Posible panel de administración de pruebas. |
| `artifactory.staging.figma.com` | No resuelta en el cuaderno | **No** (no figura en la tabla) | Posible repositorio de artefactos de desarrollo. |
| `cortex-trace-viewer-dev.staging.figma.com` | No resuelta en el cuaderno | **No** (no figura en la tabla) | Posible visor de trazas para desarrolladores. |
| `status.figma.com` | No resuelta en el cuaderno | **No** (no figura en la tabla) | Posible página de estado del servicio. |
| `static.figma.com` | No resuelta en el cuaderno | **No** (no figura en la tabla) | Aloja los PDF de cumplimiento hallados con Google Dorks (Entrada 08). |
| `www.designsystems.com` | No consultada | **No (excluido)** | Marcado como fuera de alcance en HackerOne. |

> Las IPs que no se resolvieron se indican como tal. No se dan direcciones genéricas ("AWS Cloud Cluster") porque no hay una resolución que las respalde.

--- | :--- | :--- | :--- |
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
| **Hosting Cloud** | Amazon Web Services (AWS) | Regiones citadas en el informe SOC 3 público de Figma (Entrada 08): `US West`, `US East`, `EU Central` y `EU West`. |
| **CDN / Perímetro** | Amazon CloudFront | Cabecera `via: CloudFront` (Entrada 05) y CPE de Shodan (Entrada 07). Soporta HTTP/2 y HTTP/3 (ALPN `h2,h3`, Entrada 02). La ubicación «Madrid» que dan las herramientas es la del nodo de borde de la CDN, no la de un servidor de Figma. |
| **Puertos Expuestos** | `80/TCP` (HTTP), `443/TCP` (HTTPS) | Shodan InternetDB sobre la IP `3.174.170.42`, que es un nodo de CloudFront (Entrada 07). Sin puertos de gestión (SSH/RDP) en esa IP. |
| **Servidores DNS** | Amazon Route 53 | Tres servidores de nombres anotados en la Entrada 06 (`awsdns-26.org`, `awsdns-15.co.uk`, `awsdns-40.com`). Un cuarto (`awsdns-50.net`) aparece en la salida del agente (`traza.jsonl`), no en mi cuaderno. |
| **Tecnologías Web** | Next.js, Netlify | Detectadas por `whatweb` en las cabeceras de `www.figma.com` (Entrada 05). |
| **Almacenamiento** | Posible AWS S3 | Deducido de nombres de subdominios como `s3-figma-plugin-images-production-sig.figma.com` (Entrada 03). **No verificado.** |
| **Servicio de Correo** | Google Workspace | Registros MX autorizados: `aspmx.l.google.com`. |

---

## 4. Correos y Factor Humano

- **Patrón de Correo Corporativo:** **No determinado.** `theHarvester` no devolvió ningún correo (Entrada 09), por lo que no se pudo verificar ningún patrón.
- **Resultado de `theHarvester`:** Con DuckDuckGo como única fuente no se obtuvo ningún correo en texto plano. No se puede concluir el motivo (puede deberse a la fuente o a la herramienta), por lo que no se interpreta como una medida de privacidad de Figma.
- **Servicios de Envío Autorizados (SPF DNS):**
  - **Google Workspace** (`include:_spf.google.com`): Comunicaciones directas de los trabajadores.
  - **Zendesk** (`include:mail.zendesk.com`): Plataforma oficial de tickets y atención técnica a usuarios.
  - **Greenhouse** (`include:mg-spf.greenhouse.io`): Plataforma de gestión y selección de recursos humanos (HR).
- **Política Antisuplantación:** Configuración estricta `-all` (Hard Fail), lo que mitiga el riesgo de ataques de *Email Spoofing* directo sobre el dominio principal.
- **Identidad Interna:** Según el informe SOC 3 público de Figma (Entrada 08), usan **Okta** (SSO y MFA) y **Opal** para el control de accesos. Es información que declara la propia empresa, no comprobada.

---

## 5. Puntos de Interés Prioritarios (Fase Activa)

Si en una siguiente fase tuviéramos autorización para realizar pruebas activas (pentesting), los **tres puntos donde empezaría a investigar** serían:

### 1. Auditoría de la API pública y privada (`api.figma.com`)
- **Por qué:** `api.figma.com` es uno de los dos hosts concretos del alcance oficial. En el perímetro de CloudFront solo se vieron los puertos web, por lo que en una fase activa el interés estaría en la lógica de la aplicación.
- **Qué probaría:** Buscar fallos de control de acceso en objetos (IDOR / BOLA del Top 10 de OWASP para APIs), ver cómo se validan los permisos entre diferentes usuarios que editan un mismo proyecto y comprobar si los endpoints tienen límites de peticiones (rate limiting) para evitar abusos.

### 2. Entornos de desarrollo y pruebas (`staging-admin.figma.com`, `*.staging.figma.com`) — no figuran en el alcance oficial
- **Por qué:** Los entornos de pruebas suelen estar menos cuidados que producción. **Antes de cualquier prueba activa habría que confirmar con el programa si estos subdominios son elegibles**, porque no figuran en la tabla oficial.
- **Qué probaría:** Comprobar si el panel administrativo de pruebas pide autenticación fuerte, revisar si el visor de trazas (`cortex-trace-viewer`) filtra datos técnicos y analizar las cabeceras en busca de librerías desactualizadas.

### 3. Ficheros y rutas en el subdominio de subidas (`static.figma.com/uploads/`) — no figura en el alcance oficial
- **Por qué:** Durante la búsqueda con Google Dorks encontramos que este subdominio aloja informes públicos de cumplimiento (SOC 3 e ISO 27001). Convendría comprobar si hay más documentos indexados.
- **Qué probaría:** Solo con autorización del programa, revisar los ficheros indexados por buscadores y valorar si algún documento no debería ser público.

---

*Nota metodológica: Los datos que se indican como «no verificado», «no determinado» o «deducido» no tienen respaldo directo en `cuaderno.md`. El resto se puede rastrear hasta la entrada del cuaderno que se cita.*
