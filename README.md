# KML — Falla de San Ramón (Santiago, Chile)

Archivo KML para visualizar en **Google Earth** la traza de la **Falla de San Ramón**,
la falla inversa activa que corre por el piedemonte andino al oriente de Santiago.

![Tipo](https://img.shields.io/badge/formato-KML-red) ![Datos](https://img.shields.io/badge/datos-GEM%20SARA-blue) ![Licencia](https://img.shields.io/badge/licencia-CC%20BY--SA%204.0-lightgrey)

## Qué es la Falla de San Ramón

Es una falla **inversa de vergencia oeste** que levanta el frente cordillerano por
sobre la cuenca de Santiago. A diferencia de los grandes terremotos de subducción
chilenos, esta es una falla **cortical**: es capaz de generar sus propios sismos,
con ruptura en superficie, justo debajo de una zona densamente urbanizada.

| Parámetro | Valor |
|---|---|
| Tipo de falla | Inversa (*reverse*), vergencia oeste |
| Manteo | ~37–55° hacia el Este |
| Profundidad sismogénica | 0 – 24 km |
| Tasa de deslizamiento | ~0,4 mm/año |
| Largo de la traza mapeada | ~28 km |
| Comunas atravesadas | Lo Barnechea, Las Condes, La Reina, Peñalolén, La Florida, Puente Alto, Pirque |

## Qué contiene el archivo

`falla-san-ramon.kml` incluye:

- **Traza de superficie** — una línea roja de ~28 km pegada al terreno
  (`clampToGround`), desde Lo Barnechea por el norte (lat −33,37) hasta Pirque por
  el sur (lat −33,62), corriendo por el pie del cordón de Ramón en torno a los
  −70,52 / −70,55 de longitud.
- **7 marcadores de sector**, uno por comuna atravesada, ubicados *sobre* la traza
  a la altura de cada comuna.
- **Ficha técnica** de la falla en la descripción del documento (manteo,
  profundidad, tasa de deslizamiento, fuente).
- **Vista inicial inclinada** desde el poniente, orientada para que se aprecie el
  escarpe contra la cordillera.

## Cómo usarlo

Doble clic sobre el archivo, o desde terminal:

```bash
google-earth-pro falla-san-ramon.kml
```

En **KDE Wayland**, si Google Earth Pro no arranca:

```bash
env -u QT_QPA_PLATFORMTHEME -u QT_QPA_PLATFORM google-earth-pro falla-san-ramon.kml
```

También se puede cargar en Google Earth Web (earth.google.com), QGIS o cualquier
visor que soporte KML.

## Origen de los datos

La geometría **no es una estimación propia**: proviene de la
[GEM Global Active Faults Database](https://github.com/GEMScienceTools/gem-global-active-faults),
entrada `San Ramon 01a` del modelo **SARA** (*South America Risk Assessment*),
id de catálogo `SA_71`.

## Limitaciones — léelas antes de usar esto para algo serio

1. **La traza original tiene solo 6 vértices.** Es un trazado *regional*, pensado
   para modelos de amenaza sísmica, no un mapeo geológico de detalle. En el KML
   está densificada a 123 puntos para que se pegue bien al relieve, pero eso es
   pura interpolación lineal sobre los mismos segmentos: **no agrega precisión
   real**.

2. **Sirve para ubicar la falla, no para saber si un predio concreto está encima
   de ella.** Para eso se necesita la cartografía de detalle
   (Armijo et al., 2010; Vargas et al., 2014) o un estudio de sitio.

3. **Esto no es un documento oficial** ni sustituye la información de SERNAGEOMIN
   ni de un profesional competente. Es material divulgativo y educativo.

## Referencias

- Armijo, R. et al. (2010). *The West Andean Thrust, the San Ramón Fault, and the
  seismic hazard for Santiago, Chile*. Tectonics, 29, TC2007.
- Vargas, G. et al. (2014). *Probing large intraplate earthquakes at the west
  flank of the Andes*. Geology, 42(12).
- Universidad de Chile, Depto. de Geología — [evidencias de la falla en Pirque](https://geologia.uchile.cl/noticias/220972/u-de-chile-confirma-evidencias-de-la-falla-san-ramon-en-pirque)
- [Policy Brief: La Falla San Ramón y la sostenibilidad del piedemonte](https://repositorio.uchile.cl/bitstream/handle/2250/183864/Falla-San-Ramon.pdf?sequence=1)

## Licencia

**CC BY-SA 4.0.** Obligatorio, no opcional: el dato de origen (GEM Global Active
Faults) está bajo esa licencia, y por *share-alike* cualquier obra derivada —
este KML incluido — hereda las mismas condiciones. Ver [LICENSE](LICENSE).
