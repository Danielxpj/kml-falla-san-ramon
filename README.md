# KML de la Falla de San Ramón para Google Earth 🌎

**Este repositorio contiene un archivo KML para abrir en Google Earth.** Al
cargarlo, verás dibujada sobre el mapa la traza de la **Falla de San Ramón**, la
falla geológica activa que corre por el piedemonte andino al oriente de Santiago
de Chile.

No necesitas saber nada de geología ni de programación para usarlo: se descarga,
se abre con doble clic y listo. Abajo están los pasos, uno por uno.

![Formato](https://img.shields.io/badge/formato-KML-red) ![Programa](https://img.shields.io/badge/programa-Google%20Earth-4285F4) ![Datos](https://img.shields.io/badge/datos-GEM%20SARA-blue) ![Licencia](https://img.shields.io/badge/licencia-CC%20BY--SA%204.0-lightgrey)

---

## 📥 Paso 1 — Descargar el archivo

Elige **una** de estas dos formas:

**Opción A (la más fácil):**
1. Anda arriba en esta misma página y haz clic en el archivo **`falla-san-ramon.kml`**.
2. Busca el botón de descarga (el ícono de la flecha hacia abajo ⬇️, arriba a la derecha del archivo).
3. Guárdalo donde lo encuentres después. Por ejemplo, tu carpeta **Descargas**.

**Opción B (bajar todo el repositorio):**
1. Vuelve a la página principal del repositorio.
2. Haz clic en el botón verde **`Code`**.
3. Elige **`Download ZIP`**.
4. Descomprime el ZIP. El archivo `falla-san-ramon.kml` está adentro.

> ⚠️ **Ojo:** el archivo debe terminar en `.kml`. Si tu navegador lo guardó como
> `falla-san-ramon.kml.txt`, renómbralo y bórrale el `.txt` del final.

---

## 🌍 Paso 2 — Instalar Google Earth (si no lo tienes)

- **Google Earth Pro para computador** — descárgalo gratis desde
  [google.com/earth/versions](https://www.google.com/earth/versions/) (hay versión
  para Windows, Mac y Linux).
- **O sin instalar nada:** usa Google Earth en el navegador, en
  [earth.google.com](https://earth.google.com/).

---

## 🖱️ Paso 3 — Abrir el KML

Hay **cuatro** maneras. Todas hacen exactamente lo mismo, usa la que te acomode.

### Forma 1 — Desde el menú *Archivo → Abrir* (la más a prueba de tontos)

1. Abre **Google Earth Pro**.
2. En la barra de menús de arriba, haz clic en **`Archivo`** (o **`File`** si lo
   tienes en inglés).
3. Haz clic en **`Abrir...`** (o **`Open...`**). También sirve el atajo de teclado
   **`Ctrl + O`** — en Mac, **`⌘ + O`**.
4. Se abrirá una ventana para buscar archivos. Navega hasta donde guardaste
   `falla-san-ramon.kml` (por ejemplo, la carpeta **Descargas**).
5. Haz clic en el archivo y después en el botón **`Abrir`**.
6. Google Earth volará solo hasta Santiago y verás la línea roja de la falla.

> 💡 Si en esa ventana no aparece el archivo aunque sepas que está ahí, busca
> abajo un desplegable que diga *Tipo de archivo* y déjalo en **`Todos los
> archivos`** o en **`Kml (*.kml)`**.

### Forma 2 — Doble clic

Simplemente haz **doble clic** sobre el archivo `falla-san-ramon.kml` en tu
carpeta. Si Google Earth está instalado, se abre solo.

### Forma 3 — Arrastrar y soltar

Abre Google Earth, y **arrastra** el archivo `.kml` desde tu carpeta **hasta
adentro** de la ventana de Google Earth. Suéltalo ahí.

### Forma 4 — En el navegador (Google Earth Web)

1. Entra a [earth.google.com](https://earth.google.com/).
2. En el menú lateral izquierdo (☰), elige **`Proyectos`**.
3. Haz clic en **`Abrir`** → **`Importar archivo KML`**.
4. Selecciona el archivo `falla-san-ramon.kml`.

### Desde la terminal (Linux / macOS)

```bash
google-earth-pro falla-san-ramon.kml
```

Si usas **KDE con Wayland** y Google Earth Pro no arranca o se ve mal:

```bash
env -u QT_QPA_PLATFORMTHEME -u QT_QPA_PLATFORM google-earth-pro falla-san-ramon.kml
```

---

## ✅ Paso 4 — Qué deberías ver

- Una **línea roja** de unos 28 km, de norte a sur, pegada al terreno, justo en el
  borde donde la ciudad de Santiago se topa con la cordillera.
- **Siete marcadores** con un ícono de advertencia ⚠️, uno por cada comuna que la
  falla atraviesa.
- Si haces **clic sobre la línea roja**, se abre un globo con la ficha técnica de
  la falla.
- A la izquierda, en el panel **`Lugares`**, aparecerá una carpeta llamada
  *"Falla de San Ramón"*. Ahí puedes prender y apagar las capas con las casillas.

> ⚠️ **¿No ves nada?** Revisa en el panel **`Lugares`** (izquierda) que la casilla
> de la capa esté **marcada**. Después haz doble clic sobre el nombre de la capa
> para que la cámara vuele hasta ella.

---

## 🏔️ Qué es la Falla de San Ramón

Es una falla **inversa de vergencia oeste** que levanta el frente cordillerano por
sobre la cuenca de Santiago. A diferencia de los grandes terremotos de subducción
chilenos —los que ocurren mar adentro—, esta es una falla **cortical**: puede
generar sus propios sismos, con ruptura llegando a la superficie, justo debajo de
una zona densamente urbanizada.

| Parámetro | Valor |
|---|---|
| Tipo de falla | Inversa (*reverse*), vergencia oeste |
| Manteo | ~37–55° hacia el Este |
| Profundidad sismogénica | 0 – 24 km |
| Tasa de deslizamiento | ~0,4 mm/año |
| Largo de la traza mapeada | ~28 km |
| Comunas atravesadas | Lo Barnechea, Las Condes, La Reina, Peñalolén, La Florida, Puente Alto, Pirque |

---

## 📦 Qué contiene el archivo

`falla-san-ramon.kml` incluye:

- **Traza de superficie** — línea roja de ~28 km pegada al terreno
  (`clampToGround`), desde Lo Barnechea por el norte (lat −33,37) hasta Pirque por
  el sur (lat −33,62), corriendo por el pie del cordón de Ramón en torno a los
  −70,52 / −70,55 de longitud.
- **7 marcadores de sector**, uno por comuna atravesada, ubicados *sobre* la traza
  a la altura de cada comuna.
- **Ficha técnica** de la falla en la descripción del documento (manteo,
  profundidad, tasa de deslizamiento, fuente).
- **Vista inicial inclinada** desde el poniente, orientada para que se aprecie el
  escarpe contra la cordillera.

---

## 🔬 Origen de los datos

La geometría **no es una estimación propia**: proviene de la
[GEM Global Active Faults Database](https://github.com/GEMScienceTools/gem-global-active-faults),
entrada `San Ramon 01a` del modelo **SARA** (*South America Risk Assessment*),
id de catálogo `SA_71`.

---

## ⚠️ Limitaciones — léelas antes de usar esto para algo serio

1. **La traza original tiene solo 6 vértices.** Es un trazado *regional*, pensado
   para modelos de amenaza sísmica, no un mapeo geológico de detalle. En el KML
   está densificada a 123 puntos para que se pegue bien al relieve, pero eso es
   pura interpolación lineal sobre los mismos segmentos: **no agrega precisión
   real**.

2. **Sirve para ubicar la falla, no para saber si un predio concreto está encima
   de ella.** Para eso se necesita la cartografía de detalle
   (Armijo et al., 2010; Vargas et al., 2014) o un estudio de sitio.

3. **Esto no es un documento oficial** ni sustituye la información de SERNAGEOMIN
   ni el criterio de un profesional competente. Es material divulgativo y
   educativo.

---

## 📚 Referencias

- Armijo, R. et al. (2010). *The West Andean Thrust, the San Ramón Fault, and the
  seismic hazard for Santiago, Chile*. Tectonics, 29, TC2007.
- Vargas, G. et al. (2014). *Probing large intraplate earthquakes at the west
  flank of the Andes*. Geology, 42(12).
- Universidad de Chile, Depto. de Geología — [evidencias de la falla en Pirque](https://geologia.uchile.cl/noticias/220972/u-de-chile-confirma-evidencias-de-la-falla-san-ramon-en-pirque)
- [Policy Brief: La Falla San Ramón y la sostenibilidad del piedemonte](https://repositorio.uchile.cl/bitstream/handle/2250/183864/Falla-San-Ramon.pdf?sequence=1)

---

## 📄 Licencia

**CC BY-SA 4.0.** Obligatorio, no opcional: el dato de origen (GEM Global Active
Faults) está bajo esa licencia, y por *share-alike* cualquier obra derivada —
este KML incluido — hereda las mismas condiciones. Ver [LICENSE](LICENSE).

---

## 🔎 Etiquetas

Falla de San Ramón · falla San Ramón Santiago · KML Google Earth Chile · mapa
falla geológica Santiago · riesgo sísmico Santiago · piedemonte andino ·
terremoto Santiago Chile · falla activa Chile · geología Chile · Lo Barnechea ·
Las Condes · La Reina · Peñalolén · La Florida · Puente Alto · Pirque

#FallaDeSanRamon #FallaSanRamon #Santiago #SantiagoDeChile #Chile #GoogleEarth
#KML #KMZ #Geologia #Geology #FallaGeologica #FallaActiva #ActiveFault
#RiesgoSismico #SeismicHazard #AmenazaSismica #Terremoto #Earthquake #Sismologia
#Seismology #Tectonica #Tectonics #Andes #PiedemonteAndino #Cordillera
#GIS #SIG #Geoespacial #Geospatial #Cartografia #Mapping #OpenData #DatosAbiertos
#GEM #SARA #Sernageomin #LoBarnechea #LasCondes #LaReina #Penalolen #LaFlorida
#PuenteAlto #Pirque #RegionMetropolitana #GestionDeRiesgo #DisasterRiskReduction
#CienciaCiudadana #Divulgacion #QGIS #GoogleEarthPro #Falla #Geociencias
