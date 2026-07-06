# WeChat MP HTML Compatibility

Use these rules when generating article HTML for the WeChat Official Account backend, 135 Editor, Xiumi, Yiban, or source-mode editors. The article text is immutable: preserve original wording exactly.

## Source Facts

- WeChat official article `content` supports HTML tags, removes JavaScript, must remain under the documented character/size limits, and filters external image URLs.
- Article body images should come from WeChat's "upload article image" API or be uploaded manually in the WeChat backend.
- Images uploaded through the official article image API support jpg/png and must be under 1 MB.

Primary references:

- https://developers.weixin.qq.com/doc/service/api/draftbox/draftmanage/api_draft_add.html
- https://developers.weixin.qq.com/doc/service/api/material/permanent/api_uploadimage.html
- https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Adding_Permanent_Assets.html

## Output Types

Generate the preview HTML by default:

- `公众号 HTML 预览版.html`: complete browser preview with `doctype`, `html`, `head`, `body`, `style`, and `script`. The toolbar may contain "复制全文" and "只选择全文" buttons.

Generate the source snippet only when the user explicitly asks for source mode, 135 Editor, Xiumi, Yiban, API publishing, or debugging:

- `公众号源码片段.txt`: body-only HTML snippet for source-mode copy. It must not contain `doctype`, `html`, `head`, `body`, `script`, or `style` tags.

## Safe Body Tags

Prefer:

- `section`
- `p`
- `span`
- `strong`
- `br`

Use sparingly:

- `blockquote`
- `ul`
- `ol`
- `li`

Do not use in the source snippet:

- `table`
- `iframe`
- `script`
- `style`
- `form`
- `input`
- `video`
- `audio`
- `canvas`
- `object`
- `embed`
- `img`

## CSS Rules

The source snippet must use inline CSS only.

Allowed style properties:

- `font-size`
- `line-height`
- `color`
- `background`
- `padding`
- `margin`
- `border`
- `border-radius`
- `font-weight`
- `text-align`
- `box-sizing`
- `letter-spacing`

Avoid external CSS, complex selectors, animation, media queries, and complex positioning in the source snippet.

## Visual System

- Main color: `#111`
- Body color: `#2b2b2b`
- Secondary text: `#666`
- Pale gray: `#f7f7f7` or `#f8f8f8`
- Highlight background: `#fff9ef`
- Highlight border: `#f0dfc2`
- Base font size: around `16px`
- Line height: `1.75` to `1.9`

Use a dark title card, a gray conclusion card with a dark left border, centered numbered section headings, gray data cards, pale-yellow judgment cards, and a dark closing question card only when the source article already contains the corresponding text.

## Content Rules

- Do not rewrite, summarize, polish, shorten, expand, translate, reorder, or add article content.
- Do not create new titles, subtitles, section headings, conclusions, highlighted judgments, labels, closing questions, disclaimers, or transitions unless the exact text already appears in the source article or the user explicitly provides it.
- Preserve paragraph boundaries from the source. Do not split or merge paragraphs for rhythm.
- Preserve existing bold emphasis only; do not add new bold emphasis.
- Style existing level-3 headings as compact subheadings when the source explicitly marks them.
- Style existing unnumbered closing headings such as "结语" as unnumbered section titles.
- Convert Markdown tables into data cards only when every cell's text is preserved verbatim.
- Convert compact source data groups into data cards only when every line's text is preserved verbatim and the original order is retained.
- Replace existing external image references with text placeholders such as `【图片：这里放 xxx 图】`; do not invent image needs.
- If finance, investing, crypto, or market language seems risky, warn the user outside the generated article instead of changing the article text.

## Preview Copy Rules

The preview toolbar must not be inside the copied article body. The "复制全文" button should:

- Copy only the body article region.
- Prefer rich `text/html`.
- Also provide `text/plain`.
- Fall back to selecting the article region and prompting manual copy when automatic copy fails.

The "只选择全文" button should select only the body article region.
