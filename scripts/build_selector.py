#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import html
import io
import json
import re
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STYLE_OPTIONS = ROOT / "references/style_options.md"
ASSET_MANIFEST = ROOT / "references/style_example_assets.json"
GROUP_LABELS = {
    "A": "知识图解类",
    "B": "东方、人文与情绪",
    "C": "极简设计与材质海报",
    "D": "字体材质类",
    "E": "拼贴、纸张与手工材质",
    "F": "微缩场景与品牌广告",
    "G": "空间系统与轴测图解",
    "H": "logo / 图标类",
}
GROUP_REASONS = {
    "A": "适合拆解结构与关键步骤",
    "B": "适合人文情绪与东方表达",
    "C": "适合极简视觉与材质呈现",
    "D": "适合强化标题与概念表达",
    "E": "适合手工质感与叙事表达",
    "F": "适合品牌场景与产品展示",
    "G": "适合呈现系统结构与流程",
    "H": "适合应用入口与品牌识别",
}
FORCED_RATIOS = {
    "giant_chinese_concept_poster": "4:5|1440x1800",
    "premium_product_ad_poster": "4:5|1440x1800",
    "editorial_line_infographic_poster": "9:16|1080x1920",
    "glyph_object_imagery": "1:1|1536x1536",
}
RATIO_OPTIONS = [
    ("21:9|2560x1080", "21:9 · 2560×1080（横版超宽）"),
    ("16:9|1920x1080", "16:9 · 1920×1080（横版通用）"),
    ("3:2|1800x1200", "3:2 · 1800×1200（横版文章）"),
    ("4:3|1600x1200", "4:3 · 1600×1200（横版卡片）"),
    ("1:1|1536x1536", "1:1 · 1536×1536（方形社媒）"),
    ("4:5|1440x1800", "4:5 · 1440×1800（竖版海报）"),
    ("3:4|1350x1800", "3:4 · 1350×1800（竖版封面）"),
    ("9:16|1080x1920", "9:16 · 1080×1920（手机长图）"),
]


def load_style_metadata() -> tuple[dict[str, str], dict[str, list[str]]]:
    text = STYLE_OPTIONS.read_text(encoding="utf-8")
    match = re.search(r"## 风格选择表\s*```json\s*(\{.*?\})\s*```", text, re.S)
    if not match:
        raise ValueError("无法解析 references/style_options.md 的风格选择表")
    names = {
        item["style_id"]: item["style_name"]
        for item in json.loads(match.group(1))["styles"]
    }

    logo_section = text.split("## logo / 图标模式", 1)[1].split("## 推荐匹配规则", 1)[0]
    for style_id, style_name in re.findall(
        r"^\| `([^`]+)` \| ([^|]+?) \|", logo_section, re.M
    ):
        names[style_id] = style_name.strip()

    group_section = text.split("## 风格分组", 1)[1].split("## logo / 图标模式", 1)[0]
    groups: dict[str, list[str]] = {}
    for key, line in re.findall(r"^([A-H])\. (.+)$", group_section, re.M):
        groups[key] = re.findall(r"`([^`]+)`", line)
    return names, groups


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 cc2image 交互式风格选择器")
    parser.add_argument("--output-dir", type=Path, help="自动创建唯一 fragment 的目录")
    parser.add_argument("--stdin-config", action="store_true", help="从标准输入读取 JSON 配置")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def apply_stdin_config(args: argparse.Namespace) -> None:
    payload = json.loads(sys.stdin.readline())
    if set(payload) != {"recommend", "body_count", "cover_enabled", "icon_mode"}:
        raise ValueError("stdin 配置字段无效")
    if not isinstance(payload["recommend"], list) or not all(
        isinstance(style_id, str) for style_id in payload["recommend"]
    ):
        raise ValueError("recommend 必须为 style_id 数组")
    if type(payload["body_count"]) is not int:
        raise ValueError("body_count 必须为整数")
    if type(payload["cover_enabled"]) is not bool or type(payload["icon_mode"]) is not bool:
        raise ValueError("cover_enabled 和 icon_mode 必须为布尔值")
    args.recommend = payload["recommend"]
    args.body_count = payload["body_count"]
    args.cover_enabled = str(payload["cover_enabled"]).lower()
    args.icon_mode = payload["icon_mode"]
    args.label = "App 图标" if args.icon_mode else "内容配图"
    args.output = None


def validate_inputs(
    args: argparse.Namespace,
    names: dict[str, str],
    groups: dict[str, list[str]],
    assets: dict,
) -> None:
    if len(args.recommend or []) != 3:
        raise ValueError("--recommend 必须恰好提供 3 次")
    style_ids = args.recommend
    if len(set(style_ids)) != 3:
        raise ValueError("3 个推荐风格不能重复")
    allowed = set(groups["H"] if args.icon_mode else names) - (
        set() if args.icon_mode else set(groups["H"])
    )
    for style_id in args.recommend:
        if style_id not in names:
            raise ValueError(f"未知 style_id: {style_id}")
        if style_id not in allowed:
            raise ValueError(f"style_id 与当前模式不匹配: {style_id}")
        if style_id not in assets:
            raise ValueError(f"缺少示例图映射: {style_id}")
        thumbnail = asset_path(style_id, assets)
        if thumbnail.read_bytes()[:3] != b"\xff\xd8\xff":
            raise ValueError(f"缩略图不是 JPEG: {thumbnail}")
    if not 0 <= args.body_count <= 10:
        raise ValueError("--body-count 必须在 0-10 之间")


def asset_path(style_id: str, assets: dict) -> Path:
    thumbnail = (ROOT / assets[style_id]["thumbnail"]).resolve()
    if ROOT not in thumbnail.parents or not thumbnail.is_file():
        raise ValueError(f"缩略图路径无效: {thumbnail}")
    return thumbnail


def image_data(style_id: str, assets: dict) -> str:
    thumbnail = asset_path(style_id, assets)
    return "data:image/jpeg;base64," + base64.b64encode(thumbnail.read_bytes()).decode()


def recommendation_reason(style_id: str, groups: dict[str, list[str]]) -> str:
    for key in reversed(["A", "B", "C", "D", "E", "F", "G", "H"]):
        if style_id in groups.get(key, []):
            return GROUP_REASONS[key]
    return "适合当前内容的视觉表达"


def select_groups(
    icon_mode: bool,
    names: dict[str, str],
    groups: dict[str, list[str]],
) -> list[tuple[str, list[str]]]:
    keys = ["H"] if icon_mode else ["A", "B", "C", "D", "E", "F", "G"]
    allowed = set(groups["H"] if icon_mode else names) - (
        set() if icon_mode else set(groups["H"])
    )
    owner = {
        style_id: key
        for key in keys
        for style_id in groups.get(key, [])
        if style_id in allowed
    }
    result = []
    for key in keys:
        unique = [style_id for style_id in groups.get(key, []) if owner.get(style_id) == key]
        if unique:
            result.append((GROUP_LABELS[key], unique))
    grouped = set(owner)
    ungrouped = [style_id for style_id in names if style_id in allowed and style_id not in grouped]
    if ungrouped:
        result.append(("其他风格", ungrouped))
    return result


def build_fragment(args: argparse.Namespace) -> str:
    names, groups = load_style_metadata()
    assets = json.loads(ASSET_MANIFEST.read_text(encoding="utf-8"))["styles"]
    validate_inputs(args, names, groups, assets)

    ranks = ("首选 · 推荐", "备选", "探索")
    cards = []
    for index, style_id in enumerate(args.recommend):
        reason = recommendation_reason(style_id, groups)
        cards.append(
            f'''      <button type="button" class="card style-card" data-style-id="{html.escape(style_id)}" aria-pressed="{'true' if index == 0 else 'false'}">
        <img src="{image_data(style_id, assets)}" alt="{html.escape(names[style_id])}示例">
        <span class="style-card-copy">
          <span class="style-rank text-small">{ranks[index]}</span>
          <strong>{html.escape(names[style_id])}</strong>
          <span class="text-small">{html.escape(reason.strip())}</span>
        </span>
      </button>'''
        )

    recommended_ids = set(args.recommend)
    optgroups = []
    for label, style_ids in select_groups(args.icon_mode, names, groups):
        options = "".join(
            f'<option value="{html.escape(style_id)}">{html.escape(names[style_id])}</option>'
            for style_id in style_ids
            if style_id not in recommended_ids
        )
        if options:
            optgroups.append(f'        <optgroup label="{html.escape(label)}">{options}</optgroup>')

    selected_style = args.recommend[0]
    selected_name = names[selected_style]
    cover_enabled = args.cover_enabled == "true"
    default_ratio = "1:1|1536x1536" if args.icon_mode else FORCED_RATIOS.get(selected_style, "21:9|2560x1080")
    ratio_options = "\n".join(
        f'        <option value="{value}"{" selected" if value == default_ratio else ""}>{label}</option>'
        for value, label in RATIO_OPTIONS
    )
    style_names_json = json.dumps(names, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    forced_ratios_json = json.dumps(FORCED_RATIOS, separators=(",", ":"))
    label = html.escape(args.label[:32])
    more_control = f'''<label class="form-label field-block" for="cc2image-more-style">
      <span>更多风格</span>
      <select id="cc2image-more-style" class="form-select">
        <option value="">从完整风格库选择</option>
{chr(10).join(optgroups)}
      </select>
    </label>'''

    if args.icon_mode:
        controls = f'''  {more_control}

  <div class="field-block">
    <span>输出规格</span>
    <p class="summary">1:1 方形图标 · 1 张</p>
  </div>'''
        summary = f"{html.escape(selected_name)} · 1:1 · 1 张"
    else:
        controls = f'''  <div class="fields">
    {more_control}

    <div class="field-block">
      <span>封面设置</span>
      <label class="form-check form-switch" for="cc2image-cover-enabled">
        <input id="cc2image-cover-enabled" class="form-check-input" type="checkbox"{' checked' if cover_enabled else ''}>
        <span class="form-check-label">生成封面</span>
      </label>
      <label class="form-label" for="cc2image-cover-ratio">封面比例尺寸</label>
      <select id="cc2image-cover-ratio" class="form-select">
{ratio_options}
      </select>
    </div>
  </div>

  <div class="field-block">
    <div class="range-head">
      <label for="cc2image-body-count">正文配图数量</label>
      <span id="cc2image-body-count-label" class="text-small">推荐 {args.body_count} 张 / 当前 {args.body_count} 张</span>
    </div>
    <input id="cc2image-body-count" class="form-range body-count-range" type="range" min="0" max="10" step="1" value="{args.body_count}">
  </div>'''
        ratio_text = default_ratio.split("|", 1)[0]
        summary = f"{html.escape(selected_name)} · {'封面 ' + ratio_text if cover_enabled else '不生成封面'} · 正文 {args.body_count} 张"

    return f'''<div id="cc2image-selector">
  <style>
    #cc2image-selector {{ display: grid; gap: 18px; color: var(--foreground); }}
    #cc2image-selector .section-head {{ display: flex; align-items: baseline; justify-content: space-between; gap: 12px; flex-wrap: wrap; }}
    #cc2image-selector .recommendations {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
    #cc2image-selector .style-card {{ display: grid; gap: 10px; width: 100%; text-align: left; overflow: hidden; }}
    #cc2image-selector .style-card img {{ display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: inherit; }}
    #cc2image-selector .style-card-copy {{ display: grid; gap: 5px; }}
    #cc2image-selector .style-card-copy > .text-small:last-child {{ text-wrap: balance; }}
    #cc2image-selector .style-rank {{ color: var(--muted-foreground); }}
    #cc2image-selector .style-card[aria-pressed="true"] {{ border-color: color-mix(in oklab, var(--primary) 64%, var(--border) 36%); box-shadow: inset 0 0 0 1px color-mix(in oklab, var(--primary) 46%, transparent); }}
    #cc2image-selector .style-card[aria-pressed="true"] .style-rank {{ color: var(--card-foreground); }}
    #cc2image-selector .fields {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }}
    #cc2image-selector .field-block {{ display: grid; gap: 8px; }}
    #cc2image-selector .range-head {{ display: flex; justify-content: space-between; gap: 12px; align-items: baseline; }}
    #cc2image-selector .body-count-range {{ --body-count-thumb: light-dark(color-mix(in oklab, var(--primary) 76%, var(--foreground) 24%), var(--primary)); }}
    #cc2image-selector .body-count-range::-webkit-slider-thumb {{ border-color: var(--body-count-thumb); background: var(--body-count-thumb); }}
    #cc2image-selector .body-count-range::-moz-range-thumb {{ border-color: var(--body-count-thumb); background: var(--body-count-thumb); }}
    #cc2image-selector .summary {{ margin: 0; color: var(--muted-foreground); }}
    #cc2image-selector .status {{ min-height: 1.4em; margin: 0; }}
    @media (max-width: 560px) {{
      #cc2image-selector .recommendations,
      #cc2image-selector .fields {{ grid-template-columns: 1fr; }}
    }}
  </style>

  <section aria-labelledby="cc2image-recommended-heading">
    <div class="section-head">
      <h3 id="cc2image-recommended-heading">推荐风格</h3>
      <span class="viz-badge">{label}</span>
    </div>
    <div class="viz-grid recommendations">
{chr(10).join(cards)}
    </div>
  </section>

{controls}

  <p id="cc2image-config-summary" class="summary">{summary}</p>
  <button id="cc2image-submit" type="button" class="btn btn-primary btn-block">使用此配置继续</button>
  <p id="cc2image-status" class="status text-small text-destructive" role="status" aria-live="polite"></p>

  <script>
    (() => {{
      const root = document.getElementById('cc2image-selector');
      const cards = [...root.querySelectorAll('[data-style-id]')];
      const moreStyle = root.querySelector('#cc2image-more-style');
      const summary = root.querySelector('#cc2image-config-summary');
      const submit = root.querySelector('#cc2image-submit');
      const status = root.querySelector('#cc2image-status');
      const styleNames = {style_names_json};
      const forcedRatios = {forced_ratios_json};
      const iconMode = {str(args.icon_mode).lower()};
      const recommendedBodyCount = {args.body_count};
      let selectedStyle = {json.dumps(selected_style)};
      let ratioTouched = false;
      const coverEnabled = root.querySelector('#cc2image-cover-enabled');
      const coverRatio = root.querySelector('#cc2image-cover-ratio');
      const bodyCount = root.querySelector('#cc2image-body-count');
      const bodyLabel = root.querySelector('#cc2image-body-count-label');

      const update = () => {{
        cards.forEach(card => card.setAttribute('aria-pressed', String(card.dataset.styleId === selectedStyle)));
        if (iconMode) {{
          summary.textContent = `${{styleNames[selectedStyle]}} · 1:1 · 1 张`;
          return;
        }}
        bodyLabel.textContent = `推荐 ${{recommendedBodyCount}} 张 / 当前 ${{bodyCount.value}} 张`;
        const ratio = coverRatio.value.split('|')[0];
        summary.textContent = `${{styleNames[selectedStyle]}} · ${{coverEnabled.checked ? `封面 ${{ratio}}` : '不生成封面'}} · 正文 ${{bodyCount.value}} 张`;
        coverRatio.disabled = !coverEnabled.checked;
      }};

      const selectStyle = styleId => {{
        selectedStyle = styleId;
        if (!iconMode && !ratioTouched) coverRatio.value = forcedRatios[styleId] || '21:9|2560x1080';
        update();
      }};

      cards.forEach(card => card.addEventListener('click', () => {{ moreStyle.value = ''; selectStyle(card.dataset.styleId); }}));
      moreStyle.addEventListener('change', () => {{ if (moreStyle.value) selectStyle(moreStyle.value); }});
      if (!iconMode) {{
        coverEnabled.addEventListener('change', update);
        coverRatio.addEventListener('change', () => {{ ratioTouched = true; update(); }});
        bodyCount.addEventListener('input', update);
      }}
      submit.addEventListener('click', async () => {{
        const ratio = iconMode ? '1:1' : coverRatio.value.split('|')[0];
        const size = iconMode ? '1536x1536' : coverRatio.value.split('|')[1];
        const enabled = iconMode ? true : coverEnabled.checked;
        const count = iconMode ? 0 : Number(bodyCount.value);
        const selectionPrompt = `继续执行当前 cc2image 任务，不要再次打开选择器。按以下配置生成或输出清单：\nCC2IMAGE_SELECTION_V1\nstyle_id=${{selectedStyle}}\ncover_enabled=${{enabled}}\ncover_ratio=${{ratio}}\ncover_size=${{size}}\nbody_count=${{count}}\nskip_selector=true\nEND_CC2IMAGE_SELECTION`;
        submit.disabled = true;
        submit.textContent = '正在提交…';
        status.textContent = '';
        try {{
          await window.openai.sendFollowUpMessage({{ title: '确认 cc2image 出图配置', prompt: selectionPrompt }});
        }} catch (error) {{
          submit.disabled = false;
          submit.textContent = '使用此配置继续';
          status.textContent = '提交失败，请稍后重试。';
        }}
      }});
      update();
    }})();
  </script>
</div>
'''


def write_fragment(args: argparse.Namespace, restrict_output: bool = True) -> Path:
    output_dir = getattr(args, "output_dir", None)
    if output_dir is not None:
        directory = output_dir.expanduser().resolve()
        output = directory / f"cc2image-selector-{time.time_ns()}.html"
    elif args.output is not None:
        output = args.output.expanduser()
        if not output.is_absolute():
            raise ValueError("--output 必须为绝对路径")
        directory = output.parent.resolve()
    else:
        raise ValueError("缺少 --output 或 --output-dir")
    if restrict_output:
        visualization_root = (Path.home() / ".codex/visualizations").resolve()
        if visualization_root != directory and visualization_root not in directory.parents:
            raise ValueError("输出必须位于 Codex visualization 目录")
    if output.exists() or output.is_symlink():
        raise ValueError(f"输出文件已存在: {output}")
    fragment = build_fragment(args)
    if fragment.count("<img ") != 3 or fragment.count("data:image/jpeg;base64,") != 3:
        raise ValueError("推荐示例图必须恰好为 3 张")
    if "data-lucide" in fragment:
        raise ValueError("推荐区不得使用 icon")
    if len(fragment.encode()) >= 2_000_000:
        raise ValueError("fragment 超过 2 MB")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        stream.write(fragment)
    return output


def self_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        args = argparse.Namespace(
            output=Path(directory) / "selector.html",
            recommend=[
                "handdrawn_knowledge_card",
                "editorial_object_annotation_card",
                "monochrome_system_editorial",
            ],
            label="长文 · 商业方法论",
            body_count=7,
            cover_enabled="true",
            icon_mode=False,
            self_test=True,
        )
        output = write_fragment(args, restrict_output=False)
        text = output.read_text(encoding="utf-8")
        assert "推荐 7 张 / 当前 7 张" in text
        assert "background: var(--body-count-thumb)" in text
        assert "text-wrap: balance" in text
        assert "window.openai.sendFollowUpMessage" in text
        assert '<option value="dark_neon_search_ui">' in text
        assert '<option value="scribble_furball_character_family">' in text
        assert '<optgroup label="空间系统与轴测图解">' in text
        assert output.stat().st_size < 2_000_000

        args.output = None
        args.output_dir = Path(directory)
        unique_first = write_fragment(args, restrict_output=False)
        unique_second = write_fragment(args, restrict_output=False)
        assert unique_first != unique_second

        icon_args = argparse.Namespace(
            output=Path(directory) / "icon-selector.html",
            recommend=[
                "cute_3d_plastic_icon",
                "frosted_glass_ui_icon",
                "circular_3d_texture_icon",
            ],
            label="App 图标",
            body_count=0,
            cover_enabled="true",
            icon_mode=True,
            self_test=True,
        )
        icon_output = write_fragment(icon_args, restrict_output=False)
        icon_text = icon_output.read_text(encoding="utf-8")
        assert "1:1 方形图标 · 1 张" in icon_text
        assert 'id="cc2image-body-count"' not in icon_text
        assert 'id="cc2image-cover-enabled"' not in icon_text

        stdin_args = argparse.Namespace()
        original_stdin = sys.stdin
        try:
            sys.stdin = io.StringIO(json.dumps({
                "recommend": [
                    "cute_3d_plastic_icon",
                    "frosted_glass_ui_icon",
                    "circular_3d_texture_icon",
                ],
                "body_count": 0,
                "cover_enabled": True,
                "icon_mode": True,
            }))
            apply_stdin_config(stdin_args)
        finally:
            sys.stdin = original_stdin
        assert stdin_args.label == "App 图标"


def main() -> int:
    args = parse_args()
    if args.self_test:
        self_test()
        print("self-test passed")
        return 0
    if args.stdin_config:
        apply_stdin_config(args)
    else:
        raise ValueError("运行时必须使用 --stdin-config")
    output = write_fragment(args)
    print(json.dumps({"output": str(output), "bytes": output.stat().st_size}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
