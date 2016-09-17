import hashlib, sys, os.path

def e_print(errors, separator=None, line_end=None, should_flush=False):
	print(errors, sep=separator, end=line_end, file=sys.stderr, flush=should_flush)

def hash_file(json_file):
	h = hashlib.sha512()
	if os.path.isfile(json_file):
		f = open(json_file, "r")
		h.update(f.read().encode("UTF-8"))
		f.close()
		return h.hexdigest()
	else:
		e_print("Cannot hash file, no file at \"" + json_file + '"')
		return None
