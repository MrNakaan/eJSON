from ejson_util import ePrint

def applyStringMutation(mutation, child, parentValue, childValue):
	mutationString = mutation["mutation"].split('.')
	if len(mutationString) <= 1:
		print("No string mutation present.")
	elif mutationString[1] == "format":
		if "values" in mutation.keys():
			if len(mutation["values"]) is 1:
				mutation["values"] = str(mutation["values"][0])
			elif len(mutation["values"]) is 0:
				mutation["values"] = ""
			else:
				mutation["values"] = tuple(mutation["values"])
			child[mutation["key"]] = parentValue.format(mutation["values"])
		elif "value" in mutation.keys():
			child[mutation["key"]] = parentValue.format(mutation["value"])
	elif mutationString[1] == "append":
		child[mutation["key"]] = parentValue + mutation["value"]
	elif mutationString[1] == "prepend":
		child[mutation["key"]] = mutation["value"] + parentValue
	elif mutationString[1] == "wrap":
		child[mutation["key"]] = mutation["value"] + parentValue + mutation["value"]
	elif mutationString[1] == "enclose":
		child[mutation["key"]] = parentValue + mutation["value"] + parentValue

def applyMathMutation(mutation, child, parentValue, childValue):
	mutationString = mutation["mutation"].split('.')
	if len(mutationString) <= 1:
		print("No math mutation present.")
	if mutationString[1] == "add" or mutationString[1] == "+":
		child[mutation["key"]] = parentValue + mutation["value"]
	elif mutationString[1] == "subtract" or mutationString[1] == "-":
		if len(mutationString) > 2 and mutationString[2] == "reverse":
			child[mutation["key"]] = mutation["value"] - parentValue
		else:
			child[mutation["key"]] = parentValue - mutation["value"]
	elif mutationString[1] == "multiply" or mutationString[1] == "*":
		child[mutation["key"]] = parentValue * mutation["value"]
	elif mutationString[1] == "divide" or mutationString[1] == "/":
		if len(mutationString) > 2 and mutationString[2] == "reverse":
			child[mutation["key"]] = mutation["value"] / parentValue
		else:
			child[mutation["key"]] = parentValue / mutation["value"]
	elif mutationString[1] == "mod" or mutationString[1] == "%":
		if len(mutationString) > 2 and mutationString[2] == "reverse":
			child[mutation["key"]] = mutation["value"] % parentValue
		else:
			child[mutation["key"]] = parentValue % mutation["value"]

def applyConfigMutations(parent, child):
	for m in child["mutations"]:
		if "key" not in m:
			ePrint("No key in mutation: " + str(m))
			continue
		elif m["key"] not in parent.keys():
			ePrint("Key " + m["key"] + " is not in parent")
			continue
			
		parentValue = parent[m["key"]]
		childValue = child[m["key"]]
		mutation = m["mutation"]
		
		if mutation == "overwrite":
			child[m["key"]] = childValue
		elif mutation == "toggle":
			if not isinstance(parentValue, bool):
				print("Mutation is toggle but " + m["key"] + " is not a boolean.")
			else:
				child[m["key"]] = not parentValue
		elif mutation.startswith("string."):
			applyStringMutation(m, child, parentValue, childValue)
		elif mutation.startswith("math."):
			applyMathMutation(m, child, parentValue, childValue)
	del child["mutations"]