__all__ = [
	"build_root_json"
]

import json, sys, os.path

from .ejson_util import e_print, hash_file
from .ejson_mutation import apply_mutations
from .ejson_variables import build_variables, insert_variables
from .ejson_cycles import find_circular_inheritance
from .ejson_install import install_json

keysNotToInherit = ["file_name", "file_hash", "comment"]

def read_json(JSONFile):
	if os.path.isfile(JSONFile):
		f = open(JSONFile, "r")
		c = f.read()
		f.close()
		
		config = json.loads(c)
		config["file_name"] = JSONFile
		config["file_hash"] = hash_file(JSONFile)
		
		if "data_file" in config.keys():
			config["data"] = read_json(config["data_file"])
		
		if "data" not in config.keys():
			config["data"] = {}
		
		return config
	else:
		e_print("Cannot hash file, no file at \"" + JSONFile + '"')
		return None

def inherit_config(configs, child):
	for k in configs.keys():
		if k == child["extends"]:
			if "extends" in configs[k].keys():
				return False
			
			del child["extends"]
			
			parent = configs[k]["data"]
			child = child["data"]
			
			for l in [x for x in parent.keys() if x not in child.keys() and x not in keysNotToInherit]:
				child[l] = parent[l]
			
			if "mutations" in child.keys():
				apply_mutations(parent, child)
			
			return True

def install_json(config, JSONToInstall):
	install_json(config, JSONToInstall)
	save_config(config, "config.json")
	
def save_config(config, name, pretty_print=True):
	f = open(name, "w")
	if pretty_print:
		f.write(json.dumps(config, indent=4, separators=(',', " : "), sort_keys=True))
	else:
		f.write(json.dumps(config, separators=(',', ':'), sort_keys=True))
	f.close()

def build_root_json(config_location="config.json"):
	config = read_json(config_location)
	config["data"] = {}
	extending_json = []
	for f in config["data_files"]:
		build_json(f)
		current_json = read_json(f)

		if "key" not in current_json.keys():
			print("No \"key\" element in " + f + ", skipping.")
			continue
		else:
			config["data"][current_json["key"]] = current_json
		
		if "data" in current_json.keys() and "variables" in current_json["data"].keys():
			current_json["data"]["variables"] = build_variables(current_json["data"]["variables"])
			insert_variables(current_json["data"]["variables"], current_json["data"])
		
		if "extends" in current_json.keys():
			extending_json.append(current_json)

	circularExtendGroup = find_circular_inheritance(config["data"])
	if circularExtendGroup is not None:
		print("Circular variable reference detected:")
		for r in circularExtendGroup[0:-1]:
			print(str(r))
		print(circularExtendGroup[-1])
		sys.exit(0)

	while len(extending_json) > 0:
		completedExtends = []
		for e in extending_json:
			if inherit_config(config["data"], e):
				completedExtends.append(e)
		for e in completedExtends:
			extending_json.remove(e)

	for k in config["data"].keys():
		if "data" in config["data"][k].keys() and "variables" in config["data"][k].keys():
			config["data"][k]["data"]["variables"] = build_variables(config["data"][k]["data"]["variables"])
			insert_variables(config["data"][k]["data"]["variables"], config["data"][k]["data"])

	save_config(config, "built_json.json")

	return config

def build_json(jsonLocation):
	return