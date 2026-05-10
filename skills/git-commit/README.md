# git-commit（Git 变更分析与提交信息）

## 作用

分析当前仓库 **staged / unstaged / untracked** 变更，判断是否应拆分为多条提交，并按 **Conventional Commits** 生成清晰的提交说明与提交计划；实际 `git commit` 前须由使用者确认。

规则细节、拆分策略与输出格式以 **[SKILL.md](SKILL.md)** 为准。

## 安装

```bash
npx skills add baklib-tools/skills --skill git-commit
```

手动安装：复制 [`skills/git-commit/`](https://github.com/baklib-tools/skills/tree/main/skills/git-commit) 到本地技能目录。

## 使用

在对话中加载本技能后，按 **[SKILL.md](SKILL.md)** 引导查看 `git` 状态、拟定提交计划；执行写入提交前等待用户明确同意。

## 示例

适用于任意 Git 仓库的日常提交辅助；无单独 HTML 示例目录。

## 更新日志

- 在此补充面向使用者的变更摘要；细则见 Git 历史与本目录 **[SKILL.md](SKILL.md)**。
