# 番外期·第二讲：Python、pandas与SQL金融数据工程

[打开长篇 HTML 课程](index.html) · [第一讲](../lecture-01/index.html) · [仓库目录](../../README.md)

本讲面向零基础本科生，采用连续纵向阅读的课程页面。包含数据工程价值、OHLCV字段字典、原始价与复权价、真实分红事件、AkShare采集、读取检查、清洗、pandas、SQLite/SQL、完整实操、质量验收、练习答案与课后任务。

## 阅读页面

下载整个仓库后打开 `extras/lecture-02/index.html`。请保留同目录的 `course.css` 和 `course.js`。课程文字、公式和SVG图表不依赖联网；代码复制、阅读进度、章节定位和均线窗口切换需要启用JavaScript。支持桌面侧栏、手机折叠目录、键盘操作与打印。

GitHub文件页面展示的是源码；下载后在浏览器打开，或在仓库根目录运行：

```bash
python -m http.server 8000 --bind 127.0.0.1
```

然后访问 `http://127.0.0.1:8000/extras/lecture-02/`。仓库当前未启用GitHub Pages，文件链接不等同于已经托管的在线站点。

## 必做：离线实验

要求 Python 3.10+。在仓库根目录执行：

```bash
python -m venv .venv
# Windows
.venv\Scripts\python -m pip install -r extras/lecture-02/requirements.txt
.venv\Scripts\python extras/lecture-02/lab.py --output work/lecture-02-run
```

macOS / Linux 将解释器换为 `.venv/bin/python`。若已使用正确的课程环境，也可直接 `python extras/lecture-02/lab.py --output work/lecture-02-run`。

**所有数据均为确定性模拟**，SIM001、SIM002、SIM003为虚构证券。日期是40个pandas工作日，不是真实A股交易日历。实验注入乱序、完全重复、冲突重复、日期错误、缺失、非法OHLC与负成交量。固定输入应得到：81条原始记录、73条干净记录、8条隔离记录；精确重复1条、冲突键2条、其他错误5条。缺少的7个模拟网格记录中，1个为已明确设定的模拟停牌，6个为未决数据缺口。

输出包括：

| 文件 | 用途 |
|---|---|
| `raw_simulated.csv` | 保留原始模拟输入与原始行号 |
| `clean_simulated.csv` | 已排序、主键唯一的原始价模拟行情 |
| `quarantine_simulated.csv` | 隔离记录、原因及可回查行号 |
| `features_simulated.csv` | 上一观测、观测间价格收益、MA5/MA20与历史特征 |
| `research_simulated.sqlite` | `prices`、`securities`及约束/索引 |
| `quality_report.json` | 对账、缺口、版本与检查结果 |
| `queries.sql` / `sql_results.json` | 查询与实际运行结果 |

脚本拒绝覆盖不属于本实验的非空目录；只对带本实验标记的目录重跑。默认输出为 `data/processed/lecture-02-simulation`，建议显式使用 `--output`。不要把真实数据放入实验输出目录。生成物不需要提交GitHub。

`return_observed` 是上一有效观测间的**价格收益**，不含分红与成本。整数rolling窗口按有效观测计数，缺口下不等于固定交易日长度。`gap_days` 是自然日差，周末也会增大；不能仅凭它判定停牌或丢行情。

## 选做：真实数据采集

```bash
.venv\Scripts\python -m pip install akshare
.venv\Scripts\python extras/lecture-02/collect_akshare.py --symbol 601318 --start 20250620 --end 20250704 --output work/pingan-snapshot-01
```

程序请求真实接口的raw与hfq数据，分文件保留并写入含版本、参数、UTC采集时间和SHA-256的 `manifest.json`。输出目录必须不存在。请求失败或结构异常直接报错，不用模拟值替代。每次采集换新快照目录。

采集脚本保存来源原始单位：成交量为手、成交额为元；课程演示清洗后统一成交量为股，需显式乘100。前复权历史可能重算甚至出现负值，不能把本练习“原始价必须为正”的规则套用于所有复权序列。

真实案例依据[中国平安2024年年度权益分派实施公告](https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0619/2025061901148_c.pdf)，网页未编造当日真实收盘价或收益。

## 文件

- `index.html`：完整课程正文，公式使用原生HTML上下标，表格和图像有文字说明。
- `course.css`：响应式布局与打印样式。
- `course.js`：阅读进度、目录状态、复制按钮、模拟均线交互。
- `lab.py`：完整离线实验与质量检查。
- `collect_akshare.py`：可选联网快照采集。
- `requirements.txt`：离线实验依赖；AkShare独立选装。

现有第一期、第二期及 `extras/lecture-01/` 不属于本讲修改范围。

## 验证记录

2026-11-08：14个阅读单元、24个代码块的HTML结构与内部链接检查通过；离线Python示例与13条SQL语句执行通过。完整实验在pandas 3.0.1与3.1.1、SQLite 3.53.1下通过主键、行数对账、窗口边界、未来数据扰动、一对一键对齐的pandas/SQL比较、重复运行与目录保护检查。

桌面1440px、手机390px及320px宽度均无整页横向溢出；目录定位、进度更新、窗口切换、复制成功提示与折叠答案检查通过。AkShare 1.20.35真实接口采集成功，原始价与后复权快照分开保存；实际行情文件未作为教学固定结果提交。
