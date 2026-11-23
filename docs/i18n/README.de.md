<p align="center">
  <img src="../../assets/images/readme-guide.svg" alt="Quant for babies — lernen, experimentieren, erklären" width="960" />
</p>

<p align="center">
  <a href="../../README.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.en.md">English</a> · <a href="README.ru.md">Русский</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.fr.md">Français</a> · <strong>Deutsch</strong> · <a href="README.es.md">Español</a> · <a href="README.hi.md">हिन्दी</a>
</p>

# Quantitative Finanzanalyse, ein Experiment nach dem anderen

Ein verständlicher Weg vom ersten Marktdatensatz zu Signalen, Risiken, Portfolios und reproduzierbarer Forschung. Lernen Sie mit **8 Jupyter-Notebooks, 5 Forschungsvorlesungen und 7 Browser-Demos**.

**Sprachumfang:** Dieser Leitfaden und seine Navigation sind in zehn Sprachen verfügbar. Die Notebooks, Vorlesungen und die meisten Begleitdokumente sind derzeit auf **vereinfachtem Chinesisch** verfasst; ein Sprachwechsel im README übersetzt die Kursinhalte nicht.

<p align="center">
  <a href="#start">Hier beginnen</a> · <a href="#setup">Einrichtung</a> · <a href="#curriculum">Notebooks</a> · <a href="#labs">Forschungsübungen</a> · <a href="#demos">Demos</a> · <a href="#faq">Hilfe</a>
</p>

| Verfügbare Inhalte | Format | Was Sie damit tun können |
| --- | --- | --- |
| Kapitel 01–08 · verfügbar | Jupyter-Notebooks | Kurse analysieren, eine Regel mit gleitenden Durchschnitten entwickeln, Risiken messen und Portfolios vergleichen |
| Vorlesungen 01–05 · verfügbar | Offline-HTML + vier Python-Übungen | Den Ablauf Daten → Faktoren → Bewertung → simulierter Backtest nachvollziehen |
| Sieben interaktive Demos · verfügbar | Eigenständige HTML-Dateien | Formeln visuell erkunden, ohne eine Forschungsumgebung einzurichten |
| Weitere Kapitel und fortgeschrittene Projekte · geplant | [Roadmap](../ROADMAP.md) | Vorgeschlagene Themen von bereits bereitgestellten Lektionen unterscheiden |

<a id="start"></a>
## 1. Wählen Sie Ihren Einstieg

| Ihr Ziel | Beginnen Sie mit | Erstes Ergebnis |
| --- | --- | --- |
| Die Ideen vor dem Programmieren verstehen | [Vorlesung 01](../../extras/lecture-01/index.html) und den [Demos](#demos) | Die Schritte eines quantitativen Forschungsablaufs erklären |
| Durch Schreiben und Ausführen von Python lernen | [Einrichtung der Umgebung](#setup), dann [Notebook 01](../../notebooks/phase1_intro/01_什么是量化金融.ipynb) | Marktdaten laden und das erste Kursdiagramm zeichnen |
| Einen vollständigen Forschungsprozess üben | [Vorlesungen 02–05](#labs) in dieser Reihenfolge | Datenprüfungen, Faktortabellen, Bewertungsberichte und ein simuliertes Handelsbuch erstellen |
| Einen Workshop leiten oder im Team lernen | [Vortragsnotizen zu Vorlesung 01](../../extras/lecture-01/lecture-notes.md) und den Übungsanleitungen | Eine Lerneinheit mit Aufgaben und überprüfbaren Ergebnissen durchführen |

Vorkenntnisse in quantitativer Finanzanalyse sind nicht erforderlich. Python-Grundkenntnisse helfen bei den Notebooks; Sie können zunächst die HTML-Lektionen lesen. Folgen Sie in jeder Lektion dem Ablauf **lesen → ausführen → eine Annahme ändern → Ergebnis erklären**.

### Die HTML-Lektionen lesen

**GitHub zeigt den HTML-Quellcode; ein Link auf eine Repository-Datei startet die Lektion nicht.** Laden Sie das Repository über **Code → Download ZIP** herunter, entpacken Sie es und öffnen Sie eine Datei `extras/lecture-0N/index.html` im Browser. Die fünf Vorlesungsseiten und sieben Demos lassen sich lokal offline lesen. Externe Verweise und das Herunterladen von Marktdaten benötigen weiterhin eine Verbindung.

Alternativ führen Sie im Stammverzeichnis des Repositorys Folgendes aus:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

Öffnen Sie `http://127.0.0.1:8000/extras/lecture-01/` (ersetzen Sie `01` für die anderen Vorlesungen durch `02`–`05`). Verwenden Sie unter macOS/Linux `python3`, falls `python` nicht verfügbar ist. Beenden Sie den Server mit `Ctrl+C`.

Vorlesung 01: Mit den Pfeiltasten oder der Leertaste weiterblättern; `N` zeigt Vortragsnotizen, `O` die Übersicht und `F` den Vollbildmodus.

<a id="setup"></a>
## 2. Richten Sie die Notebook-Umgebung ein

Verwenden Sie **Python 3.10+**; Python 3.12 eignet sich als Ausgangspunkt. Installieren Sie Git zum Klonen oder laden Sie stattdessen die ZIP-Datei herunter und entpacken Sie sie. Führen Sie die folgenden Befehle im Terminal aus. Direkte Pfade zum Interpreter vermeiden Probleme bei der Aktivierung der Umgebung in der Shell.

<details>
<summary><strong>Windows · PowerShell</strong></summary>

```powershell
git clone https://github.com/ThreshoLdnnis/Quant-for-babies.git
cd Quant-for-babies
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

Wenn Sie eine ZIP-Datei heruntergeladen haben, öffnen Sie PowerShell im entpackten Repository-Ordner und beginnen Sie mit `python -m venv .venv`.

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

Wenn Sie eine ZIP-Datei heruntergeladen haben, öffnen Sie ein Terminal im entpackten Repository-Ordner und beginnen Sie mit `python3 -m venv .venv`.

</details>

Jupyter gibt eine lokale URL im Terminal aus. Öffnen Sie diese im Browser, wählen Sie `notebooks/phase1_intro/01_什么是量化金融.ipynb` und führen Sie die Zellen von oben nach unten aus (`Shift+Enter`). Prüfen Sie, ob das Notebook die gerade erstellte Umgebung verwendet.

| Abhängigkeiten | Zweck | Installationsquelle |
| --- | --- | --- |
| Jupyter, NumPy, pandas, Matplotlib, seaborn | Notebooks ausführen, Tabellen und Diagramme erstellen | [Abhängigkeiten im Stammverzeichnis](../../requirements.txt) |
| yfinance, AkShare | Beispiele mit Marktdaten; Netzwerkverbindung erforderlich | Abhängigkeiten im Stammverzeichnis |
| scikit-learn | Werkzeuge für maschinelles Lernen in der Lernumgebung | Abhängigkeiten im Stammverzeichnis; spätere KI-Kapitel sind noch geplant |
| Vorlesungsspezifische Abhängigkeiten | Offline-Forschungsübungen; Vorlesung 04 benötigt auch SciPy | `requirements.txt` im jeweiligen Vorlesungsordner |
| Optionale Diagrammpakete | Abbildungen aus den Übungen exportieren | `requirements-plot.txt` in Vorlesungen 03–05 |

<a id="curriculum"></a>
## 3. Arbeiten Sie die acht Notebooks durch

Gehen Sie innerhalb jeder Phase der Reihe nach vor. Speichern Sie Ihr Diagramm, den geänderten Parameter und eine kurze Erklärung des Ergebnisses.

| Kapitel | Thema / Notebook | Lernziel |
| :---: | --- | --- |
| 01 | [Was ist quantitative Finanzanalyse?](../../notebooks/phase1_intro/01_什么是量化金融.ipynb) | Ein intuitives Verständnis entwickeln und AAPL-Kursdaten herunterladen |
| 02 | [Ihr erstes quantitatives Experiment](../../notebooks/phase1_intro/02_你的第一个量化实验.ipynb) | OHLCV lesen, Renditen berechnen und Volatilität vergleichen |
| 03 | [Strategie mit gleitenden Durchschnitten](../../notebooks/phase1_intro/03_移动平均线策略.ipynb) | MA5/MA20-Kreuzungen in eine ausdrückliche Handelsregel übersetzen |
| 04 | [Backtest einer Strategie](../../notebooks/phase1_intro/04_策略回测.ipynb) | Handel simulieren und Kapitalentwicklung, Trefferquote und Drawdown untersuchen |
| 05 | [Volatilität verstehen](../../notebooks/phase2_intro/01_理解波动率.ipynb) | Volatilität verschiedener Anlagen messen und annualisieren |
| 06 | [Sharpe-Ratio und Beta](../../notebooks/phase2_intro/02_夏普比率与Beta.ipynb) | Risikobereinigte Renditen und Marktsensitivität vergleichen |
| 07 | [Maximaler Drawdown und Positionsgröße](../../notebooks/phase2_intro/03_最大回撤与仓位管理.ipynb) | Drawdown mit Exposure und Risikotoleranz in Beziehung setzen |
| 08 | [Portfolios und Korrelation](../../notebooks/phase2_intro/04_多标的组合与相关性.ipynb) | Ein gleichgewichtetes Portfolio aufbauen und Diversifikation untersuchen |

**Phase 1 · Kapitel 01–04:** Daten → Renditen → Regeln → Backtest.<br />
**Phase 2 · Kapitel 05–08:** Volatilität → risikobereinigte Kennzahlen → Positionsgröße → Portfolios.

<details>
<summary>Vorschau auf die ersten vier Kapitel</summary>

<p>
  <img src="../../assets/images/ch01_real_stock.png" alt="Kapitel 01: Marktdaten" width="46%" />
  <img src="../../assets/images/ch02_returns.png" alt="Kapitel 02: Renditen" width="46%" />
</p>
<p>
  <img src="../../assets/images/ch03_ma_signals.png" alt="Kapitel 03: Signale gleitender Durchschnitte" width="46%" />
  <img src="../../assets/images/ch04_backtest.png" alt="Kapitel 04: Backtest" width="46%" />
</p>

</details>

<a id="labs"></a>
## 4. Entwickeln Sie einen Forschungsablauf in fünf Vorlesungen

Die Vorlesungen ergänzen die Notebooks. Lesen Sie sie in der angegebenen Reihenfolge, um den Forschungsprozess zu durchlaufen. **Behalten Sie die vollständige Repository-Struktur bei:** Die Übungen 04 und 05 importieren Code aus Vorlesung 03.

| Vorlesung | Lesematerial | Praxis und erwartete Ergebnisse |
| :---: | --- | --- |
| 01 | [Forschungsablauf](../../extras/lecture-01/index.html) · [Vortragsnotizen](../../extras/lecture-01/lecture-notes.md) | Einführung mit 13 Folien; keine Python-Übung |
| 02 | [Finanzdaten-Engineering](../../extras/lecture-02/index.html) · [Anleitung](../../extras/lecture-02/README.md) | pandas, SQLite/SQL, Bereinigung und Quarantäne → CSV-Tabellen, Datenbank und Qualitätsberichte |
| 03 | [Faktoren und Vorverarbeitung](../../extras/lecture-03/index.html) · [Anleitung](../../extras/lecture-03/README.md) | MOM20, VOL20, TURN20, MAD und Querschnitts-Z-Scores → Faktortabellen und Diagnosen |
| 04 | [Faktorbewertung und Statistik](../../extras/lecture-04/index.html) · [Anleitung](../../extras/lecture-04/README.md) | Rank IC, ICIR, Gruppen und chronologische Bewertung → Bewertungstabellen und Prüfbericht |
| 05 | [Multifaktor-Backtesting](../../extras/lecture-05/index.html) · [Anleitung](../../extras/lecture-05/README.md) | Statische Scores, Top N, Ausführung zur nächsten Eröffnung und Kosten → simulierte Konten, Handelsbücher und Forschungszusammenfassungen |

### Die vier Offline-Übungen ausführen

Führen Sie die folgenden Befehle im Stammverzeichnis des Repositorys mit aktivierter virtueller Umgebung aus. Alternativ ersetzen Sie jedes `python` unter Windows durch `.\.venv\Scripts\python.exe` oder unter macOS/Linux durch `.venv/bin/python`.

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

Verwenden Sie für jede Übung ein eigenes Ausgabeverzeichnis. Die Skripte schützen fremde, nicht leere Verzeichnisse; lesen Sie die Vorlesungsanleitung, bevor Sie einen Ausgabepfad ändern oder erneut verwenden. Optionale Diagrammskripte und die AkShare-Übung zur Datenerfassung über das Netzwerk sind in den jeweiligen Vorlesungsordnern dokumentiert.

**Ergebnisse richtig einordnen:** Die Kernübungen verwenden deterministische **simulierte Lehrdaten** und benötigen nach der Installation der Abhängigkeiten keine Verbindung zu einem Marktdatenanbieter. Kurze Stichproben und hypothetische Kosten veranschaulichen die Methoden; sie belegen weder eine investierbare Strategie noch eine formelle Out-of-Sample-Performance. Die Notebooks können echte historische Kurse herunterladen. Einige Demos enthalten gespeicherte historische Datensätze; ihre Bedienelemente laden keine Echtzeitkurse.

<a id="demos"></a>
## 5. Erkunden Sie die Konzepte visuell

Laden Sie die HTML-Dateien herunter und öffnen Sie sie, oder verwenden Sie den oben beschriebenen lokalen Server. Die [Demo-Hinweise](../../assets/interactive/README.md) erläutern Daten und Funktionsweise.

| Demo | Passendes Kapitel | Probieren Sie Folgendes aus |
| --- | --- | --- |
| [Brownsche Bewegung / Zufallsbewegung](../../assets/interactive/brownian-random-walk.html) | Kapitel 01 | Pfade vergleichen und Zufall von einer Prognose unterscheiden |
| [Tagesrenditen](../../assets/interactive/daily-return-demo.html) | Kapitel 05 | Die Berechnung von Preisen zu Renditen nachvollziehen |
| [Stichproben-Standardabweichung](../../assets/interactive/std-dev-demo.html) | Kapitel 05 | Abweichungen und ihre Zusammenfassung untersuchen |
| [Varianz der Grundgesamtheit](../../assets/interactive/population-variance-demo.html) | Kapitel 05 | Die Definition mit einem visuellen Beispiel verbinden |
| [Varianzkorrektur](../../assets/interactive/variance-formulas-demo.html) | Kapitel 05 | Die Rolle von `n` und `n−1` vergleichen |
| [Sharpe-Ratio](../../assets/interactive/sharpe-ratio-demo.html) | Kapitel 06 | Überschussrendite und Volatilität vergleichen |
| [Beta](../../assets/interactive/beta-demo.html) | Kapitel 06 | Die Beziehung zwischen einer Anlage und einer Benchmark untersuchen |

<a id="roadmap"></a>
## 6. Erfahren Sie, was als Nächstes geplant ist

| Status | Umfang | Weitere Informationen |
| --- | --- | --- |
| Verfügbar | Acht Notebooks, fünf Vorlesungen, sieben Demos | Tabellen oben |
| Geplant · Kapitel 09–14 | ML-Einstieg, XGBoost, LSTM, Transformer, Multifaktor-Selektion und ein KI-Quant-System | [Detaillierte Roadmap](../ROADMAP.md) |
| Geplant · fortgeschrittene Projekte | Finanz-NLP/RAG-Assistent; marktregimeabhängige Faktorallokation; ML-Aktienauswahl und erklärbares Alpha | [Projektvorschläge](../ROADMAP.md#advanced-projects) |
| Im Aufbau | Wiederverwendbare Module in `src/` | Derzeit Platzhalter, kein produktionsreifes Backtesting-Framework |

### Orientierung im Repository

| Pfad | Inhalt |
| --- | --- |
| [`notebooks/`](../../notebooks/) | Lektionen der Phasen 1 und 2 |
| [`extras/`](../../extras/) | HTML-Vorlesungen, Anleitungen, Übungen und optionale Diagrammwerkzeuge |
| [`assets/interactive/`](../../assets/interactive/) | Sieben Browser-Demos |
| [`assets/images/`](../../assets/images/) | Kursabbildungen und README-Grafiken |
| [`docs/`](../) | Roadmap und mehrsprachige README-Leitfäden |
| [`scripts/`](../../scripts/) | Hilfsprogramme zur Notebook-Pflege und Abbildungserstellung |
| [`requirements.txt`](../../requirements.txt) | Abhängigkeiten der Notebook-Umgebung |

<a id="faq"></a>
## 7. Häufige Probleme lösen

| Frage | Vorgehen |
| --- | --- |
| Warum sehe ich auf GitHub HTML-Code? | Laden Sie die Datei herunter und öffnen Sie sie oder verwenden Sie den lokalen HTTP-Server unter [Hier beginnen](#start). |
| Warum fehlt ein Paket in Jupyter? | Installieren Sie es mit `python -m pip` derselben Umgebung; prüfen Sie den ausgewählten Kernel und starten Sie ihn nach der Installation neu. |
| Warum ist ein Marktdaten-Download fehlgeschlagen? | Prüfen Sie Ihre Netzwerkverbindung und die Antwort des Anbieters. Leere Daten sind kein erfolgreiches Experiment. Lernen Sie mit den Offline-Übungen weiter. |
| Warum lehnt eine Übung das Ausgabeverzeichnis ab? | Wählen Sie ein neues eigenes Verzeichnis oder befolgen Sie die Regeln der Vorlesung zum erneuten Ausführen im eigenen markierten Ausgabeverzeichnis. |
| Übersetzt der Sprachwechsel auch die Notebooks? | Nein. Es gibt zehn README-Leitfäden; die Lehrinhalte bleiben vorwiegend auf vereinfachtem Chinesisch. |
| Wie melde ich ein Problem? | [Erstellen Sie ein Issue](https://github.com/ThreshoLdnnis/Quant-for-babies/issues) mit Dateipfad, Befehl, Python-Version und Fehlermeldung. Entfernen Sie Tokens und persönliche Daten aus den Protokollen. |

Beiträge sind willkommen: Korrekturen, verständlichere Beispiele und sorgfältig geprüfte Übersetzungen. Halten Sie Codepfade und Befehle in allen zehn Leitfäden konsistent; siehe die [Hinweise zur Übersetzungspflege](README.md).

---

**Lizenz:** [MIT](../../LICENSE). **Lernzweck:** Dieses Repository dient dem Lernen und der Forschung und stellt keine Anlageberatung dar. Historische oder simulierte Ergebnisse garantieren keine künftige Wertentwicklung.
