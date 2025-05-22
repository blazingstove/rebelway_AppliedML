"""
hou_a_star.py

Animates one or more NPC nodes to reach a target "main character" node
within a maze.

Usage Notes:

    This code should be copy/pasted into the HDA's python Script panel 
    in the "maze assignment" Houdini scene.

    NOTE: The "a_star.py" must be in the same folder as the .hip file or in "scripts" subfolder

"""

import os
import hou
import math
import sys

# Ensure local project path is added for module import

hip_dir = os.path.dirname(hou.hipFile.path())
sys.path.append(os.path.join(hip_dir))
sys.path.append(os.path.join(hip_dir,'scripts'))

from a_star import AStarPathFinding

def get_maze_from_grid():
    
    """ Return a matrix of maze non-wall grid positions from the grid 
    object in the scene """
    
    grid = hou.pwd().parm('grid_path').eval()
    geo = hou.node(grid).geometry()
    prims = geo.prims()
    num_rows = num_columns = int(math.sqrt(len(prims)))
    
    grid_matrix = []
    
    for row in range(num_rows):
        new_row = []
        for col in range(num_columns):
            prim_index = row * num_columns + col
            prim = geo.prim(prim_index)
            color = prim.attribValue("Cd")
            new_row.append(1 if color == (1.0,1.0,1.0) else 0)
        grid_matrix.append(new_row)

    return grid_matrix
    
def keyframe_results(node, path_steps):

    """ Keyframe the transformof the input node in the scene 
    at each position in the input path_step list.
    
    Args:
        node (object) : houdini object to keyframe transform on
        
        path_steps (list of lists): list of positional lists defining 
                                    each step along the solved path
                                    
    """
    
    node_pos = node.parmTuple("t")
        
    for frame, pos in enumerate(path_steps):
        node_pos[0].setKeyframe(hou.Keyframe(pos[0], frame))
        node_pos[2].setKeyframe(hou.Keyframe(pos[1], frame))
        
    hou.setFrame(0)
    
def get_node_for_parm(char_parm):
    """ Return the houdini node that matches the object path on the input
    string parameter at this node """
    
    try:
    
        char_path = hou.pwd().parm(char_parm).eval()
        char = hou.node(char_path)
        return char
    
    except ValueError:
    
        assert(f'Issue encountered evaluating {char_parm}')
        
def get_row_col_tup(node):
    """ Return a row/col tuple for input node's X/Z translation values """

    pos = node.parmTuple("t").eval()
    return (int(pos[0]), int(pos[2]))
               
def solve_maze():
    """ Generate a series of path steps through the maze so that each 
    NPC can reach the main character and then keyframe each NPC's position
    along the solved path. 
    
    """ 
    
    maze = get_maze_from_grid()
    main_char = get_node_for_parm("main_char")
    target_pos = get_row_col_tup(main_char)
    
    num_npc = hou.pwd().parm("npcs").eval()
    
    for iIndex in range(1, num_npc + 1):
        
        npc = get_node_for_parm(f"npc_{iIndex}")
        npc_pos = get_row_col_tup(npc)
        
        path_finder = AStarPathFinding(maze, npc_pos, target_pos)
        path_steps = path_finder.find_path()
        
        keyframe_results(npc, path_steps)