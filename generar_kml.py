#!/usr/bin/env python3
"""KML enriquecido de la Falla de San Ramon.

Capas derivadas de los parametros publicados de la falla (GEM/SARA) + limites
comunales de OpenStreetMap. Nada de geometria inventada: cada capa se calcula
a partir de manteo, profundidad sismogenica y la traza del catalogo.
"""
import json
import math
import os
import urllib.parse
import urllib.request

SCR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCR, "falla-san-ramon.kml")

GEM_URL = ("https://raw.githubusercontent.com/GEMScienceTools/"
           "gem-global-active-faults/master/geojson/gem_active_faults.geojson")
OVERPASS = "https://overpass-api.de/api/interpreter"
OVERPASS_Q = """[out:json][timeout:90];
(relation["admin_level"="8"]["boundary"="administrative"]
  ["name"~"^(Lo Barnechea|Las Condes|La Reina|Peñalolén|La Florida|Puente Alto|Pirque)$"]
  (-33.95,-70.95,-33.15,-70.05););
out geom;"""


def fetch(path, url, data=None):
    """Descarga un insumo si no esta ya en disco."""
    full = os.path.join(SCR, path)
    if os.path.exists(full):
        return full
    print("descargando %s ..." % path)
    body = urllib.parse.urlencode({"data": data}).encode() if data else None
    # Overpass rechaza el User-Agent por defecto de urllib con un HTTP 406
    req = urllib.request.Request(url, body, {"User-Agent": "kml-falla-san-ramon/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        open(full, "wb").write(r.read())
    return full


fetch("gem.geojson", GEM_URL)
fetch("comunas.json", OVERPASS, OVERPASS_Q)

# ---------------------------------------------------------------- parametros
DIP_PREF = 40.0          # grados, valor central de GEM "(37.0,40,55)"
DIP_MIN, DIP_MAX = 37.0, 55.0
Z_MAX = 24.0             # km, lower_seis_depth
CORRIDOR_KM = 1.0        # semiancho del corredor de incertidumbre
DEPTHS = [5, 10, 15, 20]

# ------------------------------------------------------------------ utilidad
def m_per_deg(lat):
    """metros por grado de lat y lon a una latitud dada (WGS84 aproximado)."""
    la = math.radians(lat)
    mlat = 111132.92 - 559.82 * math.cos(2 * la) + 1.175 * math.cos(4 * la)
    mlon = 111412.84 * math.cos(la) - 93.5 * math.cos(3 * la)
    return mlat, mlon


def east_offset(lon, lat, km):
    """Desplaza un punto km hacia el Este (dip_dir = E segun GEM)."""
    _, mlon = m_per_deg(lat)
    return lon + km * 1000.0 / mlon, lat


def densify(pts, step_deg=0.002):
    out = []
    for a, b in zip(pts, pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = max(1, int(max(abs(dx), abs(dy)) / step_deg))
        for i in range(n):
            out.append((a[0] + dx * i / n, a[1] + dy * i / n))
    out.append(tuple(pts[-1]))
    return out


def perp_offset(pts, km):
    """Desplaza la polilinea km perpendicular a su rumbo (signo = lado)."""
    out = []
    for i, p in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        mlat, mlon = m_per_deg(p[1])
        dx = (b[0] - a[0]) * mlon
        dy = (b[1] - a[1]) * mlat
        n = math.hypot(dx, dy) or 1.0
        # normal a la izquierda del sentido de avance
        nx, ny = -dy / n, dx / n
        out.append((p[0] + nx * km * 1000.0 / mlon,
                    p[1] + ny * km * 1000.0 / mlat))
    return out


def rdp(pts, eps):
    """Douglas-Peucker para aligerar los limites comunales."""
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    den = math.hypot(dx, dy)
    idx, dmax = 0, -1.0
    for i in range(1, len(pts) - 1):
        p = pts[i]
        d = (abs(dy * p[0] - dx * p[1] + b[0] * a[1] - b[1] * a[0]) / den
             if den else math.hypot(p[0] - a[0], p[1] - a[1]))
        if d > dmax:
            idx, dmax = i, d
    if dmax > eps:
        return rdp(pts[:idx + 1], eps)[:-1] + rdp(pts[idx:], eps)
    return [a, b]


def coords(pts):
    return "\n".join("%.6f,%.6f,0" % (p[0], p[1]) for p in pts)


# ------------------------------------------------------------------- fuentes
gem = json.load(open(SCR + "/gem.geojson"))
feat = next(f for f in gem["features"]
            if f["properties"].get("name") == "San Ramon 01a")
props = feat["properties"]
trace = sorted(feat["geometry"]["coordinates"], key=lambda p: -p[1])
line = densify(trace)


def hav_len(pts):
    R = 6371.0
    tot = 0.0
    for a, b in zip(pts, pts[1:]):
        p1, p2 = math.radians(a[1]), math.radians(b[1])
        h = (math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2)
             * math.sin(math.radians(b[0] - a[0]) / 2) ** 2)
        tot += 2 * R * math.asin(math.sqrt(h))
    return tot


largo = hav_len(trace)

# segmentos de subduccion en las latitudes de Santiago
subd = []
for f in gem["features"]:
    if f["properties"].get("slip_type") != "Subduction_Thrust":
        continue
    P = (f["geometry"]["coordinates"] if f["geometry"]["type"] == "LineString"
         else [p for c in f["geometry"]["coordinates"] for p in c])
    # solo el margen chileno frente a Santiago: todos los puntos dentro de la caja
    if all(-75.0 < p[0] < -70.5 and -35.0 < p[1] < -32.2 for p in P):
        subd.append(P)

comunas = json.load(open(SCR + "/comunas.json"))

# ------------------------------------------------------------ capas derivadas
def downdip(km_depth, dip):
    d = km_depth / math.tan(math.radians(dip))
    return [east_offset(p[0], p[1], d) for p in line], d


plane_edge, d_max = downdip(Z_MAX, DIP_PREF)
_, d_min_dip = downdip(Z_MAX, DIP_MAX)   # manteo alto -> banda angosta
_, d_max_dip = downdip(Z_MAX, DIP_MIN)   # manteo bajo -> banda ancha

corridor = perp_offset(line, CORRIDOR_KM) + perp_offset(line, -CORRIDOR_KM)[::-1]
plane_poly = line + plane_edge[::-1]

# barbas de falla inversa cada ~1.5 km sobre el bloque colgante (Este)
barbs = []
acc = 0.0
for i in range(len(line) - 1):
    acc += hav_len([line[i], line[i + 1]])
    if acc < 1.5:
        continue
    acc = 0.0
    a, b = line[i], line[i + 1]
    mlat, mlon = m_per_deg(a[1])
    dx, dy = (b[0] - a[0]) * mlon, (b[1] - a[1]) * mlat
    n = math.hypot(dx, dy) or 1.0
    ux, uy = dx / n, dy / n
    half, h = 350.0, 450.0
    p1 = (a[0] - ux * half / mlon, a[1] - uy * half / mlat)
    p2 = (a[0] + ux * half / mlon, a[1] + uy * half / mlat)
    # normal a la izquierda del avance N->S = Este = bloque colgante
    apex = (a[0] + (-uy) * h / mlon, a[1] + ux * h / mlat)
    barbs.append([p1, p2, apex, p1])

SECTORES = [
    (-33.372, "Lo Barnechea", "Extremo norte mapeado de la traza, sector estero Arrayan."),
    (-33.410, "Las Condes", "La falla corre por el pie del cordon de Ramon."),
    (-33.452, "La Reina", "Sector Quebrada de Ramon / Parque Natural Aguas de Ramon."),
    (-33.497, "Penalolen", "Sector Quebrada de Macul, uno de los tramos mejor estudiados."),
    (-33.535, "La Florida", "Piedemonte urbanizado sobre la traza."),
    (-33.580, "Puente Alto", "Tramo sur, hacia el valle del Maipo."),
    (-33.615, "Pirque", "Extremo sur mapeado; evidencias confirmadas por la U. de Chile."),
]

# ------------------------------------------------------------------ armado
K = []
A = K.append
A('<?xml version="1.0" encoding="UTF-8"?>')
A('<kml xmlns="http://www.opengis.net/kml/2.2"><Document>')
A("<name>Falla de San Ramon - Santiago, Chile</name>")

A("<description><![CDATA[" + """
<h3>Falla de San Ramon</h3>
<p>Falla inversa activa en el piedemonte andino oriente de Santiago. Levanta el
frente cordillerano por sobre la cuenca y puede generar sismos corticales propios,
con ruptura en superficie.</p>
<table>
<tr><td><b>Tipo</b></td><td>Inversa (reverse), vergencia oeste</td></tr>
<tr><td><b>Manteo</b></td><td>%(dmin).0f-%(dmax).0f grados al Este (valor central %(dp).0f)</td></tr>
<tr><td><b>Profundidad sismogenica</b></td><td>0 - %(z).0f km</td></tr>
<tr><td><b>Tasa de deslizamiento</b></td><td>~0,4 mm/ano</td></tr>
<tr><td><b>Largo de traza</b></td><td>~%(km).0f km</td></tr>
</table>
<h4>Leyenda</h4>
<ul>
<li><b><font color="#e62020">Linea roja</font></b> - traza de superficie. Los
triangulos apuntan al bloque colgante (simbolo de falla inversa).</li>
<li><b><font color="#e62020">Banda roja translucida</font></b> - corredor de
incertidumbre de +/-%(cor).1f km. La traza del catalogo tiene 6 vertices: la
posicion real no se conoce con precision de metros.</li>
<li><b><font color="#ff8c00">Zona naranja</font></b> - proyeccion en superficie
del plano de falla en profundidad. Se extiende ~%(dd).0f km al oriente con el
manteo central; entre %(dlo).0f y %(dhi).0f km segun el rango de manteo. Es la
franja bajo la cual esta el plano que podria romper.</li>
<li><b><font color="#ff8c00">Lineas naranjas punteadas</font></b> - profundidad
del plano a 5, 10, 15 y 20 km.</li>
<li><b><font color="#888888">Lineas grises</font></b> - limites comunales (OSM).</li>
<li><b><font color="#d7b400">Linea dorada</font></b> - contacto de subduccion
frente a la costa, para comparar escalas.</li>
</ul>
<p><b>Capas apagadas por defecto:</b> activalas en el panel <i>Lugares</i>.</p>
<p><b>Fuente:</b> GEM Global Active Faults Database, modelo SARA, id %(cid)s
(CC BY-SA 4.0). Limites comunales: OpenStreetMap (ODbL). Las capas derivadas
(corredor, plano, curvas) se calculan a partir de los parametros publicados,
asumiendo un plano de manteo constante: es una <b>simplificacion geometrica</b>,
no un modelo estructural. Sirve para entender la falla, <b>no</b> para evaluar
un predio.</p>
""" % {"dmin": DIP_MIN, "dmax": DIP_MAX, "dp": DIP_PREF, "z": Z_MAX, "km": largo,
       "cor": CORRIDOR_KM, "dd": d_max, "dlo": d_min_dip, "dhi": d_max_dip,
       "cid": props.get("catalog_id")} + "]]></description>")

A("""<LookAt><longitude>-70.62</longitude><latitude>-33.49</latitude>
<altitude>0</altitude><heading>75</heading><tilt>65</tilt><range>60000</range>
<altitudeMode>relativeToGround</altitudeMode></LookAt>""")

A("""
<Style id="traza"><LineStyle><color>ff2020e6</color><width>5</width></LineStyle></Style>
<Style id="barba"><LineStyle><color>ff2020e6</color><width>1</width></LineStyle>
  <PolyStyle><color>ff2020e6</color></PolyStyle></Style>
<Style id="corredor"><LineStyle><color>802020e6</color><width>1</width></LineStyle>
  <PolyStyle><color>2e2020e6</color></PolyStyle></Style>
<Style id="plano"><LineStyle><color>9900a5ff</color><width>2</width></LineStyle>
  <PolyStyle><color>2200a5ff</color></PolyStyle></Style>
<Style id="curva"><LineStyle><color>bb00a5ff</color><width>2</width></LineStyle></Style>
<Style id="comuna"><LineStyle><color>96b4b4b4</color><width>2</width></LineStyle>
  <PolyStyle><fill>0</fill></PolyStyle></Style>
<Style id="subd"><LineStyle><color>ff00d7ff</color><width>4</width></LineStyle></Style>
<Style id="sector"><IconStyle><color>ff2020e6</color><scale>0.9</scale>
  <Icon><href>http://maps.google.com/mapfiles/kml/shapes/caution.png</href></Icon>
  </IconStyle><LabelStyle><scale>0.8</scale></LabelStyle></Style>""")

# --- 1. traza + barbas
A('<Folder><name>1. Traza de la falla</name><open>1</open><visibility>1</visibility>')
A('<Placemark><name>Falla de San Ramon (traza de superficie)</name>')
A('<styleUrl>#traza</styleUrl>')
A('<description><![CDATA[Falla inversa activa, manteo %s-%s grados al Este, '
  'tasa ~0,4 mm/ano. Traza del catalogo GEM/SARA (6 vertices, densificados a %d '
  'puntos solo para que se pegue al relieve).]]></description>'
  % (DIP_MIN, DIP_MAX, len(line)))
A('<LineString><tessellate>1</tessellate><altitudeMode>clampToGround</altitudeMode>')
A("<coordinates>%s</coordinates></LineString></Placemark>" % coords(line))

A('<Folder><name>Simbolo de falla inversa</name><visibility>1</visibility>')
for i, b in enumerate(barbs):
    A('<Placemark><name>.</name><styleUrl>#barba</styleUrl><Polygon>'
      '<tessellate>1</tessellate><altitudeMode>clampToGround</altitudeMode>'
      '<outerBoundaryIs><LinearRing><coordinates>%s</coordinates>'
      '</LinearRing></outerBoundaryIs></Polygon></Placemark>' % coords(b))
A("</Folder></Folder>")

# --- 2. corredor
A('<Folder><name>2. Corredor de incertidumbre (+/-%.0f km)</name><visibility>1</visibility>'
  % CORRIDOR_KM)
A('<Placemark><name>Corredor de incertidumbre</name><styleUrl>#corredor</styleUrl>')
A('<description><![CDATA[La traza publicada tiene solo 6 vertices y escala '
  'regional. Esta banda de +/-%.0f km refleja esa resolucion: la falla esta '
  '<i>en algun lugar</i> de esta franja, no exactamente sobre la linea.'
  ']]></description>' % CORRIDOR_KM)
A('<Polygon><tessellate>1</tessellate><altitudeMode>clampToGround</altitudeMode>'
  '<outerBoundaryIs><LinearRing><coordinates>%s</coordinates></LinearRing>'
  '</outerBoundaryIs></Polygon></Placemark></Folder>' % coords(corridor + [corridor[0]]))

# --- 3. plano en profundidad
A('<Folder><name>3. Plano de falla en profundidad</name><visibility>0</visibility>')
A('<Placemark><visibility>0</visibility><name>Proyeccion en superficie del plano (0-%.0f km)</name>'
  '<styleUrl>#plano</styleUrl>' % Z_MAX)
A('<description><![CDATA[El plano mantea al Este, asi que en profundidad se '
  'mete bajo la cordillera. Con manteo de %.0f grados llega a %.0f km al oriente '
  'de la traza a %.0f km de profundidad (entre %.0f y %.0f km segun el rango de '
  'manteo publicado). Bajo esta franja esta la superficie que podria romper.'
  ']]></description>' % (DIP_PREF, d_max, Z_MAX, d_min_dip, d_max_dip))
A('<Polygon><tessellate>1</tessellate><altitudeMode>clampToGround</altitudeMode>'
  '<outerBoundaryIs><LinearRing><coordinates>%s</coordinates></LinearRing>'
  '</outerBoundaryIs></Polygon></Placemark>' % coords(plane_poly + [plane_poly[0]]))
for z in DEPTHS:
    pts, d = downdip(z, DIP_PREF)
    A('<Placemark><visibility>0</visibility><name>Plano a %d km de profundidad</name>'
      '<styleUrl>#curva</styleUrl>' % z)
    A('<description><![CDATA[Vertical sobre el punto donde el plano de falla '
      'pasa por los %d km de profundidad: %.1f km al oriente de la traza.'
      ']]></description>' % (z, d))
    A('<LineString><tessellate>1</tessellate><altitudeMode>clampToGround</altitudeMode>'
      '<coordinates>%s</coordinates></LineString></Placemark>' % coords(pts))
A("</Folder>")

# --- 4. sectores
A('<Folder><name>4. Sectores atravesados</name><visibility>1</visibility>')
for lat, nombre, nota in SECTORES:
    p = min(line, key=lambda q: abs(q[1] - lat))
    A('<Placemark><name>%s</name><styleUrl>#sector</styleUrl>' % nombre)
    A('<description><![CDATA[%s<br/><i>Punto sobre la traza a la altura de la '
      'comuna.</i>]]></description>' % nota)
    A('<Point><altitudeMode>clampToGround</altitudeMode>'
      '<coordinates>%.6f,%.6f,0</coordinates></Point></Placemark>' % (p[0], p[1]))
A("</Folder>")

# --- 5. comunas
A('<Folder><name>5. Comunas atravesadas (OpenStreetMap)</name><visibility>0</visibility>')
for e in comunas["elements"]:
    nom = e["tags"].get("name")
    A('<Placemark><visibility>0</visibility><name>%s</name><styleUrl>#comuna</styleUrl>'
      '<MultiGeometry>' % nom)
    for m in e.get("members", []):
        if m.get("role") != "outer" or not m.get("geometry"):
            continue
        pts = rdp([(g["lon"], g["lat"]) for g in m["geometry"]], 0.0008)
        if len(pts) < 2:
            continue
        A('<LineString><tessellate>1</tessellate>'
          '<altitudeMode>clampToGround</altitudeMode>'
          '<coordinates>%s</coordinates></LineString>' % coords(pts))
    A("</MultiGeometry></Placemark>")
A("</Folder>")

# --- 6. subduccion
A('<Folder><name>6. Contexto: contacto de subduccion</name><visibility>0</visibility>')
A('<Placemark><visibility>0</visibility><name>Contacto de subduccion (Nazca / Sudamerica)</name>'
  '<styleUrl>#subd</styleUrl>')
A('<description><![CDATA[Aqui se generan los grandes terremotos chilenos '
  '(1985, 2010). Converge a ~80 mm/ano, doscientas veces mas rapido que San '
  'Ramon (~0,4 mm/ano). La diferencia: la subduccion esta mar adentro y a '
  'decenas de km de profundidad; San Ramon esta debajo de la ciudad.'
  ']]></description>')
A("<MultiGeometry>")
for P in subd:
    A('<LineString><tessellate>1</tessellate><altitudeMode>clampToGround</altitudeMode>'
      '<coordinates>%s</coordinates></LineString>' % coords(P))
A("</MultiGeometry></Placemark></Folder>")

A("</Document></kml>")
open(OUT, "w", encoding="utf-8").write("\n".join(K))

print("largo traza      : %.1f km" % largo)
print("manteo central   : %.0f deg -> borde a %.1f km al E" % (DIP_PREF, d_max))
print("rango de manteo  : %.0f-%.0f deg -> %.1f a %.1f km" % (DIP_MIN, DIP_MAX, d_min_dip, d_max_dip))
print("barbas           : %d" % len(barbs))
print("segmentos subd.  : %d" % len(subd))
print("comunas          : %d" % len(comunas["elements"]))
print("escrito          :", OUT)
