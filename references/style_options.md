# 可选风格库

默认风格是 `handdrawn_knowledge_card`（手绘知识风）。只有用户明确指定其他风格，或用户说“合适的风格 / 帮我选风格 / 随机风格”时，才按主题自动匹配；“随机风格”也不做纯随机。正文解释图仍优先使用手绘知识风；多数非知识卡片风更适合封面图、头图、海报或系列主视觉。

## 风格选择表

```json
{
  "styles": [
    {"style_id": "handdrawn_knowledge_card", "style_name": "手绘知识风", "best_for": ["默认；正文配图、知识图解、方法论、流程图、对比图"]},
    {"style_id": "oriental_editorial_illustration", "style_name": "典籍山水风", "best_for": ["文化、历史、人文、哲学类高级封面"]},
    {"style_id": "study_note_card", "style_name": "学习笔记风", "best_for": ["学习方法、笔记整理、步骤教程、知识清单"]},
    {"style_id": "pastel_learning_pyramid", "style_name": "粉彩金字塔风", "best_for": ["分层模型、学习金字塔、能力进阶、成长路径"]},
    {"style_id": "childlike_cultural_infographic", "style_name": "童趣科普风", "best_for": ["传统文化科普、儿童教育、器物拆解"]},
    {"style_id": "frosted_glass_editorial", "style_name": "磨砂情绪风", "best_for": ["心理情绪、孤独感、音乐艺术主题"]},
    {"style_id": "translucent_object_editorial", "style_name": "透明物件风", "best_for": ["设计主题、品牌设计、作品集封面、工具系统封面"]},
    {"style_id": "glassmorphism_gradient_blob", "style_name": "玻璃气泡风", "best_for": ["品牌视觉、创意展览、趋势报告、AI 主题"]},
    {"style_id": "embossed_typography_poster", "style_name": "纸雕字体风", "best_for": ["极简封面、品牌口号、深度思考、书封设计"]},
    {"style_id": "acrylic_dimensional_type", "style_name": "亚克力字风", "best_for": ["品牌关键词、栏目标题、创意概念、年轻化封面"]},
    {"style_id": "dark_neon_search_ui", "style_name": "霓虹搜索风", "best_for": ["AI 搜索、知识探索、信息检索、灵感发现"]},
    {"style_id": "black_void_glowing_hands", "style_name": "黑场肢体风", "best_for": ["心理主题、情绪主题、关系连接、孤独感"]},
    {"style_id": "soft_neumorphism_ui", "style_name": "柔光界面风", "best_for": ["产品功能封面、AI 工具界面、智能家居、效率工具"]},
    {"style_id": "minimal_line_shadow_brand", "style_name": "线性品牌风", "best_for": ["新品发布、品牌封面、科技产品、数字主题"]},
    {"style_id": "white_mono_texture_editorial", "style_name": "白色肌理风", "best_for": ["深度文章封面、设计作品集、哲学主题、个人品牌"]},
    {"style_id": "minimal_architecture_portfolio", "style_name": "建筑线稿风", "best_for": ["作品集封面、人生路径、职业路径、空间叙事"]},
    {"style_id": "minimal_healing_metaphor_comic", "style_name": "治愈漫画风", "best_for": ["情绪疗愈、内耗、孤独、亲密关系、自我照顾"]},
    {"style_id": "retro_minimal_poster_illustration", "style_name": "复古海报风", "best_for": ["极简主义、生活方式、个人手册、创作宣言、书封"]},
    {"style_id": "editorial_balloon_collage", "style_name": "气球拼贴风", "best_for": ["团队协作、未来愿景、组织文化、品牌广告、社群主题"]},
    {"style_id": "transparent_architectural_type", "style_name": "透明字境风", "best_for": ["宏大阶段、未来路径、系统升级、人生转折、空间隐喻"]},
    {"style_id": "paper_cut_profile_silhouette", "style_name": "纸雕剪影风", "best_for": ["职业人物、行业精神、工程建筑、人物专访"]},
    {"style_id": "torn_paper_note_minimal", "style_name": "撕纸便签风", "best_for": ["一句话封面、信念提醒、极简语录、每日提醒"]},
    {"style_id": "fluffy_soft_typography", "style_name": "毛绒字体风", "best_for": ["好运、发财、治愈、可爱、祝福、轻松社媒图"]},
    {"style_id": "cloud_typography_cover", "style_name": "云朵字体风", "best_for": ["希望、成长、新开始、复原力、上升、疗愈"]},
    {"style_id": "foam_bubble_typography", "style_name": "泡沫字体风", "best_for": ["清洁、焕新、重启、梦想、生活方式海报"]},
    {"style_id": "embroidered_patch_brand", "style_name": "刺绣徽章风", "best_for": ["品牌徽章、学院风、社群身份、工具包、服饰品牌"]},
    {"style_id": "luxury_gold_typography", "style_name": "金属奢华风", "best_for": ["节日海报、高端品牌、仪式感、成就、庆典"]},
    {"style_id": "miniature_map_life_scene", "style_name": "微缩地图风", "best_for": ["人生选择、职业路径、城市迁移、成长路线"]},
    {"style_id": "miniature_checklist_scene", "style_name": "微缩清单风", "best_for": ["任务管理、行动清单、习惯养成、目标拆解"]},
    {"style_id": "fabric_micro_scene_ad", "style_name": "布料微缩风", "best_for": ["劳动节、匠心、手工、服饰品牌、工艺精神"]},
    {"style_id": "giant_letter_lifestyle_scene", "style_name": "巨字生活风", "best_for": ["品牌广告、教育、家庭、城市、组织价值"]},
    {"style_id": "oriental_floral_minimal_editorial", "style_name": "花艺留白风", "best_for": ["女性主题、母亲节、思念、关系、疗愈、节气"]},
    {"style_id": "zen_ink_philosophy_poster", "style_name": "禅意水墨风", "best_for": ["哲学、人生路径、自我修炼、觉察、东方智慧"]},
    {"style_id": "editorial_line_character", "style_name": "编辑线稿风", "best_for": ["品牌视觉、杂志海报、网站首屏、包装、角色系统、城市生活场景"]},
    {"style_id": "editorial_object_annotation_card", "style_name": "具象物品标注编辑风", "best_for": ["AI方法论、设计思维、知识卡片、认知模型、信任验证、工作流原则"]}
  ]
}
```

## 风格分组

A. 知识图解类：`handdrawn_knowledge_card`、`study_note_card`、`pastel_learning_pyramid`、`childlike_cultural_infographic`。
B. 东方 / 人文 / 情绪插画类：`oriental_editorial_illustration`、`minimal_healing_metaphor_comic`、`black_void_glowing_hands`、`oriental_floral_minimal_editorial`、`zen_ink_philosophy_poster`。
C. 极简设计 / 材质海报类：`frosted_glass_editorial`、`translucent_object_editorial`、`glassmorphism_gradient_blob`、`soft_neumorphism_ui`、`minimal_line_shadow_brand`、`white_mono_texture_editorial`、`minimal_architecture_portfolio`、`editorial_line_character`、`editorial_object_annotation_card`。
D. 字体材质类：`acrylic_dimensional_type`、`embossed_typography_poster`、`transparent_architectural_type`、`fluffy_soft_typography`、`cloud_typography_cover`、`foam_bubble_typography`、`luxury_gold_typography`。
E. 拼贴 / 纸张 / 手工材质类：`retro_minimal_poster_illustration`、`editorial_balloon_collage`、`paper_cut_profile_silhouette`、`torn_paper_note_minimal`、`embroidered_patch_brand`。
F. 微缩场景 / 品牌广告类：`miniature_map_life_scene`、`miniature_checklist_scene`、`fabric_micro_scene_ad`、`giant_letter_lifestyle_scene`。

## 默认匹配规则

自动匹配优先级：

1. 用户明确指定风格时，优先服从。
2. 用户说“合适的风格”“帮我选风格”“随机风格”时，按内容合理选择，不做纯随机。
3. 正文配图、方法论解释、流程、对比、知识系统：优先 `handdrawn_knowledge_card`。
4. 文化、历史、人文、哲学、东方智慧、古籍、文明：优先 `oriental_editorial_illustration`。
5. 学习方法、笔记整理、复习、考试、效率技巧：优先 `study_note_card`。
6. 学习金字塔、层级模型、能力进阶、成长路径、主动学习 / 被动学习：优先 `pastel_learning_pyramid`。
7. 儿童教育、传统文化科普、器物拆解、博物馆内容：优先 `childlike_cultural_infographic`。
8. 孤独、情绪、心理、音乐、艺术展、安静、疏离：优先 `frosted_glass_editorial` 或 `black_void_glowing_hands`。
9. 设计、作品集、品牌、营销、工具、系统、工作室案例：优先 `translucent_object_editorial`。
10. AI、未来感、趋势、创意展览、抽象概念、品牌视觉：优先 `glassmorphism_gradient_blob`。
11. 深度思考、认知、策略、极简口号、书封、品牌宣言：优先 `embossed_typography_poster` 或 `white_mono_texture_editorial`。
12. 单个关键词、栏目名、品牌词、年轻化视觉实验：优先 `acrylic_dimensional_type`。
13. AI 搜索、探索、信息检索、发现、推荐、知识寻找：优先 `dark_neon_search_ui`。
14. 产品界面、搜索框、控制器、智能家居、效率工具、轻科技：优先 `soft_neumorphism_ui`。
15. 新品发布、数字主题、品牌发布会、极简科技主视觉：优先 `minimal_line_shadow_brand`。
16. 作品集、建筑、路径规划、职业路线、人生路径、空间叙事：优先 `minimal_architecture_portfolio`。
17. 情绪疗愈、内耗、孤独、亲密关系、自我照顾、被爱、好运、鼓励、生活感悟、内在小孩：优先 `minimal_healing_metaphor_comic`。
18. 极简主义、生活方式、个人手册、创作宣言、书封：优先 `retro_minimal_poster_illustration`。
19. 团队协作、共同成长、组织文化、未来愿景、品牌广告：优先 `editorial_balloon_collage`。
20. 宏大阶段、未来路径、系统升级、人生转折、空间隐喻：优先 `transparent_architectural_type`。
21. 职业人物、行业精神、工程建筑、创始人故事、人物专访：优先 `paper_cut_profile_silhouette`。
22. 信念提醒、每日一句、极简语录、心理暗示、单个关键词：优先 `torn_paper_note_minimal`。
23. 好运、发财、治愈、可爱、祝福、轻松社媒图：优先 `fluffy_soft_typography`。
24. 希望、成长、新开始、复原力、上升、疗愈：优先 `cloud_typography_cover`。
25. 清洁、焕新、重启、洗去旧状态、梦想变大、生活刷新：优先 `foam_bubble_typography`。
26. 品牌徽章、社群身份、学院风、服饰、工具包、设计师身份：优先 `embroidered_patch_brand`。
27. 高端、奢华、节日、仪式感、庆典、成就、财富：优先 `luxury_gold_typography`。
28. 人生路径、职业选择、城市迁移、过去与现在、成长路线：优先 `miniature_map_life_scene`。
29. 任务清单、执行力、打卡、习惯养成、目标拆解、项目计划：优先 `miniature_checklist_scene`。
30. 匠心、劳动节、手工、服饰、工艺、细节、制造业：优先 `fabric_micro_scene_ad`。
31. 品牌名、组织价值、教育场景、家庭场景、字母空间、系列广告：优先 `giant_letter_lifestyle_scene`。
32. 女性、母亲节、思念、关系、疗愈、花、花瓣、节气、东方花艺、文学情绪：优先 `oriental_floral_minimal_editorial`。
33. 哲学、人生道路、修行、自律、克己、觉察、禅意、东方智慧、格言：优先 `zen_ink_philosophy_poster`。
34. 黑白线稿、编辑插画、品牌视觉系统、角色 set、城市生活、杂志版式、包装、网站首屏、App 概念：优先 `editorial_line_character`。
35. AI 方法论、设计原则、信任、验证、判断力、工作流原则、创作者手册、playbook、三条原则、用一个物品隐喻一个观点：优先 `editorial_object_annotation_card`。
36. 用户未指定时，普通文章封面默认 `handdrawn_knowledge_card`。
37. 若用户说“封面用 A，正文用 B”，封面和正文分别套用对应 style_id。

## 风格详情

## 1. handdrawn_knowledge_card｜手绘知识风

适合：默认；正文配图、知识图解、方法论、流程图、对比图。

## 2. oriental_editorial_illustration｜典籍山水风

适合：文化、历史、人文、哲学类高级封面。

## 3. study_note_card｜学习笔记风

适合：学习方法、笔记整理、步骤教程、知识清单。

## 4. pastel_learning_pyramid｜粉彩金字塔风

适合：分层模型、学习金字塔、能力进阶、成长路径。

## 5. childlike_cultural_infographic｜童趣科普风

适合：传统文化科普、儿童教育、器物拆解。

## 6. frosted_glass_editorial｜磨砂情绪风

适合：心理情绪、孤独感、音乐艺术主题。

## 7. translucent_object_editorial｜透明物件风

适合：设计主题、品牌设计、作品集封面、工具系统封面。

## 8. glassmorphism_gradient_blob｜玻璃气泡风

适合：品牌视觉、创意展览、趋势报告、AI 主题。

## 9. embossed_typography_poster｜纸雕字体风

适合：极简封面、品牌口号、深度思考、书封设计。

## 10. acrylic_dimensional_type｜亚克力字风

适合：品牌关键词、栏目标题、创意概念、年轻化封面。

## 11. dark_neon_search_ui｜霓虹搜索风

适合：AI 搜索、知识探索、信息检索、灵感发现。

## 12. black_void_glowing_hands｜黑场肢体风

适合：心理主题、情绪主题、关系连接、孤独感。

## 13. soft_neumorphism_ui｜柔光界面风

适合：产品功能封面、AI 工具界面、智能家居、效率工具。

## 14. minimal_line_shadow_brand｜线性品牌风

适合：新品发布、品牌封面、科技产品、数字主题。

## 15. white_mono_texture_editorial｜白色肌理风

适合：深度文章封面、设计作品集、哲学主题、个人品牌。

## 16. minimal_architecture_portfolio｜建筑线稿风

适合：作品集封面、人生路径、职业路径、空间叙事。

## 17. minimal_healing_metaphor_comic｜治愈漫画风

适合：情绪疗愈、内耗、孤独、亲密关系、自我照顾。

## 18. retro_minimal_poster_illustration｜复古海报风

适合：极简主义、生活方式、个人手册、创作宣言、书封。

## 19. editorial_balloon_collage｜气球拼贴风

适合：团队协作、未来愿景、组织文化、品牌广告、社群主题。

## 20. transparent_architectural_type｜透明字境风

适合：宏大阶段、未来路径、系统升级、人生转折、空间隐喻。

## 21. paper_cut_profile_silhouette｜纸雕剪影风

适合：职业人物、行业精神、工程建筑、人物专访。

## 22. torn_paper_note_minimal｜撕纸便签风

适合：一句话封面、信念提醒、极简语录、每日提醒。

## 23. fluffy_soft_typography｜毛绒字体风

适合：好运、发财、治愈、可爱、祝福、轻松社媒图。

## 24. cloud_typography_cover｜云朵字体风

适合：希望、成长、新开始、复原力、上升、疗愈。

## 25. foam_bubble_typography｜泡沫字体风

适合：清洁、焕新、重启、梦想、生活方式海报。

## 26. embroidered_patch_brand｜刺绣徽章风

适合：品牌徽章、学院风、社群身份、工具包、服饰品牌。

## 27. luxury_gold_typography｜金属奢华风

适合：节日海报、高端品牌、仪式感、成就、庆典。

## 28. miniature_map_life_scene｜微缩地图风

适合：人生选择、职业路径、城市迁移、成长路线。

## 29. miniature_checklist_scene｜微缩清单风

适合：任务管理、行动清单、习惯养成、目标拆解。

## 30. fabric_micro_scene_ad｜布料微缩风

适合：劳动节、匠心、手工、服饰品牌、工艺精神。

## 31. giant_letter_lifestyle_scene｜巨字生活风

适合：品牌广告、教育、家庭、城市、组织价值。

## 32. oriental_floral_minimal_editorial｜花艺留白风

适合：女性主题、母亲节、思念、关系、疗愈、节气。

## 33. zen_ink_philosophy_poster｜禅意水墨风

适合：哲学、人生路径、自我修炼、觉察、东方智慧。


## 34. editorial_line_character｜编辑线稿风

适合：品牌视觉、杂志海报、网站首屏、包装、角色系统、城市生活场景。

核心：黑白极简线稿人物、几何扁平比例、城市日常行为、杂志式强排版、大留白、少量柔和色块，适合把品牌、产品、活动或抽象主题转成一套编辑插画视觉系统。


## 35. editorial_object_annotation_card｜具象物品标注编辑风

适合：AI方法论、设计思维、知识卡片、认知模型、信任验证、工作流原则。

核心：真实具象物品 + 抽象观点映射 + 编辑排版 + 标注系统。用一个高清真实物品作为可被观察和标注的隐喻模型，左侧承载强观点标题与三条原则，右侧用虚线箭头、手写注释和极简小人讲清方法论。

结构化字段建议：主题、标题、副标题、核心物品、隐喻含义、原则1、说明1、原则2、说明2、原则3、说明3、标注1、标注2、标注3、小人动作、系列名。
