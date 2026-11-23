<p align="center">
  <img src="../../assets/images/readme-guide.svg" alt="Quant for babies — 学ぶ、実験する、説明する" width="960" />
</p>

<p align="center">
  <a href="../../README.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.en.md">English</a> · <a href="README.ru.md">Русский</a> · <strong>日本語</strong> · <a href="README.ko.md">한국어</a> · <a href="README.fr.md">Français</a> · <a href="README.de.md">Deutsch</a> · <a href="README.es.md">Español</a> · <a href="README.hi.md">हिन्दी</a>
</p>

# 実験を一つずつ重ねて学ぶクオンツ金融

初めての市場データから、シグナル、リスク、ポートフォリオ、再現可能な研究へ。**8 本の Jupyter Notebook、5 回の研究講義、7 つのブラウザデモ**を使って、順を追って学べます。

**翻訳の範囲：** このガイドとナビゲーションは 10 言語に対応しています。Notebook、講義、関連文書の大半は現在、**簡体字中国語**です。README の言語を切り替えても、教材本文は翻訳されません。

<p align="center">
  <a href="#start">はじめに</a> · <a href="#setup">環境構築</a> · <a href="#curriculum">Notebook</a> · <a href="#labs">研究実習</a> · <a href="#demos">デモ</a> · <a href="#faq">困ったときは</a>
</p>

| 利用できる内容 | 形式 | できるようになること |
| --- | --- | --- |
| 第 01〜08 章 · 公開済み | Jupyter Notebook | 価格を分析し、移動平均ルールを作り、リスクを測定し、ポートフォリオを比較する |
| 第 01〜05 回講義 · 公開済み | オフライン HTML + 4 つの Python 実習 | データ → ファクター → 評価 → シミュレーションによるバックテストを進める |
| 7 つの対話型デモ · 公開済み | 単独で開ける HTML | 研究環境をインストールせずに、数式を視覚的に理解する |
| 今後の章と発展プロジェクト · 計画中 | [ロードマップ](../ROADMAP.md) | 公開済みの教材と今後の構想を区別して確認する |

<a id="start"></a>
## 1. 自分に合った入口を選ぶ

| 目的 | 最初に取り組む内容 | 最初の成果 |
| --- | --- | --- |
| コードを書く前に考え方を理解したい | [第 01 回講義](../../extras/lecture-01/index.html)と[デモ](#demos) | クオンツ研究の手順を説明できる |
| Python を書いて動かしながら学びたい | [環境構築](#setup)の後に[Notebook 01](../../notebooks/phase1_intro/01_什么是量化金融.ipynb) | 市場データを読み込み、最初の価格チャートを描ける |
| 一連の研究プロセスを実践したい | [第 02〜05 回講義](#labs)を順番に進める | データ検査、ファクター表、評価レポート、模擬取引台帳を作れる |
| ワークショップを開いたりチームで学んだりしたい | [第 01 回の講師用ノート](../../extras/lecture-01/lecture-notes.md)と実習説明 | 演習と確認可能な成果物を使って学習会を進行できる |

クオンツ金融の経験は必要ありません。Python の基礎知識があると Notebook を学びやすくなりますが、先に HTML 教材を読むこともできます。各レッスンでは **読む → 実行する → 仮定を一つ変える → 結果を説明する** を繰り返してください。

### HTML 教材を読む

**GitHub では HTML のソースコードが表示されます。リポジトリ内のファイルリンクを開くだけでは教材は実行されません。** **Code → Download ZIP** からリポジトリをダウンロードして展開し、ブラウザで `extras/lecture-0N/index.html` を開いてください。5 回の講義ページと 7 つのデモは、ローカルでオフライン閲覧できます。外部の参考リンクや最新データのダウンロードには接続が必要です。

リポジトリのルートディレクトリで、次のコマンドを実行する方法もあります。

```bash
python -m http.server 8000 --bind 127.0.0.1
```

`http://127.0.0.1:8000/extras/lecture-01/` を開きます（ほかの講義では `01` を `02`〜`05` に置き換えます）。macOS/Linux で `python` が使えない場合は `python3` を使ってください。サーバーを停止するには `Ctrl+C` を押します。

第 01 回講義では、矢印キーまたはスペースキーでページを移動できます。`N` で講師用ノート、`O` で一覧、`F` で全画面表示を切り替えます。

<a id="setup"></a>
## 2. Notebook の実行環境を用意する

**Python 3.10 以降**を使用してください。初めてなら Python 3.12 が選択肢になります。Git をインストールしてクローンするか、ZIP をダウンロードして展開してください。以下のコマンドはターミナルで実行します。仮想環境の実行ファイルを直接指定するため、シェルでの有効化に関する問題を避けられます。

<details>
<summary><strong>Windows · PowerShell</strong></summary>

```powershell
git clone https://github.com/ThreshoLdnnis/Quant-for-babies.git
cd Quant-for-babies
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

ZIP をダウンロードした場合は、展開したリポジトリのフォルダーで PowerShell を開き、`python -m venv .venv` から実行してください。

</details>

<details>
<summary><strong>macOS / Linux · ターミナル</strong></summary>

```bash
git clone https://github.com/ThreshoLdnnis/Quant-for-babies.git
cd Quant-for-babies
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyterlab
```

ZIP をダウンロードした場合は、展開したリポジトリのフォルダーでターミナルを開き、`python3 -m venv .venv` から実行してください。

</details>

Jupyter がターミナルにローカル URL を表示します。ブラウザで開き、`notebooks/phase1_intro/01_什么是量化金融.ipynb` を選択して、セルを上から順に実行します（`Shift+Enter`）。Notebook が、作成した仮想環境を使用していることを確認してください。

| 依存パッケージ | 用途 | インストール元 |
| --- | --- | --- |
| Jupyter、NumPy、pandas、Matplotlib、seaborn | Notebook の実行、表、グラフ | [ルートの依存関係ファイル](../../requirements.txt) |
| yfinance、AkShare | 市場データの例。ネットワーク接続が必要 | ルートの依存関係ファイル |
| scikit-learn | 学習環境の機械学習ツール | ルートの依存関係ファイル。後続の AI 章は計画中 |
| 講義ごとの依存関係 | オフライン研究実習。第 04 回では SciPy も必要 | 各講義フォルダーの `requirements.txt` |
| 任意の描画パッケージ | 実習の図を出力 | 第 03〜05 回の `requirements-plot.txt` |

<a id="curriculum"></a>
## 3. 8 本の Notebook を順番に進める

各フェーズ内では順に学習してください。作成したグラフ、変更したパラメーター、結果の短い説明を保存しましょう。

| 章 | テーマ／Notebook | 学習成果 |
| :---: | --- | --- |
| 01 | [クオンツ金融とは？](../../notebooks/phase1_intro/01_什么是量化金融.ipynb) | 基本的な考え方を理解し、AAPL の価格データを取得する |
| 02 | [初めてのクオンツ実験](../../notebooks/phase1_intro/02_你的第一个量化实验.ipynb) | OHLCV を読み、リターンを計算し、ボラティリティを比較する |
| 03 | [移動平均戦略](../../notebooks/phase1_intro/03_移动平均线策略.ipynb) | MA5/MA20 のクロスを明確な売買ルールにする |
| 04 | [戦略のバックテスト](../../notebooks/phase1_intro/04_策略回测.ipynb) | 取引をシミュレーションし、資産曲線、勝率、ドローダウンを確認する |
| 05 | [ボラティリティを理解する](../../notebooks/phase2_intro/01_理解波动率.ipynb) | 複数資産のボラティリティを測定し、年率換算する |
| 06 | [シャープレシオとベータ](../../notebooks/phase2_intro/02_夏普比率与Beta.ipynb) | リスク調整後リターンと市場への感応度を比較する |
| 07 | [最大ドローダウンとポジション管理](../../notebooks/phase2_intro/03_最大回撤与仓位管理.ipynb) | ドローダウンとエクスポージャー、リスク許容度の関係を考える |
| 08 | [ポートフォリオと相関](../../notebooks/phase2_intro/04_多标的组合与相关性.ipynb) | 等ウェイトのポートフォリオを作り、分散投資を調べる |

**フェーズ 1 · 第 01〜04 章：** データ → リターン → ルール → バックテスト。<br />
**フェーズ 2 · 第 05〜08 章：** ボラティリティ → リスク調整指標 → ポジション管理 → ポートフォリオ。

<details>
<summary>最初の 4 章のプレビュー</summary>

<p>
  <img src="../../assets/images/ch01_real_stock.png" alt="第 01 章：市場データ" width="46%" />
  <img src="../../assets/images/ch02_returns.png" alt="第 02 章：リターン" width="46%" />
</p>
<p>
  <img src="../../assets/images/ch03_ma_signals.png" alt="第 03 章：移動平均シグナル" width="46%" />
  <img src="../../assets/images/ch04_backtest.png" alt="第 04 章：バックテスト" width="46%" />
</p>

</details>

<a id="labs"></a>
## 4. 5 回の講義で研究プロセスを組み立てる

これらの講義は Notebook を補完する教材です。研究の流れに沿って順番に読んでください。**リポジトリのフォルダー構成を保ってください。** 第 04・05 回の実習は、第 03 回のコードをインポートします。

| 講義 | 読む教材 | 実習と期待される出力 |
| :---: | --- | --- |
| 01 | [研究プロセス](../../extras/lecture-01/index.html) · [講師用ノート](../../extras/lecture-01/lecture-notes.md) | 13 枚の入門スライド。Python 実習はありません |
| 02 | [金融データエンジニアリング](../../extras/lecture-02/index.html) · [実行手順](../../extras/lecture-02/README.md) | pandas、SQLite/SQL、クリーニング、問題データの隔離 → CSV、データベース、品質レポート |
| 03 | [ファクターと前処理](../../extras/lecture-03/index.html) · [実行手順](../../extras/lecture-03/README.md) | MOM20、VOL20、TURN20、MAD、クロスセクション Z スコア → ファクター表と診断結果 |
| 04 | [ファクター評価と統計](../../extras/lecture-04/index.html) · [実行手順](../../extras/lecture-04/README.md) | Rank IC、ICIR、グループ分け、時系列順の評価 → 評価表と監査レポート |
| 05 | [マルチファクターのバックテスト](../../extras/lecture-05/index.html) · [実行手順](../../extras/lecture-05/README.md) | 静的スコア、上位 N 銘柄、次の始値での執行、コスト → 模擬口座、取引台帳、研究要約 |

### 4 つのオフライン実習を実行する

仮想環境を有効にした状態で、リポジトリのルートディレクトリから次を実行します。あるいは、すべての `python` を Windows では `.\.venv\Scripts\python.exe`、macOS/Linux では `.venv/bin/python` に置き換えてください。

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

各実習に専用の出力ディレクトリを用意してください。スクリプトは、無関係な空でないディレクトリを保護します。出力先を変更・再利用する前に、各講義の説明を確認してください。任意の描画スクリプトと、ネットワーク接続を使う AkShare データ収集演習についても、各講義フォルダーに記載されています。

**出力の読み方：** 中心となる実習では、決定的に生成される**教育用の模擬データ**を使用します。依存パッケージのインストール後は、市場データへの接続は不要です。短いサンプルと仮定したコストは手法の説明に用いており、実運用できる戦略や正式なアウトオブサンプル性能を示すものではありません。Notebook では実際の過去価格をダウンロードする場合があります。一部のデモは過去データのスナップショットを内蔵しており、操作してもリアルタイム価格は取得しません。

<a id="demos"></a>
## 5. 概念を視覚的に探る

HTML ファイルをダウンロードして開くか、上記のローカルサーバーを使用してください。[デモの説明](../../assets/interactive/README.md)で、データと動作を確認できます。

| デモ | 組み合わせる章 | 試してみること |
| --- | --- | --- |
| [ブラウン運動／ランダムウォーク](../../assets/interactive/brownian-random-walk.html) | 第 01 章 | 経路を比較し、ランダム性と予測を区別する |
| [日次リターン](../../assets/interactive/daily-return-demo.html) | 第 05 章 | 価格からリターンへの計算をたどる |
| [標本標準偏差](../../assets/interactive/std-dev-demo.html) | 第 05 章 | 偏差とその集計を確認する |
| [母分散](../../assets/interactive/population-variance-demo.html) | 第 05 章 | 定義を視覚的な例と結び付ける |
| [分散の補正](../../assets/interactive/variance-formulas-demo.html) | 第 05 章 | `n` と `n−1` の役割を比較する |
| [シャープレシオ](../../assets/interactive/sharpe-ratio-demo.html) | 第 06 章 | 超過リターンとボラティリティを比較する |
| [ベータ](../../assets/interactive/beta-demo.html) | 第 06 章 | 資産とベンチマークの関係を調べる |

<a id="roadmap"></a>
## 6. 今後の内容を確認する

| 状態 | 範囲 | 確認先 |
| --- | --- | --- |
| 公開済み | 8 本の Notebook、5 回の講義、7 つのデモ | 上の各表 |
| 計画中 · 第 09〜14 章 | 機械学習入門、XGBoost、LSTM、Transformer、マルチファクター銘柄選択、AI クオンツシステム | [詳細なロードマップ](../ROADMAP.md) |
| 計画中 · 発展プロジェクト | 金融 NLP/RAG アシスタント、市場状態に応じたファクター配分、機械学習による銘柄選択と説明可能な Alpha | [プロジェクト構想](../ROADMAP.md#advanced-projects) |
| 構築中 | `src/` の再利用可能モジュール | 現在はひな型のみで、実運用向けのバックテスト基盤ではありません |

### リポジトリの構成を知る

| パス | 内容 |
| --- | --- |
| [`notebooks/`](../../notebooks/) | フェーズ 1・2 の教材 |
| [`extras/`](../../extras/) | 講義 HTML、説明、実習、任意の描画ツール |
| [`assets/interactive/`](../../assets/interactive/) | 7 つのブラウザデモ |
| [`assets/images/`](../../assets/images/) | 教材の図と README の画像 |
| [`docs/`](../) | ロードマップと多言語 README ガイド |
| [`scripts/`](../../scripts/) | Notebook の保守と教材画像の生成ツール |
| [`requirements.txt`](../../requirements.txt) | Notebook 環境の依存関係 |

<a id="faq"></a>
## 7. 困ったときは

| 質問 | 対応方法 |
| --- | --- |
| GitHub で HTML コードが表示されるのはなぜ？ | ファイルをダウンロードして開くか、[はじめに](#start)のローカル HTTP サーバーを使ってください。 |
| Jupyter でパッケージが見つからないのはなぜ？ | 同じ環境の `python -m pip` でインストールしてください。選択中のカーネルを確認し、インストール後に再起動してください。 |
| 市場データをダウンロードできないのはなぜ？ | ネットワークと提供元の応答を確認してください。空のデータを実験成功と見なさず、オフラインの講義実習で学習を続けてください。 |
| 実習で出力ディレクトリを拒否されたら？ | 新しい専用ディレクトリを選ぶか、実習自身の識別情報がある出力先について、各講義の再実行ルールに従ってください。 |
| 言語を切り替えると Notebook も翻訳される？ | いいえ。README ガイドは 10 言語ですが、教材本文は主に簡体字中国語です。 |
| 不具合を報告するには？ | [Issue を作成](https://github.com/ThreshoLdnnis/Quant-for-babies/issues)し、ファイルパス、コマンド、Python のバージョン、エラーメッセージを記載してください。ログからトークンや個人情報を削除してください。 |

修正、より分かりやすい例、丁寧に確認された翻訳の貢献を歓迎します。10 言語のガイドでコードのパスとコマンドを統一してください。[翻訳の保守方針](README.md)も参照してください。

---

**ライセンス：** [MIT](../../LICENSE)。**教育目的：** このリポジトリは学習・研究用であり、投資助言ではありません。過去やシミュレーションの結果は、将来の成績を保証しません。
