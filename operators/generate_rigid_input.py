import bpy
import os
from ..utils.generate_input import generate_input_files

class LIGGGHTS_OT_GenerateRigidInput(bpy.types.Operator):
    """Generate LIGGGHTS input files for rigid meshes"""
    bl_idname = "liggghts.generate_rigid"
    bl_label = "Generate Rigid Input"

    filepath: bpy.props.StringProperty(subtype='DIR_PATH')

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        output_dir = bpy.path.abspath(self.filepath)
        generate_input_files(context, output_dir, deformable=False)
        self.report({'INFO'}, f"Rigid input files generated in {output_dir}")
        return {'FINISHED'}

# Register the operator
def register():
    bpy.utils.register_class(LIGGGHTS_OT_GenerateRigidInput)

def unregister():
    bpy.utils.unregister_class(LIGGGHTS_OT_GenerateRigidInput)