# cc2image｜zscc配图生成器

一个用于 ChatGPT / Codex 的中文文章配图 Skill。

它可以把中文文章、选题、段落、知识点，自动拆解成统一风格的图片生成方案，并在支持图片生成工具的环境中直接批量生图。

默认风格是「手绘知识卡片风」，同时内置 10 套可选风格，适合封面、正文配图、知识图解、文化封面、学习卡片、儿童科普图、透明材质海报、玻璃拟态视觉和字体实验封面。

## 能做什么

- 生成中文知识文章封面图
- 生成正文配图 / 知识图解
- 将长文章拆成「1 张封面 + 多张正文配图」
- 生成批量生图 JSON / Markdown 清单
- 根据主题自动选择合适视觉风格
- 支持在可用 `image_gen` 的环境中隐藏提示词并直接批量生图

## 支持风格

| style_id | 中文名 | 适合场景 |
| --- | --- | --- |
| `handdrawn_knowledge_card` | 手绘知识卡片风 | 默认；正文配图、知识图解、方法论解释、流程图、对比图 |
| `oriental_editorial_illustration` | 东方典籍杂志插画风 | 文化、历史、人文、哲学类高级封面 |
| `study_note_card` | 学习笔记卡片风 | 学习方法、笔记整理、步骤教程、知识清单、小红书知识卡片 |
| `pastel_learning_pyramid` | 彩色手绘学习金字塔风 | 分层模型、学习金字塔、能力进阶、成长路径 |
| `childlike_cultural_infographic` | 儿童手绘文化科普风 | 传统文化科普、儿童教育、器物拆解、历史小知识 |
| `frosted_glass_editorial` | 透明磨砂感人物海报风 | 极简封面、心理情绪主题、孤独感、音乐艺术主题 |
| `translucent_object_editorial` | 透明材质物件海报风 | 设计主题、品牌设计、作品集封面、营销主题、工具系统封面 |
| `glassmorphism_gradient_blob` | 玻璃拟态渐变气泡风 | 品牌视觉、创意展览、趋势报告、AI 主题、未来感封面 |
| `embossed_typography_poster` | 浮雕纸雕字体海报风 | 极简封面、品牌口号、深度思考、书封设计、认知策略主题 |
| `acrylic_dimensional_type` | 亚克力立体字母风 | 品牌关键词、栏目标题、创意概念、年轻化封面、视觉实验 |


## 风格效果示例

以下示例图由本 Skill 的 10 个 `style_id` 分别生成，方便快速判断风格差异。

<table>
<tr>
<td width="50%"><strong>01. 手绘知识卡片风</strong><br><code>handdrawn_knowledge_card</code><br><img src="assets/examples/01-handdrawn-knowledge-card.jpg" alt="手绘知识卡片风示例"></td>
<td width="50%"><strong>02. 东方典籍杂志插画风</strong><br><code>oriental_editorial_illustration</code><br><img src="assets/examples/02-oriental-editorial-illustration.jpg" alt="东方典籍杂志插画风示例"></td>
</tr>
<tr>
<td width="50%"><strong>03. 学习笔记卡片风</strong><br><code>study_note_card</code><br><img src="assets/examples/03-study-note-card.jpg" alt="学习笔记卡片风示例"></td>
<td width="50%"><strong>04. 彩色手绘学习金字塔风</strong><br><code>pastel_learning_pyramid</code><br><img src="assets/examples/04-pastel-learning-pyramid.jpg" alt="彩色手绘学习金字塔风示例"></td>
</tr>
<tr>
<td width="50%"><strong>05. 儿童手绘文化科普风</strong><br><code>childlike_cultural_infographic</code><br><img src="assets/examples/05-childlike-cultural-infographic.jpg" alt="儿童手绘文化科普风示例"></td>
<td width="50%"><strong>06. 透明磨砂感人物海报风</strong><br><code>frosted_glass_editorial</code><br><img src="assets/examples/06-frosted-glass-editorial.jpg" alt="透明磨砂感人物海报风示例"></td>
</tr>
<tr>
<td width="50%"><strong>07. 透明材质物件海报风</strong><br><code>translucent_object_editorial</code><br><img src="assets/examples/07-translucent-object-editorial.jpg" alt="透明材质物件海报风示例"></td>
<td width="50%"><strong>08. 玻璃拟态渐变气泡风</strong><br><code>glassmorphism_gradient_blob</code><br><img src="assets/examples/08-glassmorphism-gradient-blob.jpg" alt="玻璃拟态渐变气泡风示例"></td>
</tr>
<tr>
<td width="50%"><strong>09. 浮雕纸雕字体海报风</strong><br><code>embossed_typography_poster</code><br><img src="assets/examples/09-embossed-typography-poster.jpg" alt="浮雕纸雕字体海报风示例"></td>
<td width="50%"><strong>10. 亚克力立体字母风</strong><br><code>acrylic_dimensional_type</code><br><img src="assets/examples/10-acrylic-dimensional-type.jpg" alt="亚克力立体字母风示例"></td>
</tr>
</table>

## 典型触发词

当用户提到这些意图时使用：

- 封面 / 封面图
- 正文配图 / 配图
- 知识图解
- 内容拆图
- 批量生图 / 批量配图
- 文章配图
- 把文章做成图
- 把文章拆成几张图
- 根据文章生成封面和正文图
- 手绘知识卡片风
- 东方典籍杂志插画风
- 学习笔记卡片风
- 彩色手绘学习金字塔风
- 儿童手绘文化科普风
- 透明磨砂感人物海报风
- 透明材质物件海报风
- 玻璃拟态渐变气泡风
- 浮雕纸雕字体海报风
- 亚克力立体字母风

## 默认匹配规则

如果用户没有指定风格：

1. 正文配图、方法论解释、流程、对比、知识系统：默认 `handdrawn_knowledge_card`。
2. 文化、历史、人文、哲学、东方智慧、古籍、文明：优先 `oriental_editorial_illustration`。
3. 学习方法、笔记整理、复习、考试、效率技巧：优先 `study_note_card`。
4. 学习金字塔、层级模型、能力进阶、成长路径、主动学习 / 被动学习：优先 `pastel_learning_pyramid`。
5. 儿童教育、传统文化科普、器物拆解、博物馆内容：优先 `childlike_cultural_infographic`。
6. 孤独、情绪、心理、音乐、艺术展、安静、疏离：优先 `frosted_glass_editorial`。
7. 设计、作品集、品牌、营销、工具、系统、工作室案例：优先 `translucent_object_editorial`。
8. AI、未来感、趋势、创意展览、抽象概念、品牌视觉：优先 `glassmorphism_gradient_blob`。
9. 深度思考、认知、策略、极简口号、书封、品牌宣言：优先 `embossed_typography_poster`。
10. 单个关键词、栏目名、品牌词、年轻化视觉实验：优先 `acrylic_dimensional_type`。

> 重要：多数透明材质、玻璃拟态、纸雕字体、亚克力立体字风格更适合封面图 / 头图 / 海报 / 系列主视觉；正文解释图仍建议默认使用手绘知识卡片风。

## 安装

推荐安装到本地 Skills 目录：

```bash
git clone https://github.com/izscc/cc2image.git ~/.agents/skills/zscc配图生成器
```

如果你已经有这个目录，可以先备份或删除后再 clone。

## 使用示例

```text
使用 $zscc配图生成器，帮我把这篇文章拆成 1 张封面 + 5 张正文配图，并直接批量生图。
```

```text
用透明材质物件海报风做封面，正文用手绘知识卡片风。
```

```text
用玻璃拟态渐变气泡风，做一张 AI 趋势报告封面。
```

```text
用浮雕纸雕字体海报风，做一张关于深度思考的极简封面。
```

```text
用亚克力立体字母风，做一张品牌关键词主视觉。
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
