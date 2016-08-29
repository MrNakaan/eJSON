import os.path, json

from ejson_util import hashFile, ePrint

def isValidPath(JSONInput):
	# Accept file paths only
	if os.path.isfile(JSONInput):
		return True
	else:
		return False

def installJSON(config, JSONToInstall):
	if not (isinstance(JSONToInstall, list) or isinstance(JSONToInstall, tuple) or isinstance(JSONToInstall, range)):
		JSONToInstall = [JSONToInstall]
	for j in JSONToInstall:
		if not isValidPath(j):
			ePrint("Invalid path given for installation. Path: \"" + j + '"')
			continue
		config["data_files"].append(j)
	config["file_hash"] = hashFile(config["file_name"])
