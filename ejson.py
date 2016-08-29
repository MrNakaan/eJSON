import json, sys

from ejson_util import hashFile, ePrint
from ejson_mutation import applyConfigMutations
from ejson_variables import buildVariables, insertVariables
from ejson_cycles import findCircularInheritance
import ejson_install

keysNotToInherit = ["file_name", "file_hash", "comment"]

def readJSON(configFile):
	if os.path.isfile(JSONFile):
		f = open(configFile, "r")
		c = f.read()
		f.close()
		
		config = json.loads(c)
		config["file_name"] = configFile
		config["file_hash"] = hashFile(configFile)
		
		if "data_file" in config.keys():
			config["data"] = readJSON(config["data_file"])
		
		if "data" not in config.keys():
			config["data"] = {}
		
		return config
	else:
		ePrint("Cannot hash file, no file at \"" + JSONFile + '"')
		return None

def inheritConfig(configs, child):
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
				applyConfigMutations(parent, child)
			
			return True

def installJSON(config, JSONToInstall):
	ejson_install.installJSON(config, JSONToInstall)
	saveConfig(config, "config.json")
	
def saveConfig(config, name, pretty_print=True):
	f = open(name, "w")
	if pretty_print:
		f.write(json.dumps(config, indent=4, separators=(',', " : "), sort_keys=True))
	else:
		f.write(json.dumps(config, separators=(',', ':'), sort_keys=True))
	f.close()

def buildAndReturnJSON():
	config = readJSON("config.json")
	config["data"] = {}
	extendingConfigs = []
	for f in config["data_files"]:
		currentConfig = readJSON(f)

		if "key" not in currentConfig.keys():
			print("No \"key\" element in " + f + ", skipping.")
			continue
		else:
			config["data"][currentConfig["key"]] = currentConfig
		
		if "data" in currentConfig.keys() and "variables" in currentConfig["data"].keys():
			currentConfig["data"]["variables"] = buildVariables(currentConfig["data"]["variables"])
			insertVariables(currentConfig["data"]["variables"], currentConfig["data"])
		
		if "extends" in currentConfig.keys():
			extendingConfigs.append(currentConfig)

	circularExtendGroup = findCircularInheritance(config["data"])
	if circularExtendGroup is not None:
		print("Circular variable reference detected:")
		for r in circularExtendGroup[0:-1]:
			print(str(r))
		print(circularExtendGroup[-1])
		sys.exit(0)

	while len(extendingConfigs) > 0:
		completedExtends = []
		for e in extendingConfigs:
			if inheritConfig(config["data"], e):
				completedExtends.append(e)
		for e in completedExtends:
			extendingConfigs.remove(e)

	for k in config["data"].keys():
		if "data" in config["data"][k].keys() and "variables" in config["data"][k].keys():
			config["data"][k]["data"]["variables"] = buildVariables(config["data"][k]["data"]["variables"])
			insertVariables(config["data"][k]["data"]["variables"], config["data"][k]["data"])

	saveConfig(config, "built_json.json")

	return config
	
buildAndReturnJSON()