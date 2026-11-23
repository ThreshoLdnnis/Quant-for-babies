<p align="center">
  <img src="assets/images/readme-guide.svg" alt="Quant for babies — 理解概念，运行实验，解释结果" width="960" />
</p>

<p align="center">
  <strong>简体中文</strong> · <a href="docs/i18n/README.zh-TW.md">繁體中文</a> · <a href="docs/i18n/README.en.md">English</a> · <a href="docs/i18n/README.ru.md">Русский</a> · <a href="docs/i18n/README.ja.md">日本語</a> · <a href="docs/i18n/README.ko.md">한국어</a> · <a href="docs/i18n/README.fr.md">Français</a> · <a href="docs/i18n/README.de.md">Deutsch</a> · <a href="docs/i18n/README.es.md">Español</a> · <a href="docs/i18n/README.hi.md">हिन्दी</a>
</p>

# 从第一个实验，走进量化金融

从一份行情数据出发，逐步理解交易信号、风险、组合与可复现研究。用 **8 个 Jupyter Notebook、5 讲研究专题、7 个浏览器交互演示**，把概念变成可以运行、观察和解释的结果。

**语言说明：**本指南与导航提供十种语言版本。Notebook、专题课和多数配套文档目前主要使用**简体中文**；切换 README 语言不会翻译课程正文。

<p align="center">
  <a href="#start">从这里开始</a> · <a href="#setup">环境准备</a> · <a href="#curriculum">Notebook 课程</a> · <a href="#labs">研究实操</a> · <a href="#demos">交互演示</a> · <a href="#faq">常见问题</a>
</p>

| 当前内容 | 形式 | 你可以完成什么 |
| --- | --- | --- |
| 第 01–08 章 · 已提供 | Jupyter Notebook | 分析行情、构建均线规则、度量风险、比较组合 |
| 第 01–05 讲 · 已提供 | 离线 HTML + 四套 Python 实操 | 走通数据 → 因子 → 检验 → 模拟回测 |
| 七个交互演示 · 已提供 | 独立 HTML | 不安装研究环境，也能直观理解公式 |
| 后续章节与进阶项目 · 规划中 | [详细路线图](docs/ROADMAP.md) | 查看后续方向，区分规划与已有内容 |

<a id="start"></a>
## 1. 先选一个适合你的入口

| 你的目标 | 从哪里开始 | 第一个成果 |
| --- | --- | --- |
| 先理解概念，再考虑编程 | [第一讲](extras/lecture-01/index.html)与[交互演示](#demos) | 能讲清量化研究的基本流程 |
| 边写 Python 边学习 | [配置环境](#setup)，再打开[第 01 章](notebooks/phase1_intro/01_什么是量化金融.ipynb) | 读取行情并画出第一张价格图 |
| 练习完整研究流程 | 按顺序学习[第 02–05 讲](#labs) | 得到数据检查、因子表、评价报告和模拟交易账本 |
| 带团队学习或组织工作坊 | [第一讲逐页讲者备注](extras/lecture-01/lecture-notes.md)与各讲实操说明 | 组织有练习、有可核验成果的学习活动 |

不要求量化金融基础。运行 Notebook 时，了解基本 Python 语法会更顺利；也可以先从 HTML 课件读起。每次按 **阅读 → 运行 → 改一个假设 → 解释结果** 的顺序学习。

### 怎样打开 HTML 课件？

**GitHub 的 HTML 文件页展示源码，点击仓库链接不会直接运行课件。** 通过 **Code → Download ZIP** 下载仓库并解压，在浏览器中打开 `extras/lecture-0N/index.html`。五讲课件和七个演示均可本地离线阅读；外部参考链接与实时数据下载仍需联网。

也可以在仓库根目录运行：

```bash
python -m http.server 8000 --bind 127.0.0.1
```

浏览器访问 `http://127.0.0.1:8000/extras/lecture-01/`，把 `01` 换成 `02`–`05` 即可打开其他课件。macOS/Linux 若没有 `python` 命令，请使用 `python3`。按 `Ctrl+C` 停止服务。

第一讲快捷键：方向键或空格翻页，`N` 查看讲者备注，`O` 打开总览，`F` 进入全屏。

<a id="setup"></a>
## 2. 配好 Notebook 学习环境

使用 **Python 3.10+**，可优先选择 Python 3.12。克隆需要安装 Git；也可以下载 ZIP 后解压。以下命令在终端运行，直接使用虚拟环境的解释器路径，避免激活脚本带来的问题。

<details>
<summary><strong>Windows · PowerShell</strong></summary>

```powershell
git clone https://github.com/ThreshoLdnnis/Quant-for-babies.git
cd Quant-for-babies
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

如果使用 ZIP，请在解压后的仓库文件夹中打开 PowerShell，从 `python -m venv .venv` 开始。

</details>

<details>
<summary><strong>macOS / Linux · 终端</strong></summary>

```bash
git clone https://github.com/ThreshoLdnnis/Quant-for-babies.git
cd Quant-for-babies
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyterlab
```

如果使用 ZIP，请在解压后的仓库文件夹中打开终端，从 `python3 -m venv .venv` 开始。

</details>

Jupyter 启动后会在终端显示本地网址。在浏览器打开它，选择 `notebooks/phase1_intro/01_什么是量化金融.ipynb`，用 `Shift+Enter` 从上到下执行单元格。确认 Notebook 使用的是刚创建的环境。

| 依赖分组 | 用途 | 安装入口 |
| --- | --- | --- |
| Jupyter、NumPy、pandas、Matplotlib、seaborn | 运行 Notebook、处理表格和绘图 | [根目录 requirements](requirements.txt) |
| yfinance、AkShare | 行情示例；下载数据需要联网 | 根目录 requirements |
| scikit-learn | 学习环境中的机器学习工具 | 根目录 requirements；后续 AI 章节仍在规划中 |
| 各讲独立依赖 | 离线研究实验；第四讲还需 SciPy | 各讲文件夹的 `requirements.txt` |
| 可选绘图依赖 | 导出研究图表 | 第 03–05 讲的 `requirements-plot.txt` |

<a id="curriculum"></a>
## 3. 按顺序完成八章 Notebook

各期内部按顺序学习。每章留下三样东西：**一张结果图、一个改过的参数、一段自己的解释**。

| 章节 | 主题 / Notebook | 你将学会 |
| :---: | --- | --- |
| 01 | [什么是量化金融](notebooks/phase1_intro/01_什么是量化金融.ipynb) | 建立量化直觉，下载 AAPL 价格数据 |
| 02 | [你的第一个量化实验](notebooks/phase1_intro/02_你的第一个量化实验.ipynb) | 认识 OHLCV、计算收益率、比较波动 |
| 03 | [移动平均线策略](notebooks/phase1_intro/03_移动平均线策略.ipynb) | 将 MA5/MA20 交叉变成明确的交易规则 |
| 04 | [策略回测](notebooks/phase1_intro/04_策略回测.ipynb) | 模拟交易，观察净值、胜率和回撤 |
| 05 | [理解波动率](notebooks/phase2_intro/01_理解波动率.ipynb) | 度量与年化波动率，比较不同标的 |
| 06 | [夏普比率与 Beta](notebooks/phase2_intro/02_夏普比率与Beta.ipynb) | 理解风险调整收益与市场敏感度 |
| 07 | [最大回撤与仓位管理](notebooks/phase2_intro/03_最大回撤与仓位管理.ipynb) | 联系回撤、资金敞口与风险承受能力 |
| 08 | [多标的组合与相关性](notebooks/phase2_intro/04_多标的组合与相关性.ipynb) | 构建等权组合，理解相关性与分散化 |

**第一期 · 第 01–04 章：**行情 → 收益 → 规则 → 回测。<br />
**第二期 · 第 05–08 章：**波动 → 风险调整指标 → 仓位 → 组合。

<details>
<summary>预览前四章的结果图</summary>

<p>
  <img src="assets/images/ch01_real_stock.png" alt="第一章：行情数据" width="46%" />
  <img src="assets/images/ch02_returns.png" alt="第二章：收益率" width="46%" />
</p>
<p>
  <img src="assets/images/ch03_ma_signals.png" alt="第三章：均线信号" width="46%" />
  <img src="assets/images/ch04_backtest.png" alt="第四章：回测" width="46%" />
</p>

</details>

<a id="labs"></a>
## 4. 用五讲专题串起研究流程

专题课与 Notebook 相互补充，按顺序学习可以走通研究流程。**请保留完整仓库结构：**第四、第五讲的实验会导入第三讲代码。

| 讲次 | 阅读材料 | 实操与预期成果 |
| :---: | --- | --- |
| 01 | [量化研究完整流程](extras/lecture-01/index.html) · [讲者备注](extras/lecture-01/lecture-notes.md) | 13 页入门幻灯片；本讲没有 Python 实验 |
| 02 | [金融数据工程](extras/lecture-02/index.html) · [运行说明](extras/lecture-02/README.md) | pandas、SQLite/SQL、清洗与隔离 → CSV 表、数据库、质量报告 |
| 03 | [因子构建与预处理](extras/lecture-03/index.html) · [运行说明](extras/lecture-03/README.md) | MOM20、VOL20、TURN20、MAD、横截面 Z-score → 因子表与诊断结果 |
| 04 | [因子检验与基础统计](extras/lecture-04/index.html) · [运行说明](extras/lecture-04/README.md) | Rank IC、ICIR、分组、时间顺序评价 → 评价表与审计报告 |
| 05 | [多因子策略与回测](extras/lecture-05/index.html) · [运行说明](extras/lecture-05/README.md) | 静态评分、Top N、下一开盘执行、成本 → 模拟账户、交易账本与研究汇总 |

### 运行四套离线实操

在仓库根目录、虚拟环境已激活时运行以下命令。也可以将所有 `python` 替换为 Windows 的 `.\.venv\Scripts\python.exe`，或 macOS/Linux 的 `.venv/bin/python`。

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

每讲使用独立的输出目录。脚本会保护不属于该实验的非空目录；更换或复用路径前，请先阅读该讲说明。可选绘图工具、AkShare 联网采集练习也在各讲文档中。

**怎样理解实验结果：**核心实操使用确定性的**模拟教学数据**，安装依赖后无需行情连接。短样本和假设成本用于说明方法，不能据此认定策略可投资或已完成正式样本外验证。Notebook 的数据下载可能使用真实历史价格；部分交互演示内置历史快照，操作控件不会获取实时行情。

<a id="demos"></a>
## 5. 用交互演示理解公式

下载后用浏览器打开 HTML，或使用前文的本地服务。[演示说明](assets/interactive/README.md)介绍了各页的数据与交互方式。

| 演示 | 配合章节 | 建议观察 |
| --- | --- | --- |
| [布朗运动与随机游走](assets/interactive/brownian-random-walk.html) | 第 01 章 | 比较不同路径，区分随机性与预测 |
| [日收益率](assets/interactive/daily-return-demo.html) | 第 05 章 | 跟着价格变化计算收益率 |
| [样本标准差](assets/interactive/std-dev-demo.html) | 第 05 章 | 观察离差怎样汇总为波动 |
| [总体方差](assets/interactive/population-variance-demo.html) | 第 05 章 | 将定义与图形对应起来 |
| [方差修正公式](assets/interactive/variance-formulas-demo.html) | 第 05 章 | 比较 `n` 与 `n−1` 的作用 |
| [夏普比率](assets/interactive/sharpe-ratio-demo.html) | 第 06 章 | 对照超额收益与波动率 |
| [Beta](assets/interactive/beta-demo.html) | 第 06 章 | 观察标的与基准之间的关系 |

<a id="roadmap"></a>
## 6. 分清已有内容与后续规划

| 状态 | 内容 | 入口 |
| --- | --- | --- |
| 已提供 | 八章 Notebook、五讲专题、七个演示 | 上方课程与实操表格 |
| 规划中 · 第 09–14 章 | 机器学习入门、XGBoost、LSTM、Transformer、多因子选股、AI 量化系统 | [详细路线图](docs/ROADMAP.md) |
| 规划中 · 进阶项目 | 金融 NLP/RAG 助手、市场状态动态配置、机器学习选股与可解释 Alpha | [项目规划](docs/ROADMAP.md#advanced-projects) |
| 建设中 | `src/` 中的可复用模块 | 当前为占位目录，尚非生产级回测框架 |

### 快速认识仓库目录

| 路径 | 内容 |
| --- | --- |
| [`notebooks/`](notebooks/) | 第一期与第二期课程 |
| [`extras/`](extras/) | 专题 HTML、说明、实操与可选绘图工具 |
| [`assets/interactive/`](assets/interactive/) | 七个浏览器演示 |
| [`assets/images/`](assets/images/) | 课程插图与 README 配图 |
| [`docs/`](docs/) | 路线图与多语言 README |
| [`scripts/`](scripts/) | Notebook 维护与配图生成工具 |
| [`requirements.txt`](requirements.txt) | Notebook 环境依赖 |

<a id="faq"></a>
## 7. 遇到问题时

| 问题 | 处理方法 |
| --- | --- |
| 点击 HTML 为什么只看到代码？ | 下载后打开文件，或按[入门说明](#start)启动本地 HTTP 服务。 |
| Jupyter 提示缺少模块？ | 用同一个环境的 `python -m pip` 安装，检查所选内核，安装后重启内核。 |
| 行情下载失败怎么办？ | 检查网络与数据源响应，不要把空数据视为成功实验；可先用离线专题实操继续学习。 |
| 实验为什么拒绝输出目录？ | 选择新的独立目录，或按该讲要求复用实验自己带标记的输出目录。 |
| 切换语言会翻译 Notebook 吗？ | 不会。目前提供十种语言的 README，课程正文仍主要是简体中文。 |
| 怎样反馈错误？ | [提交 Issue](https://github.com/ThreshoLdnnis/Quant-for-babies/issues)，附文件路径、运行命令、Python 版本和报错信息；日志中请移除令牌与个人信息。 |

欢迎贡献修正、更清楚的示例与经过核对的翻译。更新时请同步十种指南的路径和命令，参见[翻译维护说明](docs/i18n/README.md)。

---

**许可：**[MIT](LICENSE)。**学习用途：**本仓库仅供学习与研究，不构成投资建议。历史或模拟结果不保证未来表现。
