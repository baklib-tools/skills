# 对象与变量

## 全局变量（各页可用）

| 变量 | 说明 |
|------|------|
| `site` | 当前站点 |
| `current_user` | 当前登录用户；未登录为空 |
| `params` | 当前请求查询参数（控制器白名单过滤后） |
| `now` | 当前时间（`Time.zone`） |
| `script_name` | 当前请求路径前缀；根路径部署时多为空，子目录部署时非空 |
| `statics` | 按路径取静态页完整 URL（见下文） |

站点层还会注入 **`statics`**：用法为 `statics['路径']`。

---

## 按场景传入的变量

以下为常见路由对应的模板变量（以实际控制器为准）。

| 场景 | 主要变量 |
|------|----------|
| 普通页面展示 | `page`、`sign_in_form`（登录表单对象） |
| 导航树接口页 `nav_tree` | `pages`、`expanded_ids`、`selected_ids`、`turbo_frame_request_id`、`depth` |
| 标签页 | `tag` |
| 搜索页 | `search`（搜索结果对象） |
| 反馈页 | `page`（被反馈对象）、成功/失败模板可能含 `success`、`errors` 等 |
| 评论回复等 | `reply` |
| 通用错误提示 | `errors`（数组或字符串） |
| 403 等 | `sign_in_form`、`page`（视模板而定） |

静态页（`statics/` 下模板）通常不传入业务变量，依赖全局变量与静态页内逻辑。

---

## `site`（站点）

| 属性/方法 | 说明 |
|-----------|------|
| `name` | 站点名称 |
| `index_path` | 首页路径（含前缀） |
| `search_path` | 搜索页路径 |
| `language` | 界面语言 |
| `time_zone` | 时区 |
| `favicon_url` | 站点图标 URL |
| `password_login_enabled` | 是否开启密码登录 |
| `baklib_login_enabled` | 是否允许 Baklib 账号登录 |
| `sso_login_enabled` | 是否开启 SSO |
| `settings` | 动态表单合并后的设置键值 |
| `theme_colors_css` / `theme_dark_colors_css` / `all_theme_colors_css` | 主题色 CSS 变量 |
| `nav_tree_path` | 导航树请求路径 |
| `pages` | 前台可访问页面集合 |
| `pages_in_list` | 参与列表展示的页面集合 |
| `tags` | 标签集合（支持 `site.tags['名称']`） |
| `users` | 成员集合 |
| `comments` | 站点下已发布评论 |
| `chat_messages` / `ai_chats` | AI 对话相关（视站点配置） |
| `plugins` | 插件配置（如反馈是否必填等） |
| `nav_tree(full_path, depth, query_params)` | 导航树数据 |
| `ai_search_enabled?` | 是否开启 AI 搜索能力 |
| `mcp_url` | 站点 MCP 入口 URL（若启用） |

---

## `page`（页面）

| 属性/方法 | 说明 |
|-----------|------|
| `id`、`slug`、`path`、`url` | 标识与链接；`path` 为站内路径，`url` 为绝对地址 |
| `link_text` | 导航/列表标题 |
| `full_slug` | 完整路径 slug |
| `template_name` / `template_style` | 模板与样式 |
| `markdown_path` / `markdown_url` | Markdown 导出路径（若启用） |
| `seo_title` / `seo_keywords` / `seo_description` | SEO 字段 |
| `settings` | 页面动态表单值 |
| `visits_count` | 访问量 |
| `edited_at` / `published_at` / `created_at` | 时间 |
| `author` | 创建者（`AuthorDrop`） |
| `parent` | 父页面 |
| `children` / `children_in_list` / `children_in_nav_menu` | 子页面集合 |
| `pages` / `pages_in_list` | 子孙页面 |
| `prev_page` / `next_page` | 同级上一篇/下一篇 |
| `comments` | 评论集合 |
| `breadcrumb` | 面包屑数组（`link_text`、`path`） |
| `nav_tree(depth, query_params)` | 以当前页为根的导航树 |
| `versions` | 历史版本列表 |
| `feedback_path` | 提交反馈的 path |
| `feedback_type_count(useful_type)` | 某类反馈数量 |
| `visitor_posted_feedback` | 当前访客是否已反馈 |
| `password_login_enabled` | 是否配置密码访问 |
| `highlighted_search_title` / `highlighted_search_content` | 搜索高亮片段 |

---

## `statics`

| 用法 | 说明 |
|------|------|
| `statics['page/nav_tree']` | 返回该静态页路径对应的完整 URL |

---

## `tag`（标签页）

| 属性 | 说明 |
|------|------|
| `name` | 标签名 |
| `path` | 标签页链接路径 |
| `color` / `bg_color` / `color_hsl` | 颜色 |
| `pages` | 带该标签的页面集合 |

---

## `search`（搜索页结果）

| 属性 | 说明 |
|------|------|
| `pages` | 搜索结果页列表 |
| `extends` | 扩展命中 |
| `keywords` | 关键词字符串（已转义） |
| `page_number` | 当前结果页码 |
| `tag` | 若与标签组合搜索时可能携带 |

---

## `paginate`（仅在 `paginate_tag` 块内）

| 属性 | 说明 |
|------|------|
| `total_count` | 总条数 |
| `total_pages` | 总页数 |
| `per_page` | 每页条数 |
| `current_page` | 当前页 |
| `prev_page` / `next_page` / `last_page` | 相邻页码 |
| `from` / `to` | 当前页序号范围 |
| `series` | 页码序列 |
| `page_param` | 页码 query 参数名 |
| `url_for` | 用页码取下页 URL：`paginate.url_for[n]` |

---

## `author` / `current_user`（成员）

常见字段：`id`、`name`、`avatar_url`、`avatar_path`、`pages_count`、`comment_count` 等；未登录无 `current_user`。

---

## `comment`（评论）

| 属性/方法 | 说明 |
|-----------|------|
| `id`、`body`、`created_at` | 基本信息 |
| `author` | 作者 |
| `reply_to_user` | 被回复用户 |
| `target` | 评论所属页面 |
| `parent` / `root` | 父评论与一级评论 |
| `replies` | 子回复 |
| `feedback_type_count` / `visitor_posted_feedback` | 与反馈交互 |

---

## 集合：`pages` / `tags`

- 可 `{% for %}` 遍历。
- 支持 `first` / `last`、与 `order_by`、`where`、`limit` 等过滤器组合。
- 按键取单页：`site.pages['/about']`（路径由系统解析，勿手写死无前缀路径）。

---

## `sign_in_form`

用于需要登录的场景，与 `page` 等一起传入；字段与方法以具体主题模板为准。
