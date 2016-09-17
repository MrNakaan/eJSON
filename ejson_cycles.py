import re

def find_circular_variable_references(values):
	for v in values:
		reference_group = [v]
		to_check = [v]
		while len(to_check) > 0:
			references = re.findall("<([0-9]*?)>", to_check[0])
			if len(references) is not 0:
				for r in references:
					if values[int(r)] in reference_group:
						reference_group.append(values[int(r)])
						return reference_group
					to_check.append(values[int(r)])
					reference_group.append(values[int(r)])
			to_check.remove(to_check[0])

def find_circular_inheritance(configs):
	for c in configs.keys():
		inheritance_group = [c]
		to_check = [c]
		while len(to_check) > 0:
			if "extends" not in configs[to_check[0]].keys():
				break
			extends = configs[to_check[0]]["extends"]
			if extends in inheritance_group:
				inheritance_group.append(extends)
				return inheritance_group
			to_check.append(extends)
			inheritance_group.append(extends)
			to_check.remove(to_check[0])