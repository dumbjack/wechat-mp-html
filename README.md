# wechat-mp-html

Codex skill for generating clean WeChat Official Account article HTML.

By default, it turns an article into one file:

- `公众号 HTML 预览版.html`: browser preview with "复制全文" and "只选择全文" buttons.

Open the HTML file, click "复制全文", then paste into the WeChat Official Account web editor. The button copies only the article body, not the toolbar.

`公众号源码片段.txt` is optional. Generate it only for source-mode workflows such as 135 Editor, Xiumi, Yiban, WeChat API publishing, or debugging.

## Install

```bash
cp -R skills/wechat-mp-html ~/.codex/skills/
```

Restart Codex, then invoke:

```text
Use $wechat-mp-html to convert this article into WeChat Official Account HTML.
```

## Usage

中文：

```text
使用 $wechat-mp-html，把下面文章转换成微信公众号 HTML 排版文件。
```

English:

```text
Use $wechat-mp-html to convert this article into WeChat Official Account HTML.
```

The skill asks Codex to preserve the article text exactly and only add WeChat-compatible HTML wrappers, inline styles, and preview copy controls.

For advanced source-mode output, ask Codex to generate the optional source snippet too, or run the generator with `--outputs both`.

## WeChat Format

The copied article body is intentionally conservative:

- no article wording changes
- inline CSS only
- mainly `section`, `p`, `span`, `strong`, `br`
- no `script`, `style`, `table`, `iframe`, `form`, media tags, or external images
- image needs become placeholders such as `【图片：这里放 xxx 图】`
- existing level-3 headings and data groups can be styled without changing their text

The preview file may contain CSS and JavaScript, but the toolbar is outside the copied article body. The optional source snippet uses the same validated article body HTML.

---

# wechat-mp-html 中文说明

这是一个用于生成微信公众号文章 HTML 排版文件的 Codex skill。

默认只输出一个文件：

- `公众号 HTML 预览版.html`：可在浏览器预览，带“复制全文”和“只选择全文”按钮。

打开 HTML 文件，点击“复制全文”，再粘贴到微信公众号网页后台即可。按钮只复制正文区域，不复制顶部工具栏。

`公众号源码片段.txt` 是可选备用文件。只有在需要源码模式、135、秀米、壹伴、微信 API 发布或调试时才生成。

## 安装

```bash
cp -R skills/wechat-mp-html ~/.codex/skills/
```

重启 Codex 后使用：

```text
使用 $wechat-mp-html，把下面文章转换成微信公众号 HTML 排版文件。
```

## 重点

- 不改写、不润色、不总结、不扩写、不翻译正文。
- 不新增标题、小标题、结论、互动问题、免责声明或数据。
- 如果原文有三级小标题、表格或数据组，可以样式化或改成卡片，但必须逐字保留原文文字。
- 被复制的正文 HTML 全部使用内联样式。
