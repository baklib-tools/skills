# BKE Markdown · 总则、链接、图片与文件卡片（第 1–4 节）

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

