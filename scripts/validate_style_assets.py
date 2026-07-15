#!/usr/bin/env python3
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "references/style_example_assets.json"


def main() -> int:
    styles = json.loads(MANIFEST.read_text(encoding="utf-8"))["styles"]
    selected = sys.argv[1:] or list(styles)
    errors = []

    for style_id in selected:
        item = styles.get(style_id)
        if item is None:
            errors.append(f"未知 style_id: {style_id}")
            continue

        source = ROOT / item["source"]
        thumbnail = ROOT / item["thumbnail"]
        if not source.is_file():
            errors.append(f"缺少源图: {item['source']}")
        if not thumbnail.is_file():
            errors.append(f"缺少缩略图: {item['thumbnail']}")
            continue
        if thumbnail.suffix.lower() != ".jpg":
            errors.append(f"缩略图必须是 JPG: {item['thumbnail']}")
        if thumbnail.stat().st_size > 150_000:
            errors.append(f"缩略图超过 150 KB: {item['thumbnail']}")

        print(f"{style_id}\t{item['thumbnail']}\t{thumbnail.stat().st_size} bytes")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"OK: {len(selected)} 个风格示例图映射可用")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
