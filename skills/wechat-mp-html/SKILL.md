---
name: wechat-mp-html
description: Generate clean, mobile-friendly WeChat Official Account article HTML without changing article wording or meaning, for copying into the WeChat backend, 135 Editor, Xiumi, or Yiban. Use when the user asks to convert an article into WeChat public account HTML, WeChat MP HTML, gongzhonghao HTML, 公众号 HTML 排版, source snippets, browser previews with copy buttons, or finance/research-style WeChat article formatting while preserving the original content exactly.
---

# WeChat MP HTML

## Overview

Convert an article into a WeChat-safe HTML source snippet and a browser preview file with copy/select buttons. Preserve the original article text exactly; only add HTML wrappers, inline styles, and copy/select preview controls.

## Workflow

1. Read `references/wechat-mp-html-compat.md` before generating output.
2. Preserve all article wording exactly. Do not rewrite, summarize, polish, shorten, expand, translate, or add any article content.
3. Convert the article into structured JSON for `scripts/generate_wechat_mp_html.py`.
4. Run the generator to create:
   - `公众号 HTML 预览版.html`
   - `公众号源码片段.txt`
5. Inspect the generator warnings and fix the JSON/content if it reports forbidden tags, external images, or length risk.
6. Tell the user where the files are and that the preview page's copy button copies only the article body.

## Non-Modification Contract

Treat the user's article as immutable source text.

- Do not add a title, subtitle, conclusion, section heading, highlight, label, closing question, disclaimer, transition sentence, or data point unless that exact text already appears in the source article or the user explicitly provides it.
- Do not create new numbered headings from your own interpretation. If the source has headings, preserve their wording and style them as section headings. If it has no headings, render the original paragraphs without invented headings.
- Do not split, merge, or reorder paragraphs unless the input already uses explicit blank lines, headings, lists, or tables that define the structure.
- Do not add bold emphasis. Preserve existing bold markers such as `**text**` only when they appear in the source or are explicitly supplied by the user.
- Converting a Markdown table into data cards is allowed only if every cell's text is preserved verbatim.
- Replacing an actual image URL or image request with `【图片：这里放 xxx 图】` is allowed only when the source article already contains that image reference or the user asks for an image placeholder.

## JSON Shape

Create a temporary UTF-8 JSON file using only text present in the article:

```json
{
  "title": "Existing article title only",
  "subtitle": "Existing subtitle only",
  "conclusion": "Existing standfirst or conclusion sentence only",
  "intro": ["Original paragraph", "Original paragraph"],
  "sections": [
    {
      "title": "Existing section heading only",
      "number": "01",
      "paragraphs": ["Original paragraph", "Use **bold** only if source already used it"],
      "blocks": [
        {"type": "paragraph", "text": "Original paragraph"},
        {"type": "subheading", "text": "Existing level-3 heading only"},
        {"type": "data", "items": ["Original data line", {"label": "Original label", "value": "Original value"}]}
      ],
      "data": [
        {"label": "近 30 天总手续费", "value": "约 xxxx 万美元"},
        "占比：约 xx%"
      ],
      "highlights": ["Existing highlighted sentence only"],
      "bullets": ["Original bullet"],
      "images": ["Original image reference"]
    }
  ],
  "closing_question": "Existing closing question only"
}
```

Omit any field that is not present in the original article. Use `blocks` when a section contains level-3 headings or data groups that must stay in their original order. Set `"number": false` for unnumbered source headings such as "结语"; otherwise use the existing source number, or omit `number` when the section is naturally numbered. Supported aliases: `data_cards` for `data`, `judgement_cards` or `highlight_cards` for `highlights`, and `closing.question` for `closing_question`.

Run:

```bash
python3 path/to/wechat-mp-html/scripts/generate_wechat_mp_html.py article.json --out-dir output-dir
```

## Formatting Rules

- Keep the original paragraph boundaries. Do not shorten paragraphs just to improve rhythm.
- Use a dark title card only when the original article has a title. Use a gray conclusion card, centered numbered section headings, gray data cards, pale-yellow judgment cards, and a dark closing card only when the corresponding text exists in the original.
- Style existing level-3 headings as subheadings through `blocks` with `type: "subheading"`; do not invent subheadings.
- Style existing data groups as data cards through `blocks` with `type: "data"` or section-level `data`; preserve every data line exactly.
- Style existing unnumbered closing headings such as "结语" as a section title with `"number": false`.
- Prefer `section`, `p`, `span`, `strong`, and `br` in the source snippet. Use `blockquote`, `ul`, `ol`, and `li` only when the content truly needs them.
- Never use tables for data. Convert tables into stacked data cards while preserving every cell's text.
- Never emit external image links. Replace existing image references with `【图片：这里放 xxx 图】`.
- Do not alter absolute investment language yourself; if risky language appears in the source, preserve it and optionally warn the user outside the generated article.

## Resources

- `references/wechat-mp-html-compat.md`: WeChat-compatible HTML rules and source notes.
- `scripts/generate_wechat_mp_html.py`: Deterministic generator for the preview file and source snippet.
