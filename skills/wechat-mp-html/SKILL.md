---
name: wechat-mp-html
description: 撰写可粘贴到微信公众平台图文的 HTML：正文根节点 #js_content、inline style、无 class、标准「复制正文到公众号」按钮（ClipboardItem）；含版式组件配方与本地预览壳模板。在用户要生成公众号排版 HTML、135/微信兼容片段、或一键复制富文本到公众号后台时使用；不负责账号登录、群发与合规审核。
---

# 微信公众号图文 HTML（可复制富文本）

面向**本地排版 → 浏览器预览 → 复制 `#js_content` 到公众号后台**的流程。技术要点来自对 `mp.weixin.qq.com` 正文 DOM 的归纳与团队实践：**正文依赖 inline 样式**，粘贴后**不会**带上页面里的 `<style>`，故组件必须自带 `style="..."`。

## 何时打开详规

- 需要**完整约束、组件配方、文章类型模板**时，按需阅读 `references/` 下各篇。
- 需要**可直接改写的整页骨架**时，复制 [references/shell-template.html](references/shell-template.html) 到自有项目后编辑。

## 核心约定（必读）

1. **唯一粘贴对象**：`<section id="js_content">` 的 **outerHTML**（或编辑器要求的 innerHTML，以粘贴效果为准）；标题栏、作者、封面在公众号后台单独填写。
2. **样式**：正文内**只用 inline `style`**，**不要**依赖正文里的 `class`；页面 `<head>` 里样式仅用于本地预览，**不会**随复制进入公众号。
3. **复制按钮**：使用标准 **`#copy-to-weixin`** + **`#copy-toast`** + `ClipboardItem` 写入 `text/html` + `text/plain` 的实现，见 [references/constraints.md](references/constraints.md) 与 [references/shell-template.html](references/shell-template.html)；**禁止**沿用旧版 `.copy-btn` / `alert()` 片段。
4. **图片**：相对路径仅用于本地预览；**发布前**须替换为已在公众号素材库上传后的 **https URL**，或使用后台插入图片后的链接。

## 文档索引（`references/`）

| 文件 | 内容 |
|------|------|
| [constraints.md](references/constraints.md) | DOM 与标签约束、span/strong 规则、空格与换行、复制脚本规范 |
| [components.md](references/components.md) | 数字步骤标题、h2 大标题、总结框、导读等可复制 HTML 块 |
| [editorial-patterns.md](references/editorial-patterns.md) | 常见文章类型结构（教程/评测/更新汇总）与组件化思路 |
| [shell-template.html](references/shell-template.html) | 含预览样式与标准复制按钮的完整 HTML 壳（占位符需自行替换） |

## 能力边界（不做什么）

- 不代替用户登录公众平台、上传素材、群发或付费推广。
- 不保证编辑器版本差异下的 100% 样式保留；粘贴后若有个别样式丢失，可在后台用自带格式微调。
- 不嵌入第三方统计、外链跳转脚本等可能违反平台规则的代码。
