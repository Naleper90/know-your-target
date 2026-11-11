# Proyecto 1 · Know Your Target — Reconocimiento Pasivo y Agente de IA

<p align="center">
  <img src="https://img.shields.io/badge/Auditora-Natalia%20Alejo%20P%C3%A9rez-blue.svg" alt="Auditora" />
  <img src="https://img.shields.io/badge/Curso-Especializaci%C3%B3n%20en%20Ciberseguridad-red.svg" alt="Curso" />
  <img src="https://img.shields.io/badge/Centro-IES%20Rafael%20Alberti-green.svg" alt="Centro" />
  <img src="https://img.shields.io/badge/Objetivo-Figma%20Inc.-purple.svg" alt="Objetivo" />
</p>

---

## 🎯 Resumen del Proyecto

Este repositorio documenta el desarrollo y los resultados del **Proyecto 1: Know Your Target** dentro del módulo de Hacking Ético del Curso de Especialización en Ciberseguridad.

El proyecto aborda la **fase de reconocimiento pasivo y modelado de superficie de ataque** sobre una organización tecnológica real: **Figma Inc.** (`figma.com`), bajo el marco legal de su programa público de divulgación responsable en **HackerOne**.

La investigación se ha ejecutado en **dos fases complementarias**:
1. **Fase Manual:** Aplicación de las 8 técnicas de recolección de información pública (RDAP/WHOIS, DNS, subdominios, huella tecnológica, ficheros expuestos, Shodan InternetDB, Google Dorks y correos/SPF), sin escaneos activos. Las peticiones directas a Figma se limitaron a `robots.txt`, `security.txt` y las cabeceras de `www.figma.com`. Cada acción consta en el cuaderno de trabajo.
2. **Fase Autónoma (Agente Ofensivo de IA):** Implementación y extensión del esqueleto `aap-base`, dotando al modelo de lenguaje de **11 herramientas pasivas desarrolladas en Python**, protegidas por el `scope-guard` de `aap-base`.
3. **Fase Comparativa y Reflexión:** Evaluación crítica que enfrenta el trabajo manual frente al informe autónomo del agente, analizando tiempos, omisiones, errores de interpretación y qué conviene comprobar siempre en el informe de un agente.

---

## 📁 Estructura del Repositorio

El repositorio sigue la estructura de entrega indicada en el enunciado:

```text
know-your-target/
├── README.md               # Portada, resumen ejecutivo y mapa de navegación
├── alcance.md              # Marco legal, programa HackerOne, reglas y exclusiones
├── scope.txt               # Fichero de alcance en texto plano para el Scope-Guard
├── cuaderno.md             # Bitácora cronológica paso a paso (las 5 anotaciones obligatorias)
├── mapa.md                 # Mapa de superficie de ataque y modelado de amenazas
├── comparativa.md          # Análisis comparativo profundo: humano vs agente + reflexión
├── img/                    # Evidencias gráficas y capturas oficiales de cada técnica
└── agente/
    ├── src/
    │   └── tus_herramientas.py  # 11 herramientas pasivas implementadas con timeout
    ├── pruebas.md          # Batería de pruebas de alcance y disección del prompt del sistema
    ├── instrucciones.md    # Plantilla de directivas éticas y de reporte del agente
    ├── traza.jsonl         # Traza técnica real de la ejecución del agente en el aula
    └── informe.md          # Informe técnico redactado de forma autónoma por la IA
```

---

## 🧭 Mapa de Documentación y Acceso Rápido

| Documento | Descripción y Contenido Clave | Enlace Directo |
| :--- | :--- | :---: |
| 📋 **Alcance y Marco Legal** | Análisis del programa de HackerOne, límites de peticiones, prohibición de DoS y reglas éticas. | [alcance.md](./alcance.md) |
| 🎯 **Fichero de Scope** | Formato de inclusión y exclusión (`!`) que consume el motor de Python del agente. | [scope.txt](./scope.txt) |
| 📓 **Cuaderno de Trabajo** | Bitácora de 9 entradas cronológicas documentando comandos, salidas y siguientes pasos. | [cuaderno.md](./cuaderno.md) |
| 🗺️ **Mapa de Superficie** | Informe técnico con resumen en 5 líneas, tabla de subdominios, infraestructura AWS y puntos de entrada. | [mapa.md](./mapa.md) |
| 🤖 **Pruebas del Agente** | Comprobación de límites con activos reales de Figma y análisis de las directivas del prompt. | [agente/pruebas.md](./agente/pruebas.md) |
| 📊 **Informe del Agente** | Documento Markdown generado por el modelo tras consultar las herramientas en el aula. | [agente/informe.md](./agente/informe.md) |
| ⚖️ **Análisis Comparativo** | Tabla comparativa humano vs máquina, análisis de fallos en traza y reflexión ética. | [comparativa.md](./comparativa.md) |

---

## 🛠️ Herramientas Implementadas en el Agente (`src/tus_herramientas.py`)

Para extender las capacidades del agente más allá del ejemplo básico, se programaron e integraron **11 herramientas pasivas** en Python:

1. `whois_dominio`: Consulta y parseo de entidades registradoras y servidores de nombres autoritativos.
2. `dns_registros`: Resolución de tipos de registros A, AAAA, MX, NS, SOA y TXT con `dnspython`.
3. `subdominios_crtsh`: Extracción de subdominios a partir del registro público de transparencia de certificados TLS.
4. `subdominios_subfinder`: Integración en segundo plano con la herramienta oficial Subfinder respetando timeouts.
5. `shodan_host`: Consulta de la API InternetDB de Shodan para identificación de puertos y vulnerabilidades sin escaneo activo.
6. `ficheros_sensibles`: Descarga y conteo de directivas en `/robots.txt` y políticas en `/.well-known/security.txt`.
7. `correo_postura`: Evaluación de cabeceras de seguridad SPF y directivas de cuarentena/rechazo en DMARC.
8. `tecnologias_web`: Inspección de cabeceras HTTP públicas (detección de la CDN CloudFront y de HSTS).
9. `reputacion_ip_asn`: Consulta de enrutamiento BGP, sistema autónomo (ASN) y geolocalización de IPs.
10. `fuga_correos`: Búsqueda pasiva de correos expuestos con theHarvester.
11. `wayback_endpoints`: Consulta de rutas históricas archivadas en la Wayback Machine.

---

## ✏️ Correcciones y Limitaciones

El 11/11/2026 se revisó la documentación contra la traza del agente y las capturas de HackerOne:

- El alcance oficial (`scope.txt`, [alcance.md](./alcance.md)) se corrigió: el comodín `*.figma.com` no figura en la tabla de HackerOne.
- El agente se ejecutó con un alcance más amplio que el `scope.txt` actual y la ejecución no puede repetirse (apartado 3.4 de [comparativa.md](./comparativa.md)).
- La [comparativa](./comparativa.md) y el [mapa](./mapa.md) se corrigieron con los datos reales de la traza y del cuaderno.

---

## 👩‍💻 Autoría y Declaración de Originalidad

- **Estudiante:** Natalia Alejo Pérez (Alumno 20)
- **Centro Educativo:** IES Rafael Alberti
- **Curso Académico:** 2026/2027
- **Compromiso Ético:** Toda la actividad descrita en este repositorio ha sido desarrollada estrictamente con fines formativos, limitándose al marco legal del programa público de Figma en HackerOne y respetando el principio de no interferencia con la disponibilidad de los servicios auditados.
