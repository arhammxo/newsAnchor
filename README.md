# newsAnchor 📰🎙️

> Turns live news into teleprompter‑ready scripts for an AI news‑anchor livestream. Scrapes BBC News and PR Newswire in real time, then uses Gemini to rewrite each story as broadcast copy.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![LLM: Gemini](https://img.shields.io/badge/LLM-Gemini-4285F4)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

Built as the content engine for an AI livestream product: it removed the manual scripting step and cut content‑generation time by ~40% while keeping delivery accurate to the source article.

## How it works

```mermaid
flowchart LR
    S1[BBC News] --> SC[requests + BeautifulSoup scraper]
    S2[PR Newswire] --> SC
    SC --> P[Prompt builder<br/>anchor tone, length, safety config]
    P --> G[Gemini generate_content]
    G --> T[Teleprompter script]
```

| File | Purpose |
|---|---|
| `promptGenerator.py` | Scrape BBC headlines/articles → Gemini → anchor script |
| `prnewswireScrapper.py` | Same pipeline for PR Newswire press releases |

## Quickstart

```bash
git clone https://github.com/arhammxo/newsAnchor.git && cd newsAnchor
pip install -r requirements.txt
cp .env.example .env && export GEMINI_API_KEY=...   # never commit keys
python promptGenerator.py
```

## Notes

- Scraping respects the sites' `robots.txt`; use for personal/research purposes and check each publisher's terms before commercial use.
- Model name is set in each script (`gemini-pro`); swap for a current Gemini model as needed.

## License

MIT — see [LICENSE](LICENSE).
