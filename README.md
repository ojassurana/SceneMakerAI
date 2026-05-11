# SceneMakerAI

[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-black)](https://github.com/topics/agent-skills)
[![Codex](https://img.shields.io/badge/Built%20for-Codex-111111)](https://github.com/topics/codex-skills)
[![Install with skills](https://img.shields.io/badge/install%20with-skills.sh-000000)](https://skills.sh)

**Turn any 2D image into a world you can look around in.**

Give Codex an image, describe how you want the world to feel, and get back an **interactive 360 preview**.

Start with any scene. Then **ITERATE** with plain-English edits: add UFOs, turn a lake pink, or change the mood.

**No 3D modeling. No scene setup. Just image in, world out, preview live.**

## Install

Method 1: ask your agent to install it.

```text
Install this skill:
https://github.com/ojassurana/SceneMakerAI
```

Method 2: use the skills CLI with `npx`.

```bash
npx skills add ojassurana/SceneMakerAI --skill scenemakerai
```

## Examples

<table>
  <tr>
    <th width="50%">Desert Mesa</th>
    <th width="50%">Moraine Lake</th>
  </tr>
  <tr>
    <td width="50%">
      <img src="./assets/example-input.png" alt="Desert mesa input image">
    </td>
    <td width="50%">
      <img src="./assets/example-2-input.jpg" alt="Moraine Lake input image">
    </td>
  </tr>
  <tr>
    <td width="50%">
      <strong>Prompt</strong><br>
      <code>Make a 3D world for this image. <strong>Add 2 big ufos in the appropriate places.</strong></code>
    </td>
    <td width="50%">
      <strong>Prompt</strong><br>
      <code>Make a 3D world for this image. <strong>Make it a pink lake instead.</strong></code>
    </td>
  </tr>
  <tr>
    <td width="50%"><img src="./assets/example-demo.gif" alt="SceneMakerAI desert world preview"></td>
    <td width="50%"><img src="./assets/example-2-demo.gif" alt="SceneMakerAI lake world preview"></td>
  </tr>
</table>

## What It Does

- Turns one image into an interactive 360-style world.
- Lets you describe edits in plain language.
- Supports follow-up iterations after the first preview.
- Automatically hosts a local preview URL.
- Refreshes the preview with cache-busted URLs so edits show up promptly.

## What It Does Not Do

- It does not create walkable 3D geometry.
- It does not output cubemap faces.
- It does not treat generated unseen areas as factual reconstruction.

## Technical Output

SceneMakerAI generates one `2:1` spherical equirectangular environment-map image and previews it with Pannellum. It is still a flat image file, but it is authored to wrap inside a 360 viewer sphere, not to behave like a normal wide scenic banner.

The final image is saved under the agent's current working directory:

```text
outputs/scenemakerai/<run-id>/panorama.png
```

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
