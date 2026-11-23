<p align="center">
  <img src="../../assets/images/readme-guide.svg" alt="Quant for babies — aprende, experimenta, explica" width="960" />
</p>

<p align="center">
  <a href="../../README.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.en.md">English</a> · <a href="README.ru.md">Русский</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.fr.md">Français</a> · <a href="README.de.md">Deutsch</a> · <strong>Español</strong> · <a href="README.hi.md">हिन्दी</a>
</p>

# Finanzas cuantitativas, un experimento a la vez

Un recorrido accesible desde tu primer conjunto de datos de mercado hasta las señales, el riesgo, las carteras y la investigación reproducible. Aprende con **8 cuadernos de Jupyter, 5 lecciones de investigación y 7 demostraciones para el navegador**.

**Alcance de los idiomas:** esta guía y su navegación están disponibles en diez idiomas. Los cuadernos, las lecciones y la mayoría de los documentos de apoyo están actualmente en **chino simplificado**; cambiar el idioma de este README no traduce el contenido del curso.

<p align="center">
  <a href="#start">Empieza aquí</a> · <a href="#setup">Instalación</a> · <a href="#curriculum">Cuadernos</a> · <a href="#labs">Laboratorios de investigación</a> · <a href="#demos">Demostraciones</a> · <a href="#faq">Ayuda</a>
</p>

| Material disponible | Formato | Qué puedes hacer |
| --- | --- | --- |
| Capítulos 01–08 · disponibles | Cuadernos de Jupyter | Analizar precios, crear una regla de medias móviles, medir el riesgo y comparar carteras |
| Lecciones 01–05 · disponibles | HTML sin conexión + cuatro laboratorios de Python | Seguir el proceso datos → factores → evaluación → backtesting simulado |
| Siete demostraciones interactivas · disponibles | HTML independiente | Explorar las fórmulas visualmente, sin instalar un entorno de investigación |
| Capítulos posteriores y proyectos avanzados · previstos | [Hoja de ruta](../ROADMAP.md) | Consultar los temas propuestos por separado de las lecciones ya disponibles |

<a id="start"></a>
## 1. Elige tu punto de partida

| Tu objetivo | Empieza con | Primer resultado |
| --- | --- | --- |
| Comprender las ideas antes de programar | [Lección 01](../../extras/lecture-01/index.html) y las [demostraciones](#demos) | Explicar las etapas de un proceso de investigación cuantitativa |
| Aprender escribiendo y ejecutando Python | [Configuración del entorno](#setup) y después el [Cuaderno 01](../../notebooks/phase1_intro/01_什么是量化金融.ipynb) | Cargar datos de mercado y dibujar tu primer gráfico de precios |
| Practicar un proceso de investigación completo | [Lecciones 02–05](#labs), en orden | Generar controles de datos, tablas de factores, informes de evaluación y un registro de operaciones simuladas |
| Impartir un taller o estudiar en equipo | [Notas para el ponente de la lección 01](../../extras/lecture-01/lecture-notes.md) e instrucciones de los laboratorios | Dirigir una sesión con ejercicios y resultados que se puedan inspeccionar |

No necesitas experiencia previa en finanzas cuantitativas. Conocimientos básicos de Python ayudan con los cuadernos; puedes comenzar por las lecturas en HTML. En cada lección, sigue la secuencia **leer → ejecutar → cambiar un supuesto → explicar el resultado**.

### Lee las lecciones en HTML

**GitHub muestra el código fuente HTML; un enlace a un archivo del repositorio no abre la lección en funcionamiento.** Descarga el repositorio mediante **Code → Download ZIP**, descomprímelo y abre un archivo `extras/lecture-0N/index.html` en tu navegador. Las cinco páginas de lecciones y las siete demostraciones se pueden consultar localmente sin conexión. Las referencias externas y las descargas de datos en línea sí necesitan conexión.

También puedes ejecutar lo siguiente desde la raíz del repositorio:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

Abre `http://127.0.0.1:8000/extras/lecture-01/` (sustituye `01` por `02`–`05` para las demás lecciones). En macOS/Linux, usa `python3` si `python` no está disponible. Detén el servidor con `Ctrl+C`.

Lección 01: usa las flechas o la barra espaciadora para avanzar, `N` para las notas del ponente, `O` para la vista general y `F` para la pantalla completa.

<a id="setup"></a>
## 2. Configura tu entorno para los cuadernos

Usa **Python 3.10+**; Python 3.12 es un punto de partida razonable. Instala Git para clonar el repositorio, o descarga y descomprime el ZIP. Ejecuta los siguientes comandos en una terminal. Las rutas directas al entorno evitan problemas de activación en el intérprete de comandos.

<details>
<summary><strong>Windows · PowerShell</strong></summary>

```powershell
git clone https://github.com/ThreshoLdnnis/Quant-for-babies.git
cd Quant-for-babies
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

Si descargaste un ZIP, abre PowerShell en la carpeta del repositorio descomprimido y empieza en `python -m venv .venv`.

</details>

<details>
<summary><strong>macOS / Linux · Terminal</strong></summary>

```bash
git clone https://github.com/ThreshoLdnnis/Quant-for-babies.git
cd Quant-for-babies
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyterlab
```

Si descargaste un ZIP, abre una terminal en la carpeta del repositorio descomprimido y empieza en `python3 -m venv .venv`.

</details>

Jupyter muestra una URL local en la terminal. Ábrela en tu navegador, selecciona `notebooks/phase1_intro/01_什么是量化金融.ipynb` y ejecuta las celdas de arriba abajo (`Shift+Enter`). Comprueba que el cuaderno utiliza el entorno que acabas de crear.

| Grupo de dependencias | Finalidad | Dónde instalarlas |
| --- | --- | --- |
| Jupyter, NumPy, pandas, Matplotlib, seaborn | Ejecutar cuadernos, tablas y gráficos | [Requisitos de la raíz](../../requirements.txt) |
| yfinance, AkShare | Ejemplos con datos de mercado; requieren conexión | Requisitos de la raíz |
| scikit-learn | Herramientas de aprendizaje automático en el entorno de aprendizaje | Requisitos de la raíz; los capítulos posteriores de IA siguen previstos |
| Requisitos de cada lección | Laboratorios de investigación sin conexión; la lección 04 también necesita SciPy | El archivo `requirements.txt` de cada carpeta de lección |
| Paquetes opcionales de gráficos | Exportar figuras de los laboratorios | `requirements-plot.txt` de las lecciones 03–05 |

<a id="curriculum"></a>
## 3. Sigue el recorrido de ocho cuadernos

Trabaja en orden dentro de cada fase. Guarda tu gráfico, el parámetro que cambiaste y una breve explicación de lo ocurrido.

| Capítulo | Tema / cuaderno | Resultado de aprendizaje |
| :---: | --- | --- |
| 01 | [¿Qué son las finanzas cuantitativas?](../../notebooks/phase1_intro/01_什么是量化金融.ipynb) | Desarrollar intuición y descargar datos de precios de AAPL |
| 02 | [Tu primer experimento cuantitativo](../../notebooks/phase1_intro/02_你的第一个量化实验.ipynb) | Leer OHLCV, calcular rentabilidades y comparar volatilidades |
| 03 | [Estrategia de medias móviles](../../notebooks/phase1_intro/03_移动平均线策略.ipynb) | Convertir los cruces de MA5/MA20 en una regla de negociación explícita |
| 04 | [Backtesting de estrategias](../../notebooks/phase1_intro/04_策略回测.ipynb) | Simular operaciones y examinar el capital, la tasa de acierto y el drawdown |
| 05 | [Comprender la volatilidad](../../notebooks/phase2_intro/01_理解波动率.ipynb) | Medir y anualizar la volatilidad de distintos activos |
| 06 | [Ratio de Sharpe y Beta](../../notebooks/phase2_intro/02_夏普比率与Beta.ipynb) | Comparar rentabilidades ajustadas al riesgo y sensibilidad al mercado |
| 07 | [Drawdown máximo y tamaño de las posiciones](../../notebooks/phase2_intro/03_最大回撤与仓位管理.ipynb) | Relacionar el drawdown con la exposición y la tolerancia al riesgo |
| 08 | [Carteras y correlación](../../notebooks/phase2_intro/04_多标的组合与相关性.ipynb) | Crear una cartera equiponderada y explorar la diversificación |

**Fase 1 · Capítulos 01–04:** datos → rentabilidades → reglas → backtest.<br />
**Fase 2 · Capítulos 05–08:** volatilidad → métricas ajustadas al riesgo → tamaño de posiciones → carteras.

<details>
<summary>Vista previa de los primeros cuatro capítulos</summary>

<p>
  <img src="../../assets/images/ch01_real_stock.png" alt="Capítulo 01: datos de mercado" width="46%" />
  <img src="../../assets/images/ch02_returns.png" alt="Capítulo 02: rentabilidades" width="46%" />
</p>
<p>
  <img src="../../assets/images/ch03_ma_signals.png" alt="Capítulo 03: señales de medias móviles" width="46%" />
  <img src="../../assets/images/ch04_backtest.png" alt="Capítulo 04: backtest" width="46%" />
</p>

</details>

<a id="labs"></a>
## 4. Construye un proceso de investigación en cinco lecciones

Estas lecciones complementan los cuadernos. Léelas en orden para seguir el proceso de investigación. **Conserva la estructura completa del repositorio:** los laboratorios 04 y 05 importan código de la lección 03.

| Lección | Lectura | Práctica y resultado esperado |
| :---: | --- | --- |
| 01 | [Proceso de investigación](../../extras/lecture-01/index.html) · [Notas para el ponente](../../extras/lecture-01/lecture-notes.md) | Introducción de 13 diapositivas; sin laboratorio de Python |
| 02 | [Ingeniería de datos financieros](../../extras/lecture-02/index.html) · [Instrucciones](../../extras/lecture-02/README.md) | pandas, SQLite/SQL, limpieza y aislamiento de registros problemáticos → tablas CSV, una base de datos e informes de calidad |
| 03 | [Factores y preprocesamiento](../../extras/lecture-03/index.html) · [Instrucciones](../../extras/lecture-03/README.md) | MOM20, VOL20, TURN20, MAD y puntuaciones Z transversales → tablas de factores y diagnósticos |
| 04 | [Evaluación de factores y estadística](../../extras/lecture-04/index.html) · [Instrucciones](../../extras/lecture-04/README.md) | Rank IC, ICIR, grupos y evaluación cronológica → tablas de evaluación y un informe de auditoría |
| 05 | [Backtesting multifactor](../../extras/lecture-05/index.html) · [Instrucciones](../../extras/lecture-05/README.md) | Puntuaciones estáticas, Top N, ejecución en la siguiente apertura y costes → cuentas simuladas, registros de operaciones y resúmenes de investigación |

### Ejecuta los cuatro laboratorios sin conexión

Desde la raíz del repositorio, con tu entorno virtual activo, ejecuta lo siguiente. También puedes sustituir cada `python` por `.\.venv\Scripts\python.exe` en Windows o `.venv/bin/python` en macOS/Linux.

```bash
python -m pip install -r extras/lecture-02/requirements.txt
python extras/lecture-02/lab.py --output work/lecture-02-run

python -m pip install -r extras/lecture-03/requirements.txt
python extras/lecture-03/factor_lab.py --output work/lecture-03-run

python -m pip install -r extras/lecture-04/requirements.txt
python extras/lecture-04/evaluation_lab.py --output work/lecture-04-run

python -m pip install -r extras/lecture-05/requirements.txt
python extras/lecture-05/backtest_lab.py --output work/lecture-05-run
```

Usa un directorio de salida dedicado para cada laboratorio. Los scripts protegen los directorios no vacíos que no les pertenecen; consulta las instrucciones de la lección antes de cambiar o reutilizar una ruta de salida. Los scripts opcionales de gráficos y el ejercicio de recopilación de datos de AkShare con conexión se documentan en las carpetas correspondientes.

**Cómo interpretar los resultados:** los laboratorios principales utilizan **datos didácticos simulados** y deterministas, y no necesitan conexión a datos de mercado una vez instaladas las dependencias. Las muestras cortas y los costes hipotéticos ilustran métodos; no demuestran una estrategia apta para invertir ni un rendimiento formal fuera de muestra. Las descargas de los cuadernos pueden utilizar precios históricos reales. Algunas demostraciones incluyen instantáneas históricas; sus controles no consultan precios en tiempo real.

<a id="demos"></a>
## 5. Explora los conceptos visualmente

Descarga y abre los archivos HTML, o utiliza el servidor local descrito anteriormente. Las [notas de las demostraciones](../../assets/interactive/README.md) explican sus datos y funcionamiento.

| Demostración | Mejor junto con | Prueba esto |
| --- | --- | --- |
| [Movimiento browniano / paseo aleatorio](../../assets/interactive/brownian-random-walk.html) | Capítulo 01 | Comparar trayectorias y distinguir la aleatoriedad de una predicción |
| [Rentabilidades diarias](../../assets/interactive/daily-return-demo.html) | Capítulo 05 | Seguir el cálculo desde el precio hasta la rentabilidad |
| [Desviación estándar muestral](../../assets/interactive/std-dev-demo.html) | Capítulo 05 | Examinar las desviaciones y cómo se agregan |
| [Varianza poblacional](../../assets/interactive/population-variance-demo.html) | Capítulo 05 | Relacionar la definición con un ejemplo visual |
| [Corrección de la varianza](../../assets/interactive/variance-formulas-demo.html) | Capítulo 05 | Comparar el papel de `n` y `n−1` |
| [Ratio de Sharpe](../../assets/interactive/sharpe-ratio-demo.html) | Capítulo 06 | Comparar el exceso de rentabilidad con la volatilidad |
| [Beta](../../assets/interactive/beta-demo.html) | Capítulo 06 | Explorar la relación entre un activo y un índice de referencia |

<a id="roadmap"></a>
## 6. Conoce los próximos pasos

| Estado | Alcance | Dónde consultar |
| --- | --- | --- |
| Disponible | Ocho cuadernos, cinco lecciones y siete demostraciones | Las tablas anteriores |
| Previsto · Capítulos 09–14 | Introducción al aprendizaje automático, XGBoost, LSTM, Transformer, selección multifactor y un sistema de IA cuantitativa | [Hoja de ruta detallada](../ROADMAP.md) |
| Previsto · proyectos avanzados | Asistente financiero de NLP/RAG; asignación de factores según el régimen de mercado; selección de acciones mediante aprendizaje automático y Alpha explicable | [Propuestas de proyectos](../ROADMAP.md#advanced-projects) |
| En construcción | Módulos reutilizables en `src/` | Actualmente son marcadores de posición, no un marco de backtesting para producción |

### Oriéntate en el repositorio

| Ruta | Contenido |
| --- | --- |
| [`notebooks/`](../../notebooks/) | Lecciones de las fases 1 y 2 |
| [`extras/`](../../extras/) | Lecciones HTML, instrucciones, laboratorios y herramientas opcionales de gráficos |
| [`assets/interactive/`](../../assets/interactive/) | Siete demostraciones para el navegador |
| [`assets/images/`](../../assets/images/) | Ilustraciones del curso y gráficos del README |
| [`docs/`](../) | Hoja de ruta y guías README multilingües |
| [`scripts/`](../../scripts/) | Utilidades para mantener los cuadernos y generar ilustraciones |
| [`requirements.txt`](../../requirements.txt) | Dependencias del entorno de los cuadernos |

<a id="faq"></a>
## 7. Resuelve los problemas

| Pregunta | Qué hacer |
| --- | --- |
| ¿Por qué veo código HTML en GitHub? | Descarga y abre el archivo, o utiliza el servidor HTTP local de [Empieza aquí](#start). |
| ¿Por qué falta un paquete en Jupyter? | Instálalo con `python -m pip` del mismo entorno; comprueba el kernel seleccionado y reinícialo después de instalarlo. |
| ¿Por qué falló una descarga de datos de mercado? | Comprueba tu conexión y la respuesta del proveedor. No interpretes datos vacíos como un experimento correcto. Continúa aprendiendo con los laboratorios sin conexión. |
| ¿Por qué un laboratorio rechazó el directorio de salida? | Elige un directorio nuevo y dedicado, o sigue las reglas de la lección para volver a ejecutar sobre su propia salida marcada. |
| ¿Cambiar de idioma traduce los cuadernos? | No. Hay diez guías README; el contenido didáctico sigue principalmente en chino simplificado. |
| ¿Cómo comunico un problema? | [Abre una incidencia](https://github.com/ThreshoLdnnis/Quant-for-babies/issues) con la ruta del archivo, el comando, la versión de Python y el mensaje de error. Elimina los tokens y la información personal de los registros. |

Las contribuciones son bienvenidas: correcciones, ejemplos más claros y traducciones cuidadosamente revisadas. Mantén coherentes las rutas del código y los comandos en las diez guías; consulta las [notas de mantenimiento de las traducciones](README.md).

---

**Licencia:** [MIT](../../LICENSE). **Uso educativo:** este repositorio está destinado al aprendizaje y la investigación, no constituye asesoramiento de inversión. Los resultados históricos o simulados no garantizan el rendimiento futuro.
