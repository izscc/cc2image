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
        '整体风格为怪诞小人风：16:9 横版，纯白背景，大量留白，黑色细线手绘，线条自然略带抖动。画面中有一个或多个怪诞小人角色；优先参考内置校准样图目录 assets/examples/xiaohei/ 的小黑 IP 稳定特征，但不要照抄任何样图构图或物件。小黑必须是黑色实心不规则小怪物，白色圆点眼睛，细胳膊细腿，空表情、认真、冷幽默，像低调的系统操作员，不是普通线稿小人、可爱吉祥物或儿童卡通。小黑必须承担核心概念动作，例如搬运、拉线、分拣、称重、守门、修补、卡在机器里、从输出口出来；不能只是站在旁边当装饰。每张图只讲一个认知锚点或核心结构，版式由内容动作决定，不固定左题右图。主体约占画面 40%-60%，至少保留 35% 空白。中文手写标注最多 5-8 处，每处 2-8 字。黑色用于主体线稿和小黑，橙色用于主流程，红色用于风险、问题或重点，蓝色用于反馈、系统状态或补充说明。不要写“流程图/系统架构/常见坑/路线图”等类型标题，不要 PPT、正式流程图、商业插画、儿童卡通、真实 UI、复杂架构、纸纹、渐变、阴影、密集文字。\nQuirky doodle character flow style, standalone 16:9 Chinese article illustration, pure white background, lots of negative space, thin black hand-drawn lines, slightly wobbly sketch quality. Use the bundled calibration examples in assets/examples/xiaohei/ only to stabilize the recurring Xiaohei IP character, line density, whitespace and restrained red/orange/blue labels; do not copy any example composition or object. Xiaohei is a small solid-black irregular blob creature with white dot eyes, tiny thin arms and legs, blank serious deadpan expression, like a quiet system operator; not a generic stick figure, not a cute mascot, not children illustration. The character must perform the core conceptual action: carrying, pulling, sorting, weighing, guarding, repairing, getting stuck inside a machine, coming out of an output door; never decorative. One image explains one cognitive anchor. Content-driven layout, not a fixed template. Main subject around 40-60% of the canvas, at least 35% blank white space. Use at most 5-8 short handwritten Chinese labels. Orange for main flow, red for risk/problem/focus, blue for feedback/system state. Do not write structure type titles. Not PPT, not formal flowchart, not commercial illustration, not cute mascot poster, not children illustration, not realistic UI, not paper texture, not gradients, not dense text.'
    ),
    "minimal_line_art": (
        '整体风格为线条艺术风：纯白或暖白背景，大量留白，用极简黑色线条表达主体。线条可以是连续一笔画，也可以是少量克制的轮廓线，线条自然流动、干净、轻盈。画面只保留最关键的人物姿态、关系动作、场景轮廓或概念符号，不画复杂细节。允许根据主题加入少量点缀色，例如浅粉爱心、黄色灯泡、浅蓝远方、红色重点或浅灰阴影。整体安静、优雅、克制、有情绪和概念感。不要复杂背景，不要厚重上色，不要写实人物，不要 3D，不要卡通夸张，不要高饱和颜色，不要密集文字。\nMinimal line art style, clean white background, lots of negative space, simple black continuous line drawing, elegant flowing outlines, minimal details, expressive posture and emotion, one-line illustration feel. Use only a tiny accent color when needed, such as pale pink heart, yellow light bulb, soft blue distance, red focus mark, or light gray shadow. Quiet, poetic, modern, minimal, conceptual. Not realistic, not 3D, not colorful cartoon, not complex background, not dense text.'
    ),
    "isometric_modular_system": (
        '整体风格为轴测模块系统风：统一等距/轴测视角，所有物体服从同一套斜向网格和轴线，远近不缩放，不使用戏剧化透视。画面像高端产品官网、SaaS 架构图、城市地图、服务流程图或品牌插画体系。主体由可组合模块构成：平台、方块、楼层、路径、台阶、管道、桥、门、窗口、浮动信息卡片、微型人物和图标。顶面承载路径、地图或平面关系；侧面承载层级、结构和状态；标签短而清楚。配色低饱和，常用米白、浅蓝、浅绿、浅黄、深蓝灰，线条统一，阴影轻微。重点对象通过尺寸、位置、颜色和描边控制优先级。适合解释系统、流程、空间、路线、组件关系和品牌系列。不要强透视，不要近大远小，不要电影景深，不要真实 3D 渲染，不要复杂装饰，不要密集文字，不要英文乱码。\nIsometric modular system illustration style, consistent isometric/axonometric grid, no perspective shrinkage, equal scale for near and far objects, modular blocks, platforms, paths, stairs, pipes, bridges, cards, tiny people and icons, clean SaaS architecture diagram or product website illustration, muted colors, clear hierarchy, reusable component system, no dramatic perspective, no depth of field, not realistic 3D, not cluttered.'
    ),
    "isometric_timeline_miniature": (
        '整体风格为时间微缩风：使用 45° 等距俯视视角，创建一个横向展开的微型 3D 时间轴展台。画面像微型博物馆、桌面沙盘或精致教育插画。底座被分成 4-6 个清晰时代区域，从左到右展示主题从早期到现代的演化。每个区域放置该时代最具代表性的物件、工具、设备、环境或技术，并加入少量微型人物与场景互动。顶部居中放大标题，下方放副标题和极简时间轴图标。整体材质柔和、干净、精致，光线均匀，背景为纯色或柔和渐变。不要复杂写实场景，不要拥挤，不要卡通夸张，不要高饱和杂乱，不要密集文字。\nClean isometric miniature 3D timeline diorama style, 45-degree top-down perspective, horizontal stepped base divided into clear time periods, each section shows era-specific objects, tools, environments, or technology. Add tiny stylized figures interacting with each stage, minimal facial detail. Soft refined materials, realistic PBR shading, neutral balanced lighting, clean solid background. Top center title, subtitle showing From [start era] to [modern era], small timeline icon underneath. Educational museum-like miniature evolution diagram, not cluttered, not cartoonish, not dense infographic.'
    ),
    "real_object_doodle_composite": (
        '整体风格为实物涂鸦风：干净白色或暖白纸张背景，真实日常物品被物理放置在画面中，并与黑色手绘线稿角色无缝结合。真实物品必须成为角色或场景的关键部分，例如头、头发、大脑、身体、负担、心脏、武器、衣服、道具或爆炸效果。手绘部分使用简单黑色墨线，像快速漫画草图，表情夸张、动作明确、幽默而有情绪。画面通过真实物品和线稿之间的语义错位形成视觉双关，既聪明又易懂。背景极简，大量留白，真实物品有自然光影和摄影质感。可以加入一句短手写吐槽文字。不要复杂背景，不要完整彩色插画，不要 3D，不要普通拼贴，不要让物品只是装饰，不要密集文字。\nReal object doodle composite style: clean white paper background, one real everyday object physically placed in the scene and seamlessly integrated into a black ink hand-drawn cartoon illustration. The real object becomes a key part of the character or scene, such as the head, hair, brain, body, burden, heart, weapon, clothing, prop, or explosion. Simple expressive black line art, quick sketch feeling, exaggerated facial expression and clear action. The image creates a witty visual pun by turning the object into a meaningful part of the drawing. Photorealistic object, natural shadows, minimalist negative space, optional short handwritten caption. Not a full color illustration, not 3D, not cluttered, not ordinary collage, the object must not be decorative only.'
    ),
    "expressive_3d_quirky_character": (
        '整体风格为3D怪表情风：极简白色、浅灰或浅米色背景，大量留白，一个圆润夸张的 3D 小人角色作为主视觉。参考内置校准样图 assets/examples/3d_quirky/ 的角色质感、表情强度、动作夸张度和极简背景，但不要照抄样图人物、服装、构图或道具。角色头大身小，脸颊饱满，皮肤柔软，简单纯色服装，表情非常丰富，眼神、眉毛、嘴角和脸部肌肉都要夸张传达情绪。可表现不屑、无语、嫌弃、崩溃、焦虑、疲惫、得意、开心、怀疑、委屈、震惊、认真等表情，并配合抱臂、叉腰、摊手、抱头、OK 手势、指向、拖步、趴桌、举牌、推箱子等动作。整体像高质量 3D 表情包角色、轻量动画角色或 3D 版怪诞小人。可以搭配少量道具、流程元素或 8 字以内短句；不要真实儿童摄影，不要复杂背景，不要过度可爱玩具感，不要高饱和颜色，不要密集文字。\nExpressive quirky 3D character style: clean white, light gray or warm beige background with lots of negative space. Use bundled calibration examples in assets/examples/3d_quirky/ only to stabilize rounded 3D character quality, expressive facial intensity, exaggerated body language and sparse composition; do not copy any example identity, outfit, composition or prop. A rounded exaggerated 3D character as the main visual, big head, small body, chubby cheeks, soft skin, simple clothes, highly expressive face. Emotion is communicated through exaggerated eyes, eyebrows, mouth corners and facial muscles. The character can show skeptical, annoyed, unimpressed, exhausted, anxious, shocked, smug, happy, doubtful, embarrassed, confident or dramatic expressions, with matching body language such as crossed arms, hands on hips, shrugging, holding head, OK gesture, pointing, dragging feet, lying on a desk, holding a sign or pushing a box. High-quality 3D render, soft studio lighting, sticker-like or animated character feel. Not real child photography, not cluttered, not overly cute toy style, not dense text.'
    ),
    "giant_chinese_concept_poster": (
        '整体风格为大字海报风：高级中文概念海报，竖版 3:4 或 4:5，巨大中文主标题是绝对主体，字形清晰完整、无错字、无缺笔，占据画面 45%-75%。画面必须先理解输入文字的表层含义、深层寓意、情绪气质、文化联想、人物命运感和隐含张力，再自动决定最适合的字体气质、构图、色彩和视觉隐喻。人物、物体、空间或象征元素必须与大字发生关系，例如字中开门、字里藏城市、字的缝隙透出风景、字像建筑、字像墙、字像路、字像牢笼、字像窗、字像裂缝、字被光穿透、人物站在字下或走入字中。大字是第一视觉，隐喻图像是第二视觉，小字是第三视觉。小字只保留三处：左上角 2-4 个关键词，右侧竖排一句命运感短句，左下角一句传播力总结句。整体高级、极简、克制、展览级，有强排版、强隐喻、强情绪、强记忆点。不要拥挤，不要廉价广告感，不要多余英文，不要解释性长文案，不要普通插画，不要让大字不可读。\nGiant Chinese concept poster style: premium vertical concept poster, 3:4 or 4:5 ratio, oversized Chinese title as the dominant visual, clear complete characters, no missing strokes, no wrong characters, occupying most of the composition. The visual language is generated from the meaning of the input word: emotional tone, cultural association, hidden tension, metaphor and fate-like atmosphere. The image metaphor must interact with the giant typography: a doorway inside the characters, city hidden in the strokes, landscape visible through gaps, characters as architecture, wall, road, monument or stage, a small human figure entering or standing beneath the word. Minimal, refined, cinematic, exhibition-level, strong typography, strong metaphor, strong emotion, memorable composition. Only three small text areas: top-left keywords, vertical poetic sentence on the right, short summary line at bottom-left. No clutter, no cheap advertising, no long explanatory copy, no ordinary illustration.'
    ),
    "premium_product_ad_poster": (
        '整体风格为产品海报风：竖版高级商业广告海报，产品是绝对主角，使用高质量商业摄影或超真实 CGI 渲染，产品清晰锐利、材质真实、细节丰富、光影专业。产品占画面 35%-70%，边缘锐利、结构可信，不能被人物或文字抢走主体地位。根据产品属性自动选择最适合的广告创意方向：英雄近景、时尚巨物、极端场景、爆炸拆解、微缩人物互动或生活方式大片。画面需要具有强第一视觉、强产品质感、强卖点表达和高级品牌感。可使用巨大标题、功能卖点标注、细线说明、图标、数字信息、品牌式排版。背景干净、有设计感，色彩根据产品和品牌气质自动选择。整体像高端电商首图、科技新品发布海报、时尚杂志广告或产品工程解析图。不要廉价促销感，不要杂乱背景，不要低质 3D，不要错误产品结构，不要密集长文案，不要让人物抢走产品主体。\nPremium product advertising poster style: vertical high-impact commercial product poster, the product is the absolute hero. Hyper-realistic product photography or ultra-detailed CGI render, sharp product details, realistic materials, professional studio lighting, cinematic depth of field. Choose the most suitable creative direction based on the product: hero close-up, editorial fashion scale, extreme environment monument, exploded-view technical infographic, miniature figures interacting with oversized product, or clean lifestyle product campaign. Strong first visual, premium product texture, clear selling points, brand-level layout. Use oversized typography, feature callouts, thin annotation lines, icons, bold numbers and concise specs. Clean designed background, color palette driven by product and brand mood. High-end e-commerce hero image, tech launch poster, fashion magazine ad, or product engineering presentation. Not cheap promotion, not cluttered, not low-quality 3D, not incorrect product structure, not dense copy, product must remain dominant.'
    ),
    "cute_3d_plastic_icon": (
        "3D 新拟物风小图标：主体是圆润可爱的 3D app icon，半哑光塑料或精致树脂材质，饱满圆角、柔和轮廓、轻微倒角、干净结构。"
        "使用主色、次色、点缀色形成清晰但柔和的多色分层；等距前视角居中，浅灰或白色棚拍背景，轻柔阴影。"
        "避免软塌黏土、单色无对比、写实产品、金属、复杂细节、文字、水印和外部 logo。"
    ),
    "candy_glass_3d_icon": (
        "3D 糖果风格图标：主体像光滑糖果或磨砂半透明玻璃，圆润极简几何，低对比、清爽可爱。"
        "使用同色系粉彩主色和辅助色，带奶白细节、柔和内部模糊、边缘微光、丝滑亚克力质感；3/4 顶前视角，纯白背景，轻接触阴影。"
        "避免强色相分离、饱和色、玉石/石头/陶瓷感、不透明塑料、复杂细节、文字和水印。"
    ),
    "airbnb_soft_miniature_icon": (
        "Airbnb 风软拟物图标：主体是温暖生活方式 3D miniature，小玩具模型般的大块面、粗圆比例、柔和圆边和哑光 clay-like 表面。"
        "可加入 1-2 个简单辅助物，形成 cozy 场景；使用低饱和暖色主色、辅助色、点缀色；暖白背景、柔和棚拍灯光、轻接触阴影。"
        "避免真实产品摄影、皮革/织物/金属真实纹理、锐利反光、高细节渲染、忙乱构图、人物、文字和 logo。"
    ),
    "circular_2_5d_vector_icon": (
        "圆形轻拟物风格图标：柔和 2.5D 轴测矢量插画，像中文移动 App 金刚区功能图标。"
        "使用一个干净的圆形粉彩渐变背景作为裁切边界；主体占圆形约 72%-76%，略低于中心，使用分层矢量形状、柔和渐变、内阴影、边缘高光和清晰色块边界。"
        "不要 3D 渲染、C4D、黏土、玩具模型、真实产品、平台地面、额外前景弧、文字、标签、边框和水印。"
    ),
    "soft_frosted_glass_icon": (
        "软糖风格图标：单个独立主体置于纯白背景，整体为柔软奶霜式 glassmorphism。"
        "使用奶白半透明磨砂玻璃、层叠半透明表面、圆润边缘、轻微景深和柔和折射；主体后方有主色/辅助色的柔雾光晕，颜色透过磨砂材质扩散。"
        "避免清透硬塑料、玩具亮面、金属边、尖锐高光、真实摄影、外部容器、装饰背景、文字和多图标。"
    ),
    "circular_3d_texture_icon": (
        "环形 3D 质感图标：系统级现代 3D app icon，1:1 方形画布，白色外背景，中心是大圆形低饱和马卡龙渐变底。"
        "圆形只是平面渐变背景，不是 3D 圆盘；内部是柔软 3D 拟物主体，低饱和同色系、奶油质感、圆润厚边、必要结构简化。"
        "主体略放大并被圆形底部裁切约 15%，3/4 等距视角，柔和左上光和轻微背后阴影。避免霓虹、高对比、外圈容器、浮雕进背景、金属、文字、水印和复杂场景。"
    ),
    "frosted_glass_ui_icon": (
        "磨砂玻璃质感小图标：极简分层 UI 图标，纯白背景、居中构图、没有外框。"
        "使用重叠圆角 UI 图层或简单几何来表达主体；超大 squircle 圆角、前层约 55% 半透明磨砂覆盖，后层同色系渐变并轻微上/左偏移，边缘柔和模糊，像 CSS backdrop-filter blur。"
        "可加入一个小圆角强调色装饰点。避免黑色背景、App 外部容器、厚重 3D、亮面水晶玻璃、奶白不透明板、尖角、文字和复杂底纹。"
    ),
    "pastel_reward_badge_icon": (
        "少女风奖牌图标：可爱柔软的移动 App reward badge，紧凑居中，半扁平 2.5D 卡通 UI 风格。"
        "主体是小盾牌奖牌或圆润徽章，可有柔和翅膀丝带、底部小星星/小花章、中心大号数字或极短字；粉彩渐变从主色到辅助色，半透明珐琅质感、低对比内阴影、柔和边缘光。"
        "浅色干净背景、柔和模糊投影、1:1 画幅。避免史诗幻想、奖杯奢华感、尖锐水晶、强闪光、霓虹、厚重 3D、真实金属、暗影和复杂细节。"
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
    "isometric_modular_system": "轴测模块系统风",
    "monochrome_system_editorial": "黑白系统风",
    "isometric_timeline_miniature": "时间微缩风",
    "real_object_doodle_composite": "实物涂鸦风",
    "expressive_3d_quirky_character": "3D怪表情风",
    "giant_chinese_concept_poster": "大字海报风",
    "premium_product_ad_poster": "产品海报风",
    "cute_3d_plastic_icon": "3D 新拟物风小图标",
    "candy_glass_3d_icon": "3D 糖果风格图标",
    "airbnb_soft_miniature_icon": "Airbnb 风软拟物图标",
    "circular_2_5d_vector_icon": "圆形轻拟物风格图标",
    "soft_frosted_glass_icon": "软糖风格图标",
    "circular_3d_texture_icon": "环形 3D 质感图标",
    "frosted_glass_ui_icon": "磨砂玻璃质感小图标",
    "pastel_reward_badge_icon": "少女风奖牌图标",
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
    "轴测模块图",
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
    placement: str = ""
    core_idea: str = ""
    visual_anchor: str = ""
    shot_type: str = ""
    suggested_elements: str = ""
    short_labels: str = ""
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
    character_profile: str = ""
    outfit: str = ""
    expression: str = ""
    props: str = ""
    short_phrase: str = ""
    background_color: str = ""
    product_name: str = ""
    product_category: str = ""
    product_texture: str = ""
    creative_direction: str = ""
    brand_mood: str = ""
    color_palette: str = ""
    selling_point1: str = ""
    selling_point2: str = ""
    selling_point3: str = ""
    selling_point4: str = ""
    selling_point5: str = ""
    style_id: str = DEFAULT_STYLE_ID


@dataclass
class IconSpec:
    subject: str
    title: str = ""
    primary_color: str = "低饱和品牌主色"
    secondary_color: str = "柔和辅助色"
    accent_color: str = "少量点缀色"
    auxiliary_objects: str = ""
    scene_theme: str = ""
    core_feature: str = ""
    number: str = ""
    style_id: str = "cute_3d_plastic_icon"


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
    placement: str = ""
    core_idea: str = ""
    visual_anchor: str = ""
    shot_type: str = ""
    suggested_elements: str = ""
    short_labels: str = ""
    feedback_loop: str = ""
    risk_label: str = ""
    character_profile: str = ""
    outfit: str = ""
    expression: str = ""
    props: str = ""
    short_phrase: str = ""
    background_color: str = ""
    product_name: str = ""
    product_category: str = ""
    product_texture: str = ""
    creative_direction: str = ""
    brand_mood: str = ""
    color_palette: str = ""
    selling_point1: str = ""
    selling_point2: str = ""
    selling_point3: str = ""
    selling_point4: str = ""
    selling_point5: str = ""
    style_id: str = DEFAULT_STYLE_ID


def normalize_style(style_id: str | None) -> str:
    style_id = (style_id or DEFAULT_STYLE_ID).strip()
    if style_id not in STYLE_ANCHORS:
        raise ValueError(f"未知 style_id: {style_id}. 可用值: {', '.join(STYLE_ANCHORS)}")
    return style_id


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def infer_logo_icon_style(raw: Dict[str, Any]) -> str:
    text = " ".join(str(value) for value in raw.values() if isinstance(value, (str, int, float))).lower()
    if _contains_any(text, ("少女", "女孩", "儿童", "奖牌", "徽章", "勋章", "badge", "reward", "medal", "number", "数字")):
        return "pastel_reward_badge_icon"
    if _contains_any(text, ("金刚区", "支付宝", "淘宝", "盒马", "2.5d", "2.5d", "矢量", "vector", "圆形轻拟物")):
        return "circular_2_5d_vector_icon"
    if _contains_any(text, ("环形", "圆形背景", "圆形遮罩", "圆形底", "圆盘", "system-level", "系统级")):
        return "circular_3d_texture_icon"
    if _contains_any(text, ("airbnb", "民宿", "露营", "旅行", "背包", "帐篷", "吐司", "厨房", "生活方式", "cozy")):
        return "airbnb_soft_miniature_icon"
    if _contains_any(text, ("ui", "圆角", "卡片", "文件夹", "钱包", "磨砂玻璃质感", "backdrop", "squircle")):
        return "frosted_glass_ui_icon"
    if _contains_any(text, ("软糖", "奶霜", "奶冻", "milky", "frosted glass", "glassmorphism", "毛玻璃", "半透明", "透明", "玻璃")):
        return "soft_frosted_glass_icon"
    if _contains_any(text, ("糖果", "candy", "低对比", "清爽", "果冻")):
        return "candy_glass_3d_icon"
    return "cute_3d_plastic_icon"


def is_logo_icon_request(raw: Dict[str, Any]) -> bool:
    text = " ".join(str(value) for value in raw.values() if isinstance(value, (str, int, float))).lower()
    return _contains_any(text, ("logo", "图标", "小图标", "app icon", "icon", "功能入口", "功能图标"))


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
    flow_action = spec.flow_action or spec.character_action or "小黑把素材塞进一台怪机器，拉动判断杆，再把结果推向输出口"
    core_structure = spec.core_structure or spec.metaphor or "输入 → 判断 → 处理 → 输出 → 反馈"
    node1 = spec.node1 or "输入"
    node2 = spec.node2 or "判断"
    node3 = spec.node3 or "处理"
    node4 = spec.node4 or "输出"
    feedback_loop = spec.feedback_loop or "输出反馈回到输入"
    risk_label = spec.risk_label or "别乱跑"
    core_idea = spec.core_idea or spec.bottom_sentence or "把复杂流程变成一个可执行的动作"
    visual_anchor = spec.visual_anchor or "输入输出闭环 / 分流判断 / 卡住到跑起来"
    shot_type = spec.shot_type or "Workflow / 系统局部 / 概念隐喻"
    suggested_elements = spec.suggested_elements or spec.elements or "旧机器、文件、门、输出卡片、虚线回路"
    short_labels = spec.short_labels or f"{node1} / {node2} / {node3} / {node4} / {risk_label}"
    return f"""请生成一张怪诞小人风的中文封面图。
主题是「{spec.title}」。画面使用纯白背景、大量留白、黑色细线手绘和少量红蓝橙标注，整体像轻松怪诞的工作流封面或产品系统草图。
这张图只表达一个认知锚点：「{visual_anchor}」。核心意思是：「{core_idea}」。不要平均铺开多个观点。
版式不固定，不要固定左标题右图；根据核心动作选择合适构图：「{shot_type}」。可以是 Workflow、系统局部、前后对比、角色状态、概念隐喻、方法分层、地图路线或小漫画分镜。
标题「{spec.title}」和副标题「{spec.subtitle}」只作为简短封面文字，放在留白区域，不要做成 PPT 标题栏。
画面中必须有一个怪诞小黑角色（参考 assets/examples/xiaohei/ 的小黑角色 DNA，不复制样图）：黑色实心不规则小怪物，白色圆点眼睛，细胳膊细腿，空表情、认真但有点荒诞。小黑正在执行核心动作：「{flow_action}」。如果去掉小黑后画面隐喻仍完整，就说明小黑太装饰，必须让它承担动作。
请把内容组织成一个清晰但不正式的结构：「{core_structure}」。节点只保留：「{node1}」「{node2}」「{node3}」「{node4}」。建议元素：「{suggested_elements}」。短标注：「{short_labels}」。每个标注 2-8 个字，最多 5-8 处。
用橙色表示主流程或移动路径；用蓝色虚线表示反馈回路：「{feedback_loop}」；用红色标注关键风险或判断：「{risk_label}」。底部可写很短的判断句：「{spec.bottom_sentence}」。
不要写“流程图 / 系统架构 / 常见坑 / 路线图”等类型标题。不要画成正式流程图、课程页、复杂架构图或儿童卡通。
{STYLE_ANCHORS['quirky_doodle_character_flow']}"""


def render_quirky_doodle_body(spec: BodySpec) -> str:
    core_idea = spec.core_idea or spec.bottom_sentence or "这张图要表达文章中的一个关键判断"
    visual_anchor = spec.visual_anchor or spec.structure or "核心判断 / 断点 / 输入输出 / 分流 / 对比 / 承接 / 常见坑 / 状态变化"
    shot_type = spec.shot_type or spec.structure or "Workflow / 系统局部 / 概念隐喻"
    suggested_elements = spec.suggested_elements or spec.modules or "旧机器、纸箱、抽屉、漏斗、门、文件、路径线"
    short_labels = spec.short_labels or spec.notes or spec.modules
    feedback_loop = spec.feedback_loop or "反馈回流"
    risk_label = spec.risk_label or "关键判断"
    return f"""请生成一张怪诞小人风的中文正文配图。
这是一张独立的 16:9 横版文章配图，主题是「{spec.title}」。画面必须是纯白背景、大量留白、黑色细线手绘，整体像轻松怪诞的产品工作流草图，而不是 PPT 或正式流程图。
这张图只表达一个认知锚点：「{visual_anchor}」。核心意思是：「{core_idea}」。不要把多个段落或多个观点塞进同一张图。
版式不固定，根据内容动作选择一种结构：「{shot_type}」。可用 Workflow、系统局部、前后对比、角色状态、概念隐喻、方法分层、地图路线或小漫画分镜；不要把结构类型写在画面上。
画面中必须有小黑（参考 assets/examples/xiaohei/ 的小黑角色 DNA，不复制样图）：一个黑色实心不规则小怪物，白色圆点眼睛，细胳膊细腿，空表情、认真、冷幽默。小黑正在「{spec.character_action}」。小黑必须承担核心动作，不是站在角落看图。
把抽象概念转成一个物理动作或低科技物件：卡住、漏掉、变重、分拣、沉淀、发酵、开门、折叠、拆包、回流；可使用纸箱、抽屉、旧机器、漏斗、秤、邮筒、门、井、梯子、水管、线团、闸门、怪表盘等。建议元素：「{suggested_elements}」。
画面只保留 3-5 个主要元素。中文手写短标注为：「{short_labels}」。每处 2-8 个字，最多 5-8 处。
颜色规则：黑色用于主体线稿和小黑；橙色用于主流程、路径或箭头；蓝色虚线用于反馈或系统状态：「{feedback_loop}」；红色只用于问题、风险或关键判断：「{risk_label}」。底部判断句：「{spec.bottom_sentence}」。
主体约占画面 40%-60%，至少 35% 空白。不要写左上角大标题，不要写“工作流/系统架构/常见坑/路线图”等类型标题，不要真实 UI 截图，不要纸纹、米色背景、渐变、复杂阴影或密集文字。
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
    "quirky_doodle_character_flow": "纯白背景、大量留白，黑色细线手绘怪诞小黑角色承担核心动作；先抓文章认知锚点，再用旧机器、纸箱、抽屉、漏斗、门、路径线、橙色主流程、蓝色反馈和红色风险标注，讲清 AI 工作流或系统卡点。",
    "minimal_line_art": "纯白或暖白背景，大量留白，用极简黑色连续线条或少量克制轮廓线表现人物、关系、城市、旅行、课堂、灵感灯泡或抽象符号；只加入极少点缀色，整体优雅克制。",
    "isometric_modular_system": "统一等距/轴测视角，远近不缩放，模块化平台、路径、楼层、管道、信息卡片和微型人物共同构成系统、流程、地图或服务架构说明。",
    "monochrome_system_editorial": "黑白灰高对比，巨型粗体中文或英文字压场，配合档案盒、索引卡、锁、阶梯、门、路径线、路线图、货船、集装箱或微缩人物，并加入细线网格、编号、条形码和工业化信息排版。",
    "isometric_timeline_miniature": "45° 等距俯视视角，横向展开的微型 3D 时间轴展台，底座分成 4-6 个时代区域；每段有代表物件、技术或环境，并加入少量微型人物互动；顶部标题、副标题和极简时间轴图标清晰呈现从过去到现代的演化。",
    "real_object_doodle_composite": "干净白色或暖白纸张背景，一个真实日常物品作为关键语义零件，与黑色手绘线稿角色无缝结合；物品变成头、头发、大脑、身体、负担、心脏、道具或爆炸，制造幽默易懂的视觉双关。",
    "expressive_3d_quirky_character": "极简白色、浅灰或浅米色背景，一个圆润夸张的 3D 小人作为主视觉；用准确夸张的表情和肢体动作表达情绪、态度、吐槽、状态或轻剧情。",
    "giant_chinese_concept_poster": "竖版 3:4 或 4:5，高级中文概念海报；巨型中文词作为绝对主体，词义驱动字体、隐喻场景、人物命运感和三处克制小字。",
    "premium_product_ad_poster": "竖版高端商业广告海报，产品是绝对主角；用超清产品质感、巨大标题、功能卖点标注、创意场景或爆炸拆解制造品牌感和转化力。",
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



def render_expressive_3d_quirky_cover(spec: CoverSpec) -> str:
    background = spec.background_color or spec.background or "浅灰或暖白"
    character = spec.character_profile or "一个圆润夸张的 3D 小人，头大身小，脸颊饱满，皮肤柔软"
    outfit = spec.outfit or "简单纯色 T 恤或基础服装"
    expression = spec.expression or spec.emotion or "无语、怀疑或认真吐槽"
    action = spec.character_action or "双手摊开，身体微微后仰，像在表达一个明确态度"
    props = spec.props or spec.elements or "提示词卡片、文件、按钮、放大镜、工具箱或小旗子"
    phrase = spec.short_phrase or spec.speech_bubble or spec.bottom_sentence[:8] or "别乱来"
    viewpoint = spec.metaphor_meaning or spec.metaphor or spec.bottom_sentence or "把抽象观点变成一个有传播感的角色反应"
    return f"""请生成一张3D怪表情风的中文封面图。
主题是「{spec.title}」。画面背景为{background}，大量留白，整体像高质量 3D 表情包角色或 3D 版怪诞小人风。
标题「{spec.title}」使用清晰粗体中文字体，副标题「{spec.subtitle}」更小、更轻，放在留白区域，不要做成复杂信息页。
画面主体是{character}，穿着「{outfit}」。角色表情是「{expression}」，要通过眼神、眉毛、嘴角、脸颊和头部姿态夸张表达。
角色动作是：「{action}」。这个动作要表达「{viewpoint}」，肢体语言清楚、有戏剧性、有一点搞怪，但不要失控。
可以加入少量道具或流程元素：「{props}」。道具只辅助表达，不要抢角色。
如需文字，只加入一句很短的手写或粗体短句：「{phrase}」。文字不要超过 8 个字，像表情包吐槽或封面提示。
参考 assets/examples/3d_quirky/ 的角色质感、表情强度、动作夸张度和极简背景；不要照抄样图人物、服装、构图或道具。
{STYLE_ANCHORS['expressive_3d_quirky_character']}"""


def render_expressive_3d_quirky_body(spec: BodySpec) -> str:
    background = spec.background_color or "白色、浅灰或浅米色"
    character = spec.character_profile or "一个圆润夸张的 3D 小人，头大身小，脸颊饱满，皮肤柔软"
    outfit = spec.outfit or "简单纯色 T 恤或基础服装"
    expression = spec.expression or spec.risk_label or spec.visual_anchor or "无语、焦虑、疲惫或震惊"
    action = spec.character_action or "用夸张动作表达当前状态"
    props = spec.props or spec.suggested_elements or spec.modules or "电脑、提示词卡片、文件、按钮、放大镜、工具箱、纸张或流程节点"
    phrase = spec.short_phrase or spec.speech_bubble or spec.bottom_sentence[:8] or "又卡住了"
    idea = spec.core_idea or spec.bottom_sentence or spec.notes or "把一个情绪、观点或流程节点变成角色反应"
    return f"""请生成一张3D怪表情风的角色配图。
主题是「{spec.title}」。画面使用极简 {background} 背景，大量留白，整体像高质量 3D 表情包角色或 3D 版怪诞小人风。
画面中有{character}，穿着「{outfit}」。角色的表情是「{expression}」，要通过眼神、眉毛、嘴角、脸颊和头部姿态夸张表达。
角色正在做动作：「{action}」。这个动作要表达「{idea}」。肢体语言要清楚、有戏剧性、有一点搞怪，但不要失控。
可以加入少量道具：「{props}」。道具只辅助表达，不要抢角色。
如果需要文字，在旁边加入一句很短的手写或粗体短句：「{phrase}」。文字不要超过 8 个字，像表情包吐槽或正文配图提示。
画面只表达一个状态、态度、吐槽、反应或轻剧情节点；不要把复杂流程、长段文字或多层知识卡塞进一张图。
参考 assets/examples/3d_quirky/ 的角色质感、表情强度、动作夸张度和极简背景；不要照抄样图人物、服装、构图或道具。
{STYLE_ANCHORS['expressive_3d_quirky_character']}"""


def render_giant_chinese_concept_poster_cover(spec: CoverSpec) -> str:
    input_text = spec.main_visual_text or spec.title
    keywords = spec.short_labels or spec.label1 or spec.speech_bubble or "关键词 情绪 命运"
    fate_sentence = spec.label2 or spec.subtitle or "让这个词像一道命运入口。"
    summary = spec.label3 or spec.bottom_sentence or "一个词，打穿一种情绪。"
    metaphor = spec.metaphor or spec.visual_anchor or "让巨大中文字成为空间本身，人物或光从字中穿过"
    color_mood = spec.background or spec.texture_keywords or spec.emotion or "根据词义自动选择高级、节制的色彩气质"
    font_mood = spec.specified_material or spec.core_structure or "根据词义自动选择厚重书法、碑刻、工业粗体、纸质肌理、石质墙体、光影字或极简几何字"
    subject = spec.core_subject or spec.character_action or "一个极小的人物或象征物，与大字发生关系"
    return f"""请生成一张大字海报风的高级中文概念海报。
画幅：竖版 3:4。核心文字为「{input_text}」。
请先深度理解「{input_text}」的表层含义、深层寓意、情绪气质、文化联想、人物命运感与隐含张力，再决定最适合它的画面风格、构图方式、色彩气质和视觉隐喻。
画面中，巨大中文主标题「{input_text}」必须是绝对主体，字形清晰完整，无错字无缺笔，占据画面 45%-75%，形成最强第一视觉。字体气质：「{font_mood}」。字体必须高级、克制、有力量，不能变形到不可读。
请提炼一个最准确、最有代表性的视觉隐喻：「{metaphor}」。让人物、物体、空间或象征元素与大字发生关系，例如字中开门、字里藏城市、字的缝隙透出风景、字像建筑、字像墙、字像路、字被光穿透、人物站在字下或走入字中。主体或人物：「{subject}」。隐喻图像是第二视觉，不要抢走大字主体。
整体色彩：「{color_mood}」。色彩根据词义自动调整，但必须高级、节制，可以更冷峻、更诗意、更悲剧、更锋利、更温柔或更庄严。
小字文案只保留三处：
左上角：「{keywords}」
右侧竖排：「{fate_sentence}」
左下角：「{summary}」
文字是第一视觉，隐喻图像是第二视觉，小字是第三视觉。元素少，概念准，留白克制。最终效果像展览级文学人物或概念主题海报，把「{input_text}」背后的精神状态和文化意味真正视觉化。
不要拥挤，不要廉价广告感，不要多余英文，不要解释性长文案，不要普通插画，不要只画人物外貌，不要让大字不可读。
{STYLE_ANCHORS['giant_chinese_concept_poster']}"""


def render_giant_chinese_concept_poster_body(spec: BodySpec) -> str:
    input_text = spec.title
    keywords = spec.short_labels or spec.notes or "关键词 情绪 命运"
    fate_sentence = spec.subtitle or spec.speech_bubble or "让这个词像一道命运入口。"
    summary = spec.bottom_sentence or "一个词，打穿一种情绪。"
    metaphor = spec.visual_anchor or spec.core_idea or spec.modules or "让巨大中文字成为空间本身，人物或光从字中穿过"
    return f"""请生成一张大字海报风的高级中文概念海报。
画幅：竖版 3:4。核心文字为「{input_text}」。
这不是正文解释图，不要做流程图或知识卡片；只用一个中文词打穿一种情绪。
巨大中文主标题「{input_text}」必须清晰完整、无错字、无缺笔，占据画面 45%-75%。
视觉隐喻：「{metaphor}」。让人物、物体、空间或象征元素与大字发生关系，例如字中开门、字里藏城市、字的缝隙透出风景、字像建筑、字像墙、字像路、人物站在字下或走入字中。
小字文案只保留三处：左上角「{keywords}」；右侧竖排「{fate_sentence}」；左下角「{summary}」。
整体高级、极简、克制、展览级，有强排版、强隐喻、强情绪、强记忆点。不要拥挤，不要长文案，不要普通插画，不要让大字不可读。
{STYLE_ANCHORS['giant_chinese_concept_poster']}"""


def _product_selling_points(spec: CoverSpec | BodySpec) -> list[str]:
    points = [spec.selling_point1, spec.selling_point2, spec.selling_point3, spec.selling_point4, spec.selling_point5]
    fallback = []
    if hasattr(spec, "short_labels") and getattr(spec, "short_labels"):
        fallback = [p.strip() for p in str(getattr(spec, "short_labels")).replace("、", "/").split("/") if p.strip()]
    if not any(points) and hasattr(spec, "label1"):
        points = [getattr(spec, "label1", ""), getattr(spec, "label2", ""), getattr(spec, "label3", ""), getattr(spec, "label4", ""), ""]
    merged = [p for p in points if p] or fallback or ["核心卖点", "高级质感", "清晰功能", "品牌体验"]
    return merged[:5]


def render_premium_product_ad_poster_cover(spec: CoverSpec) -> str:
    product = spec.product_name or spec.title
    category = spec.product_category or spec.core_object or "根据产品名称自动判断品类"
    texture = spec.product_texture or spec.texture_keywords or "根据产品自动突出金属、玻璃、皮革、织物、水珠、屏幕、透明材质或柔软填充等关键质感"
    direction = spec.creative_direction or spec.shot_type or "根据产品属性自动选择英雄近景 / 时尚巨物 / 极端场景 / 爆炸拆解 / 微缩互动 / 生活方式大片"
    metaphor = spec.metaphor or spec.visual_anchor or "让产品卖点自然变成高级广告视觉创意"
    headline = spec.main_visual_text or spec.title
    subtitle = spec.subtitle or "Premium Product Campaign"
    brand_mood = spec.brand_mood or spec.emotion or "根据产品自动选择科技、奢华、运动、年轻、极简、户外、未来或温柔气质"
    color = spec.color_palette or spec.background or spec.texture_keywords or "产品颜色和品牌色优先，背景服务产品，强调色只用于引导视线"
    points = _product_selling_points(spec)
    point_lines = "\n".join(f"{i + 1}. {point}" for i, point in enumerate(points))
    return f"""请生成一张产品海报风的竖版高级商业广告海报。
产品是「{product}」。产品品类：「{category}」。如果提供了产品图片，请识别并保留产品主体的外观、颜色、结构、材质和关键特征，并基于它进行创意广告海报设计；不要随意改变产品品类或关键结构。
画面中产品必须是绝对主角，清晰锐利，占据画面 35%-70% 的主要视觉位置。产品材质要真实、有高级感，突出「{texture}」。
请根据产品属性自动选择最适合的广告创意方向：「{direction}」。可以是英雄近景、时尚巨物、极端场景、爆炸拆解、微缩人物互动或生活方式大片。不要机械套模板，要让产品卖点自然变成视觉创意。
核心视觉隐喻是：「{metaphor}」。让产品与人物、空间、环境或功能卖点发生强关系，形成高级、记忆点强、有商业转化力的画面。
画面标题为「{headline}」，使用巨大、干净、有冲击力的无衬线字体，可以放在背景层并被产品部分遮挡。副标题为「{subtitle}」。
请加入 {len(points)} 个简短卖点信息：
{point_lines}
卖点用小图标、细线标注、数字模块或简洁信息块呈现，不要长篇解释。
品牌气质：「{brand_mood}」。色彩倾向：「{color}」。专业棚拍光线，产品高光自然，背景干净，整体高级、清爽、有视觉冲击力。
不要廉价促销感，不要杂乱背景，不要低质量 3D，不要错误产品结构，不要密集长文案，不要让人物抢走产品主体。
{STYLE_ANCHORS['premium_product_ad_poster']}"""


def render_premium_product_ad_poster_body(spec: BodySpec) -> str:
    product = spec.product_name or spec.title
    category = spec.product_category or spec.structure or "产品卖点图"
    texture = spec.product_texture or spec.modules or "突出产品真实材质和关键细节"
    direction = spec.creative_direction or spec.shot_type or "英雄近景 / 爆炸拆解 / 微缩互动 / 生活方式大片"
    metaphor = spec.visual_anchor or spec.core_idea or "让产品卖点自然变成视觉创意"
    points = _product_selling_points(spec)
    point_lines = "\n".join(f"{i + 1}. {point}" for i, point in enumerate(points))
    return f"""请生成一张产品海报风的竖版高级商业广告海报。
产品是「{product}」。产品品类：「{category}」。这不是正文知识卡或流程图，产品必须是绝对主角。
产品清晰锐利，占据画面 35%-70% 的主要视觉位置，材质真实可信，突出「{texture}」。
广告创意方向：「{direction}」。核心视觉隐喻：「{metaphor}」。让产品与人物、空间、环境或功能卖点发生强关系。
画面标题为「{product}」或一句短广告语，使用巨大、干净、有冲击力的字体；副标题或短句为「{spec.bottom_sentence}」。
请加入简短卖点信息：
{point_lines}
卖点用小图标、细线标注、数字模块或简洁信息块呈现，不要长篇解释。
背景干净、有设计感，色彩根据产品和品牌气质自动选择。整体像高端电商首图、科技新品发布海报、时尚杂志广告或产品工程解析图。
不要廉价促销感，不要杂乱背景，不要低质量 3D，不要错误产品结构，不要密集长文案，不要让人物抢走产品主体。
{STYLE_ANCHORS['premium_product_ad_poster']}"""


def render_icon(spec: IconSpec) -> str:
    spec.style_id = normalize_style(spec.style_id)
    auxiliary = spec.auxiliary_objects or "必要时加入 1-2 个简单辅助物，但不能抢主体"
    scene_theme = spec.scene_theme or "干净、友好、可作为 App / 产品图标使用"
    core_feature = spec.core_feature or "主体轮廓一眼可识别"
    if spec.style_id == "pastel_reward_badge_icon":
        number = spec.number or "1"
        content_rule = f"中心允许出现一个大号数字「{number}」，除此之外不要出现文字。"
    else:
        content_rule = "不要出现文字、字母、品牌名、标签或水印；如果用户要 logo，也只生成图标化视觉符号。"
    return f"""请生成一个 1:1 方形 logo / 图标模式图像。
主体：{spec.subject}。
使用场景：{scene_theme}。
辅助元素：{auxiliary}。
核心识别特征：{core_feature}。
配色：主色为 {spec.primary_color}，辅助色为 {spec.secondary_color}，点缀色为 {spec.accent_color}。
构图要求：单个主体，居中，留白干净，适合缩小到 App icon、功能图标或产品 logo 使用；主体边界清楚，不要复杂背景，不要多主体拼贴。
文字规则：{content_rule}
{STYLE_ANCHORS[spec.style_id]}"""


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
    if spec.style_id == "expressive_3d_quirky_character":
        return render_expressive_3d_quirky_cover(spec)
    if spec.style_id == "giant_chinese_concept_poster":
        return render_giant_chinese_concept_poster_cover(spec)
    if spec.style_id == "premium_product_ad_poster":
        return render_premium_product_ad_poster_cover(spec)
    if spec.style_id == "isometric_modular_system":
        return render_extra_cover(spec) or render_handdrawn_cover(spec)
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
    if spec.style_id == "expressive_3d_quirky_character":
        return render_expressive_3d_quirky_body(spec)
    if spec.style_id == "giant_chinese_concept_poster":
        return render_giant_chinese_concept_poster_body(spec)
    if spec.style_id == "premium_product_ad_poster":
        return render_premium_product_ad_poster_body(spec)
    # Cover/editorial styles are not ideal for body diagrams; still render a sparse editorial visual if explicitly requested.
    return f"""请生成一张中文知识视觉图，主题是「{spec.title}」。
画面不要做成密集正文解释图，只保留少量核心概念。核心模块包括：「{spec.modules}」。必要注释：「{spec.notes}」。
底部写一句判断式结论：「{spec.bottom_sentence}」。
{STYLE_ANCHORS[spec.style_id]}"""


def build_image_item(raw: Dict[str, Any], index: int) -> Dict[str, Any]:
    raw = dict(raw)
    image_type = raw.get("type")
    if not image_type and is_logo_icon_request(raw):
        image_type = "icon"
    if image_type in {"icon", "logo"}:
        style_id = normalize_style(raw.get("style_id") or raw.get("style") or infer_logo_icon_style(raw))
    else:
        style_id = normalize_style(raw.get("style_id") or raw.get("style") or DEFAULT_STYLE_ID)
    if image_type in {"icon", "logo"}:
        subject = raw.get("subject") or raw.get("主体") or raw.get("core_subject") or raw.get("product_name") or raw.get("title") or "抽象品牌符号"
        spec = IconSpec(
            subject=str(subject),
            title=raw.get("title", ""),
            primary_color=raw.get("primary_color") or raw.get("主色") or raw.get("color_palette") or "低饱和品牌主色",
            secondary_color=raw.get("secondary_color") or raw.get("辅助色") or "柔和辅助色",
            accent_color=raw.get("accent_color") or raw.get("点缀色") or "少量点缀色",
            auxiliary_objects=raw.get("auxiliary_objects") or raw.get("辅助物") or raw.get("elements") or "",
            scene_theme=raw.get("scene_theme") or raw.get("场景") or raw.get("brand_mood") or "",
            core_feature=raw.get("core_feature") or raw.get("核心识别特征") or raw.get("visual_anchor") or "",
            number=str(raw.get("number") or raw.get("数字") or ""),
            style_id=style_id,
        )
        return {
            "id": raw.get("id") or f"icon_{index:02d}",
            "type": "icon",
            "aspect_ratio": raw.get("aspect_ratio") or "1:1",
            "style_id": style_id,
            "style_name": STYLE_NAMES[style_id],
            "title": raw.get("title") or spec.subject,
            "subject": spec.subject,
            "prompt": render_icon(spec),
        }
    if image_type == "cover":
        if style_id == "giant_chinese_concept_poster":
            raw.setdefault("subtitle", raw.get("fate_sentence") or raw.get("命运感短句") or "让一个词成为画面的命运入口")
            raw.setdefault("metaphor", raw.get("visual_metaphor") or raw.get("视觉隐喻") or raw.get("visual_anchor") or "巨大中文字成为空间本身，人物或光从字中穿过")
            raw.setdefault("elements", raw.get("subject") or raw.get("人物或主体") or raw.get("core_subject") or "极小人物、光、门、城市、风景或裂缝")
            raw.setdefault("character_action", raw.get("subject") or raw.get("人物或主体") or "人物与巨型中文大字发生关系")
            raw.setdefault("speech_bubble", raw.get("keywords") or raw.get("关键词") or raw.get("short_labels") or "关键词 情绪 命运")
            raw.setdefault("bottom_sentence", raw.get("summary_sentence") or raw.get("总结句") or "一个词，打穿一种情绪。")
        if style_id == "premium_product_ad_poster":
            raw.setdefault("subtitle", raw.get("subtitle") or raw.get("副标题") or "Premium Product Campaign")
            raw.setdefault("metaphor", raw.get("visual_metaphor") or raw.get("视觉隐喻") or "让产品卖点自然变成高级广告视觉创意")
            raw.setdefault("elements", raw.get("props") or raw.get("product_features") or raw.get("产品卖点") or "产品、功能标注、细线说明、品牌背景")
            raw.setdefault("character_action", raw.get("creative_direction") or raw.get("创意方向") or "产品作为绝对主角")
            raw.setdefault("speech_bubble", raw.get("selling_point1") or raw.get("卖点1") or "核心卖点")
            raw.setdefault("bottom_sentence", raw.get("summary_sentence") or raw.get("slogan") or raw.get("副标题") or "让产品一眼被记住。")
        raw.setdefault("metaphor", raw.get("visual_anchor") or raw.get("core_structure") or raw.get("core_idea", ""))
        raw.setdefault("elements", raw.get("suggested_elements", ""))
        raw.setdefault("character_action", raw.get("main_action") or raw.get("flow_action", ""))
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
            specified_material=raw.get("specified_material") or raw.get("font_mood") or raw.get("字体气质", ""),
            texture_keywords=raw.get("texture_keywords") or raw.get("color_mood") or raw.get("色彩气质", ""),
            background=raw.get("background") or raw.get("color_mood") or raw.get("色彩气质", ""),
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
            placement=raw.get("placement", ""),
            core_idea=raw.get("core_idea", ""),
            visual_anchor=raw.get("visual_anchor", ""),
            shot_type=raw.get("shot_type") or raw.get("structure_type", ""),
            suggested_elements=raw.get("suggested_elements", ""),
            short_labels=raw.get("short_labels", ""),
            core_subject=raw.get("core_subject") or raw.get("subject") or raw.get("人物或主体", ""),
            relation_action=raw.get("relation_action") or raw.get("action", ""),
            accent_element=raw.get("accent_element", ""),
            line_type=raw.get("line_type", ""),
            emotion=raw.get("emotion", ""),
            main_visual_text=raw.get("main_visual_text") or raw.get("hero_text") or raw.get("primary_text") or raw.get("input_text") or raw.get("输入文字", ""),
            label1=raw.get("label1") or raw.get("keywords") or raw.get("关键词", ""),
            label2=raw.get("label2") or raw.get("fate_sentence") or raw.get("命运感短句", ""),
            label3=raw.get("label3") or raw.get("summary_sentence") or raw.get("总结句", ""),
            label4=raw.get("label4", ""),
            stage1=raw.get("stage1", ""),
            stage2=raw.get("stage2", ""),
            stage3=raw.get("stage3", ""),
            stage4=raw.get("stage4", ""),
            serial_number=raw.get("serial_number") or raw.get("number", ""),
            date_info=raw.get("date_info") or raw.get("date", ""),
            english_title=raw.get("english_title", ""),
            character_profile=raw.get("character_profile") or raw.get("character") or raw.get("role", ""),
            outfit=raw.get("outfit") or raw.get("clothing", ""),
            expression=raw.get("expression") or raw.get("emotion", ""),
            props=raw.get("props") or raw.get("prop") or raw.get("elements", ""),
            short_phrase=raw.get("short_phrase") or raw.get("caption") or raw.get("speech_bubble", ""),
            background_color=raw.get("background_color") or raw.get("background", ""),
            product_name=raw.get("product_name") or raw.get("产品名称") or raw.get("title", ""),
            product_category=raw.get("product_category") or raw.get("产品品类", ""),
            product_texture=raw.get("product_texture") or raw.get("核心材质或质感") or raw.get("texture", ""),
            creative_direction=raw.get("creative_direction") or raw.get("创意方向") or raw.get("shot_type", ""),
            brand_mood=raw.get("brand_mood") or raw.get("品牌气质", ""),
            color_palette=raw.get("color_palette") or raw.get("色彩倾向", ""),
            selling_point1=raw.get("selling_point1") or raw.get("卖点1", ""),
            selling_point2=raw.get("selling_point2") or raw.get("卖点2", ""),
            selling_point3=raw.get("selling_point3") or raw.get("卖点3", ""),
            selling_point4=raw.get("selling_point4") or raw.get("卖点4", ""),
            selling_point5=raw.get("selling_point5") or raw.get("卖点5", ""),
            style_id=style_id,
        )
        return {
            "id": raw.get("id") or f"cover_{index:02d}",
            "type": "cover",
            "aspect_ratio": raw.get("aspect_ratio") or ("3:4" if style_id == "giant_chinese_concept_poster" else ("4:5" if style_id == "premium_product_ad_poster" else "21:9")),
            "style_id": style_id,
            "style_name": STYLE_NAMES[style_id],
            "title": spec.title,
            "subtitle": spec.subtitle,
            "prompt": render_cover(spec),
        }
    if image_type == "body":
        raw.setdefault("modules", raw.get("suggested_elements", ""))
        raw.setdefault("notes", raw.get("short_labels", ""))
        raw.setdefault("character_action", raw.get("main_action") or raw.get("flow_action", ""))
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
            placement=raw.get("placement", ""),
            core_idea=raw.get("core_idea", ""),
            visual_anchor=raw.get("visual_anchor", ""),
            shot_type=raw.get("shot_type") or raw.get("structure_type", ""),
            suggested_elements=raw.get("suggested_elements", ""),
            short_labels=raw.get("short_labels", ""),
            feedback_loop=raw.get("feedback_loop", ""),
            risk_label=raw.get("risk_label", ""),
            character_profile=raw.get("character_profile") or raw.get("character") or raw.get("role", ""),
            outfit=raw.get("outfit") or raw.get("clothing", ""),
            expression=raw.get("expression") or raw.get("emotion", ""),
            props=raw.get("props") or raw.get("prop") or raw.get("modules", ""),
            short_phrase=raw.get("short_phrase") or raw.get("caption") or raw.get("speech_bubble", ""),
            background_color=raw.get("background_color") or raw.get("background", ""),
            product_name=raw.get("product_name") or raw.get("产品名称") or raw.get("title", ""),
            product_category=raw.get("product_category") or raw.get("产品品类", ""),
            product_texture=raw.get("product_texture") or raw.get("核心材质或质感") or raw.get("texture", ""),
            creative_direction=raw.get("creative_direction") or raw.get("创意方向") or raw.get("shot_type", ""),
            brand_mood=raw.get("brand_mood") or raw.get("品牌气质", ""),
            color_palette=raw.get("color_palette") or raw.get("色彩倾向", ""),
            selling_point1=raw.get("selling_point1") or raw.get("卖点1", ""),
            selling_point2=raw.get("selling_point2") or raw.get("卖点2", ""),
            selling_point3=raw.get("selling_point3") or raw.get("卖点3", ""),
            selling_point4=raw.get("selling_point4") or raw.get("卖点4", ""),
            selling_point5=raw.get("selling_point5") or raw.get("卖点5", ""),
            style_id=style_id,
        )
        return {
            "id": raw.get("id") or f"body_{index:02d}",
            "type": "body",
            "aspect_ratio": raw.get("aspect_ratio") or ("3:4" if style_id == "giant_chinese_concept_poster" else ("4:5" if style_id == "premium_product_ad_poster" else "16:9")),
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
    assert is_logo_icon_request({"title": "生成一个 AI 笔记 App logo"})
    assert not is_logo_icon_request({"title": "写一个品牌 slogan 海报"})
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
            {
                "type": "body",
                "style_id": "quirky_doodle_character_flow",
                "title": "AI 内容工作流",
                "structure": "Workflow",
                "modules": "信息源、判断机器、内容卡片、承接口",
                "notes": "信息源 / 判断 / 输出 / 回流",
                "character_action": "把素材塞进旧机器，拉动判断杆，再推着输出卡片跑向门口",
                "speech_bubble": "跑起来",
                "bottom_sentence": "系统不是一次搭好，而是在回流里变稳。",
                "core_idea": "从混乱素材到稳定输出，需要一个可回流的判断机器",
                "visual_anchor": "输入输出闭环",
                "shot_type": "Workflow",
                "feedback_loop": "用户反馈回到信息源",
                "risk_label": "别乱写",
            },
            {
                "type": "body",
                "style_id": "expressive_3d_quirky_character",
                "title": "提示词又写崩了",
                "structure": "角色状态",
                "modules": "提示词卡片、报错纸张、巨大按钮",
                "notes": "别急着生成",
                "character_action": "双手抱头，瞪大眼睛看着飞出来的报错纸张",
                "speech_bubble": "又崩了",
                "bottom_sentence": "先看清问题，再开始生成。",
                "expression": "崩溃又无语",
                "background_color": "浅灰",
            },
            {
                "type": "cover",
                "style_id": "giant_chinese_concept_poster",
                "title": "破局",
                "subtitle": "困住你的不是墙，是你默认它没有门。",
                "visual_metaphor": "巨大破局二字像黑色石墙，被一道白光从中间劈开",
                "elements": "裂缝、白光、小人物、石墙",
                "character_action": "一个很小的人正走向裂缝中的白光",
                "speech_bubble": "裂缝 判断 出口",
                "bottom_sentence": "真正的出口，常从裂缝开始。",
                "keywords": "裂缝 判断 出口",
                "fate_sentence": "困住你的不是墙，是你默认它没有门。",
                "summary_sentence": "真正的出口，常从裂缝开始。",
                "font_mood": "石质裂纹、硬边、锋利",
                "color_mood": "黑白强对比、冷白光",
            },
            {
                "type": "cover",
                "style_id": "premium_product_ad_poster",
                "title": "HEADPHONES",
                "subtitle": "Over-Ear Wireless",
                "product_name": "Apple Pods Pro 3",
                "product_category": "无线头戴耳机",
                "product_texture": "哑光白金属、柔软耳罩、黑色网孔、绿色 LED",
                "creative_direction": "英雄近景",
                "visual_metaphor": "用户把耳机递向镜头，像邀请观众进入沉浸式声音世界",
                "selling_point1": "Premium Sound",
                "selling_point2": "40 Hours Battery",
                "selling_point3": "Fast Charge",
                "selling_point4": "Spatial Audio",
                "selling_point5": "Bluetooth 5.4",
                "brand_mood": "科技、年轻、时尚",
                "color_palette": "白色、银色、青柠绿、彩虹棱镜光",
            },
            {
                "type": "icon",
                "title": "生成一个少女风奖牌图标",
                "subject": "奖励徽章",
                "number": "1",
                "primary_color": "粉色",
                "secondary_color": "奶油黄",
                "accent_color": "浅橙",
            },
            {
                "title": "生成一个 AI 笔记 App logo",
                "subject": "圆润笔记本和小星星",
                "primary_color": "蓝紫色",
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
    assert batch["images"][5]["style_id"] == "quirky_doodle_character_flow"
    assert "小黑必须承担核心动作" in batch["images"][5]["prompt"]
    assert "认知锚点" in batch["images"][5]["prompt"]
    assert "assets/examples/xiaohei/" in batch["images"][5]["prompt"]
    assert batch["images"][6]["style_id"] == "expressive_3d_quirky_character"
    assert "3D怪表情风" in batch["images"][6]["prompt"]
    assert "assets/examples/3d_quirky/" in batch["images"][6]["prompt"]
    assert batch["images"][7]["style_id"] == "giant_chinese_concept_poster"
    assert batch["images"][7]["aspect_ratio"] == "3:4"
    assert "大字海报风" in batch["images"][7]["prompt"]
    assert "巨大中文主标题" in batch["images"][7]["prompt"]
    assert batch["images"][8]["style_id"] == "premium_product_ad_poster"
    assert batch["images"][8]["aspect_ratio"] == "4:5"
    assert "产品海报风" in batch["images"][8]["prompt"]
    assert "Apple Pods Pro 3" in batch["images"][8]["prompt"]
    assert batch["images"][9]["type"] == "icon"
    assert batch["images"][9]["style_id"] == "pastel_reward_badge_icon"
    assert batch["images"][9]["aspect_ratio"] == "1:1"
    assert "少女风奖牌图标" in batch["images"][9]["prompt"]
    assert "奖励徽章" in batch["images"][9]["prompt"]
    assert batch["images"][10]["type"] == "icon"
    assert batch["images"][10]["style_id"] == "cute_3d_plastic_icon"
    assert "1:1 方形 logo / 图标模式" in batch["images"][10]["prompt"]
    assert "圆润笔记本和小星星" in batch["images"][10]["prompt"]
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
