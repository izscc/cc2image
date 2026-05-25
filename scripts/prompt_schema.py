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


EXTRA_COVER_GUIDES = {
    "retro_minimal_poster_illustration": "米白旧纸背景，复古印刷颗粒，大面积钴蓝和芥末黄色块，几何化人物或物件，像中世纪现代海报、复古书封或丝网印刷插画。",
    "editorial_balloon_collage": "白色纸张背景，大量留白，半透明彩色圆片像气球或光片，下方用细线素描人物或物件，并用细线连接到圆片，像品牌广告或编辑设计封面。",
    "transparent_architectural_type": "浅灰或雾白背景，巨大透明玻璃数字、字母或汉字作为建筑空间，内部有云雾、天空、山体、光线、微型人物或空间场景。",
    "paper_cut_profile_silhouette": "白色或浅米色纸张背景，单色纸雕剪影作为主体，剪影内部嵌入行业场景、建筑、工具、道路、书本或系统结构，有纸张厚度和投影。",
    "torn_paper_note_minimal": "米色、暖白或浅灰纸张背景，大量留白，中心或偏下只有一小片白色撕裂纸条，纸条上写一个词或一句很短的话。",
    "fluffy_soft_typography": "白色、奶油色或浅灰背景，标题文字变成真实可触摸的毛绒、毛巾布、羊羔绒或绒线立体字体，边缘有细密绒毛和柔和阴影。",
    "cloud_typography_cover": "蓝天或青蓝渐变天空背景，标题文字由真实蓬松的白云组成，有阳光照射、云影和细腻云气质感，画面开阔、明亮、向上。",
    "editorial_line_character": "白色或奶油白背景，大量留白，黑白极简线稿人物作为主要叙事角色，搭配杂志式大标题、非对称网格和少量柔和色块；可做成品牌视觉板、海报、网站首屏、包装或多面板编辑插画。",
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
