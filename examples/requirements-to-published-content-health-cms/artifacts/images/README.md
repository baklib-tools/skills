# 示例配图（三镜头）

与 [image-plan-from-content.md](../image-plan-from-content.md) 及 [prompts/](prompts/) 中提示词对应：

| 文件 | 镜头 |
|------|------|
| `rtc-demo-shot1.png` | 痛点：内容分散、多屏混乱 |
| `rtc-demo-shot2.png` | 方案：统一内容枢纽 |
| `rtc-demo-shot3.png` | 结果/CTA：分期路径 |

[06-wechat-article.html](../06-wechat-article.html) 使用相对路径 `images/rtc-demo-shot*.png` 引用；本地用浏览器打开该 HTML 即可预览。

## 重新生成（维护者）

在仓库根目录 `skills`（含 `.config/UCLOUD_API_KEY`）下执行：

```bash
python3 skills/image-generation-ucloud/scripts/generate_ucloud_image.py \
  --prompt examples/requirements-to-published-content-health-cms/artifacts/images/prompts/shot1-pain.txt \
  --output examples/requirements-to-published-content-health-cms/artifacts/images/rtc-demo-shot1.png \
  --size 4:3 --image-size 1K
```

将 `shot1-pain` / `shot2-solution` / `shot3-cta` 与输出文件名轮换执行三次。模型与密钥说明见 [image-generation-ucloud](../../../../skills/image-generation-ucloud/SKILL.md)。
