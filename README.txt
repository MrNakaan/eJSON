-=Global Keys=-
key: required; a string identifying this config which must be unique across all included configs; not necessary in config.json
extends: optional; a string that is the key for another included config
data_file: optional; a relative path to a JSON file containing the definition for the config element; if present, this key will overwrite any included config key
data: optional; the actual configuration contained within this JSON file
variables: optional; a list of variables that may be included/used in other keys; these are referenced by their index (starting at 0) surrounded by angle brackets (eg <0>) and may even be used in other variables
mutations: optional; a list of opjects (mutations) to apply to a parent config
name: optional; a friendly name for this config
version: optional; the config version
file_hash: generated; the SHA2-512 hash of the file this config was built from; used to determine if a rebuild is necessary
file_name: generated; the name of the file this config was built from; used to determine if a rebuild is necessary
comment: ignored; a comment on this object

-=config.json=-
data_files: a list of relative paths to the config files that need to be included in the build process. These are relative to the directory containing config.json
key_map_file: MAY BE REMOVED; a relative path to a JSON file containing the allowed keys and their possible values/value types in included configs

-=Mutations=-
key: required; a key contained within the parent config
mutation: required; the mutation to apply
value: optional; a single value used by this mutation
values: optional; a list of values used by this mutation

Allowed mutation operations:
	overwrite: the long version of simply including a value for the key listed
	toggle: flip the parent value if it is a boolean
	string.: a category of string mutations; must use one the values below beginning with string.
		string.format: the python string format operation
	math.: a category of math mutations; must use one the values below beginning with math.
		math.add: add the parent value to this mutation's value
		math.+: same as math.add
		math.subtract: subtract this mutation's value from the parent value
		math.subtract.reverse: subtract the parent value from this mutation's value
		math.-: same as math.subtract
		math.-.reverse: same as math.subtract.reverse
		math.multiply: multiple the parent value to this mutation's value
		math.*: same as math.multiply
		math.divide: divide this mutation's value from the parent value
		math.divide.reverse: divide the parent value from this mutation's value
		math./: same as math.divide
		math./.reverse: same as math.divide.reverse
		math.mod: divide this mutation's value from the parent value and get the remainder
		math.mod.reverse: divide the parent value from this mutation's value and get the remainder
		math.%: same as math.mod
		math.%.reverse: same as math.mod.reverse