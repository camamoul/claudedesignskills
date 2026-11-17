---
name: fake-volumetrics
description: Fake volumetric light beams, haze and smoke for EEVEE in Blender 5.3 without volume shaders. Use when spotlight beams look blocky, grey or come from nowhere, when volumetrics make a render too slow, or for runway, stage, concert and fashion-show lighting with visible beams. Builds additive emissive cones parented to each spot light with a visible fixture at the source, soft edges and a fade to the floor, plus faint camera-facing haze planes with drifting noise.
---

# Fake Volumetrics

Real volumes in EEVEE are slow and produce grey blocks. A beam that reads as light needs three things: a **visible source**, a **soft edge**, a **fade towards the floor**. This skill builds exactly that.

## Rules of a believable beam
- Every beam starts at a lamp the viewer can see (a black can with a glowing lens). No source, no beam.
- The beam axis is the lamp's real axis, and the lamp really lights the stage: the pool of light on the floor sits where the cone lands.
- Bright at the source, fading to nothing at the floor: never a hard ellipse on the ground.
- Background stays black. Beams read only against dark; if the frame turns grey, the haze is too strong.
- Fewer, stronger beams beat many weak ones. Symmetric pairs for a fashion show.

## Recipe
```bash
/Applications/Blender.app/Contents/MacOS/Blender -b scene.blend \
  -P .claude/skills/fake-volumetrics/scripts/fake_volumetrics.py -- \
  --remove-volumes --beams --prefix spot_ --fixtures --strength 0.3 --haze 3 --save
```
- `--beams` builds one cone per spot light (filter with `--prefix`). Cone length = ray cast from the lamp to the first surface; angle = the spot cone; the cone is parented to the lamp, so animating the lamp moves the beam.
- `--fixtures` adds a black metal can and an emissive lens at each apex.
- `--haze N` adds N faint additive planes parented to the active camera (re-run per camera if the shot changes camera).
- Re-running replaces the previous beams and haze (collections `FX_Beams`, `FX_Haze`).

## Tuning
| Problem | Fix |
|---|---|
| beams too bright / milky | `--strength 0.15` to 0.2, or lower lamp colour value |
| beams invisible | strength 0.5 to 0.8; check the world is near black |
| whole frame grey | `--haze-strength 0.008` or fewer haze planes |
| beam ends in mid-air | nothing under the lamp: aim the lamp at the runway or raise `--max-length` |
| hard edge on the cone | edge power in `beam_material` (default 3; raise to 4) |
| flicker between frames | keep EEVEE samples at 16 or more; the noise is animated slowly on purpose |

## Light the stage for real
The cones are only the visible air. The stage still needs the actual spot lights with shadows on the key ones (see fast-eevee `--key-lights`). Typical runway: 6 to 10 spots in symmetric pairs along the runway, warm 3200 K for the room, cold 5600 K key spots on the walkway, a long emissive light bar on the ceiling for the Saint Laurent look.

## Related skills
fast-eevee (render time), blender-lighting (key, rim, colour temperature), blender-rendering.
