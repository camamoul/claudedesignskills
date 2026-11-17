---
name: fast-eevee
description: Fast EEVEE rendering for long Blender 5.3 animations on a laptop GPU (Apple M-series). Use when a full render must finish in about an hour, when EEVEE takes more than a few seconds per frame, or before launching any 1000-plus frame render. Covers a cheap EEVEE preset, rendering only the active 2.39 to 1 image and letterboxing in ffmpeg, keeping shadows on key lights only, per-shot collection hiding, light crowds, measuring seconds per frame before committing, chunked per-shot renders and keeping the Mac awake.
---

# Fast EEVEE

Target: 1080 frames (45 s at 24 fps) in under 60 min means **about 3 s per frame**. Measure, do not guess.

## Budget first
- `total = frames x seconds_per_frame`. 1080 x 3 s = 54 min, 1080 x 10 s = 3 h, 1080 x 60 s = 18 h.
- Shader compilation makes the first frame slow; judge from frames 2+.
- The slowest shot decides the night: benchmark one frame per shot.

## Recipe
1. Remove real volumetrics (world volume, volume scatter cubes): they are the main cost. Replace them with the `fake-volumetrics` skill.
2. Apply the preset and benchmark:
   ```bash
   /Applications/Blender.app/Contents/MacOS/Blender -b scene.blend \
     -P .claude/skills/fast-eevee/scripts/fast_eevee.py -- \
     --apply --samples 16 --res 1920x804 --key-lights key_,rim_ --bench 6 --save
   ```
   The script prints s/frame per sampled frame and the projected total. With camera markers it samples one frame per shot.
3. Too slow? Lower in this order, re-benchmark after each:
   - drop shadows from more lights (`--key-lights` with fewer prefixes): flashes, practicals, chandelier bulbs never need shadows;
   - hide per shot what the camera cannot see (below);
   - crowds: instance a few base dolls (Alt+D linked duplicates / collection instances), subdivision 0 for anything further than 5 m, `scene.render.simplify_subdivision_render = 1`;
   - `--samples 8` for fast-moving shots, keep 16 to 32 for slow close-ups;
   - textures: 2K is enough for anything not in close-up.
4. Never lower: resolution of the active image, colour management, motion of the camera.

## Render the active image only (2.39:1)
Render 1920x804 and add the bars at the end (about 25 % fewer pixels):
```bash
ffmpeg -framerate 24 -i renders/frames/%04d.png \
  -vf "pad=1920:1080:0:138:black" -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p out.mp4
```
(1080 - 804) / 2 = 138.

## Per-shot hiding and chunked renders
Render each shot as its own range so one bad shot can be re-rendered alone, and hide what the shot cannot see:
```python
import bpy
SHOTS = {  # name: (start, end, collections hidden in this shot)
    "s01_ticket": (1, 72, ["Crowd", "Runway", "FX_Beams", "FX_Haze"]),
    "s05_pose":   (241, 312, ["Salon", "Bedroom"]),
}
def render_shot(name):
    s, e, hidden = SHOTS[name]
    sc = bpy.context.scene
    for c in bpy.data.collections:
        c.hide_render = c.name in hidden
    sc.frame_start, sc.frame_end = s, e
    sc.render.filepath = f"//renders/frames/"      # same folder, frame numbers stay global
    bpy.ops.render.render(animation=True)
```
Run shots in sequence from one Blender process; do not launch two EEVEE renders in parallel on one GPU (they fight for VRAM and are rarely faster).

## Keep the Mac awake
```bash
caffeinate -dimsu /Applications/Blender.app/Contents/MacOS/Blender -b scene.blend -a > render.log 2>&1 &
```
The display may turn off; the lid must stay open and the charger plugged in. Resume after an interruption with `-s FIRST_MISSING -e LAST` (keep `use_overwrite = False` and `use_placeholder = True` so finished frames are skipped).

## Checks before launching the night render
- benchmark printed and total accepted;
- `ls renders/frames | wc -l` grows during a 1 min test;
- no warning about volumetrics or shadow-buffer overflow in the log;
- the first and last frame of each shot open correctly.

## Related skills
blender-rendering (presets, compositor), fake-volumetrics (beams and haze without volumes), blender-video-editing (final edit).
