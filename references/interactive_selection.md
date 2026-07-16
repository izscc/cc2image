# 可视化交互选型规范

本文件定义 cc2image 在 `visualize` 中的风格、封面和配图数量选择流程。它只负责配置选择，不负责生图。

## 触发与跳过

- 触发：用户要生成封面、文章配图、整套图片、内容拆图、logo 或图标，但没有明确指定当前风格库中的中文风格名或有效 style_id。封面比例和正文图数量是否明确不影响该门禁。
- 跳过：仅当用户已明确指定有效风格，或输入含有效的 `CC2IMAGE_SELECTION_V1` 配置块时跳过。
- “直接生成 / 用默认值 / 不用选择 / 不用问我 / 用合适的风格 / 帮我选 / 随机风格”均不算指定风格，必须触发选择器。
- 图标模式：仍可展示 8 套图标风格选择，但固定 1:1、1 张，不展示封面开关和正文数量。
- 无 `Visualize:visualize`：停止出图并说明无法打开交互选择器；不得采用自动匹配第一名继续，也不改用普通问答逐项追问。

## 回合边界

1. 未指定有效风格的当前轮，只允许读取内容、计算推荐、创建 visualization fragment 和输出 `::codex-inline-vis{file="<实际文件名>.html"}`。
2. 输出 inline visualization directive 后立即结束当前轮；同一轮不得调用 `image_gen`、不得输出最终 prompt/JSON、不得生成任何封面或正文图。
3. 用户点击“使用此配置继续”后，`window.openai.sendFollowUpMessage` 发回 `CC2IMAGE_SELECTION_V1`；下一轮校验配置后才能进入 prompt 构建和 `image_gen`。
4. 任何“为了省一步而自动采用首选推荐”的行为都属于门禁失败。

## 首显性能预算

- 每次选择器调用必须复用 `scripts/build_selector.py`，不得让模型重新创作整份 HTML。
- 运行时通过生成器的 stdin JSON 通道传入 3 个推荐 style_id、正文推荐张数和必要开关，不把动态内容拼进 shell 命令；中文风格名、分组短理由、完整下拉分组、缩略图映射、比例选项与提交脚本由生成器补齐。
- 首显前不运行 `render.py`、Playwright、浏览器截图、`view_image` 或双尺寸 QA。这些验证属于生成器本身的开发检查，不属于每次出图任务。
- 首显前不启动子代理。文章读取和推荐判断是短关键路径，子代理编排开销通常大于收益；并行能力留给用户完成选择后的多图规划或其他独立工作。
- 生成命令成功后立即输出 inline visualization directive，不再追加解释、审计或预览步骤。

## 推荐计算

1. 从 `references/style_options.md` 的现有风格和默认匹配规则中选择，不能发明 style_id。
2. 选出 3 个互有差异、都能解释内容的候选：第一项是最匹配的稳妥方案，第二项强调另一种表达方式，第三项提供合理的视觉张力。
3. 推荐顺序即匹配度顺序。首项默认选中，并显示“推荐”标记和生成器提供的 8-15 字视觉侧重点理由。
4. 用户明确说“随机风格”时仍按内容推荐，不做随机抽样。

## 交互布局

使用 Visualize 插件的 HTML fragment 规范，在当前任务的 visualization 目录创建新文件。界面在 736px 宽度下保持紧凑，在 320px 下自然堆叠。

### 视觉方向

- 整体采用“克制磨砂编辑感”：轻透明层次、柔和景深、低饱和主题色、较大的呼吸空间和清楚的中文排版。只参考磨砂玻璃、叠层和留白关系，不照搬参考图的粉、黑、白配色。
- 颜色必须来自 `visualize` 主题变量和 `--viz-series-*`，建议以雾蓝或灰紫作为主要选中态，以暖砂或柔金作为极少量辅助层次；同时适配亮色和暗色主题，不写死具体色值。
- 顶层保持透明且不加边框。`.card` 是唯一允许承载磨砂表面的容器；不要自造卡片边框、阴影和圆角，不嵌套卡片，也不要堆叠装饰性面板。
- 视觉重点依次是：当前首选风格、另外两个推荐方向、出图参数、最终操作。不要让所有元素同等醒目。
- 保持文字短而完整，不缩小字号挤内容，不让标签、数字、开关和滑杆互相错位。桌面端使用清晰的两列节奏，320px 下按“推荐 → 更多风格 → 封面 → 数量 → 确认”顺序单列堆叠。
- 只使用必要的轻量状态变化。选中态由 `aria-pressed` 和系统主题色表达；不要增加悬浮装饰动画、循环光效或与状态无关的渐变动画。

### 用户可见文案

- 推荐卡、更多风格下拉框、当前配置摘要、按钮、状态提示和错误信息全部使用简体中文。
- **禁止在任何用户可见位置显示 style_id**，包括 `<code>`、卡片副标题、tooltip、下拉选项、摘要、加载状态和错误信息。
- style_id 只允许存在于 DOM 的 `data-style-id`、JavaScript 状态和 `CC2IMAGE_SELECTION_V1` 提交内容中。
- 推荐理由由生成器按风格分组提供 8-15 字的视觉侧重点，不重复风格名；短文案应在 736px 三列卡片中保持自然换行。
- 推荐顺序用“首选 / 备选 / 探索”或等价的简短中文标签表达；只给第一项使用高强调标记。

### 1. 推荐风格

- 最上方展示 3 个推荐项，推荐第一项优先。
- **3 个推荐项必须全部展示对应风格示例图，不能降级成 icon。** `scripts/build_selector.py` 会从 `references/style_example_assets.json` 取得精确映射，读取 `assets/style-thumbnails/` 中的低分辨率缩略图，并以 `data:image/jpeg;base64,...` 嵌入 fragment。禁止使用 Lucide、emoji、SVG、单色块、渐变块或其他抽象图标替代示例图。
- 缩略图均由仓库中现有的 `image_gen` 风格示例图派生，只用于选择器预览，不是新的出图结果。不得凭风格名临时绘制预览，不得把其他风格图片错配给当前 style_id。
- 运行时只调用一次 `scripts/build_selector.py`。生成器会逐项验证 3 个推荐 style_id 的映射和缩略图文件，完成 base64 嵌入，并检查 `<img` 恰好为 3、`data:image/jpeg;base64,` 恰好为 3、`data-lucide` 为 0、fragment 小于 2 MB；任一条件失败时不输出残缺选择器。
- 每项只显示中文风格名、推荐理由和必要的中文排序标签；不得显示 style_id。style_id 放入 button 的 `data-style-id`。选择状态使用原生 button 的 `aria-pressed`，不要增加第二套选择状态。
- 卡片内容采用上下结构：上方是 16:9 示例图或稳定的视觉预览区，下方是完整中文风格名和两行以内理由。禁止把风格名、style_id、理由塞进同一横行。
- 736px 下使用 3 列等宽推荐卡；320px 下改为单列，图片、风格名和理由都不得裁切或横向溢出。
- 不允许以“没有可靠映射”或“图片可能超限”为由改用图标；本仓库已经为全部内容风格和图标风格提供轻量缩略图映射。

### 2. 更多风格

- 用一个原生 `<select>` 承载其余现有风格，并用 `<optgroup>` 对应 `references/style_options.md` 的风格分组。
- `<option>` 只显示中文风格名；value 可以保留内部 style_id，但用户可见文本不能附带英文 ID。
- 选中更多风格后，同步更新顶部的当前选择摘要；不要添加搜索、筛选、收藏或重置功能。

### 3. 封面

- 使用一个原生 checkbox 表示“生成封面”，文章配图任务默认开启；明确只要正文图时默认关闭。
- 使用一个原生 `<select>` 选择比例尺寸，选项固定为：
  - 21:9 · 2560×1080（横版超宽，普通封面默认）
  - 16:9 · 1920×1080（横版通用）
  - 3:2 · 1800×1200（横版文章）
  - 4:3 · 1600×1200（横版卡片）
  - 1:1 · 1536×1536（方形社媒）
  - 4:5 · 1440×1800（竖版海报）
  - 3:4 · 1350×1800（竖版封面）
  - 9:16 · 1080×1920（手机长图）
- 更换风格时，只有用户尚未手动改过比例，才把比例更新为该风格的推荐默认值；不能覆盖用户已做的选择。

### 4. 正文配图数量

- 用一个原生 range 控件选择 0-10 张，并在标签旁实时显示“推荐 N 张 / 当前 N 张”。
- 短文少于 1200 个中文字符默认 3 张；中等文章 1200-3000 默认 5 张；长文超过 3000 默认 7 张；只有主题而没有正文默认 0 张。
- 不增加第二套加减按钮或预设按钮，避免一个状态由多种控件重复控制。
- 数量标签、推荐值、当前值与滑杆放在同一逻辑区域：标题在左，当前张数在右，滑杆独占下一行；不要把“当前”与数字拆到不同列或让数字漂到界面边缘。
- 给正文数量 range 同时添加 `.form-range` 和 `.body-count-range`。滑轨继续使用 Visualize 默认中性色，只覆盖圆形 thumb 的填充与边框：亮色主题呈深蓝色，暗色主题使用 `--primary` 保持对比；禁止继续显示白色或透明圆点。
- 使用下面的最小样式，不改变 thumb 尺寸、滑轨几何、焦点环或交互状态：

```css
.body-count-range {
  --body-count-thumb: light-dark(
    color-mix(in oklab, var(--primary) 76%, var(--foreground) 24%),
    var(--primary)
  );
}

.body-count-range::-webkit-slider-thumb {
  border-color: var(--body-count-thumb);
  background: var(--body-count-thumb);
}

.body-count-range::-moz-range-thumb {
  border-color: var(--body-count-thumb);
  background: var(--body-count-thumb);
}
```

### 5. 当前配置与提交

- 在主操作前显示一行当前配置摘要：风格、封面比例尺寸、正文图数量。
- 摘要只显示中文风格名，例如“怪诞小人风 · 封面 21:9 · 正文 5 张”，不得显示 style_id。
- 只有一个主操作按钮：“使用此配置继续”。
- 主操作使用 `.btn .btn-primary .btn-block`，作为整个界面唯一的高强调操作；不要再添加取消、重置或第二个确认按钮。
- 点击后调用：

```js
await window.openai.sendFollowUpMessage({
  title: "确认 cc2image 出图配置",
  prompt: selectionPrompt
});
```

- 提交期间禁用按钮并显示“正在提交…”。失败时恢复按钮，并显示简短可行动错误信息。

## 提交协议

`selectionPrompt` 使用以下稳定文本格式。布尔值只能是 `true` 或 `false`；数量只能是 0-10 的整数；style_id 必须存在于风格库；ratio 和 size 必须是上面的配对。

```text
继续执行当前 cc2image 任务，不要再次打开选择器。按以下配置生成或输出清单：
CC2IMAGE_SELECTION_V1
style_id=handdrawn_knowledge_card
cover_enabled=true
cover_ratio=21:9
cover_size=2560x1080
body_count=5
skip_selector=true
END_CC2IMAGE_SELECTION
```

收到配置后先做边界校验，再继续原任务。不要再次复述问题或打开选择器；如果 `cover_enabled=false`，忽略 cover_ratio 和 cover_size；如果 `body_count=0`，不生成正文图。

## 可访问性与视觉约束

- 使用 `visualize` 提供的 `.viz-grid`、`.viz-controls`、`.card`、`.btn`、`.form-select`、`.form-range` 和主题变量，不重造控件样式；唯一允许的 range 外观覆盖是上文 `.body-count-range` 的深蓝色 thumb。
- 所有交互使用原生 button、checkbox、select、range；标签与控件正确关联；保留键盘焦点样式。
- 不写死亮色或暗色主题，不使用固定外宽、内部滚动、横向滚动或 viewport 高度。
- 第一屏即显示已选推荐方案和可直接提交的默认值；用户零修改也能完成选择。
- JavaScript 只管理本地选择状态和 `sendFollowUpMessage`；不得 fetch、XHR、WebSocket 或访问外部 API。
- 在 320px、736px 两种宽度下检查：无横向溢出、无中文截断、无英文 ID 泄露、图片比例稳定、标签与控件对齐、主按钮完整可见。
