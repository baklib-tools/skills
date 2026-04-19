# 新建主题（脚手架）

在 **`themes/[scope]/[theme_name]/`** 下创建目录结构与基础文件，便于立即开始开发。目录与命名细则见 [directory-and-naming.md](directory-and-naming.md)。

## 使用场景

- 创建新模板 / 新主题
- 初始化空的 `themes/` 子目录与最小文件集

## 工作流程

### 步骤 1：获取模板信息

1. **模板类型（scope）**：`cms`、`wiki` 或 `community`（默认 `cms`）
2. **模板名称**：
   - ✅ 只能包含：小写字母、数字、下划线
   - ❌ 不能使用连字符（如 `my-theme` → `my_theme`）
   - 长度：3–50 个字符

### 步骤 2：创建目录结构

```
themes/[scope]/[theme_name]/
├── assets/
│   ├── css/
│   ├── images/
│   └── javascripts/
├── config/
├── layout/
├── locales/
├── snippets/
├── src/
│   ├── stylesheets/
│   └── javascripts/
├── statics/
└── templates/
```

### 步骤 3：创建基础文件

| 文件 | 说明 |
|------|------|
| `config/settings_schema.json` | 模板配置 |
| `layout/theme.liquid` | 主布局 |
| `templates/index.liquid` | 首页模板 |
| `templates/page.liquid` | 页面模板 |
| `snippets/_header.liquid` | Header 片段 |
| `snippets/_footer.liquid` | Footer 片段 |
| `locales/zh-CN.json` | 中文国际化 |
| `locales/en.json` | 英文国际化 |
| `package.json` | NPM 配置 |
| `tailwind.config.js` | TailwindCSS 配置 |
| `src/stylesheets/application.css` | 基础样式 |
| `README.md` | 说明文档 |

### 步骤 4：验证和提示

1. 检查目录结构
2. 检查文件内容
3. 提示下一步操作（例如进入主题目录执行 `npm install && npm run dev`，以项目实际脚本为准）

## 生成的文件示例

### config/settings_schema.json

```json
[
  {
    "name": "theme_info",
    "theme_name": "[theme_name]",
    "theme_version": "0.0.1",
    "theme_scope": "[scope]"
  }
]
```

### layout/theme.liquid

```liquid
<!doctype html>
<html lang="{{ site.language }}">
<head>
  {% meta_tags %}
  {{ 'stylesheets/application.css' | asset_url | stylesheet_tag }}
</head>
<body>
  {% render 'header' %}
  {{ content_for_layout }}
  {% render 'footer' %}
</body>
</html>
```

## 重要规则

1. **模板名称规范**：只能使用小写字母、数字、下划线
2. **目录检查**：若模板目录已存在，须询问是否覆盖
3. **自动转换**：连字符建议转为下划线并与用户确认

## 使用示例（对话中）

```
创建 cms 模板 my_theme
→ 使用模板类型：cms
→ 使用模板名称：my_theme
→ 创建目录结构
→ 创建所有基础文件
→ 提示：cd themes/cms/my_theme && npm install && npm run dev
```
