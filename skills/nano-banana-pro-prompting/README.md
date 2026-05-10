# nano-banana-pro-prompting（Nano Banana Pro 出图提示词）

## 作用

指导使用 **Gemini 3 Pro Image**（Nano Banana / Nano Banana Pro）生成配图或撰写其**出图提示词**：结构、约束与复查清单。**不包含**代运行脚本、调用计费 API 或代选供应商。

提示词模板与禁止项以 **[SKILL.md](SKILL.md)** 为准。

## 安装

```bash
npx skills add baklib-tools/skills --skill nano-banana-pro-prompting
```

手动安装：复制 [`skills/nano-banana-pro-prompting/`](https://github.com/baklib-tools/skills/tree/main/skills/nano-banana-pro-prompting)。

## 使用

在需要撰写或审阅该模型提示词时加载本技能，按 **[SKILL.md](SKILL.md)** 输出自包含、可执行的提示词正文。

## 示例

实际出图在用户所选平台完成；本技能仅产出自然语言提示词稿件。

## 更新日志

- 在此补充面向使用者的变更摘要；细则见 Git 历史与本目录 **[SKILL.md](SKILL.md)**。
