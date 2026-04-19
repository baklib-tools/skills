# 指令（Liquid Tag）

以下除 **Liquid 内置** 外，均为 Baklib 主题引擎或站点扩展提供的指令。页面模板文件位于 `templates/*.liquid`，布局位于 `layout/*.liquid`（部分产品目录名写作 `layouts/`，以实际主题为准）。

## 可用范围总览

| 范围 | 指令 |
|------|------|
| **页面模板** | `layout`、`render`（内置）、`paginate_tag`、`query`、`search`、`track_event`、`form_tag`、`form_field_tag` |
| **布局** | `schema`、`response_status`、`response_type`、`meta_tags`、`set_meta_title`、`set_meta_description`、`set_meta_keywords`、`weixin_share_tag` |
| **布局 + 页面模板** | 布局侧指令仅在布局文件中生效；页面模板侧指令在布局中不可用（`layout` 指令写在页面模板中用于选布局） |

---

## `layout` — 指定布局

```liquid
{% layout "invite" %}
{% layout none %}
```

- 默认通常等价于 `theme` 布局。
- `none` 表示不包裹布局，直接输出页面模板内容。

---

## `render` — 渲染片段（Liquid 内置）

片段放在 `snippets/_名称.liquid`。

```liquid
{% render "tag", tag: my_tag %}
```

### 产品内置共享片段（`@shared/`）

写法：`{% render '@shared/片段名' %}`（片段名**不含**前缀 `_` 与扩展名 `.liquid`）。

- **机制**：以 `@shared/` 开头时，从**产品内置**共享片段读取，**不会**读当前主题自己的 `snippets/`。主题内普通 `{% render "foo" %}` 仍读本主题 `snippets/_foo.liquid`。
- **当前内置清单**（与仓库 `themes/shared/snippets/` 一致；若增删文件，须同步更新本文、`docs/theme-dev/liquid-tags.md` 与 [shared-snippets-source.md](shared-snippets-source.md) 中的原文）：

| `{% render %}` 写法 | 用途概要 |
|---------------------|----------|
| `{% render '@shared/paginate' %}` | 分页 UI（依赖上下文中已有 `paginate` 对象，通常放在 `paginate_tag` 块内或兼容上下文） |
| `{% render '@shared/breadcrumb' %}` | 面包屑（需传入 `breadcrumb` 数组，项含 `link_text`、`path`） |
| `{% render '@shared/empty' %}` | 空状态占位插画与布局（需传入 **`message`** 文案） |

```liquid
{% render '@shared/paginate' %}
{% render '@shared/breadcrumb', breadcrumb: page.breadcrumb %}
{% render '@shared/empty', message: '暂无内容' %}
```

**完整 Liquid 原文**（与实现逐字一致，便于复制到自有主题修改）：见 [shared-snippets-source.md](shared-snippets-source.md)。

---

## `paginate_tag` / `endpaginate_tag` — 集合分页

仅页面模板。块内可使用 **`paginate`** 对象（见 `objects-and-drops.md`）。

```liquid
{% paginate_tag site.pages, as: "items", per: 10 %}
  {% for p in items %}
    <a href="{{ p.path }}">{{ p.link_text }}</a>
  {% endfor %}
  {% if paginate.next_page %}
    <a href="{{ paginate.url_for[paginate.next_page] }}">下一页</a>
  {% endif %}
{% endpaginate_tag %}
```

| 参数 | 说明 |
|------|------|
| 第一参数 | 要分页的集合（如 `site.pages`、`page.children`） |
| `as: "变量名"` | 当前页条目的变量名，默认与集合变量相关 |
| `per: N` | 每页条数，最大 50 |
| `page: N` | 当前页码，默认来自请求参数 |

---

## `query` / `endquery` — 结构化查询

从 **`site.pages`** 或 **`page.*`** 等页面集合，或评论集合中筛选。块内为 **JSON** 条件（支持 `where`、`order_by`、`limit`、`offset` 等）。

```liquid
{% query faq_list from site.pages %}
  { "where": { "template_name_eq": "faq" }, "order_by": ["created_at desc"], "limit": 10 }
{% endquery %}
```

评论集合用法类似，条件字段以产品查询引擎为准。

---

## `search` / `endsearch` — 页内搜索

在页面模板中对 **`PagesDrop`** 集合做关键词搜索；结果写入 **`search`** 变量（见 `objects-and-drops.md`）。支持直达跳转、记录搜索日志等；块内可渲染结果列表。

属性示例：`keywords: ...`、`by_user: true|false`、`allow_empty_keywords: true|false`（具体以模板所需为准）。

---

## `track_event` — 行为统计

第一个参数为**事件名**（须在 `settings_schema.json` 的 `track_events` 中注册）。可选传入 `page: page` 等。

```liquid
{% assign event_name = 'resource_download' %}
{% track_event event_name, page: page %}
```

预览模式下不记录。

---

## `form_tag` / `endform_tag` — 站点表单

块内使用 Rails 风格 `form` 对象渲染字段（具体 helper 以各表单实现为准）。第一参数为**表单类型**字符串，部分表单可跟页面对象等参数。

| 表单名（首参） | 用途 |
|----------------|------|
| `feedback` | 当前页或指定页的反馈 |
| `delete_feedback` | 取消反馈 |
| `search` | 搜索表单 |
| `page` | 创建页面 |
| `edit_page` | 编辑页面 |
| `delete_page` | 删除页面 |
| `reply` | 评论回复 |
| `sign_in_with_password` | 密码登录 |
| `sign_in_with_baklib` | Baklib 账号登录 |
| `sign_in_with_sso` | SSO 登录 |
| `sign_out` | 登出 |

示例（摘自实现注释）：

```liquid
{% form_tag "feedback" %}
  ...
{% endform_tag %}
{% form_tag "feedback", page %}
  ...
{% endform_tag %}
```

---

## `form_field_tag` — 动态表单字段

用于模板变量表单中的自定义字段类型，例如：

| 字段类型名 | 说明 |
|------------|------|
| `richtext` | 富文本 |
| `color` | 颜色 |
| `tag` | 标签选择 |
| `range` | 范围 |
| `dam_image` | DAM 图片 |
| `dam_video` | DAM 视频 |

语法形态（示意）：

```liquid
{% form_field_tag 'dam_video', 'page[template_variables][video_url]', page, width: '256', height: '192' %}
```

参数顺序与选项以实际主题字段为准。

---

## 布局专用指令

### `schema` / `endschema`

块内为 **JSON**，描述模板/区块元数据（名称、设置项等），**不**直接输出到 HTML。

### `meta_tags`

输出基础 `<head>` meta（与 `set_meta_*` 配合）。

### `set_meta_title` / `set_meta_description` / `set_meta_keywords`

参数为字符串或表达式，设置 SEO 相关 meta。

### `weixin_share_tag`

微信分享相关标签与属性（按属性列表传入）。

### `response_status`

```liquid
{% response_status 404 %}
```

### `response_type`

```liquid
{% response_type "turbo_stream" %}
{% response_type "json" %}
{% response_type "xml" %}
{% response_type "html" %}
```

用于配合 Turbo Stream、JSON、整页 HTML 等响应。

---

## 小结：与旧文档对照

若你手中的文档只列出 `layout`、`render`、`paginate_tag`、`query`、`search`，请**补充**：**`track_event`**、**`form_tag`**、**`form_field_tag`**，以及布局中的 **`weixin_share_tag`** 等；页面模板与布局的指令集合**不同**，勿混用。
