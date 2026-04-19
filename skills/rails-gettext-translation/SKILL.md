---
name: rails-gettext-translation
description: 在 Ruby on Rails 项目中维护 gettext 工作流：GNU gettext（msgmerge/msgattrib/msgfmt）、Rails 提取任务、以及用 gpt-po-translator 批量翻译或修复 .po 的 fuzzy；支持 OpenAI / Anthropic / Azure / OpenAI 兼容网关 / Ollama；须先 --list-models 再经用户确认 --model，禁止写死模型名；密钥从环境变量或工作区 .config/ 按变量名加载。适用于新增 _() 文案后更新 PO、msgmerge 后出现大量 fuzzy、或纯 PO 批量翻译。不负责替用户提交密钥到仓库、不执行除文档所述外的任意供应商计费操作。
---

# Rails + gettext（.po）翻译工作流

面向 **Rails + gettext（fast_gettext / gettext_i18n_rails 等）** 或多语言 **`.po` 文件** 的提取、合并、校验与 **AI 辅助翻译**。与具体产品无关：目录名、域名、语言列表均以**当前项目**为准。

## 何时使用

- 跑完 Rails 的 **字符串提取任务**后出现新 `msgid`、空 `msgstr`、或大量 `#, fuzzy`
- 需要批量处理 fuzzy / 待译，而不是手工改数千行 `.po`
- 审查 `_()` / `s_()` 用法与占位符是否与 `msgid` 一致

## 能力边界（不做什么）

- **不**在技能或示例中要求用户提交真实密钥到 Git；配置仅说明**环境变量**或**本地 `.config/` 文件**（见本仓库 [AGENTS.md](../../AGENTS.md)）。
- **不**绑定某一闭源产品或私有内网流程；示例路径用 `locale/`、`*.pot` 等占位，实际以项目为准。
- **不**代替用户选择付费供应商或承担 API 费用；**须用户确认**模型 id 后再跑长时间翻译命令。

## 依赖

| 依赖 | 用途 |
|------|------|
| GNU gettext（`msgfmt`、`msgmerge`、`msgattrib`） | 合并 POT、筛选 fuzzy、校验 |
| Ruby / Bundler | 运行 Rails 的 gettext 相关 rake 任务 |
| **PyPI：`gpt-po-translator`** | AI 批量翻译 `.po`（`--fix-fuzzy`、`--bulk` 等） |

```bash
pip install gpt-po-translator
# 或
pipx install gpt-po-translator
```

工具参数以官方为准：`gpt-po-translator --help`（[pescheckit/python-gpt-po](https://github.com/pescheckit/python-gpt-po)）。

## 配置（API 密钥与端点）

**不要**把密钥写入仓库。约定：从**工作区根目录** `.config/` 读取，文件名与**环境变量名**一致、全大写；**环境变量已设置时不覆盖**（便于 CI 注入）。详见 [references/config-examples.md](references/config-examples.md) 与仓库级 AGENTS.md。

安装本技能后，在 Rails 项目根目录可 **source** 随技能提供的脚本（路径以你本机安装位置为准）：

```bash
source path/to/rails-gettext-translation/scripts/load_po_translator_env.sh
```

脚本会将 `.config/OPENAI_API_KEY` 等文件导出为同名环境变量，并为 OpenAI 兼容客户端同步 `OPENAI_COMPATIBLE_BASE_URL`（当未单独设置且已设置 `OPENAI_BASE_URL` 时）。

检查是否已注入（**勿**在日志中打印密钥内容）：

```bash
test -n "${OPENAI_API_KEY:-}" && echo "OPENAI_API_KEY=set"
test -n "${OPENAI_COMPATIBLE_API_KEY:-}" && echo "OPENAI_COMPATIBLE_API_KEY=set"
```

## API 提供方选择（Agent 探测）

`gpt-po-translator` 的 `--provider openai_compatible` 面向 **OpenAI HTTP 形态**的端点（如 LM Studio、vLLM、自建网关）。应结合 **Base URL 与密钥** 选择 provider，**不要写死**。

### 建议顺序

1. 已 **source** 加载脚本（若使用 `.config/`）。
2. **官方 OpenAI**（主机为 `api.openai.com` 或文档规定的官方域）且 **`OPENAI_API_KEY` 非空** → `--provider openai`，**不要**用 `dummy` 探活。
3. **OpenAI 兼容 HTTP**（Base URL 含 `…/v1`、本机/内网、或用户说明为兼容网关）→ `--provider openai_compatible`。
4. **兼容端点且加载后仍无任何 key**：可先 `--openai-compatible-key dummy` 再跑 **`--list-models`** 探活（仅适用于本机或明确无鉴权的服务）；**不要**对公网未信任端点滥用占位符。
5. **Ollama 原生接口** → `--provider ollama`（见 `--help`），**不要**与 `openai_compatible` 混用。
6. 最终以 **`--list-models` 是否成功**为准。

**安全**：勿在日志中打印真实 Key；`dummy` 仅用于本机或明确无鉴权的环境。

## 模型选择（执行翻译前必做）

工具支持 `--model`；**禁止**在文档或回复中写死某一厂商的固定模型名。**唯一可信来源**是当前 provider 下 **`--list-models` 的输出**，或用户在本轮对话中**明确给出**的完整模型 id。

### 流程

1. 选定 provider 与 key 策略（与上一节一致）。
2. 执行 **`gpt-po-translator -f <PO 目录> --provider <...> --list-models`**（按需附加兼容端点、key 等参数）。
3. 将列表展示给用户；可建议：批量修 fuzzy 时优先**非 embedding**、体量适中的聊天模型。
4. **用户确认**某一模型 id 后，再执行 **`--bulk` / `--fix-fuzzy`** 等长时间任务；非交互环境加 **`-y`**。
5. 正式命令必须包含 **`--model "<完整 id>"`**。

若用户已写出完整 id，仍应**复述并请其确认**后再执行，避免误粘贴。

## 推荐主流程

以下占位符请替换为当前项目实际路径与语言列表。

### 1. 提取与合并（Rails）

提取任务名因 gem 而异，常见为：

```bash
bin/rails gettext:find
# 或
# bundle exec rake gettext:find
```

以项目文档或 `rake -T | grep -i gettext` 为准。

合并 POT 到各语言（示例：`locale/<lang>/app.po` 与 `locale/app.pot`）：

```bash
for lang in en ja zh_CN; do
  msgmerge --update --backup=none "locale/${lang}/app.po" locale/app.pot
done
```

### 2. 查看 fuzzy 工作量（可选）

```bash
msgattrib --only-fuzzy locale/en/app.po -o /tmp/en-fuzzy-only.po
msgfmt --statistics -o /dev/null /tmp/en-fuzzy-only.po 2>&1 || true
```

### 3. AI 翻译

在 **list-models → 用户确认 model** 之后（参数以 `--help` 为准），示例：

```bash
source path/to/rails-gettext-translation/scripts/load_po_translator_env.sh

gpt-po-translator --folder locale --folder-language --bulk --fix-fuzzy \
  --provider openai_compatible \
  --openai-compatible-key dummy \
  --model "<用户确认的模型 id>" \
  -y
```

说明：

- **`--folder-language`**：按 `locale/<语言代码>/*.po` 识别语言；若目录结构不同，改用 `-l` 等选项（见工具文档）。
- **`--fix-fuzzy`**：重译并去除 `#, fuzzy`（行为以工具为准）。
- 若 **bulk JSON 解析失败**或模型输出不稳：去掉 `--bulk`，或减小 `--bulksize`，或换模型。

### 4. 取消与残留进程

长时间任务被中断时，子进程可能不会自动退出。确认应停止后：

```bash
pgrep -fl gpt-po-translator
pkill -f gpt-po-translator
```

之后用 `git diff` 检查 `.po` 是否部分写入，再决定保留或回滚。

### 5. 验证

```bash
for f in locale/*/*.po; do
  msgfmt -c -v -o /dev/null "$f"
done
```

## Ruby i18n 提示（通用）

- **`_("...")`**：占位符须与代码中 `%{name}` / `%s` 等一致；不要用 Ruby 字符串插值拼进 `msgid`（除非项目刻意如此）。
- **`s_("上下文|文案")`（或等价 API）**：部分项目要求 `msgstr` **只翻译竖线右侧**；是否如此以**项目既有 PO 与文档**为准。
- **源语言 PO**：有的项目对「默认语言」故意留空 `msgstr`；**不要**在不了解产品约定时强行填满。

## msgattrib 速查

| 场景 | 命令 |
|------|------|
| 只导出 fuzzy 条目 | `msgattrib --only-fuzzy in.po -o fuzzy.po` |
| 未重译前 **不要**随意 `--clear-fuzzy`** | 易把错误译文当成定稿 |

## 检查清单

- [ ] 已按项目任务执行提取，并完成各语言 `msgmerge`
- [ ] AI：已选 provider；**先** `--list-models`，**经用户确认**后再带 `--model`；未写死具体模型名
- [ ] 全量 `msgfmt -c` 通过
- [ ] 中断后已检查无残留 `gpt-po-translator` 进程
- [ ] 密钥仅在本机 `.config/`、密钥管理或 CI 变量中，**未提交**

## 更多说明

- 配置示例与复制方式：[references/config-examples.md](references/config-examples.md)
