# software-dev-requirements-lifecycle

通用：**文档真源**、需求接收与变更闭环、用户故事与验收、排期与 ADR、**用户帮助中心**信息架构。与具体产品、云厂商、Baklib **无绑定**。

主说明见 **[SKILL.md](SKILL.md)**；模板与目录见 **[reference.md](reference.md)** 与 **[references/](references/)**。

## 安装方式

### 1. 命令行（推荐）

在已安装 Node.js 的环境中：

```bash
npx skills add baklib-tools/skills --skill software-dev-requirements-lifecycle
```

具体参数以 `npx skills --help` 为准。若本仓库为 monorepo，通常需 `--skill` 指向本目录名。

### 2. 手动复制到全局技能目录

将本目录**整体**复制到所用 Agent/编辑器约定的**用户级或项目级**技能目录，保持目录名与 `SKILL.md` 中 `name` 一致，例如：

| 工具/约定 | 常见路径（示例） |
|-----------|------------------|
| Cursor | `~/.cursor/skills/software-dev-requirements-lifecycle/` 或 项目内 `.cursor/skills/` |
| 其他 Agent | `~/.agents/skills/software-dev-requirements-lifecycle/` |

复制后应存在：`SKILL.md`、`reference.md`（可选）、`references/`（可选）。

### 3. 私有仓库 / Fork

若希望在内网或自有组织维护同一技能：

1. Fork [baklib-tools/skills](https://github.com/baklib-tools/skills) 或仅复制 `skills/software-dev-requirements-lifecycle/` 到**单独仓库根下同名路径**（保证 `skills/<name>/SKILL.md` 与上游列表兼容）。  
2. 安装：

```bash
npx skills add <your-org>/<your-repo> --skill software-dev-requirements-lifecycle
```

若私有仓库**只含单个技能**且目录在仓库根（无 `skills/` 前缀），以你所用 `skills` CLI 版本说明为准，或改为「手动复制」方式。

## 配合其他技能

若需求以 **PDF** 或 **Office**（DOCX / PPTX / XLSX 等）提供，可先安装并遵循 **[`mineru-office-to-markdown`](https://github.com/baklib-tools/skills/blob/main/skills/mineru-office-to-markdown/SKILL.md)**（单独 `npx skills add … --skill mineru-office-to-markdown`），在本地用 MinerU 转为 Markdown 后再做需求 Intake。若尚未安装 MinerU，代理应说明环境成本并**征得同意**后再引导安装与转换（见 `SKILL.md` 中「PDF / Office 需求材料」）。

## 仓库位置

本技能随 **[baklib-tools/skills](https://github.com/baklib-tools/skills)** 发布，与 Baklib 相关技能并列，便于统一 `npx skills add`。
