# 可选风格库

本文件是风格选择、自动推荐和 `visualize` 交互选型的单一风格来源。交互控件不得发明本文件之外的 style_id；推荐排序、封面比例和正文图数量的交互规则见 `interactive_selection.md`。

`handdrawn_knowledge_card`（手绘知识风）是普通知识内容的常见首选推荐，不是自动直出的默认值。用户未明确指定有效风格时，必须先进入 `Visualize:visualize` 选择器；“合适的风格 / 帮我选风格 / 随机风格”只影响推荐排序，不允许自动确认。正文解释图可优先推荐手绘知识风；多数非知识卡片风更适合封面图、头图、海报或系列主视觉。

## 风格选择表

```json
{
  "styles": [
    {"style_id": "handdrawn_knowledge_card", "style_name": "手绘知识风", "best_for": ["常见首选推荐；正文配图、知识图解、方法论、流程图、对比图"]},
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
    {"style_id": "editorial_object_annotation_card", "style_name": "具象标注风", "best_for": ["AI方法论、设计思维、知识卡片、认知模型、信任验证、工作流原则"]},
    {"style_id": "crowd_typography_scene", "style_name": "人群造字风", "best_for": ["社会议题、财经封面、就业问题、人口变化、城市议题、商业趋势、群体行为"]},
    {"style_id": "semantic_material_typography", "style_name": "语义字体风", "best_for": ["关键词封面、品牌标题、栏目标题、概念海报、单词视觉化、强标题主视觉"]},
    {"style_id": "quirky_doodle_character_flow", "style_name": "怪诞小人风", "best_for": ["AI工作流、系统流程、正文配图、方法论拆解、工具链说明、长文认知锚点"]},
    {"style_id": "minimal_line_art", "style_name": "线条艺术风", "best_for": ["亲密关系、旅行、毕业、学习、课堂、会议、城市、灵感、个人成长、极简封面"]},
    {"style_id": "isometric_modular_system", "style_name": "轴测模块系统风", "best_for": ["SaaS架构、服务流程、空间地图、系统关系、模块化品牌插画"]},
    {"style_id": "monochrome_system_editorial", "style_name": "黑白系统风", "best_for": ["Skill封面、SOP封面、提示词库、方法论手册、AI工作流、标准化流程"]},
    {"style_id": "isometric_timeline_miniature", "style_name": "时间微缩风", "best_for": ["技术演化", "行业发展史", "工具变迁", "产品迭代", "内容生产演化", "学习方式演化", "AI工作流演化", "知识管理演化", "品牌发展历程", "商业模式演化", "教育工具演化", "创作者工具链"], "not_best_for": ["单一情绪表达", "纯标题海报", "复杂数据图表", "严肃财经封面", "大量文字型知识卡片"], "core_features": ["45度等距俯视", "微型3D时间轴", "横向分段展台", "4到6个时代区域", "时代代表物", "微缩人物互动", "柔和材质", "均匀光照", "顶部标题和副标题", "教育博物馆感"]},
    {"style_id": "real_object_doodle_composite", "style_name": "实物涂鸦风", "best_for": ["幽默封面", "创意配图", "社媒传播图", "情绪表达", "工作压力", "学习压力", "心理状态", "生活方式内容", "视觉双关", "轻量观点", "正文配图"], "not_best_for": ["严肃财经报告", "复杂系统流程", "数据图表", "高端方法论封面", "东方水墨", "正式企业封面"], "core_features": ["真实日常物品", "黑色手绘线稿", "白色纸张背景", "视觉双关", "物品成为角色关键部分", "漫画表情", "自然阴影", "大量留白", "短手写吐槽"]},
    {"style_id": "expressive_3d_quirky_character", "style_name": "3D怪表情风", "best_for": ["情绪表达", "观点吐槽", "文章封面", "正文配图", "社媒表情图", "AI工作流节点", "创作者状态", "学习状态", "工作压力", "产品提示", "轻剧情配图"], "not_best_for": ["严肃财经封面", "东方水墨", "高端黑白系统封面", "复杂数据图表", "大量文字知识卡", "抽象材质字体", "真实产品摄影"], "core_features": ["圆润3D小人", "夸张表情", "态度动作", "极简背景", "低饱和色", "柔和灯光", "短句吐槽", "3D版怪诞小人"]},
    {"style_id": "giant_chinese_concept_poster", "style_name": "大字海报风", "best_for": ["中文概念海报", "文学感封面", "人物命运主题", "情绪关键词", "节日祝福海报", "城市观察", "社会情绪", "品牌态度海报", "短词强视觉", "朋友圈传播图", "公众号头图", "展览级主题海报"], "not_best_for": ["复杂流程图", "正文解释图", "多节点知识卡片", "数据图表", "工具教程", "大量文字海报", "儿童科普", "可爱表情包"], "core_features": ["竖版3:4或4:5", "巨大中文主标题", "文字绝对主体", "词义驱动画面", "强视觉隐喻", "人物与大字发生关系", "小字只保留三处", "高级克制", "强情绪", "展览级概念海报"]},
    {"style_id": "premium_product_ad_poster", "style_name": "产品海报风", "best_for": ["电商主图", "新品发布海报", "品牌广告", "产品卖点图", "详情页首屏", "小红书产品封面", "科技产品海报", "时尚产品广告", "运动装备海报", "功能拆解图", "产品概念视觉", "AI产品包装图"], "not_best_for": ["纯情绪短句", "文学概念海报", "复杂流程图", "时间演化图", "水墨禅意图", "手绘知识卡", "怪诞小人流程图"], "core_features": ["竖版商业海报", "产品绝对主角", "高质量产品摄影", "超真实CGI", "专业棚拍光线", "巨大标题", "卖点标注", "功能图标", "时尚人物", "夸张尺度", "极端场景", "爆炸拆解", "微缩人物互动", "高级品牌感"]},
    {"style_id": "glyph_object_imagery", "style_name": "字物意象风", "best_for": ["中文金句", "观点短句", "品牌口号", "成语祝福", "情绪短句", "文字造物", "创意字体图", "社媒传播图", "东方趣味视觉符号"], "not_best_for": ["复杂流程图", "多节点知识卡片", "数据图表", "真实产品广告", "长篇正文海报", "纯写实插画"], "core_features": ["文字参与造型", "文字和物品融合", "具象隐喻物", "粗黑手写书法", "极简线稿", "少量点睛色", "红色印章", "大量留白", "幽默意境", "清晰可读"]},
    {"style_id": "editorial_line_infographic_poster", "style_name": "竖版线稿长图风", "best_for": ["竖版教程长图", "SOP", "规则卡", "项目复盘", "AI工作流", "多步骤方法论", "知识海报", "手机端阅读长图"], "not_best_for": ["纯情绪海报", "真实产品广告", "单一大字概念海报", "复杂数据图表", "写实场景插画"], "core_features": ["竖版9:16", "黑白线稿人物", "粗黑中文标题", "2x2或纵向多面板", "圆角信息卡片", "编号黑点", "箭头连接", "少量浅黄淡紫强调块", "底部总结区", "手机端可读"]},
    {"style_id": "scribble_furball_character_family", "style_name": "毛球角色家族风", "best_for": ["情绪表达", "知识卡片", "办公状态", "教育内容", "品牌IP", "角色设定", "社媒传播图"], "not_best_for": ["写实人物", "复杂数据图表", "高端产品摄影", "多色复杂背景", "严肃财经报告"], "core_features": ["中等密度乱线团", "中心略密外缘较松", "巨大纵向椭圆白眼", "固定黄色流苏围巾", "黑色单线四肢", "强情绪动作", "同一IP状态变体", "黑白骨架", "单一亮色点缀", "干净留白", "治愈呆萌", "高识别IP感"]}
  ]
}
```

## 风格分组

A. 知识图解类：`handdrawn_knowledge_card`、`study_note_card`、`pastel_learning_pyramid`、`childlike_cultural_infographic`、`quirky_doodle_character_flow`、`real_object_doodle_composite`、`editorial_line_infographic_poster`。
B. 东方 / 人文 / 情绪插画类：`oriental_editorial_illustration`、`minimal_healing_metaphor_comic`、`black_void_glowing_hands`、`oriental_floral_minimal_editorial`、`zen_ink_philosophy_poster`、`minimal_line_art`、`expressive_3d_quirky_character`、`giant_chinese_concept_poster`。
C. 极简设计 / 材质海报类：`premium_product_ad_poster`、`frosted_glass_editorial`、`translucent_object_editorial`、`glassmorphism_gradient_blob`、`soft_neumorphism_ui`、`minimal_line_shadow_brand`、`white_mono_texture_editorial`、`minimal_architecture_portfolio`、`editorial_line_character`、`editorial_object_annotation_card`、`isometric_modular_system`、`monochrome_system_editorial`。
D. 字体材质类：`acrylic_dimensional_type`、`embossed_typography_poster`、`transparent_architectural_type`、`fluffy_soft_typography`、`cloud_typography_cover`、`foam_bubble_typography`、`luxury_gold_typography`、`semantic_material_typography`、`glyph_object_imagery`。
E. 拼贴 / 纸张 / 手工材质类：`retro_minimal_poster_illustration`、`editorial_balloon_collage`、`paper_cut_profile_silhouette`、`torn_paper_note_minimal`、`embroidered_patch_brand`。
F. 微缩场景 / 品牌广告类：`miniature_map_life_scene`、`miniature_checklist_scene`、`isometric_timeline_miniature`、`fabric_micro_scene_ad`、`giant_letter_lifestyle_scene`、`crowd_typography_scene`。
G. 空间系统 / 轴测图解类：`isometric_modular_system`。

H. logo / 图标类：`cute_3d_plastic_icon`、`candy_glass_3d_icon`、`airbnb_soft_miniature_icon`、`circular_2_5d_vector_icon`、`soft_frosted_glass_icon`、`circular_3d_texture_icon`、`frosted_glass_ui_icon`、`pastel_reward_badge_icon`。

## logo / 图标模式

当用户说“生成一个 logo / 图标 / 小图标 / app icon / 功能图标”时，固定进入 1:1 方形图标模式，不再按文章封面或正文配图处理。可用图标风格：

| style_id | 风格名 | 适合场景 |
| --- | --- | --- |
| `cute_3d_plastic_icon` | 3D 新拟物风小图标 | 常见首选推荐；工具、功能、App 图标 |
| `candy_glass_3d_icon` | 3D 糖果风格图标 | 低对比、清爽可爱、半透明糖果质感 |
| `airbnb_soft_miniature_icon` | Airbnb 风软拟物图标 | 旅行、生活方式、露营、家居、厨房等温暖场景 |
| `circular_2_5d_vector_icon` | 圆形轻拟物风格图标 | 金刚区、功能入口、中文移动 App 矢量图标 |
| `soft_frosted_glass_icon` | 软糖风格图标 | 奶霜、毛玻璃、柔软透明质感的独立图标 |
| `circular_3d_texture_icon` | 环形 3D 质感图标 | 圆形渐变底、系统级 3D App icon |
| `frosted_glass_ui_icon` | 磨砂玻璃质感小图标 | 钱包、文件夹、卡片、面板等简洁 UI 图标 |
| `pastel_reward_badge_icon` | 少女风奖牌图标 | 奖励徽章、等级奖牌、儿童或少女风粉彩图标 |

## 推荐匹配规则

自动匹配优先级：

1. 用户明确指定风格时，优先服从。
2. 用户说“生成一个 logo / 图标 / 小图标 / app icon / 功能图标”时，进入 logo/图标模式；未指定图标风格时仍先展示选择器。奖牌/徽章/少女/儿童优先推荐 `pastel_reward_badge_icon`，金刚区/矢量/2.5D 优先推荐 `circular_2_5d_vector_icon`，旅行/露营/生活方式优先推荐 `airbnb_soft_miniature_icon`，毛玻璃/半透明/软糖优先推荐 `soft_frosted_glass_icon`，钱包/文件夹/卡片/UI 圆角层优先推荐 `frosted_glass_ui_icon`，圆形底/系统级 App icon 优先推荐 `circular_3d_texture_icon`，未命中明显风格时优先推荐 `cute_3d_plastic_icon`。
3. 用户说“合适的风格”“帮我选风格”“随机风格”时，按内容生成推荐排序并展示选择器，不做纯随机，也不自动确认。
4. 正文配图、方法论解释、流程、对比、知识系统：优先 `handdrawn_knowledge_card`。
5. 文化、历史、人文、哲学、东方智慧、古籍、文明：优先 `oriental_editorial_illustration`。
6. 学习方法、笔记整理、复习、考试、效率技巧：优先 `study_note_card`。
7. 学习金字塔、层级模型、能力进阶、成长路径、主动学习 / 被动学习：优先 `pastel_learning_pyramid`。
8. 儿童教育、传统文化科普、器物拆解、博物馆内容：优先 `childlike_cultural_infographic`。
9. 孤独、情绪、心理、音乐、艺术展、安静、疏离：优先 `frosted_glass_editorial` 或 `black_void_glowing_hands`。
10. 设计、作品集、品牌、营销、工具、系统、工作室案例：优先 `translucent_object_editorial`。
11. AI、未来感、趋势、创意展览、抽象概念、品牌视觉：优先 `glassmorphism_gradient_blob`。
12. 深度思考、认知、策略、极简口号、书封、品牌宣言：优先 `embossed_typography_poster` 或 `white_mono_texture_editorial`。
13. 单个关键词、栏目名、品牌词、年轻化视觉实验：优先 `acrylic_dimensional_type`。
14. AI 搜索、探索、信息检索、发现、推荐、知识寻找：优先 `dark_neon_search_ui`。
15. 产品界面、搜索框、控制器、智能家居、效率工具、轻科技：优先 `soft_neumorphism_ui`。
16. 新品发布、数字主题、品牌发布会、极简科技主视觉：优先 `minimal_line_shadow_brand`。
17. 作品集、建筑、路径规划、职业路线、人生路径、空间叙事：优先 `minimal_architecture_portfolio`。
18. 情绪疗愈、内耗、孤独、亲密关系、自我照顾、被爱、好运、鼓励、生活感悟、内在小孩：优先 `minimal_healing_metaphor_comic`。
19. 极简主义、生活方式、个人手册、创作宣言、书封：优先 `retro_minimal_poster_illustration`。
20. 团队协作、共同成长、组织文化、未来愿景、品牌广告：优先 `editorial_balloon_collage`。
21. 宏大阶段、未来路径、系统升级、人生转折、空间隐喻：优先 `transparent_architectural_type`。
22. 职业人物、行业精神、工程建筑、创始人故事、人物专访：优先 `paper_cut_profile_silhouette`。
23. 信念提醒、每日一句、极简语录、心理暗示、单个关键词：优先 `torn_paper_note_minimal`。
24. 好运、发财、治愈、可爱、祝福、轻松社媒图：优先 `fluffy_soft_typography`。
25. 希望、成长、新开始、复原力、上升、疗愈：优先 `cloud_typography_cover`。
26. 清洁、焕新、重启、洗去旧状态、梦想变大、生活刷新：优先 `foam_bubble_typography`。
27. 品牌徽章、社群身份、学院风、服饰、工具包、设计师身份：优先 `embroidered_patch_brand`。
28. 高端、奢华、节日、仪式感、庆典、成就、财富：优先 `luxury_gold_typography`。
29. 人生路径、职业选择、城市迁移、过去与现在、成长路线：优先 `miniature_map_life_scene`。
30. 任务清单、执行力、打卡、习惯养成、目标拆解、项目计划：优先 `miniature_checklist_scene`。
31. 匠心、劳动节、手工、服饰、工艺、细节、制造业：优先 `fabric_micro_scene_ad`。
32. 品牌名、组织价值、教育场景、家庭场景、字母空间、系列广告：优先 `giant_letter_lifestyle_scene`。
33. 女性、母亲节、思念、关系、疗愈、花、花瓣、节气、东方花艺、文学情绪：优先 `oriental_floral_minimal_editorial`。
34. 哲学、人生道路、修行、自律、克己、觉察、禅意、东方智慧、格言：优先 `zen_ink_philosophy_poster`。
35. 黑白线稿、编辑插画、品牌视觉系统、角色 set、城市生活、杂志版式、包装、网站首屏、App 概念：优先 `editorial_line_character`。
36. AI 方法论、设计原则、信任、验证、判断力、工作流原则、创作者手册、playbook、三条原则、用一个物品隐喻一个观点：优先 `editorial_object_annotation_card`。
37. 社会议题、就业、人口、城市、群体行为、商业趋势、用户规模、公共政策、平台经济、组织协作，或需要很多真实小人组成符号、文字、数字或图形：优先 `crowd_typography_scene`。
38. 突出标题文字本身、关键词视觉化、品牌字、栏目名、短句封面、材质字体、醒目主视觉，或希望根据内容自动设计字体质感：优先 `semantic_material_typography`。
39. AI 工作流、系统流程、工具链、Prompt 结构、自动化步骤、内容生产系统、从混乱到输出、卡住到跑起来，或希望用轻松怪诞的小人表现复杂流程：优先 `quirky_doodle_character_flow`。
40. 极简表达人物、关系、旅行、毕业、学习、课堂、会议、城市、灵感、孤独、陪伴、个人成长，或希望用少量线条抽象表达一个概念：优先 `minimal_line_art`。
41. 系统架构、服务流程、产品功能总览、空间地图、园区/工厂/城市、AI Agent 节点关系、SaaS 模块关系，或需要统一等距视角、可组合组件和系列化品牌插画：优先 `isometric_modular_system`。
42. Skill、SOP、提示词库、方法论、系统搭建、标准化、知识资产、流程封装、AI 工作流、路由判断、商业路径、出海增长，或需要黑白高对比、巨型文字、专业系统封面：优先 `monochrome_system_editorial`。
43. 当用户主题涉及发展史、演化、变迁、从 A 到 B、过去到现在、技术迭代、行业阶段、工具演进、产品版本、时间线讲解时，优先 `isometric_timeline_miniature`（时间微缩风）。
44. 当用户需要幽默创意配图、视觉双关、真实物品与手绘角色结合、表达压力 / 疲惫 / 焦虑 / 卡住 / 情绪隐喻，或希望“用一个日常物品变成画面关键部分”时，优先 `real_object_doodle_composite`（实物涂鸦风）。
45. 当用户需要 3D 版怪诞小人、夸张表情、观点吐槽、情绪状态、工作/学习压力、AI 工作流节点、轻剧情或社媒表情图时，优先 `expressive_3d_quirky_character`（3D怪表情风）。
46. 当用户输入中文短词、成语、祝福语、情绪词、人物命运词、社会观察词，或要求高级概念海报、文学感封面、强中文大字视觉时，优先 `giant_chinese_concept_poster`（大字海报风）。
47. 当用户输入中文金句、观点短句、品牌口号、成语祝福、情绪短句，或希望文字组成物品轮廓、填充物体、沿轨迹排列、变成纹理和隐喻物时，优先 `glyph_object_imagery`（字物意象风）。
48. 当用户需要竖版教程长图、手机端知识海报、SOP、规则卡、项目复盘、AI 工作流、多步骤方法论，或参考黑白线稿人物 + 多面板信息图时，优先 `editorial_line_infographic_poster`（竖版线稿长图风）。
49. 当用户需要用乱线毛球萌物表达情绪、知识、办公状态、教育内容、品牌吉祥物或角色家族，或希望用大眼睛、单色点缀和强情绪动作转译抽象概念时，优先 `scribble_furball_character_family`（毛球角色家族风）。
50. 当用户提供产品名称、产品图片、商品卖点，或要求电商海报、新品发布图、品牌广告、产品卖点图、功能拆解图、产品概念视觉时，优先 `premium_product_ad_poster`（产品海报风）。
51. 用户未指定风格时必须展示选择器；普通文章封面可把 `handdrawn_knowledge_card` 作为首选推荐，但不得自动确认或直接生成。
52. 若用户说“封面用 A，正文用 B”，封面和正文分别套用对应 style_id。

## 风格详情

## 1. handdrawn_knowledge_card｜手绘知识风

适合：常见首选推荐；正文配图、知识图解、方法论、流程图、对比图。

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


## 35. editorial_object_annotation_card｜具象标注风

适合：AI方法论、设计思维、知识卡片、认知模型、信任验证、工作流原则。

核心：真实具象物品 + 抽象观点映射 + 编辑排版 + 标注系统。用一个高清真实物品作为可被观察和标注的隐喻模型，左侧承载强观点标题与三条原则，右侧用虚线箭头、手写注释和极简小人讲清方法论。

结构化字段建议：主题、标题、副标题、核心物品、隐喻含义、原则1、说明1、原则2、说明2、原则3、说明3、标注1、标注2、标注3、小人动作、系列名。


## 36. crowd_typography_scene｜人群造字风

适合：社会议题、财经封面、就业问题、人口变化、城市议题、商业趋势、群体行为。

核心：高空俯视白色空间，大量真实微缩小人排列成文字、数字、符号、路径或图表，搭配像印在地面上的财经杂志式标题、目录、期号和页码。适合公共议题、群体关系、社会结构和趋势封面。

结构化字段建议：主题、刊名或栏目、标题、副标题、核心图形、隐喻含义、人群状态、散落元素、顶部目录、底部信息。


## 37. semantic_material_typography｜语义字体风

适合：关键词封面、品牌标题、栏目标题、概念海报、单词视觉化、强标题主视觉。

核心：文字本身是主视觉，先判断标题语义，再自动选择最贴合含义的真实材质、物体结构或自然纹理。它是字体材质类的总控风格：如果用户指定具体材质，服从指定；如果只给标题和语义，就自动选材质。

结构化字段建议：主题、标题、副标题、语义方向、指定材质、质感关键词、背景、randomness、surprise_mode。


## 38. quirky_doodle_character_flow｜怪诞小人风

适合：AI工作流、系统流程、正文配图、方法论拆解、工具链说明、自动化流程、长文里的关键判断和卡点。

核心：纯白背景、黑色细线手绘、怪诞小黑角色、少量红/橙/蓝手写标注。小黑优先参考 `assets/examples/xiaohei/` 的内置校准样图：黑色实心不规则身体、白点眼、细胳膊细腿、空表情、认真冷幽默；只参考角色 DNA 和画面密度，不复刻样图构图。先从文章中抓“认知锚点”（核心判断、断点、输入输出、分流、前后对比、承接路径、常见坑、角色状态），再把它变成一个怪诞但成立的物理动作。小黑必须承担核心动作，不能只是站在旁边。版式不固定，按内容动作选择 Workflow、系统局部、前后对比、角色状态、概念隐喻、方法分层、地图路线或小漫画分镜。

一致性规则：16:9 横版正文配图；纯白背景，不用纸纹和渐变；主体占 40%-60%，至少 35% 留白；中文标注最多 5-8 处，每处 2-8 字；橙色只表示主流程，红色只表示风险/问题/重点，蓝色只表示反馈/系统状态/补充说明；不要写“流程图/系统架构/常见坑”等类型标题；不要做成 PPT 或正式流程图。

结构化字段建议：任务、主题、标题、副标题、放置位置、核心意思、认知锚点、核心结构、视觉隐喻、流程动作、节点1、节点2、节点3、节点4、反馈回路、风险标注、短标注、小人动作、底部判断句。详细规则见 `quirky_doodle_method.md`。


## 39. minimal_line_art｜线条艺术风

适合：亲密关系、旅行、毕业、学习、课堂、会议、城市、灵感、个人成长、极简封面。

核心：用尽可能少的连续黑色线条表达人物、关系、场景、城市或抽象概念。背景纯白或暖白，大量留白，只使用极少点缀色，整体优雅、克制、安静、有情绪和概念感。

结构化字段建议：任务、主题、标题、副标题、核心主体、动作或关系、核心隐喻、点缀色元素、线条类型、情绪。


## 40. monochrome_system_editorial｜黑白系统风

适合：Skill封面、SOP封面、提示词库、方法论手册、AI工作流、系统搭建、知识资产、标准化流程、企业内训、商业路线图、增长路径、出海策略。

核心：黑白灰高对比，巨型粗体文字压场，结合透明档案盒、索引卡、锁、阶梯、门、路径线、路线图、货船、集装箱、柱状图、微缩人物等系统隐喻物件，并使用细线网格、编号、条形码、REF 编号和工业化信息排版，形成专业系统手册和 SOP 封面感。

结构化字段建议：任务、主题、主视觉文字、标题、副标题、核心物件、隐喻含义、标签1、标签2、标签3、标签4、阶段1、阶段2、阶段3、阶段4、编号、日期、英文小标题。


## 41. isometric_modular_system｜轴测模块系统风

适合：SaaS架构、服务流程、产品功能总览、空间地图、系统关系、AI Agent 节点关系、模块化品牌插画。

核心：统一等距/轴测视角，远近不缩放，所有对象服从同一斜向网格。把复杂系统拆成平台、方块、楼层、路径、台阶、管道、桥、门、窗口、浮动信息卡片、微型人物和图标。顶面承载路径/地图/平面关系，侧面承载结构/层级/状态，标题和关键说明保持正向可读。

结构化字段建议：information_task、target_reader、isometric_angle、grid_rule、main_plane、modules、path_or_relation、priority_object、labels、component_reuse_notes。详细规则见 `kashika_isometric_method.md`。

## 42. isometric_timeline_miniature｜时间微缩风

一句话描述：用等距视角的微型 3D 场景，把一个主题从早期到现代的演化过程，拆成多个时代展台，像一座横向展开的微型历史博物馆。

适合：技术演化、行业发展史、工具变迁、产品迭代、内容生产演化、学习方式演化、AI 工作流演化、知识管理演化、品牌发展历程、商业模式演化、教育工具演化、创作者工具链。尤其适合“从 A 到 B”“某某发展史”“某某演化过程”“某某的过去、现在和未来”“5 个阶段看懂某某”。

不适合：单一情绪表达、纯标题海报、复杂数据图表、严肃财经封面、高端黑白系统封面、大量文字型知识卡片。它是叙事型时间演化图，不是强标题封面。

风格锚点：整体风格为时间微缩风：使用 45° 等距俯视视角，创建一个横向展开的微型 3D 时间轴展台。画面像微型博物馆、桌面沙盘或精致教育插画。底座被分成 4-6 个清晰时代区域，从左到右展示主题从早期到现代的演化。每个区域放置该时代最具代表性的物件、工具、设备、环境或技术，并加入少量微型人物与场景互动。顶部居中放大标题，下方放副标题和极简时间轴图标。整体材质柔和、干净、精致，光线均匀，背景为纯色或柔和渐变。不要复杂写实场景，不要拥挤，不要卡通夸张，不要高饱和杂乱，不要密集文字。

英文锚点：Clean isometric miniature 3D timeline diorama style, 45-degree top-down perspective, horizontal stepped base divided into clear time periods, each section shows era-specific objects, tools, environments, or technology. Add tiny stylized figures interacting with each stage, minimal facial detail. Soft refined materials, realistic PBR shading, neutral balanced lighting, clean solid background. Top center title, subtitle showing From [start era] to [modern era], small timeline icon underneath. Educational museum-like miniature evolution diagram, not cluttered, not cartoonish, not dense infographic.

Prompt 模板：

```text
请生成一张时间微缩风的中文信息图封面。
主题是「{主题}」。画面使用 45° 等距俯视视角，做成一个横向展开的微型 3D 时间轴展台，像精致的微型博物馆、桌面沙盘或教育展览模型。
底座从左到右分成 {阶段数量} 个时代区域，每个区域代表一个阶段：
1. {阶段1名称}：放置 {阶段1代表物}
2. {阶段2名称}：放置 {阶段2代表物}
3. {阶段3名称}：放置 {阶段3代表物}
4. {阶段4名称}：放置 {阶段4代表物}
5. {阶段5名称}：放置 {阶段5代表物}
每个阶段加入 1-3 个微型人物，小人正在使用、观察、搬运或体验该阶段的工具和场景。人物要小巧、简化、有模型感，不要复杂表情。
画面顶部居中写标题「{标题}」，使用清晰粗体字体。标题下方写副标题「从 {起点时代} 到 {现代阶段}」。副标题下面放一条极简时间轴图标，表示时间推进。
底座下方为每个阶段加短标签，标签简洁清楚。阶段之间用细线、箭头、台阶或分隔线表示时间流动。
整体风格为时间微缩风：45° 等距视角、微型 3D 时间轴、横向分段展台、时代代表物、微缩人物互动、柔和材质、均匀光照、干净背景、教育图解感。不要做成普通扁平信息图，不要复杂真实场景，不要卡通夸张，不要高饱和杂乱，不要密集文字。
```

结构化字段：

```text
风格：时间微缩风
主题：
标题：
起点时代：
现代阶段：
阶段数量：
阶段1名称：
阶段1代表物：
阶段2名称：
阶段2代表物：
阶段3名称：
阶段3代表物：
阶段4名称：
阶段4代表物：
阶段5名称：
阶段5代表物：
背景颜色：
整体情绪：教育感 / 科技感 / 怀旧感 / 未来感 / 商业感
```

示例：AI 内容生产演化。标题“内容生产演化”，从手工写作时代到 AI Agent 时代；阶段可为手写时代、电脑写作、搜索时代、AI 辅助、Agent 时代；代表物依次使用纸张钢笔书桌手稿、台式电脑键盘文档软件、搜索框网页资料堆、聊天界面提示词卡片生成按钮、自动化工作台多模态屏幕流程节点小机器人。

## 43. real_object_doodle_composite｜实物涂鸦风

一句话描述：把真实生活物品嵌入黑色手绘线稿中，让物品变成角色身体、头发、负担、情绪、道具或场景的一部分，形成幽默、聪明、意外的视觉双关。

适合：情绪表达、幽默海报、创意封面、社媒传播图、生活方式内容、心理状态、创作者状态、工作压力、学习压力、关系隐喻、轻量观点、正文配图、视觉双关。尤其适合“我被压垮了”“我已经焦了”“脑子炸了”“压力太大”“灵感卡住”“被工作掏空”“关系是一团线”等主题。

不适合：严肃财经报告、复杂系统流程、高端品牌方法论、数据图表、东方水墨、正式企业封面、大段文字知识卡片。它的强项是一个画面讲一个隐喻，不是承载复杂信息。

风格锚点：整体风格为实物涂鸦风：干净白色或暖白纸张背景，真实日常物品被物理放置在画面中，并与黑色手绘线稿角色无缝结合。真实物品必须成为角色或场景的关键部分，例如头、头发、大脑、身体、负担、心脏、武器、衣服、道具或爆炸效果。手绘部分使用简单黑色墨线，像快速漫画草图，表情夸张、动作明确、幽默而有情绪。画面通过真实物品和线稿之间的语义错位形成视觉双关，既聪明又易懂。背景极简，大量留白，真实物品有自然光影和摄影质感。可以加入一句短手写吐槽文字。不要复杂背景，不要完整彩色插画，不要 3D，不要普通拼贴，不要让物品只是装饰，不要密集文字。

英文锚点：Real object doodle composite style: clean white paper background, one real everyday object physically placed in the scene and seamlessly integrated into a black ink hand-drawn cartoon illustration. The real object becomes a key part of the character or scene, such as the head, hair, brain, body, burden, heart, weapon, clothing, prop, or explosion. Simple expressive black line art, quick sketch feeling, exaggerated facial expression and clear action. The image creates a witty visual pun by turning the object into a meaningful part of the drawing. Photorealistic object, natural shadows, minimalist negative space, optional short handwritten caption. Not a full color illustration, not 3D, not cluttered, not ordinary collage, the object must not be decorative only.

Prompt 模板：

```text
请生成一张实物涂鸦风的创意插画。
主题是「{主题}」。画面使用干净白色或暖白纸张背景，大量留白，竖版 9:16，柔和摄影棚光线。
画面中放置一个真实日常物品：「{真实物品}」。这个物品必须有真实摄影质感、自然阴影、清晰纹理和高细节。
请把这个真实物品巧妙地变成手绘角色或场景的关键部分：「{物品变成什么}」。它可以变成角色的头、头发、大脑、身体、负担、心脏、武器、衣服、道具、爆炸或情绪本体。
围绕真实物品画一个黑色手绘线稿角色。角色是「{角色设定}」，正在「{动作}」。手绘部分使用简单黑色墨线，像快速漫画草图，表情夸张、动作明确，和真实物品无缝衔接。
这个画面要表达的视觉双关是：「{视觉双关}」。整体要幽默、聪明、有情绪，但画面极简。
可以在下方加入一句短手写文字：「{短句}」。文字像随手写在纸上的吐槽，不要正式排版。
整体风格为实物涂鸦风：真实日常物品 + 黑色手绘线稿 + 视觉双关 + 白色留白背景 + 摄影质感 + 幽默表达。不要复杂背景，不要完整彩色插画，不要 3D，不要普通拼贴，不要让物品只是装饰，不要密集文字。
```

结构化字段：

```text
风格：实物涂鸦风
主题：
真实物品：
物品变成什么：
角色设定：
动作：
视觉双关：
短句：
画幅：9:16 / 1:1 / 4:5
情绪：幽默 / 疲惫 / 焦虑 / 崩溃 / 温柔 / 讽刺 / 惊喜
```

示例：工作压力。真实物品是一块真实石头，把石头变成疲惫小男孩背上的巨大负担；小男孩弯腰往前走、满头大汗，视觉双关是“压力像一块真实的石头压在身上”，短句“我只是有点累”。

## 44. expressive_3d_quirky_character｜3D怪表情风

一句话描述：用一个圆润、夸张、表情丰富的 3D 小人角色，在极简背景中做出搞怪表情和肢体动作，把抽象情绪、观点、工作状态或流程节点表现成有传播感的角色画面。

适合：情绪表达、观点吐槽、文章封面、正文配图、社媒表情图、AI 工作流节点、创作者状态、学习状态、工作压力、产品提示、轻松解释、流程中的角色替身、失败/卡住/完成/发布等状态图。

不适合：严肃财经封面、东方水墨、高端黑白系统封面、复杂数据图表、大量文字知识卡、抽象材质字体、真实产品摄影。它适合“情绪和态度”，不适合“严肃系统权威”。

核心：这是 38 号「怪诞小人风」的 3D 角色版。38 号用黑白线稿小黑解释流程；44 号用立体表情角色表达状态、态度、吐槽、反应和轻剧情。角色应头大身小、脸颊饱满、皮肤柔软、服装简单、表情夸张，眉毛、眼神、嘴角和脸部肌肉承担主要情绪。

表情库：不屑、无语、嫌弃、崩溃、焦虑、疲惫、得意、开心、怀疑、委屈、自信、震惊、偷笑、认真。动作库：抱臂、叉腰、OK 手势、抱头、摊手、指向、后仰、拖步、趴桌、观察、举牌、推文件箱、被纸张淹没、站在流程节点上、坐在巨大按钮旁、从洞里探头。

一致性规则：参考 `assets/examples/3d_quirky/` 的角色质感、表情强度、动作夸张度、极简背景和低饱和颜色；不要照抄样图人物、服装、构图或道具。背景使用纯白、浅灰、浅米或低饱和纯色；角色为高质量 3D 渲染、圆润柔软、柔和棚拍光；不要真实儿童摄影、复杂背景、过度可爱玩具感、高饱和颜色或密集文字。

结构化字段建议：任务、主题、标题、副标题、角色设定、表情、动作、情绪或观点、道具、短句、背景颜色、服装、画幅。

## 45. giant_chinese_concept_poster｜大字海报风

一句话描述：以巨型中文文字作为绝对主体，根据词义自动生成最匹配的视觉隐喻、空间关系、人物命运感和色彩气质，形成高级、克制、强情绪的概念海报。

适合：中文概念海报、文学感封面、人物命运主题、情绪关键词、节日祝福海报、城市观察、社会情绪、品牌态度海报、短词强视觉、朋友圈传播图、小红书封面、公众号头图、展览级主题海报。尤其适合“平安喜乐、外卖、孤独、重启、破局、自由、沉默、回家、选择、边界、长期主义、松弛感、普通人、夜归、热爱、清醒”等短词。

不适合：复杂流程图、正文解释图、多节点知识卡片、数据图表、工具教程、大量文字海报、儿童科普、可爱表情包。这个风格适合“一个词打穿一个情绪”。

核心：词义驱动画面，而不是模板驱动画面。大字是第一视觉，隐喻场景是第二视觉，小字文案是第三视觉。巨型中文主标题必须清晰完整、无错字、无缺笔，占画面 45%-75%，可以与场景遮挡、穿插、开窗、透光，但不能破坏可读性。

构图类型：字中开门型（希望、重启、平安、归来、未来、选择）；城市夹缝型（外卖、打工、夜归、租房、孤独、城市生活）；碑刻命运型（命运、克制、告别、沉默、牺牲、尊严）；诗意祝愿型（平安、喜乐、祝福、团圆、春风、好运）；极简锋利型（真相、判断、边界、自由、破局、选择）。

小字规则：只保留三处——左上角 2-4 个关键词，右侧竖排一句命运感短句，左下角一句传播力总结句。不要再加说明文。

结构化字段建议：任务、输入文字、关键词、命运感短句、总结句、视觉隐喻、色彩气质、字体气质、人物或主体、画幅。

## 46. premium_product_ad_poster｜产品海报风

一句话描述：用高端商业摄影、超清产品主视觉、巨型排版、功能卖点标注、时尚人物或创意尺度关系，把任意产品生成具有电商转化力和品牌视觉感的竖版广告海报。

适合：电商主图、新品发布海报、品牌广告、产品卖点图、详情页首屏、小红书产品封面、科技产品海报、时尚产品广告、运动装备海报、功能拆解图、产品概念视觉、AI 产品包装图。尤其适合耳机、手机、手表、眼镜、球鞋、高跟鞋、香水、饮料、咖啡、包、美妆、键盘、相机、家居、智能硬件、AI 工具产品、课程产品、知识产品包装。

不适合：纯情绪短句、文学概念海报、复杂流程图、时间演化图、水墨禅意图、手绘卡片知识图、怪诞小人流程图。这个风格必须有明确产品主体。

核心：产品主角化、卖点视觉化、品牌广告化、场景创意化。产品必须清晰、完整、质感强，占画面 35%-70%，产品边缘锐利、细节清楚、材质真实可信，不能被人物或文字抢走主体地位。若用户提供产品图片，优先保留产品主体外观、颜色、结构、材质和关键特征，不随意改变产品品类。

构图类型：英雄近景型（耳机、手机、香水、手表、小家电、美妆）；时尚巨物型（眼镜、鞋、包、服饰、家具、潮流单品）；极端场景型（饮料、户外用品、运动装备、汽车、耐用产品）；爆炸拆解型（鞋、耳机、机械产品、键盘、相机、电脑、科技硬件）；微缩互动型（鞋、包、家具、珠宝、玩具、家居产品、文创产品）。

卖点规则：保留 3-6 个核心卖点，每个卖点配小图标、细线标注、数字模块或简洁信息块。信息必须短，不写长段说明。

结构化字段建议：任务、产品名称、产品图片、产品品类、核心材质或质感、主标题、副标题、创意方向、视觉隐喻、卖点1、卖点2、卖点3、卖点4、卖点5、品牌气质、色彩倾向、画幅。

## 47. glyph_object_imagery｜字物意象风

一句话描述：将用户输入的文字、观点或金句，提炼成一个最贴切的具象物品、动作或场景，并用手写书法字、粗黑笔触、极简线稿与少量点睛色，把文字和物品形态融合成一张有意境、有巧思、有记忆点的创意字体图。

适合：中文金句、观点短句、品牌口号、成语祝福、情绪短句、社媒传播图、手写文字 logo、东方趣味视觉符号。尤其适合“只要火候够，迟早会翻身”“把话说开”“撑住”“人生果然”“很多时候就差临门一脚”等一句话视觉化。

不适合：复杂流程图、多节点知识卡片、数据图表、真实产品广告、长篇正文海报、纯写实插画。它的强项是把一句话变成一个可一眼看懂又觉得巧妙的视觉隐喻。

核心：文字即图形，图形即寓意，物品即隐喻。先读懂一句话，再找到它的隐喻物，最后让文字排成这个物的形状。文字必须参与造型，而不是贴在图上。

融合方式：字成物、字填物、字沿线、字变景、字作符号。文字可以组成物品轮廓、填满物品内部、沿着边缘或动作轨迹弯曲，或变成物品的纹理、蒸汽、水流、枝叶、尾巴、影子和结构。

视觉规则：白色或浅灰背景，粗黑手写书法字，干刷笔触，极简线稿，大量留白，少量点睛色和小红印章。颜色不是装饰，而是帮助物品成立。核心文字必须准确、清晰、可读，不要为了造型牺牲识别。

结构化字段建议：核心文字、文字类型、核心情绪、推荐物品、融合方式、主色、点睛色、是否加红印章、画幅。


## 48. editorial_line_infographic_poster｜竖版线稿长图风

一句话描述：把流程、教程、规则、SOP、AI 工作流或项目复盘，组织成手机端可读的 9:16 竖版中文线稿长图。

适合：竖版教程长图、SOP、规则卡、项目复盘、AI 工作流、多步骤方法论、知识海报、手机端阅读长图。尤其适合“犯错 → 修复 → 追因 → 写入规则”“输入 → 判断 → 输出 → 复用”等可拆成 4-6 个模块的内容。

不适合：纯情绪海报、真实产品广告、单一大字概念海报、复杂数据图表、写实场景插画。它的强项是“多步骤讲清楚”，不是单一氛围图。

核心：竖版 9:16，白色或暖白纸张背景，粗黑中文标题，黑白线稿人物，2x2 或纵向多面板，圆角信息卡片，编号黑点，箭头连接，底部总结区。浅黄色、淡紫色、浅橙或浅绿色只用于强调块、提示框和状态标记。

视觉规则：人物是极简黑白线稿和几何扁平比例，表情简单但动作明确；常用道具包括代码窗口、文件夹、便签、规则卡、放大镜、清单、箭头、状态标记。文字允许比普通配图更多，但必须短句化、分区清楚、手机端可读，避免密集小字和 PPT 模板感。

结构化字段建议：主题、主标题、副标题、核心流程、模块1、模块2、模块3、模块4、必要注释、人物动作、强调色、底部总结、画幅。


## 49. scribble_furball_character_family｜毛球角色家族风

一句话描述：以乱线团萌物为核心 IP，用大眼睛、简洁动作与单色点缀，把情绪、知识、观点和场景转化为可爱而有传播力的角色视觉。

适合：情绪状态、教育知识卡、办公表达、品牌吉祥物、角色设定板、表情状态合集、双角色互动和社媒传播图。

不适合：写实人物、复杂数据图表、高端产品摄影、多色复杂背景、严肃财经报告。它的强项是角色化转译与情绪共鸣，不是写实还原。

核心：严格锁定同一 IP。身体由中等数量、粗细均匀的黑色长线与大小环线自然交叉，中心略密、外缘较松，白底明显透出，外围保留数根逸出大弧线；两只紧贴且略有高低差的巨大纵向椭圆白眼直接嵌在线团中；四肢为黑色单线、极简黑手和扁平小黑脚；每个角色固定佩戴横向包身、右侧垂尾的明黄色流苏围巾。

配色与版式：白色、米白或极浅暖色背景，黑白为骨架，只使用 1 种高明度点缀色，最多 2 种。颜色集中在围巾、帽子、眼镜、灯泡、便签、书本和小图标；留白舒适，避免复杂场景与满版纹理。

视觉规则：情绪必须一眼可读；同一角色的状态变体只能改变瞳孔朝向、嘴型、动作与道具，不能改变线团结构、眼睛比例、四肢画法和黄色围巾。线条自然略抖，既不能过度稀疏光滑成钢丝球，也不能密集涂黑成煤球。不要眼镜式眼框、缺少围巾、不同物种家族、3D、写实、贴纸套壳、额外颜色或暗黑压抑气质。

结构化字段建议：主题、角色性格或职业、核心情绪、主动作、互动关系、道具、点缀色、标题、短句、画幅。
