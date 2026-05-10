# image-generation-openrouter（OpenRouter 出图）

## 作用

通过 **OpenRouter** 调用支持图像输出的 chat/completions（含 `modalities` 等参数约定），用于与 OpenRouter 生态对接的出图场景。

端点、请求体与注意事项以 **[SKILL.md](SKILL.md)** 为准。

## 安装

```bash
npx skills add baklib-tools/skills --skill image-generation-openrouter
```

可与 **`image-generation`** 总览技能配合使用。

## 使用

1. 配置 OpenRouter API Key（`.config/` 或环境变量，优先级见 **[SKILL.md](SKILL.md)**）。
2. 在用户确认计费与用途后，按技能说明发起请求。

## 示例

见 **`SKILL.md`** 中的 JSON 示例与字段说明。

## 更新日志

- 在此补充面向使用者的变更摘要；细则见 Git 历史与本目录 **[SKILL.md](SKILL.md)**。
