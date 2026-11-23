<p align="center">
  <img src="../../assets/images/readme-guide.svg" alt="Quant for babies — apprendre, expérimenter, expliquer" width="960" />
</p>

<p align="center">
  <a href="../../README.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.en.md">English</a> · <a href="README.ru.md">Русский</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <strong>Français</strong> · <a href="README.de.md">Deutsch</a> · <a href="README.es.md">Español</a> · <a href="README.hi.md">हिन्दी</a>
</p>

# La finance quantitative, une expérience à la fois

Un parcours accessible, de votre premier jeu de données de marché aux signaux, au risque, aux portefeuilles et à la recherche reproductible. Apprenez avec **8 notebooks Jupyter, 5 cours de recherche et 7 démonstrations dans le navigateur**.

**Langues disponibles :** ce guide et sa navigation sont proposés en dix langues. Les notebooks, les cours et la plupart des documents complémentaires sont actuellement en **chinois simplifié** ; changer la langue de ce README ne traduit pas le contenu pédagogique.

<p align="center">
  <a href="#start">Commencer</a> · <a href="#setup">Installation</a> · <a href="#curriculum">Notebooks</a> · <a href="#labs">Travaux pratiques</a> · <a href="#demos">Démonstrations</a> · <a href="#faq">Aide</a>
</p>

| Contenu disponible | Format | Ce que vous pourrez faire |
| --- | --- | --- |
| Chapitres 01–08 · disponibles | Notebooks Jupyter | Analyser les prix, construire une règle de moyennes mobiles, mesurer le risque et comparer des portefeuilles |
| Cours 01–05 · disponibles | HTML hors ligne + quatre TP Python | Suivre le parcours données → facteurs → évaluation → backtest simulé |
| Sept démonstrations interactives · disponibles | Fichiers HTML autonomes | Explorer visuellement les formules sans installer un environnement de recherche |
| Chapitres suivants et projets avancés · prévus | [Feuille de route](../ROADMAP.md) | Distinguer les sujets proposés des leçons déjà disponibles |

<a id="start"></a>
## 1. Choisissez votre point de départ

| Votre objectif | Commencez par | Premier résultat |
| --- | --- | --- |
| Comprendre les idées avant de coder | Le [cours 01](../../extras/lecture-01/index.html) et les [démonstrations](#demos) | Expliquer les étapes d’une démarche de recherche quantitative |
| Apprendre en écrivant et en exécutant du Python | L’[installation de l’environnement](#setup), puis le [notebook 01](../../notebooks/phase1_intro/01_什么是量化金融.ipynb) | Charger des données de marché et tracer votre premier graphique de prix |
| Pratiquer une chaîne de recherche complète | Les [cours 02–05](#labs), dans l’ordre | Produire des contrôles de données, des tables de facteurs, des rapports d’évaluation et un journal de transactions simulées |
| Animer un atelier ou apprendre en équipe | Les [notes de présentation du cours 01](../../extras/lecture-01/lecture-notes.md) et les consignes des TP | Animer une séance avec des exercices et des résultats vérifiables |

Aucune expérience préalable en finance quantitative n’est nécessaire. Des bases en Python facilitent le travail dans les notebooks ; vous pouvez commencer par la lecture des cours HTML. Pour chaque leçon, suivez le cycle **lire → exécuter → modifier une hypothèse → expliquer le résultat**.

### Lire les cours HTML

**GitHub affiche le code source HTML ; un lien vers un fichier du dépôt ne lance pas le cours.** Téléchargez le dépôt avec **Code → Download ZIP**, décompressez-le et ouvrez un fichier `extras/lecture-0N/index.html` dans votre navigateur. Les cinq pages de cours et les sept démonstrations sont consultables localement hors ligne. Les références externes et les téléchargements de données de marché nécessitent toujours une connexion.

Vous pouvez aussi exécuter cette commande à la racine du dépôt :

```bash
python -m http.server 8000 --bind 127.0.0.1
```

Ouvrez `http://127.0.0.1:8000/extras/lecture-01/` (remplacez `01` par `02` à `05` pour les autres cours). Sous macOS/Linux, utilisez `python3` si `python` n’est pas disponible. Arrêtez le serveur avec `Ctrl+C`.

Cours 01 : utilisez les flèches ou Espace pour avancer, `N` pour les notes de présentation, `O` pour la vue d’ensemble et `F` pour le plein écran.

<a id="setup"></a>
## 2. Préparez l’environnement des notebooks

Utilisez **Python 3.10+** ; Python 3.12 constitue un point de départ adapté. Installez Git pour cloner le dépôt, ou téléchargez et décompressez le ZIP. Exécutez les commandes suivantes dans un terminal. Les chemins directs vers l’interpréteur évitent les problèmes d’activation de l’environnement dans le shell.

<details>
<summary><strong>Windows · PowerShell</strong></summary>

```powershell
git clone https://github.com/ThreshoLdnnis/Quant-for-babies.git
cd Quant-for-babies
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

Si vous avez téléchargé un ZIP, ouvrez PowerShell dans le dossier du dépôt décompressé et commencez à `python -m venv .venv`.

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

Si vous avez téléchargé un ZIP, ouvrez un terminal dans le dossier du dépôt décompressé et commencez à `python3 -m venv .venv`.

</details>

Jupyter affiche une URL locale dans le terminal. Ouvrez-la dans votre navigateur, choisissez `notebooks/phase1_intro/01_什么是量化金融.ipynb`, puis exécutez les cellules de haut en bas (`Shift+Enter`). Vérifiez que le notebook utilise bien l’environnement que vous venez de créer.

| Groupe de dépendances | Utilité | Source d’installation |
| --- | --- | --- |
| Jupyter, NumPy, pandas, Matplotlib, seaborn | Exécution des notebooks, tableaux et graphiques | [Dépendances à la racine](../../requirements.txt) |
| yfinance, AkShare | Exemples de données de marché ; connexion requise | Dépendances à la racine |
| scikit-learn | Outils de machine learning dans l’environnement pédagogique | Dépendances à la racine ; les chapitres IA suivants restent prévus |
| Dépendances propres à chaque cours | TP de recherche hors ligne ; le cours 04 nécessite aussi SciPy | `requirements.txt` dans le dossier de chaque cours |
| Bibliothèques graphiques facultatives | Export des figures des TP | `requirements-plot.txt` dans les cours 03–05 |

<a id="curriculum"></a>
## 3. Suivez le parcours des huit notebooks

Progressez dans l’ordre à l’intérieur de chaque phase. Conservez votre graphique, le paramètre modifié et une courte explication de ce qui s’est passé.

| Chapitre | Sujet / notebook | Objectif d’apprentissage |
| :---: | --- | --- |
| 01 | [Qu’est-ce que la finance quantitative ?](../../notebooks/phase1_intro/01_什么是量化金融.ipynb) | Développer son intuition et télécharger les prix d’AAPL |
| 02 | [Votre première expérience quantitative](../../notebooks/phase1_intro/02_你的第一个量化实验.ipynb) | Lire les données OHLCV, calculer les rendements et comparer la volatilité |
| 03 | [Stratégie de moyennes mobiles](../../notebooks/phase1_intro/03_移动平均线策略.ipynb) | Transformer les croisements MA5/MA20 en une règle de négociation explicite |
| 04 | [Backtest d’une stratégie](../../notebooks/phase1_intro/04_策略回测.ipynb) | Simuler des transactions et examiner le capital, le taux de réussite et le drawdown |
| 05 | [Comprendre la volatilité](../../notebooks/phase2_intro/01_理解波动率.ipynb) | Mesurer et annualiser la volatilité de plusieurs actifs |
| 06 | [Ratio de Sharpe et bêta](../../notebooks/phase2_intro/02_夏普比率与Beta.ipynb) | Comparer les rendements ajustés du risque et la sensibilité au marché |
| 07 | [Drawdown maximal et taille des positions](../../notebooks/phase2_intro/03_最大回撤与仓位管理.ipynb) | Relier le drawdown à l’exposition et à la tolérance au risque |
| 08 | [Portefeuilles et corrélation](../../notebooks/phase2_intro/04_多标的组合与相关性.ipynb) | Construire un portefeuille équipondéré et explorer la diversification |

**Phase 1 · Chapitres 01–04 :** données → rendements → règles → backtest.<br />
**Phase 2 · Chapitres 05–08 :** volatilité → indicateurs ajustés du risque → taille des positions → portefeuilles.

<details>
<summary>Aperçu des quatre premiers chapitres</summary>

<p>
  <img src="../../assets/images/ch01_real_stock.png" alt="Chapitre 01 : données de marché" width="46%" />
  <img src="../../assets/images/ch02_returns.png" alt="Chapitre 02 : rendements" width="46%" />
</p>
<p>
  <img src="../../assets/images/ch03_ma_signals.png" alt="Chapitre 03 : signaux de moyennes mobiles" width="46%" />
  <img src="../../assets/images/ch04_backtest.png" alt="Chapitre 04 : backtest" width="46%" />
</p>

</details>

<a id="labs"></a>
## 4. Construisez une démarche de recherche en cinq cours

Ces cours complètent les notebooks. Lisez-les dans l’ordre pour suivre toute la chaîne de recherche. **Conservez la structure complète du dépôt :** les TP 04 et 05 importent du code du cours 03.

| Cours | Lecture | Pratique et résultats attendus |
| :---: | --- | --- |
| 01 | [Démarche de recherche](../../extras/lecture-01/index.html) · [Notes de présentation](../../extras/lecture-01/lecture-notes.md) | Introduction en 13 diapositives ; aucun TP Python |
| 02 | [Ingénierie des données financières](../../extras/lecture-02/index.html) · [Consignes](../../extras/lecture-02/README.md) | pandas, SQLite/SQL, nettoyage et mise en quarantaine → tables CSV, base de données et rapports de qualité |
| 03 | [Facteurs et prétraitement](../../extras/lecture-03/index.html) · [Consignes](../../extras/lecture-03/README.md) | MOM20, VOL20, TURN20, MAD et scores Z transversaux → tables de facteurs et diagnostics |
| 04 | [Évaluation des facteurs et statistiques](../../extras/lecture-04/index.html) · [Consignes](../../extras/lecture-04/README.md) | Rank IC, ICIR, groupes et évaluation chronologique → tables d’évaluation et rapport d’audit |
| 05 | [Backtest multifactoriel](../../extras/lecture-05/index.html) · [Consignes](../../extras/lecture-05/README.md) | Scores statiques, Top N, exécution à l’ouverture suivante et coûts → comptes simulés, journaux de transactions et synthèses de recherche |

### Exécuter les quatre TP hors ligne

À la racine du dépôt, avec l’environnement virtuel activé, exécutez les commandes suivantes. Vous pouvez aussi remplacer chaque `python` par `.\.venv\Scripts\python.exe` sous Windows ou `.venv/bin/python` sous macOS/Linux.

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

Utilisez un dossier de sortie dédié pour chaque TP. Les scripts protègent les dossiers non vides qui ne leur appartiennent pas ; consultez les consignes du cours avant de modifier ou de réutiliser un chemin de sortie. Les scripts graphiques facultatifs et l’exercice de collecte AkShare en ligne sont documentés dans les dossiers des cours concernés.

**Interprétation des résultats :** les TP principaux utilisent des **données pédagogiques simulées** déterministes et ne nécessitent pas de connexion aux données de marché après installation des dépendances. Les échantillons courts et les coûts hypothétiques illustrent les méthodes ; ils ne démontrent ni une stratégie prête à investir ni des performances formelles hors échantillon. Les téléchargements des notebooks peuvent utiliser des prix historiques réels. Certaines démonstrations contiennent des instantanés historiques ; leurs commandes ne récupèrent pas de prix en temps réel.

<a id="demos"></a>
## 5. Explorez les concepts visuellement

Téléchargez et ouvrez les fichiers HTML, ou utilisez le serveur local décrit plus haut. Les [notes des démonstrations](../../assets/interactive/README.md) expliquent leurs données et leur fonctionnement.

| Démonstration | À associer à | À essayer |
| --- | --- | --- |
| [Mouvement brownien / marche aléatoire](../../assets/interactive/brownian-random-walk.html) | Chapitre 01 | Comparer les trajectoires et distinguer le hasard d’une prévision |
| [Rendements journaliers](../../assets/interactive/daily-return-demo.html) | Chapitre 05 | Suivre le calcul du rendement à partir des prix |
| [Écart-type d’un échantillon](../../assets/interactive/std-dev-demo.html) | Chapitre 05 | Examiner les écarts et leur agrégation |
| [Variance d’une population](../../assets/interactive/population-variance-demo.html) | Chapitre 05 | Relier la définition à un exemple visuel |
| [Correction de la variance](../../assets/interactive/variance-formulas-demo.html) | Chapitre 05 | Comparer le rôle de `n` et de `n−1` |
| [Ratio de Sharpe](../../assets/interactive/sharpe-ratio-demo.html) | Chapitre 06 | Comparer le rendement excédentaire à la volatilité |
| [Bêta](../../assets/interactive/beta-demo.html) | Chapitre 06 | Explorer la relation entre un actif et un indice de référence |

<a id="roadmap"></a>
## 6. Découvrez la suite du parcours

| Statut | Périmètre | Où consulter |
| --- | --- | --- |
| Disponible | Huit notebooks, cinq cours, sept démonstrations | Les tableaux ci-dessus |
| Prévu · Chapitres 09–14 | Introduction au ML, XGBoost, LSTM, Transformer, sélection multifactorielle et système quantitatif avec IA | [Feuille de route détaillée](../ROADMAP.md) |
| Prévus · projets avancés | Assistant financier NLP/RAG ; allocation de facteurs selon les régimes de marché ; sélection d’actions par ML et alpha explicable | [Propositions de projets](../ROADMAP.md#advanced-projects) |
| En construction | Modules réutilisables dans `src/` | Pour le moment, des fichiers réservés, pas un framework de backtest de production |

### Repérez-vous dans le dépôt

| Chemin | Contenu |
| --- | --- |
| [`notebooks/`](../../notebooks/) | Leçons des phases 1 et 2 |
| [`extras/`](../../extras/) | Cours HTML, consignes, TP et outils graphiques facultatifs |
| [`assets/interactive/`](../../assets/interactive/) | Sept démonstrations dans le navigateur |
| [`assets/images/`](../../assets/images/) | Illustrations du cours et éléments graphiques du README |
| [`docs/`](../) | Feuille de route et guides README multilingues |
| [`scripts/`](../../scripts/) | Utilitaires de maintenance des notebooks et de génération d’illustrations |
| [`requirements.txt`](../../requirements.txt) | Dépendances de l’environnement des notebooks |

<a id="faq"></a>
## 7. Résolvez les difficultés courantes

| Question | Que faire ? |
| --- | --- |
| Pourquoi GitHub affiche-t-il du code HTML ? | Téléchargez et ouvrez le fichier, ou utilisez le serveur HTTP local présenté dans [Commencer](#start). |
| Pourquoi un paquet manque-t-il dans Jupyter ? | Installez-le avec le `python -m pip` du même environnement ; vérifiez le noyau sélectionné et redémarrez-le après l’installation. |
| Pourquoi un téléchargement de données de marché a-t-il échoué ? | Vérifiez votre connexion et la réponse du fournisseur. Ne considérez pas des données vides comme une expérience réussie. Poursuivez avec les TP hors ligne. |
| Pourquoi un TP refuse-t-il le dossier de sortie ? | Choisissez un nouveau dossier dédié, ou suivez les règles du cours pour relancer le TP dans son propre dossier marqué. |
| Le changement de langue traduit-il les notebooks ? | Non. Dix guides README sont proposés ; le contenu pédagogique reste principalement en chinois simplifié. |
| Comment signaler un problème ? | [Ouvrez une issue](https://github.com/ThreshoLdnnis/Quant-for-babies/issues) en précisant le chemin du fichier, la commande, la version de Python et le message d’erreur. Supprimez les jetons et les informations personnelles des journaux. |

Les contributions sont les bienvenues : corrections, exemples plus clairs et traductions soigneusement relues. Gardez les chemins et les commandes identiques dans les dix guides ; consultez les [notes de maintenance des traductions](README.md).

---

**Licence :** [MIT](../../LICENSE). **Usage pédagogique :** ce dépôt est destiné à l’apprentissage et à la recherche ; il ne constitue pas un conseil en investissement. Les résultats historiques ou simulés ne garantissent pas les performances futures.
