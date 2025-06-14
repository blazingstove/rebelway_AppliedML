import hou
import os
from glob import glob

# Local path to ARKit blendshapes

base_path = r"F:\Projects\Rebelway\AppliedML\data\ARKitOBJ\*obj"
base_name = "Neutral"

all_files = []
neutral_path=''
for strOBJPath in sorted(glob(base_path)):
    if base_name in os.path.basename(strOBJPath):
        neutral_path = strOBJPath
    else:
        all_files.append(strOBJPath)

# Create blendshape subnet in the current geometry node

node = hou.pwd()
geo = node.parent()

if not geo.node("blendshapes_node"):

    blendshape_sop = geo.createNode("blendshapes::2.0", "blendshapes_node")
    
    # Load neutral mesh
    
    file_neutral = geo.createNode("file", "base_shape")
    file_neutral.parm("file").set(neutral_path)
    blendshape_sop.setInput(0, file_neutral)
    
    # Load each shape and connect it to blendshapes node
    for i, shape_file in enumerate(all_files):
        name = os.path.basename(shape_file.split('.')[0])
        file_node = geo.createNode("file", name)
        file_node.parm("file").set(shape_file)
        blendshape_sop.setInput(i + 1, file_node)
    
    # Layout nodes
    
    geo.layoutChildren()

else:
    print('Blendshape node already setup!')