"""Import a doll GLB and print a height profile (x-extent clusters per z slice) to place joints.
Usage: python analyze.py model.glb"""
import sys, bpy
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=sys.argv[1])
obs=[o for o in bpy.context.scene.objects if o.type=='MESH']
pts=[]
for o in obs:
    m=o.matrix_world
    pts+= [m@v.co for i,v in enumerate(o.data.vertices) if i%7==0]
zs=[p.z for p in pts]; z0,z1=min(zs),max(zs); H=z1-z0
print("bounds x",min(p.x for p in pts),max(p.x for p in pts),"y",min(p.y for p in pts),max(p.y for p in pts),"z",z0,z1)
N=40
for i in range(N):
    a=z0+H*i/N; b=a+H/N
    xs=sorted(p.x for p in pts if a<=p.z<b)
    if not xs: continue
    cl=[[xs[0],xs[0]]]
    for x in xs[1:]:
        if x-cl[-1][1]>0.015*H: cl.append([x,x])
        else: cl[-1][1]=x
    print(f"{(i+0.5)/N:5.3f}h  " + "  ".join(f"[{c[0]/H:+.3f},{c[1]/H:+.3f}]" for c in cl))
