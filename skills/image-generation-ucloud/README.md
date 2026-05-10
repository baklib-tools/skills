# image-generation-ucloud（UCloud ModelVerse 图像 API）

## 作用

通过 **UCloud ModelVerse** 图像 API 出图：鉴权、端点、模型与尺寸等约定。适用于指定 **api.modelverse.cn** 或文中列举的模型别名场景。

请求格式、模型列表与安全边界以 **[SKILL.md](SKILL.md)** 为准。

## 安装

```bash
npx skills add baklib-tools/skills --skill image-generation-ucloud
```

常与 **`image-generation`** 总览技能一并安装以便路由。

## 使用

1. 按 **[SKILL.md](SKILL.md)** 与仓库 [AGENTS.md](https://github.com/baklib-tools/skills/blob/main/AGENTS.md) 配置密钥（`.config/` 或环境变量）。
2. 仅在用户明确同意计费调用后，按技能说明构造请求。

## 示例

参见 **`SKILL.md`** 中的请求示例；完整流水线可与 **requirements-to-published-content** 等工作流组合。

## 更新日志

- 在此补充面向使用者的变更摘要；细则见 Git 历史与本目录 **[SKILL.md](SKILL.md)**。
