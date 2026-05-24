# cc2image｜zscc配图生成器

一个用于 ChatGPT / Codex 的中文知识手绘配图 Skill。

它可以把中文文章、选题、段落、知识点，自动拆解成统一风格的图片生成方案，并在支持图片生成工具的环境中直接批量生图。

## 能做什么

- 生成中文知识文章封面图
- 生成正文配图 / 知识图解
- 将长文章拆成「1 张封面 + 多张正文配图」
- 生成批量生图 JSON / Markdown 清单
- 统一输出暖白纸感、黑灰细线、低饱和浅色块、中文手写风格的知识卡片

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
- 手绘知识卡片风格
- 米白背景、手绘、浅色块、留白风格

## 视觉风格

核心风格是：

> 高质量中文知识博主的手绘知识图解系统。暖白纸感背景、黑灰细线手绘、低饱和浅色块、自然成熟中文手写字、极简抽象小人、小气泡、底部判断句、留白充足、轻商业内容资产感。

避免：PPT、课程课件、商业海报、科技风信息图、3D、可爱儿童插画、复杂信息图、密集小字、高饱和颜色、英文乱码、水印。

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
帮我给这篇文章做一套图：封面图 + 正文配图，风格统一，米白背景、手绘、浅色块。
```

```text
主题：个人知识库真正的用法
帮我生成一张封面图。
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
