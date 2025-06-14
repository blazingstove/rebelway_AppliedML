import hou
import json

node = hou.pwd()
geo = node.parent()

# Load the blendshape coefficients exported from mediapipe

mp_face_blendshapes_solve = r"F:\Projects\Rebelway\AppliedML\houdini\data\face_blendshapes.json"
face_blendshapes = []
with open(mp_face_blendshapes_solve, 'r') as f:
    face_blendshapes = json.load(f)

blendshape = geo.node("blendshapes_node") or None
   
# Key frame the blendshape weights as each frame

if blendshape:
    key = hou.Keyframe()
    for i in range(len(face_blendshapes)):
        key.setFrame(i + 1)
        for shape in face_blendshapes[i]:
            if 'neutral' not in shape:
                value = face_blendshapes[i][shape]
                key.setValue(value)
                blendshape.parm(shape).setKeyframe(key)