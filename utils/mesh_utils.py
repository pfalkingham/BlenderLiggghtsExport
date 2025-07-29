import bpy
import os

def ensure_stl_export_addon():
    """Ensure the STL export addon is enabled."""
    if not bpy.ops.wm.stl_export.poll():
        bpy.ops.preferences.addon_enable(module="io_mesh_stl")

def export_stl(filepath, objects):
    """Export the given objects as an STL file."""
    ensure_stl_export_addon()
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]  # Set an active object
    bpy.ops.wm.stl_export(filepath=filepath, export_selected_objects=True, ascii_format=True)

def export_rigid_stls(output_dir, objects):
    """Export each object as a separate STL file for rigid meshes."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for obj in objects:
        filepath = os.path.join(output_dir, f"{obj.name}.stl")
        export_stl(filepath, [obj])

def export_deformable_stls(output_dir, objects, frame_start, frame_end):
    """Export objects as STL files for each frame in the range for deformable meshes."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for frame in range(frame_start, frame_end + 1):
        bpy.context.scene.frame_set(frame)
        for obj in objects:
            filepath = os.path.join(output_dir, f"{obj.name}_{frame}.stl")
            export_stl(filepath, [obj])