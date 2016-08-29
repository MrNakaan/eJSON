import re

def findCircularVariableReferences(values):
	for v in values:
		referenceGroup = [v]
		toCheck = [v]
		while len(toCheck) > 0:
			references = re.findall("<([0-9]*?)>", toCheck[0])
			if len(references) is not 0:
				for r in references:
					if values[int(r)] in referenceGroup:
						referenceGroup.append(values[int(r)])
						return referenceGroup
					toCheck.append(values[int(r)])
					referenceGroup.append(values[int(r)])
			toCheck.remove(toCheck[0])

def findCircularInheritance(configs):
	for c in configs.keys():
		inheritanceGroup = [c]
		toCheck = [c]
		while len(toCheck) > 0:
			if "extends" not in configs[toCheck[0]].keys():
				break
			extends = configs[toCheck[0]]["extends"]
			if extends in inheritanceGroup:
				inheritanceGroup.append(extends)
				return inheritanceGroup
			toCheck.append(extends)
			inheritanceGroup.append(extends)
			toCheck.remove(toCheck[0])