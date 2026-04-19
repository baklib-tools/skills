# `.config/` 示例（与仓库 [AGENTS.md](../../../AGENTS.md) 一致）

在 **Rails 项目根目录**下创建 `.config/`，仅存放本机或流水线密钥；**不要**把去掉 `.example` 后缀后的真实密钥文件提交到 Git。

可将本技能根目录（与 `SKILL.md` 同级）中的示例文件复制到项目 `.config/`，**去掉 `.example` 后缀**后再填入真实值：

| 示例文件（随技能发布） | 复制为（项目内） | 由脚本导出为 |
|------------------------|------------------|----------------|
| `OPENAI_API_KEY.example` | `.config/OPENAI_API_KEY` | `OPENAI_API_KEY` |
| `OPENAI_BASE_URL.example` | `.config/OPENAI_BASE_URL` | `OPENAI_BASE_URL` |
| `OPENAI_COMPATIBLE_API_KEY.example` | `.config/OPENAI_COMPATIBLE_API_KEY` | `OPENAI_COMPATIBLE_API_KEY` |

`scripts/load_po_translator_env.sh` 只读取**无** `.example` 后缀的文件；**环境变量已设置则不覆盖**。
