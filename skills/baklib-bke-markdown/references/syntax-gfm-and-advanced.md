# BKE Markdown · 表格、任务列表、标题与 GFM 扩展（第 12–19 节）

## 12. 表格 `table`

**GFM 管道表**；表头与表体间须有分隔行（至少两行时）。

```md
| 列 A | 列 B |
| --- | --- |
| 1 | 2 |
```

单元格内 `|` 写作 `\|`。

---

## 13. 任务列表 `taskList`

```md
- [ ] 未完成
- [x] 已完成
```

---

## 14. 文档标题区 `documentTitle`

全文**第一个块**的单行 `# …` 为文档标题区（非正文第一个 `#` 的特例）。

```md
# 纯文本标题
# 📌 我的文档
```

emoji 与标题间一个空格。

---

## 15. 正文标题 `heading`

常规则 `##`～`######`；正文内一级 `#` 行为以通用 Markdown/kramdown 为准。

---

## 16. 段落对齐与缩进

**段后 IAL**（kramdown），写在**该段下一行**：

```md
正文
{: align="center"}
```

```md
正文
{: data-indent="1"}
```

可合并：`{: align="right" data-indent="2"}`。

---

## 17. Markdown 源码块 `markdownBlock`

围栏语言名必须是 **`markdown-block`**（区别于普通代码块）；结束围栏与开始反引号数量相同；内可嵌套其它围栏。

````text
```markdown-block
## 内层标题
- 列表
```js
nested()
```
```
````

---

## 18. 高亮与行内样式 `highlight` / `textStyle`（v1）

无专用 BKE 句法：依赖 **行内 HTML**（如 `<mark>`、`<span style="…">`）在 BKE 管道内保留与往返；不保证第三方渲染器样式一致。

---

## 19. 标准 Markdown

列表、引用块、围栏代码块（语言**不是** `markdown-block`）、分割线等遵循 CommonMark/GFM/kramdown 惯例即可。

