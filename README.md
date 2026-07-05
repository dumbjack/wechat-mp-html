# wechat-mp-html

Codex skill for generating clean WeChat Official Account article HTML.

It turns an article into:

- `公众号 HTML 预览版.html`: browser preview with "复制全文" and "只选择全文" buttons.
- `公众号源码片段.txt`: inline-style HTML snippet for WeChat backend source mode, 135 Editor, Xiumi, or Yiban.

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

The skill asks Codex to preserve the article's facts and viewpoint, structure it into short mobile-readable sections, and call the bundled generator.

## WeChat Format

The source snippet is intentionally conservative:

- inline CSS only
- mainly `section`, `p`, `span`, `strong`, `br`
- no `script`, `style`, `table`, `iframe`, `form`, media tags, or external images
- image needs become placeholders such as `【图片：这里放 xxx 图】`

The preview file may contain CSS and JavaScript, but the toolbar is outside the copied article body.

---

# wechat-mp-html 中文说明

这是一个用于生成微信公众号文章 HTML 排版文件的 Codex skill。

它会输出：

- `公众号 HTML 预览版.html`：可在浏览器预览，带“复制全文”和“只选择全文”按钮。
- `公众号源码片段.txt`：可复制到微信公众号后台源码模式、135、秀米或壹伴。

## 安装

```bash
cp -R skills/wechat-mp-html ~/.codex/skills/
```

重启 Codex 后使用：

```text
使用 $wechat-mp-html，把下面文章转换成微信公众号 HTML 排版文件。
```

## 重点

- 不大幅改写原文观点。
- 不新增未经确认的数据。
- 财经、投资、加密货币判断保持克制。
- 表格数据改成卡片。
- 正文源码全部使用内联样式。
