# image-generation（图像生成工作流总览）

## 作用

图像生成相关技能的**工作流总览**与路由说明：**不绑定单一供应商**。实际出图须配合 **`image-generation-ucloud`**、**`image-generation-openrouter`** 等子技能（或用户自备管线）。

工作流程拆分与确认门以 **[SKILL.md](SKILL.md)** 为准。

## 安装

```bash
npx skills add baklib-tools/skills --skill image-generation
```

建议按目标云平台或网关同时安装对应子技能，例如：

```bash
npx skills add baklib-tools/skills --skill image-generation --skill image-generation-ucloud
```

## 使用

先阅读 **[SKILL.md](SKILL.md)** 确定当前任务应激活哪个子技能；计费与写入外部系统前须用户确认。

## 示例

与各服务商子技能目录中的说明一致；仓库示例目录见 [examples/](https://github.com/baklib-tools/skills/tree/main/examples)。

## 更新日志

- 在此补充面向使用者的变更摘要；细则见 Git 历史与本目录 **[SKILL.md](SKILL.md)**。
