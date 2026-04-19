---
name: baklib-theme-dev
description: Baklib 站点主题（模板）开发：Liquid 目录结构、命名、全局与场景变量、对象属性与方法、自定义指令与过滤器、静态页 URL、种子与迁移、资源与行为限制。在用户编写或修改 .liquid 模板、snippets、layouts、statics、settings_schema、或排查模板语法与变量时使用；本技能自包含规范说明，不依赖外站文档。
---

# Baklib 模板开发

Baklib 站点前台使用 **[Liquid](https://shopify.github.io/liquid/)** 模板（与 Shopify 模板体系相近）。模板作者通过 **对象（变量）**、**指令**（控制逻辑，官方称 Tag）、**过滤器**（转换输出）组合页面。

## 术语

| 术语 | 含义 |
|------|------|
| 对象 | 在 `{{ }}` 中输出的变量或属性，如 `{{ site.name }}` |
| 指令 | 在 `{% %}` 中控制流程；本文称「指令」以免与站点内容「标签」混淆 |
| 过滤器 | 在 `{{ }}` 内用 `\|` 连接，如 `{{ site.pages \| order_by: "-published_at" }}` |

## 文档索引（`references/`）

按需打开下列文件获取完整表格与示例：

| 文件 | 内容 |
|------|------|
| [directory-and-naming.md](references/directory-and-naming.md) | 主题目录、`templates`/`layout`/`snippets`/`statics`/`assets`/`config`/`locales`/`src` 与文件命名 |
| [liquid-tags.md](references/liquid-tags.md) | 页面模板与布局中的自定义指令、`render`、`form_tag`、`track_event`、`paginate_tag`、`query`、`search` 等 |
| [objects-and-drops.md](references/objects-and-drops.md) | 全局变量、按场景传入的变量、`site` / `page` / `tag` / `search` / `paginate` 等对象 |
| [filters.md](references/filters.md) | 产品提供的自定义过滤器（含站点扩展） |
| [limits-and-security.md](references/limits-and-security.md) | 主题名规则、分页上限、`strict_filters`、反向代理与路径前缀 |
| [seeds-and-migrations.md](references/seeds-and-migrations.md) | `seeds/` 初始化数据与 `migrations/` 主题迁移 |

## 能力边界

- **说明对象**：面向在 Baklib 站点主题中编写 Liquid 的开发者；**不**描述 Baklib 应用后台或 Rails 实现细节。
- **与标准 Liquid 的关系**：除下列自定义能力外，可使用 [Liquid 标准语法与内置过滤器](https://shopify.github.io/liquid/)。
- **版本差异**：具体站点是否开启登录、搜索、反馈、AI 等功能以租户配置为准；模板中应对空值做判断（如 `{% if current_user %}`）。

## 快速示例

```liquid
{% layout "theme" %}
<h1>{{ site.name }}</h1>
{% for p in site.pages | limit: 5 %}
  <a href="{{ p.path }}">{{ p.link_text }}</a>
{% endfor %}
```

## 相关工作流技能（可选安装）

与模板落地相关的流程可单独安装（单技能安装时请使用下列 **GitHub 稳定链接** 打开对应 `SKILL.md`）：

| 技能 | 说明 |
|------|------|
| [baklib-website-cloning](https://github.com/baklib-tools/skills/blob/main/skills/baklib-website-cloning/SKILL.md) | 参考站分析、复刻流程与质量清单 |
| [baklib-create-theme](https://github.com/baklib-tools/skills/blob/main/skills/baklib-create-theme/SKILL.md) | 新建 `themes/[scope]/[name]/` 脚手架与基础文件约定 |

安装示例：`npx skills add baklib-tools/skills --skill baklib-website-cloning`、`npx skills add baklib-tools/skills --skill baklib-create-theme`。
