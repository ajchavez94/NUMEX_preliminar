"""
Tablas resumen (media ± SD por especie y tratamiento) en el formato de Summary_template.docx.

Uso:
    pip install python-docx pandas openpyxl
    python tablas_summary.py

Pon este script, Summary_template.docx y los Excel en la misma carpeta (o cambia las rutas
de la sección OPCIONES). Para otra tabla, añade una entrada a TABLAS.

Cómo funciona: abre el template y usa su tabla como MOLDE. Copia la fila de encabezado y las
filas de cada tipo (Control con borde superior, N rosa, P azul, N+P gris con borde inferior),
y solo cambia el texto y el color de las columnas de elevación/especie. Así se conservan las
fuentes, tamaños, bordes y colores del template sin redefinirlos a mano. Si la tabla tiene más
columnas que el template, se añaden copiando la última columna y se reparten los anchos.
"""
import copy
import difflib
import math
import re

import pandas as pd
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

# ============================================================================
# OPCIONES
# ============================================================================
TEMPLATE = "Summary_template.docx"
SALIDA = "Summary_tables_NUMEX.docx"

# Especies en el orden de la tabla: (nombre en la tabla, nombre en el Excel, elevación)
ESPECIES = [
    ("P. torta",        "Pouteria torta",         1000),
    ("C. racemosa",     "Clarisia racemosa",      1000),
    ("A. lojaensis",    "Alchornea lojaensis",    2000),
    ("Myrcia sp. nov.", "Myrcia sp nov",          2000),
    ("H. purpurascens", "Hedyosmum purpurascens", 3000),
    ("W. loxensis",     "Weinmannia loxensis",    3000),
]

# Tratamientos: código en la columna "Sub" del Excel -> texto en la tabla (en este orden)
TRATAMIENTOS = [("C", "Control"), ("N", "N"), ("P", "P"), ("NP", "N+P")]

# Color de las columnas de elevación y especie (los del template). Cambia aquí si quieres
# otra paleta, p. ej. {1000: "FFF2A8", 2000: "C7E6A3", 3000: "7FBF7B"}.
COLOR_ELEV = {1000: "FFF2CC", 2000: "DAE0D5", 3000: "97B895"}

# Celdas con pocos árboles: superíndice en el tratamiento + nota al pie.
# (Las celdas con n = 1 no tienen SD en el Excel y se escriben sin "±" automáticamente.)
LLAMADAS = {("C. racemosa", "N"): "a", ("W. loxensis", "N+P"): "b"}
NOTAS_LLAMADAS = {"a": "n = 1 (no SD).", "b": "n = 2."}

# Cada tabla: Excel de entrada, título, y columnas como
#   (patrón del nombre de la columna en el Excel, encabezado en la tabla, decimales)
# El encabezado None conserva el del template (con sus superíndices); solo sirve si la tabla
# tiene las mismas columnas que el template y en el mismo orden.
TABLAS = [
    dict(
        excel="Summary_main.xlsx",
        titulo="Table 2. Leaf traits by species and treatment (mean ± SD)",
        columnas=[
            (r"^δ13C",                 None, 2),
            (r"^iWUE",                 None, 1),
            (r"^LNC$",                 None, 2),
            (r"^LPC$",                 None, 2),
            (r"^N:P$",                 None, 1),
            (r"^Specific leaf area",   None, 1),
        ],
    ),
    dict(
        excel="Summary_supp.xlsx",
        titulo="Table S3. Additional leaf traits by species and treatment (mean ± SD)",
        apaisada=True,   # 8 columnas de datos: en horizontal caben sin partir cada celda
        columnas=[
            (r"^LCC$",                 "LCC (mg g⁻¹)",            1),
            (r"^C:N$",                 "C:N",                     1),
            (r"^N_area$",              "Nₐᵣₑₐ (g m⁻²)",           2),
            (r"^P_area$",              "Pₐᵣₑₐ (g m⁻²)",           2),  # el Excel ya viene con 2 decimales
            (r"^thickness",            "Thickness (mm)",          2),
            (r"^force to punch",       "Punch force (kN m⁻¹)",    2),
            (r"^Leaf area",            "Leaf area (cm²)",         1),
            (r"^dry matter content",   "LDMC (mg g⁻¹)",           1),
        ],
    ),
]

# Ancho útil de la página en twips (1 cm = 567): A4 con márgenes de 2.54 cm
ANCHO_UTIL = {False: 9026, True: 13958}   # vertical / apaisada
ANCHO_ID = [860, 1394, 923]  # columnas Elevation, Species, Treatment (como el template)

# ============================================================================
# LECTURA DEL EXCEL
# ============================================================================
def leer_excel(ruta):
    """Excel con 2 filas de encabezado (variable / mean-std) y una fila de nombres
    (elevation_m, name, Sub). Devuelve {(especie_excel, Sub): {variable: (media, sd)}}
    y la lista de variables en orden."""
    raw = pd.read_excel(ruta, header=None)
    variables = raw.iloc[0].ffill()
    stats = raw.iloc[1]
    datos = raw.iloc[3:].copy()
    datos[0] = datos[0].ffill()
    datos[1] = datos[1].ffill()
    out, orden = {}, []
    for _, fila in datos.iterrows():
        clave = (str(fila[1]).strip(), str(fila[2]).strip())
        d = {}
        for j in range(3, raw.shape[1]):
            v = str(variables[j]).strip()
            if v not in orden:
                orden.append(v)
            d.setdefault(v, [None, None])
            x = fila[j]
            x = None if (x is None or (isinstance(x, float) and math.isnan(x))) else float(x)
            d[v][0 if str(stats[j]).strip() == "mean" else 1] = x
        out[clave] = d
    return out, orden


def buscar_columna(patron, variables):
    hit = [v for v in variables if re.search(patron, v)]
    if len(hit) != 1:
        raise ValueError(f"El patrón {patron!r} encontró {len(hit)} columnas: {hit}")
    return hit[0]

# ============================================================================
# EDICIÓN DEL XML DEL TEMPLATE
# ============================================================================
def celdas(tr):
    return tr.findall(qn("w:tc"))


def poner_texto(tc, texto, superindice=None):
    """Cambia el texto de una celda conservando el formato de su primer run."""
    p = tc.find(qn("w:p"))
    for extra in tc.findall(qn("w:p"))[1:]:
        tc.remove(extra)
    runs = p.findall(qn("w:r"))
    if not runs:
        r = OxmlElement("w:r"); p.append(r); runs = [r]
    molde = runs[0]
    for r in runs[1:]:
        p.remove(r)
    for el in p.findall(qn("w:proofErr")):
        p.remove(el)
    for t in molde.findall(qn("w:t")):
        molde.remove(t)
    t = OxmlElement("w:t"); t.text = texto; t.set(qn("xml:space"), "preserve")
    molde.append(t)
    if superindice:
        r2 = copy.deepcopy(molde)
        r2.find(qn("w:t")).text = superindice
        rpr = r2.find(qn("w:rPr"))
        if rpr is None:
            rpr = OxmlElement("w:rPr"); r2.insert(0, rpr)
        va = OxmlElement("w:vertAlign"); va.set(qn("w:val"), "superscript")
        rpr.append(va)
        molde.addnext(r2)


def poner_color(tc, fill):
    shd = tc.find(qn("w:tcPr")).find(qn("w:shd"))
    shd.set(qn("w:fill"), fill)


def poner_ancho(tc, w):
    tc.find(qn("w:tcPr")).find(qn("w:tcW")).set(qn("w:w"), str(w))


def ajustar_columnas(tr, n_total, anchos):
    """Añade (copiando la última) o quita celdas para tener n_total columnas."""
    tcs = celdas(tr)
    while len(tcs) < n_total:
        tcs[-1].addnext(copy.deepcopy(tcs[-1])); tcs = celdas(tr)
    while len(tcs) > n_total:
        tr.remove(tcs[-1]); tcs = celdas(tr)
    for tc, w in zip(tcs, anchos):
        poner_ancho(tc, w)


def repetir_encabezado(tr):
    trPr = tr.find(qn("w:trPr"))
    if trPr is None:
        trPr = OxmlElement("w:trPr"); tr.insert(0, trPr)
    h = OxmlElement("w:tblHeader"); h.set(qn("w:val"), "true"); trPr.append(h)


def formato(media, sd, dec):
    if media is None:
        return "—"
    txt = f"{media:.{dec}f}"
    return txt if sd is None else f"{txt} ± {sd:.{dec}f}"

# ============================================================================
# CONSTRUCCIÓN
# ============================================================================
doc = Document(TEMPLATE)
molde = doc.tables[0]._tbl
filas_molde = molde.findall(qn("w:tr"))
FILA_ENC = filas_molde[0]
# Moldes por tratamiento (el bloque de la primera especie del template: filas 1-4)
FILA_TRAT = {texto: filas_molde[1 + i] for i, (_, texto) in enumerate(TRATAMIENTOS)}

body = doc.element.body
sectPr = body.find(qn("w:sectPr"))
for el in list(body):
    if el is not sectPr:
        body.remove(el)


def parrafo(texto, negrita=False, tam=9, antes=0, despues=0, salto=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before, pf.space_after = Pt(antes), Pt(despues)
    pf.page_break_before = salto
    pf.keep_with_next = negrita
    r = p.add_run(texto); r.bold = negrita; r.font.name = "Calibri"; r.font.size = Pt(tam)
    body.remove(p._p); sectPr.addprevious(p._p)
    return p


for k, conf in enumerate(TABLAS):
    datos, variables = leer_excel(conf["excel"])
    cols = [(buscar_columna(pat, variables), enc, dec) for pat, enc, dec in conf["columnas"]]

    # Los nombres de especie del Excel pueden traer erratas antiguas ("Hedyosmun",
    # "Weinmania"): se emparejan con el nombre más parecido y se imprime el resultado.
    nombres_excel = sorted({e for e, _ in datos})
    alias = {}
    for _, nombre_cfg, _ in ESPECIES:
        m = difflib.get_close_matches(nombre_cfg, nombres_excel, n=1, cutoff=0.85)
        if not m:
            raise KeyError(f"{nombre_cfg!r} no se parece a ningún nombre del Excel: {nombres_excel}")
        alias[nombre_cfg] = m[0]
        if m[0] != nombre_cfg:
            print(f"   aviso: {nombre_cfg!r} se emparejó con {m[0]!r} del Excel")
    print(f"\n{conf['excel']}: columnas usadas")
    for v, _, _ in cols:
        if v.startswith("iWUE") and "Bernacchi" not in v:
            print(f"   ¡ATENCIÓN! {v!r} es el iWUE antiguo, no iWUE_Bernacchi (el del manuscrito).")
        if v.startswith("Leaf area"):
            print(f"   ¡ATENCIÓN! {v!r} es el área TOTAL de la muestra; el área de una hoja es la columna LA.")
    for v, enc, _ in cols:
        print(f"   {v!r:40} -> {enc or '(encabezado del template)'}")

    n_total = 3 + len(cols)
    apaisada = conf.get("apaisada", False)
    resto = ANCHO_UTIL[apaisada] - sum(ANCHO_ID)
    anchos = ANCHO_ID + [resto // len(cols)] * len(cols)

    tbl = copy.deepcopy(molde)
    for tr in tbl.findall(qn("w:tr")):
        tbl.remove(tr)
    grid = tbl.find(qn("w:tblGrid"))
    for gc in list(grid):
        grid.remove(gc)
    for w in anchos:
        gc = OxmlElement("w:gridCol"); gc.set(qn("w:w"), str(w)); grid.append(gc)

    # Encabezado
    enc = copy.deepcopy(FILA_ENC)
    mismo_que_template = n_total == len(celdas(FILA_ENC)) and all(e is None for _, e, _ in cols)
    ajustar_columnas(enc, n_total, anchos)
    if not mismo_que_template:
        for tc, (_, texto, _) in zip(celdas(enc)[3:], cols):
            if texto is not None:
                poner_texto(tc, texto)
    repetir_encabezado(enc)
    tbl.append(enc)

    # Filas de datos
    elev_previa = None
    for nombre, nombre_excel, elev in ESPECIES:
        for codigo, texto_trat in TRATAMIENTOS:
            clave = (alias[nombre_excel], codigo)
            if clave not in datos:
                raise KeyError(f"No está en {conf['excel']}: {clave}")
            tr = copy.deepcopy(FILA_TRAT[texto_trat])
            ajustar_columnas(tr, n_total, anchos)
            tcs = celdas(tr)
            primera = codigo == TRATAMIENTOS[0][0]
            poner_texto(tcs[0], str(elev) if (primera and elev != elev_previa) else "")
            poner_texto(tcs[1], nombre if primera else "")
            poner_texto(tcs[2], texto_trat, LLAMADAS.get((nombre, texto_trat)))
            for tc in tcs[:2]:
                poner_color(tc, COLOR_ELEV[elev])
            for tc, (v, _, dec) in zip(tcs[3:], cols):
                media, sd = datos[clave][v]
                poner_texto(tc, formato(media, sd, dec))
            tbl.append(tr)
            if primera:
                elev_previa = elev

    # Cambio de orientación: se cierra la sección anterior con un salto de sección
    if k > 0 and apaisada != TABLAS[k - 1].get("apaisada", False):
        cierre = doc.add_paragraph()
        body.remove(cierre._p); sectPr.addprevious(cierre._p)
        cierre._p.get_or_add_pPr().append(copy.deepcopy(sectPr))
        pg = sectPr.find(qn("w:pgSz"))
        w, h = sorted([int(pg.get(qn("w:w"))), int(pg.get(qn("w:h")))])
        pg.set(qn("w:w"), str(h if apaisada else w)); pg.set(qn("w:h"), str(w if apaisada else h))
        if apaisada:
            pg.set(qn("w:orient"), "landscape")
        elif pg.get(qn("w:orient")) is not None:
            del pg.attrib[qn("w:orient")]
        salto = False
    else:
        salto = k > 0
    parrafo(conf["titulo"], negrita=True, tam=10, despues=4, salto=salto)
    sectPr.addprevious(tbl)
    sup = str.maketrans("abcdefgh", "ᵃᵇᶜᵈᵉᶠᵍʰ")
    notas = " ".join(f"{a.translate(sup)} {t}" for a, t in NOTAS_LLAMADAS.items())
    parrafo(f"Values are mean ± SD of individual trees. {notas}", tam=8, antes=4)

doc.save(SALIDA)
print("\nGuardado:", SALIDA)
