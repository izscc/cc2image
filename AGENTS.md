# AGENTS.md

## 项目特定规则

### Skill 安装与创建

1. 涉及 skill 的安装与创建时，skill 的 name 和描述都需要使用简体中文。
2. skill 统一安装路径：`/Users/zscc.in/.agents/skills`。

### 素材库路径

凡是提到“素材库”，都指 Obsidian 路径：

`/Users/zscc.in/Desktop/船仓文件/Obsidian/OB/00-资料库/📄 素材库`

### 新增风格的硬性流程

以后给 cc2image 新增任何风格时，必须同时完成以下事项：

1. 更新本地 skill 文件与相关风格库说明，确保新 `style_id` 可被本地 skill 识别和使用。
2. 使用 `image_gen` 生成该风格的示例图；不得使用本地脚本、Pillow、SVG、HTML/Canvas、浏览器截图、设计软件、命令行图片工具或其他替代方式生成示例图。
3. 将示例图更新到 `README.md` 的“风格效果示例”板块中。
4. 同步更新 `README.md`、`SKILL.md`、`references/style_options.md` 和必要的脚本/测试。
5. 运行必要验证，至少包括脚本自测、风格库 JSON/引用检查和 `git diff --check`。
6. 完成 GitHub 提交并推送。

## 通用行为准则

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```text
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
