# Mapa de Superficie de Ataque — Figma Inc.

- **Organización:** Figma Inc. (`figma.com`)
- **Fecha de consolidación:** 2 de noviembre de 2026
- **Auditor/a:** Natalia Alejo Pérez (Alumno 20)
- **Ámbito:** `*.figma.com`, `weavy.ai`, `!www.designsystems.com` (Programa público HackerOne)

---

## 1. Resumen Ejecutivo (en 5 líneas)

Figma Inc. ofrece una plataforma SaaS de diseño colaborativo alojada íntegramente en la nube de **Amazon Web Services (AWS)**, repartida entre centros de datos de Estados Unidos y Europa. Su acceso público está protegido mediante **AWS CloudFront y cortafuegos AWS WAF**, dejando abiertos únicamente los puertos web habituales: HTTP (80) y HTTPS (443). El control de acceso y las cuentas internas se gestionan a través de **Okta (con autenticación multifactor)**, y el correo corporativo se apoya en **Google Workspace**. Tras esta fase de reconocimiento pasivo no se han detectado contraseñas expuestas ni servicios de administración abiertos a internet, aunque sí una superficie amplia de APIs y entornos de pruebas (staging) visibles públicamente.

---

## 2. Dominios y Subdominios Relevantes

De los **100 subdominios descubiertos** durante la fase de reconocimiento pasivo mediante `subfinder` y certificados SSL, se destacan en la siguiente tabla los activos más representativos y críticos para el modelado de amenazas.

> **Nota metodológica y anexo:** El listado completo y sin procesar de los 100 subdominios identificados se encuentra registrado en la **Entrada 03** del [cuaderno.md](./cuaderno.md) y preservado en el fichero de trabajo del entorno del laboratorio (`subdominios.txt`), garantizando la trazabilidad integral de la superficie descubierta.

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
- **Medidas Activas de Privacidad en Búsquedas Abiertas:** Durante la consulta con `theHarvester` sobre motores públicos (DuckDuckGo), no se identificaron direcciones de correo electrónico indexadas en texto plano accesible. Esto evidencia una **medida activa y deliberada de privacidad corporativa por parte de Figma** (ofuscación de datos en directorios públicos, prevención de recolección automatizada y políticas estrictas contra el scraping no autorizado para proteger a su plantilla contra ataques de ingeniería social y spam masivo).
- **Servicios de Envío Autorizados (SPF DNS):**
  - **Google Workspace** (`include:_spf.google.com`): Comunicaciones directas de los trabajadores.
  - **Zendesk** (`include:mail.zendesk.com`): Plataforma oficial de tickets y atención técnica a usuarios.
  - **Greenhouse** (`include:mg-spf.greenhouse.io`): Plataforma de gestión y selección de recursos humanos (HR).
- **Política Antisuplantación:** Configuración estricta `-all` (Hard Fail), lo que mitiga el riesgo de ataques de *Email Spoofing* directo sobre el dominio principal.
- **Identidad Interna:** Toda la plantilla opera bajo autenticación multifactor obligatoria gestionada mediante **Okta** y **Perma Security (Opal)** para asignación de privilegios de mínimo acceso.

---

## 5. Puntos de Interés Prioritarios (Fase Activa)

Si en una siguiente fase tuviéramos autorización para realizar pruebas activas (pentesting), los **tres puntos donde empezaría a investigar** serían:

### 1. Auditoría de la API pública y privada (`api.figma.com`)
- **Por qué:** Los puertos y la red están bien protegidos por AWS, por lo que el punto más débil suele ser la propia lógica de la aplicación web.
- **Qué probaría:** Buscar fallos de control de acceso en objetos (IDOR / BOLA del Top 10 de OWASP para APIs), ver cómo se validan los permisos entre diferentes usuarios que editan un mismo proyecto y comprobar si los endpoints tienen límites de peticiones (rate limiting) para evitar abusos.

### 2. Entornos de desarrollo y pruebas (`staging-admin.figma.com`, `*.staging.figma.com`)
- **Por qué:** En casi todas las empresas, las máquinas de staging o pruebas suelen tener configuraciones más descuidadas que las de producción real (versiones viejas, mensajes de error detallados con rutas internas o logins provisionales).
- **Qué probaría:** Comprobar si el panel administrativo de pruebas pide autenticación fuerte, revisar si el visor de trazas (`cortex-trace-viewer`) filtra datos técnicos y analizar las cabeceras en busca de librerías desactualizadas.

### 3. Ficheros y rutas en el subdominio de subidas (`static.figma.com/uploads/`)
- **Por qué:** Durante la búsqueda con Google Dorks encontramos que en este subdominio se alojan informes completos de auditoría interna de años anteriores.
- **Qué probaría:** Hacer fuzzing o rastreo de nombres de archivo comunes en ese bucket para comprobar si se han dejado por descuido otros documentos internos, manuales de procedimiento o archivos de configuración sin proteger.

---

*Nota metodológica: Cada dato incluido en este informe se encuentra debidamente respaldado por su correspondiente registro cronológico y evidencia gráfica en `cuaderno.md`.*
