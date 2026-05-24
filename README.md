# cc2image｜zscc配图生成器

一个用于 ChatGPT / Codex 的中文文章配图 Skill。

它可以把中文文章、选题、段落、知识点，自动拆解成图片生成方案，并在支持图片生成工具的环境中直接批量生图。

默认风格是「手绘知识风」，同时内置 16 套可选风格。用户不指定风格时默认使用 `handdrawn_knowledge_card`；用户说“合适的风格”“帮我选风格”“随机风格”时，会根据内容合理选择，不做纯随机。

## 能做什么

- 生成中文知识文章封面图
- 生成正文配图 / 知识图解
- 将长文章拆成「1 张封面 + 多张正文配图」
- 生成批量生图 JSON / Markdown 清单
- 根据主题自动选择合适视觉风格
- 支持在可用 `image_gen` 的环境中隐藏提示词并直接批量生图

## 16 套风格

| style_id | 风格名 | 适合场景 |
| --- | --- | --- |
| `handdrawn_knowledge_card` | 手绘知识卡片风 | 默认；正文配图、知识图解、方法论、流程图、对比图 |
| `oriental_editorial_illustration` | 东方典籍杂志插画风 | 文化、历史、人文、哲学类高级封面 |
| `study_note_card` | 学习笔记卡片风 | 学习方法、笔记整理、步骤教程、知识清单 |
| `pastel_learning_pyramid` | 彩色手绘学习金字塔风 | 分层模型、学习金字塔、能力进阶、成长路径 |
| `childlike_cultural_infographic` | 儿童手绘文化科普风 | 传统文化科普、儿童教育、器物拆解 |
| `frosted_glass_editorial` | 透明磨砂感人物海报风 | 心理情绪、孤独感、音乐艺术主题 |
| `translucent_object_editorial` | 透明材质物件海报风 | 设计主题、品牌设计、作品集封面、工具系统封面 |
| `glassmorphism_gradient_blob` | 玻璃拟态渐变气泡风 | 品牌视觉、创意展览、趋势报告、AI 主题 |
| `embossed_typography_poster` | 浮雕纸雕字体海报风 | 极简封面、品牌口号、深度思考、书封设计 |
| `acrylic_dimensional_type` | 亚克力立体字母风 | 品牌关键词、栏目标题、创意概念、年轻化封面 |
| `dark_neon_search_ui` | 霓虹搜索风 | AI 搜索、知识探索、信息检索、灵感发现 |
| `black_void_glowing_hands` | 黑场肢体风 | 心理主题、情绪主题、关系连接、孤独感 |
| `soft_neumorphism_ui` | 柔光界面风 | 产品功能封面、AI 工具界面、智能家居、效率工具 |
| `minimal_line_shadow_brand` | 线性品牌风 | 新品发布、品牌封面、科技产品、数字主题 |
| `white_mono_texture_editorial` | 白色肌理风 | 深度文章封面、设计作品集、哲学主题、个人品牌 |
| `minimal_architecture_portfolio` | 建筑线稿风 | 作品集封面、人生路径、职业路径、空间叙事 |

## 风格效果示例

下面 10 张图用于展示核心风格的视觉效果，实际生成时会根据用户文章主题、任务类型和指定 `style_id` 自动调整。

<table>
  <tr>
    <td width="50%"><strong>01｜手绘知识卡片风</strong><br><code>handdrawn_knowledge_card</code><br><img src="assets/examples/01-handdrawn-knowledge-card.jpg" alt="手绘知识卡片风示例"></td>
    <td width="50%"><strong>02｜东方典籍杂志插画风</strong><br><code>oriental_editorial_illustration</code><br><img src="assets/examples/02-oriental-editorial-illustration.jpg" alt="东方典籍杂志插画风示例"></td>
  </tr>
  <tr>
    <td width="50%"><strong>03｜学习笔记卡片风</strong><br><code>study_note_card</code><br><img src="assets/examples/03-study-note-card.jpg" alt="学习笔记卡片风示例"></td>
    <td width="50%"><strong>04｜彩色手绘学习金字塔风</strong><br><code>pastel_learning_pyramid</code><br><img src="assets/examples/04-pastel-learning-pyramid.jpg" alt="彩色手绘学习金字塔风示例"></td>
  </tr>
  <tr>
    <td width="50%"><strong>05｜儿童手绘文化科普风</strong><br><code>childlike_cultural_infographic</code><br><img src="assets/examples/05-childlike-cultural-infographic.jpg" alt="儿童手绘文化科普风示例"></td>
    <td width="50%"><strong>06｜透明磨砂感人物海报风</strong><br><code>frosted_glass_editorial</code><br><img src="assets/examples/06-frosted-glass-editorial.jpg" alt="透明磨砂感人物海报风示例"></td>
  </tr>
  <tr>
    <td width="50%"><strong>07｜透明材质物件海报风</strong><br><code>translucent_object_editorial</code><br><img src="assets/examples/07-translucent-object-editorial.jpg" alt="透明材质物件海报风示例"></td>
    <td width="50%"><strong>08｜玻璃拟态渐变气泡风</strong><br><code>glassmorphism_gradient_blob</code><br><img src="assets/examples/08-glassmorphism-gradient-blob.jpg" alt="玻璃拟态渐变气泡风示例"></td>
  </tr>
  <tr>
    <td width="50%"><strong>09｜浮雕纸雕字体海报风</strong><br><code>embossed_typography_poster</code><br><img src="assets/examples/09-embossed-typography-poster.jpg" alt="浮雕纸雕字体海报风示例"></td>
    <td width="50%"><strong>10｜亚克力立体字母风</strong><br><code>acrylic_dimensional_type</code><br><img src="assets/examples/10-acrylic-dimensional-type.jpg" alt="亚克力立体字母风示例"></td>
  </tr>
</table>

## 默认匹配规则

如果用户没有指定风格：

1. 普通知识/正文配图：默认 `handdrawn_knowledge_card`。
2. 用户说“合适的风格”“帮我选风格”“随机风格”：根据内容合理选择。
3. 文化、历史、人文、哲学、东方智慧：优先 `oriental_editorial_illustration`。
4. 学习方法、笔记、复习、考试：优先 `study_note_card`。
5. 学习金字塔、层级模型、能力进阶：优先 `pastel_learning_pyramid`。
6. 儿童教育、传统文化科普、器物拆解：优先 `childlike_cultural_infographic`。
7. 孤独、情绪、心理、艺术展：优先 `frosted_glass_editorial` 或 `black_void_glowing_hands`。
8. 设计、品牌、作品集、工具系统：优先 `translucent_object_editorial`。
9. AI、未来感、趋势、品牌视觉：优先 `glassmorphism_gradient_blob`。
10. 深度思考、极简口号、书封：优先 `embossed_typography_poster` 或 `white_mono_texture_editorial`。
11. AI 搜索、探索、检索、推荐：优先 `dark_neon_search_ui`。
12. 产品界面、搜索框、控制器、智能家居：优先 `soft_neumorphism_ui`。
13. 新品发布、数字主题、极简科技：优先 `minimal_line_shadow_brand`。
14. 作品集、路径规划、空间叙事：优先 `minimal_architecture_portfolio`。

> 多数封面型风格更适合头图 / 海报 / 系列主视觉；正文解释图仍建议默认使用手绘知识风。

## 安装

推荐安装到本地 Skills 目录：

```bash
git clone https://github.com/izscc/cc2image.git ~/.agents/skills/zscc配图生成器
```

## 使用示例

```text
使用 $zscc配图生成器，帮我把这篇文章拆成 1 张封面 + 5 张正文配图，并直接批量生图。
```

```text
用合适的风格，帮我给这篇文章做一张封面。
```

```text
用霓虹搜索风，做一张 AI 搜索产品封面。
```

```text
用黑场肢体风，做一张关于孤独和连接的封面。
```

```text
用柔光界面风，做一张效率工具功能封面。
```

## 文件结构

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── article_breakdown.md
│   ├── body_prompt.md
│   ├── cover_prompt.md
│   ├── style_options.md
│   └── visual_style.md
└── scripts/
    └── prompt_schema.py
```

## 辅助脚本

`scripts/prompt_schema.py` 可用于把结构化字段渲染成批量生图 JSON。

自测：

```bash
python3 scripts/prompt_schema.py --self-test
```

## 许可证

MIT License
