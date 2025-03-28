import bpy
from ..utils.generate_input import generate_input_files

class LIGGGHTS_OT_GenerateDeformableInput(bpy.types.Operator):
    """Generate LIGGGHTS input files for deformable meshes"""
    bl_idname = "liggghts.generate_deformable"
    bl_label = "Generate Deformable Input"

    filepath: bpy.props.StringProperty(subtype='DIR_PATH')

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        output_dir = bpy.path.abspath(self.filepath)
        generate_input_files(context, output_dir, deformable=True)
        self.report({'INFO'}, f"Deformable input files generated in {output_dir}")
        return {'FINISHED'}

# Register the operator
def register():
    bpy.utils.register_class(LIGGGHTS_OT_GenerateDeformableInput)

def unregister():
    bpy.utils.unregister_class(LIGGGHTS_OT_GenerateDeformableInput)