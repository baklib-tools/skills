# 目录结构与命名

## 主题目录（常见布局）

```
themes/[scope]/[theme_name]/
├── assets/              # 静态资源（CSS/JS/图片等），通过 asset_url 等引用
├── config/
│   └── settings_schema.json   # 主题设置项、预览图、track_events 等元数据
├── layout/              # 布局（如 theme.liquid、error.liquid）
├── locales/             # 翻译文件，配合 `t` 过滤器
├── snippets/            # 片段，文件名以下划线开头
├── statics/             # 静态页模板（按路径映射，见下文）
├── src/                 # 可选：前端源码，构建后输出到 assets
└── templates/           # 页面模板
```

官方示例主题可参考 GitHub 组织 [baklib-templates](https://github.com/baklib-templates) 下的仓库。

## 页面模板（`templates/`）

| 类型 | 命名约定 | 说明 |
|------|----------|------|
| 首页 / 列表 | `index.liquid`、`index.样式名.liquid` | 与后台配置的模板名 + 样式对应 |
| 内容页 | `page.liquid`、`page.样式名.liquid` | 普通内容页 |
| 标签页 | `tag.liquid` | 标签聚合页 |
| 搜索页 | `search.liquid` | 站点搜索 |
| 反馈成功/失败等 | `feedback.liquid`、`feedback_success.liquid`、`feedback_error.liquid` 等 | 与路由返回的模板名一致 |
| Turbo / 提示 | `toast_error.liquid`、`feedback_turbo_stream.liquid` 等 | 按产品约定命名 |

## 布局（`layout/`）

- 默认整站布局多为 `theme.liquid`。
- 错误页等可使用 `error.liquid` 等。
- 在页面模板中用 `{% layout "theme" %}` 或 `{% layout "error" %}` 指定（**不带** `.liquid` 扩展名）。
- 使用 `{% layout none %}` 表示**不**再套布局，直接输出页面模板全文。

## 片段（`snippets/`）

- 文件名为 **`_名称.liquid`**（带下划线前缀）。
- 引用：`{% render "header" %}`（不写 `_` 与扩展名）。
- 支持子目录：`snippets/foo/_bar.liquid` → `{% render "foo/bar" %}`。

## 静态页（`statics/`）

- 文件路径即访问路径：根目录 `about.liquid` → 路径 `about`；`page/nav_tree.liquid` → 路径 `page/nav_tree`。
- 在模板中**不要写死** `/s/...`，应使用全局变量 **`statics`** 按路径取完整 URL（见 `objects-and-drops.md` 与 `limits-and-security.md`）。

## 资源（`assets/`）

- 建议分子目录如 `images/`、`javascripts/`、`stylesheets/`。
- 通过 `asset_url`、`stylesheet_tag`、`script_tag` 等生成 URL，避免手写静态路径。

## 主题名称（安装 / 标识）

安装主题时名称需满足常见约定（小写字母、数字、下划线，长度与正则以产品校验为准）。若用户给出含连字符的名称，可改为下划线以符合校验。
