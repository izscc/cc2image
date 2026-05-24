# 可选风格库

默认风格是 `handdrawn_knowledge_card`（手绘知识卡片风）。只有用户明确指定其他风格，或主题非常明显适配时，才自动切换。正文解释图仍优先使用手绘知识卡片风；多数非知识卡片风更适合封面图、头图、海报或系列主视觉。

## 风格选择表

```json
{
  "styles": [
    {"style_id": "handdrawn_knowledge_card", "style_name": "手绘知识卡片风", "best_for": ["正文配图", "知识图解", "方法论解释", "流程图", "对比图"]},
    {"style_id": "oriental_editorial_illustration", "style_name": "东方典籍杂志插画风", "best_for": ["封面图", "文化主题", "历史人文", "哲学主题", "高级文章头图"]},
    {"style_id": "study_note_card", "style_name": "学习笔记卡片风", "best_for": ["学习方法", "笔记整理", "步骤教程", "知识清单", "小红书知识卡片"]},
    {"style_id": "pastel_learning_pyramid", "style_name": "彩色手绘学习金字塔风", "best_for": ["分层模型", "学习金字塔", "能力进阶", "成长路径", "主动被动对比"]},
    {"style_id": "childlike_cultural_infographic", "style_name": "儿童手绘文化科普风", "best_for": ["传统文化科普", "儿童教育", "器物拆解", "历史小知识", "博物馆内容"]},
    {"style_id": "frosted_glass_editorial", "style_name": "透明磨砂感人物海报风", "best_for": ["极简封面", "心理情绪主题", "孤独感", "音乐艺术主题", "高级品牌海报"]},
    {"style_id": "translucent_object_editorial", "style_name": "透明材质物件海报风", "best_for": ["设计主题", "品牌设计", "作品集封面", "营销主题", "工具系统封面"]},
    {"style_id": "glassmorphism_gradient_blob", "style_name": "玻璃拟态渐变气泡风", "best_for": ["品牌视觉", "创意展览", "趋势报告", "AI主题", "未来感封面"]},
    {"style_id": "embossed_typography_poster", "style_name": "浮雕纸雕字体海报风", "best_for": ["极简封面", "品牌口号", "深度思考", "书封设计", "认知策略主题"]},
    {"style_id": "acrylic_dimensional_type", "style_name": "亚克力立体字母风", "best_for": ["品牌关键词", "栏目标题", "创意概念", "年轻化封面", "视觉实验"]},
    {"style_id": "dark_neon_search_ui", "style_name": "暗黑霓虹搜索界面风", "best_for": ["AI搜索", "知识探索", "信息检索", "灵感发现", "AI工具封面"]},
    {"style_id": "black_void_glowing_hands", "style_name": "黑场发光肢体概念风", "best_for": ["心理主题", "情绪主题", "关系连接", "孤独感", "艺术海报"]},
    {"style_id": "soft_neumorphism_ui", "style_name": "柔光新拟态界面风", "best_for": ["产品功能封面", "AI工具界面", "智能家居", "效率工具", "交互设计"]},
    {"style_id": "minimal_line_shadow_brand", "style_name": "极简线性光影品牌风", "best_for": ["新品发布", "品牌封面", "科技产品", "数字主题", "产品发布会"]},
    {"style_id": "white_mono_texture_editorial", "style_name": "白色单色肌理编辑风", "best_for": ["深度文章封面", "设计作品集", "哲学主题", "个人品牌", "高级博客头图"]},
    {"style_id": "minimal_architecture_portfolio", "style_name": "极简建筑作品集线稿风", "best_for": ["作品集封面", "人生路径", "职业路径", "空间叙事", "设计策略主题"]}
  ]
}
```

## 默认匹配规则

1. 正文配图、方法论解释、流程、对比、知识系统：默认 `handdrawn_knowledge_card`。
2. 文化、历史、人文、哲学、东方智慧、古籍、文明：优先 `oriental_editorial_illustration`。
3. 学习方法、笔记整理、复习、考试、效率技巧：优先 `study_note_card`。
4. 学习金字塔、层级模型、能力进阶、成长路径、主动学习 / 被动学习：优先 `pastel_learning_pyramid`。
5. 儿童教育、传统文化科普、器物拆解、博物馆内容：优先 `childlike_cultural_infographic`。
6. 孤独、情绪、心理、音乐、艺术展、安静、疏离：优先 `frosted_glass_editorial` 或 `black_void_glowing_hands`。
7. 设计、作品集、品牌、营销、工具、系统、工作室案例：优先 `translucent_object_editorial`。
8. AI、未来感、趋势、创意展览、抽象概念、品牌视觉：优先 `glassmorphism_gradient_blob`。
9. 深度思考、认知、策略、极简口号、书封、品牌宣言：优先 `embossed_typography_poster` 或 `white_mono_texture_editorial`。
10. 单个关键词、栏目名、品牌词、年轻化视觉实验：优先 `acrylic_dimensional_type`。
11. AI 搜索、探索、信息检索、发现、推荐、知识寻找：优先 `dark_neon_search_ui`。
12. 产品界面、搜索框、控制器、智能家居、效率工具、轻科技：优先 `soft_neumorphism_ui`。
13. 新品发布、数字主题、品牌发布会、极简科技主视觉：优先 `minimal_line_shadow_brand`。
14. 作品集、建筑、路径规划、职业路线、人生路径、空间叙事：优先 `minimal_architecture_portfolio`。
15. 若用户说“封面用 A，正文用 B”，封面和正文分别套用对应风格。

## 风格定位速查

- `frosted_glass_editorial`：人物/物体隔着磨砂玻璃，情绪、疏离、艺术感。
- `translucent_object_editorial`：透明文件夹、亚克力物件、设计工作室封面。
- `glassmorphism_gradient_blob`：彩色液态玻璃 blob，未来感品牌视觉。
- `soft_neumorphism_ui`：浅色 UI 控件、软阴影、智能界面。
- `minimal_line_shadow_brand`：细线数字/符号、品牌发布、极简科技。
- `white_mono_texture_editorial`：白色刷痕、纸张肌理、编辑网页、深度文章。
- `embossed_typography_poster`：文字本身浮雕/压痕/纸雕，是字体实验。
- `minimal_architecture_portfolio`：细线、虚线、人物剪影、路径、作品集封面。

## 1. handdrawn_knowledge_card｜手绘知识卡片风

整体风格像高质量中文知识博主的手绘知识图解系统：暖白纸感背景，黑灰细线手绘，低饱和浅色块，中文手写字，自然成熟，克制精致，留白充足，轻商业内容资产感。不要做成 PPT，不要课程课件，不要科技海报，不要 3D，不要可爱儿童插画，不要复杂信息图，不要密集小字，不要高饱和颜色，不要英文乱码，不要水印。

## 2. oriental_editorial_illustration｜东方典籍杂志插画风

适合文化、人文、历史、哲学类封面。以暖白宣纸、蓝金配色、巨大古籍/卷轴/山河隐喻、微缩人物和诗意留白为核心，像高端文化杂志或图书封面。

## 3. study_note_card｜学习笔记卡片风

米白纸张背景，中间是一张笔记纸卡片，周围有胶带、回形针、便签、贴纸等学习手账元素。适合学习方法、笔记整理、知识清单、步骤教程。

## 4. pastel_learning_pyramid｜彩色手绘学习金字塔风

纸张纹理背景，主体是柔和粉彩笔刷绘制的分层金字塔、阶梯或漏斗。适合层级模型、学习金字塔、能力进阶、成长路径。

## 5. childlike_cultural_infographic｜儿童手绘文化科普风

白色纸张背景，黑色手绘边框，水彩手绘插画，虚线箭头、标签说明和气泡旁白。适合传统文化科普、儿童教育、器物拆解。

## 6. frosted_glass_editorial｜透明磨砂感人物海报风

纯粹情绪主视觉。主体像隔着一层半透明磨砂玻璃被观看，模糊轮廓、低对比背景、大量留白，适合孤独、情绪、心理、音乐、艺术展。

## 7. translucent_object_editorial｜透明材质物件海报风

半透明玻璃、磨砂塑料、亚克力、柔软充气材质构成抽象物件，像高端设计工作室作品集或设计展海报。

## 8. glassmorphism_gradient_blob｜玻璃拟态渐变气泡风

半透明液态玻璃 blob，柔和橙粉蓝青渐变光晕，文字和玻璃前后穿插。适合 AI、趋势、未来感、品牌视觉。

## 9. embossed_typography_poster｜浮雕纸雕字体海报风

文字本身作为主视觉，使用纸张浮雕、凹刻、压痕、挖空和柔和阴影，像艺术书封或品牌口号页。

## 10. acrylic_dimensional_type｜亚克力立体字母风

标题文字变成真实可触摸的 3D 字母物件，透明亚克力、半透明彩色塑料、线框金属、磨砂玻璃或纸质。

## 11. dark_neon_search_ui｜暗黑霓虹搜索界面风

纯黑深空背景，彩色颗粒霓虹光带，半透明磨砂搜索框，极简小角色。适合 AI 搜索、知识探索、信息检索、发现推荐。

模板：请生成一张暗黑霓虹搜索界面风的中文封面图。主题是「{主题}」。画面使用纯黑或深黑背景，整体像 AI 搜索产品、探索工具或未来感网页启动页。背景中有彩色霓虹光带或光环，前景有半透明磨砂搜索框，搜索框里写「{标题或关键词}」。可加入极简白色小角色。整体神秘、现代、轻未来感，不要复杂赛博朋克，不要密集 UI，不要游戏界面。

## 12. black_void_glowing_hands｜黑场发光肢体概念风

纯黑背景，大量留黑，几只手、手臂或身体局部从黑暗中浮现，边缘有柔和白色轮廓光。适合触达、连接、孤独、关系、心理、沉默、求助。

模板：请生成一张黑场发光肢体概念风的中文封面图。主题是「{主题}」。画面使用纯黑背景，大量留黑。几只手或手臂从不同方向伸入黑暗，手势表达「{核心情绪或动作}」。标题使用极简现代字体。不要恐怖片，不要血腥，不要写实惊悚。

## 13. soft_neumorphism_ui｜柔光新拟态界面风

浅灰白、淡蓝灰或雾白背景，UI 控件像从背景中柔和凸起或凹陷，带软阴影、内阴影和柔和环境光。适合产品功能封面、AI 工具界面、智能家居、效率工具。

模板：请生成一张柔光新拟态界面风的中文封面图。主题是「{主题}」。画面中心放置一个新拟态 UI 主控件，例如搜索框、圆形旋钮、温度环、滑杆、卡片或控制面板。控件中显示少量文字或数字：「{标题或关键词}」。整体浅色、柔和、轻科技。

## 14. minimal_line_shadow_brand｜极简线性光影品牌风

浅灰白背景，大量留白，主体由极细黑灰线条构成巨大数字、符号、字母或几何形，并带半透明长阴影和微弱光点。适合新品发布、品牌封面、科技产品、数字主题。

模板：请生成一张极简线性光影品牌风的中文封面图。主题是「{主题}」。中心放置由极细黑灰线条构成的巨大符号、数字、字母或几何形，核心隐喻是「{核心隐喻}」。排版极简，像高端科技品牌发布会。

## 15. white_mono_texture_editorial｜白色单色肌理编辑风

几乎只使用白色、浅灰和黑色，主体是白色材质痕迹，如厚涂刷痕、纸张折痕、压痕、浮起边缘、光影切面。适合深度文章封面、设计作品集、哲学主题、个人品牌、高级博客头图。

模板：请生成一张白色单色肌理编辑风的中文封面图。主题是「{主题}」。主体是一道白色材质痕迹，核心隐喻是「{核心隐喻}」。标题使用克制字体，放在留白区域。整体安静、冷静、有深度。

## 16. minimal_architecture_portfolio｜极简建筑作品集线稿风

白色或浅灰纸张背景，大量留白，极细黑线、水平基准线、虚线路径、微型人物剪影和少量文字排版。适合作品集封面、人生路径、职业路径、空间叙事、设计策略主题。

模板：请生成一张极简建筑作品集线稿风的中文封面图。主题是「{主题}」。画面中使用极细黑色线条绘制水平基准线、虚线路径和空间关系。加入几个微型黑色人物剪影，表达「{核心隐喻}」。整体像建筑设计 portfolio 封面。
