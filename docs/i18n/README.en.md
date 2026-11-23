<p align="center">
  <img src="../../assets/images/readme-guide.svg" alt="Quant for babies — learn, experiment, explain" width="960" />
</p>

<p align="center">
  <a href="../../README.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <strong>English</strong> · <a href="README.ru.md">Русский</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.fr.md">Français</a> · <a href="README.de.md">Deutsch</a> · <a href="README.es.md">Español</a> · <a href="README.hi.md">हिन्दी</a>
</p>

# Quantitative finance, one experiment at a time

An approachable path from your first market dataset to signals, risk, portfolios and reproducible research. Learn with **8 Jupyter notebooks, 5 research lectures and 7 browser demos**.

**Language scope:** this guide and its navigation are available in ten languages. The notebooks, lectures and most supporting documents are currently in **Simplified Chinese**; switching this README does not translate the course content.

<p align="center">
  <a href="#start">Start here</a> · <a href="#setup">Setup</a> · <a href="#curriculum">Notebooks</a> · <a href="#labs">Research labs</a> · <a href="#demos">Demos</a> · <a href="#faq">Help</a>
</p>

| What is available | Format | What you can do |
| --- | --- | --- |
| Chapters 01–08 · available | Jupyter notebooks | Analyze prices, build a moving-average rule, measure risk and compare portfolios |
| Lectures 01–05 · available | Offline HTML + four Python labs | Follow data → factors → evaluation → simulated backtesting |
| Seven interactive demos · available | Standalone HTML | Explore formulas visually, without installing a research environment |
| Later chapters and advanced projects · planned | [Roadmap](../ROADMAP.md) | See proposed topics separately from delivered lessons |

<a id="start"></a>
## 1. Choose your starting point

| Your goal | Start with | First result |
| --- | --- | --- |
| Understand the ideas before coding | [Lecture 01](../../extras/lecture-01/index.html) and the [demos](#demos) | Explain the steps of a quantitative research workflow |
| Learn by writing and running Python | [Environment setup](#setup), then [Notebook 01](../../notebooks/phase1_intro/01_什么是量化金融.ipynb) | Load market data and draw your first price chart |
| Practice a complete research pipeline | [Lectures 02–05](#labs), in order | Produce data checks, factor tables, evaluation reports and a simulated trade ledger |
| Teach a workshop or study with a team | [Lecture 01 speaker notes](../../extras/lecture-01/lecture-notes.md) and the lab instructions | Lead a session with exercises and inspectable outputs |

You do not need prior quantitative finance experience. Basic Python helps with the notebooks; the HTML reading path can be used first. Follow **read → run → change one assumption → explain the result** for each lesson.

### Read the HTML lessons

**GitHub shows HTML source; a repository file link does not launch the lesson.** Download the repository using **Code → Download ZIP**, extract it, and open an `extras/lecture-0N/index.html` file in your browser. The five lecture pages and seven demos can be read locally offline. External references and live data downloads still require a connection.

Alternatively, from the repository root:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/extras/lecture-01/` (replace `01` with `02`–`05` for the other lectures). On macOS/Linux, use `python3` if `python` is unavailable. Stop the server with `Ctrl+C`.

Lecture 01: use arrow keys or Space to advance, `N` for speaker notes, `O` for overview and `F` for fullscreen.

<a id="setup"></a>
## 2. Set up your notebook environment

Use **Python 3.10+**; Python 3.12 is a reasonable starting point. Install Git to clone, or download and extract the ZIP instead. Run the commands below from a terminal. The direct environment paths avoid shell activation issues.

<details>
<summary><strong>Windows · PowerShell</strong></summary>

```powershell
git clone https://github.com/ThreshoLdnnis/Quant-for-babies.git
cd Quant-for-babies
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

If you downloaded a ZIP, open PowerShell in the extracted repository folder and start at `python -m venv .venv`.

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

If you downloaded a ZIP, open a terminal in the extracted repository folder and start at `python3 -m venv .venv`.

</details>

Jupyter prints a local URL in the terminal. Open it in your browser, choose `notebooks/phase1_intro/01_什么是量化金融.ipynb`, and run the cells from top to bottom (`Shift+Enter`). Confirm that the notebook uses the environment you just created.

| Dependency group | Purpose | Install from |
| --- | --- | --- |
| Jupyter, NumPy, pandas, Matplotlib, seaborn | Notebook execution, tables and charts | [Root requirements](../../requirements.txt) |
| yfinance, AkShare | Market-data examples; network required | Root requirements |
| scikit-learn | Machine-learning toolkit in the learning environment | Root requirements; later AI chapters remain planned |
| Per-lecture requirements | Offline research labs; Lecture 04 also needs SciPy | Each lecture folder's `requirements.txt` |
| Optional plotting packages | Export lab figures | `requirements-plot.txt` in Lectures 03–05 |

<a id="curriculum"></a>
## 3. Follow the eight-notebook path

Work in order within each phase. Save your chart, your changed parameter and a short explanation of what happened.

| Chapter | Topic / notebook | Learning outcome |
| :---: | --- | --- |
| 01 | [What is quantitative finance?](../../notebooks/phase1_intro/01_什么是量化金融.ipynb) | Build intuition and download AAPL price data |
| 02 | [Your first quantitative experiment](../../notebooks/phase1_intro/02_你的第一个量化实验.ipynb) | Read OHLCV, calculate returns and compare volatility |
| 03 | [Moving-average strategy](../../notebooks/phase1_intro/03_移动平均线策略.ipynb) | Turn MA5/MA20 crossovers into an explicit trading rule |
| 04 | [Strategy backtesting](../../notebooks/phase1_intro/04_策略回测.ipynb) | Simulate trades and inspect equity, win rate and drawdown |
| 05 | [Understanding volatility](../../notebooks/phase2_intro/01_理解波动率.ipynb) | Measure and annualize volatility across assets |
| 06 | [Sharpe ratio and Beta](../../notebooks/phase2_intro/02_夏普比率与Beta.ipynb) | Compare risk-adjusted returns and market sensitivity |
| 07 | [Maximum drawdown and position sizing](../../notebooks/phase2_intro/03_最大回撤与仓位管理.ipynb) | Relate drawdown to exposure and risk tolerance |
| 08 | [Portfolios and correlation](../../notebooks/phase2_intro/04_多标的组合与相关性.ipynb) | Build an equal-weight portfolio and explore diversification |

**Phase 1 · Chapters 01–04:** data → returns → rules → backtest.<br />
**Phase 2 · Chapters 05–08:** volatility → risk-adjusted metrics → sizing → portfolios.

<details>
<summary>Preview the first four chapters</summary>

<p>
  <img src="../../assets/images/ch01_real_stock.png" alt="Chapter 01: market data" width="46%" />
  <img src="../../assets/images/ch02_returns.png" alt="Chapter 02: returns" width="46%" />
</p>
<p>
  <img src="../../assets/images/ch03_ma_signals.png" alt="Chapter 03: moving-average signals" width="46%" />
  <img src="../../assets/images/ch04_backtest.png" alt="Chapter 04: backtest" width="46%" />
</p>

</details>

<a id="labs"></a>
## 4. Build a research workflow in five lectures

These lectures complement the notebooks. Read them in order for the research pipeline. **Keep the complete repository structure:** Labs 04 and 05 import code from Lecture 03.

| Lecture | Read | Practice and expected output |
| :---: | --- | --- |
| 01 | [Research workflow](../../extras/lecture-01/index.html) · [Speaker notes](../../extras/lecture-01/lecture-notes.md) | 13-slide introduction; no Python lab |
| 02 | [Financial data engineering](../../extras/lecture-02/index.html) · [Instructions](../../extras/lecture-02/README.md) | pandas, SQLite/SQL, cleaning and quarantine → CSV tables, a database and quality reports |
| 03 | [Factors and preprocessing](../../extras/lecture-03/index.html) · [Instructions](../../extras/lecture-03/README.md) | MOM20, VOL20, TURN20, MAD and cross-sectional Z-scores → factor tables and diagnostics |
| 04 | [Factor evaluation and statistics](../../extras/lecture-04/index.html) · [Instructions](../../extras/lecture-04/README.md) | Rank IC, ICIR, groups and chronological evaluation → evaluation tables and an audit report |
| 05 | [Multi-factor backtesting](../../extras/lecture-05/index.html) · [Instructions](../../extras/lecture-05/README.md) | Static scores, Top N, next-open execution and costs → simulated accounts, trade ledgers and research summaries |

### Run the four offline labs

From the repository root, with your virtual environment active, run the following. Alternatively, replace every `python` with `.\.venv\Scripts\python.exe` on Windows or `.venv/bin/python` on macOS/Linux.

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

Use a dedicated output directory for each lab. The scripts protect unrelated nonempty directories; consult the lecture instructions before changing or reusing an output path. Optional plotting scripts and the networked AkShare collection exercise are documented in their lecture folders.

**How to interpret the outputs:** the core labs use deterministic **simulated teaching data** and do not need a market-data connection after dependencies are installed. Short samples and hypothetical costs illustrate methods; they do not establish an investable strategy or formal out-of-sample performance. Notebook data downloads may use real historical prices. Some demos embed historical snapshots; their controls do not fetch live prices.

<a id="demos"></a>
## 5. Explore the concepts visually

Download and open the HTML files, or use the local server described above. [Demo notes](../../assets/interactive/README.md) explain their data and behavior.

| Demo | Best paired with | Try this |
| --- | --- | --- |
| [Brownian motion / random walk](../../assets/interactive/brownian-random-walk.html) | Chapter 01 | Compare paths and distinguish randomness from a forecast |
| [Daily returns](../../assets/interactive/daily-return-demo.html) | Chapter 05 | Follow the price-to-return calculation |
| [Sample standard deviation](../../assets/interactive/std-dev-demo.html) | Chapter 05 | Inspect deviations and their aggregation |
| [Population variance](../../assets/interactive/population-variance-demo.html) | Chapter 05 | Connect the definition to a visual example |
| [Variance correction](../../assets/interactive/variance-formulas-demo.html) | Chapter 05 | Compare the roles of `n` and `n−1` |
| [Sharpe ratio](../../assets/interactive/sharpe-ratio-demo.html) | Chapter 06 | Compare excess return with volatility |
| [Beta](../../assets/interactive/beta-demo.html) | Chapter 06 | Explore the relationship between an asset and a benchmark |

<a id="roadmap"></a>
## 6. Know what comes next

| Status | Scope | Where to look |
| --- | --- | --- |
| Available | Eight notebooks, five lectures, seven demos | The tables above |
| Planned · Chapters 09–14 | Introductory ML, XGBoost, LSTM, Transformer, multi-factor selection and an AI quant system | [Detailed roadmap](../ROADMAP.md) |
| Planned · advanced projects | Financial NLP/RAG assistant; regime-aware factor allocation; ML equity selection and explainable Alpha | [Project proposals](../ROADMAP.md#advanced-projects) |
| Under construction | Reusable modules in `src/` | Currently placeholders, not a production backtesting framework |

### Find your way around the repository

| Path | Contents |
| --- | --- |
| [`notebooks/`](../../notebooks/) | Phase 1 and Phase 2 lessons |
| [`extras/`](../../extras/) | Lecture HTML, instructions, labs and optional plotting tools |
| [`assets/interactive/`](../../assets/interactive/) | Seven browser demos |
| [`assets/images/`](../../assets/images/) | Course illustrations and README graphics |
| [`docs/`](../) | Roadmap and multilingual README guides |
| [`scripts/`](../../scripts/) | Notebook maintenance and illustration-generation utilities |
| [`requirements.txt`](../../requirements.txt) | Notebook environment dependencies |

<a id="faq"></a>
## 7. Get unstuck

| Question | What to do |
| --- | --- |
| Why do I see HTML code on GitHub? | Download and open the file, or use the local HTTP server in [Start here](#start). |
| Why is a package missing in Jupyter? | Install it with the same environment's `python -m pip`; check the selected kernel and restart it after installation. |
| Why did a market-data download fail? | Check your network and the provider's response. Do not treat empty data as a successful experiment. Use the offline lecture labs to continue learning. |
| Why did a lab refuse the output directory? | Choose a fresh dedicated directory, or follow that lecture's rules for rerunning its own marked output. |
| Does switching language translate the notebooks? | No. Ten README guides are provided; the teaching content remains primarily Simplified Chinese. |
| How do I report a problem? | [Open an issue](https://github.com/ThreshoLdnnis/Quant-for-babies/issues) with the file path, command, Python version and error message. Remove tokens and personal information from logs. |

Contributions are welcome: fixes, clearer examples and carefully reviewed translations. Keep code paths and commands consistent across the ten guides; see the [translation maintenance notes](README.md).

---

**License:** [MIT](../../LICENSE). **Educational use:** this repository is for learning and research, not investment advice. Historical or simulated results do not guarantee future performance.
