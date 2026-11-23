# README translation guide / 多语言维护说明

The repository provides ten README guides. These translate the introduction, navigation, setup and learning instructions; notebooks, HTML lectures and most supporting documents remain primarily Simplified Chinese.

仓库提供十种语言的 README，覆盖介绍、导航、环境配置和学习说明；课程正文尚未完成多语言翻译。

| Language | Guide |
| --- | --- |
| 简体中文 | [README](../../README.md) |
| 繁體中文 | [README.zh-TW](README.zh-TW.md) |
| English | [README.en](README.en.md) |
| Русский | [README.ru](README.ru.md) |
| 日本語 | [README.ja](README.ja.md) |
| 한국어 | [README.ko](README.ko.md) |
| Français | [README.fr](README.fr.md) |
| Deutsch | [README.de](README.de.md) |
| Español | [README.es](README.es.md) |
| हिन्दी | [README.hi](README.hi.md) |

## Keep the guides aligned

1. Update the Simplified Chinese and English guides together when the repository changes, then update the other eight guides.
2. Preserve all ten language links and stable anchors: `start`, `setup`, `curriculum`, `labs`, `demos`, `roadmap`, `faq`.
3. Translate explanatory text, headings and image descriptions. Keep file paths, commands, package names and technical identifiers unchanged, including Chinese notebook filenames.
4. Keep the same inventory: eight notebooks, five lectures and seven demos. Distinguish available lessons, placeholders and planned work.
5. Keep the language-scope note, offline/online data distinctions, environment instructions and output-directory safeguards.
6. Verify relative links from each file's own directory. The root guide uses `docs/i18n/`; other guides use sibling filenames and `../../` for repository-root files.

Run the documentation integrity check from the repository root:

```bash
python scripts/check_readme_links.py
```

This checks local link targets, explicit anchors, language navigation and command-block consistency. It does not verify translation quality or execute the research notebooks.
