# 番外期·第四讲：因子有效性检验与基础统计

[打开单文件HTML](index.html) · [检验实操](evaluation_lab.py) · [绘图脚本](plot_evaluation.py) · [第三讲](../lecture-03/README.md) · [课程目录](../../README.md)

《量化金融研究基础与多因子策略实战》系列第四讲，按PPT04的15项规划扩写成完整纵向阅读教程。包含未来标签、Rank IC、手算与并列、IC时间序列、ICIR、稳定性、统计不确定性、五分组、相关性、时间切分、完整程序与练习答案。没有提前实现交易策略、净值回测、动态配置或机器学习。

## 阅读

只下载 `index.html`，在浏览器直接打开即可。样式、交互、图表数据与Python附件全部内置，不依赖同目录CSS/JS或联网图表库。提供17个阅读单元、章节锚点、进度、代码复制、因子切换、得分/平均秩散点切换及折叠答案。文献与GitHub导航需要联网。

GitHub文件页显示源码。可下载后打开，或从仓库根目录启动 `python -m http.server 8000 --bind 127.0.0.1`，再访问 `http://127.0.0.1:8000/extras/lecture-04/`。这不是已发布的GitHub Pages站点。

## 数据连续性

核心实验直接导入第三讲的 [factor_lab.py](../lecture-03/factor_lab.py)，原样复用8只虚构股票、80个模拟工作日、价格与缺失、MAD、Z-score和固定方向。模拟无公司行为，日期不是真实A股交易日历。输出不是真实A股因子有效性证据。

`evaluation_lab.py`先找同目录的`factor_lab.py`，再找仓库相邻的第三讲目录；运行报告记录源文件和原始输入哈希。单独下载代码时，需把这两个脚本及`requirements.txt`放在一起；单文件HTML已提供对应附件。

## 核心实验

Python 3.10+，在仓库根目录运行：

```bash
python -m venv .venv
# Windows；已有课程环境可复用
.venv\Scripts\python -m pip install -r extras/lecture-04/requirements.txt
.venv\Scripts\python extras/lecture-04/evaluation_lab.py --output data/processed/lecture04-simulation
```

macOS / Linux将解释器换成`.venv/bin/python`。单独文件模式去掉`extras/lecture-04/`前缀。程序不联网，只管理带专用标记的输出目录，拒绝覆盖其他非空目录。

固定模拟结果：640行完整网格；427个非空未来标签；223个三因子与标签共同配对；40个有效评价日×3因子=120个有效IC。IC明细仍保留预热、标签未成熟和异常状态，不将空值填0。

## 固定研究口径

- 标签为`t`收盘至`t+20`收盘价格收益，要求21个有效价格作为保守质量政策；最后20个日期留空。标签只用于事后评价，不进入当期因子和方向，也不是可执行策略收益。
- 每个日期三因子共用同一配对样本；`min_n=5`仅是教学参数。并列采用平均秩，因子或标签常量时IC不可定义。
- ICIR使用有效IC的样本标准差`ddof=1`，不年化；不足2期或标准差为0则缺失。
- 每日20期标签重叠，不能假定40个日期独立。只提供两个预定非重叠起点对照，不强报朴素t统计量或独立日期置信区间。
- 五分组检查真实组数，分位边界重复导致少于5组时跳过并审计，不按股票代码强拆并列。MOM/VOL/TURN各有39/40/32个可用五分组日期；主图使用共同31日期，原各自日期结果另存。
- 组内按股等权、跨日期按日期等权平均20期未来价格收益。不是日策略收益，不复利成NAV。
- 因子Pearson相关矩阵使用固定日期的当期因子有效样本，不按未来标签筛股票；与因子—未来收益的Rank IC不同。

## 统计与样本外边界

五股课堂例子的Rank IC为0.8。无并列情况下完整枚举120个标签配对，按本课双侧绝对值尾部定义有16个至少同样极端，精确课堂p=16/120≈0.133333；SciPy默认小样本近似p≈0.104088，二者分开记录。置换依赖课堂交换性假设，不是对真实市场独立性的保证。

时间段预先固定为索引`[0,40)`开发、`[40,60)`验证、`[60,80)`测试。要求标签终点仍在本段；三段共同成熟X–Y配对均为0。开发段有139个成熟标签行，但其对应因子未完成预热；验证和测试各仅20个日期，连完整20期未来标签都无法在段内成熟。程序诚实报告不足，不回头改切分凑出样本外结论。正式研究需要更长历史。

## 输出与图表

输出包括标签面板、手算排名、IC明细与汇总、非重叠样本对照、分组成员/每期收益/各自及共同日期均值/审计、因子相关矩阵、时间切分明细与汇总、`chart_data.json`和`quality_report.json`。具体文件名以程序实际输出为准。

```bash
.venv\Scripts\python -m pip install -r extras/lecture-04/requirements-plot.txt
.venv\Scripts\python extras/lecture-04/plot_evaluation.py --input data/processed/lecture04-simulation/chart_data.json --output data/processed/lecture04-figures
```

绘图输出PNG/SVG：固定日散点、IC时间序列、共同日期五组均值、因子相关性、相同均值的稳定性对照。全部标明SIMULATED及日期/样本/单位；图形不是实证结论。

## 本版验证

13段页面Python示例运行通过，核心实验19项检查通过；重复运行CSV/JSON结果一致。已核对公式手算、表格和图表数据、17个章节锚点、内置附件、单文件打包重复执行，以及1440px桌面、390px与320px手机布局。目录、进度、因子切换、平均秩视角、复制按钮及答案展开均已实际检查。

## 维护说明

`course.css`和`course.js`为样式与交互源文件。修改资源或配套代码后运行`python scripts/build_lecture04_standalone.py`，重新内置到HTML。第三讲模块作为附件读取原文件，不在第四讲复制一份源代码。

第一期、第二期及番外期前三讲课程内容保持不变；第三讲本次仅按用户要求新增README封面，根README增加第四讲入口。
