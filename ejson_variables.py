import re

from .ejson_cycles import find_circular_variable_references

def build_variables(values):
	circular_variable_references = find_circular_variable_references(values)
	if circular_variable_references is not None:
		print("Circular variable reference detected:")
		for r in circular_variable_references[0:-1]:
			print(str(r))
		print(circular_variable_references[-1])
		return

	independent_values = [];
	dependent_values = [];

	for i in range(0, len(values)):
		if re.search("<[0-9]*?>", values[i]) is not None:
			dependent_values.append([i, values[i]])
		else:
			independent_values.append([i, values[i]])

	for i in range(0, len(independent_values)):
		for j in range(0, len(dependent_values)):
			pattern = "<" + str(independent_values[i][0]) + ">"
			replacement = independent_values[i][1]
			string = dependent_values[j][1]
			dependent_values[j][1] = re.sub(pattern, replacement, string)

	for i in range(0, len(dependent_values)):
		for j in range(0, len(dependent_values)):
			pattern = "<" + str(dependent_values[i][0]) + ">"
			replacement = dependent_values[i][1]
			string = dependent_values[j][1]
			dependent_values[j][1] = re.sub(pattern, replacement, string)

	values = dependent_values + independent_values
	values = sorted(values, key=lambda x: x[0])

	for i in range(0, len(values)):
		values[i] = values[i][1]
	return values

def insert_variables(variables, parent_json):
	if isinstance(parent_json, list):
		for i in range(0, len(parent_json)):
			if isinstance(parent_json[i], list) or isinstance(parent_json[i], dict):
				insert_variables(variables, parent_json[i])
			elif isinstance(parent_json[i], str):
				for j in range(0, len(variables)):
					pattern = "<" + str(j) + ">"
					parent_json[i] = re.sub(pattern, variables[j], parent_json[i])
	elif isinstance(parent_json, dict):
		for k in parent_json.keys():
			if isinstance(parent_json[k], list) or isinstance(parent_json[k], dict):
				insert_variables(variables, parent_json[k])
			elif isinstance(parent_json[k], str):
				for i in range(0, len(variables)):
					pattern = "<" + str(i) + ">"
					parent_json[k] = re.sub(pattern, variables[i], parent_json[k])