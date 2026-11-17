"""Rig a Rodin doll GLB with a simple humanoid armature, skin it, add a catwalk cycle, export GLB.

Joints are given as fractions of the doll height (from analyze.py profiles).
Skinning reuses EL4CTEO blender-character-rigging bind_mesh.run (heat weights, voxel-proxy fallback).

Usage: python rig.py DOLL in.glb out.glb SKILLS_DIR
"""
import math
import sys

import bpy
from mathutils import Vector

doll, src, dst, skills = sys.argv[1:5]
sys.path.insert(0, skills + "/blender-character-rigging/scripts")

# (x, y, z) as fractions of height H; -y is the front of the doll.
JOINTS = {
    "kylie": dict(hip=0.47, pelvis=0.49, spine=0.56, chest=0.63, neck=0.74, head=0.775, top=1.0,
                  leg_x=0.045, knee=0.25, ankle=0.045, toe=0.0, toe_y=-0.06,
                  sh_in=(0.035, 0.70), sh=(0.095, 0.655), elbow=(0.132, 0.55), wrist=(0.165, 0.465), tip=(0.18, 0.43)),
    "jade": dict(hip=0.37, pelvis=0.39, spine=0.47, chest=0.58, neck=0.745, head=0.775, top=1.0,
                 leg_x=0.05, knee=0.20, ankle=0.05, toe=0.0, toe_y=-0.07,
                 sh_in=(0.04, 0.70), sh=(0.11, 0.68), elbow=(0.17, 0.575), wrist=(0.225, 0.465), tip=(0.245, 0.43)),
}[doll]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
for o in bpy.context.scene.objects:
    o.select_set(o.type == "MESH")
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
body = bpy.context.view_layer.objects.active
body.parent = None
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
body.name = "Body"
zs = [v.co.z for v in body.data.vertices]
z0 = min(zs)
H = max(zs) - z0
for v in body.data.vertices:
    v.co.z -= z0
print("H", H)

J = JOINTS
P = lambda x, z, y=0.0: Vector((x * H, y * H, z * H))
arm_data = bpy.data.armatures.new("Rig")
rig = bpy.data.objects.new("Rig", arm_data)
bpy.context.collection.objects.link(rig)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode="EDIT")
eb = arm_data.edit_bones


def bone(name, head, tail, parent=None, connect=False):
    b = eb.new(name)
    b.head, b.tail = head, tail
    if parent:
        b.parent = eb[parent]
        b.use_connect = connect
    return b


root = bone("root", P(0, 0), P(0, 0, -0.08))
root.use_deform = False
bone("hips", P(0, J["hip"]), P(0, J["pelvis"]), "root")
bone("spine", P(0, J["pelvis"]), P(0, J["spine"]), "hips", True)
bone("chest", P(0, J["spine"]), P(0, J["chest"]), "spine", True)
bone("neck", P(0, J["chest"]), P(0, J["head"]), "chest", True)
bone("head", P(0, J["head"]), P(0, J["top"]), "neck", True)
for s, side in ((1, "L"), (-1, "R")):  # Blender +X = doll's left (doll faces -Y)
    lx = J["leg_x"] * s
    bone(f"thigh.{side}", P(lx, J["hip"]), P(lx, J["knee"], -0.01), "hips")
    bone(f"shin.{side}", P(lx, J["knee"], -0.01), P(lx, J["ankle"]), f"thigh.{side}", True)
    bone(f"foot.{side}", P(lx, J["ankle"]), P(lx, J["toe"], J["toe_y"]), f"shin.{side}", True)
    bone(f"shoulder.{side}", P(J["sh_in"][0] * s, J["sh_in"][1]), P(J["sh"][0] * s, J["sh"][1]), "chest")
    bone(f"upperarm.{side}", P(J["sh"][0] * s, J["sh"][1]), P(J["elbow"][0] * s, J["elbow"][1], 0.01),
         f"shoulder.{side}", True)
    bone(f"forearm.{side}", P(J["elbow"][0] * s, J["elbow"][1], 0.01), P(J["wrist"][0] * s, J["wrist"][1]),
         f"upperarm.{side}", True)
    bone(f"hand.{side}", P(J["wrist"][0] * s, J["wrist"][1]), P(J["tip"][0] * s, J["tip"][1]),
         f"forearm.{side}", True)
# Consistent rolls: X axis points to world +X so local-X rotation = forward/back swing.
for b in eb:
    b.align_roll(Vector((0, -1, 0)) if abs(b.vector.normalized().z) > 0.7 else Vector((0, 0, 1)))
bpy.ops.object.mode_set(mode="OBJECT")

import bind_mesh  # noqa: E402  (EL4CTEO skill script)

res = bind_mesh.run(armature="Rig", meshes=["Body"], method="auto", limit=4, clean=0.01)
print("bind", {k: v for k, v in res.items() if k != "meshes"} if isinstance(res, dict) else res)

# ---- catwalk cycle (in place; forward travel handled by the scene) ----
FPS, CYCLE = 24, 24  # one full cycle (2 steps) per second
bpy.context.scene.render.fps = FPS
pb = rig.pose.bones
for p in pb:
    p.rotation_mode = "XYZ"
act_frames = range(0, CYCLE + 1, 2)


def key(name, attr, frame, value):
    p = pb[name]
    setattr(p, attr, value)
    p.keyframe_insert(attr, frame=frame)


for f in act_frames:
    t = 2 * math.pi * f / CYCLE
    s = math.sin(t)
    c = math.cos(t)
    # legs: thigh swing, knee bends while swinging forward, feet cross toward center line (catwalk)
    for side, ph in (("L", 0.0), ("R", math.pi)):
        sw = math.sin(t + ph)
        lift = max(0.0, math.sin(t + ph + math.pi / 2))
        key(f"thigh.{side}", "rotation_euler", f, (math.radians(-24 * sw), 0,
                                                    math.radians(6 if side == "L" else -6)))
        key(f"shin.{side}", "rotation_euler", f, (math.radians(38 * lift), 0, 0))
        key(f"foot.{side}", "rotation_euler", f, (math.radians(-12 * sw), 0, 0))
        # arms: relaxed down from the A-pose, gentle counter-swing
        key(f"upperarm.{side}", "rotation_euler", f, (math.radians(14 * sw), 0,
                                                       math.radians(-22 if side == "L" else 22)))
        key(f"forearm.{side}", "rotation_euler", f, (math.radians(-10 - 6 * max(0, sw)), 0, 0))
    # hips: sway side to side + twist, slight bob; chest counter-rotates; head stays level
    key("hips", "rotation_euler", f, (0, math.radians(7 * s), math.radians(5 * c)))
    key("hips", "location", f, (0.012 * H * s, abs(c) * 0.008 * H, 0))
    key("chest", "rotation_euler", f, (math.radians(-3), math.radians(-6 * s), math.radians(-3 * c)))
    key("head", "rotation_euler", f, (math.radians(4), math.radians(-1 * s), math.radians(2 * c)))
for fc in (rig.animation_data.action.fcurves if hasattr(rig.animation_data.action, "fcurves") else []):
    fc.modifiers.new("CYCLES")
rig.animation_data.action.name = "Catwalk"
bpy.context.scene.frame_start, bpy.context.scene.frame_end = 0, CYCLE - 1

bpy.ops.export_scene.gltf(filepath=dst, export_format="GLB", export_animations=True,
                          export_skins=True, export_apply=False)
print("exported", dst)
