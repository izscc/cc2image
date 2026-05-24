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
        "整体风格为东方典籍杂志插画风：暖白宣纸质感背景，低饱和蓝金配色，石青、金色、米白、墨灰为主，"
        "画面像高端文化杂志或图书封面。主体使用巨大文化隐喻物，例如打开的古籍、卷轴、山河、地图、书页、河流。"
        "加入少量微缩人物，人物像行走在典籍和山水之间。整体诗意、克制、留白充足，有历史感、文化感、东方美学和高级出版物质感。"
        "不要做成 PPT，不要科技风，不要可爱卡通，不要二次元，不要游戏概念图，不要 3D，不要高饱和颜色，不要拥挤。\n"
        "Oriental editorial illustration style, premium cultural magazine cover, New Chinese aesthetic, warm ivory paper texture, muted blue and gold palette, "
        "stone blue, ochre gold, rice white, ink gray, poetic negative space, monumental cultural metaphor object, open ancient book, scroll, mountains, rivers, "
        "map-like landscape, tiny wandering figures in minimal traditional robes, subtle calligraphy fragments, literary, historical, elegant, calm, refined, "
        "high-end publishing design, not anime, not cartoon, not cyberpunk, not 3D, not PPT infographic, not crowded."
    ),
    "study_note_card": (
        "整体风格为学习笔记卡片风：米白纸张背景，中间是一张带轻微阴影的笔记纸卡片，周围有胶带、回形针、便签、贴纸等学习手账元素。"
        "使用低饱和浅紫、浅黄、奶油白、深绿色配色。标题醒目，正文分区清晰，搭配少量手绘学习图标和简笔插画。"
        "整体像精心整理的学习笔记、小红书知识卡片或高质量学习手账，不要做成商务 PPT，不要科技风，不要复杂海报，不要高饱和颜色，不要过度装饰。"
    ),
    "pastel_learning_pyramid": (
        "整体风格为彩色手绘学习金字塔风：白色或米白纸张纹理背景，主体是柔和粉彩笔刷绘制的分层金字塔、阶梯或漏斗。"
        "每层使用低饱和粉色、橙色、黄色、薄荷绿、浅蓝、浅紫等色块。文字像手写笔记，搭配虚线、箭头、百分比、小标签。"
        "整体轻松、清楚、学习感强，像手绘学习方法海报。不要做成商务图表，不要 3D 金字塔，不要科技风，不要高饱和颜色，不要复杂背景。"
    ),
    "childlike_cultural_infographic": (
        "整体风格为儿童手绘文化科普风：白色纸张背景，黑色手绘边框，水彩手绘插画，线条自然、有童趣。"
        "画面包含多个文化物件、可爱人物、虚线箭头、标签说明和气泡旁白。配色温和，像少儿文化科普海报、儿童绘本知识页或课堂小报。"
        "文字清楚但不要过密，整体活泼、有趣、易懂。不要做成写实插画，不要商业海报，不要科技风，不要 3D，不要高级冷淡风。"
    ),
    "frosted_glass_editorial": (
        "整体风格为透明磨砂感海报风：画面像隔着一层半透明磨砂玻璃观看人物或物体，主体轮廓被柔和模糊，只露出局部阴影、形状和深色轮廓。"
        "背景为低饱和冷灰、灰绿、雾白或浅蓝色，大量留白，构图极简。文字采用现代极简排版，可以用少量亮黄色或黑色作为强调。"
        "整体像艺术节、音乐节、设计展或高级品牌海报，安静、神秘、克制、疏离。不要做成信息图，不要手绘卡通，不要 3D 科技风，不要复杂背景，不要高饱和色，不要密集文字。\n"
        "Frosted glass editorial poster style, translucent frosted glass surface, blurred human silhouette or abstract object behind glass, soft diffusion, low contrast, "
        "muted pale green gray background, minimal composition, large negative space, modern Swiss editorial typography, small bright yellow accent text, quiet, mysterious, "
        "restrained, premium art festival poster, not infographic, not cartoon, not 3D, not cyberpunk, not crowded."
    ),
}

STYLE_NAMES = {
    "handdrawn_knowledge_card": "手绘知识卡片风",
    "oriental_editorial_illustration": "东方典籍杂志插画风",
    "study_note_card": "学习笔记卡片风",
    "pastel_learning_pyramid": "彩色手绘学习金字塔风",
    "childlike_cultural_infographic": "儿童手绘文化科普风",
    "frosted_glass_editorial": "透明磨砂感海报风",
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
    return f"""请生成一张东方典籍杂志插画风的中文文章封面图。
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


def render_cover(spec: CoverSpec) -> str:
    spec.style_id = normalize_style(spec.style_id)
    if spec.style_id == "oriental_editorial_illustration":
        return render_oriental_cover(spec)
    if spec.style_id == "frosted_glass_editorial":
        return render_frosted_cover(spec)
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
    return f"""请生成一张学习笔记卡片风的中文知识图。
主题是「{spec.title}」。画面使用米白色纸张背景，中间放置一张略带阴影的笔记纸卡片，整体像精心整理的学习手账页面。
顶部用醒目的中文标题写「{spec.title}」，标题可以放在浅紫色手绘色块或浅黄色标签上。标题字体清楚、圆润、自然，有学习笔记感。
画面内容分为 3 到 5 个清晰区域，每个区域有小标题、简短说明和少量重点词高亮。核心内容包括：「{spec.modules}」。
加入少量学习类装饰元素，例如胶带、回形针、便签、贴纸、手绘笔记本、清单、箭头、小星星。装饰要克制，不要抢内容。
正文使用深绿色或深灰色文字，重点词可以用浅黄色或浅紫色荧光笔效果标注。必要注释：「{spec.notes}」。
底部写一句总结：「{spec.bottom_sentence}」。
{STYLE_ANCHORS['study_note_card']}"""


def render_pyramid(spec: BodySpec) -> str:
    return f"""请生成一张彩色手绘学习金字塔风的中文知识图。
主题是「{spec.title}」。画面为竖版或横版纸张纹理背景，整体干净、轻松、有手绘学习海报感。
顶部写一个醒目的中文手写标题：「{spec.title}」，标题下方可以有柔和的粉彩笔刷底色。副标题写「{spec.subtitle or spec.bottom_sentence}」，字号较小，像手写笔记。
画面中心绘制一个分层结构，可以是金字塔、阶梯或漏斗。分层包括：「{spec.modules}」。每一层使用不同的低饱和粉彩色块，例如粉色、橙色、黄色、薄荷绿、浅蓝、浅紫。色块边缘保留手绘笔刷质感。
在每一层旁边加入简短标注：「{spec.notes}」。可以使用虚线、箭头、小标签、百分比框来连接说明。
如果内容有对比关系，可以在左侧标注「被动学习」，在下方或右侧标注「主动学习」，用虚线和箭头表达层级变化。
{STYLE_ANCHORS['pastel_learning_pyramid']}"""


def render_childlike(spec: BodySpec) -> str:
    return f"""请生成一张儿童手绘文化科普风的中文知识图。
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
    assert "东方典籍杂志插画风" in batch["images"][0]["prompt"]
    assert batch["images"][1]["style_id"] == "study_note_card"
    assert "学习笔记卡片风" in batch["images"][1]["prompt"]
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
