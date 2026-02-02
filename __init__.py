import bpy
from .ui import LIGGGHTS_PT_MainPanel
from .operators.generate_rigid_input import LIGGGHTS_OT_GenerateRigidInput
from .operators.generate_deformable_input import LIGGGHTS_OT_GenerateDeformableInput
from .utils.file_writer import write_setup_file, write_run_file
from .utils.generate_input import LIGGGHTS_OT_GenerateInput

bl_info = {
    "name": "LIGGGHTS Addon",
    "author": "Your Name",
    "version": (2, 0, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Tool Shelf > LIGGGHTS Tab",
    "description": "Addon for generating LIGGGHTS input files.",
    "warning": "",
    "wiki_url": "https://example.com",
    "tracker_url": "https://example.com/issues",
    "category": "Import-Export",
}

class LIGGGHTS_MovingObjectItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Object Name")

def get_timestep_str(self):
    return "{:.6e}".format(self.liggghts_timestep)

def set_timestep_str(self, value):
    try:
        self.liggghts_timestep = float(value)
    except ValueError:
        pass

def register_properties():
    bpy.utils.register_class(LIGGGHTS_MovingObjectItem)
    bpy.types.Scene.liggghts_moving_objects = bpy.props.CollectionProperty(type=LIGGGHTS_MovingObjectItem)
    bpy.types.Scene.liggghts_moving_objects_index = bpy.props.IntProperty()

    bpy.types.Scene.liggghts_tray = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.liggghts_insertion_volume = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.liggghts_simulation_volume = bpy.props.PointerProperty(type=bpy.types.Object)

    bpy.types.Scene.liggghts_radius = bpy.props.FloatProperty(name="Radius", default=0.001, precision=6)
    bpy.types.Scene.liggghts_timestep = bpy.props.FloatProperty(name="Timestep", default=0.000001, precision=15)
    bpy.types.Scene.liggghts_timestep_str = bpy.props.StringProperty(
        name="Timestep", 
        get=get_timestep_str, 
        set=set_timestep_str, 
        description="Timestep in scientific notation"
    )
    bpy.types.Scene.liggghts_youngs_modulus = bpy.props.FloatProperty(name="Young's Modulus", default=5.0e7)
    bpy.types.Scene.liggghts_cohesion = bpy.props.FloatProperty(name="Cohesion", default=75000)
    bpy.types.Scene.liggghts_poisson_ratio = bpy.props.FloatProperty(name="Poisson Ratio", default=0.4)
    bpy.types.Scene.liggghts_framerate = bpy.props.FloatProperty(name="Framerate", default=250.0, precision=1)

def unregister_properties():
    del bpy.types.Scene.liggghts_moving_objects
    del bpy.types.Scene.liggghts_moving_objects_index

    del bpy.types.Scene.liggghts_timestep_str
    del bpy.types.Scene.liggghts_tray
    del bpy.types.Scene.liggghts_insertion_volume
    del bpy.types.Scene.liggghts_simulation_volume

    del bpy.types.Scene.liggghts_radius
    del bpy.types.Scene.liggghts_timestep
    del bpy.types.Scene.liggghts_youngs_modulus
    del bpy.types.Scene.liggghts_cohesion
    del bpy.types.Scene.liggghts_poisson_ratio
    del bpy.types.Scene.liggghts_framerate

    bpy.utils.unregister_class(LIGGGHTS_MovingObjectItem)

class LIGGGHTS_OT_AddMovingObject(bpy.types.Operator):
    """Add selected objects to the moving objects list"""
    bl_idname = "liggghts.add_moving_object"
    bl_label = "Add Moving Object"

    def execute(self, context):
        scene = context.scene
        existing_names = {item.name for item in scene.liggghts_moving_objects}
        for obj in context.selected_objects:
            if obj.name not in existing_names:
                item = scene.liggghts_moving_objects.add()
                item.name = obj.name
        return {'FINISHED'}

class LIGGGHTS_OT_RemoveMovingObject(bpy.types.Operator):
    """Remove selected objects from the moving objects list"""
    bl_idname = "liggghts.remove_moving_object"
    bl_label = "Remove Moving Object"

    def execute(self, context):
        scene = context.scene
        index = scene.liggghts_moving_objects_index
        if 0 <= index < len(scene.liggghts_moving_objects):
            scene.liggghts_moving_objects.remove(index)
        return {'FINISHED'}

class LIGGGHTS_OT_SetTray(bpy.types.Operator):
    """Set the selected object as the tray"""
    bl_idname = "liggghts.set_tray"
    bl_label = "Set Tray"

    def execute(self, context):
        scene = context.scene
        if context.object:
            scene.liggghts_tray = context.object
        return {'FINISHED'}

class LIGGGHTS_OT_SetInsertionVolume(bpy.types.Operator):
    """Set the selected object as the insertion volume"""
    bl_idname = "liggghts.set_insertion_volume"
    bl_label = "Set Insertion Volume"

    def execute(self, context):
        scene = context.scene
        if context.object:
            scene.liggghts_insertion_volume = context.object
        return {'FINISHED'}

class LIGGGHTS_OT_SetSimulationVolume(bpy.types.Operator):
    """Set the selected object as the simulation volume"""
    bl_idname = "liggghts.set_simulation_volume"
    bl_label = "Set Simulation Volume"

    def execute(self, context):
        scene = context.scene
        if context.object:
            scene.liggghts_simulation_volume = context.object
        return {'FINISHED'}

# Register the addon components
def register():
    register_properties()
    bpy.utils.register_class(LIGGGHTS_PT_MainPanel)
    bpy.utils.register_class(LIGGGHTS_OT_AddMovingObject)
    bpy.utils.register_class(LIGGGHTS_OT_RemoveMovingObject)
    bpy.utils.register_class(LIGGGHTS_OT_SetTray)
    bpy.utils.register_class(LIGGGHTS_OT_SetInsertionVolume)
    bpy.utils.register_class(LIGGGHTS_OT_SetSimulationVolume)
    bpy.utils.register_class(LIGGGHTS_OT_GenerateInput)


def unregister():
    unregister_properties()
    bpy.utils.unregister_class(LIGGGHTS_PT_MainPanel)
    bpy.utils.unregister_class(LIGGGHTS_OT_AddMovingObject)
    bpy.utils.unregister_class(LIGGGHTS_OT_RemoveMovingObject)
    bpy.utils.unregister_class(LIGGGHTS_OT_SetTray)
    bpy.utils.unregister_class(LIGGGHTS_OT_SetInsertionVolume)
    bpy.utils.unregister_class(LIGGGHTS_OT_SetSimulationVolume)
    bpy.utils.unregister_class(LIGGGHTS_OT_GenerateInput)

if __name__ == "__main__":
    register()