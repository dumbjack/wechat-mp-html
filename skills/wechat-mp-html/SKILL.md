---
name: wechat-mp-html
description: Generate clean, mobile-friendly WeChat Official Account article HTML for copying into the WeChat backend, 135 Editor, Xiumi, or Yiban. Use when the user asks to convert an article into WeChat public account HTML, WeChat MP HTML, gongzhonghao HTML,公众号 HTML 排版, source snippets, browser previews with copy buttons, or finance/research-style WeChat article formatting.
---

# WeChat MP HTML

## Overview

Convert an article into a WeChat-safe HTML source snippet and a browser preview file with copy/select buttons. Keep the output professional, restrained, mobile-readable, and compatible with the WeChat article editor's HTML filtering.

## Workflow

1. Read `references/wechat-mp-html-compat.md` before generating output.
2. Preserve the user's viewpoint and facts. Improve paragraph rhythm, headings, emphasis, and data presentation, but do not invent unsupported data or stronger investment claims.
3. Convert the article into structured JSON for `scripts/generate_wechat_mp_html.py`.
4. Run the generator to create:
   - `公众号 HTML 预览版.html`
   - `公众号源码片段.txt`
5. Inspect the generator warnings and fix the JSON/content if it reports forbidden tags, external images, or length risk.
6. Tell the user where the files are and that the preview page's copy button copies only the article body.

## JSON Shape

Create a temporary UTF-8 JSON file with this shape:

```json
{
  "title": "Article title",
  "subtitle": "Optional subtitle",
  "conclusion": "One-sentence core judgment",
  "intro": ["Short opening paragraph", "Second opening paragraph"],
  "sections": [
    {
      "title": "Section heading",
      "paragraphs": ["Short paragraph", "Use **bold** for key claims"],
      "data": [
        {"label": "近 30 天总手续费", "value": "约 xxxx 万美元"},
        "占比：约 xx%"
      ],
      "highlights": ["Core judgment card text"],
      "bullets": ["Optional bullet"],
      "images": ["这里放 xxx 图"]
    }
  ],
  "closing_question": "你觉得 xxx 是远期合理定价，还是牛市叙事？"
}
```

Supported aliases: `data_cards` for `data`, `judgement_cards` or `highlight_cards` for `highlights`, and `closing.question` for `closing_question`.

Run:

```bash
python3 path/to/wechat-mp-html/scripts/generate_wechat_mp_html.py article.json --out-dir output-dir
```

## Formatting Rules

- Use short mobile paragraphs, usually 2-4 lines on a phone.
- Use a dark title card, a gray conclusion card, centered numbered section headings, gray data cards, pale-yellow judgment cards, and a dark closing card.
- Prefer `section`, `p`, `span`, `strong`, and `br` in the source snippet. Use `blockquote`, `ul`, `ol`, and `li` only when the content truly needs them.
- Never use tables for data. Convert tables into stacked data cards.
- Never emit external image links. Replace image needs with `【图片：这里放 xxx 图】`.
- Avoid absolute investment language such as "一定上涨", "稳赚", "必然翻倍", or "无风险".

## Resources

- `references/wechat-mp-html-compat.md`: WeChat-compatible HTML rules and source notes.
- `scripts/generate_wechat_mp_html.py`: Deterministic generator for the preview file and source snippet.
