#!/usr/bin/env python3
"""
Fast EEVEE preset + render-time benchmark for Blender 5.3.

Applies a low-cost EEVEE preset to the open .blend (or the scene built by a
script that ran before this one), then optionally renders a few sample frames
to measure seconds per frame and project the total render time.

Run inside Blender (not plain python):
    Blender -b scene.blend -P fast_eevee.py -- --apply --save
    Blender -b scene.blend -P fast_eevee.py -- --apply --bench 6
    Blender -b scene.blend -P fast_eevee.py -- --apply --samples 24 --res 1920x804 \
        --key-lights key_,rim_,spot_ --save

Arguments (after --):
    --apply            apply the fast preset (otherwise only benchmark)
    --samples N        EEVEE render samples (default 16; 8 for previews, 32 if noisy)
    --res WxH          output resolution (default 1920x804 = 2.39:1 active image,
                       letterbox bars are added later in ffmpeg)
    --key-lights a,b   only lights whose name starts with one of these prefixes
                       keep shadows; every other light loses its shadow
                       (default: keep all shadows)
    --bench N          render N frames spread over the frame range (or one per
                       camera marker if markers exist) and print a time estimate
    --save             save the .blend after applying
Exit code 0 on success, 1 on bad arguments.
"""
import os
import sys
import tempfile
import time

try:
    import bpy
except ImportError:
    sys.exit("Run this inside Blender: Blender -b scene.blend -P fast_eevee.py -- --apply")

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def opt(name, default=None, flag=False):
    if name not in ARGS:
        return False if flag else default
    if flag:
        return True
    i = ARGS.index(name)
    if i + 1 >= len(ARGS):
        sys.exit(f"missing value after {name}")
    return ARGS[i + 1]


def apply_preset(scene, samples, res, key_prefixes):
    scene.render.engine = "BLENDER_EEVEE"
    e = scene.eevee
    e.taa_render_samples = samples
    e.use_raytracing = False          # screen-space only; big saving
    e.use_fast_gi = False
    e.use_shadows = True
    e.shadow_ray_count = 1
    e.shadow_step_count = 4
    e.shadow_resolution_scale = 0.5
    e.use_volumetric_shadows = False
    e.volumetric_samples = 16         # only matters if a volume is left in the scene
    e.volumetric_tile_size = "16"
    e.light_threshold = 0.1
    scene.render.use_motion_blur = False
    scene.render.use_simplify = True
    scene.render.simplify_subdivision_render = min(scene.render.simplify_subdivision_render, 2)
    w, h = (int(v) for v in res.lower().split("x"))
    scene.render.resolution_x, scene.render.resolution_y = w, h
    scene.render.resolution_percentage = 100
    img = scene.render.image_settings
    img.file_format = "PNG"
    img.color_mode = "RGB"
    img.color_depth = "8"
    img.compression = 15              # fast PNG writes
    kept = dropped = 0
    for light in bpy.data.lights:
        if key_prefixes and not any(light.name.startswith(p) or
                                    any(o.name.startswith(p) for o in bpy.data.objects if o.data == light)
                                    for p in key_prefixes):
            light.use_shadow = False
            dropped += 1
        else:
            kept += 1
    volumes = [o.name for o in scene.objects
               if o.type == "MESH" and any(s.material and s.material.node_tree and
                                           s.material.node_tree.nodes.get("Material Output") and
                                           s.material.node_tree.nodes["Material Output"].inputs["Volume"].is_linked
                                           for s in o.material_slots)]
    world = scene.world
    world_volume = bool(world and world.node_tree and any(
        n.type == "OUTPUT_WORLD" and n.inputs["Volume"].is_linked for n in world.node_tree.nodes))
    print(f"[fast-eevee] samples={samples} res={w}x{h} shadows kept={kept} dropped={dropped}")
    if volumes or world_volume:
        print(f"[fast-eevee] WARNING volumetrics still present: objects={volumes} world={world_volume}. "
              "Replace with fake-volumetrics for speed.")


def bench_frames(scene, n):
    markers = sorted((m for m in scene.timeline_markers if m.camera), key=lambda m: m.frame)
    if markers:
        ends = [m.frame for m in markers[1:]] + [scene.frame_end + 1]
        frames = [(m.frame + e) // 2 for m, e in zip(markers, ends)]
    else:
        span = scene.frame_end - scene.frame_start
        frames = [scene.frame_start + round(span * (i + 0.5) / n) for i in range(n)]
    return frames


def bench(scene, n):
    frames = bench_frames(scene, n)
    tmp = tempfile.mkdtemp(prefix="fast_eevee_")
    old = scene.render.filepath
    times = []
    # warm-up render: shader compilation is not representative of steady state
    scene.frame_set(frames[0])
    scene.render.filepath = os.path.join(tmp, "warmup.png")
    bpy.ops.render.render(write_still=True)
    for f in frames:
        scene.frame_set(f)
        scene.render.filepath = os.path.join(tmp, f"f{f:05d}.png")
        t = time.time()
        bpy.ops.render.render(write_still=True)
        dt = time.time() - t
        times.append(dt)
        print(f"[fast-eevee] frame {f}: {dt:.2f} s")
    scene.render.filepath = old
    total_frames = scene.frame_end - scene.frame_start + 1
    avg = sum(times) / len(times)
    print(f"[fast-eevee] avg {avg:.2f} s/frame, worst {max(times):.2f} s; "
          f"{total_frames} frames -> about {avg * total_frames / 60:.0f} min "
          f"(worst case {max(times) * total_frames / 60:.0f} min). Samples in {tmp}")
    return avg


def main():
    scene = bpy.context.scene
    try:
        samples = int(opt("--samples", 16))
        res = opt("--res", "1920x804")
        n = int(opt("--bench", 0))
    except ValueError as err:
        print(f"bad argument: {err}")
        sys.exit(1)
    keys = [p for p in (opt("--key-lights", "") or "").split(",") if p]
    if opt("--apply", flag=True):
        apply_preset(scene, samples, res, keys)
    if opt("--save", flag=True) and bpy.data.filepath:
        bpy.ops.wm.save_mainfile()
        print(f"[fast-eevee] saved {bpy.data.filepath}")
    if n > 0:
        bench(scene, n)


main()
