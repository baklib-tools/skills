# 用户帮助中心：目录与阅读体验

读者是**非技术用户**；组织目标是：**少层级、强导航、任务优先**，避免按「研发团队脑中的模块名」堆砌。

## 推荐信息架构（由浅入深）

1. **入口层**：`help/README.md` 作为**唯一首页**——简短说明 + **分组链接**（不要只列几十个平铺文件）。分组可选：
   - **按角色**：管理员 / 运营 / 终端用户（与产品角色一致时最直观）；  
   - **按任务场景**：下单、售后、对账、店铺设置（用户「想做什么」比内部模块名更好找）。
2. **任务层（主力）**：`how-to-*.md` 一篇一事，标题用用户语言（例如「如何导出订单」）。
3. **参考层**：术语、字段释义、状态含义 → `reference/` 或 `glossary-for-users.md`，避免打断 how-to 正文。
4. **问题解决层**：`faq.md` 和/或 `troubleshooting/`（错误提示、常见失败原因），与 how-to 文末互链。

## 示例目录（中等体量产品）

```text
docs/help/
├── README.md                      # 首页：分组导航 + 热门任务
├── getting-started.md             # 可选：最短路径上手
├── how-to-create-order.md
├── how-to-export-orders.md
├── admin/                         # 管理端与 C 端差异大时
│   ├── README.md
│   └── how-to-configure-webhook.md
├── orders/                        # 按业务域聚类
│   ├── README.md
│   └── how-to-refund.md
├── reference/
│   └── order-status-meanings.md
├── faq.md
└── troubleshooting/
    └── payment-failed.md
```

## 单篇 how-to 建议结构

- 一句话：本文帮你完成什么  
- **前置条件**（权限、账号状态、必要配置）  
- **操作步骤**（有序列表，关键步骤可配图）  
- **预期结果**  
- **常见问题**（链到 faq / troubleshooting）  
- **相关文档**（少量深链）

## 维护约定

- 新增 how-to 时，必须在 `help/README.md`（及所属子域 `*/README.md`）增加链接，避免孤岛页。  
- 产品重命名或菜单调整时，同步更新标题、截图与首页分组。  
- 若使用 GitBook、Docusaurus 等，**侧边栏顺序**与仓库内分组保持一致；Markdown 仍为真源时，用 `README` 模拟「侧栏」。
