# 1.2 Alcance del Proyecto: Figma Inc.

- **Organización / Programa:** Figma Inc.
- **Plataforma:** HackerOne
- **Enlace al programa oficial:** [https://hackerone.com/figma](https://hackerone.com/figma)
- **Fecha de consulta:** 28 de octubre de 2026

---

## 1. Dentro del Alcance (In-Scope)

Según la tabla oficial de activos de HackerOne, los siguientes elementos están formalmente en el ámbito:

| Activo | Tipo | Cobertura | Gravedad Máxima | Elegibilidad |
| :--- | :--- | :--- | :--- | :--- |
| `www.figma.com` | Dominio | En el ámbito | Crítico | Elegible |
| `api.figma.com` | Dominio | En el ámbito | Crítico | Elegible |
| `weavy.ai` (Tejido Figma / Weave) | Web / Iframe | En el ámbito | Crítico | Elegible |
| Aplicación de escritorio Figma | Aplicación | En el ámbito | Crítico | Elegible |
| Aplicaciones para iOS y Android | Móvil | En el ámbito | Crítico | Elegible |
| Integraciones oficiales (Slack, Teams, Atlassian Jira) | Integraciones | En el ámbito | Crítico | Elegible |

---

> **Nota sobre el comodín (corrección del 11/11/2026):** La tabla oficial de HackerOne **no incluye el comodín `*.figma.com` ni el dominio raíz `figma.com`**: lista solo hosts concretos (`www.figma.com`, `api.figma.com`), Figma Weave (`weavy.ai`), las aplicaciones y las integraciones. Una versión anterior de `scope.txt` incluía `*.figma.com`, `!zendesk.com` y `!statuspage.io`, líneas que no proceden de la política del programa y que se han retirado. El `scope.txt` actual contiene solo los dominios que la tabla lista. Las aplicaciones (escritorio, iOS/Android) y las integraciones (Slack, Teams, Atlassian) no se pueden expresar como dominios y no se tocan en este proyecto.

> **Limitación conocida:** El agente de la Parte 2 se ejecutó el 06/11/2026 con un alcance más amplio que este `scope.txt` (el prompt reproducido en `agente/pruebas.md` autoriza `figma.com`, `*.figma.com` y dos rangos `/24` de Amazon CloudFront). La ejecución no puede repetirse. Se explica en el apartado 3.4 de [`comparativa.md`](./comparativa.md).

---

## 2. Fuera del Alcance (Out-of-Scope)

- **`www.designsystems.com`**: aparece en la tabla oficial como **Fuera de alcance / Inelegible**.
- Cualquier activo que no figure en la tabla de activos (por ejemplo, el dominio raíz `figma.com` o los subdominios descubiertos con `subfinder`, como `staging-admin.figma.com`) **no está listado como dentro del alcance**.
- Según las reglas visibles del programa: la **ingeniería social** (phishing, vishing, smishing) está prohibida, y acceder, modificar, guardar o transferir datos de usuarios queda fuera de lo permitido.

---

## 3. Reglas Específicas que Afectan a Este Proyecto

Lo que sigue se basa en las capturas de la política de Figma de este repositorio (`img/01b` y `img/01c`) y en las normas de este proyecto. Lo que la política no dice se indica como tal.

### 3.1 ¿Permite herramientas automáticas?
- **Según el programa de Figma:** La política indica que el envío masivo de formularios mediante escáneres de vulnerabilidades automatizados no da lugar a recompensa (está fuera del alcance) y pide actuar de buena fe para evitar la degradación del servicio (incluida la denegación de servicio). **No he encontrado en las capturas una lista de herramientas prohibidas.**
- **Según las reglas de este proyecto:** No se permite el uso de escáneres activos ni fuerza bruta (eso pertenece a la UD2). Solo se autoriza la **recolección de información pasiva** (consultas públicas, `subfinder`, `whois`/RDAP, etc.).

### 3.2 ¿Existe límite de peticiones?
- **La política visible no fija un límite numérico de peticiones.** Pide no degradar ni interrumpir el servicio.
- En este proyecto las peticiones directas a los servidores de Figma se limitaron a unas pocas consultas puntuales (`robots.txt`, `security.txt` y las cabeceras de `www.figma.com`).

### 3.3 ¿Prohíbe contactar con empleados?
- **La política prohíbe la ingeniería social** (phishing, vishing, smishing) y las normas del centro prohíben contactar con personas del objetivo.
- No se contactó con ningún empleado ni se crearon cuentas.

### 3.4 ¿Existe algún requisito de identificación?
- **En las capturas de la política no aparece ningún requisito de cabecera de identificación** (como `X-Bug-Bounty`) ni de registro previo para el trabajo pasivo. No se ha comprobado el texto completo de la política más allá de esas capturas.
- Al trabajar en modo pasivo no se crearon cuentas en los servicios de Figma.

### 3.5 Política ante hallazgos sensibles o graves
- Si apareciera un panel expuesto, credenciales o datos personales de terceros: no se explota ni se descarga, se anota de forma anonimizada, se avisa al profesor y, si procede, se informa por el canal de HackerOne.
- En este proyecto no se encontraron credenciales ni datos personales. Los documentos hallados con Google Dorks (informe SOC 3 y certificado ISO 27001) son documentos de cumplimiento que Figma publica en su sitio.

---

## 4. Evidencias Gráficas (Capturas del Programa y Activos)

### 4.1 Resumen y Recompensas del Programa (HackerOne)
<p align="center">
  <img src="img/01a-hackerone-programa.png" alt="Programa de Bug Bounty y Recompensas de Figma" width="650" style="max-width: 100%; height: auto; border-radius: 6px;" />
</p>

### 4.2 Objetivos de Respuesta y Política de Divulgación
<p align="center">
  <img src="img/01b-hackerone-descripcion.png" alt="Descripción General y Política de Divulgación" width="650" style="max-width: 100%; height: auto; border-radius: 6px;" />
</p>

### 4.3 Reglas del Programa y Exclusiones Específicas
<p align="center">
  <img src="img/01c-hackerone-reglas.png" alt="Reglas del Programa y Vulnerabilidades Fuera de Alcance" width="650" style="max-width: 100%; height: auto; border-radius: 6px;" />
</p>

### 4.4 Tabla Detallada de Activos (In-Scope y Out-of-Scope)
<p align="center">
  <img src="img/02-hackerone-assets-scope.png" alt="Tabla Oficial de Activos de Figma en HackerOne" width="650" style="max-width: 100%; height: auto; border-radius: 6px;" />
</p>
<p align="center">
  <em>(Evidencia de la tabla oficial de HackerOne donde se aprecia <code>www.figma.com</code> y <code>api.figma.com</code> en el ámbito, y <code>www.designsystems.com</code> fuera de alcance).</em>
</p>
