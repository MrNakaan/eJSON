import re

from ejson_cycles import findCircularVariableReferences

def buildVariables(values):
	circularVariableReferences = findCircularVariableReferences(values)
	if circularVariableReferences is not None:
		print("Circular variable reference detected:")
		for r in circularVariableReferences[0:-1]:
			print(str(r))
		print(circularVariableReferences[-1])
		return

	#independentValues
	iv = [];
	#dependentValues
	dv = [];

	for i in range(0, len(values)):
		if re.search("<[0-9]*?>", values[i]) is not None:
			dv.append([i, values[i]])
		else:
			iv.append([i, values[i]])

	for i in range(0, len(iv)):
		for j in range(0, len(dv)):
			dv[j][1] = re.sub("<" + str(iv[i][0]) + ">", iv[i][1], dv[j][1])

	for i in range(0, len(dv)):
		for j in range(0, len(dv)):
			dv[j][1] = re.sub("<" + str(dv[i][0]) + ">", dv[i][1], dv[j][1])

	values = dv + iv
	values = sorted(values, key=lambda x: x[0])

	for i in range(0, len(values)):
		values[i] = values[i][1]
	return values

def insertVariables(variables, parentConfig):
	if isinstance(parentConfig, list):
		for i in range(0, len(parentConfig)):
			if isinstance(parentConfig[i], list) or isinstance(parentConfig[i], dict):
				insertVariables(variables, parentConfig[i])
			elif isinstance(parentConfig[i], str):
				for j in range(0, len(variables)):
					parentConfig[i] = re.sub("<" + str(j) + ">", variables[j], parentConfig[i])
	elif isinstance(parentConfig, dict):
		for k in parentConfig.keys():
			if isinstance(parentConfig[k], list) or isinstance(parentConfig[k], dict):
				insertVariables(variables, parentConfig[k])
			elif isinstance(parentConfig[k], str):
				for i in range(0, len(variables)):
					parentConfig[k] = re.sub("<" + str(i) + ">", variables[i], parentConfig[k])