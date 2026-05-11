# SceneMakerAI

SceneMakerAI is a Codex skill for turning one image into a single `2:1` equirectangular panorama and immediately previewing it in a local Pannellum viewer.

## What It Does

- Takes one source image as the visual starting point.
- Accepts optional scene instructions, such as adding objects, changing materials, or adjusting the scene.
- Generates one wide `2:1` equirectangular panorama image.
- Saves the final image under the agent's current working directory:

```text
outputs/scenemakerai/<run-id>/panorama.png
```

- Creates a lightweight Pannellum preview automatically.
- Returns a cache-busted localhost preview URL so edits show up promptly.
- Supports follow-up edits by editing the latest panorama and refreshing the preview URL.

## What It Does Not Do

- It does not create walkable 3D geometry.
- It does not output cubemap faces.
- It does not treat generated unseen areas as factual reconstruction.

## Skill Layout

```text
SKILL.md
agents/openai.yaml
references/prompting.md
scripts/prepare_pano_canvas.py
scripts/create_pannellum_viewer.py
```

`SKILL.md` is the main Codex skill file. The scripts handle deterministic canvas preparation and Pannellum viewer generation.

## Basic Use

Ask Codex to use the skill with an image:

```text
Use SceneMakerAI for this image. Add a few helium airships around the skyline.
```

The expected final response includes:

- the saved panorama path
- the local Pannellum preview URL

## Preview Behavior

The viewer helper copies the panorama into the viewer with a content-hashed filename and returns a cache-busted URL, for example:

```text
http://localhost:8000/?v=714c78f44b70
```

This avoids stale browser or Pannellum cache after edits.
