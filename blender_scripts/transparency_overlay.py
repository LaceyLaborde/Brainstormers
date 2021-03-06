import bpy
import random
from random import randint

scene = bpy.context.scene
initial_transparency = .3
object_count = len(scene.objects)
transparency_decrease = initial_transparency/len(scene.objects)

def sort_by_volume(objects):
	volumes = {}
	for obj in objects:
		volume = obj.dimensions[0] * obj.dimensions[1] * obj.dimensions[2]
		volumes[obj] = volume
	return sorted(volumes.items(), key=lambda x:x[1])

def set_color(obj):
	obj.active_material.diffuse_color = get_color()

def get_color():
	color1 = randint(0, 10) / 10
	color2 = randint(0, 10) / 10
	color3 = randint(0, 10) / 10
	return (color1, color2, color3)

def modify_objects(sortedVolumeTuples):
	transparency = initial_transparency
	for volumeTuple in sortedVolumeTuples:
		current_object = volumeTuple[0]
		if is_not_lamp_or_camera(current_object):
			if current_object.active_material is None:
				add_material(current_object)
			set_active_material(current_object, transparency);
			orient(current_object)
			set_color(current_object)
			transparency -= transparency_decrease

def is_not_lamp_or_camera(obj):
	return obj.type != 'LAMP' and obj.type != 'CAMERA'

def add_material(obj):
		material = bpy.data.materials.new('material for ' + obj.name)
		obj.data.materials.append(material)

def set_active_material(obj, transparency):
		obj.active_material.use_transparency = True
		obj.active_material.alpha = transparency

def orient(obj):
	scene.objects.active = obj
	bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
	obj.select = True
	obj.location[0]=0
	obj.location[1]=0
	obj.location[2]=0
	obj.rotation_euler[0]=0


def add_lamp():
	for obj in scene.objects:
		if obj.type == 'LAMP':
			return
	create_lamp()

def create_lamp():
	lamp_block = bpy.data.lamps.new(name="New Lamp", type="POINT")
	lamp_object = bpy.data.objects.new(name="Point", object_data=lamp_block)
	scene.objects.link(lamp_object)

def add_sun():
	for obj in scene.objects:
		if obj.type == 'LAMP' and obj.name == 'Sun':
			return
	create_sun()

def create_sun():
	sun_block = bpy.data.lamps.new(name="Sun", type="SUN")
	sun_object = bpy.data.objects.new(name="Sun", object_data=sun_block)
	scene.objects.link(sun_object)
	sun_object.location = (1000, 1000, 1000)

def run():
	add_lamp()
	add_sun()
	sortedVolumes = sort_by_volume(scene.objects)
	modify_objects(sortedVolumes)
	print("Congrats - success!")

run()