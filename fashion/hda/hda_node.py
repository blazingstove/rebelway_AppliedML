# NOTE: This python block lives in the PythonModule of the HDA in the scene
# Provided here for review

import hou
import os
import sys

hip_dir = os.path.dirname(hou.hipFile.path())
sys.path.append(os.path.join(hip_dir))
sys.path.append(os.path.join(hip_dir,'hda'))

from image_identify_hda import (identify_drawing, identify_image)