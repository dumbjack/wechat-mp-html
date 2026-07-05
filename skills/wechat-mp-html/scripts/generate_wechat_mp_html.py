#!/usr/bin/env python3
"""Generate WeChat Official Account HTML preview and source snippet.

Input is a UTF-8 JSON article structure prepared by Codex. Output is:
- 公众号 HTML 预览版.html
- 公众号源码片段.txt
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any


PREVIEW_NAME = "公众号 HTML 预览版.html"
SNIPPET_NAME = "公众号源码片段.txt"

FORBIDDEN_TAGS = {
    "doctype",
    "html",
    "head",
    "body",
    "script",
    "style",
    "table",
    "iframe",
    "form",
    "input",
    "video",
    "audio",
    "canvas",
    "object",
    "embed",
    "img",
}

LIMIT_WARNING_CHARS = 18000
LIMIT_MAX_CHARS = 20000
LIMIT_MAX_BYTES = 1024 * 1024

STYLE_CONTAINER = (
    "margin:0 auto;padding:0 16px 28px;"
    "font-size:16px;line-height:1.82;color:#333;background:#fff;"
)
STYLE_TITLE_CARD = (
    "margin:0 0 18px;padding:22px 20px;border-radius:8px;background:#111;color:#fff;"
)
STYLE_TITLE = "margin:0;font-size:24px;line-height:1.35;color:#fff;font-weight:700;"
STYLE_SUBTITLE = "margin:10px 0 0;font-size:14px;line-height:1.7;color:#d6d6d6;"
STYLE_META = "margin:12px 0 0;font-size:13px;line-height:1.6;color:#b8b8b8;"
STYLE_CONCLUSION = (
    "margin:0 0 22px;padding:14px 16px;border-left:4px solid #111;"
    "border-radius:6px;background:#f7f7f7;"
)
STYLE_P = "margin:0 0 16px;font-size:16px;line-height:1.8;"
STYLE_STRONG = "font-weight:700;color:#111;"
STYLE_SECTION = "margin:30px 0 0;"
STYLE_SECTION_HEAD = "margin:0 0 18px;text-align:center;"
STYLE_NUM = (
    "display:inline-block;margin:0 0 10px;padding:3px 12px;border-radius:999px;"
    "background:#111;color:#fff;font-size:13px;line-height:1.5;font-weight:700;"
)
STYLE_SECTION_TITLE = (
    "display:block;margin:0;font-size:19px;line-height:1.45;color:#111;"
    "font-weight:700;text-align:center;"
)
STYLE_SUBHEADING = (
    "margin:24px 0 12px;padding:0 0 0 10px;border-left:3px solid #111;"
    "font-size:16px;line-height:1.7;color:#111;font-weight:700;"
)
STYLE_DATA_CARD = (
    "margin:0 0 18px;padding:15px 16px;border-radius:8px;background:#f8f8f8;"
)
STYLE_DATA_ROW = "margin:0 0 9px;font-size:15px;line-height:1.75;"
STYLE_HIGHLIGHT = (
    "margin:0 0 18px;padding:15px 16px;border:1px solid #f0dfc2;"
    "border-radius:8px;background:#fff9ef;"
)
STYLE_IMAGE = (
    "margin:0 0 18px;padding:13px 15px;border-radius:8px;background:#f7f7f7;"
    "color:#666;font-size:15px;line-height:1.75;text-align:center;"
)
STYLE_LIST = "margin:0 0 18px;padding-left:22px;"
STYLE_LI = "margin:0 0 8px;font-size:16px;line-height:1.8;"
STYLE_QUOTE = (
    "margin:0 0 18px;padding:12px 16px;border-left:4px solid #d8d8d8;"
    "background:#f8f8f8;color:#555;"
)
STYLE_CLOSING = (
    "margin:34px 0 0;padding:18px 18px;border-radius:8px;background:#111;color:#fff;"
)
STYLE_CLOSING_LABEL = "margin:0 0 8px;font-size:14px;line-height:1.7;color:#d6d6d6;"
STYLE_CLOSING_Q = "margin:0;font-size:17px;line-height:1.75;color:#fff;font-weight:700;"


def as_list(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    return [value]


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def render_inline(text: Any) -> str:
    raw = clean_text(text)
    if not raw:
        return ""

    parts: list[str] = []
    pattern = re.compile(r"(\*\*.+?\*\*|__.+?__)", re.S)
    pos = 0
    for match in pattern.finditer(raw):
        parts.append(html.escape(raw[pos : match.start()]).replace("\n", "<br>"))
        token = match.group(0)[2:-2]
        parts.append(
            f'<strong style="{STYLE_STRONG}">'
            f'{html.escape(token).replace(chr(10), "<br>")}</strong>'
        )
        pos = match.end()
    parts.append(html.escape(raw[pos:]).replace("\n", "<br>"))
    return "".join(parts)


def p(text: Any, style: str = STYLE_P) -> str:
    body = render_inline(text)
    if not body:
        return ""
    return f'<p style="{style}">{body}</p>'


def split_paragraphs(items: Any) -> list[str]:
    paragraphs: list[str] = []
    for item in as_list(items):
        text = clean_text(item)
        if not text:
            continue
        chunks = [chunk.strip() for chunk in re.split(r"\n\s*\n", text) if chunk.strip()]
        paragraphs.extend(chunks or [text])
    return paragraphs


def render_title_card(article: dict[str, Any]) -> str:
    title = clean_text(article.get("title"))
    subtitle = clean_text(article.get("subtitle"))
    meta = clean_text(article.get("meta") or article.get("byline"))
    if not title and not subtitle and not meta:
        return ""
    lines = [
        f'<section style="{STYLE_TITLE_CARD}">',
    ]
    if title:
        lines.append(f'<p style="{STYLE_TITLE}">{render_inline(title)}</p>')
    if subtitle:
        lines.append(f'<p style="{STYLE_SUBTITLE}">{render_inline(subtitle)}</p>')
    if meta:
        lines.append(f'<p style="{STYLE_META}">{render_inline(meta)}</p>')
    lines.append("</section>")
    return "\n".join(lines)


def render_conclusion(article: dict[str, Any]) -> str:
    conclusion = clean_text(
        article.get("conclusion")
        or article.get("one_sentence_conclusion")
    )
    if not conclusion:
        return ""
    return (
        f'<section style="{STYLE_CONCLUSION}">'
        f'<p style="margin:0;font-size:16px;line-height:1.8;color:#111;font-weight:700;">'
        f'{render_inline(conclusion)}</p></section>'
    )


def render_data_card(data: Any) -> str:
    rows: list[str] = []
    for item in as_list(data):
        if isinstance(item, dict):
            label = clean_text(item.get("label") or item.get("name") or item.get("key"))
            value = clean_text(item.get("value") or item.get("text"))
            text = f"{label}：{value}" if label and value else label or value
        else:
            text = clean_text(item)
        if text:
            rows.append(f'<p style="{STYLE_DATA_ROW}">{render_inline(text)}</p>')
    if not rows:
        return ""
    rows[-1] = rows[-1].replace("margin:0 0 9px;", "margin:0;")
    return f'<section style="{STYLE_DATA_CARD}">\n' + "\n".join(rows) + "\n</section>"


def render_highlights(values: Any) -> str:
    blocks: list[str] = []
    for value in as_list(values):
        text = clean_text(value)
        if text:
            blocks.append(
                f'<section style="{STYLE_HIGHLIGHT}">'
                f'<p style="margin:0;font-size:16px;line-height:1.85;color:#111;font-weight:700;">'
                f'{render_inline(text)}</p></section>'
            )
    return "\n".join(blocks)


def render_subheading(text: Any) -> str:
    body = render_inline(text)
    if not body:
        return ""
    return f'<p style="{STYLE_SUBHEADING}">{body}</p>'


def render_images(values: Any) -> str:
    blocks: list[str] = []
    for value in as_list(values):
        text = clean_text(value)
        if not text:
            continue
        if text.startswith("【图片"):
            placeholder = text
        else:
            placeholder = f"【图片：这里放 {text}】"
        blocks.append(f'<p style="{STYLE_IMAGE}">{html.escape(placeholder)}</p>')
    return "\n".join(blocks)


def render_list(values: Any, ordered: bool = False) -> str:
    items = [clean_text(item) for item in as_list(values) if clean_text(item)]
    if not items:
        return ""
    tag = "ol" if ordered else "ul"
    rows = [f'<li style="{STYLE_LI}">{render_inline(item)}</li>' for item in items]
    return f'<{tag} style="{STYLE_LIST}">\n' + "\n".join(rows) + f"\n</{tag}>"


def render_section(section: dict[str, Any], index: int) -> str:
    title = clean_text(section.get("title") or section.get("heading"))
    lines = [f'<section style="{STYLE_SECTION}">']
    if title:
        number_setting = section.get("number", section.get("show_number", True))
        if number_setting is False:
            number_markup = ""
        elif isinstance(number_setting, str):
            number_markup = f'<span style="{STYLE_NUM}">{render_inline(number_setting)}</span>'
        else:
            number_markup = f'<span style="{STYLE_NUM}">{index:02d}</span>'
        lines.extend(
            [
                f'<section style="{STYLE_SECTION_HEAD}">',
                number_markup,
                f'<span style="{STYLE_SECTION_TITLE}">{render_inline(title)}</span>',
                "</section>",
            ]
        )

    blocks = section.get("blocks")
    if blocks:
        for block in as_list(blocks):
            rendered = render_block(block)
            if rendered:
                lines.append(rendered)
    else:
        for paragraph in split_paragraphs(section.get("paragraphs") or section.get("body")):
            lines.append(p(paragraph))

        quote = clean_text(section.get("quote") or section.get("blockquote"))
        if quote:
            lines.append(f'<blockquote style="{STYLE_QUOTE}">{p(quote, "margin:0;font-size:15px;line-height:1.8;color:#555;")}</blockquote>')

        data = section.get("data", section.get("data_cards"))
        rendered_data = render_data_card(data)
        if rendered_data:
            lines.append(rendered_data)

        highlights = (
            section.get("highlights")
            or section.get("highlight_cards")
            or section.get("judgement_cards")
            or section.get("judgment_cards")
        )
        rendered_highlights = render_highlights(highlights)
        if rendered_highlights:
            lines.append(rendered_highlights)

        bullets = render_list(section.get("bullets"))
        if bullets:
            lines.append(bullets)

        ordered = render_list(section.get("ordered") or section.get("steps"), ordered=True)
        if ordered:
            lines.append(ordered)

        images = render_images(section.get("images") or section.get("image_placeholders"))
        if images:
            lines.append(images)

    lines.append("</section>")
    return "\n".join(lines)


def render_block(block: Any) -> str:
    if isinstance(block, str):
        return p(block)
    if not isinstance(block, dict):
        return ""
    block_type = clean_text(block.get("type") or block.get("kind")).lower()
    if not block_type:
        if "subheading" in block or "heading" in block:
            block_type = "subheading"
        elif "data" in block or "items" in block:
            block_type = "data"
        elif "highlight" in block:
            block_type = "highlight"
        else:
            block_type = "paragraph"

    if block_type in {"subheading", "h3", "minor-heading"}:
        return render_subheading(block.get("text") or block.get("subheading") or block.get("heading"))
    if block_type in {"data", "data-card", "data_cards"}:
        return render_data_card(block.get("items") or block.get("data") or block.get("rows"))
    if block_type in {"highlight", "highlight-card", "judgment", "judgement"}:
        return render_highlights([block.get("text") or block.get("highlight")])
    if block_type in {"quote", "blockquote"}:
        quote = clean_text(block.get("text") or block.get("quote"))
        return f'<blockquote style="{STYLE_QUOTE}">{p(quote, "margin:0;font-size:15px;line-height:1.8;color:#555;")}</blockquote>' if quote else ""
    if block_type in {"list", "bullets", "ul"}:
        return render_list(block.get("items") or block.get("bullets"))
    if block_type in {"ordered", "steps", "ol"}:
        return render_list(block.get("items") or block.get("steps"), ordered=True)
    if block_type in {"image", "images"}:
        return render_images(block.get("items") or block.get("images") or block.get("text"))
    return p(block.get("text") or block.get("paragraph") or block.get("body"))


def render_closing(article: dict[str, Any]) -> str:
    closing = article.get("closing")
    label = ""
    question = ""
    if isinstance(closing, dict):
        label = clean_text(closing.get("label"))
        question = clean_text(closing.get("question") or closing.get("text"))
    else:
        question = clean_text(closing)
    question = clean_text(article.get("closing_question")) or question
    if not question:
        return ""
    lines = [f'<section style="{STYLE_CLOSING}">']
    if label:
        lines.append(f'<p style="{STYLE_CLOSING_LABEL}">{render_inline(label)}</p>')
    lines.append(f'<p style="{STYLE_CLOSING_Q}">{render_inline(question)}</p>')
    lines.append("</section>")
    return "".join(lines)


def render_snippet(article: dict[str, Any]) -> str:
    lines = [f'<section style="{STYLE_CONTAINER}">', render_title_card(article)]
    conclusion = render_conclusion(article)
    if conclusion:
        lines.append(conclusion)
    for paragraph in split_paragraphs(article.get("intro") or article.get("opening")):
        lines.append(p(paragraph))
    for index, section in enumerate(as_list(article.get("sections")), start=1):
        if isinstance(section, dict):
            lines.append(render_section(section, index))
    closing = render_closing(article)
    if closing:
        lines.append(closing)
    lines.append("</section>")
    return "\n".join(line for line in lines if line).strip() + "\n"


def html_to_text(markup: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", markup, flags=re.I)
    text = re.sub(r"</p\s*>", "\n\n", text, flags=re.I)
    text = re.sub(r"</section\s*>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def render_preview(snippet: str, title: str) -> str:
    safe_title = html.escape(title or "公众号 HTML 预览版")
    plain_text_js = json.dumps(html_to_text(snippet), ensure_ascii=False)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_title}</title>
  <link rel="icon" href="data:,">
  <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: #f3f3f3; color: #2b2b2b; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    .toolbar {{ position: fixed; top: 0; left: 0; right: 0; z-index: 10; display: flex; gap: 10px; align-items: center; padding: 10px 14px; background: rgba(255,255,255,.94); border-bottom: 1px solid #e8e8e8; backdrop-filter: blur(8px); }}
    .toolbar button {{ border: 0; border-radius: 6px; padding: 8px 12px; font-size: 14px; line-height: 1.2; cursor: pointer; }}
    .toolbar .primary {{ background: #111; color: #fff; }}
    .toolbar .secondary {{ background: #ededed; color: #111; }}
    .toolbar .status {{ margin-left: auto; color: #666; font-size: 13px; }}
    .page {{ max-width: 430px; margin: 0 auto; padding: 62px 0 28px; background: #fff; min-height: 100vh; }}
  </style>
</head>
<body>
  <section class="toolbar" aria-label="copy tools">
    <button class="primary" type="button" onclick="copyArticle()">复制全文</button>
    <button class="secondary" type="button" onclick="selectArticle()">只选择全文</button>
    <span class="status" id="copy-status">只复制正文区域</span>
  </section>
  <main class="page">
    <section id="wechat-article">
{snippet}
    </section>
  </main>
  <script>
    const article = document.getElementById('wechat-article');
    const statusNode = document.getElementById('copy-status');
    const plainText = {plain_text_js};

    function selectArticle() {{
      const range = document.createRange();
      range.selectNodeContents(article);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      statusNode.textContent = '已选中正文';
    }}

    async function copyArticle() {{
      const html = article.innerHTML;
      try {{
        if (navigator.clipboard && window.ClipboardItem) {{
          const item = new ClipboardItem({{
            'text/html': new Blob([html], {{ type: 'text/html' }}),
            'text/plain': new Blob([plainText], {{ type: 'text/plain' }})
          }});
          await navigator.clipboard.write([item]);
        }} else {{
          selectArticle();
          document.execCommand('copy');
        }}
        statusNode.textContent = '已复制正文';
      }} catch (error) {{
        selectArticle();
        statusNode.textContent = '请手动复制';
        alert('浏览器限制了自动复制，已为你选中正文，请按 Ctrl/Cmd + C 复制。');
      }}
    }}
  </script>
</body>
</html>
"""


def validate_snippet(snippet: str) -> list[str]:
    warnings: list[str] = []
    forbidden = sorted(
        tag
        for tag in FORBIDDEN_TAGS
        if re.search(rf"<\s*/?\s*{re.escape(tag)}(?:\s|>|/)", snippet, flags=re.I)
    )
    if forbidden:
        raise ValueError("Forbidden source snippet tag(s): " + ", ".join(forbidden))
    if re.search(r"https?://", snippet, flags=re.I):
        warnings.append("Source snippet contains http(s) text. Confirm it is not an external image URL.")
    char_count = len(snippet)
    byte_count = len(snippet.encode("utf-8"))
    if char_count > LIMIT_MAX_CHARS:
        warnings.append(f"Source snippet exceeds {LIMIT_MAX_CHARS} characters: {char_count}.")
    elif char_count > LIMIT_WARNING_CHARS:
        warnings.append(f"Source snippet is close to WeChat's character limit: {char_count}.")
    if byte_count > LIMIT_MAX_BYTES:
        warnings.append(f"Source snippet exceeds 1 MB: {byte_count} bytes.")
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article_json", help="UTF-8 JSON file describing the article")
    parser.add_argument("--out-dir", default=".", help="Directory for generated files")
    parser.add_argument("--preview-name", default=PREVIEW_NAME)
    parser.add_argument("--snippet-name", default=SNIPPET_NAME)
    args = parser.parse_args()

    input_path = Path(args.article_json)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    article = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(article, dict):
        raise SystemExit("Article JSON must be an object.")

    snippet = render_snippet(article)
    warnings = validate_snippet(snippet)
    preview = render_preview(snippet, clean_text(article.get("title")))

    snippet_path = out_dir / args.snippet_name
    preview_path = out_dir / args.preview_name
    snippet_path.write_text(snippet, encoding="utf-8")
    preview_path.write_text(preview, encoding="utf-8")

    print(f"Wrote: {preview_path}")
    print(f"Wrote: {snippet_path}")
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
