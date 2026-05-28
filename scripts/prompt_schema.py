#!/usr/bin/env python3
"""Prompt helpers for zscc配图生成器.

Validate image plan JSON and render stable prompts for multiple styles.
This script does not call image generation APIs; Codex should use the rendered
prompts with the available image generation tool when requested.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any, Dict, List

DEFAULT_STYLE_ID = "handdrawn_knowledge_card"

STYLE_ANCHORS: Dict[str, str] = {
    "handdrawn_knowledge_card": (
        "整体风格像高质量中文知识博主的手绘知识图解系统：暖白纸感背景，黑灰细线手绘，"
        "低饱和浅色块，中文手写字，自然成熟，克制精致，留白充足，轻商业内容资产感。"
        "不要做成 PPT，不要课程课件，不要科技海报，不要 3D，不要可爱儿童插画，"
        "不要复杂信息图，不要密集小字，不要高饱和颜色，不要英文乱码，不要水印。"
    ),
    "oriental_editorial_illustration": (
        "整体风格为典籍山水风：暖白宣纸质感背景，低饱和蓝金配色，石青、金色、米白、墨灰为主，"
        "画面像高端文化杂志或图书封面。主体使用巨大文化隐喻物，例如打开的古籍、卷轴、山河、地图、书页、河流。"
        "加入少量微缩人物，人物像行走在典籍和山水之间。整体诗意、克制、留白充足，有历史感、文化感、东方美学和高级出版物质感。"
        "不要做成 PPT，不要科技风，不要可爱卡通，不要二次元，不要游戏概念图，不要 3D，不要高饱和颜色，不要拥挤。\n"
        "Oriental editorial illustration style, premium cultural magazine cover, New Chinese aesthetic, warm ivory paper texture, muted blue and gold palette, "
        "stone blue, ochre gold, rice white, ink gray, poetic negative space, monumental cultural metaphor object, open ancient book, scroll, mountains, rivers, "
        "map-like landscape, tiny wandering figures in minimal traditional robes, subtle calligraphy fragments, literary, historical, elegant, calm, refined, "
        "high-end publishing design, not anime, not cartoon, not cyberpunk, not 3D, not PPT infographic, not crowded."
    ),
    "study_note_card": (
        "整体风格为学习笔记风：米白纸张背景，中间是一张带轻微阴影的笔记纸卡片，周围有胶带、回形针、便签、贴纸等学习手账元素。"
        "使用低饱和浅紫、浅黄、奶油白、深绿色配色。标题醒目，正文分区清晰，搭配少量手绘学习图标和简笔插画。"
        "整体像精心整理的学习笔记、小红书知识卡片或高质量学习手账，不要做成商务 PPT，不要科技风，不要复杂海报，不要高饱和颜色，不要过度装饰。"
    ),
    "pastel_learning_pyramid": (
        "整体风格为粉彩金字塔风：白色或米白纸张纹理背景，主体是柔和粉彩笔刷绘制的分层金字塔、阶梯或漏斗。"
        "每层使用低饱和粉色、橙色、黄色、薄荷绿、浅蓝、浅紫等色块。文字像手写笔记，搭配虚线、箭头、百分比、小标签。"
        "整体轻松、清楚、学习感强，像手绘学习方法海报。不要做成商务图表，不要 3D 金字塔，不要科技风，不要高饱和颜色，不要复杂背景。"
    ),
    "childlike_cultural_infographic": (
        "整体风格为童趣科普风：白色纸张背景，黑色手绘边框，水彩手绘插画，线条自然、有童趣。"
        "画面包含多个文化物件、可爱人物、虚线箭头、标签说明和气泡旁白。配色温和，像少儿文化科普海报、儿童绘本知识页或课堂小报。"
        "文字清楚但不要过密，整体活泼、有趣、易懂。不要做成写实插画，不要商业海报，不要科技风，不要 3D，不要高级冷淡风。"
    ),
    "frosted_glass_editorial": (
        "整体风格为磨砂情绪风：画面像隔着一层半透明磨砂玻璃观看人物、身体局部或情绪化物体，主体轮廓被柔和模糊，只露出局部阴影、形状和深色轮廓。"
        "背景为低饱和冷灰、灰绿、雾白或浅蓝色，大量留白，构图极简。文字采用现代极简排版，可以用少量亮黄色或黑色作为强调。"
        "整体像艺术节、音乐节、设计展或高级品牌海报，安静、神秘、克制、疏离。不要做成信息图，不要手绘卡通，不要 3D 科技风，不要复杂背景，不要高饱和色，不要密集文字。\n"
        "Frosted glass editorial poster style, translucent frosted glass surface, blurred human silhouette or emotional object behind glass, soft diffusion, low contrast, "
        "muted pale green gray background, minimal composition, large negative space, modern Swiss editorial typography, small bright yellow accent text, quiet, mysterious, "
        "restrained, premium art festival poster, not infographic, not cartoon, not 3D, not cyberpunk, not crowded."
    ),
    "translucent_object_editorial": (
        "整体风格为透明物件风：低饱和米灰、浅灰绿或雾白背景，大量留白，中心放置一个由半透明玻璃、磨砂塑料、亚克力或柔软充气材质构成的抽象物件。"
        "物件内部可以有被磨砂遮挡的柔和彩色块，边缘有细腻高光、折射、阴影和真实材质感。文字使用现代无衬线排版，克制、干净、像高端设计工作室作品集或设计展海报。"
        "不要做成 PPT，不要手绘卡通，不要科技赛博，不要复杂背景，不要高饱和颜色，不要密集文字。"
    ),
    "glassmorphism_gradient_blob": (
        "整体风格为玻璃气泡风：浅灰白背景，主体是半透明液态玻璃 blob，有柔和的橙色、粉色、蓝色、青色渐变光晕，边缘有折射、高光和柔和阴影。"
        "文字与玻璃形体形成前后穿插，部分文字被磨砂玻璃模糊遮挡，部分文字清晰浮在前景。整体现代、轻盈、未来感、设计感强，但不要赛博朋克，不要霓虹，不要复杂 3D 场景，不要信息图。"
    ),
    "embossed_typography_poster": (
        "整体风格为纸雕字体风：文字本身作为主视觉，使用同色系纸张浮雕、凹刻、压痕、挖空和柔和阴影来呈现立体感。"
        "背景是白色、浅灰、米色或牛皮纸质感，整体接近单色，极简、大量留白、安静、高级，像艺术书封、设计海报或品牌口号页。"
        "不要复杂插画，不要彩色大图，不要科技风，不要卡通，不要信息图。"
    ),
    "acrylic_dimensional_type": (
        "整体风格为亚克力字风：标题文字被设计成真实可触摸的 3D 字母物件，材质包括透明亚克力、半透明彩色塑料、线框金属、磨砂玻璃或纸质。"
        "背景为干净白色或浅灰摄影棚，光线柔和，字母投下自然阴影。整体年轻、现代、轻盈、有品牌设计感。"
        "不要做成普通平面文字，不要信息图，不要复杂场景，不要卡通，不要过度科技风。"
    ),
    "dark_neon_search_ui": (
        "整体风格为霓虹搜索风：纯黑深空背景，彩色霓虹光带或光环在画面中穿梭，带有细腻颗粒噪点和柔和辉光。"
        "前景是一个半透明磨砂质感的搜索框、输入框或胶囊按钮，文字极少，像 AI 搜索产品的启动界面。"
        "可以加入一个极简白色小角色或小动物，增强探索感。整体神秘、现代、轻未来感、数字产品感。"
        "不要做成复杂赛博朋克，不要密集 UI，不要游戏界面，不要过多文字，不要卡通幼稚。"
    ),
    "black_void_glowing_hands": (
        "整体风格为黑场肢体风：纯黑背景，大量留黑，画面中只有几只手、手臂或身体局部从黑暗中浮现，边缘有柔和白色轮廓光，主体部分渐隐到黑暗里。"
        "构图极简但有强烈心理隐喻，表达触达、连接、孤独、寻找、求助、关系张力。文字极少，像艺术展海报或心理主题封面。"
        "不要做成恐怖片海报，不要血腥，不要写实惊悚，不要复杂背景，不要霓虹赛博。"
    ),
    "soft_neumorphism_ui": (
        "整体风格为柔光界面风：浅灰白、淡蓝灰或雾白背景，UI 控件像从背景中柔和凸起或凹陷，带有细腻软阴影、内阴影和环境光。"
        "主体可以是搜索框、圆形控制器、滑杆、卡片或数字面板。可以加入少量暖橙、浅蓝、浅绿光晕作为反馈状态。"
        "整体干净、轻科技、柔和、安静，像高端智能产品界面或交互设计海报。不要做成传统扁平 UI，不要重色阴影，不要霓虹赛博，不要复杂仪表盘，不要密集文字。"
    ),
    "minimal_line_shadow_brand": (
        "整体风格为线性品牌风：浅灰白或淡蓝灰背景，大量留白，主体由极细黑灰线条构成一个巨大的数字、符号、字母或几何形。"
        "主体带有半透明长阴影、轻微折射和淡淡彩色光点。排版极简，像高端科技品牌发布会、手机新品海报或设计品牌主视觉。"
        "不要复杂 3D，不要霓虹赛博，不要卡通，不要信息图，不要密集文字。"
    ),
    "white_mono_texture_editorial": (
        "整体风格为白色肌理风：画面几乎只使用白色、浅灰和黑色，主体是白色材质痕迹，例如厚涂刷痕、纸张折痕、压痕、浮起边缘、光影切面或微妙纹理。"
        "大量留白，文字排版像高端编辑网页、艺术书页或设计作品集封面。整体安静、克制、深思感强。"
        "不要彩色插画，不要复杂图形，不要信息图，不要手绘卡通，不要高饱和颜色。"
    ),
    "minimal_architecture_portfolio": (
        "整体风格为建筑线稿风：白色或浅灰纸张背景，大量留白，使用极细黑色线条、水平基准线、虚线路径、微型人物剪影和少量文字排版。"
        "画面像建筑设计作品集封面、空间叙事图或设计学院 portfolio。整体冷静、克制、理性，有路径感和空间感。"
        "不要彩色插画，不要 3D 建筑渲染，不要复杂图表，不要卡通，不要高饱和颜色。"
    ),
    "minimal_healing_metaphor_comic": (
        "整体风格为极简治愈隐喻漫画风：暖白纸张纹理背景，大量留白，黑色手绘线条，线条自然略带抖动。"
        "画面中有一个小小的圆脸小孩，黑色短发，穿黄色连帽衫或黄色上衣，黑色短裤，白色小鞋，脸颊有浅粉色腮红。"
        "用极少的道具表达情绪隐喻，例如花、浇水壶、充电线、爱心、磁铁、云朵、太阳、旗子、文字雨。"
        "配色极简，只使用黑白、黄色、少量红色和浅粉。画面安静、温柔、治愈、像成人内在小孩漫画或极简情绪绘本。"
        "不要复杂背景，不要精致商业插画，不要 3D，不要赛博朋克，不要高饱和颜色，不要密集文字，不要写实人物。\n"
        "Minimal healing metaphor comic style, warm off-white paper texture background, lots of negative space, simple black hand-drawn line art, slightly wobbly ink lines, "
        "a tiny round-faced child with messy black hair wearing a yellow hoodie or yellow shirt, black shorts, white shoes, soft pink cheeks, quiet tender expression, "
        "simple symbolic props such as a flower, watering can, charging cable, plug, heart, magnet, cloud, sun, flag, rain of words, emotional metaphor, inner child illustration, "
        "gentle, warm, comforting, poetic, minimal colors, black white yellow with tiny red accents, not realistic, not 3D, not complex, not colorful, not commercial illustration."
    ),
    "retro_minimal_poster_illustration": (
        "整体风格为复古海报风：米白旧纸背景，轻微复古纸张纹理，大面积纯色块构成主体，常用钴蓝、芥末黄、米白、少量黑色。"
        "人物和物件高度几何化、简化，像中世纪现代海报、复古书封、丝网印刷或版画插画。构图简洁，留白充足，字体克制优雅。"
        "不要写实，不要复杂插画，不要 3D，不要高饱和霓虹色，不要信息图。"
    ),
    "editorial_balloon_collage": (
        "整体风格为气球拼贴风：白色纸张背景，大量留白，主体由几个半透明彩色圆片组成，像气球、光片或抽象希望符号。"
        "圆片颜色可以是粉色、橙色、黄色、深蓝、紫色，带透明叠加和投影。下方加入灰黑色细线素描人物、购物车、篮子、船、平台等叙事元素，用细线连接到圆片。"
        "文字采用粗体黑色编辑排版，像高质量品牌广告或企业文化海报。不要儿童卡通，不要 PPT，不要复杂信息图，不要高饱和廉价配色。"
    ),
    "transparent_architectural_type": (
        "整体风格为透明字境风：浅灰或雾白背景，画面中心是一个巨大的数字、字母或汉字，像透明玻璃、水晶或亚克力建筑。"
        "字体内部有云雾、天空、山体、光线、微型人物或空间场景，边缘有清晰的玻璃折射和细白线轮廓。整体超现实、安静、宏大、有建筑空间感和高级封面质感。"
        "不要普通 3D 字体，不要霓虹赛博，不要卡通，不要复杂信息图。"
    ),
    "paper_cut_profile_silhouette": (
        "整体风格为纸雕剪影风：白色或浅色纸张背景，主体是一个单色纸雕剪影，通常是人物侧脸、头像、动物或象征物。"
        "剪影内部嵌入行业相关元素，例如桥梁、城市、工具、设备、书本、树木、道路或系统结构。剪影有纸张厚度、切割边缘和真实投影。"
        "配色克制，可以使用红色、深蓝、黑色或单色。不要卡通，不要复杂插画，不要 3D 渲染感过强，不要高饱和多色。"
    ),
    "torn_paper_note_minimal": (
        "整体风格为撕纸便签风：大面积米色或暖灰纸张背景，中心或偏下放一小片白色撕裂纸条，边缘不规则，有真实纸张纤维和柔和投影。"
        "纸条上只写一个词或一句非常短的话。构图极简、大量留白、安静、私密，像信念便签、心理提醒卡或每日一句。"
        "不要复杂插画，不要多色装饰，不要商业海报，不要信息图。"
    ),
    "fluffy_soft_typography": (
        "整体风格为毛绒字体风：文字本身是主视觉，字体由柔软的毛绒、毛巾布、羊羔绒、绒线或蓬松纤维构成，边缘有细密绒毛，触感柔软。"
        "背景为白色、奶油色或浅灰色，光线柔和，文字投下自然阴影。可以加入小星星、笑脸、暖光或少量可爱符号。整体温暖、治愈、可爱、轻松。"
        "不要硬质 3D 金属字，不要科技风，不要复杂背景，不要高饱和杂乱配色。"
    ),
    "cloud_typography_cover": (
        "整体风格为云朵字体风：蓝天或青蓝渐变天空背景，标题文字由真实蓬松的白云组成，云朵边缘柔软、自然、立体，有阳光照射和云影。"
        "画面开阔、明亮、向上，带有希望、成长、疗愈和新开始的感觉。可以加入少量小云、阳光、远处山影或天空层次。"
        "不要卡通云，不要儿童贴纸风，不要复杂信息图，不要霓虹色，不要厚重黑暗风。"
    ),
    "foam_bubble_typography": (
        "整体风格为泡沫字体风：蓝色湿润瓷砖或浴室墙面背景，表面有水滴、泡泡、凝结水珠和高光反射。标题文字一部分是醒目的扁平粗体字，一部分是由白色清洁泡沫、海绵或肥皂泡组成的立体字，边缘有泡孔和湿润质感。整体清爽、有能量、广告海报感强，适合表达焕新、清洁、重启、梦想变大。不要普通 3D 字，不要卡通，不要复杂场景，不要暗黑风。"
    ),
    "embroidered_patch_brand": (
        "整体风格为刺绣徽章风：背景是柔软织物、帆布、棉布或牛仔布，主体由皮革贴片、刺绣布标、缝线和补丁组成。标题或标志像缝在布料上的徽章，有真实皮革纹理、针脚、边缘包边、轻微阴影和手工质感。颜色可使用复古红、黄、蓝、绿和米白。整体像学院风徽章、品牌补丁、服饰标签或设计师工具包封面。不要普通平面 logo，不要光滑塑料感，不要科技风，不要复杂背景。"
    ),
    "luxury_gold_typography": (
        "整体风格为金属奢华风：浅米色、象牙白或暖灰背景，标题使用金色、香槟金或银色立体 serif 字体，具有金属反射、高光、斜面、柔和投影和高级光泽。画面排版克制，加入少量细线图标、装饰线和小号说明文字。整体像高端品牌、节日庆典、颁奖活动或奢华餐饮海报。不要廉价黄金字，不要过度装饰，不要花哨背景，不要卡通，不要信息图。"
    ),
    "miniature_map_life_scene": (
        "整体风格为微缩地图风：背景是浅色地图、城市平面图、地铁路线图或世界地图，带柔和景深和轻微模糊。画面中放置几个微缩人物，像小模型一样站在不同地点，形成过去的自己与现在的自己之间的对话。主标题和文案像印在地图上的路标、坐标或路线说明。配色柔和，常用浅蓝、淡绿、米白、灰蓝。不要真实地图截图，不要复杂信息图，不要卡通，不要高饱和颜色。"
    ),
    "miniature_checklist_scene": (
        "整体风格为微缩清单风：背景是一张巨大清单、计划表、任务表或笔记纸，上面有复选框、表格线、打勾符号和淡化文字。几个微缩人物像小模型一样在纸面上工作、打勾、画线、搬运目标或完成任务。画面采用斜俯视角，景深柔和，配色为米色、浅灰、淡黄和深灰文字。整体像执行力、项目管理或习惯养成主题的温柔广告海报。不要普通流程图，不要 PPT，不要复杂信息图，不要卡通。"
    ),
    "fabric_micro_scene_ad": (
        "整体风格为布料微缩风：背景是真实织物、衬衫、布料、皮革或服装局部，能看到纤维纹理、纽扣、缝线和褶皱。主题文字或数字像刺绣、织纹、印花或补丁一样出现在布料上。几个微缩人物像模型工人一样在文字周围工作、缝制、绘制、修补或协作。画面有真实摄影感、浅景深和品牌广告质感，适合表达匠心、劳动、细节和工艺。不要卡通，不要普通平面海报，不要复杂信息图。"
    ),
    "giant_letter_lifestyle_scene": (
        "整体风格为巨字生活风：纯色摄影棚背景，通常是深蓝、浅蓝、白色或品牌色；画面中心是巨大的立体白色字母或中文文字结构，每个字母像一个可进入的小空间。人物在字母中学习、开会、阅读、陪伴、休息或互动，形成温暖的生活场景。光线柔和，阴影真实，排版极简，像高端品牌广告或系列视觉海报。不要普通 3D 字，不要卡通，不要复杂背景，不要信息图。"
    ),
    "oriental_floral_minimal_editorial": (
        "整体风格为花艺留白风：浅色纸张或墙面肌理背景，大面积留白，画面中使用红色花瓣、花枝、圆月、水面倒影、小鸟、女性侧脸或优雅剪影作为核心意象。色彩克制，以象牙白、浅青、灰绿、墨色、红色和淡粉为主。构图安静、诗意、精致，有东方美学、文学杂志和高端花艺海报质感。不要浓艳国潮，不要复杂插画，不要卡通，不要科技风，不要高饱和颜色，不要密集文字。"
    ),
    "zen_ink_philosophy_poster": (
        "整体风格为禅意水墨风：米白宣纸质感背景，大面积留白，黑色水墨笔触作为主体，搭配一个红色或粉色圆日。画面中可以有极小的人物剪影、行者、武士、僧人、松树、山石、路径或远山。构图极简，文字像哲学格言或书页排版，可以中英混排，少量红色印章点缀。整体安静、克制、东方、内省、有修行感。不要浓艳国潮，不要复杂山水，不要卡通，不要写实摄影，不要高饱和颜色，不要密集文字。"
    ),
    "editorial_line_character": (
        '整体风格为编辑线稿风：现代编辑设计语言，黑白极简线稿人物，干净扁平几何比例，简单脸部，风格化身体。画面把主题转译成日常城市生活场景，例如通勤、手机使用、阅读、购物、自拍、行走、休息、听音乐、工作和多任务处理。使用杂志式大标题、非对称排版层级、大量留白和强版面块。人物主体保持黑白单色，柔和色块只用于背景、包装、UI 面板、产品标签和分区块。点缀色可用柔黄、低饱和紫、暖橙、低饱和粉和奶油白。整体像品牌视觉系统、杂志插画、网站首屏、包装或多面板 campaign board。不要写实光影，不要 3D，不要光泽渲染，不要厚重渐变，不要动漫，不要儿童吉祥物，不要过度彩色，不要杂乱背景。\nModern editorial illustration system, minimalist black-and-white line art characters, clean flat geometric proportions, simple faces, stylized bodies, everyday urban lifestyle scenes, bold magazine typography, asymmetrical editorial hierarchy, large negative space, strong layout blocks, selective pastel accents, flat vector-like finish, no realistic lighting, no 3D, no glossy rendering, no anime, no childish mascot, no busy background.'
    ),
    "editorial_object_annotation_card": (
        '整体风格为具象标注风：纯白或暖白背景，大量留白，左侧是大号现代无衬线标题、副标题和三条原则列表，右侧是一个高清真实具象物品作为核心隐喻。物品可以是植物、叶子、花、石头、钥匙、镜子、指南针、绳子、书、杯子、灯泡、地图等，不局限于植物。物品具有真实摄影质感、自然阴影、细腻纹理和局部细节，像被放在白纸上的研究对象。画面周围加入虚线箭头、小圆点定位、括号、波浪下划线、手写注释、手绘星星、小爱心和下划线等标注系统，并加入一个极简手绘小人作为观察者或操作者。整体像高级编辑知识卡片、设计方法论页或 AI playbook 页面。不要做成 PPT，不要复杂信息图，不要卡通海报，不要 3D 科技风，不要高饱和颜色，不要密集文字。\nEditorial object annotation card style, clean white background, lots of negative space, bold modern sans-serif headline, subtitle and three numbered principles on the left, one high-resolution realistic object as the central metaphor on the right, not limited to plants, can be leaf, flower, stone, key, mirror, compass, rope, book, cup, light bulb, map. Real photographic texture, natural shadow, fine details. Add dotted arrows, small annotation labels, hand-drawn stars, hearts, underlines, tiny sketch character observing or interacting with the object. Premium design playbook page, AI methodology card, editorial learning card, not PPT, not dense infographic, not cartoon poster, not cyberpunk, not cluttered.'
    ),
    "crowd_typography_scene": (
        '整体风格为人群造字风：白色或浅灰色巨大地面空间，高空俯视视角，大量真实微缩小人按照主题排列成一个有意义的巨大文字、数字、符号、图表或隐喻图形。小人有真实服装颜色和自然长阴影，部分人物成群，部分人物零散分布，形成社会观察感。文字排版像印在地面上，主标题使用粗黑中文字体，副标题较小，顶部可加入杂志栏目、目录、页码和灰色刊名，整体像财经杂志、深度报道或社会议题封面。不要做成卡通小人，不要普通信息图，不要拥挤杂乱，不要 3D 游戏场景，不要高饱和背景。\nCrowd typography editorial cover style, high-angle aerial view, vast white or light gray ground plane, hundreds of realistic tiny people arranged into a meaningful giant Chinese character, number, symbol, chart, path, arrow, question mark, or abstract diagram. Realistic clothing colors, long natural shadows, some scattered individuals around the main formation. Typography looks printed on the ground, bold black editorial headline, smaller subtitle, magazine cover layout with issue lines and page numbers, serious business and social issue magazine aesthetic, not cartoon, not infographic, not game scene, not crowded background.'
    ),
    "semantic_material_typography": (
        '整体风格为语义字体风：文字本身是画面主角，根据标题含义自动选择最贴合语义的真实材质、物体结构或自然纹理来构成字体。字体可以由木板、石头、苔藓、沙尘、蜂蜜、水果、金属机械、玻璃、纸张、布料、火焰、水、云朵、泥土、齿轮、线稿或混合材料构成。材质必须服务内容含义，而不是随机装饰。画面背景简洁，通常为白色、浅灰或干净摄影棚背景，保留大量留白。文字要醒目、可读、有强烈触感和真实光影。可以加入少量副标题、标签或编辑说明，但不要喧宾夺主。不要做成普通平面字，不要廉价 3D 字，不要杂乱拼贴，不要复杂信息图，不要高饱和背景。\nSemantic material typography style, the text itself is the main visual. Transform the title into a physical material or object structure that matches its meaning: wood planks, stone, moss, dust, sand, honey, fruit peel, golden paint, mechanical parts, glass, fabric, paper, metal, clouds, water, fire, soil, or mixed materials. The material must express the concept, not just decorate it. Clean white or light gray studio background, strong readability, realistic texture, tactile surface, natural shadows, premium editorial poster feel, minimal supporting text, not flat typography, not cheap 3D, not cluttered, not infographic.'
    ),
    "quirky_doodle_character_flow": (
        '整体风格为怪诞小人风：纯白或暖白背景，大量留白，黑色细线手绘，线条自然略带抖动。画面中有一个或多个怪诞小人角色，默认是黑色不规则小怪物，圆角身体，短手短脚，白色小眼睛，表情呆萌、困惑或努力。用小怪物参与流程：搬运文件、操作机器、判断、卡住、跑起来、举牌、掉进洞、从输出口出来。画面用极简图标、盒子、机器、漏斗、传送带、门、文件、工具箱、旗子、箭头、虚线来表达系统流程。配色以黑白为主，只用少量红色、蓝色和橙色做标注与箭头。整体像轻松怪诞的手绘工作流漫画、AI 系统草图、产品流程白板图。不要做成精致商业插画，不要复杂彩色卡通，不要 3D，不要拟真，不要高饱和颜色，不要密集文字。\nQuirky doodle character flow style, clean white background, lots of negative space, thin black hand-drawn lines, slightly wobbly sketch quality. Small strange black blob characters with rounded bodies, tiny arms and legs, white eyes, cute awkward expressions. Characters interact with the workflow: carrying files, operating machines, judging, getting stuck, running, holding signs, falling into holes, coming out of output doors. Use simple icons, boxes, machines, funnels, conveyor belts, doors, documents, toolboxes, flags, arrows and dotted feedback lines. Mostly black and white, with tiny red, blue and orange annotations. Looks like a playful AI workflow doodle, product system sketch, whiteboard process comic. Not polished commercial illustration, not colorful cartoon, not 3D, not realistic, not dense text.'
    ),
    "minimal_line_art": (
        '整体风格为线条艺术风：纯白或暖白背景，大量留白，用极简黑色线条表达主体。线条可以是连续一笔画，也可以是少量克制的轮廓线，线条自然流动、干净、轻盈。画面只保留最关键的人物姿态、关系动作、场景轮廓或概念符号，不画复杂细节。允许根据主题加入少量点缀色，例如浅粉爱心、黄色灯泡、浅蓝远方、红色重点或浅灰阴影。整体安静、优雅、克制、有情绪和概念感。不要复杂背景，不要厚重上色，不要写实人物，不要 3D，不要卡通夸张，不要高饱和颜色，不要密集文字。\nMinimal line art style, clean white background, lots of negative space, simple black continuous line drawing, elegant flowing outlines, minimal details, expressive posture and emotion, one-line illustration feel. Use only a tiny accent color when needed, such as pale pink heart, yellow light bulb, soft blue distance, red focus mark, or light gray shadow. Quiet, poetic, modern, minimal, conceptual. Not realistic, not 3D, not colorful cartoon, not complex background, not dense text.'
    ),
    "monochrome_system_editorial": (
        '整体风格为黑白系统风：黑白灰单色，高对比，白色或浅灰背景，巨型黑色粗体中文或英文字作为主视觉，搭配细线网格、编号、条形码、页码、REF 编号、模块分隔线和工业化信息排版。画面中使用系统隐喻物件，例如透明档案盒、索引卡、文件柜、锁、阶梯、门、路径线、路线图、货船、集装箱、柱状图、微缩人物等，表达知识封装、方法系统、SOP、路径判断、流程标准化或规模化分发。构图像高级方法论手册、SOP 封面、品牌 guideline、工业设计板或专业知识产品封面。整体冷静、专业、系统、权威、可执行。不要彩色插画，不要卡通，不要治愈风，不要复杂照片背景，不要高饱和颜色，不要杂乱排版。\nMonochrome system editorial style, black white and gray only, high contrast, clean white or light gray background, oversized bold black Chinese or English typography as the dominant visual, strict grid layout, thin technical lines, barcode, reference number, page index, module dividers, industrial information design. Use system metaphor objects such as transparent archive box, index cards, file cabinet, padlock, stairs, doorway, routing lines, path map, cargo ship, containers, bar chart, tiny human figures. Express knowledge encapsulation, SOP, prompt library, workflow standardization, decision routing, scalable distribution. Premium methodology manual cover, SOP playbook, industrial design board, professional knowledge product visual. Not colorful, not cartoon, not emotional illustration, not cluttered, not cyberpunk.'
    ),
}

STYLE_NAMES = {
    "handdrawn_knowledge_card": "手绘知识风",
    "oriental_editorial_illustration": "典籍山水风",
    "study_note_card": "学习笔记风",
    "pastel_learning_pyramid": "粉彩金字塔风",
    "childlike_cultural_infographic": "童趣科普风",
    "frosted_glass_editorial": "磨砂情绪风",
    "translucent_object_editorial": "透明物件风",
    "glassmorphism_gradient_blob": "玻璃气泡风",
    "embossed_typography_poster": "纸雕字体风",
    "acrylic_dimensional_type": "亚克力字风",
    "dark_neon_search_ui": "霓虹搜索风",
    "black_void_glowing_hands": "黑场肢体风",
    "soft_neumorphism_ui": "柔光界面风",
    "minimal_line_shadow_brand": "线性品牌风",
    "white_mono_texture_editorial": "白色肌理风",
    "minimal_architecture_portfolio": "建筑线稿风",
    "minimal_healing_metaphor_comic": "治愈漫画风",
    "retro_minimal_poster_illustration": "复古海报风",
    "editorial_balloon_collage": "气球拼贴风",
    "transparent_architectural_type": "透明字境风",
    "paper_cut_profile_silhouette": "纸雕剪影风",
    "torn_paper_note_minimal": "撕纸便签风",
    "fluffy_soft_typography": "毛绒字体风",
    "cloud_typography_cover": "云朵字体风",
    "foam_bubble_typography": "泡沫字体风",
    "embroidered_patch_brand": "刺绣徽章风",
    "luxury_gold_typography": "金属奢华风",
    "miniature_map_life_scene": "微缩地图风",
    "miniature_checklist_scene": "微缩清单风",
    "fabric_micro_scene_ad": "布料微缩风",
    "giant_letter_lifestyle_scene": "巨字生活风",
    "oriental_floral_minimal_editorial": "花艺留白风",
    "zen_ink_philosophy_poster": "禅意水墨风",
    "editorial_line_character": "编辑线稿风",
    "editorial_object_annotation_card": "具象标注风",
    "crowd_typography_scene": "人群造字风",
    "semantic_material_typography": "语义字体风",
    "quirky_doodle_character_flow": "怪诞小人风",
    "minimal_line_art": "线条艺术风",
    "monochrome_system_editorial": "黑白系统风",
}

BODY_STRUCTURES = {
    "闭环机制图",
    "横向流程图",
    "分类树图",
    "左右对比图",
    "结构类比图",
    "风险路径图",
    "光谱选择图",
    "随附场景图",
    "学习笔记卡片",
    "分层金字塔",
    "儿童文化科普图",
}


@dataclass
class CoverSpec:
    title: str
    subtitle: str
    metaphor: str
    elements: str
    character_action: str
    speech_bubble: str
    bottom_sentence: str
    principle1: str = ""
    description1: str = ""
    principle2: str = ""
    description2: str = ""
    principle3: str = ""
    description3: str = ""
    core_object: str = ""
    metaphor_meaning: str = ""
    annotation1: str = ""
    annotation2: str = ""
    annotation3: str = ""
    series_name: str = ""
    magazine_name: str = ""
    core_shape: str = ""
    crowd_state: str = ""
    scattered_elements: str = ""
    top_directory: str = ""
    bottom_info: str = ""
    semantic_direction: str = ""
    specified_material: str = ""
    texture_keywords: str = ""
    background: str = ""
    randomness: str = ""
    surprise_mode: bool = False
    flow_action: str = ""
    core_structure: str = ""
    node1: str = ""
    node2: str = ""
    node3: str = ""
    node4: str = ""
    feedback_loop: str = ""
    risk_label: str = ""
    core_subject: str = ""
    relation_action: str = ""
    accent_element: str = ""
    line_type: str = ""
    emotion: str = ""
    main_visual_text: str = ""
    label1: str = ""
    label2: str = ""
    label3: str = ""
    label4: str = ""
    stage1: str = ""
    stage2: str = ""
    stage3: str = ""
    stage4: str = ""
    serial_number: str = ""
    date_info: str = ""
    english_title: str = ""
    style_id: str = DEFAULT_STYLE_ID


@dataclass
class BodySpec:
    title: str
    structure: str
    modules: str
    notes: str
    character_action: str
    speech_bubble: str
    bottom_sentence: str
    subtitle: str = ""
    style_id: str = DEFAULT_STYLE_ID


def normalize_style(style_id: str | None) -> str:
    style_id = (style_id or DEFAULT_STYLE_ID).strip()
    if style_id not in STYLE_ANCHORS:
        raise ValueError(f"未知 style_id: {style_id}. 可用值: {', '.join(STYLE_ANCHORS)}")
    return style_id


def require_fields(data: Dict[str, Any], fields: List[str], label: str) -> None:
    missing = [field for field in fields if not str(data.get(field, "")).strip()]
    if missing:
        raise ValueError(f"{label} 缺少字段: {', '.join(missing)}")


def render_handdrawn_cover(spec: CoverSpec) -> str:
    return f"""请生成一张 21:9 横版中文知识文章封面图。
主题是「{spec.title}」。画面使用暖白色纸张背景，带轻微纸张纹理，整体干净、克制、精致、有大量留白。
采用左右结构：左侧约 45% 放主标题和副标题，右侧约 55% 放手绘概念图。
左侧用自然成熟的中文手写大字写标题：「{spec.title}」。标题可以分成两行或三行，其中一行背后可以加一块很淡的低饱和手绘笔刷色块。标题要大、有冲击力，但保持松弛、精致、克制，不要像广告字，不要像儿童字体，不要像毛笔书法。
标题下方写副标题：「{spec.subtitle}」。副标题使用较小的细线手写字，清楚、自然、安静。
右侧画一个简单的手绘概念图，核心隐喻是「{spec.metaphor}」。画面元素包括「{spec.elements}」。图解要简洁，不要复杂，像知识隐喻，不是插画场景。图解中可以有少量中文标签，每个标签 2 到 6 个字。
右下角画一个极简抽象小人，{spec.character_action}。小人旁边有一个小气泡，写着：「{spec.speech_bubble}」。
底部用很轻的小字写一句判断式结论：「{spec.bottom_sentence}」。
{STYLE_ANCHORS['handdrawn_knowledge_card']}"""


def render_oriental_cover(spec: CoverSpec) -> str:
    subtitle_or_bottom = spec.subtitle or spec.bottom_sentence
    return f"""请生成一张典籍山水风的中文文章封面图。
主题是「{spec.title}」。画面整体像高端文化杂志或图书封面，具有新中式东方美学、历史感、文学感和高级出版物质感。
画面使用暖白色宣纸质感背景，带细腻纸张颗粒。整体配色为低饱和蓝金色系，以石青、青蓝、金色、土黄、米白、墨灰为主，色彩克制、安静、典雅。
画面主体是一个巨大的文化隐喻物：「{spec.metaphor}」。这个隐喻物占据画面中心，像一个展开的古籍、卷轴、山河、地图或书页空间。让主体具有宏大空间感和诗意叙事感。
在主体中融入「{spec.elements}」，例如山脉、河流、书页、古文字、金色纹理、地图线条、印章、微缩人物等。元素要少而精，不要拥挤。
画面中加入几个微缩人物，人物穿着极简东方长袍或素色衣服，像行走在典籍、山水和历史之间。人物很小，只用于增强尺度感和叙事感，不要成为主角。
顶部或画面上方放置大标题「{spec.title}」，标题具有高级杂志封面感，可以使用优雅的衬线字体、中文书卷感字体或克制的手写字。标题要大气、留白充足，不要像广告字。
底部可以放一句很轻的副标题或判断句：「{subtitle_or_bottom}」。文字要小、克制、像出版物说明。
{STYLE_ANCHORS['oriental_editorial_illustration']}"""


def render_frosted_cover(spec: CoverSpec) -> str:
    return f"""请生成一张透明磨砂感海报风的中文封面图。
主题是「{spec.title}」。画面整体极简、高级、安静，像艺术节、音乐节、设计展或高端品牌海报。
背景是一整块低饱和冷灰绿色、雾白色或浅蓝灰色的半透明磨砂玻璃质感。主体像隔着磨砂玻璃看到的人物或物体，只露出模糊轮廓、深色阴影和局部形状，边缘柔和扩散，不要清晰写实。主体隐喻是「{spec.metaphor}」，画面元素包括「{spec.elements}」。
画面保留大量留白。主体可以放在画面中央偏上、偏左或偏下，形成疏离、神秘、克制的视觉情绪。
文字采用现代极简排版。标题写「{spec.title}」，可以放在画面右侧或中部偏右，使用简洁现代字体。副标题写「{spec.subtitle}」，字号较小。可以使用少量亮黄色或黑色文字作为视觉强调。
不要放太多信息，只保留最必要的标题、日期或一句短说明：「{spec.bottom_sentence}」。
{STYLE_ANCHORS['frosted_glass_editorial']}"""


def render_translucent_object_cover(spec: CoverSpec) -> str:
    return f"""请生成一张透明物件风的中文封面图。
主题是「{spec.title}」。画面整体像高端设计工作室作品集封面、设计展海报或品牌案例主视觉，极简、克制、干净、有高级感。
背景使用低饱和米灰、浅灰绿、雾白或浅冷灰色，保留大量留白。画面中心放置一个抽象主视觉物件，核心隐喻是「{spec.metaphor}」。这个物件由半透明玻璃、磨砂塑料、亚克力或柔软充气材质构成，边缘有细腻高光、折射、柔和阴影和真实材质感。
物件内部可以隐约看到被磨砂遮挡的柔和彩色块，例如珊瑚橙、雾蓝、浅粉、浅青色，颜色被玻璃材质扩散和模糊，不要过于鲜艳。
顶部或上方放置大标题「{spec.title}」，使用现代无衬线字体，颜色为浅灰或黑灰，排版克制。标题下方可以有一小段说明文字：「{spec.subtitle}」，字号小，像设计工作室说明文案。
画面中可以加入少量极简标识元素，例如小箭头、圆形标记、短横线、细线框，但不要复杂。画面元素包括：「{spec.elements}」。
{STYLE_ANCHORS['translucent_object_editorial']}"""


def render_glassmorphism_blob_cover(spec: CoverSpec) -> str:
    return f"""请生成一张玻璃气泡风的中文封面图。
主题是「{spec.title}」。画面使用浅灰白或雾白背景，整体极简、现代、轻盈，有高级设计展海报感。
画面中心放置 1 到 3 个半透明液态玻璃 blob 形体，形体边缘柔和，有折射、高光和磨砂质感。blob 内部有低饱和渐变光晕，颜色包括橙色、粉色、蓝色、青色或浅紫，颜色自然扩散，不要过度鲜艳。核心隐喻是「{spec.metaphor}」，画面元素包括：「{spec.elements}」。
标题写「{spec.title}」，使用现代无衬线大字。文字可以与玻璃 blob 前后穿插：一部分文字清晰在前景，一部分文字被玻璃材质模糊遮挡，形成空间层次。
副标题写「{spec.subtitle}」，字号较小，放在标题附近或画面边缘，排版克制。
整体保留大量留白，构图有呼吸感。画面可以有轻微投影和柔和环境光，但不要做成复杂 3D 场景。
{STYLE_ANCHORS['glassmorphism_gradient_blob']}"""


def render_embossed_typography_cover(spec: CoverSpec) -> str:
    return f"""请生成一张纸雕字体风的中文封面图。
主题是「{spec.title}」。画面以文字本身作为主视觉，不使用复杂插画。背景使用白色、浅灰、米白或牛皮纸质感，整体接近单色，极简、高级、有大量留白。
画面中心用大号中文或中英混排文字写「{spec.title}」。文字以纸张浮雕、凹刻、压痕、挖空或纸雕方式呈现，像从纸面凸起或被刻进纸面。字体边缘有细腻阴影和光照层次，形成真实纸雕质感。
副标题「{spec.subtitle}」可以使用很小的现代无衬线字体，放在标题上方或下方，排版克制。
整体构图要安静、稳重、留白充足。文字要成为唯一主角。可以加入非常轻微的纸张纹理，但不要加入复杂图案。底部短句：「{spec.bottom_sentence}」。
{STYLE_ANCHORS['embossed_typography_poster']}"""


def render_acrylic_type_cover(spec: CoverSpec) -> str:
    return f"""请生成一张亚克力字风的中文或中英混排封面图。
主题是「{spec.title}」。画面使用干净的白色或浅灰摄影棚背景，整体极简、现代、轻盈。
画面中心将标题「{spec.title}」设计成一组真实可触摸的 3D 立体字母物件。每个字母或部分文字可以使用不同材质，例如透明亚克力、半透明彩色塑料、磨砂玻璃、细金属线框、浅色纸板。字母之间有细腻的空间关系和自然阴影。
颜色使用低饱和绿色、珊瑚橙、浅黄、浅粉、奶油白、透明灰等，整体干净但有趣。不要使用高饱和霓虹色。核心隐喻是「{spec.metaphor}」，画面元素包括：「{spec.elements}」。
副标题「{spec.subtitle}」可以作为小号现代无衬线文字放在边缘或底部，不能抢主视觉。
{STYLE_ANCHORS['acrylic_dimensional_type']}"""



def render_dark_neon_search_cover(spec: CoverSpec) -> str:
    return f"""请生成一张霓虹搜索风的中文封面图。
主题是「{spec.title}」。画面使用纯黑或深黑背景，整体像 AI 搜索产品、探索工具或未来感网页启动页，神秘、安静、现代。
画面左侧或背景中有几条彩色霓虹光带或光环，颜色可以包含蓝色、紫色、绿色、橙色和黄色，光带带有颗粒噪点和柔和辉光，像正在流动的信息路径。
画面中心或偏右放置一个半透明磨砂质感的搜索框或胶囊按钮，搜索框里写「{spec.title}」。搜索框边缘柔和发光，带细腻颗粒感和阴影。
可以在搜索框旁边加入一个极简白色小角色、小猫或小人，像正在等待搜索结果。角色要很小、简洁、可爱但不幼稚。
画面顶部或角落加入一句很轻的副标题：「{spec.subtitle}」。文字要少，使用现代无衬线字体，灰白色或低亮度。画面元素包括：「{spec.elements}」。
{STYLE_ANCHORS['dark_neon_search_ui']}"""


def render_black_void_hands_cover(spec: CoverSpec) -> str:
    action = spec.character_action or spec.metaphor
    return f"""请生成一张黑场肢体风的中文封面图。
主题是「{spec.title}」。画面使用纯黑背景，大量留黑，整体极简、安静、戏剧化，像心理主题艺术海报。
画面中出现几只手或手臂，从不同方向伸入黑暗中。手部只被柔和白色边缘光照亮，部分轮廓清晰，部分逐渐消失在黑暗里。手势表达「{action}」，例如寻找、触碰、拒绝、拉近、求助、连接、悬停。
主体不要太多，保持构图克制。手部有真实感但不恐怖，像概念摄影或高级艺术海报。
标题「{spec.title}」使用极简现代字体，放在画面边缘或底部，颜色为灰白色。副标题「{spec.subtitle}」更小、更轻。
{STYLE_ANCHORS['black_void_glowing_hands']}"""


def render_soft_neumorphism_cover(spec: CoverSpec) -> str:
    return f"""请生成一张柔光界面风的中文封面图。
主题是「{spec.title}」。画面使用浅灰白、淡蓝灰或雾白背景，整体干净、柔和、轻科技，有高端智能产品界面的感觉。
画面中心放置一个新拟态 UI 主控件，核心隐喻是「{spec.metaphor}」，可以是搜索框、圆形旋钮、温度环、滑杆、卡片或控制面板。控件像从背景中轻轻凸起或凹陷，具有细腻软阴影、内阴影、圆角和柔和环境光。
控件中显示少量文字或数字：「{spec.title}」。可以加入一个简洁图标，例如搜索、目标、温度、进度、开关、光线。画面元素包括：「{spec.elements}」。
画面中可以有少量暖橙、浅蓝或浅绿光晕，表示状态变化或智能反馈。整体不要复杂，留白充足。
标题「{spec.title}」使用现代无衬线字体，排版极简。副标题「{spec.subtitle}」放在下方或角落，字号小、颜色浅。
{STYLE_ANCHORS['soft_neumorphism_ui']}"""


def render_minimal_line_shadow_cover(spec: CoverSpec) -> str:
    return f"""请生成一张线性品牌风的中文封面图。
主题是「{spec.title}」。画面使用浅灰白、淡蓝灰或雾白背景，大量留白，整体极简、克制、高级，像科技品牌发布会或产品主视觉。
画面中心放置一个由极细黑灰线条构成的巨大符号、数字、字母或几何形，核心隐喻是「{spec.metaphor}」。主体可以带有半透明长阴影、轻微折射、淡淡彩色光点或柔和环境光。
标题「{spec.title}」使用现代极细无衬线字体，可以放在主体下方、右下或顶部。副标题「{spec.subtitle}」字号更小，排版疏朗。
整体信息极少，画面要有空气感和品牌发布会感。画面元素包括：「{spec.elements}」。
{STYLE_ANCHORS['minimal_line_shadow_brand']}"""


def render_white_mono_texture_cover(spec: CoverSpec) -> str:
    return f"""请生成一张白色肌理风的中文封面图。
主题是「{spec.title}」。画面几乎只使用白色、浅灰和黑色，整体极简、安静、高级，有编辑网页或设计作品集封面的感觉。
画面主体是一道白色材质痕迹，核心隐喻是「{spec.metaphor}」，可以是厚涂刷痕、纸张折痕、压痕、浮起边缘、光影切面或白色材质块。主体与背景同色系，但通过细腻阴影、纹理和光照产生层次。
标题「{spec.title}」使用克制的字体，可以是优雅衬线体或现代无衬线体，放在画面左侧或留白区域。副标题「{spec.subtitle}」更小，像编辑说明文字。
画面保留大量留白，构图要安静、冷静、有深度，不要加入多余装饰。画面元素包括：「{spec.elements}」。
{STYLE_ANCHORS['white_mono_texture_editorial']}"""


def render_minimal_architecture_cover(spec: CoverSpec) -> str:
    return f"""请生成一张建筑线稿风的中文封面图。
主题是「{spec.title}」。画面使用白色或浅灰纸张背景，大量留白，整体像建筑设计作品集、空间叙事图或设计学院 portfolio 封面。
画面中使用极细黑色线条绘制几条水平基准线、虚线路径和简洁空间关系。可以加入几个微型黑色人物剪影，人物站在不同水平线上，沿着虚线路径移动，表达「{spec.metaphor}」。
标题「{spec.title}」使用极简现代字体，放在左下、下方或画面留白处。副标题「{spec.subtitle}」字号较小，像作品集说明。可以加入年份、项目编号或极简坐标标记，但要很少。
画面元素包括：「{spec.elements}」。
{STYLE_ANCHORS['minimal_architecture_portfolio']}"""


def render_healing_metaphor_cover(spec: CoverSpec) -> str:
    return f"""请生成一张极简治愈隐喻漫画风的中文封面图。
主题是「{spec.title}」。画面使用暖白色纸张纹理背景，大量留白，整体安静、温柔、治愈。
画面中心或下方放一个小小的圆脸小孩，黑色短发或毛茸茸头发，穿黄色连帽衫或黄色上衣，黑色短裤，白色小鞋，脸颊有浅粉色腮红。小孩正在「{spec.character_action}」。
用一个简单的情绪隐喻道具表达主题：「{spec.metaphor}」。道具可以是花、浇水壶、充电线、插头、爱心、磁铁、云朵、太阳、旗子、文字雨或网兜。道具与小孩之间要形成一个清楚的故事瞬间。
标题「{spec.title}」使用自然手写中文，放在画面上方或留白处。标题要短、温柔、安静，不要像广告语。
副标题「{spec.subtitle}」使用很小的手写字，放在标题下方或画面底部。
画面元素和少量中文词语包括：「{spec.elements}」。文字必须少，可以像漂浮在空中、被吸引过来、落下来或藏在道具里。底部短句：「{spec.bottom_sentence}」。
{STYLE_ANCHORS['minimal_healing_metaphor_comic']}"""


def render_healing_metaphor_body(spec: BodySpec) -> str:
    return f"""请生成一张极简治愈隐喻漫画风的文章正文配图。
这张图用于表达文章中的这句话：「{spec.title}」。
画面使用暖白色纸张纹理背景，大量留白。画面中有一个小小的圆脸小孩，黑色短发，穿黄色连帽衫或黄色上衣，黑色短裤，白色小鞋，脸颊有浅粉色腮红。
小孩正在「{spec.character_action}」，旁边有一个简单隐喻道具：「{spec.modules}」。这个道具用来象征「{spec.notes}」。
画面可以加入极少量中文词语：「{spec.speech_bubble}」，文字像雨、风、星星、光、被吸来的词、飘走的词或藏在道具里的词。文字不能多。
画面底部可以有一句很轻的安慰语：「{spec.bottom_sentence}」。
{STYLE_ANCHORS['minimal_healing_metaphor_comic']}"""


def render_object_annotation_cover(spec: CoverSpec) -> str:
    core_object = spec.core_object or spec.metaphor
    metaphor_meaning = spec.metaphor_meaning or spec.bottom_sentence or spec.metaphor
    principle1 = spec.principle1 or "暂停"
    description1 = spec.description1 or "先观察对象，不急着下结论"
    principle2 = spec.principle2 or "验证"
    description2 = spec.description2 or "沿着纹理检查事实和来源"
    principle3 = spec.principle3 or "负责"
    description3 = spec.description3 or "只输出你能承担的判断"
    annotation1 = spec.annotation1 or "观察纹理"
    annotation2 = spec.annotation2 or "定位证据"
    annotation3 = spec.annotation3 or "确认边界"
    series_name = spec.series_name or "AI Design & Beyond"
    return f"""请生成一张具象标注风的知识封面图。
主题是「{spec.title}」。画面使用纯白或暖白背景，大量留白，整体像高级编辑知识卡片、设计方法论页或 AI playbook 页面。
采用左右结构：左侧放大标题、副标题和 3 条原则列表；右侧放一个高清真实具象物品作为核心隐喻。
左侧标题写「{spec.title}」，使用大号现代无衬线黑体，左对齐，观点明确、有力量。标题下方写副标题「{spec.subtitle}」，字号较小，语气克制。
左下方放 3 条编号原则：
01「{principle1}」— {description1}
02「{principle2}」— {description2}
03「{principle3}」— {description3}
右侧核心物品是「{core_object}」，用来隐喻「{metaphor_meaning}」。物品要有真实摄影质感、自然阴影、细腻纹理和局部细节，可以带水珠、纤维、折痕、划痕、光泽或自然瑕疵。物品不局限于植物，也可以是钥匙、镜子、指南针、绳子、杯子、书、石头、灯泡、地图等。
在物品周围加入虚线箭头、小圆点定位、括号、波浪下划线、手绘星星、小爱心和短注释。注释内容包括：「{annotation1}」「{annotation2}」「{annotation3}」。标注要少而准，像设计师观察笔记。
画面中加入一个极简黑线手绘小人，正在「{spec.character_action}」。小人很小，只作为观察者或操作者，不要抢主视觉。
右下角或底部放系列名和署名：「{series_name}」。画面元素包括：「{spec.elements}」。
{STYLE_ANCHORS['editorial_object_annotation_card']}"""


def render_crowd_typography_cover(spec: CoverSpec) -> str:
    magazine_name = spec.magazine_name or spec.series_name or "Future Work Weekly"
    core_shape = spec.core_shape or spec.metaphor or "一个巨大的问号"
    metaphor_meaning = spec.metaphor_meaning or spec.bottom_sentence or spec.metaphor
    crowd_state = spec.crowd_state or "大量人群排成主体图形，少数人从边缘走向外部"
    scattered_elements = spec.scattered_elements or "周围散落少量独立个体和小群体，有人在停留、有人在离开、有人在排队"
    top_directory = spec.top_directory or "特别报道｜趋势观察｜城市与就业"
    bottom_info = spec.bottom_info or spec.bottom_sentence or "2026 Special Issue"
    return f"""请生成一张人群造字风的中文杂志封面图。
主题是「{spec.title}」。画面使用白色或浅灰色巨大地面空间，高空俯视视角，整体像财经杂志、深度报道或社会议题封面。
根据主题，把大量真实微缩小人排列成一个最合适的巨大图形：「{core_shape}」。这个图形可以是一个汉字、数字、问号、箭头、天平、裂缝、阶梯、漏斗、地图路径、趋势曲线或组织结构。图形必须能够直观表达「{metaphor_meaning}」。
小人要有真实服装颜色和自然动作，像真实人群从高处俯拍。人群状态是「{crowd_state}」。周围散落元素：「{scattered_elements}」。每个人都投下自然长阴影，增强俯视空间感。
画面中的文字排版像印在地面上。顶部放灰色杂志刊名或栏目名「{magazine_name}」，可以加入少量目录信息、页码和细线分隔：「{top_directory}」。中下方放主标题「{spec.title}」，使用粗黑中文字体。副标题写「{spec.subtitle}」，字号较小，排版克制。底部放日期、期号或页码：「{bottom_info}」。
画面元素包括：「{spec.elements}」。
{STYLE_ANCHORS['crowd_typography_scene']}"""


def infer_semantic_material(title: str, semantic_direction: str = "", specified_material: str = "", randomness: str = "", surprise_mode: bool = False) -> tuple[str, str]:
    text = f"{title} {semantic_direction}".lower()
    if specified_material:
        return specified_material, "使用用户指定材质，并确保材质与标题语义一致。"
    groups = [
        (("基础", "稳定", "框架", "结构", "长期", "根基", "搭建", "可靠"), "粗木板、木纹、钉子、石头、混凝土、年轮", "厚重、手工、稳定、粗粝"),
        (("成长", "复利", "自然", "生长", "沉淀", "慢慢来", "生命力"), "石头、苔藓、种子、藤蔓、土壤、枝叶", "有机、缓慢、自然、时间感"),
        (("混乱", "噪声", "消散", "遗忘", "不确定", "脆弱", "灰度"), "沙尘、灰尘、粉末、碎片、颗粒", "边缘散落、颗粒飞散、脆弱感"),
        (("甜蜜", "快乐", "能量", "生活", "轻松", "欲望", "奖励"), "蜂蜜、糖浆、奶油、水果、香蕉、果冻", "黏稠、柔软、明亮、可口"),
        (("ai", "系统", "自动化", "机器", "效率", "工程", "底层", "架构"), "机械零件、齿轮、金属、螺丝、弹簧、电路、轴承", "复杂精密、工业、结构清晰"),
        (("创作", "表达", "签名", "品味", "价值", "个人品牌", "审美"), "金色油漆、厚涂笔触、墨迹、刷痕、颜料", "手写、艺术、动态、高级"),
        (("prompt", "提示词", "生成", "草稿", "迭代", "原型", "设计过程"), "线稿描边、构造线、实心字、草图纸、半成品字形", "设计稿、生成过程、层次叠加"),
        (("信任", "连接", "关系", "身份", "承诺", "手工", "温度"), "布料、刺绣、皮革、缝线、纸张、印章、绳结", "手工、可靠、温暖、可触摸"),
    ]
    material, hint = "混合材质块、纸张、金属、木头和细线结构", "语义清晰、材质与概念强相关"
    for keywords, candidate, style_hint in groups:
        if any(k.lower() in text for k in keywords):
            material, hint = candidate, style_hint
            break
    if surprise_mode or randomness == "high":
        hint += "；启用惊喜模式，可混合 2 种非直白但相关的材质隐喻，但文字可读性优先"
    elif randomness == "medium":
        hint += "；允许 1-2 种材质混合，增加创意但保持可读"
    else:
        hint += "；严格按语义选择最明显材质，画面稳定易懂"
    return material, hint


def render_semantic_material_typography_cover(spec: CoverSpec) -> str:
    material, material_hint = infer_semantic_material(
        spec.title,
        semantic_direction=spec.semantic_direction,
        specified_material=spec.specified_material,
        randomness=spec.randomness,
        surprise_mode=spec.surprise_mode,
    )
    background = spec.background or "纯白、浅灰或干净摄影棚背景"
    texture_keywords = spec.texture_keywords or material_hint
    semantic_direction = spec.semantic_direction or spec.metaphor or spec.bottom_sentence
    return f"""请生成一张语义字体风的封面图。
主题是「{spec.metaphor or spec.title}」。画面中最重要的主视觉是标题文字「{spec.title}」，文字本身必须成为画面主体。
请先根据「{spec.title}」的语义，自动选择最合适的材质和结构来设计字体。材质必须服务内容含义，而不是随机装饰。
语义方向是「{semantic_direction}」。推荐材质方向：「{material}」。质感关键词：「{texture_keywords}」。
字体要有真实材质质感、自然光影、细节纹理和强烈触感。背景使用「{background}」，保留大量留白。标题必须清楚可读、醒目、有冲击力。
如果主题偏「稳定、基础、长期主义」，优先使用木头、石头、混凝土等厚重材质。
如果主题偏「成长、自然、生长」，优先使用苔藓、植物、种子、土壤、石头。
如果主题偏「消散、混乱、脆弱」，优先使用沙尘、灰尘、碎片、颗粒。
如果主题偏「甜蜜、能量、生活方式」，优先使用蜂蜜、水果、糖浆、奶油。
如果主题偏「系统、AI、自动化、工程」，优先使用机械零件、金属、齿轮、电路。
如果主题偏「创作、表达、品味」，优先使用金色笔触、油漆、手写刷痕。
如果主题偏「Prompt、生成、设计过程」，优先使用线稿描边、草图层、构造线和实心字体组合。
副标题「{spec.subtitle}」可以用小号现代字体放在标题下方或角落，不能抢主视觉。画面元素包括：「{spec.elements}」。底部短句：「{spec.bottom_sentence}」。
{STYLE_ANCHORS['semantic_material_typography']}"""


def render_quirky_doodle_cover(spec: CoverSpec) -> str:
    flow_action = spec.flow_action or spec.character_action or "小黑怪把素材送进机器，在机器里判断，然后推着输出卡片跑出来"
    core_structure = spec.core_structure or spec.metaphor or "信息源 → 判断机器 → 内容卡片 → 承接口 → 反馈回收"
    node1 = spec.node1 or "信息源"
    node2 = spec.node2 or "判断"
    node3 = spec.node3 or "内容生产"
    node4 = spec.node4 or "承接"
    feedback_loop = spec.feedback_loop or "用户反馈回到信息源"
    risk_label = spec.risk_label or "别乱写"
    return f"""请生成一张怪诞小人风的中文封面图。
主题是「{spec.title}」。画面白底留白，使用黑色细线手绘和少量红蓝橙标注，整体像一张轻松怪诞的工作流封面。
画面左侧放大标题「{spec.title}」，标题使用清晰黑色粗体或自然手写字。副标题写「{spec.subtitle}」，字号较小。
画面右侧或中间画一个怪诞小黑角色，正在「{flow_action}」。它周围有简单的系统装置，例如机器、文件堆、漏斗、工具箱、传送带、门、输出卡片或旗子，用来隐喻「{spec.metaphor}」。
请把内容组织成清晰结构：「{core_structure}」。节点包括：「{node1}」「{node2}」「{node3}」「{node4}」。每个节点只写 2-6 个字。
用橙色箭头表示主流程，用蓝色虚线表示反馈回路：「{feedback_loop}」，用红色文字标注关键风险或核心判断：「{risk_label}」。底部可以写一句很短的判断句：「{spec.bottom_sentence}」。
画面元素包括：「{spec.elements}」。画面要轻松、有趣、清楚，不要拥挤。
{STYLE_ANCHORS['quirky_doodle_character_flow']}"""


def render_quirky_doodle_body(spec: BodySpec) -> str:
    return f"""请生成一张怪诞小人风的中文正文配图。
主题是「{spec.title}」。画面使用纯白或暖白背景，大量留白，整体像轻松怪诞的手绘工作流漫画或 AI 系统草图。
画面中有一个或多个怪诞小人角色，默认是黑色不规则小怪物，圆角身体，短手短脚，白色小眼睛，表情呆萌、困惑或努力。小怪物正在参与这个流程：「{spec.character_action}」。
请把内容拆成一个清晰的流程或结构：「{spec.structure}」。可以使用机器、盒子、漏斗、传送带、门、文件、工具箱、旗子、输入口、输出口、路径线等极简手绘元素。
使用橙色箭头表示主流程，蓝色虚线表示反馈回路或回收路径，红色文字标注关键风险或核心判断。黑色用于普通线条和节点说明。
画面中的文字要少而清楚，核心节点包括：「{spec.modules}」。必要注释：「{spec.notes}」。每个节点只写 2-6 个字。底部判断句：「{spec.bottom_sentence}」。
{STYLE_ANCHORS['quirky_doodle_character_flow']}"""


def render_minimal_line_art_cover(spec: CoverSpec) -> str:
    core_subject = spec.core_subject or spec.metaphor or "一个极简人物或关系场景"
    action = spec.relation_action or spec.character_action or "安静地行走、靠近、思考或共同协作"
    accent = spec.accent_element or "一个很小的黄色灯泡、粉色爱心、红色小点或浅蓝远方线"
    line_type = spec.line_type or "连续一笔画或简洁轮廓线"
    emotion = spec.emotion or spec.bottom_sentence or "安静、克制、有概念感"
    return f"""请生成一张线条艺术风的中文封面图。
主题是「{spec.title}」。画面白底留白，使用极简黑色线条作为主视觉，整体安静、现代、克制。
画面主体是「{core_subject}」，用{line_type}表现。主体正在「{action}」，用来隐喻「{spec.metaphor}」。线条要干净、有流动感，不追求写实细节。
标题「{spec.title}」放在留白区域，使用简洁黑色字体。副标题「{spec.subtitle}」字号较小。可以加入一个很小的点缀色元素：「{accent}」。
画面情绪是「{emotion}」。画面元素包括：「{spec.elements}」。底部短句：「{spec.bottom_sentence}」。
{STYLE_ANCHORS['minimal_line_art']}"""


def render_minimal_line_art_body(spec: BodySpec) -> str:
    return f"""请生成一张线条艺术风的中文插画。
主题是「{spec.title}」。画面使用纯白或暖白背景，大量留白，整体极简、安静、优雅。
用黑色极简线条表现「{spec.modules}」。主体可以是人物、关系动作、城市轮廓、课堂场景、旅行场景、灵感灯泡、动物陪伴或抽象符号。线条要自然流动，像连续一笔画或少量克制轮廓线，只保留关键姿态和情绪，不画复杂细节。
画面核心动作是：「{spec.character_action}」。通过线条表达「{spec.notes}」。
可以根据主题加入少量点缀色，例如浅粉爱心、黄色灯泡、浅蓝远方、红色重点、小星星或浅灰阴影。点缀色必须很少，不能破坏黑白极简感。
如果需要文字，加入短标题「{spec.title}」，使用极简中文字体或自然手写字，放在留白处。底部判断句：「{spec.bottom_sentence}」。
{STYLE_ANCHORS['minimal_line_art']}"""


EXTRA_COVER_GUIDES = {
    "retro_minimal_poster_illustration": "米白旧纸背景，复古印刷颗粒，大面积钴蓝和芥末黄色块，几何化人物或物件，像中世纪现代海报、复古书封或丝网印刷插画。",
    "editorial_balloon_collage": "白色纸张背景，大量留白，半透明彩色圆片像气球或光片，下方用细线素描人物或物件，并用细线连接到圆片，像品牌广告或编辑设计封面。",
    "transparent_architectural_type": "浅灰或雾白背景，巨大透明玻璃数字、字母或汉字作为建筑空间，内部有云雾、天空、山体、光线、微型人物或空间场景。",
    "paper_cut_profile_silhouette": "白色或浅米色纸张背景，单色纸雕剪影作为主体，剪影内部嵌入行业场景、建筑、工具、道路、书本或系统结构，有纸张厚度和投影。",
    "torn_paper_note_minimal": "米色、暖白或浅灰纸张背景，大量留白，中心或偏下只有一小片白色撕裂纸条，纸条上写一个词或一句很短的话。",
    "fluffy_soft_typography": "白色、奶油色或浅灰背景，标题文字变成真实可触摸的毛绒、毛巾布、羊羔绒或绒线立体字体，边缘有细密绒毛和柔和阴影。",
    "cloud_typography_cover": "蓝天或青蓝渐变天空背景，标题文字由真实蓬松的白云组成，有阳光照射、云影和细腻云气质感，画面开阔、明亮、向上。",
    "editorial_line_character": "白色或奶油白背景，大量留白，黑白极简线稿人物作为主要叙事角色，搭配杂志式大标题、非对称网格和少量柔和色块；可做成品牌视觉板、海报、网站首屏、包装或多面板编辑插画。",
    "editorial_object_annotation_card": "纯白或暖白背景，大量留白，左侧大标题、副标题和三条编号原则，右侧一个高清真实具象物品作为核心隐喻，周围有虚线箭头、小圆点、手写短注释和极简手绘小人，像高级方法论知识卡片。",
    "crowd_typography_scene": "白色或浅灰色巨大地面，高空俯视，大量真实微缩小人排列成文字、数字、问号、箭头、天平、裂缝、阶梯、路径、趋势曲线或组织结构；文字像印在地面上，整体是财经杂志或深度社会议题封面。",
    "semantic_material_typography": "简洁白色或浅灰摄影棚背景，标题文字本身是唯一主视觉；根据标题语义自动选择木头、石头、苔藓、沙尘、蜂蜜、机械、金属、线稿、布料等真实材质，让材质表达含义，保持文字醒目可读。",
    "quirky_doodle_character_flow": "白底大量留白，黑色细线手绘怪诞小黑角色参与工作流；用机器、盒子、漏斗、传送带、文件、门、工具箱、旗子、橙色箭头、蓝色虚线反馈和红色风险标注表达 AI 系统流程。",
    "minimal_line_art": "纯白或暖白背景，大量留白，用极简黑色连续线条或少量克制轮廓线表现人物、关系、城市、旅行、课堂、灵感灯泡或抽象符号；只加入极少点缀色，整体优雅克制。",
    "monochrome_system_editorial": "黑白灰高对比，巨型粗体中文或英文字压场，配合档案盒、索引卡、锁、阶梯、门、路径线、路线图、货船、集装箱或微缩人物，并加入细线网格、编号、条形码和工业化信息排版。",
}


def render_extra_cover(spec: CoverSpec) -> str | None:
    guide = EXTRA_COVER_GUIDES.get(spec.style_id)
    if not guide:
        return None
    return f"""请生成一张{STYLE_NAMES[spec.style_id]}的中文封面图。
主题是「{spec.title}」。{guide}
核心隐喻是「{spec.metaphor}」。画面元素包括：「{spec.elements}」。
标题「{spec.title}」作为画面主视觉或重要文字，副标题「{spec.subtitle}」使用小号克制排版，底部短句为「{spec.bottom_sentence}」。
整体构图要干净、克制、留白充足，符合高质量文章封面、书封或社交媒体主视觉。
{STYLE_ANCHORS[spec.style_id]}"""

def render_monochrome_system_editorial_cover(spec: CoverSpec) -> str:
    main_text = spec.main_visual_text or spec.title or "SYSTEM"
    core_object = spec.core_object or spec.metaphor or "透明档案盒、索引卡、锁、阶梯、门、路径线或路线图"
    meaning = spec.metaphor_meaning or spec.metaphor or "把经验、流程和标准封装成可复用系统"
    labels = [spec.label1 or "SYSTEM", spec.label2 or "METHOD", spec.label3 or "PROCESS", spec.label4 or "STANDARD"]
    stages = [spec.stage1 or "输入", spec.stage2 or "标准化", spec.stage3 or "执行", spec.stage4 or "复用"]
    serial = spec.serial_number or "REF W-001"
    date_info = spec.date_info or "SYSTEM PLAYBOOK"
    english = spec.english_title or "Monochrome System Editorial"
    return f"""请生成一张黑白系统风的中文封面图。
主题是「{spec.title}」。画面使用黑白灰单色，高对比，白色或浅灰背景，整体冷静、专业、系统、权威，像高级方法论手册、SOP 封面、工业设计板或专业知识产品封面。
画面主视觉使用巨型黑色粗体文字：「{main_text}」。文字可以是中文、英文或中英混排，占据画面 40%-70%，字形厚重、方正、工业、极具压迫感。文字可以与物件发生遮挡或空间关系。
画面中加入一个系统隐喻物件：「{core_object}」。这个物件用来表达「{meaning}」。物件要真实、克制、有工业设计感，不要花哨。补充元素包括：「{spec.elements}」。
排版中加入细线网格、模块分隔线、编号、条形码、REF 编号、页码、日期和小号英文标签。可以出现如下小标签：「{labels[0]}」「{labels[1]}」「{labels[2]}」「{labels[3]}」。
标题写「{spec.title}」，副标题写「{spec.subtitle}」。标题使用粗黑中文字体，副标题使用小号无衬线字体。底部加入流程导航：「01 {stages[0]} / 02 {stages[1]} / 03 {stages[2]} / 04 {stages[3]}」。角落加入「{serial}」和「{date_info}」，英文小标题为「{english}」。底部判断句：「{spec.bottom_sentence}」。
{STYLE_ANCHORS['monochrome_system_editorial']}"""


def render_cover(spec: CoverSpec) -> str:
    spec.style_id = normalize_style(spec.style_id)
    if spec.style_id == "oriental_editorial_illustration":
        return render_oriental_cover(spec)
    if spec.style_id == "frosted_glass_editorial":
        return render_frosted_cover(spec)
    if spec.style_id == "translucent_object_editorial":
        return render_translucent_object_cover(spec)
    if spec.style_id == "glassmorphism_gradient_blob":
        return render_glassmorphism_blob_cover(spec)
    if spec.style_id == "embossed_typography_poster":
        return render_embossed_typography_cover(spec)
    if spec.style_id == "acrylic_dimensional_type":
        return render_acrylic_type_cover(spec)
    if spec.style_id == "dark_neon_search_ui":
        return render_dark_neon_search_cover(spec)
    if spec.style_id == "black_void_glowing_hands":
        return render_black_void_hands_cover(spec)
    if spec.style_id == "soft_neumorphism_ui":
        return render_soft_neumorphism_cover(spec)
    if spec.style_id == "minimal_line_shadow_brand":
        return render_minimal_line_shadow_cover(spec)
    if spec.style_id == "white_mono_texture_editorial":
        return render_white_mono_texture_cover(spec)
    if spec.style_id == "minimal_architecture_portfolio":
        return render_minimal_architecture_cover(spec)
    if spec.style_id == "minimal_healing_metaphor_comic":
        return render_healing_metaphor_cover(spec)
    if spec.style_id == "editorial_object_annotation_card":
        return render_object_annotation_cover(spec)
    if spec.style_id == "crowd_typography_scene":
        return render_crowd_typography_cover(spec)
    if spec.style_id == "semantic_material_typography":
        return render_semantic_material_typography_cover(spec)
    if spec.style_id == "quirky_doodle_character_flow":
        return render_quirky_doodle_cover(spec)
    if spec.style_id == "minimal_line_art":
        return render_minimal_line_art_cover(spec)
    if spec.style_id == "monochrome_system_editorial":
        return render_monochrome_system_editorial_cover(spec)
    extra_prompt = render_extra_cover(spec)
    if extra_prompt:
        return extra_prompt
    # Other styles can still render as knowledge-style cover with their style anchor.
    if spec.style_id == "handdrawn_knowledge_card":
        return render_handdrawn_cover(spec)
    return f"""请生成一张中文知识文章封面图。
主题是「{spec.title}」。画面为横版封面构图，标题清楚，主体隐喻明确，整体适合{STYLE_NAMES[spec.style_id]}。
标题：「{spec.title}」。副标题：「{spec.subtitle}」。
核心隐喻：「{spec.metaphor}」。画面元素包括：「{spec.elements}」。
加入少量人物或手绘元素，{spec.character_action}。可以有一句小气泡：「{spec.speech_bubble}」。
底部写一句轻量判断句：「{spec.bottom_sentence}」。
{STYLE_ANCHORS[spec.style_id]}"""


def render_handdrawn_body(spec: BodySpec) -> str:
    if spec.structure not in BODY_STRUCTURES:
        raise ValueError(f"未知正文结构: {spec.structure}")
    return f"""请生成一张中文文章正文配图，不是封面图。
主题是「{spec.title}」。画面为横版 16:9 构图，暖白色纸张背景，轻微纸感纹理，整体干净、克制、精致、有大量留白。
画面顶部居中写一个自然成熟的中文手写标题：「{spec.title}」，标题下方可以有一条很轻的手绘短线。
画面中间绘制一个「{spec.structure}」。核心模块包括：「{spec.modules}」。模块使用低饱和浅色圆角卡片、便签、框图或标签承载，模块之间用黑灰色细线手绘箭头连接。主体图解不要过大，四周保留明显留白。
在图解旁加入少量极简短注释：「{spec.notes}」。注释必须短，不要生成大段正文，不要密集小字。
画面右侧或右下角画一个极简抽象小人，细线条，成人感，{spec.character_action}。小人旁边有一个小气泡，写着：「{spec.speech_bubble}」。
画面底部用轻微手写小字写一句判断式结论：「{spec.bottom_sentence}」。
{STYLE_ANCHORS['handdrawn_knowledge_card']}"""


def render_study_note(spec: BodySpec) -> str:
    return f"""请生成一张学习笔记风的中文知识图。
主题是「{spec.title}」。画面使用米白色纸张背景，中间放置一张略带阴影的笔记纸卡片，整体像精心整理的学习手账页面。
顶部用醒目的中文标题写「{spec.title}」，标题可以放在浅紫色手绘色块或浅黄色标签上。标题字体清楚、圆润、自然，有学习笔记感。
画面内容分为 3 到 5 个清晰区域，每个区域有小标题、简短说明和少量重点词高亮。核心内容包括：「{spec.modules}」。
加入少量学习类装饰元素，例如胶带、回形针、便签、贴纸、手绘笔记本、清单、箭头、小星星。装饰要克制，不要抢内容。
正文使用深绿色或深灰色文字，重点词可以用浅黄色或浅紫色荧光笔效果标注。必要注释：「{spec.notes}」。
底部写一句总结：「{spec.bottom_sentence}」。
{STYLE_ANCHORS['study_note_card']}"""


def render_pyramid(spec: BodySpec) -> str:
    return f"""请生成一张粉彩金字塔风的中文知识图。
主题是「{spec.title}」。画面为竖版或横版纸张纹理背景，整体干净、轻松、有手绘学习海报感。
顶部写一个醒目的中文手写标题：「{spec.title}」，标题下方可以有柔和的粉彩笔刷底色。副标题写「{spec.subtitle or spec.bottom_sentence}」，字号较小，像手写笔记。
画面中心绘制一个分层结构，可以是金字塔、阶梯或漏斗。分层包括：「{spec.modules}」。每一层使用不同的低饱和粉彩色块，例如粉色、橙色、黄色、薄荷绿、浅蓝、浅紫。色块边缘保留手绘笔刷质感。
在每一层旁边加入简短标注：「{spec.notes}」。可以使用虚线、箭头、小标签、百分比框来连接说明。
如果内容有对比关系，可以在左侧标注「被动学习」，在下方或右侧标注「主动学习」，用虚线和箭头表达层级变化。
{STYLE_ANCHORS['pastel_learning_pyramid']}"""


def render_childlike(spec: BodySpec) -> str:
    return f"""请生成一张童趣科普风的中文知识图。
主题是「{spec.title}」。画面使用白色纸张背景，外圈有自然的黑色手绘边框，整体像少儿文化科普海报或儿童绘本知识页。
顶部用大号中文手写标题写「{spec.title}」，副标题写「{spec.subtitle or spec.bottom_sentence}」，标题自然、童趣、清楚。
画面中分布多个手绘文化物件或知识元素，包括：「{spec.modules}」。每个物件用黑色手绘线条和轻水彩上色表现，风格可爱、自然、有课堂小报感。
用虚线箭头连接不同物件，旁边加入简短中文注释：「{spec.notes}」。注释像手写小标签，清楚易懂，不要太长。
可以加入 1 到 2 个可爱的手绘人物或拟人小角色，用气泡说一句话：「{spec.speech_bubble}」。人物要童趣、亲切，不要写实。
{STYLE_ANCHORS['childlike_cultural_infographic']}"""


def render_body(spec: BodySpec) -> str:
    spec.style_id = normalize_style(spec.style_id)
    if spec.style_id == "handdrawn_knowledge_card":
        return render_handdrawn_body(spec)
    if spec.style_id == "study_note_card":
        return render_study_note(spec)
    if spec.style_id == "pastel_learning_pyramid":
        return render_pyramid(spec)
    if spec.style_id == "childlike_cultural_infographic":
        return render_childlike(spec)
    if spec.style_id == "minimal_healing_metaphor_comic":
        return render_healing_metaphor_body(spec)
    if spec.style_id == "quirky_doodle_character_flow":
        return render_quirky_doodle_body(spec)
    if spec.style_id == "minimal_line_art":
        return render_minimal_line_art_body(spec)
    # Cover/editorial styles are not ideal for body diagrams; still render a sparse editorial visual if explicitly requested.
    return f"""请生成一张中文知识视觉图，主题是「{spec.title}」。
画面不要做成密集正文解释图，只保留少量核心概念。核心模块包括：「{spec.modules}」。必要注释：「{spec.notes}」。
底部写一句判断式结论：「{spec.bottom_sentence}」。
{STYLE_ANCHORS[spec.style_id]}"""


def build_image_item(raw: Dict[str, Any], index: int) -> Dict[str, Any]:
    image_type = raw.get("type")
    style_id = normalize_style(raw.get("style_id") or raw.get("style") or DEFAULT_STYLE_ID)
    if image_type == "cover":
        require_fields(raw, ["title", "subtitle", "metaphor", "elements", "character_action", "speech_bubble", "bottom_sentence"], "cover")
        spec = CoverSpec(
            title=raw["title"],
            subtitle=raw["subtitle"],
            metaphor=raw["metaphor"],
            elements=raw["elements"],
            character_action=raw["character_action"],
            speech_bubble=raw["speech_bubble"],
            bottom_sentence=raw["bottom_sentence"],
            principle1=raw.get("principle1", ""),
            description1=raw.get("description1", ""),
            principle2=raw.get("principle2", ""),
            description2=raw.get("description2", ""),
            principle3=raw.get("principle3", ""),
            description3=raw.get("description3", ""),
            core_object=raw.get("core_object", ""),
            metaphor_meaning=raw.get("metaphor_meaning", ""),
            annotation1=raw.get("annotation1", ""),
            annotation2=raw.get("annotation2", ""),
            annotation3=raw.get("annotation3", ""),
            series_name=raw.get("series_name", ""),
            magazine_name=raw.get("magazine_name") or raw.get("column_name", ""),
            core_shape=raw.get("core_shape", ""),
            crowd_state=raw.get("crowd_state", ""),
            scattered_elements=raw.get("scattered_elements", ""),
            top_directory=raw.get("top_directory", ""),
            bottom_info=raw.get("bottom_info", ""),
            semantic_direction=raw.get("semantic_direction", ""),
            specified_material=raw.get("specified_material", ""),
            texture_keywords=raw.get("texture_keywords", ""),
            background=raw.get("background", ""),
            randomness=raw.get("randomness", ""),
            surprise_mode=(raw.get("surprise_mode") is True or str(raw.get("surprise_mode", "")).lower() in {"1", "true", "yes", "y", "是", "启用", "开启"}),
            flow_action=raw.get("flow_action", ""),
            core_structure=raw.get("core_structure", ""),
            node1=raw.get("node1", ""),
            node2=raw.get("node2", ""),
            node3=raw.get("node3", ""),
            node4=raw.get("node4", ""),
            feedback_loop=raw.get("feedback_loop", ""),
            risk_label=raw.get("risk_label", ""),
            core_subject=raw.get("core_subject", ""),
            relation_action=raw.get("relation_action") or raw.get("action", ""),
            accent_element=raw.get("accent_element", ""),
            line_type=raw.get("line_type", ""),
            emotion=raw.get("emotion", ""),
            main_visual_text=raw.get("main_visual_text") or raw.get("hero_text") or raw.get("primary_text", ""),
            label1=raw.get("label1", ""),
            label2=raw.get("label2", ""),
            label3=raw.get("label3", ""),
            label4=raw.get("label4", ""),
            stage1=raw.get("stage1", ""),
            stage2=raw.get("stage2", ""),
            stage3=raw.get("stage3", ""),
            stage4=raw.get("stage4", ""),
            serial_number=raw.get("serial_number") or raw.get("number", ""),
            date_info=raw.get("date_info") or raw.get("date", ""),
            english_title=raw.get("english_title", ""),
            style_id=style_id,
        )
        return {
            "id": raw.get("id") or f"cover_{index:02d}",
            "type": "cover",
            "aspect_ratio": raw.get("aspect_ratio") or "21:9",
            "style_id": style_id,
            "style_name": STYLE_NAMES[style_id],
            "title": spec.title,
            "subtitle": spec.subtitle,
            "prompt": render_cover(spec),
        }
    if image_type == "body":
        require_fields(raw, ["title", "structure", "modules", "notes", "character_action", "speech_bubble", "bottom_sentence"], "body")
        spec = BodySpec(
            title=raw["title"],
            structure=raw["structure"],
            modules=raw["modules"],
            notes=raw["notes"],
            character_action=raw["character_action"],
            speech_bubble=raw["speech_bubble"],
            bottom_sentence=raw["bottom_sentence"],
            subtitle=raw.get("subtitle", ""),
            style_id=style_id,
        )
        return {
            "id": raw.get("id") or f"body_{index:02d}",
            "type": "body",
            "aspect_ratio": raw.get("aspect_ratio") or "16:9",
            "style_id": style_id,
            "style_name": STYLE_NAMES[style_id],
            "title": spec.title,
            "structure": spec.structure,
            "prompt": render_body(spec),
        }
    raise ValueError(f"未知图片类型: {image_type}")


def build_batch(series_title: str, raw_images: List[Dict[str, Any]]) -> Dict[str, Any]:
    cover_i = body_i = 0
    images = []
    for raw in raw_images:
        if raw.get("type") == "cover":
            cover_i += 1
            images.append(build_image_item(raw, cover_i))
        elif raw.get("type") == "body":
            body_i += 1
            images.append(build_image_item(raw, body_i))
        else:
            images.append(build_image_item(raw, len(images) + 1))
    return {
        "series_title": series_title,
        "visual_style": DEFAULT_STYLE_ID,
        "available_styles": STYLE_NAMES,
        "global_style_prompt": STYLE_ANCHORS[DEFAULT_STYLE_ID],
        "images": images,
    }


def self_test() -> None:
    batch = build_batch(
        "个人知识库真正的用法",
        [
            {
                "type": "cover",
                "style_id": "oriental_editorial_illustration",
                "title": "文明的长河",
                "subtitle": "从典籍里看见时间",
                "metaphor": "展开的古籍化作山河与河流",
                "elements": "书页、山脉、河流、金色文字、微缩人物",
                "character_action": "微缩人物在书页山河间行走",
                "speech_bubble": "山河在书里",
                "bottom_sentence": "文明不是过去，而是持续流动的时间。",
            },
            {
                "type": "cover",
                "style_id": "translucent_object_editorial",
                "title": "重新设计工作流",
                "subtitle": "让系统替你承担复杂度",
                "metaphor": "透明文件夹里容纳彩色流程模块",
                "elements": "磨砂文件夹、柔和彩色块、小箭头、细线框",
                "character_action": "旁边有极小的抽象人物观察物件",
                "speech_bubble": "系统来承重",
                "bottom_sentence": "复杂度应该被系统吸收。",
            },
            {
                "type": "cover",
                "style_id": "dark_neon_search_ui",
                "title": "寻找答案",
                "subtitle": "AI 搜索从问题开始",
                "metaphor": "黑暗中的信息光带汇入搜索框",
                "elements": "霓虹光带、搜索框、极简小猫、颗粒噪点",
                "character_action": "小猫等待搜索结果",
                "speech_bubble": "Searching",
                "bottom_sentence": "探索从一个好问题开始。",
            },
            {
                "type": "cover",
                "style_id": "minimal_healing_metaphor_comic",
                "title": "给自己充电",
                "subtitle": "低能量的时候，也可以先停下来",
                "metaphor": "插头、充电线、低电量图标",
                "elements": "慢慢来、恢复中、红色小爱心",
                "character_action": "坐在地上低头休息，旁边有充电线",
                "speech_bubble": "恢复中",
                "bottom_sentence": "你可以先慢慢恢复。",
            },
            {
                "type": "body",
                "style_id": "study_note_card",
                "title": "知识库不是收藏夹",
                "structure": "学习笔记卡片",
                "modules": "输入、连接、输出、复用",
                "notes": "少存一点、多连接一点、能用才算数",
                "character_action": "指向知识卡片",
                "speech_bubble": "要能产出",
                "bottom_sentence": "不能输出的资料，只是库存。",
            },
        ],
    )
    assert batch["images"][0]["style_id"] == "oriental_editorial_illustration"
    assert "典籍山水风" in batch["images"][0]["prompt"]
    assert batch["images"][1]["style_id"] == "translucent_object_editorial"
    assert "透明物件风" in batch["images"][1]["prompt"]
    assert batch["images"][2]["style_id"] == "dark_neon_search_ui"
    assert "霓虹搜索风" in batch["images"][2]["prompt"]
    assert batch["images"][3]["style_id"] == "minimal_healing_metaphor_comic"
    assert "极简治愈隐喻漫画风" in batch["images"][3]["prompt"]
    assert batch["images"][4]["style_id"] == "study_note_card"
    assert "学习笔记风" in batch["images"][4]["prompt"]
    print("self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description="渲染 zscc配图生成器批量 prompt JSON")
    parser.add_argument("input", nargs="?", help="输入 JSON 文件；省略时从 stdin 读取")
    parser.add_argument("--self-test", action="store_true", help="运行内置测试")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    text = open(args.input, "r", encoding="utf-8").read() if args.input else sys.stdin.read()
    data = json.loads(text)
    series_title = data.get("series_title") or data.get("title") or "未命名系列"
    raw_images = data.get("images") or []
    if not isinstance(raw_images, list) or not raw_images:
        raise ValueError("输入 JSON 必须包含非空 images 数组")
    json.dump(build_batch(series_title, raw_images), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
