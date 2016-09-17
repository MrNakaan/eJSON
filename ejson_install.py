import os.path

from .ejson_util import e_print, hash_file

def is_valid_path(json_location):
	# Accept file paths only
	if os.path.isfile(json_location):
		return True
	else:
		return False

def install_json(config, json_to_install):
	if not (isinstance(json_to_install, list) or isinstance(json_to_install, tuple) or isinstance(json_to_install, range)):
		json_to_install = [json_to_install]
	for j in json_to_install:
		if not is_valid_path(j):
			e_print("Invalid path given for installation. Path: \"" + j + '"')
			continue
		config["data_files"].append(j)
	config["file_hash"] = hash_file(config["file_name"])
