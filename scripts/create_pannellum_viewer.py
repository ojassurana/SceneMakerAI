#!/usr/bin/env python3
import argparse
import hashlib
import html
import json
import shutil
from pathlib import Path


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SceneMakerAI Preview</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.css">
  <style>
    html, body, #panorama {{
      width: 100%;
      height: 100%;
      margin: 0;
    }}
    body {{
      background: #111;
      overflow: hidden;
    }}
  </style>
</head>
<body>
  <div id="panorama"></div>
  <script src="https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.js"></script>
  <script>
    pannellum.viewer('panorama', {{
      type: 'equirectangular',
      panorama: '{panorama_name}',
      autoLoad: true,
      showControls: true
    }});
  </script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Create a lightweight Pannellum preview folder for a panorama image.")
    parser.add_argument("panorama", help="Path to the final 2:1 equirectangular panorama image")
    parser.add_argument("--out-dir", default="pannellum_viewer", help="Output viewer directory")
    parser.add_argument("--port", type=int, default=8000, help="Suggested localhost port")
    args = parser.parse_args()

    panorama_path = Path(args.panorama).expanduser().resolve()
    if not panorama_path.exists():
        raise SystemExit(f"Panorama not found: {panorama_path}")

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    digest = hashlib.sha256(panorama_path.read_bytes()).hexdigest()[:12]
    suffix = panorama_path.suffix.lower() or ".png"
    viewer_image = out_dir / f"panorama-{digest}{suffix}"
    shutil.copy2(panorama_path, viewer_image)

    index_path = out_dir / "index.html"
    cache_busted_name = f"{viewer_image.name}?v={digest}"
    index_path.write_text(
        HTML_TEMPLATE.format(panorama_name=html.escape(cache_busted_name, quote=True)),
        encoding="utf-8",
    )

    url = f"http://localhost:{args.port}/?v={digest}"
    result = {
        "viewer_dir": str(out_dir),
        "index": str(index_path),
        "panorama": str(viewer_image),
        "server_command": f"cd {out_dir} && python -m http.server {args.port}",
        "url": url,
        "direct_image_url": f"http://localhost:{args.port}/{cache_busted_name}",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
