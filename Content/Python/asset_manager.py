import unreal
import json
from os import path


# Import an asset from export-state.json set inside app
def import_asset():

    print('Asset Manager: Importing asset...')

    # Get path to asset manager state
    asset_manager_state_path = path.expandvars(r'%APPDATA%\asset-manager\state.json')

    # Load asset_manager_export_state json
    asset_manager_state = json.load(open(asset_manager_state_path))

    # Get path to asset manager export state
    asset_manager_export_state_path = path.expandvars(r'%APPDATA%\asset-manager\export-state.json')

    # Load asset_manager_export_state json
    asset_manager_export_state = json.load(open(asset_manager_export_state_path))

    # Define variables used in import
    asset_name = asset_manager_export_state['name']
    destination_path = '/Game/' + asset_manager_state['setting']['ueSettings']['ueExportDirectoryName'] + '/'\
                       + asset_name

    # Create mesh import task
    mesh_task = import_mesh(destination_path, asset_manager_export_state['model']['path'])

    # Create texture import tasks
    albedo_task = import_texture(destination_path, asset_manager_export_state['albedo']['path'])
    metalness_task = import_texture(destination_path, asset_manager_export_state['metalness']['path'])
    roughness_task = import_texture(destination_path, asset_manager_export_state['roughness']['path'])
    normal_task = import_texture(destination_path, asset_manager_export_state['normal']['path'])

    # Run tasks
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([
        mesh_task, albedo_task, metalness_task, roughness_task, normal_task
    ])

    # Get parent material for new material instance
    base_material = unreal.load_asset('/AssetManager/BaseMaterials/M_BaseSurface')

    # Albedo
    albedo = unreal.load_asset(destination_path + '/' + asset_name + '_Albedo')
    albedo_parameter = unreal.TextureParameterValue(
        parameter_info=unreal.MaterialParameterInfo(name='albedo'),
        parameter_value=albedo
    )

    # Metalness
    metalness = unreal.load_asset(destination_path + '/' + asset_name + '_Metalness')
    metalness.set_editor_property('defer_compression', True)
    metalness.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_BC7)
    metalness.set_editor_property('srgb', False)
    metalness_parameter = unreal.TextureParameterValue(
        parameter_info=unreal.MaterialParameterInfo(name='metalness'),
        parameter_value=metalness
    )

    # Roughness
    roughness = unreal.load_asset(destination_path + '/' + asset_name + '_Roughness')
    roughness.set_editor_property('defer_compression', True)
    roughness.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_BC7)
    roughness.set_editor_property('srgb', False)
    roughness_parameter = unreal.TextureParameterValue(
        parameter_info=unreal.MaterialParameterInfo(name='roughness'),
        parameter_value=roughness
    )

    # Normal
    normal = unreal.load_asset(destination_path + '/' + asset_name + '_Normal')
    normal_parameter = unreal.TextureParameterValue(
        parameter_info=unreal.MaterialParameterInfo(name='normal'),
        parameter_value=normal
    )

    # Build an array containing all texture parameters for asset material instance
    texture_parameters = [albedo_parameter, metalness_parameter, roughness_parameter, normal_parameter]

    # Try to create material instance
    material_instance = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        'M_' + asset_name, destination_path, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew()
    )

    # If material instance already exists
    if material_instance is None:
        material_instance = unreal.load_asset(destination_path + '/' + 'M_' + asset_name)

    # Assign parameters to material instance
    material_instance.set_editor_property('parent', base_material)
    material_instance.set_editor_property('texture_parameter_values', texture_parameters)

    # Load mesh and assign it material instance
    mesh = unreal.load_asset(destination_path + '/SM_' + asset_name + '_LOD0')
    mesh.set_material(0, material_instance)


# Import mesh
def import_mesh(destination_path, mesh_path):

    print('Asset Manager: Importing mesh...')

    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', '')
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('filename', mesh_path)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('save', False)

    options = unreal.FbxImportUI()
    options.import_materials = False

    task.set_editor_property('options', options)

    return task


# Import a texture
def import_texture(destination_path, texture_path):

    print('Asset Manager: Importing texture ' + texture_path)

    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', '')
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('filename', texture_path)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('save', False)

    return task
