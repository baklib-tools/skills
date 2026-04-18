# BKE Markdown · 链接卡片、分栏、标注与嵌入（第 5–11 节）

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

