# cc2image｜zscc配图生成器

一个用于 ChatGPT / Codex 的中文文章配图 Skill。

它可以把中文文章、选题、段落、知识点，自动拆解成统一风格的图片生成方案，并在支持图片生成工具的环境中直接批量生图。

默认风格是「手绘知识卡片风」，同时内置多套可选风格，适合封面、正文配图、知识图解、文化封面、学习卡片、儿童科普图和极简海报。

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
| `frosted_glass_editorial` | 透明磨砂感海报风 | 极简封面、品牌海报、艺术展览、心理情绪主题 |

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
- 透明磨砂感海报风

## 默认匹配规则

如果用户没有指定风格：

1. 正文配图默认使用 `handdrawn_knowledge_card`。
2. 普通文章封面默认使用 `handdrawn_knowledge_card`。
3. 文化、人文、历史、哲学、文明、古籍、东方主题封面优先使用 `oriental_editorial_illustration`。
4. 学习方法、笔记、复习、考试主题优先使用 `study_note_card`。
5. 金字塔、层级、能力模型、主动学习主题优先使用 `pastel_learning_pyramid`。
6. 儿童教育、传统文化科普、器物介绍优先使用 `childlike_cultural_infographic`。
7. 艺术、音乐、品牌、心理情绪、极简主题封面优先使用 `frosted_glass_editorial`。

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
用东方典籍杂志插画风做封面，正文用手绘知识卡片风。
```

```text
用学习笔记卡片风，帮我把这篇学习方法文章拆成 5 张图。
```

```text
用透明磨砂感海报风，做一张关于孤独和自我觉察的封面。
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
