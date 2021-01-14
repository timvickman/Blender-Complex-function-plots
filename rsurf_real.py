# Imports:
from typing import Any

import bpy
import bmesh
import numpy as np


bl_info = {
    "name": "Riemann Surface (Real)",
    "description": "Plots a complex-valued function. Z coordinate represents the real component of the output.",
    "author": "Lemmaxiom",
    "version": (1, 0),
    "blender": (2, 91, 0),
    "location": "View3D > Add > Mesh",
    "category": "Add Mesh"
}

class MESH_OT_real_rsurf(bpy.types.Operator):
    """Create a Riemann Surface (Real Representation)"""   # Operator tool-tips description
    bl_idname = "mesh.riemann_real_add"     # Operator ID name (for typing in console)
    bl_label = "Real Riemann Surface"          # Operator name (for searching using F3 shortcut)
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

# Defining adjustable properties that appear in the undo panel in the viewport:

    sub_num: bpy.props.IntProperty(
        name="Subdivisions",
        description = "Assigns the number of subdivisions for the plane.",
        default=32,
        min=0,soft_max=128)
            
    x_size: bpy.props.FloatProperty(
        name="Size X",
        description = "Determines size of the plane in the x-direction.",
        default=1,
        min=0,soft_max=10)
        
    y_size: bpy.props.FloatProperty(
        name="Size Y",
        description = "Determines size of the plane in the y-direction.",
        default=1,
        min=0,soft_max=10)
        
    x_loc: bpy.props.FloatProperty(
        name="Location: X",
        description = "Moves plane along the x-axis.",
        default=0,
        soft_min=-20,soft_max=20)
        
    y_loc: bpy.props.FloatProperty(
        name ="Location: Y",
        description = "Moves plane along the y-axis.",
        default = 0,
        soft_min = -20,soft_max=20)
        
    function: bpy.props.StringProperty(
        name="Function",
        description = "Defines the function. Variable must be 'z' and requires use of numpy operations (make sure to type 'np.' before functions)",
        default = "np.log(z)/np.cosh(z)")

# Executing the code:

    def execute(self, context):

        function = self.function
        
        bpy.ops.mesh.primitive_plane_add()  # Adds in a plane to work with
       
        me = bpy.context.active_object.data  # Selects the plane's data

        bm = bmesh.new()   # Creates an empty BMesh
        bm.from_mesh(me)   # Fills it in using the plane 

        plane_size = [self.x_size, self.y_size, 1]  # Takes user inputs
        
        location = [self. x_loc, self.y_loc, 1]  # Takes user inputs
        
# Subdividing, scaling, and moving the plane according to user inputs:  
             
        bmesh.ops.subdivide_edges(bm,edges=bm.edges,cuts=self.sub_num,use_grid_fill=True)

        bmesh.ops.scale(bm,vec=plane_size,verts=bm.verts)
        
        bmesh.ops.translate(bm,vec=location,verts=bm.verts)

# Defining a grid of complex points and computing the user's function:

        for v in bm.verts:
            X,Y = np.meshgrid(v.co.x, v.co.y)
            z = X + 1j*Y

# Need to use compile() to convert the input string into a code object,
# then finally the eval() function to get a viable complex-valued output:

            result = compile(function,'','eval')
            func = eval(result)
            
# "v.co.z", the z-coordinate of each vertex, represents the absolute value of the function's output:

            v.co.z = np.real(func)
            
        bm.to_mesh(me)  # Freeing the BMesh, moving on to coloring the domain
        bm.free()

# Setting to object mode:

        bpy.ops.object.mode_set(mode='OBJECT')
                
        return {'FINISHED'}

# Adding an "add mesh" button to the UI menu:

def add_button(self,context):
    self.layout.operator(
        MESH_OT_real_rsurf.bl_idname,
        text = "Riemann Surface (Real)",
        icon = 'SURFACE_NSURFACE')

def register():
    bpy.utils.register_class(MESH_OT_real_rsurf)
    bpy.types.VIEW3D_MT_mesh_add.append(add_button)

def unregister():
    bpy.utils.unregister_class(MESH_OT_real_rsurf)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_button)
if __name__ == "__main__":
    register()