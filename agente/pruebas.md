# Comprobaciones de Alcance y Construcción del Prompt

- **Estudiante:** Natalia Alejo Pérez (Alumno 20)
- **Objetivo auditado:** Figma Inc. (`figma.com`)
- **Fichero de alcance:** `scope.txt`

---

## 2.1 Comprueba tu alcance (`scope.txt`)

Siguiendo las directrices del proyecto, se definen los casos de prueba con nombres y activos reales de la infraestructura de Figma Inc., contrastando el comportamiento esperado con el resultado obtenido por el sistema `Scope-Guard` de `aap-base`:

| Objetivo | Tipo de Activo | Resultado esperado | Resultado obtenido | Justificación / Regla |
| :--- | :--- | :---: | :---: | :--- |
| `api.figma.com` | Subdominio API | **Dentro** | **Dentro** | Coincide con la regla comodín `*.figma.com` y está explícitamente en `scope.txt`. |
| `https://www.figma.com/login` | URL web con ruta | **Dentro** | **Dentro** | El host extraído (`www.figma.com`) coincide con la lista de autorizados. |
| `weavy.ai` | Activo corporativo | **Dentro** | **Dentro** | Tecnología conversacional adquirida por Figma listada en el alcance de HackerOne. |
| `3.174.170.15` | Dirección IPv4 | **Dentro** | **Dentro** | Dirección perteneciente al rango de red autorizado de balanceo de Figma (`3.174.170.0/24`). |
| `www.designsystems.com` | Web comunitaria | **Fuera (excluido)** | **Fuera (BLOQUEADO)** | Regla explícita de exclusión `!www.designsystems.com` marcada como Out-of-Scope. |
| `zendesk.com` | Servicio de soporte | **Fuera (excluido)** | **Fuera (BLOQUEADO)** | Regla de exclusión `!zendesk.com` para evitar escanear infraestructura de terceros. |
| `statuspage.io` | Monitor de estado | **Fuera (excluido)** | **Fuera (BLOQUEADO)** | Regla de exclusión `!statuspage.io` (servicio SaaS externo no auditable). |
| `figma.com.evil.net` | Dominio engañoso | **Fuera** | **Fuera (BLOQUEADO)** | No pertenece al dominio base `figma.com` ni a sus subdominios legítimos. |
| `otraempresa.com` | Dominio no autorizado | **Fuera** | **Fuera (BLOQUEADO)** | Totalmente ajeno al alcance definido para la auditoría. |

---

## 2.3 Mira cómo se construye su prompt

Se ejecutó el comando de inspección del prompt ensamblado en el entorno de ejecución:
```bash
python lanzar.py --ver-prompt
```

### Prompt de Sistema resultante ensamblado:
```markdown
Eres un analista de reconocimiento pasivo dentro de una auditoria autorizada.

Esta es una PLANTILLA. El alcance y la lista de herramientas (más abajo) los rellena
el sistema solo, a partir de tu scope.txt y de las herramientas que tengas activas.
Puedes ver el prompt ya montado con: python lanzar.py --ver-prompt

## Objetivo y alcance

El objetivo te lo da el usuario. Solo puedes investigar lo que esté dentro de este
alcance autorizado:

Autorizado: figma.com, www.figma.com, api.figma.com, *.figma.com, weavy.ai, 3.174.170.0/24, 65.8.202.0/24
Excluido (nunca): www.designsystems.com, zendesk.com, statuspage.io

Si una herramienta te responde `BLOQUEADO`, ese objetivo está fuera: no insistas ni
lo intentes por otro camino; sigue con otra cosa.

## Herramientas disponibles

- whois_dominio: Consulta el registro WHOIS de un dominio. Devuelve registrador, fechas de registro y servidores de nombres (NS).
- dns_registros: Consulta registros DNS de un dominio. tipo: A, AAAA, MX, NS, TXT, CNAME o SOA.
- subdominios_crtsh: Enumera subdominios de un dominio por transparencia de certificados (crt.sh).
- shodan_host: Consulta la API de Shodan InternetDB para una dirección IP.
- ficheros_sensibles: Inspecciona ficheros públicos clave: /robots.txt y /.well-known/security.txt.
- subdominios_subfinder: Enumera subdominios pasivos usando la herramienta Subfinder instalada en el sistema.
- correo_postura: Evalúa la postura de seguridad del correo para el dominio.
- tecnologias_web: Inspecciona las cabeceras HTTP públicas (Server, CloudFront, HSTS, Cookies).
- reputacion_ip_asn: Consulta información de enrutamiento BGP, ASN, proveedor de hosting (ISP) y geolocalización.
- wayback_endpoints: Busca endpoints y rutas históricas archivadas en Wayback Machine (archive.org).
- fuga_correos: Recolecta de forma pasiva direcciones de correo y empleados expuestos usando theHarvester.

## Orden de trabajo

1. Registro del dominio.
2. DNS.
3. Subdominios.
4. Lo demás.

## Límites

- Como máximo 20 llamadas a herramientas. Usa todas las que aporten algo.
- Solo técnicas pasivas: nada que envíe tráfico al objetivo más allá de consultas públicas.

## Informe

Termina con un informe en Markdown. Para **cada dato**, indica qué herramienta lo devolvió, por ejemplo: `NS: ns1.empresa.com (whois_dominio)`. Si no tienes una herramienta que respalde un dato, no lo incluyas.
```

### Análisis explicativo del prompt montado:
1. **Origen del bloque de Alcance (`{alcance}`):** Proviene íntegramente del procesamiento de nuestro archivo `scope.txt`. El motor parsea automáticamente las líneas limpias como objetivos autorizados (`figma.com`, `*.figma.com`, `weavy.ai`, etc.) y convierte las líneas con prefijo `!` en exclusiones estrictas (`Excluido (nunca): www.designsystems.com, zendesk.com, statuspage.io`).
2. **Origen del bloque de Herramientas (`{herramientas}`):** Proviene de la lista de herramientas registradas en `lanzar.py`. El sistema extrae el docstring y los parámetros de cada función decorada en `herramientas/tus_herramientas.py` y `herramientas/whois.py`, presentándoselas al LLM con su firma técnica para que sepa cuándo y cómo invocarlas vía *Function Calling*.
3. **Instrucciones ante `BLOQUEADO`:** El prompt delimita explícitamente el comportamiento ético del modelo: si `Scope-Guard` intercepta una llamada y responde `BLOQUEADO`, el modelo tiene orden imperativa de no insistir ni buscar rodeos o técnicas evasivas, debiendo continuar con el siguiente activo autorizado.
4. **Atribución estricta de fuentes:** Para evitar alucinaciones, el prompt exige que todo dato plasmado en el informe final cite obligatoriamente la herramienta que lo obtuvo entre paréntesis (ej. `(whois_dominio)` o `(dns_registros)`), prohibiendo incluir datos que no hayan sido devueltos formalmente por una función.

