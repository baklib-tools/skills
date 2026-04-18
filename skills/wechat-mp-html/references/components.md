# 微信公众号 HTML：版式组件配方

以下片段均为 **inline style**，可直接嵌入 `#js_content`。替换 `{{标题}}`、`{{编号}}`、`{{正文}}` 等占位即可。

## 导读 / 摘要块

```html
<section style="margin:0 0 24px;color:#555;background:#f8fafc;padding:16px;border-left:4px solid #0d9488;">
  <section style="line-height:1.75;margin:0;"><strong style="color:#0d9488;">导读</strong>：此处为导语，一句话点明读者收益。</section>
</section>
```

## 简化步骤标题（单行绿条）

适用于「01 步骤名」类小标题：

```html
<section style="margin:32px 0 24px;padding:10px 16px;background:#dcfce7;border-left:4px solid #0d9488;font-weight:700;font-size:17px">
  <section style="line-height:1.75;margin:0;"><strong style="color:#0d9488">01</strong> 步骤名称</section>
</section>
```

蓝色变体：背景 `#dbeafe`，左边框与强调色 `#2563eb`。

## 数字标题（公众号常见：左侧数字块 + 右侧渐变斜切）

**仅替换 `{{编号}}`、`{{标题}}` 两处文字**；勿改嵌套结构与 style 字符串（若需改品牌色可整体替换色值）。

```html
<section style="margin: 40px 0 10px 0;">
  <section style="margin: 10px 0;display: flex;justify-content: flex-start;">
    <section style="display: flex;align-items: center;">
      <section style="flex-shrink: 0;z-index: 4;">
        <section
          style="font-size: 24px;letter-spacing: 1.5px;color: #ffffff;background-color: #0d9488;padding: 1px 6px;box-sizing:border-box;">
          <section style="line-height:1.75;margin:0;"><strong>{{编号}}</strong></section>
        </section>
      </section>
      <section style="display: flex;margin-left: -10px;">
        <section
          style="background: linear-gradient(to right,#20c1ad,#0d9488);padding: 3px 15px 3px 25px;box-sizing:border-box;transform: skew(-15deg);-webkit-transform: skew(-15deg);-moz-transform: skew(-15deg);-o-transform: skew(-15deg);">
          <section
            style="transform: skew(15deg);-webkit-transform: skew(15deg);-moz-transform: skew(15deg);-o-transform: skew(15deg);">
            <section style="font-size: 16px;color: #ffffff;text-align: left;">
              <section style="line-height:1.75;font-size: 16px;margin:0;"><strong>{{标题}}</strong></section>
            </section>
          </section>
        </section>
        <section
          style="flex-shrink: 0;padding-left: 3px;display: flex;align-items: flex-end;box-sizing:border-box;">
          <section
            style="width: 10px;height: 15px;background-color: #20c3ac;box-sizing:border-box;transform: skew(-15deg);-webkit-transform: skew(-15deg);-moz-transform: skew(-15deg);-o-transform: skew(-15deg);">
          </section>
        </section>
      </section>
    </section>
  </section>
</section>
```

蓝色变体：数字块背景 `#2563eb`，渐变 `linear-gradient(to right, #60a5fa, #2563eb)`。

## 章节主标题（居中 h2 风格 + 底纹条）

**仅替换 `{{标题}}`**。

```html
<section style="margin: 50px auto;display: flex;justify-content: center;">
  <section>
    <section
      style="font-size: 24px;color: #0d9488;text-align: center;padding: 0px 25px;box-sizing: border-box;">
      <section style="line-height:1.4;margin:0;"><strong>{{标题}}</strong></section>
    </section>
    <section
      style="width: 100%;height: 14px;background-color: #f3fbe9;border-bottom: 1px solid #ffe076;margin-top: -14px;max-width:100% !important;box-sizing:border-box;">
    </section>
  </section>
</section>
```

色值参考：标题字 `#0d9488`，底纹 `#f3fbe9`，底边 `#ffe076`。

## 总结框（左侧橙色竖条）

**替换 `{{标题}}`、`{{正文}}`**（正文可多段，复制内层 `section` 即可）。

```html
<section style="background:#f8fafc;border-left:4px solid #ea580c;padding:14px 16px;margin-top:20px;margin-bottom:20px;">
  <section style="margin:0 0 12px;font-size:17px;line-height:1.75;color:#333"><strong>{{标题}}</strong></section>
  <section style="margin:0 0 20px;font-size:17px;line-height:1.75;color:#333">{{正文}}</section>
</section>
```

## 正文段落与图片

普通段落：

```html
<section style="margin:0 0 16px;line-height:1.75;color:#333;text-align:justify">正文文字，<strong style="color:#0d9488">关键词</strong>可加粗。</section>
```

图片：

```html
<section style="margin:24px 0;text-align:center">
  <img src="https://example.com/your-image.png" alt="说明" style="max-width:100%;height:auto;display:block;margin:0 auto;border-radius:8px;">
</section>
```

## 篇首 / 篇尾占位图（可选）

若团队有统一头图/尾图，可在 `#js_content` 最前与最后插入各一张；`src` 发布前改为已上传素材 URL。
