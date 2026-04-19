# 自定义过滤器

除 [Liquid 内置过滤器](https://shopify.github.io/liquid/) 外，Baklib 主题还提供下列过滤器（**必须使用已注册的名称**，见 `limits-and-security.md`）。

## 主题引擎内置

| 过滤器 | 说明 |
|--------|------|
| `asset_url` | 主题资源名 → URL |
| `dam_asset_url` | DAM 资源 ID → URL |
| `contains` | 字符串/数组是否包含 |
| `highlight` | 搜索高亮 |
| `inspect` | 调试输出 |
| `json` / `to_json` | 解析 JSON / 序列化为 JSON |
| `limit` | 限制数组长度 |
| `t` | 国际化翻译（依赖 locales） |
| `nav_tree` | 从 `site` 或 `page` 生成导航树，可传深度 |
| `order_by` | 集合排序，如 `order_by: "-published_at"` |
| `present?` / `blank?` / `presence` | 空值判断 |
| `reg_split` | 正则拆分 |
| `script_tag` / `stylesheet_tag` | 生成 `<script>` / `<link>` |
| `sanitize_html` / `sanitize_html_basic` / `sanitize_html_relaxed` | HTML 消毒 |
| `time_ago` | 相对时间 |
| `to_string` / `to_integer` / `to_float` | 类型转换 |
| `typeof` | 类型判断 |
| `tag` | 在 `site.tags` 上按关键词模糊筛选 |
| `can_access?` | 当前用户是否可访问给定页面对象 |

## 站点扩展

| 过滤器 | 说明 |
|--------|------|
| `where` | 页面集合按属性筛选：`where: 'template_name', 'post'` 或 `where: 'related', member_id` |
| `feedback_count` | 页面对象 → 反馈总次数 |
| `feedback_type_count` | 页面 + 类型 → 某类反馈次数 |
| `roots` | 评论集合 → 仅一级评论 |

## 示例

```liquid
{{ site.pages | order_by: "-published_at" | limit: 10 }}
{{ page | nav_tree: 2 }}
{{ "nav.home" | t }}
{{ now | time_ago }}
{{ page | feedback_count }}
{{ page.comments | roots }}
{{ site.pages | where: 'template_name', 'faq' }}
```
