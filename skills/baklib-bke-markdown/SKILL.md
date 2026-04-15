---
name: baklib-bke-markdown
description: Self-contained guide for writing Baklib BKE Markdown (L1/L2, DAM dam-id, file colon-syntax, link cards, fragments, embeds, tables). Use when authoring or importing BKE Markdown, inserting DAM assets, or resolving DAM ids via MCP; not for editor implementation or maintaining product docs repos.
---

# BKE Markdown 撰写指南（独立副本）

本文件**单独发布即可使用**，不依赖其它仓库路径。BKE 是 Baklib 基于 Tiptap 的编辑器；交换格式在 **标准 Markdown / GFM** 之上增加 **圆括号第三段引号** 与 **成对 HTML 注释块（L2）**。

---

## 1. 键值与三层结构（总则）

### 1.1 圆括号第三段（L1 常见形态）

用于 `[文本](url "…")` 与 `![alt](url "…")`：第三段为英文引号包裹、**空格分隔**的片段。

- **默认**：各片段为 **`键=值`**（等号连接）。
- **唯一例外**：**DAM 文件卡片**独占段第三段用 **`键:值`**（冒号），如 `dam-id:553 dam-type:file`。
- **布尔/开关**：如 `controls=1`；具体键以各节为准。
- **`sync-master`**：**仅当**要「固定版本、不跟主版本」时书写。图片/链接/片段/L2 等多为 **`sync-master=false`**（等号）。文件卡片第三段为 **`sync-master:false`**（冒号）。默认跟随主版本时**省略**该键（勿写 `sync-master=true`）。

### 1.2 L2：成对 HTML 注释（块级自定义节点）

```md
<!-- bke:<类型名>#<配对id> 键=值 … -->
…块内正文（格式由类型决定）…
<!-- /bke:<类型名>#<配对id> -->
```

- **`<类型名>`**：如 `link-card`、`fragment`、`columns`、`callout`、`emoji`、`emoji-block`。
- **`<配对id>`**：仅用于**锚定这一对注释**，手写时起止**相同**即可；**不是** DAM 资源编号。
- **开放标签内属性**：一律 **`键=值`**；值含空格、`=`、引号或 URL 时，用**英文双引号**包住整个值，例如 `dam-desk-url="https://example.com/x"`。
- **属性名**不带 `bke-` 前缀（`bke:` 只出现在**类型名**里）。
- **安全**：属性值中勿出现字面量 **`--`**（HTML 注释结束序列）。
- **嵌套**：允许块内再套 L2；须按**栈**正确闭合。
- **`bke:link-card`**：**不写 `v=`**；**不写 `display=`**（块本身就是卡片）；**导出不写 `signed-id=`**，手写也不要加。
- **L3**：当前 v1 **不使用** Base64 payload 大块占位。

### 1.3 与 DOM / `data-*` 的关系

用户只写本文所述 **Markdown 字面量**；不要手写入库 HTML 的 `data-*`、`bke-role` 等——那是产品内部形态。

### 1.4 DAM 资源编号 `dam-id`

**`dam-id`**：工作台**打开该 DAM 资源时，浏览器地址栏中的编号**（多为数字）。链接、图片、文件卡片、片段嵌入等均用此概念；**配对 id** 与 **`dam-id`** 职责不同。

产品内部可能另有 `dam-file-id`、`link-id` 等字段名；**手写 Markdown 只使用本文出现的键名**（以 `dam-id` 为主）。

---

## 2. 文字链接与第三段（含站内）

### 2.1 基础

```md
[可见文字](https://example.com/path)
```

站内可用相对或绝对 URL：

```md
[代码开发](/kb/1/-/articles/ex4sdwmz)
```

### 2.2 第三段总表（非文件卡片）

引号内为 **空格分隔**；多数为 **`键=值`**。**文件卡片**见第 4 节（**冒号**语法）。

| 属性 | 必填 | 默认 | 说明 |
|------|:---:|------|------|
| `dam-id` | 否 | 无 | DAM 资源编号；第三段多为 `dam-id=…` |
| `dam-type` | 条件 | 因场景而异 | 文件卡片等在独占段用 `dam-type:`；其余见各节 |
| `internal-id` | 否 | 无 | 站内实体短码；**系统导出的 Markdown 会带，请勿改其值** |
| `internal-type` | 否 | 有 id 或推断成功时多为 `kb_article` | `kb_article`、`site_page` |
| `embed` | 条件 | 无 | `iframe` 或 `video` 表示嵌入块，须**独占一段** |
| `height` | 否 | 无 | 与 `embed=iframe` 等配合；须带单位（如 `400px`） |
| `display` | 否 | 无 | 链接展示，如 `title`、`card`；省略常为 URL 类 |
| `align` | 否 | 无 | `center`、`right` |
| `width` | 否 | 无 | 如 `50%` |
| `sync-master` | 否 | 省略 | **仅写 `sync-master=false`** 表示固定版本 |

示例：

```md
[文本](https://example.com "dam-id=12345")
```

### 2.3 站内解析链接

**导出形态**（不要改 `internal-id`）：

```md
[文章标题](/kb/1/-/articles/ex4sdwmz "internal-id=ex4sdwmz internal-type=kb_article")
```

**手写**可省略 `internal-id`，只写 URL + 类型：

```md
[文章标题](/kb/1/-/articles/ex4sdwmz "internal-type=kb_article")
```

| `internal-type` | 含义 |
|-----------------|------|
| `kb_article` | 知识库文章 |
| `site_page` | 站点页面 |

---

## 3. 图片 `image`（含 DAM）

**普通图**：`![alt](url)`。

**DAM 图**：第三段 **`键=值`**：

```md
![相册图](https://cdn.example.com/x.png "dam-id=267244 align=center width=50% sync-master=false")
```

无可用 `src` 时可用占位：

```md
![](<> "dam-id=267244")
```

| 属性 | 必填 | 默认 | 说明 |
|------|:---:|------|------|
| `dam-id` | 是 | 无 | DAM 资源编号 |
| `dam-desk-url` | 否 | 无 | **多仅导出**：工作台资源页链接；特殊字符按引号规则 |
| `align` | 否 | 无 | `left`、`center`、`right` |
| `width` | 否 | 无 | 如 `50%`、`400px` |
| `sync-master` | 否 | 省略 | 仅 `sync-master=false` |

---

## 4. 文件卡片 `file`（DAM）

块级；**独占一段**（段内仅一条链接）。第三段为 **`键:值`**（冒号），空格分隔。

```md
[需求.docx](https://your-desk.example/dam/dl/... "dam-id:553 dam-type:file")
```

- 链接文字：优先资源名。
- URL：优先下载链 → 工作台详情 → 可为 `#`（仅保留第三段）。

| 属性 | 必填 | 默认 | 说明 |
|------|:---:|------|------|
| `dam-id` | 是 | 无 | 资源编号 |
| `dam-type` | 是 | 无 | 仅 `file`、`video`、`audio` |
| `sync-master` | 否 | 省略 | 仅 **`sync-master:false`**（冒号） |
| `align` | 否 | 无 | `center`、`right` |
| `width` | 否 | 无 | 如 `50%` |

| `dam-type` | 说明 |
|------------|------|
| `file` | 文件下载卡片 |
| `video` | 视频播放器（DAM 视频优先用本类型，而非第 9 节原生 video） |
| `audio` | 音频播放器 |

---

## 5. 链接卡片 `link-card`

块级卡片：**URL 在块内标准链接行**；L2 注释类型名 **`bke:link-card`**。注释内**不要**写 `display=`（卡片即卡片展示）。

**形态 A**：整段仅一条链接时，可用第三段 `display=card` 等（见第 2 节），**不必**套 L2。

**形态 B**：多行描述等，用 L2：

```md
<!-- bke:link-card#n1 align=left -->
[链接标题](https://example.com)
> 这里是描述（可多行）。
<!-- /bke:link-card#n1 -->
```

**L2 开放标签属性**：

| 属性 | 必填 | 默认 | 说明 |
|------|:---:|------|------|
| `align` | 否 | `left` | `left`、`center`、`right` |
| `icon` | 否 | 无 | 图标 URL 或产品内标识 |
| `width` | 否 | 无 | 如 `50%` |

**块内**：第一行一条 `[文本](url "可选第三段")`（可含 `dam-id=` 等）；可选连续 `>` 引用行为描述；**同一卡片仅一行主链接**。

```md
<!-- bke:link-card#a1B2c3d4 align=center width=50% -->
[Example 标题](https://example.com)
> 描述。
<!-- /bke:link-card#a1B2c3d4 -->
```

---

## 6. 知识片段嵌入 `fragment`

L2，类型名 **`bke:fragment`**；**必须**绑定 `dam-id=`（开放标签内，等号）。

```md
<!-- bke:fragment#a3Bc4412 dam-id=267244 -->
快照可任意写；导入时忽略，正文以 DAM 为准。
<!-- /bke:fragment#a3Bc4412 -->
```

| 属性 | 必填 | 默认 | 说明 |
|------|:---:|------|------|
| `dam-id` | 是 | 无 | 被嵌入片段的资源编号 |
| `sync-master` | 否 | 省略 | 仅 `sync-master=false` |
| `dam-desk-url` | 否 | 无 | **多仅导出** |

---

## 7. 分栏 `columns`

外层 **`bke:columns`**，每栏 **`bke:column`**，栏内 GFM。

```md
<!-- bke:columns#x7Kp9021 count=2 layout="1:1" -->

<!-- bke:column#a3Bc4412 -->
第一栏
<!-- /bke:column#a3Bc4412 -->

<!-- bke:column#d2Ef5912 -->
第二栏
<!-- /bke:column#d2Ef5912 -->

<!-- /bke:columns#x7Kp9021 -->
```

**`bke:columns` 开放标签**：

| 属性 | 必填 | 默认 | 说明 |
|------|:---:|------|------|
| `count` | 否 | 无 | 栏数，如 2～5 |
| `layout` | 否 | 无 | 如 `1:1`、`1:2:1`；含冒号建议 `layout="1:2:1"` |

子块 `bke:column` 的配对 id 须全局不冲突。

---

## 8. 标注框 `callout`

L2 **`bke:callout`**，块内 GFM；可选首行单独 emoji。

```md
<!-- bke:callout#c1 bg-color=#f0f0f0 -->
💡

这是一段**标注**正文。
<!-- /bke:callout#c1 -->
```

| 属性 | 必填 | 说明 |
|------|:---:|------|
| `bg-color` | 否 | 背景色，如 `#f0f0f0` |
| `border-color` | 否 | 边框色 |
| `text-color` | 否 | 文字色 |

---

## 9. 嵌入网页 `iframe`

**独占一段**；第三段 `embed=iframe`，`height` **必须带单位**。

```md
[https://example.com/embed](https://example.com/embed "embed=iframe height=400px")
```

---

## 10. 原生视频 `video`（非 DAM 文件卡片）

**独占一段**；第三段 **`embed=video`**，可含 `width`、`height`、`poster=`、`preload=`、`playsinline=`；布尔可用 `controls=1` 等。

```md
[https://cdn.example.com/a.mp4](https://cdn.example.com/a.mp4 "embed=video width=640 height=360 poster=https://example.com/p.jpg controls=1")
```

**DAM 托管视频**：用第 4 节 **`dam-type:video`** 文件卡片，勿与本节混淆。

---

## 11. 表情 `emoji` / `emoji-block`

L2；行内 **`bke:emoji`**，块级 **`bke:emoji-block`**。开放标签**无额外属性**。注释对之间为**单个** Emoji 字素。

```md
<!-- bke:emoji#a1B2c3d4 -->👍<!-- /bke:emoji#a1B2c3d4 -->
```

```md
<!-- bke:emoji-block#a1B2c3d4 -->👍<!-- /bke:emoji-block#a1B2c3d4 -->
```

---

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

---

## 20. DAM 与 MCP（可选）

- **编号来源**：界面地址栏、用户告知、或 **Baklib 工作区 MCP**（工具名因发行版可能为 `dam_upload_entity`、`dam_get_entity`、`dam_list_entities` 等）。
- **`dam_upload_entity`**：本地 `file_path` 上传；`type` 常见 `image` / `file` / `video` / `audio`；响应中的**数字 `id`** 即手写 Markdown 的 **`dam-id`**。
- **`dam_get_entity`**：按 `id` 查元数据（名称、类型等）写 `alt` 或链接文字；若工具支持 `include_signed_id`，用于**编辑器 HTML** 等场景——**BKE Markdown 用户向仍以 `dam-id` 为主**。
- **`dam_list_entities`**：分页筛选，从条目取 `id`。
- 调用前以**当前环境 MCP 工具描述**为准（参数必填项、枚举）。
- 通常**无需**单独「下载文件」工具即可写 Markdown；落地文件用实体详情中的 URL 或产品下载能力。

---

## 21. 自检清单

- [ ] 文件卡片第三段是否为 **`dam-id:`** / **`dam-type:`** / **`sync-master:false`**（冒号），未与图片的 `=` 混用？
- [ ] L2 是否**成对**且 **`#<配对id>`** 起止一致？
- [ ] 需绑 DAM 处是否写上 **`dam-id`**（或文件卡片的 **`dam-id:`**）？
- [ ] `sync-master` 是否仅在「固定版本」时书写（图片/链接/片段为 `false`，文件卡片为 `:false`）？
- [ ] 是否避免在属性值中写字面量 **`--`**？
- [ ] `bke:link-card` 注释内是否**未写** `display=` / `signed-id=`？

---

## 22. 版本与复制说明

- 语法以 Baklib BKE **面向用户的交换格式**为准；产品升级可能导致细节增减，以当前编辑器导入结果为准。
- 复制本技能给他人时：**仅分发本 `SKILL.md` 即可**；若需追新，应对比 Baklib 官方发布的 BKE Markdown 说明。
