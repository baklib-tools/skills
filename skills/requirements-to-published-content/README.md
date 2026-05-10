# requirements-to-published-content（需求到发布内容工作流）

## 作用

多步工作流技能：**需求采集 → 分析 → 方案 → 对外文稿 →（可选）配图 / 公众号 HTML / Baklib 站点发布**；可扩展更多渠道。含**执行前确认门**：软文、公众号 HTML、计费出图、写入线上系统等步骤须用户明确同意后方可执行。

步骤清单、风险与扩展点以 **[SKILL.md](SKILL.md)** 为准。

## 安装

```bash
npx skills add baklib-tools/skills --skill requirements-to-published-content
```

常与 **wechat-mp-html**、**baklib-mcp**、图像子技能等组合安装。

## 使用

代理接手任务后应先列出拟执行步骤并征求确认，再按 **[SKILL.md](SKILL.md)** 与各子技能推进。

## 示例

- 仓库示例：[requirements-to-published-content-health-cms/](../../examples/requirements-to-published-content-health-cms/README.md)（脱敏医疗 CMS 场景，含公众号 HTML 与 walkthrough）。

## 更新日志

- 在此补充面向使用者的变更摘要；细则见 Git 历史与本目录 **[SKILL.md](SKILL.md)**。
