#!/usr/bin/env python3
"""Prompt helpers for 中文知识手绘配图生成器.

Use this script to validate image plan JSON and render stable cover/body prompts.
It does not call any image generation API; Codex should use the rendered prompts
with the available image generation tool when requested.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Literal

GLOBAL_STYLE_ANCHOR = (
    "整体风格像高质量中文知识博主的手绘知识图解系统：暖白纸感背景，黑灰细线手绘，"
    "低饱和浅色块，中文手写字，自然成熟，克制精致，留白充足，轻商业内容资产感。"
    "不要做成 PPT，不要课程课件，不要科技海报，不要 3D，不要可爱儿童插画，"
    "不要复杂信息图，不要密集小字，不要高饱和颜色，不要英文乱码，不要水印。"
)

BODY_STRUCTURES = {
    "闭环机制图",
    "横向流程图",
    "分类树图",
    "左右对比图",
    "结构类比图",
    "风险路径图",
    "光谱选择图",
    "随附场景图",
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


@dataclass
class BodySpec:
    title: str
    structure: str
    modules: str
    notes: str
    character_action: str
    speech_bubble: str
    bottom_sentence: str


def require_fields(data: Dict[str, Any], fields: List[str], label: str) -> None:
    missing = [field for field in fields if not str(data.get(field, "")).strip()]
    if missing:
        raise ValueError(f"{label} 缺少字段: {', '.join(missing)}")


def render_cover(spec: CoverSpec) -> str:
    return f"""请生成一张 21:9 横版中文知识文章封面图。
主题是「{spec.title}」。画面使用暖白色纸张背景，带轻微纸张纹理，整体干净、克制、精致、有大量留白。
采用左右结构：左侧约 45% 放主标题和副标题，右侧约 55% 放手绘概念图。
左侧用自然成熟的中文手写大字写标题：「{spec.title}」。标题可以分成两行或三行，其中一行背后可以加一块很淡的低饱和手绘笔刷色块。标题要大、有冲击力，但保持松弛、精致、克制，不要像广告字，不要像儿童字体，不要像毛笔书法。
标题下方写副标题：「{spec.subtitle}」。副标题使用较小的细线手写字，清楚、自然、安静。
右侧画一个简单的手绘概念图，核心隐喻是「{spec.metaphor}」。画面元素包括「{spec.elements}」。图解要简洁，不要复杂，像知识隐喻，不是插画场景。图解中可以有少量中文标签，每个标签 2 到 6 个字。
右下角画一个极简抽象小人，{spec.character_action}。小人旁边有一个小气泡，写着：「{spec.speech_bubble}」。
底部用很轻的小字写一句判断式结论：「{spec.bottom_sentence}」。
{GLOBAL_STYLE_ANCHOR}"""


def render_body(spec: BodySpec) -> str:
    if spec.structure not in BODY_STRUCTURES:
        raise ValueError(f"未知正文结构: {spec.structure}")
    return f"""请生成一张中文文章正文配图，不是封面图。
主题是「{spec.title}」。画面为横版 16:9 构图，暖白色纸张背景，轻微纸感纹理，整体干净、克制、精致、有大量留白。
画面顶部居中写一个自然成熟的中文手写标题：「{spec.title}」，标题下方可以有一条很轻的手绘短线。
画面中间绘制一个「{spec.structure}」。核心模块包括：「{spec.modules}」。模块使用低饱和浅色圆角卡片、便签、框图或标签承载，模块之间用黑灰色细线手绘箭头连接。主体图解不要过大，四周保留明显留白。
在图解旁加入少量极简短注释：「{spec.notes}」。注释必须短，不要生成大段正文，不要密集小字。
画面右侧或右下角画一个极简抽象小人，细线条，成人感，{spec.character_action}。小人旁边有一个小气泡，写着：「{spec.speech_bubble}」。
画面底部用轻微手写小字写一句判断式结论：「{spec.bottom_sentence}」。
{GLOBAL_STYLE_ANCHOR}"""


def build_image_item(raw: Dict[str, Any], index: int) -> Dict[str, Any]:
    image_type = raw.get("type")
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
        )
        return {
            "id": raw.get("id") or f"cover_{index:02d}",
            "type": "cover",
            "aspect_ratio": "21:9",
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
        )
        return {
            "id": raw.get("id") or f"body_{index:02d}",
            "type": "body",
            "aspect_ratio": "16:9",
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
        "visual_style": "warm-paper-handdrawn-chinese-knowledge-card",
        "global_style_prompt": GLOBAL_STYLE_ANCHOR,
        "images": images,
    }


def self_test() -> None:
    batch = build_batch(
        "个人知识库真正的用法",
        [
            {
                "type": "cover",
                "title": "个人知识库真正的用法",
                "subtitle": "不是收藏更多，而是形成可复用的思考系统",
                "metaphor": "工作台上的卡片循环系统",
                "elements": "输入卡片、主题连接、输出按钮、循环箭头",
                "character_action": "站在工作台旁整理卡片",
                "speech_bubble": "让知识动起来",
                "bottom_sentence": "知识库的价值在于被反复调用。",
            },
            {
                "type": "body",
                "title": "知识库不是收藏夹",
                "structure": "左右对比图",
                "modules": "收藏夹、知识系统、输入、连接、输出",
                "notes": "少存一点、多连接一点、能用才算数",
                "character_action": "指向右侧的知识系统",
                "speech_bubble": "要能产出",
                "bottom_sentence": "不能输出的资料，只是库存。",
            },
        ],
    )
    assert batch["images"][0]["aspect_ratio"] == "21:9"
    assert batch["images"][1]["structure"] == "左右对比图"
    assert GLOBAL_STYLE_ANCHOR in batch["images"][0]["prompt"]
    assert GLOBAL_STYLE_ANCHOR in batch["images"][1]["prompt"]
    print("self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description="渲染中文知识手绘配图批量 prompt JSON")
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
