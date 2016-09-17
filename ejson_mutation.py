from .ejson_util import e_print

def apply_string_mutation(mutation, child, parent_value, child_value):
	mutation_string = mutation["mutation"].split('.')
	if len(mutation_string) <= 1:
		print("No string mutation present.")
	elif mutation_string[1] == "format":
		if "values" in mutation.keys():
			if len(mutation["values"]) is 1:
				mutation["values"] = str(mutation["values"][0])
			elif len(mutation["values"]) is 0:
				mutation["values"] = ""
			else:
				mutation["values"] = tuple(mutation["values"])
			child[mutation["key"]] = parent_value.format(mutation["values"])
		elif "value" in mutation.keys():
			child[mutation["key"]] = parent_value.format(mutation["value"])
	elif mutation_string[1] == "append":
		child[mutation["key"]] = parent_value + mutation["value"]
	elif mutation_string[1] == "prepend":
		child[mutation["key"]] = mutation["value"] + parent_value
	elif mutation_string[1] == "wrap":
		child[mutation["key"]] = mutation["value"] + parent_value + mutation["value"]
	elif mutation_string[1] == "enclose":
		child[mutation["key"]] = parent_value + mutation["value"] + parent_value

def apply_math_mutation(mutation, child, parent_value, child_value):
	mutation_string = mutation["mutation"].split('.')
	if len(mutation_string) <= 1:
		print("No math mutation present.")
	if mutation_string[1] == "add" or mutation_string[1] == "+":
		child[mutation["key"]] = parent_value + mutation["value"]
	elif mutation_string[1] == "subtract" or mutation_string[1] == "-":
		if len(mutation_string) > 2 and mutation_string[2] == "reverse":
			child[mutation["key"]] = mutation["value"] - parent_value
		else:
			child[mutation["key"]] = parent_value - mutation["value"]
	elif mutation_string[1] == "multiply" or mutation_string[1] == "*":
		child[mutation["key"]] = parent_value * mutation["value"]
	elif mutation_string[1] == "divide" or mutation_string[1] == "/":
		if len(mutation_string) > 2 and mutation_string[2] == "reverse":
			child[mutation["key"]] = mutation["value"] / parent_value
		else:
			child[mutation["key"]] = parent_value / mutation["value"]
	elif mutation_string[1] == "mod" or mutation_string[1] == "%":
		if len(mutation_string) > 2 and mutation_string[2] == "reverse":
			child[mutation["key"]] = mutation["value"] % parent_value
		else:
			child[mutation["key"]] = parent_value % mutation["value"]

def apply_mutations(parent, child):
	for m in child["mutations"]:
		if "key" not in m:
			e_print("No key in mutation: " + str(m))
			continue
		elif m["key"] not in parent.keys():
			e_print("Key " + m["key"] + " is not in parent")
			continue
			
		parent_value = parent[m["key"]]
		child_value = child[m["key"]]
		mutation = m["mutation"]
		
		if mutation == "overwrite":
			child[m["key"]] = child_value
		elif mutation == "toggle":
			if not isinstance(parent_value, bool):
				print("Mutation is toggle but " + m["key"] + " is not a boolean.")
			else:
				child[m["key"]] = not parent_value
		elif mutation.startswith("string."):
			apply_string_mutation(m, child, parent_value, child_value)
		elif mutation.startswith("math."):
			apply_math_mutation(m, child, parent_value, child_value)
	del child["mutations"]