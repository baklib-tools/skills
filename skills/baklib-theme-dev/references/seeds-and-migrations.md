# Seeds 与主题迁移

## Seeds（`seeds/`）

用于定义站点**初始化数据**。支持 `.yml` / `.yaml` / `.json`。

### 目录结构示例

```
templates/
  ├── assets/
  ├── seeds/
  │   ├── 001_site.yml
  │   ├── 002_pages.yml
  └── presets/          # 可选：长文本、富文本外链
      ├── hero_content.html
      └── faq.md
```

### 文件命名

- **推荐**：编号 + 含义，如 `001_site.yml`、`002_pages.yml`。
- **执行顺序**：按文件名排序。
- **解析规则**：由文件**顶级 key** 决定类型（`site` / `pages`），而非仅靠文件名。

### 顶级 key：`site`

站点级配置，常对应站点设置：

```yaml
site:
  language: ''
  settings:
    hero_bg_color: "#20466D"
    hero_image: "images/theme/banner.png"
```

值可为字符串、数字、布尔、数组。资源引用：`images/...` 指向主题 `assets/`；`http(s)://...` 为外链。

### 顶级 key：`pages`

定义页面树，支持 `children` 嵌套：

```yaml
pages:
  title: "首页"
  slug: "index"
  template: "page"
  settings:
    hero_title: "欢迎使用"
    hero_content: "preset:hero_content.html"
  children:
    - title: "子页面"
      slug: "child"
      template: "page"
```

### `preset:` 引用

避免在 YAML 中写大段 HTML/Markdown：

```yaml
body: "preset:faq.md"
```

默认从 `templates/presets/` 加载；内容读入后作为字段值。

### 执行规则（概要）

1. 扫描 `seeds/` 下文件并排序。
2. 顶级 `site` → 合并站点配置；顶级 `pages` → 创建页面树。
3. 字段值以 `preset:` 开头时替换为预设文件内容。
4. 资源路径按产品规则解析。
5. 已存在相同层级/slug 的页面时可能跳过（以产品实现为准）。

---

## Migrations（`migrations/`）

用于主题**版本间**增量变更，与「全量 seeds」配合。

### 目录结构示例

```
template/
  ├── seeds/
  ├── migrations/
  │   ├── 20250101000000_add_faq_page.yml
  │   └── 20250215000000_change_hero_block.yml
  └── config/
      └── settings_schema.json
```

### 原则

- 每次发布只写**相对上一版本**的迁移。
- 站点记录当前**主题版本**；升级/回滚按链式执行 `up` / `down`。
- 回滚通常是**顺序逆过程**，不是任意版本一键跳转。

### 文件示例

```yaml
version: v2.0.0

up:
  pages:
    - match:
        slug: "index"
      update:
        settings:
          hero_title: "新版标题"

down:
  pages:
    - match:
        slug: "index"
      update:
        settings:
          hero_title: "欢迎使用"
```

- `version`：应用该迁移后期望的主题版本标识。
- `match`：定位要改的页面（slug、模板名等，以产品支持为准）。
- `up` / `down`：升级与回退时的变更内容。

### 多步回退

从 `v3.0.0` 回到 `v1.0.0` 时，按产品策略**依次**执行中间版本的 `down`，与常见数据库迁移思路一致。
