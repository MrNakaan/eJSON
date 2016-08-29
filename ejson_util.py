import hashlib, sys, os.path

def ePrint(errors, separator=None, line_end=None, should_flush=False):
	print(errors, sep=separator, end=line_end, file=sys.stderr, flush=should_flush)

def hashFile(JSONFile):
	h = hashlib.sha512()
	if os.path.isfile(JSONFile):
		f = open(JSONFile, "r")
		h.update(f.read().encode("UTF-8"))
		f.close()
		return h.hexdigest()
	else:
		ePrint("Cannot hash file, no file at \"" + JSONFile + '"')
		return None
