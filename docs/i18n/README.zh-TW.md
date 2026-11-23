<p align="center">
  <img src="../../assets/images/readme-guide.svg" alt="Quant for babies — 學習、實驗、解釋" width="960" />
</p>

<p align="center">
  <a href="../../README.md">简体中文</a> · <strong>繁體中文</strong> · <a href="README.en.md">English</a> · <a href="README.ru.md">Русский</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.fr.md">Français</a> · <a href="README.de.md">Deutsch</a> · <a href="README.es.md">Español</a> · <a href="README.hi.md">हिन्दी</a>
</p>

# 透過一次次實驗，學會量化金融

從第一份市場資料開始，逐步理解訊號、風險、投資組合與可重現的研究。透過 <strong>8 份 Jupyter Notebook、5 講研究課程與 7 個瀏覽器互動示範</strong>，循序入門。

<strong>語言範圍：</strong> 本指南與導覽提供十種語言。Notebook、課程及大部分配套文件目前以<strong>簡體中文</strong>為主；切換 README 語言不會翻譯課程正文。

<p align="center">
  <a href="#start">從這裡開始</a> · <a href="#setup">環境設定</a> · <a href="#curriculum">Notebook 課程</a> · <a href="#labs">研究實作</a> · <a href="#demos">互動示範</a> · <a href="#faq">常見問題</a>
</p>

| 已提供的內容 | 形式 | 你可以完成 |
| --- | --- | --- |
| 第 01–08 章 · 已提供 | Jupyter Notebook | 分析價格、建立移動平均線規則、衡量風險及比較投資組合 |
| 第 01–05 講 · 已提供 | 離線 HTML + 四個 Python 實作 | 走完資料 → 因子 → 評估 → 模擬回測流程 |
| 七個互動示範 · 已提供 | 獨立 HTML | 透過視覺化理解公式，無需安裝研究環境 |
| 後續章節與進階專案 · 規劃中 | [路線圖](../ROADMAP.md) | 清楚區分預定主題與已完成課程 |

<a id="start"></a>
## 1. 選擇你的起點

| 你的目標 | 從哪裡開始 | 第一項成果 |
| --- | --- | --- |
| 寫程式前先理解概念 | [第 01 講](../../extras/lecture-01/index.html)與[互動示範](#demos) | 能說明量化研究流程的各個步驟 |
| 透過編寫與執行 Python 學習 | [設定環境](#setup)，再開啟[第 01 份 Notebook](../../notebooks/phase1_intro/01_什么是量化金融.ipynb) | 載入市場資料，畫出第一張價格圖 |
| 練習完整研究流程 | 依序學習[第 02–05 講](#labs) | 產出資料檢查、因子表、評估報告與模擬交易帳本 |
| 帶領工作坊或團隊共學 | [第 01 講講者備註](../../extras/lecture-01/lecture-notes.md)及實作說明 | 帶領包含練習與可檢查成果的學習活動 |

不需要量化金融經驗。基礎 Python 有助於學習 Notebook；也可以先從 HTML 閱讀路線開始。每一課都遵循 <strong>閱讀 → 執行 → 改變一項假設 → 解釋結果</strong>。

### 閱讀 HTML 課程

<strong>GitHub 會顯示 HTML 原始碼；點擊儲存庫檔案連結不會啟動課程。</strong> 請透過 <strong>Code → Download ZIP</strong> 下載儲存庫，解壓縮後，在瀏覽器開啟 `extras/lecture-0N/index.html`。五講課程頁面與七個示範均可在本機離線閱讀；外部參考連結與即時資料下載仍需連網。

也可以在儲存庫根目錄執行：

```bash
python -m http.server 8000 --bind 127.0.0.1
```

開啟 `http://127.0.0.1:8000/extras/lecture-01/`（其他課程請將 `01` 換成 `02`–`05`）。macOS/Linux 若無 `python` 指令，請使用 `python3`。按 `Ctrl+C` 停止伺服器。

第 01 講：使用方向鍵或空白鍵翻頁，`N` 顯示講者備註，`O` 開啟總覽，`F` 切換全螢幕。

<a id="setup"></a>
## 2. 設定 Notebook 環境

使用 <strong>Python 3.10+</strong>；Python 3.12 適合作為起點。安裝 Git 後即可複製儲存庫，或直接下載並解壓縮 ZIP。請在終端機執行以下指令。直接指定虛擬環境路徑，可避開 Shell 啟用環境時的問題。

<details>
<summary><strong>Windows · PowerShell</strong></summary>

```powershell
git clone https://github.com/ThreshoLdnnis/Quant-for-babies.git
cd Quant-for-babies
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

若使用 ZIP，請在解壓縮後的儲存庫資料夾開啟 PowerShell，從 `python -m venv .venv` 開始執行。

</details>

<details>
<summary><strong>macOS / Linux · 終端機</strong></summary>

```bash
git clone https://github.com/ThreshoLdnnis/Quant-for-babies.git
cd Quant-for-babies
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyterlab
```

若使用 ZIP，請在解壓縮後的儲存庫資料夾開啟終端機，從 `python3 -m venv .venv` 開始執行。

</details>

Jupyter 會在終端機顯示本機網址。於瀏覽器開啟該網址，選擇 `notebooks/phase1_intro/01_什么是量化金融.ipynb`，由上至下執行儲存格（`Shift+Enter`）。請確認 Notebook 使用剛建立的環境。

| 相依套件群組 | 用途 | 安裝來源 |
| --- | --- | --- |
| Jupyter、NumPy、pandas、Matplotlib、seaborn | 執行 Notebook、製作表格與圖表 | [根目錄相依套件清單](../../requirements.txt) |
| yfinance、AkShare | 市場資料範例；需要網路 | 根目錄相依套件清單 |
| scikit-learn | 學習環境中的機器學習工具 | 根目錄相依套件清單；後續 AI 章節仍在規劃中 |
| 各講相依套件 | 離線研究實作；第 04 講另需 SciPy | 各講資料夾的 `requirements.txt` |
| 選用繪圖套件 | 匯出實作圖表 | 第 03–05 講的 `requirements-plot.txt` |

<a id="curriculum"></a>
## 3. 依序學習八份 Notebook

請在每一期中依序學習。保留你的圖表、修改過的參數，以及對結果的簡短解釋。

| 章節 | 主題／Notebook | 學習成果 |
| :---: | --- | --- |
| 01 | [什麼是量化金融？](../../notebooks/phase1_intro/01_什么是量化金融.ipynb) | 建立量化直覺並下載 AAPL 價格資料 |
| 02 | [你的第一個量化實驗](../../notebooks/phase1_intro/02_你的第一个量化实验.ipynb) | 理解 OHLCV、計算報酬率並比較波動率 |
| 03 | [移動平均線策略](../../notebooks/phase1_intro/03_移动平均线策略.ipynb) | 將 MA5/MA20 交叉轉為明確的交易規則 |
| 04 | [策略回測](../../notebooks/phase1_intro/04_策略回测.ipynb) | 模擬交易，檢查淨值、勝率與回撤 |
| 05 | [理解波動率](../../notebooks/phase2_intro/01_理解波动率.ipynb) | 衡量不同資產的波動率並進行年化換算 |
| 06 | [夏普比率與 Beta](../../notebooks/phase2_intro/02_夏普比率与Beta.ipynb) | 比較風險調整後報酬與市場敏感度 |
| 07 | [最大回撤與部位管理](../../notebooks/phase2_intro/03_最大回撤与仓位管理.ipynb) | 理解回撤、曝險與風險承受度之間的關係 |
| 08 | [投資組合與相關性](../../notebooks/phase2_intro/04_多标的组合与相关性.ipynb) | 建立等權重投資組合並探索分散化 |

<strong>第一期 · 第 01–04 章：</strong> 資料 → 報酬率 → 規則 → 回測。<br />
<strong>第二期 · 第 05–08 章：</strong> 波動率 → 風險調整指標 → 部位管理 → 投資組合。

<details>
<summary>預覽前四章</summary>

<p>
  <img src="../../assets/images/ch01_real_stock.png" alt="第 01 章：市場資料" width="46%" />
  <img src="../../assets/images/ch02_returns.png" alt="第 02 章：報酬率" width="46%" />
</p>
<p>
  <img src="../../assets/images/ch03_ma_signals.png" alt="第 03 章：移動平均線訊號" width="46%" />
  <img src="../../assets/images/ch04_backtest.png" alt="第 04 章：回測" width="46%" />
</p>

</details>

<a id="labs"></a>
## 4. 透過五講課程建立研究流程

這些課程補充 Notebook 的內容。請依序閱讀，理解完整研究流程。<strong>保留完整儲存庫結構：</strong> 第 04、05 講的實作會匯入第 03 講的程式碼。

| 講次 | 閱讀內容 | 實作與預期產出 |
| :---: | --- | --- |
| 01 | [研究流程](../../extras/lecture-01/index.html) · [講者備註](../../extras/lecture-01/lecture-notes.md) | 13 頁入門投影片；無 Python 實作 |
| 02 | [金融資料工程](../../extras/lecture-02/index.html) · [執行說明](../../extras/lecture-02/README.md) | pandas、SQLite/SQL、清理與異常資料隔離 → CSV 表格、資料庫與品質報告 |
| 03 | [因子與預處理](../../extras/lecture-03/index.html) · [執行說明](../../extras/lecture-03/README.md) | MOM20、VOL20、TURN20、MAD 與橫斷面 Z 分數 → 因子表與診斷結果 |
| 04 | [因子評估與統計](../../extras/lecture-04/index.html) · [執行說明](../../extras/lecture-04/README.md) | Rank IC、ICIR、分組與時間順序評估 → 評估表與稽核報告 |
| 05 | [多因子回測](../../extras/lecture-05/index.html) · [執行說明](../../extras/lecture-05/README.md) | 靜態評分、Top N、下一開盤執行與成本 → 模擬帳戶、交易帳本與研究摘要 |

### 執行四個離線實作

啟用虛擬環境後，在儲存庫根目錄執行以下指令。也可以將每個 `python` 換成 Windows 的 `.\.venv\Scripts\python.exe`，或 macOS/Linux 的 `.venv/bin/python`。

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

每個實作請使用獨立的輸出目錄。腳本會保護不屬於該實作的非空目錄；變更或重用輸出路徑前，請閱讀該講說明。選用繪圖腳本與需連網的 AkShare 資料擷取練習，均記載於各講資料夾。

<strong>如何理解產出：</strong> 核心實作使用確定性的<strong>模擬教學資料</strong>，安裝相依套件後不需要連接市場資料服務。短樣本與假設成本用來說明方法，無法證明策略可實際投資或具備正式樣本外績效。Notebook 下載的資料可能是真實歷史價格；部分示範內嵌歷史快照，操作控制項不會取得即時行情。

<a id="demos"></a>
## 5. 透過視覺化探索概念

下載並開啟 HTML 檔案，或使用上文的本機伺服器。[示範說明](../../assets/interactive/README.md)介紹各示範的資料與操作方式。

| 示範 | 建議搭配 | 試著這樣做 |
| --- | --- | --- |
| [布朗運動／隨機漫步](../../assets/interactive/brownian-random-walk.html) | 第 01 章 | 比較不同路徑，區分隨機性與預測 |
| [日報酬率](../../assets/interactive/daily-return-demo.html) | 第 05 章 | 逐步理解價格如何轉為報酬率 |
| [樣本標準差](../../assets/interactive/std-dev-demo.html) | 第 05 章 | 觀察偏差與彙總過程 |
| [母體變異數](../../assets/interactive/population-variance-demo.html) | 第 05 章 | 將定義與視覺化範例連結 |
| [變異數修正](../../assets/interactive/variance-formulas-demo.html) | 第 05 章 | 比較 `n` 與 `n−1` 的作用 |
| [夏普比率](../../assets/interactive/sharpe-ratio-demo.html) | 第 06 章 | 比較超額報酬與波動率 |
| [Beta](../../assets/interactive/beta-demo.html) | 第 06 章 | 探索資產與基準之間的關係 |

<a id="roadmap"></a>
## 6. 了解後續內容

| 狀態 | 範圍 | 查看位置 |
| --- | --- | --- |
| 已提供 | 八份 Notebook、五講課程、七個示範 | 上方表格 |
| 規劃中 · 第 09–14 章 | 機器學習入門、XGBoost、LSTM、Transformer、多因子選股與 AI 量化系統 | [詳細路線圖](../ROADMAP.md) |
| 規劃中 · 進階專案 | 金融 NLP/RAG 助手；市場狀態感知因子配置；機器學習選股與可解釋 Alpha | [專案提案](../ROADMAP.md#advanced-projects) |
| 建置中 | `src/` 中的可重用模組 | 目前為預留結構，尚非可供正式使用的回測框架 |

### 認識儲存庫結構

| 路徑 | 內容 |
| --- | --- |
| [`notebooks/`](../../notebooks/) | 第一期與第二期課程 |
| [`extras/`](../../extras/) | 課程 HTML、說明、實作與選用繪圖工具 |
| [`assets/interactive/`](../../assets/interactive/) | 七個瀏覽器示範 |
| [`assets/images/`](../../assets/images/) | 課程插圖與 README 圖片 |
| [`docs/`](../) | 路線圖與多語 README 指南 |
| [`scripts/`](../../scripts/) | Notebook 維護與插圖產生工具 |
| [`requirements.txt`](../../requirements.txt) | Notebook 環境相依套件 |

<a id="faq"></a>
## 7. 排除常見問題

| 問題 | 處理方式 |
| --- | --- |
| 為什麼 GitHub 顯示 HTML 程式碼？ | 下載後開啟檔案，或使用[從這裡開始](#start)介紹的本機 HTTP 伺服器。 |
| 為什麼 Jupyter 顯示缺少套件？ | 使用同一環境的 `python -m pip` 安裝；檢查選取的核心，並在安裝後重新啟動核心。 |
| 為什麼市場資料下載失敗？ | 檢查網路與資料供應商回應。空資料不代表實驗成功；可以先透過離線課程實作繼續學習。 |
| 為什麼實作拒絕使用輸出目錄？ | 選擇全新專用目錄，或依照該講規則重新執行有歸屬標記的輸出目錄。 |
| 切換語言會翻譯 Notebook 嗎？ | 不會。目前提供十種 README 指南，教學正文仍以簡體中文為主。 |
| 如何回報問題？ | [建立 Issue](https://github.com/ThreshoLdnnis/Quant-for-babies/issues)，附上檔案路徑、指令、Python 版本與錯誤訊息。請先移除紀錄中的權杖及個人資訊。 |

歡迎貢獻修正、更清楚的範例與經仔細審閱的翻譯。請讓十種指南的程式路徑與指令保持一致；詳見[翻譯維護說明](README.md)。

---

<strong>授權：</strong> [MIT](../../LICENSE)。<strong>教學用途：</strong> 本儲存庫供學習與研究使用，不構成投資建議。歷史或模擬結果不保證未來績效。
