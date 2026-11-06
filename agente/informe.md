

## Informe de Reconocimiento Pasivo

### Alcance y Limitaciones
- **google.com**: ❌ **BLOQUEADO** - Fuera del alcance autorizado (solo figma.com, www.figma.com, api.figma.com, *.figma.com, weavy.ai, 3.174.170.0/24, 65.8.202.0/24)
- **figma.com**: ✅ Dentro del alcance - Investigado
- **blog.figma.com**: ✅ Dentro del alcance (*.figma.com) - Investigado

---

### 1. Registro del Dominio (WHOIS)

**figma.com** (`whois_dominio`):
- **Registrador**: Entidad 468
- **Fecha de registro**: 1999-04-10
- **Fecha de expiración**: 2027-04-10
- **Último cambio**: 2026-05-15
- **Estado**: client transfer prohibited
- **Nameservers**: ns-1239.awsdns-26.org, ns-1657.awsdns-15.co.uk, ns-326.awsdns-40.com, ns-912.awsdns-50.net

**blog.figma.com** (`whois_dominio`):
- No es un dominio registrado por separado (error de resolución WHOIS)

---

### 2. Registros DNS

**figma.com**:

| Registro | Valor | Herramienta |
|----------|-------|-------------|
| **A** | 3.174.170.18, 3.174.170.84, 3.174.170.42, 3.174.170.3 | `dns_registros` |
| **AAAA** | Sin registros IPv6 | `dns_registros` |
| **MX** | 1 aspmx.l.google.com, 5 alt1.aspmx.l.google.com, 5 alt2.aspmx.l.google.com, 10 aspmx2.googlemail.com, 10 aspmx3.googlemail.com | `dns_registros` |
| **NS** | ns-326.awsdns-40.com, ns-912.awsdns-50.net, ns-1239.awsdns-26.org, ns-1657.awsdns-15.co.uk | `dns_registros` |
| **SOA** | ns-1657.awsdns-15.co.uk, awsdns-hostmaster.amazon.com, serial 1, refresh 7200, retry 900, expire 1209600, minimum 86400 | `dns_registros` |
| **TXT** | SPF configurado: `v=spf1 a include:_spf.google.com ip4:149.72.216.165 ip4:167.89.79.69 ip4:167.89.87.53 ip4:168.245.25.177 ip4:167.89.97.206 include:mail.zendesk.com include:mg-spf.greenhouse.io -all` | `dns_registros` |
| **TXT** | Múltiples verificaciones de dominio (Google, OpenAI, Stripe, Twilio, Atlassian, Adobe, etc.) | `dns_registros` |

**blog.figma.com**:

| Registro | Valor | Herramienta |
|----------|-------|-------------|
| **A** | 3.174.170.25, 3.174.170.54, 3.174.170.109, 3.174.170.126 | `dns_registros` |
| **AAAA** | Sin registros IPv6 | `dns_registros` |
| **CNAME** | Sin registros CNAME | `dns_registros` |

---

### 3. Subdominios

- **crt.sh**: ❌ Error temporal (HTTP 502 Bad Gateway)
- **Subfinder**: ❌ Error (tiempo de espera excedido >35s)

---

### 4. Infraestructura y Tecnologías

**Análisis de IPs (Shodan)**:

| IP | Puertos | Tecnología | Hostname | Herramienta |
|----|---------|------------|----------|-------------|
| 3.174.170.18 | 80, 443 | Amazon CloudFront | server-3-174-170-18.mad56.r.cloudfront.net | `shodan_host` |
| 3.174.170.84 | 80, 443 | Amazon CloudFront | server-3-174-170-84.mad56.r.cloudfront.net | `shodan_host` |
| 3.174.170.25 | 80 | Amazon CloudFront | server-3-174-170-25.mad56.r.cloudfront.net | `shodan_host` |
| 3.174.170.54 | 80, 443 | Amazon CloudFront | server-3-174-170-54.mad56.r.cloudfront.net, jobs2live.com | `shodan_host` |

**Reputación IP/ASN**:

| IP | ASN | Proveedor | Ubicación | Tipo | Herramienta |
|----|-----|-----------|-----------|------|-------------|
| 3.174.170.18 | AS16509 | Amazon.com, Inc. (AWS CloudFront GLOBAL) | Madrid, España | Datacenter/Cloud | `reputacion_ip_asn` |
| 3.174.170.25 | AS16509 | Amazon.com, Inc. (AWS CloudFront GLOBAL) | Madrid, España | Datacenter/Cloud | `reputacion_ip_asn` |

**Tecnologías Web**:

| Dominio | HTTP | Cabeceras Clave | Herramienta |
|---------|------|-----------------|-------------|
| figma.com | HTTP/2 301 | via: CloudFront, HSTS: max-age=31536000; includeSubDomains; preload | `tecnologias_web` |
| blog.figma.com | HTTP/2 301 | via: CloudFront, HSTS: max-age=31536000; includeSubDomains; preload | `tecnologias_web` |

---

### 5. Postura de Seguridad

**Correo (figma.com)** (`correo_postura`):
- **SPF**: ✅ Configurado - `v=spf1 a include:_spf.google.com ip4:149.72.216.165 ip4:167.89.79.69 ip4:167.89.87.53 ip4:168.245.25.177 ip4:167.89.97.206 include:mail.zendesk.com include:mg-spf.greenhouse.io -all`
- **DMARC**: ✅ Configurado - `v=DMARC1; p=quarantine`
- **MX**: 5 servidores Google Workspace configurados

**Ficheros Sensibles**:

| Dominio | robots.txt | security.txt | Herramienta |
|---------|------------|--------------|-------------|
| figma.com | ✅ 9016 directivas (múltiples Disallow) | ✅ 5 entradas: Contact: hackerone.com/figma, Policy: hackerone.com/figma, Expires: 2027-10-21 | `ficheros_sensibles` |
| blog.figma.com | ✅ Vacío/sin directivas relevantes | ✅ 14 entradas (HTML renderizado con assets de Netlify/Next.js) | `ficheros_sensibles` |

**Vulnerabilidades conocidas**: Ninguna CVE pública directa detectada en las IPs consultadas (`shodan_host`).

---

### 6. Exposición de Correos

- **figma.com**: No se detectaron correos expuestos públicamente de forma inmediata (`fuga_correos`).

---

### 7. Endpoints Históricos (Wayback Machine)

- **figma.com**: ❌ Error temporal (timeout)
- **blog.figma.com**: ✅ 20 rutas descubiertas, principalmente imágenes y assets estáticos (`wayback_endpoints`)

---

### Resumen Ejecutivo

1. **figma.com** es un dominio maduro (registrado en 1999) que utiliza infraestructura AWS (CloudFront + Route 53) con servidores en Madrid.
2. La postura de correo es sólida: SPF, DMARC (cuarentena) y MX con Google Workspace están configurados.
3. **blog.figma.com** comparte la misma infraestructura CloudFront y usa Netlify/Next.js según sus assets estáticos.
4. No hay vulnerabilidades CVE públicas en las IPs consultadas.
5. **google.com** no pudo ser investigado al estar fuera del alcance autorizado.