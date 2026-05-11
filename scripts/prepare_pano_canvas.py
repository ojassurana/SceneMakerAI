#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw


def fit_size(src_w, src_h, max_w, max_h):
    scale = min(max_w / src_w, max_h / src_h)
    return max(1, round(src_w * scale)), max(1, round(src_h * scale))


def main():
    parser = argparse.ArgumentParser(
        description="Place one input image onto a 2:1 panorama canvas and create an outpainting mask."
    )
    parser.add_argument("image", help="Input image path")
    parser.add_argument("--out-dir", default="pano_prep", help="Output directory")
    parser.add_argument("--width", type=int, default=2048, help="Canvas width")
    parser.add_argument("--height", type=int, default=1024, help="Canvas height")
    parser.add_argument(
        "--front-width-ratio",
        type=float,
        default=0.5,
        help="Max fraction of canvas width used by the source/front image",
    )
    parser.add_argument(
        "--front-height-ratio",
        type=float,
        default=0.8,
        help="Max fraction of canvas height used by the source/front image",
    )
    parser.add_argument(
        "--protect-white",
        action="store_true",
        help="Use white for protected source region and black for generated area. Default is black protected, white generated.",
    )
    args = parser.parse_args()

    if args.width != args.height * 2:
        raise SystemExit("Canvas must be 2:1. Use width equal to height * 2.")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    image = Image.open(args.image).convert("RGB")
    src_w, src_h = image.size
    max_w = round(args.width * args.front_width_ratio)
    max_h = round(args.height * args.front_height_ratio)
    fit_w, fit_h = fit_size(src_w, src_h, max_w, max_h)
    image = image.resize((fit_w, fit_h), Image.Resampling.LANCZOS)

    x = (args.width - fit_w) // 2
    y = (args.height - fit_h) // 2

    canvas = Image.new("RGB", (args.width, args.height), (128, 128, 128))
    canvas.paste(image, (x, y))

    if args.protect_white:
        mask_bg, mask_fg = 0, 255
        mask_convention = "white=protected black=generate"
    else:
        mask_bg, mask_fg = 255, 0
        mask_convention = "black=protected white=generate"

    mask = Image.new("L", (args.width, args.height), mask_bg)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([x, y, x + fit_w - 1, y + fit_h - 1], fill=mask_fg)

    alpha = Image.new("L", (args.width, args.height), 0)
    alpha_draw = ImageDraw.Draw(alpha)
    alpha_draw.rectangle([x, y, x + fit_w - 1, y + fit_h - 1], fill=255)
    mask_alpha = Image.new("RGBA", (args.width, args.height), (255, 255, 255, 255))
    mask_alpha.putalpha(alpha)

    preview = canvas.copy()
    overlay = Image.new("RGBA", canvas.size, (255, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([x, y, x + fit_w - 1, y + fit_h - 1], outline=(0, 255, 0, 255), width=4)
    preview = Image.alpha_composite(preview.convert("RGBA"), overlay).convert("RGB")

    canvas_path = out_dir / "canvas.png"
    mask_path = out_dir / "mask.png"
    mask_alpha_path = out_dir / "mask-alpha.png"
    preview_path = out_dir / "preview.png"
    meta_path = out_dir / "metadata.json"

    canvas.save(canvas_path)
    mask.save(mask_path)
    mask_alpha.save(mask_alpha_path)
    preview.save(preview_path)
    meta_path.write_text(
        json.dumps(
            {
                "canvas": str(canvas_path),
                "mask": str(mask_path),
                "mask_alpha": str(mask_alpha_path),
                "preview": str(preview_path),
                "source_box": {"x": x, "y": y, "width": fit_w, "height": fit_h},
                "mask_convention": mask_convention,
            },
            indent=2,
        )
        + "\n"
    )

    print(
        json.dumps(
            {
                "canvas": str(canvas_path),
                "mask": str(mask_path),
                "mask_alpha": str(mask_alpha_path),
                "preview": str(preview_path),
                "metadata": str(meta_path),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
