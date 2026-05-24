# cc2image｜zscc配图生成器

一个用于 ChatGPT / Codex 的中文文章配图 Skill。

它可以把中文文章、选题、段落、知识点，自动拆解成统一风格的图片生成方案，并在支持图片生成工具的环境中直接批量生图。

默认风格是「手绘知识卡片风」，同时内置 16 套可选风格，适合封面、正文配图、知识图解、文化封面、学习卡片、儿童科普图、透明材质海报、玻璃拟态视觉、字体实验封面、AI 搜索界面、情绪概念海报、柔光产品 UI、极简品牌发布和建筑作品集线稿。

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
| `study_note_card` | 学习笔记卡片风 | 学习方法、笔记整理、步骤教程、知识清单 |
| `pastel_learning_pyramid` | 彩色手绘学习金字塔风 | 分层模型、学习金字塔、能力进阶、成长路径 |
| `childlike_cultural_infographic` | 儿童手绘文化科普风 | 传统文化科普、儿童教育、器物拆解、历史小知识 |
| `frosted_glass_editorial` | 透明磨砂感人物海报风 | 心理情绪、孤独感、音乐艺术主题 |
| `translucent_object_editorial` | 透明材质物件海报风 | 设计主题、品牌设计、作品集封面、工具系统封面 |
| `glassmorphism_gradient_blob` | 玻璃拟态渐变气泡风 | 品牌视觉、创意展览、趋势报告、AI 主题、未来感封面 |
| `embossed_typography_poster` | 浮雕纸雕字体海报风 | 极简封面、品牌口号、深度思考、书封设计 |
| `acrylic_dimensional_type` | 亚克力立体字母风 | 品牌关键词、栏目标题、创意概念、年轻化封面 |
| `dark_neon_search_ui` | 暗黑霓虹搜索界面风 | AI 搜索、知识探索、信息检索、灵感发现 |
| `black_void_glowing_hands` | 黑场发光肢体概念风 | 心理主题、情绪主题、关系连接、孤独感 |
| `soft_neumorphism_ui` | 柔光新拟态界面风 | 产品功能封面、AI 工具界面、智能家居、效率工具 |
| `minimal_line_shadow_brand` | 极简线性光影品牌风 | 新品发布、品牌封面、科技产品、数字主题 |
| `white_mono_texture_editorial` | 白色单色肌理编辑风 | 深度文章封面、设计作品集、哲学主题、个人品牌 |
| `minimal_architecture_portfolio` | 极简建筑作品集线稿风 | 作品集封面、人生路径、职业路径、空间叙事 |

## 默认匹配规则

如果用户没有指定风格：

1. 正文配图、方法论解释、流程、对比、知识系统：默认 `handdrawn_knowledge_card`。
2. 文化、历史、人文、哲学、东方智慧、古籍、文明：优先 `oriental_editorial_illustration`。
3. 学习方法、笔记整理、复习、考试、效率技巧：优先 `study_note_card`。
4. 学习金字塔、层级模型、能力进阶、成长路径、主动学习 / 被动学习：优先 `pastel_learning_pyramid`。
5. 儿童教育、传统文化科普、器物拆解、博物馆内容：优先 `childlike_cultural_infographic`。
6. 孤独、情绪、心理、音乐、艺术展、安静、疏离：优先 `frosted_glass_editorial` 或 `black_void_glowing_hands`。
7. 设计、作品集、品牌、营销、工具、系统、工作室案例：优先 `translucent_object_editorial`。
8. AI、未来感、趋势、创意展览、抽象概念、品牌视觉：优先 `glassmorphism_gradient_blob`。
9. 深度思考、认知、策略、极简口号、书封、品牌宣言：优先 `embossed_typography_poster` 或 `white_mono_texture_editorial`。
10. AI 搜索、探索、信息检索、发现、推荐、知识寻找：优先 `dark_neon_search_ui`。
11. 产品界面、搜索框、控制器、智能家居、效率工具、轻科技：优先 `soft_neumorphism_ui`。
12. 新品发布、数字主题、品牌发布会、极简科技主视觉：优先 `minimal_line_shadow_brand`。
13. 作品集、建筑、路径规划、职业路线、人生路径、空间叙事：优先 `minimal_architecture_portfolio`。

> 重要：多数透明材质、玻璃拟态、纸雕字体、亚克力立体字、霓虹搜索、黑场肢体、新拟态 UI、线性品牌、单色肌理、建筑线稿风格更适合封面图 / 头图 / 海报 / 系列主视觉；正文解释图仍建议默认使用手绘知识卡片风。

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
用暗黑霓虹搜索界面风，做一张 AI 搜索产品封面。
```

```text
用黑场发光肢体概念风，做一张关于孤独和连接的封面。
```

```text
用柔光新拟态界面风，做一张效率工具功能封面。
```

```text
用极简建筑作品集线稿风，做一张职业路径主题封面。
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
