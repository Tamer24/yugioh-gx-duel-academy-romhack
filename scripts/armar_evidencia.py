"""Arma la galeria de la revision por capturas (evidencia/index.html).

Recorre evidencia/rondaN/NN-carta/resultado.md (formato de evidencia/COMO-REVISAR.md) y arma
una pagina con una tarjeta por carta: cada ronda con su resultado, lo esperado, lo visto y las
capturas clave. El sello de la tarjeta es el resultado de la ultima ronda. Tambien imprime el
resumen. No modifica las sesiones.

Uso (desde la raiz del proyecto):
  python3 scripts/armar_evidencia.py evidencia
"""
import html
import os
import re
import sys

CAMPOS = ("carta", "resultado", "esperado", "visto", "antes", "despues", "capturas clave",
          "diferencias con la guía", "pasos usados", "verificado")
COLORES = {"COINCIDE": "ok", "NO COINCIDE": "mal", "NO LLEGUE": "duda"}
MAX_CAPTURAS = 8

ESTILO = """
:root{--fondo:#f6f5f1;--tarjeta:#fff;--texto:#1d1d1b;--suave:#66645e;--borde:#dcd9d0;
--ok:#1f7a4d;--mal:#b3261e;--duda:#8a6100}
@media (prefers-color-scheme:dark){:root{--fondo:#17171a;--tarjeta:#212125;--texto:#ecebe6;
--suave:#a3a199;--borde:#34343a;--ok:#6fd3a0;--mal:#ff8a80;--duda:#f0c05a}}
*{box-sizing:border-box}body{margin:0;padding:24px 16px 64px;background:var(--fondo);color:var(--texto);
font:15px/1.5 system-ui,sans-serif}main{max-width:1040px;margin:0 auto}
h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:0}p{margin:6px 0}
h3{font-size:13px;margin:14px 0 0;color:var(--suave);font-weight:600}section+section{border-top:1px solid var(--borde);margin-top:14px}
.resumen{color:var(--suave);margin-bottom:20px}
article{background:var(--tarjeta);border:1px solid var(--borde);border-radius:10px;padding:16px;margin:14px 0}
header{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.sello{font-size:12px;font-weight:700;letter-spacing:.04em;padding:2px 8px;border-radius:999px;border:1px solid}
.ok{color:var(--ok)}.mal{color:var(--mal)}.duda{color:var(--duda)}
dt{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--suave);margin-top:10px}dd{margin:2px 0 0}
.capturas{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px;margin-top:12px}
figure{margin:0}img{width:100%;height:auto;image-rendering:pixelated;border-radius:6px;display:block}
figcaption{font-size:12px;color:var(--suave);margin-top:3px}
nav{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0 4px}nav a{font-size:13px;text-decoration:none;
border:1px solid var(--borde);border-radius:999px;padding:2px 10px;background:var(--tarjeta)}
"""


def leer_resultado(ruta):
    """{campo: texto}. Un campo sigue hasta que empieza el siguiente."""
    datos, actual = {}, None
    for linea in open(ruta, encoding="utf-8").read().splitlines():
        m = re.match(r"\s*\**([a-záéíóúñ ]+?)\**\s*:\s*(.*)", linea, re.I)
        clave = m.group(1).strip().lower() if m else None
        if clave in CAMPOS:
            actual = clave
            datos[actual] = m.group(2).strip()
        elif actual and linea.strip() and not linea.startswith("```"):
            datos[actual] += "\n" + linea.strip()
    return datos


def capturas(datos, carpeta):
    """Archivos de captura nombrados en el resultado que existen, en el orden en que aparecen."""
    texto = "\n".join(datos.get(c, "") for c in ("antes", "despues", "capturas clave"))
    vistas = []
    for nombre in re.findall(r"\b(\d{3}(?:-[a-z])?\.png)", texto):
        if nombre not in vistas and os.path.exists(os.path.join(carpeta, nombre)):
            vistas.append(nombre)
    return vistas[:MAX_CAPTURAS]


def parrafos(texto):
    return "<br>".join(html.escape(t) for t in texto.split("\n"))


def main(argv):
    if len(argv) != 1 or not os.path.isdir(argv[0]):
        raise SystemExit(__doc__)
    raiz = argv[0]
    rondas = sorted(d for d in os.listdir(raiz) if re.fullmatch(r"ronda\d+", d))
    cartas = {}                                    # "NN-carta" -> [(ronda, datos, carpeta relativa)]
    for r in rondas:
        for s in sorted(os.listdir(os.path.join(raiz, r))):
            ruta = os.path.join(raiz, r, s, "resultado.md")
            if re.match(r"\d\d-", s) and os.path.exists(ruta):
                cartas.setdefault(s, []).append((r, leer_resultado(ruta), f"{r}/{s}"))
    tarjetas, cuenta, enlaces = [], {}, []
    for s in sorted(cartas):
        bloques, final, titulo = [], "SIN RESULTADO", s
        for r, datos, rel in cartas[s]:
            texto = datos.get("resultado", "").split("\n")[0].strip().upper()
            final = next((k for k in COLORES if texto.startswith(k)), "SIN RESULTADO")
            titulo = datos.get("carta", s).split("\n")[0]
            clase = COLORES.get(final, "duda")
            figuras = "".join(f'<figure><a href="{rel}/{c}"><img src="{rel}/{c}" alt="{s} {c}" loading="lazy"></a>'
                              f"<figcaption>{c}</figcaption></figure>" for c in capturas(datos, os.path.join(raiz, rel)))
            campos = "".join(f"<dt>{html.escape(c)}</dt><dd>{parrafos(datos[c])}</dd>"
                             for c in ("esperado", "visto", "diferencias con la guía", "verificado") if datos.get(c))
            bloques.append(f'<section><h3>{r.replace("ronda", "Ronda ")} <span class="sello {clase}">{final}</span></h3>'
                           f'<dl>{campos}</dl><div class="capturas">{figuras}</div></section>')
        cuenta[final] = cuenta.get(final, 0) + 1
        clase = COLORES.get(final, "duda")
        print(f"{s:34} {final:14} ({len(cartas[s])} ronda{'s' if len(cartas[s]) > 1 else ''})")
        enlaces.append(f'<a class="{clase}" href="#{s}">{s[:2]}</a>')
        tarjetas.append(f'<article id="{s}"><header><h2>{html.escape(titulo)}</h2>'
                        f'<span class="sello {clase}">{final}</span></header>{"".join(bloques)}</article>')
    resumen = " · ".join(f"{n} {k.lower()}" for k, n in sorted(cuenta.items()))
    pagina = (f'<!doctype html><html lang="es"><meta charset="utf-8">'
              f'<meta name="viewport" content="width=device-width,initial-scale=1">'
              f"<title>Revisión por capturas</title><style>{ESTILO}</style><main>"
              f"<h1>Revisión por capturas</h1>"
              f'<p class="resumen">{len(cartas)} filas de la guía · {resumen} (resultado de la última ronda de cada una). '
              f"COINCIDE = se vio lo que dice la guía; NO COINCIDE = la carta no hace lo que debería. "
              f"Cada captura abre en tamaño real.</p>"
              f"<nav>{''.join(enlaces)}</nav>{''.join(tarjetas)}</main></html>")
    salida = os.path.join(raiz, "index.html")
    with open(salida, "w", encoding="utf-8") as f:
        f.write(pagina)
    print(f"\n{resumen}\ngaleria: {salida}")


if __name__ == "__main__":
    main(sys.argv[1:])
