"""Herramientas iniciales de reconocimiento. AQUÍ PUEDES AÑADIR LAS TUYAS.

WHOIS (whois.py), DNS y crt.sh ya están implementadas y activas en lanzar.py.
DNS y crt.sh proceden de la solución del profesor (herramientas/recon.py).

Para ampliar: una tarea por función, @protegida, sin shell, con timeout,
salida recortada, errores como texto y resultados filtrados por el alcance.
Importa tu nueva función en lanzar.py y añádela a HERRAMIENTAS.

Ideas: subdominios_subfinder, wayback_urls, correos (theHarvester / hunter.io),
infraestructura_ip, correo_postura (SPF/DMARC/MTA-STS/CAA), urlscan, shodan_host.
"""

import json
import subprocess
import urllib.parse
import urllib.request

from guard import protegida, filtrar
from whois import recortar

UA = "aap-recon/1.0 (educativo; IES Rafael Alberti)"
TIPOS_DNS = {"A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"}


def _http(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


@protegida(objetivo="dominio")
def dns_registros(dominio: str, tipo: str = "A") -> str:
    """Consulta registros DNS de un dominio. tipo: A, AAAA, MX, NS, TXT, CNAME o SOA.
    Devuelve los valores, uno por línea."""
    tipo = tipo.upper()
    if tipo not in TIPOS_DNS:
        return f"ERROR: tipo DNS no válido ({tipo}). Usa uno de: {', '.join(sorted(TIPOS_DNS))}."
    try:
        r = subprocess.run(["dig", "+short", tipo, dominio],
                           capture_output=True, text=True, timeout=20)
    except subprocess.TimeoutExpired:
        return "ERROR: dig no respondió en 20 segundos."
    except OSError as e:
        return recortar(f"ERROR: no se pudo ejecutar dig: {e}")
    if r.returncode != 0:
        return recortar(f"ERROR: dig falló ({r.returncode}): {r.stderr.strip() or 'sin detalles'}")
    salida = recortar(r.stdout.strip())
    return salida or f"Sin registros {tipo} para {dominio}."


@protegida(objetivo="dominio")
def subdominios_crtsh(dominio: str) -> str:
    """Enumera subdominios de un dominio por transparencia de certificados (crt.sh).
    Pasivo: no toca el objetivo. Devuelve solo los subdominios dentro del alcance."""
    url = f"https://crt.sh/?q=%25.{urllib.parse.quote(dominio)}&output=json"
    try:
        datos = json.loads(_http(url, timeout=90))
    except Exception as e:
        return (f"ERROR: crt.sh no respondió ({e}). crt.sh suele ir lento; "
                "puedes reintentar más tarde o añadir otra fuente de subdominios.")
    if not isinstance(datos, list) or any(
        not isinstance(fila, dict) or not isinstance(fila.get("name_value"), str)
        for fila in datos
    ):
        return "ERROR: crt.sh devolvió un formato de certificados inesperado."
    nombres = set()
    for fila in datos:
        for n in str(fila.get("name_value", "")).splitlines():
            n = n.strip().lstrip("*.").lower()
            if n:
                nombres.add(n)
    dentro, fuera = filtrar(sorted(nombres))
    cab = f"{len(dentro)} subdominios en alcance ({fuera} filtrados por estar fuera):\n"
    return recortar(cab + "\n".join(dentro))


@protegida(objetivo="ip")
def shodan_host(ip: str) -> str:
    """Consulta la API de Shodan InternetDB para una dirección IP.
    Devuelve puertos abiertos, CPEs de tecnologías, vulnerabilidades (CVEs) y hostnames.
    Totalmente pasivo y no interactúa con la víctima."""
    url = f"https://internetdb.shodan.io/{urllib.parse.quote(ip)}"
    try:
        resp = _http(url, timeout=15)
        datos = json.loads(resp)
    except Exception as e:
        return f"Sin datos públicos en Shodan InternetDB para {ip} (o timeout: {e})."

    puertos = datos.get("ports", [])
    cves = datos.get("vulns", [])
    cpes = datos.get("cpes", [])
    hostnames = datos.get("hostnames", [])

    lineas = [
        f"Resultados Shodan InternetDB para {ip}:",
        f"- Puertos abiertos: {', '.join(map(str, puertos)) if puertos else 'Ninguno detectado'}",
        f"- Tecnologías (CPE): {', '.join(cpes[:5]) if cpes else 'No identificadas'}",
        f"- Vulnerabilidades conocidas: {', '.join(cves[:5]) if cves else 'Ninguna CVE pública directa'}",
        f"- Hostnames asociados: {', '.join(hostnames[:3]) if hostnames else 'Ninguno'}"
    ]
    return recortar("\n".join(lineas))

@protegida(objetivo="dominio")
def ficheros_sensibles(dominio: str) -> str:
    """Inspecciona ficheros publicos clave: /robots.txt y /.well-known/security.txt.
    Permite descubrir rutas ocultas/disallow y politicas de divulgacion de vulnerabilidades.
    Tecnica puramente pasiva y estandar."""
    resultados = [f"Inspeccion de ficheros publicos en {dominio}:"]

    # 1. Analisis de robots.txt
    url_robots = f"https://{dominio}/robots.txt"
    try:
        cuerpo_robots = _http(url_robots, timeout=10)
        lineas_interes = []
        for linea in cuerpo_robots.splitlines():
            linea_l = linea.strip()
            if linea_l.lower().startswith(("disallow:", "sitemap:", "allow:")):
                lineas_interes.append(linea_l)

        if lineas_interes:
            # Tomamos hasta 10 rutas relevantes para ahorrar tokens
            muestra = lineas_interes[:10]
            aviso = f" (y {len(lineas_interes)-10} mas omitidas)" if len(lineas_interes) > 10 else ""
            resultados.append(f"-> /robots.txt encontrado ({len(lineas_interes)} directivas):\n   " + "\n   ".join(muestra) + aviso)
        else:
            resultados.append("-> /robots.txt existe pero esta vacio o sin directivas relevantes.")
    except Exception as e:
        resultados.append(f"-> /robots.txt no accesible o no encontrado ({e}).")

    # 2. Analisis de security.txt
    url_sec = f"https://{dominio}/.well-known/security.txt"
    try:
        cuerpo_sec = _http(url_sec, timeout=10)
        campos_sec = [l.strip() for l in cuerpo_sec.splitlines() if l.strip() and not l.strip().startswith("#")]
        if campos_sec:
            resultados.append(f"-> /security.txt encontrado ({len(campos_sec)} entradas):\n   " + "\n   ".join(campos_sec[:5]))
        else:
            resultados.append("-> /security.txt no contiene directivas legibles.")
    except Exception:
        resultados.append("-> /.well-known/security.txt no implementado.")

    return recortar("\n".join(resultados))

@protegida(objetivo="dominio")
def subdominios_subfinder(dominio: str) -> str:
    """Enumera subdominios pasivos usando la herramienta Subfinder instalada en el sistema.
    Filtra los resultados contra el scope autorizado y limita la salida para ahorrar tokens."""
    try:
        r = subprocess.run(
            ["/usr/local/bin/subfinder", "-d", dominio, "-silent"],
            capture_output=True,
            text=True,
            timeout=35
        )
    except subprocess.TimeoutExpired:
        return "ERROR: subfinder tardo mas de 35 segundos."
    except Exception as e:
        return f"ERROR ejecutando subfinder: {e}"

    lineas = [l.strip() for l in r.stdout.splitlines() if l.strip()]
    if not lineas:
        return f"No se descubrieron subdominios con subfinder para {dominio}."

    dentro, fuera = filtrar(sorted(set(lineas)))
    cab = f"{len(dentro)} subdominios descubiertos con Subfinder ({fuera} descartados fuera de scope):\n"
    muestra = dentro[:25]
    aviso = f"\n... (y {len(dentro) - 25} mas en scope)" if len(dentro) > 25 else ""
    return recortar(cab + "\n".join(muestra) + aviso)


@protegida(objetivo="dominio")
def correo_postura(dominio: str) -> str:
    """Evalua la postura de seguridad del correo para el dominio.
    Comprueba registros SPF (TXT), DMARC (_dmarc) y servidores MX usando dig.
    Permite detectar riesgos de suplantacion (spoofing) o falta de politicas."""
    lineas = [f"Postura de seguridad de correo para {dominio}:"]

    # 1. Registro SPF en TXT
    try:
        r_spf = subprocess.run(["dig", "+short", "TXT", dominio], capture_output=True, text=True, timeout=10)
        spf = [l.strip(' "') for l in r_spf.stdout.splitlines() if "v=spf1" in l]
        if spf:
            lineas.append(f"- SPF: Configurado -> {spf[0][:120]}")
        else:
            lineas.append("- SPF: ALERTA -> No se encontro registro SPF v=spf1.")
    except Exception as e:
        lineas.append(f"- SPF: Error consultando ({e})")

    # 2. Registro DMARC
    try:
        r_dmarc = subprocess.run(["dig", "+short", "TXT", f"_dmarc.{dominio}"], capture_output=True, text=True, timeout=10)
        dmarc = [l.strip(' "') for l in r_dmarc.stdout.splitlines() if "v=DMARC1" in l]
        if dmarc:
            lineas.append(f"- DMARC: Configurado -> {dmarc[0][:120]}")
        else:
            lineas.append("- DMARC: ALERTA -> No tiene politica DMARC (_dmarc).")
    except Exception as e:
        lineas.append(f"- DMARC: Error consultando ({e})")

    # 3. Servidores MX
    try:
        r_mx = subprocess.run(["dig", "+short", "MX", dominio], capture_output=True, text=True, timeout=10)
        mx_list = [l.strip() for l in r_mx.stdout.splitlines() if l.strip()]
        if mx_list:
            lineas.append(f"- Servidores MX: {', '.join(mx_list[:4])}")
        else:
            lineas.append("- Servidores MX: Ninguno configurado.")
    except Exception as e:
        lineas.append(f"- MX: Error consultando ({e})")

    return recortar("\n".join(lineas))


@protegida(objetivo="dominio")
def tecnologias_web(dominio: str) -> str:
    """Inspecciona las cabeceras HTTP publicas (Server, CloudFront, HSTS, Cookies)
    para identificar la infraestructura y tecnologias web del activo."""
    try:
        r = subprocess.run(
            ["curl", "-s", "-I", "-m", "10", f"https://{dominio}"],
            capture_output=True,
            text=True,
            timeout=12
        )
        lineas = [l.strip() for l in r.stdout.splitlines() if l.strip()]
        if not lineas:
            return f"No se obtuvieron cabeceras HTTP de https://{dominio}."

        # Filtramos cabeceras tecnicas relevantes
        interes = []
        for l in lineas:
            if any(l.lower().startswith(p) for p in ("http/", "server:", "via:", "x-served-by:", "strict-transport-security:", "content-type:")):
                interes.append(l)

        resultado = f"Cabeceras y tecnologias en https://{dominio}:\n" + "\n".join(interes if interes else lineas[:6])
        return recortar(resultado)
    except subprocess.TimeoutExpired:
        return f"ERROR: timeout conectando a https://{dominio}."
    except Exception as e:
        return f"ERROR analizando tecnologias de {dominio}: {e}"


@protegida(objetivo="ip")
def reputacion_ip_asn(ip: str) -> str:
    """Consulta informacion de enrutamiento BGP, ASN, proveedor de hosting (ISP) y
    geolocalizacion de una IP de forma 100% pasiva via API publica."""
    url = f"http://ip-api.com/json/{urllib.parse.quote(ip)}?fields=status,message,country,regionName,city,isp,org,as,hosting"
    try:
        resp = _http(url, timeout=10)
        d = json.loads(resp)
        if d.get("status") != "success":
            return f"No se pudo resolver ASN/Geolocalizacion para {ip}: {d.get('message', 'desconocido')}"

        info = [
            f"Infraestructura de red para la IP {ip}:",
            f"- ASN / BGP: {d.get('as', 'N/D')}",
            f"- Proveedor (ISP): {d.get('isp', 'N/D')} ({d.get('org', 'N/D')})",
            f"- Ubicacion fisica: {d.get('city', 'N/D')}, {d.get('regionName', 'N/D')} ({d.get('country', 'N/D')})",
            f"- Tipo Datacenter/Hosting: {'Si (Infraestructura Cloud)' if d.get('hosting') else 'No'}"
        ]
        return recortar("\n".join(info))
    except Exception as e:
        return f"ERROR consultando reputacion de IP {ip}: {e}"

@protegida(objetivo="dominio")
def wayback_endpoints(dominio: str) -> str:
    """Busca endpoints y rutas historicas archivadas en Wayback Machine (archive.org).
    Tecnica pasiva clasica de Bug Bounty para descubrir rutas y parametros olvidados."""
    url = f"https://web.archive.org/cdx/search/cdx?url=*.{urllib.parse.quote(dominio)}/*&output=json&fl=original&collapse=urlkey&limit=30"
    try:
        resp = _http(url, timeout=15)
        datos = json.loads(resp)
        if not datos or len(datos) <= 1:
            return f"Sin registros historicos archivados para {dominio}."

        # Omitimos la cabecera ["original"]
        urls = [fila[0] for fila in datos[1:] if fila]
        urls_unicas = sorted(set(urls))[:20]

        resultado = [f"Rutas historicas descubiertas en Wayback Machine para {dominio} ({len(urls_unicas)} muestras):"]
        for u in urls_unicas:
            resultado.append(f"  * {u}")
        return recortar("\n".join(resultado))
    except Exception as e:
        return f"ERROR consultando Wayback Machine para {dominio}: {e}"

@protegida(objetivo="dominio")
def fuga_correos(dominio: str) -> str:
    """Recolecta de forma pasiva direcciones de correo y empleados expuestos usando theHarvester.
    Permite evaluar el vector de exposicion a ataques de ingenieria social y phishing."""
    try:
        r = subprocess.run(
            ["/usr/bin/theHarvester", "-d", dominio, "-b", "duckduckgo,bing", "-l", "50"],
            capture_output=True,
            text=True,
            timeout=35
        )
        lineas = r.stdout.splitlines()
        correos = []
        guardando = False
        for l in lineas:
            limpia = l.strip()
            if "Emails found:" in limpia:
                guardando = True
                continue
            if guardando:
                if limpia.startswith("[*]") or limpia.startswith("[-]"):
                    break
                if "@" in limpia and dominio in limpia:
                    correos.append(limpia)

        if correos:
            correos_unicos = sorted(set(correos))[:15]
            return recortar(f"Correos publicamente expuestos asociados a {dominio}:\n" + "\n".join(f"  - {c}" for c in correos_unicos))
        return f"No se detectaron correos expuestos publicamente de forma inmediata para {dominio}."
    except subprocess.TimeoutExpired:
        return "ERROR: theHarvester excedio el tiempo maximo de 35s."
    except Exception as e:
        return f"ERROR ejecutando theHarvester: {e}"
