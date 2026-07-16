---
name: zscc配图生成器
description: zscc配图生成器；当用户提到封面、正文配图、配图、知识图解、内容拆图、批量生图、文章配图、手绘知识卡片、小红书、公众号配图，或说“生成一个 logo / 图标 / 小图标 / app icon”，或指定内置 49 套内容风格与 8 套 logo/图标风格时使用。将中文主题、文章、段落、知识点或产品概念拆解为封面、正文图、logo/图标与批量生图方案；用户未明确指定有效风格时，必须先进入 Visualize:visualize 可视化交互选择，完成选择后才可调用 image_gen。
---

# zscc配图生成器

## 强制风格门禁（最高优先级）

本节优先于本 Skill 的所有默认值、自动匹配规则和直接生图规则。

1. 首先检查用户是否明确指定了当前风格库中的中文风格名、有效 style_id，或消息中是否含有效的 `CC2IMAGE_SELECTION_V1` 配置块。
2. **只要没有明确指定有效风格，就必须调用插件 Skill `Visualize:visualize`，进入可视化交互选型。** “用合适的风格”“帮我选”“随机风格”“直接生成”“用默认值”“不用问我”都不算指定风格，仍然必须进入选择器。
3. 选择器必须让用户选择风格，并同时确认封面开关、封面比例尺寸和正文配图数量；图标模式选择图标风格并固定 1:1、1 张。
4. 创建 visualization HTML fragment 后，在回复中输出 `::codex-inline-vis{file="<实际文件名>.html"}`，然后立即结束当前轮。
5. **展示选择器的同一轮禁止调用 `image_gen`、禁止直接输出最终 prompt/JSON、禁止自动采用第一推荐风格。** 必须等待选择器通过 `window.openai.sendFollowUpMessage` 返回 `CC2IMAGE_SELECTION_V1` 后，下一轮才能继续生成。
6. 只有两种情况可跳过选择器：用户已明确指定有效风格；或消息中已有有效的 `CC2IMAGE_SELECTION_V1`。仅仅指定图片数量、封面比例或说“直接生成”不能跳过。
7. 如果 `Visualize:visualize` 确实不可用，停止生图并明确告知无法打开风格选择器；不得回退到手绘知识风或其他自动风格继续生成。

## 选择器首显快速路径（强制）

未指定风格的首轮目标只有一个：**尽快显示选择器**。必须使用已经预校验的确定性生成器，禁止每次临时编写和调试 HTML。

1. 读取用户内容后，直接在当前 Skill 的匹配规则中确定 3 个推荐 style_id 和正文推荐张数。不要为了生成选择器再次完整读取 `style_options.md`、`interactive_selection.md` 或 `style_example_assets.json`；生成器会统一解析并校验这些文件，并按风格分组补齐短中文理由。
2. 调用 `Visualize:visualize` 后，将当前线程的 visualization 目录设为命令工作目录，关闭 login shell，并以 PTY 启动下面这个固定命令；命令行不得拼接用户文本或模型选择的 style_id：

```bash
python3 <SKILL_ROOT>/scripts/build_selector.py --stdin-config --output-dir .
```

进程等待输入后，通过工具的 stdin 通道发送一行 JSON，动态内容不得经过 shell：

```json
{"recommend":["<STYLE_ID_1>","<STYLE_ID_2>","<STYLE_ID_3>"],"body_count":5,"cover_enabled":true,"icon_mode":false}
```

图标任务使用 `"icon_mode":true`；明确只要正文图时使用 `"cover_enabled":false`。

3. 命令成功后读取 JSON 输出中的唯一文件名，立即输出对应的 `::codex-inline-vis{file="<实际文件名>"}` 并结束当前轮。不得复用旧 selector 文件名。
4. **选择器首显前禁止执行**：手写或 `apply_patch` 生成 HTML、`render.py`、Playwright/浏览器 QA、截图、`view_image`、加载浏览器依赖、再次读取完整风格库、全量素材验证、启动子代理、生成 prompt 或调用 `image_gen`。
5. `scripts/build_selector.py` 已负责 style_id、缩略图、数量边界、3 张示例图、2 MB 上限和交互协议拼装。浏览器与双尺寸视觉 QA 只在修改生成器或交互规范时执行一次，不得在每次用户调用 Skill 时重复执行。
6. 选择器首显阶段不使用子代理：这里只有“读内容 → 推荐 → 生成 fragment → 展示”的短串行关键路径，子代理启动与回收会增加等待。用户提交配置后，后续多图提示词规划可并行，但不得延迟选择器首显。

## 核心目标

把中文文章、选题、段落或知识点转成一套可批量生成的视觉资产：封面图、正文配图、内容拆图、logo/图标和批量生图清单。内置 49 套内容视觉风格和 8 套 logo/图标风格；未指定风格时先通过可视化选择器让用户确认，不自动采用手绘知识风直接生成。

## 默认执行原则

1. 先判断用户要的是：封面图、正文配图、内容拆图规划、批量生图、还是 prompts/JSON 清单。
2. 仅在通过“强制风格门禁”后，若用户要求“生成图、批量生图、做一套图、封面和正文图”等，且当前环境可用 `image_gen`：先在内部生成稳定提示词，不默认展示完整 prompt，然后按每张图逐次调用 `image_gen`。
3. 硬性限制：cc2image 直接生图只能使用 `image_gen`。禁止改用本地脚本、Pillow、SVG、HTML/Canvas、浏览器截图、设计软件、命令行图片工具或其他替代方式生成图片。
4. 若当前环境不可用 `image_gen`，或用户明确要求“提示词、JSON、清单、给程序用”：只输出结构化字段和完整 prompt，不直接生成图片。
5. 若用户说“生成一个 logo / 图标 / 小图标 / app icon / 功能图标”：先识别为 logo/图标模式；未指定图标风格时仍必须进入选择器，选择后固定生成 1 张 1:1 方形图标。
6. 通过风格门禁后，若用户只给主题：默认生成 1 张 21:9 封面图；如“正文配图”意图明显，则生成 1 张 16:9 正文图。
7. 通过风格门禁后，若用户给文章并要求配图/拆图：默认规划 1 张封面 + 3 到 6 张正文图；长文章可用 1 张封面 + 6 到 10 张正文图；用户指定数量时优先服从。
8. 未指定有效风格时，必须使用 `Visualize:visualize` 生成一次选择器；不要用连续文字追问替代，也不要自动继续。
9. 若用户说“封面用 A，正文用 B”，封面和正文分别套用对应 style_id。
10. 若用户说“用合适的风格”“帮我选风格”“随机风格”，不要替用户直接选定；根据内容计算推荐顺序并在可视化选择器中置顶展示。
11. 用户已明确当前风格库中的中文风格名或有效 style_id 时，可以跳过选择器；封面比例和正文图数量缺失时按本 Skill 默认值补齐。
12. 收到 `CC2IMAGE_SELECTION_V1` 配置块后，视为用户已经完成选择；校验字段后继续当前任务，绝不再次打开选择器。

## 生图工具硬性原则

- 直接生成图片时只能调用 `image_gen`。
- 禁止使用本地脚本、Pillow、SVG、HTML/Canvas、浏览器截图、设计软件、命令行图片工具或其他替代方式生成图片。
- 若 `image_gen` 不可用，不得“想办法”用其他工具出图；只能输出 prompt、JSON 或 Markdown 生图清单，等待用户在有 `image_gen` 的环境中生成。
- 仓库示例图若由 cc2image 流程新增，也必须来自 `image_gen` 输出或用户明确提供的图片资产；不要用本地程序绘制示例图冒充生图结果。
- `scripts/prompt_schema.py` 等脚本只负责校验和渲染 prompt，不负责图片合成。

## 可视化交互选型

用户未明确指定有效风格时，无条件使用插件 Skill `Visualize:visualize`，并在调用 `image_gen` 前完成一次可视化选择。完整交互规范见 `references/interactive_selection.md`。

1. 先理解主题或文章，再按自动匹配规则计算 3 个推荐风格；按匹配度排序并置顶，第一项默认选中。推荐结果必须来自当前 49 套内容风格或 8 套图标风格，不能临时发明 style_id。
2. 使用 `Visualize:visualize` 创建一张精炼的磨砂编辑感交互界面。推荐区的 3 张卡片必须从 `references/style_example_assets.json` 解析对应缩略图并以 `<img>` 显示，同时显示中文风格名和一句推荐理由；禁止用 Lucide、emoji、SVG、色块或其他抽象 icon 代替示例图。style_id 只保存在控件数据与提交协议中，禁止出现在任何用户可见位置。
3. 普通文章任务在同一界面选择：风格、是否生成封面、封面比例尺寸、正文配图数量。图标模式只显示图标风格和固定 1:1，不显示正文数量。
4. 封面默认比例为 21:9（2560×1080）；若推荐风格有强制竖版规则，则使用该风格默认比例：`giant_chinese_concept_poster` 和 `premium_product_ad_poster` 默认 4:5（1440×1800），`editorial_line_infographic_poster` 默认 9:16（1080×1920），`glyph_object_imagery` 默认 1:1（1536×1536）。用户仍可修改。
5. 文章正文图推荐数量按正文长度计算：短文（少于 1200 个中文字符）3 张，中等文章（1200-3000）5 张，长文（超过 3000）7 张；单一主题默认 0 张。界面把推荐值直接预填，允许在 0-10 张内修改；数量滑杆的圆形 thumb 必须使用 `references/interactive_selection.md` 规定的主题自适应深蓝色，不能保留默认白色圆点。
6. 主操作按钮使用 `window.openai.sendFollowUpMessage` 提交结构化 `CC2IMAGE_SELECTION_V1` 配置，按钮文案为“使用此配置继续”。提交内容必须带 `skip_selector=true`，避免循环打开选择器。
7. 选择器只负责收集配置，不生成任何图片，不得把 HTML、SVG、Canvas 或截图当作 cc2image 图片结果。最终封面和正文配图仍只能由 `image_gen` 生成。
8. fragment 的映射检查、缩略图读取、base64 嵌入和体积校验全部由 `scripts/build_selector.py` 一次完成；运行时不得手工重复这些步骤。若生成器报告任一推荐缩略图缺失，停止创建选择器并修复资产映射，不得静默回退到 icon。
9. 若 `Visualize:visualize` 不可用、界面提交失败，或当前客户端不支持交互，停止当前出图任务并说明原因；禁止使用第一推荐风格回退直出。
10. 视觉层级、磨砂质感、中文文案、卡片排版与响应式细节必须遵守 `references/interactive_selection.md`；不要把风格名、英文 ID 和理由压进同一行，也不要让控件标签与数值错位。

## 风格选择

`handdrawn_knowledge_card`（手绘知识风）是普通知识内容的常见首选推荐，不是绕过选择器的自动默认值。用户可直接说“用典籍山水风做封面”“正文用手绘知识风”“用泡沫字体风”；明确指定有效风格后可直接执行。完整风格库见 `references/style_options.md`。

支持的 style_id：

- `handdrawn_knowledge_card`：手绘知识风；常见首选推荐；正文配图、知识图解、方法论、流程图、对比图。
- `oriental_editorial_illustration`：典籍山水风；适合文化、历史、人文、哲学类高级封面。
- `study_note_card`：学习笔记风；适合学习方法、笔记整理、步骤教程、知识清单。
- `pastel_learning_pyramid`：粉彩金字塔风；适合分层模型、学习金字塔、能力进阶、成长路径。
- `childlike_cultural_infographic`：童趣科普风；适合传统文化科普、儿童教育、器物拆解。
- `frosted_glass_editorial`：磨砂情绪风；适合心理情绪、孤独感、音乐艺术主题。
- `translucent_object_editorial`：透明物件风；适合设计主题、品牌设计、作品集封面、工具系统封面。
- `glassmorphism_gradient_blob`：玻璃气泡风；适合品牌视觉、创意展览、趋势报告、AI 主题。
- `embossed_typography_poster`：纸雕字体风；适合极简封面、品牌口号、深度思考、书封设计。
- `acrylic_dimensional_type`：亚克力字风；适合品牌关键词、栏目标题、创意概念、年轻化封面。
- `dark_neon_search_ui`：霓虹搜索风；适合AI 搜索、知识探索、信息检索、灵感发现。
- `black_void_glowing_hands`：黑场肢体风；适合心理主题、情绪主题、关系连接、孤独感。
- `soft_neumorphism_ui`：柔光界面风；适合产品功能封面、AI 工具界面、智能家居、效率工具。
- `minimal_line_shadow_brand`：线性品牌风；适合新品发布、品牌封面、科技产品、数字主题。
- `white_mono_texture_editorial`：白色肌理风；适合深度文章封面、设计作品集、哲学主题、个人品牌。
- `minimal_architecture_portfolio`：建筑线稿风；适合作品集封面、人生路径、职业路径、空间叙事。
- `minimal_healing_metaphor_comic`：治愈漫画风；适合情绪疗愈、内耗、孤独、亲密关系、自我照顾。
- `retro_minimal_poster_illustration`：复古海报风；适合极简主义、生活方式、个人手册、创作宣言、书封。
- `editorial_balloon_collage`：气球拼贴风；适合团队协作、未来愿景、组织文化、品牌广告、社群主题。
- `transparent_architectural_type`：透明字境风；适合宏大阶段、未来路径、系统升级、人生转折、空间隐喻。
- `paper_cut_profile_silhouette`：纸雕剪影风；适合职业人物、行业精神、工程建筑、人物专访。
- `torn_paper_note_minimal`：撕纸便签风；适合一句话封面、信念提醒、极简语录、每日提醒。
- `fluffy_soft_typography`：毛绒字体风；适合好运、发财、治愈、可爱、祝福、轻松社媒图。
- `cloud_typography_cover`：云朵字体风；适合希望、成长、新开始、复原力、上升、疗愈。
- `foam_bubble_typography`：泡沫字体风；适合清洁、焕新、重启、梦想、生活方式海报。
- `embroidered_patch_brand`：刺绣徽章风；适合品牌徽章、学院风、社群身份、工具包、服饰品牌。
- `luxury_gold_typography`：金属奢华风；适合节日海报、高端品牌、仪式感、成就、庆典。
- `miniature_map_life_scene`：微缩地图风；适合人生选择、职业路径、城市迁移、成长路线。
- `miniature_checklist_scene`：微缩清单风；适合任务管理、行动清单、习惯养成、目标拆解。
- `fabric_micro_scene_ad`：布料微缩风；适合劳动节、匠心、手工、服饰品牌、工艺精神。
- `giant_letter_lifestyle_scene`：巨字生活风；适合品牌广告、教育、家庭、城市、组织价值。
- `oriental_floral_minimal_editorial`：花艺留白风；适合女性主题、母亲节、思念、关系、疗愈、节气。
- `zen_ink_philosophy_poster`：禅意水墨风；适合哲学、人生路径、自我修炼、觉察、东方智慧。
- `editorial_line_character`：编辑线稿风；适合品牌视觉、杂志海报、网站首屏、包装、角色系统、城市生活场景。
- `editorial_object_annotation_card`：具象标注风；适合AI方法论、设计思维、知识卡片、认知模型、信任验证、工作流原则。
- `crowd_typography_scene`：人群造字风；适合社会议题、财经封面、就业问题、人口变化、城市议题、商业趋势、群体行为。
- `semantic_material_typography`：语义字体风；适合关键词封面、品牌标题、栏目标题、概念海报、单词视觉化、强标题主视觉。
- `quirky_doodle_character_flow`：怪诞小人风；适合AI工作流、系统流程、正文配图、方法论拆解、工具链说明、长文认知锚点。
- `minimal_line_art`：线条艺术风；适合亲密关系、旅行、毕业、学习、课堂、会议、城市、灵感、个人成长、极简封面。
- `isometric_modular_system`：轴测模块系统风；适合SaaS架构、服务流程、空间地图、系统关系、模块化品牌插画。
- `monochrome_system_editorial`：黑白系统风；适合Skill封面、SOP封面、提示词库、方法论手册、AI工作流、标准化流程。
- `isometric_timeline_miniature`：时间微缩风；适合技术演化、行业发展史、工具变迁、产品迭代、内容生产演化、学习方式演化、AI工作流演化、知识管理演化、品牌发展历程、商业模式演化、教育工具演化、创作者工具链。
- `real_object_doodle_composite`：实物涂鸦风；适合幽默封面、创意配图、社媒传播图、情绪表达、工作压力、学习压力、心理状态、生活方式内容、视觉双关、轻量观点、正文配图。
- `expressive_3d_quirky_character`：3D怪表情风；适合情绪表达、观点吐槽、社媒表情图、AI工作流节点、轻剧情配图。
- `giant_chinese_concept_poster`：大字海报风；适合中文概念海报、文学感封面、情绪关键词、短词强视觉。
- `premium_product_ad_poster`：产品海报风；适合电商主图、新品发布海报、品牌广告、产品卖点图、功能拆解图。
- `glyph_object_imagery`：字物意象风；适合中文金句、观点短句、品牌口号、成语祝福、情绪短句、文字造物、创意字体图。
- `editorial_line_infographic_poster`：竖版线稿长图风；适合竖版教程长图、SOP、规则卡、项目复盘、AI工作流、多步骤方法论、手机端知识海报。
- `scribble_furball_character_family`：毛球角色家族风；以中等密度、中心略密外缘较松的乱线团、巨大椭圆白眼、黑色单线四肢和固定黄色流苏围巾为同一 IP 原型；适合情绪表达、知识卡片、办公状态、教育内容、品牌 IP、角色设定和社媒传播图。

logo/图标模式专用 style_id：

- `cute_3d_plastic_icon`：3D 新拟物风小图标；常见首选推荐，适合工具、功能、App 图标。
- `candy_glass_3d_icon`：3D 糖果风格图标；适合低对比、清爽可爱、半透明糖果质感图标。
- `airbnb_soft_miniature_icon`：Airbnb 风软拟物图标；适合旅行、生活方式、露营、家居、厨房等温暖场景。
- `circular_2_5d_vector_icon`：圆形轻拟物风格图标；适合金刚区、功能入口、中文移动 App 矢量图标。
- `soft_frosted_glass_icon`：软糖风格图标；适合奶霜、毛玻璃、柔软透明质感的独立图标。
- `circular_3d_texture_icon`：环形 3D 质感图标；适合圆形渐变底、系统级 3D App icon。
- `frosted_glass_ui_icon`：磨砂玻璃质感小图标；适合钱包、文件夹、卡片、面板等简洁 UI 图标。
- `pastel_reward_badge_icon`：少女风奖牌图标；适合奖励徽章、等级奖牌、儿童或少女风粉彩图标。

自动匹配优先级：

1. 用户明确指定风格时，优先服从。
2. 用户说“生成一个 logo / 图标 / 小图标 / app icon / 功能图标”时，进入 logo/图标模式，输出 1:1 图标；根据需求在 8 套图标风格中选择，不使用普通文章封面风格。
3. 图标模式中：奖牌/徽章/少女/儿童优先推荐 `pastel_reward_badge_icon`；金刚区/矢量/2.5D 优先推荐 `circular_2_5d_vector_icon`；旅行/露营/生活方式优先推荐 `airbnb_soft_miniature_icon`；毛玻璃/半透明/软糖优先推荐 `soft_frosted_glass_icon`；钱包/文件夹/卡片/UI 圆角层优先推荐 `frosted_glass_ui_icon`；圆形底/系统级 App icon 优先推荐 `circular_3d_texture_icon`；未指定时把 `cute_3d_plastic_icon` 置于选择器推荐位，不直接生成。
4. 用户说“合适的风格”“帮我选风格”“随机风格”时，按内容生成推荐排序并展示选择器，不做纯随机，也不替用户确认。
5. 正文配图、方法论解释、流程、对比、知识系统：优先 `handdrawn_knowledge_card`。
6. 文化、历史、人文、哲学、东方智慧、古籍、文明：优先 `oriental_editorial_illustration`。
7. 学习方法、笔记整理、复习、考试、效率技巧：优先 `study_note_card`。
8. 学习金字塔、层级模型、能力进阶、成长路径、主动学习 / 被动学习：优先 `pastel_learning_pyramid`。
9. 儿童教育、传统文化科普、器物拆解、博物馆内容：优先 `childlike_cultural_infographic`。
10. 孤独、情绪、心理、音乐、艺术展、安静、疏离：优先 `frosted_glass_editorial` 或 `black_void_glowing_hands`。
11. 设计、作品集、品牌、营销、工具、系统、工作室案例：优先 `translucent_object_editorial`。
12. AI、未来感、趋势、创意展览、抽象概念、品牌视觉：优先 `glassmorphism_gradient_blob`。
13. 深度思考、认知、策略、极简口号、书封、品牌宣言：优先 `embossed_typography_poster` 或 `white_mono_texture_editorial`。
14. 单个关键词、栏目名、品牌词、年轻化视觉实验：优先 `acrylic_dimensional_type`。
15. AI 搜索、探索、信息检索、发现、推荐、知识寻找：优先 `dark_neon_search_ui`。
16. 产品界面、搜索框、控制器、智能家居、效率工具、轻科技：优先 `soft_neumorphism_ui`。
17. 新品发布、数字主题、品牌发布会、极简科技主视觉：优先 `minimal_line_shadow_brand`。
18. 作品集、建筑、路径规划、职业路线、人生路径、空间叙事：优先 `minimal_architecture_portfolio`。
19. 情绪疗愈、内耗、孤独、亲密关系、自我照顾、被爱、好运、鼓励、生活感悟、内在小孩：优先 `minimal_healing_metaphor_comic`。
20. 极简主义、生活方式、个人手册、创作宣言、书封：优先 `retro_minimal_poster_illustration`。
21. 团队协作、共同成长、组织文化、未来愿景、品牌广告：优先 `editorial_balloon_collage`。
22. 宏大阶段、未来路径、系统升级、人生转折、空间隐喻：优先 `transparent_architectural_type`。
23. 职业人物、行业精神、工程建筑、创始人故事、人物专访：优先 `paper_cut_profile_silhouette`。
24. 信念提醒、每日一句、极简语录、心理暗示、单个关键词：优先 `torn_paper_note_minimal`。
25. 好运、发财、治愈、可爱、祝福、轻松社媒图：优先 `fluffy_soft_typography`。
26. 希望、成长、新开始、复原力、上升、疗愈：优先 `cloud_typography_cover`。
27. 清洁、焕新、重启、洗去旧状态、梦想变大、生活刷新：优先 `foam_bubble_typography`。
28. 品牌徽章、社群身份、学院风、服饰、工具包、设计师身份：优先 `embroidered_patch_brand`。
29. 高端、奢华、节日、仪式感、庆典、成就、财富：优先 `luxury_gold_typography`。
30. 人生路径、职业选择、城市迁移、过去与现在、成长路线：优先 `miniature_map_life_scene`。
31. 任务清单、执行力、打卡、习惯养成、目标拆解、项目计划：优先 `miniature_checklist_scene`。
32. 匠心、劳动节、手工、服饰、工艺、细节、制造业：优先 `fabric_micro_scene_ad`。
33. 品牌名、组织价值、教育场景、家庭场景、字母空间、系列广告：优先 `giant_letter_lifestyle_scene`。
34. 女性、母亲节、思念、关系、疗愈、花、花瓣、节气、东方花艺、文学情绪：优先 `oriental_floral_minimal_editorial`。
35. 哲学、人生道路、修行、自律、克己、觉察、禅意、东方智慧、格言：优先 `zen_ink_philosophy_poster`。
36. 黑白线稿、编辑插画、品牌视觉系统、角色 set、城市生活、杂志版式、包装、网站首屏、App 概念：优先 `editorial_line_character`。
37. AI 方法论、设计原则、信任、验证、判断力、工作流原则、创作者手册、playbook、三条原则、用一个物品隐喻一个观点：优先 `editorial_object_annotation_card`。
38. 社会议题、就业、人口、城市、群体行为、商业趋势、用户规模、公共政策、平台经济、组织协作，或需要很多真实小人组成符号、文字、数字或图形：优先 `crowd_typography_scene`。
39. 突出标题文字本身、关键词视觉化、品牌字、栏目名、短句封面、材质字体、醒目主视觉，或希望根据内容自动设计字体质感：优先 `semantic_material_typography`。
40. AI 工作流、系统流程、工具链、Prompt 结构、自动化步骤、内容生产系统、从混乱到输出、卡住到跑起来，或希望用轻松怪诞的小人表现复杂流程：优先 `quirky_doodle_character_flow`。
41. 极简表达人物、关系、旅行、毕业、学习、课堂、会议、城市、灵感、孤独、陪伴、个人成长，或希望用少量线条抽象表达一个概念：优先 `minimal_line_art`。
42. 系统架构、服务流程、产品功能总览、空间地图、园区/工厂/城市、AI Agent 节点关系、SaaS 模块关系，或需要统一等距视角、可组合组件和系列化品牌插画：优先 `isometric_modular_system`。
43. Skill、SOP、提示词库、方法论、系统搭建、标准化、知识资产、流程封装、AI 工作流、路由判断、商业路径、出海增长，或需要黑白高对比、巨型文字、专业系统封面：优先 `monochrome_system_editorial`。
44. 当用户主题涉及发展史、演化、变迁、从 A 到 B、过去到现在、技术迭代、行业阶段、工具演进、产品版本、时间线讲解时，优先 `isometric_timeline_miniature`。
45. 当用户需要幽默创意配图、视觉双关、真实物品与手绘角色结合、表达压力 / 疲惫 / 焦虑 / 卡住 / 情绪隐喻，或希望“用一个日常物品变成画面关键部分”时，优先 `real_object_doodle_composite`。
46. 当用户需要 3D 版怪诞小人、夸张表情、观点吐槽、情绪状态、工作/学习压力、AI 工作流节点、轻剧情或社媒表情图时，优先 `expressive_3d_quirky_character`。
47. 当用户输入中文短词、成语、祝福语、情绪词、人物命运词、社会观察词，或要求高级概念海报、文学感封面、强中文大字视觉时，优先 `giant_chinese_concept_poster`。
48. 当用户输入中文金句、观点短句、品牌口号、成语祝福、情绪短句，或希望文字组成物品轮廓、填充物体、沿轨迹排列、变成纹理和隐喻物时，优先 `glyph_object_imagery`。
49. 当用户需要竖版教程长图、手机端知识海报、SOP、规则卡、项目复盘、AI 工作流、多步骤方法论，或参考黑白线稿人物 + 多面板信息图时，优先 `editorial_line_infographic_poster`。
50. 当用户需要用乱线毛球萌物表达情绪、知识、办公状态、教育内容、品牌吉祥物或角色家族，或希望用大眼睛、单色点缀和强情绪动作转译抽象概念时，优先 `scribble_furball_character_family`。
51. 当用户提供产品名称、产品图片、商品卖点，或要求电商海报、新品发布图、品牌广告、产品卖点图、功能拆解图、产品概念视觉时，优先 `premium_product_ad_poster`。
52. 用户未指定风格时，必须进入可视化选择器；普通文章可把 `handdrawn_knowledge_card` 作为首选推荐，但不得自动确认或直接生成。
53. 若用户说“封面用 A，正文用 B”，封面和正文分别套用对应 style_id。

## 49 号毛球角色家族风 IP 硬约束

使用 `scribble_furball_character_family` 时，必须把参考角色视为同一个固定 IP，而不是自由发挥的“毛球类角色”：

- 身体固定为近圆但不规整的乱线团；使用中等数量、粗细均匀的黑色手绘长线和大小环线，中心略密、外缘较松，白底明显透出，外围保留数根逸出大弧线。
- 面部固定为两只紧贴、略有高低差的巨大纵向椭圆白眼和较小黑色椭圆瞳孔；眼睛直接嵌在线团中，不画眼镜式外框，不画常规鼻子。
- 四肢固定为粗细适中的黑色单线、三至四指极简黑手和扁平黑色小椭圆脚。
- 每个角色固定佩戴同款明黄色长围巾：宽围巾横向包住身体下半部，右侧垂下一条带流苏的围巾尾，并保留少量黑色褶皱线。
- 状态变体只能改变瞳孔朝向、嘴型、动作和道具；不得改变线团身体、眼睛比例、四肢画法和黄色围巾。
- 只使用黑色、纸白和明黄色。禁止过度稀疏光滑的钢丝球、密集涂黑的煤球、缺少围巾、不同物种家族、3D、写实、贴纸风和额外颜色。

## 视觉锚点

每个最终图片 prompt 都必须附加所选 style_id 对应的风格锚点。默认风格锚点：

> 整体风格像高质量中文知识博主的手绘知识图解系统：暖白纸感背景，黑灰细线手绘，低饱和浅色块，中文手写字，自然成熟，克制精致，留白充足，轻商业内容资产感。不要做成 PPT，不要课程课件，不要科技海报，不要 3D，不要可爱儿童插画，不要复杂信息图，不要密集小字，不要高饱和颜色，不要英文乱码，不要水印。

详细风格规范见 `references/visual_style.md`；风格库和非默认模板见 `references/style_options.md`；默认封面与正文模板见 `references/cover_prompt.md`、`references/body_prompt.md`。当任务需要“更会讲故事、更像品牌资产、更适合长期运营”时，参考 `references/kashika_method.md` 的可视化研究所方法论：先语言整理，再控制信息密度，最后做角色化、图解化和系列化交付。若任务涉及系统、流程、空间、路径、模块关系或品牌插画组件库，参考 `references/kashika_isometric_method.md`，使用统一轴测网格、三面信息分工和模块化组件思路。若任务涉及“解释度取舍、数据准确性、问卷故事化、角色连续性、品牌复用性或出图质量评估”，参考 `references/kashika_advanced_methods.md` 的解释度滑杆、7轴评估、数据动作映射和漫画共感型信息图。当使用 `quirky_doodle_character_flow` 时，额外参考 `references/quirky_doodle_method.md`；并把 `assets/examples/xiaohei/` 作为小黑角色稳定性校准素材，只参考角色比例、线条密度、白底留白和红/橙/蓝短批注克制度，不照抄样图构图。当使用 `expressive_3d_quirky_character` 时，把 `assets/examples/3d_quirky/` 作为 3D 角色校准素材，只参考角色质感、表情强度、动作夸张度、极简背景和低饱和色，不照抄样图人物、服装、构图或道具。当使用 `giant_chinese_concept_poster` 时，优先生成竖版 3:4 或 4:5 概念海报，确保巨大中文主标题清晰完整、无错字缺笔，并让隐喻场景与大字发生空间关系。当使用 `glyph_object_imagery` 时，优先生成 1:1 创意字体图，先为句子选择最贴切的具象物品、动作或场景，再让文字参与轮廓、内部填充、边缘轨迹、纹理或结构，确保核心文字准确可读。当使用 `editorial_line_infographic_poster` 时，优先生成竖版 9:16 教程长图，用黑白线稿人物、多面板圆角卡片、编号黑点、箭头连接和少量浅黄/淡紫强调块组织 4-6 个步骤，确保手机端可读。当使用 `premium_product_ad_poster` 时，优先生成竖版 4:5 / 2:3 / 9:16 商业广告海报；若用户提供产品图，先保持产品主体外观、颜色、结构、材质和关键特征，再做创意广告设计。

## 输入类型与处理

### 只给主题

- 自动补全：副标题、核心隐喻、画面元素、小人动作、小人气泡、底部判断句。
- 默认生成封面 prompt 或直接生图。

### 给一篇文章

先提取：文章主题、目标读者、核心观点、主要论证结构、适合视觉化的关键段落。再生成 1 张封面 + 多张正文图。

### 明确要正文配图

根据用户给出的题图、结构、核心模块、必要注释、小人动作、小人气泡、底部判断句直接生成正文 prompt；缺失字段自动补齐。若主题复杂，先补齐 `关键词抽取 → 要约 → 目标读者 → 信息密度 → 视觉类型`，再写 prompt。

### 明确要封面图

根据主题、副标题、核心隐喻、画面元素、小人动作、小人气泡、底部判断句生成封面 prompt；缺失字段自动补齐。

### 明确要 logo / 图标

- 当用户说“生成一个 logo”“生成一个图标”“做一个 app icon”“做一个功能小图标”时，固定进入 logo/图标模式。
- 默认生成 1 张 1:1 方形图标，不生成 21:9 封面或 16:9 正文配图。
- 先提取：主体物、使用场景、主色、辅助色、点缀色、核心识别特征、是否需要辅助物。
- 未指定图标风格时不要自动选择；按需求计算 8 套图标风格的推荐顺序并展示可视化选择器。未命中明显方向时把 `cute_3d_plastic_icon` 放在首选推荐位，由用户确认。
- logo 需求默认理解为“可作为 App / 产品 logo 的图标化视觉符号”；除用户明确要求字标外，不生成品牌名、长文字、标签或水印。

### 批量生图

创建批量计划。若可调用 `image_gen`，默认隐藏 prompt 并逐张调用 `image_gen` 生成图片；若不可调用 `image_gen` 或用户明确要清单，则输出 JSON 或 Markdown 清单。不得使用其他工具替代生图。

## 封面图规则

- 比例：21:9 横版宽屏。
- 固定左右结构：左侧约 45% 是主标题 + 副标题；右侧约 55% 是手绘概念图 / 流程图 / 系统图 / 隐喻图。
- 右下角或右侧放极简抽象小人 + 气泡。
- 底部放一句轻量判断句。
- 字段：主题、副标题、核心隐喻、画面元素、小人动作、小人气泡、底部判断句。
- 使用 `references/cover_prompt.md` 的模板渲染完整 prompt。

## 正文配图规则

- 比例：16:9 横版。
- 正文图不是封面，不采用左大标题右图解结构。
- 结构：顶部可选小标题；中间主体图解；周围少量短注释；右侧或右下角可有小人气泡；底部一句判断式结论。
- 字段：题图、结构、核心模块、必要注释、小人动作、小人气泡、底部判断句。
- 使用 `references/body_prompt.md` 的模板渲染完整 prompt。

### 正文结构选择

- 闭环机制图：系统循环、内容流动、持续迭代。
- 横向流程图：步骤、路径、生产流程。
- 分类树图：层级、分类、组成结构。
- 左右对比图：旧方法 vs 新方法、误区 vs 正解。
- 结构类比图：脚手架、抽屉、盒子、工厂、管道、工作台等隐喻。
- 风险路径图：错误路径、损耗、陷阱、失败原因。
- 光谱选择图：从低到高、轻到重、手动到自动、简单到复杂。
- 随附场景图：真实使用场景，人物、工具、输入、输出和轻流程。

## 解释度与质量评估

复杂配图在生成前先判断 `explanation_level`：

- 5：图解型；最准确，适合手册、教程、教材、数据事实。
- 4：夸张型；保留结构并放大重点，适合封面、广告、核心观点。
- 3：场景型；补充前后情境，适合服务介绍、案例、故事板。
- 1：世界观型；解释责任低，氛围和余韵高，适合品牌主视觉和书封。

每张图生成前用 7 个轴快速自检：品牌调性、目标读者、复用性、记忆符号、独有信息、趣味钩子、可访问性/安全性。数据图额外检查来源、指标、比较维度、可表达结论和禁止推出的结论。

## 文章拆图流程

按 `references/article_breakdown.md` 执行：

1. 提炼文章主题、目标读者、核心观点、主要段落。
2. 先找“认知锚点”，不要平均按段落配图；优先画核心判断、认知断点、输入输出闭环、分流、前后对比、承接路径、常见坑和角色状态变化。
3. 判断图片数量：默认 1 封面 + 3 到 6 正文；短文可 1 到 3 正文；长文通常不超过 9 张正文，用户指定优先。
4. 将每个认知锚点映射成一种正文结构或视觉隐喻；一张图只表达一个核心结构。
5. 为每张图补全字段，并写清 `core_idea`、`target_reader`、`keyword_extract`、`compressed_sentence`、`visual_type`、`information_density`、`deformation_level`、`visual_anchor`、`main_action`、`short_labels` 等策略信息。
6. 生成完整 prompt，或在 `image_gen` 可用时直接调用 `image_gen`；不得使用其他工具替代生图。

## 轴测模块系统风规则

当使用 `isometric_modular_system` 时：

1. 先判断信息任务是路径、结构、流程、空间、层级还是数据关系。
2. 先定统一等距/轴测网格，再画元素；所有物体服从同一套轴线。
3. 避免近大远小、强透视、强景深和真实 3D 渲染；目标是清晰空间，不是电影镜头。
4. 把对象拆成可复用模块：平台、方块、楼层、路径、台阶、管道、桥、门、窗口、浮动信息卡片、人物和图标。
5. 明确三面分工：顶面承载路径/地图/平面关系，侧面承载结构/层级/状态，正向文字承载标题和关键说明。
6. 用尺寸、位置、颜色、描边控制视觉优先级；不要让所有模块同等显眼。
7. 输出时写清 `information_task`、`isometric_angle`、`grid_rule`、`main_plane`、`modules`、`path_or_relation`、`component_reuse_notes`。

## 怪诞小人风多图规则

当用户要求用 `quirky_doodle_character_flow` 拆成多张正文配图时：

1. 先从文章里找认知锚点：核心判断、断点、输入输出、分流、对比、承接、常见坑或角色状态。
2. 每张图只表达一个锚点；不要把多个流程、多个观点塞进一张图。
3. 版式不固定，按内容选择 Workflow、系统局部、前后对比、角色状态、概念隐喻、方法分层、地图路线或小漫画分镜。
4. 每张图保留同一个小黑怪作为连续角色；优先参照 `assets/examples/xiaohei/` 的小黑 IP 稳定特征：黑色实心不规则身体、白色圆点眼、细胳膊细腿、空表情、认真冷幽默、像低调系统操作员。
5. 小黑必须执行核心动作，例如拉、扛、塞、捞、压、称、缝、剪、拧、守、推、接、拆、标记、回收；不要只是站在角落看。
6. 如果去掉小黑后隐喻仍完整，说明小黑太装饰，必须重写 prompt。
7. 每张图最多 3 到 5 个主要元素，中文手写标注最多 5 到 8 处，每处 2 到 8 字。
8. 背景使用纯白；红色表示风险或错误路径，橙色表示主行动，蓝色表示反馈或长期回路。
9. 不要写“流程图/系统架构/常见坑/路线图”等类型标题；不要做成 PPT 或正式流程图。
10. 多张图之间保持同样白底、线条粗细、角色造型和标注风格，但构图可以变化。

## Typography Intelligence

当选择 `semantic_material_typography`（语义字体风）时，不要盲目套固定材质。先判断标题语义：

1. 稳定、根基、长期结构：用木头、石头、混凝土、钉子、年轮。
2. 成长、自然、复利、耐心：用苔藓、种子、藤蔓、叶片、土壤、石头。
3. 混乱、不确定、消散、脆弱：用灰尘、沙子、颗粒、碎片、烟雾。
4. 甜蜜、奖励、能量、愉悦：用蜂蜜、糖浆、水果、果冻、奶油。
5. AI、系统、自动化、工程：用机械零件、齿轮、电路、金属、螺丝。
6. 创作、品味、表达、签名：用油漆、笔触、墨迹、金色颜料、手工痕迹。
7. Prompt、生成、迭代、设计过程：用线稿描边、构造线、叠层字体、未完成字形。
8. 信任、关系、身份、归属：用布料、刺绣、皮革、纸张、印章、绳结。

始终优先保证文字可读。材质创意不能破坏标题识别。`randomness` 可用 `low` / `medium` / `high`；当用户说“给我惊喜”“随机发挥”时，可启用 surprise_mode，最多混合两种相关材质。

## 输出格式

### Markdown 拆图规划

```markdown
文章核心主题：
{文章核心主题}
目标读者：
{目标读者}
系列视觉定位：
高质量中文知识博主的手绘知识图解系统，暖白纸感背景，黑灰细线手绘，低饱和浅色块，留白充足，轻商业内容资产感。
建议图片数量：
1 张封面 + {N} 张正文配图
---
图 1｜封面图
主题：{主题}
副标题：{副标题}
核心隐喻：{核心隐喻}
画面元素：{画面元素}
小人动作：{小人动作}
小人气泡：{小人气泡}
底部判断句：{底部判断句}
图片提示词：{完整封面 prompt}
---
图 2｜正文配图
题图：{题图}
结构：{结构}
核心模块：{核心模块}
必要注释：{必要注释}
小人动作：{小人动作}
小人气泡：{小人气泡}
底部判断句：{底部判断句}
图片提示词：{完整正文 prompt}
```

### 批量 JSON 清单

当用户要求 JSON、程序化、Codex-ready、批量清单或不直接生图时输出：

```json
{
  "series_title": "",
  "visual_style": "handdrawn_knowledge_card",
  "global_style_prompt": "整体风格像高质量中文知识博主的手绘知识图解系统：暖白纸感背景，黑灰细线手绘，低饱和浅色块，中文手写字，自然成熟，克制精致，留白充足，轻商业内容资产感。不要做成 PPT，不要课程课件，不要科技海报，不要 3D，不要可爱儿童插画，不要复杂信息图，不要密集小字，不要高饱和颜色，不要英文乱码，不要水印。",
  "images": [
    {
      "id": "cover_01",
      "type": "cover",
      "aspect_ratio": "21:9",
      "style_id": "handdrawn_knowledge_card",
      "title": "",
      "subtitle": "",
      "prompt": ""
    },
    {
      "id": "body_01",
      "type": "body",
      "aspect_ratio": "16:9",
      "style_id": "handdrawn_knowledge_card",
      "title": "",
      "structure": "",
      "prompt": ""
    }
  ]
}
```

## 可选脚本

`scripts/prompt_schema.py` 提供可复用的字段校验、封面/正文 prompt 渲染和批量 JSON 组装逻辑。需要稳定批量生产或把拆图结果转成 JSON 时，优先使用该脚本或复用其中模板。
