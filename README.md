## What? ##
eJSON stands for Extensible JSON and is a tool for building JSON files. It brings inheritance, variables, and value mutations/overrides to the JSON files you write.

## Why? ##
I am working on a project that is going to take quite a few JSON files for configurations. Instead of writing monolithic, several hundred line JSON files with plenty of room for mistakes and missing lines, I decided that I could and would bring some form of inheritance to those files. As a natural extension of this, I added in a few [potentially] useful ways to override and/or mutate values that children receive from their parents. Finally, I realized that variables would also come in handy, given how many spots I was using values in, so I added those, as well.

## Where? ##
Right now it is written targeting Python 3.5 with a planned port to Java. Other languages may get ports as well, but nothing else is planned right now.

## How? ##
### The Basics ###
You can embed this project into your own if you plan to have users being able to add in their own configurations, or you can use it as a standalone tool to build configurations before you deploy. The script will look in the current working directory for a file named config.json, which looks something like this:
	
	{
		"data_files": [
			"json/base.json",
			"json/extension.json"
		],
		"version": ".1"
	}

The version key isn't required (in fact, it's ignored), but the data\_files key is. It's a list of all the JSON files as you want eJSON to build. Each of these JSON files follows another simple format:

	{
		"name" : "extension",
	    "key" : "extension",
	    "version" : ".1",
		"extends" : "base",
		"data_file" : "extension_data.json",
		"data" : {
		    "variables" : [
			    "variable 1",
				"variable 2"
			],
			"stuff" : "doesn't matter, this is all you."
		}
	}

Here's the rundown:

* key - required; a string that **must** be unique across all JSON files to be built and is used both to reference the final built config and for children JSON to reference that they extend this file
* name - optional; a friendly name for future use by eJSON or things that work with eJSON
* version - optional; serves a similar role as name (it's for your use and maybe future eJSON versions)
* extends - optional; the key of the JSON file that this file is extending
* data\_file - optional; if you don't want to include the data element, you can use data\_file to point to the file that contains your data object
* data - optional; if you don't want to reference a separate file, you can insert your data right here
* variables - optional; an array of string that you can reference in values anywhere within the data object

If you include both data and data\_file, data\_file will be ignored. If you include neither, the data key will be inserted and given an empty object The stuff in data is what gets inherited and gets variables and mutations applied

### Variables ###
Inside of the data object is your array of variables. So far only strings are supported as variables. You can reference variables in any value within the data object. Let's work with this data:

	{
	    "variables" : [
		    "some/file/path",
			"<2>/cool.txt",
			"<0>/to/something"
		],
		"location" : "<1>"
	}

The first thing you'll notice is that we have 3 numbers wrapped in angle brackets in various spots, including in the variable list. The number is the array index (starting at 0) of the value you're referencing. Since you can use variable references anywhere, you can even use variables to build other variables. After processing, that object will look like this:

	{
	    "variables" : [
		    "some/file/path",
			"some/file/path/to/something/cool.txt",
			"some/file/path/to/something"
		],
		"location" : "some/file/path/to/something/cool.txt"
	}

### Mutations ###
Mutations are operations that you can do on the values that a file inherits. Below is the full list of mutations that are currently implemented and I will expand the list as the need arises. Assume the following is in a child file's data object:

	{
		"mutations" : [
			{
				"mutation" : "overwrite",
				"value" : "this worked!"
			},
			{
				"key" : "",
				"mutation" : "overwrite",
				"value" : "this worked!"
			},
			{
				"key" : "some_number",
				"mutation" : "math.add",
				"value" : 6
			},
			{
				"key" : "some_boolean",
				"mutation" : "toggle"
			},
			{
				"key" : "some_string",
				"mutation" : "string.format",
				"values" : [
					"this also worked!"
				]
			}
		]
	}

Mutations are stored in an array with the mutations key. There are 4 keys within a mutation object:

* key - required; the key in the parent whose value this mutation will act on
* mutation - required; a string identifying the mutation operation
* value - optional; a single value which will be used by the mutation
* values - optional; an array of values which will be used by the mutation

The first 2 mutations above will do nothing. The first one has no key and the second one has an empty key. The third one will add 6 to the parent value, the 4th will toggle a boolean value, and the last one performs Python's string format operation.

## Other Keys ##
file\_hash: generated; the SHA2-512 hash of the file this config was built from; used to determine if a rebuild is necessary (not implemented yet)
file\_name: generated; the name of the file this config was built from; used to determine if a rebuild is necessary (not implemented yet)
comment: ignored; a comment on this object

## config.json Exclusive Keys ##
data\_files: required; a list of relative paths to the config files that need to be included in the build process. These are relative to the directory containing config.json
key\_map\_file: PROBABLY GOING BE REMOVED; a relative path to a JSON file containing the allowed keys and their possible values/value types in included configs

## Mutation Operations ##
* overwrite: the long version of simply including a value for the key listed
* toggle: flip the parent value if it is a boolean
* string: a category of string mutations; must use one the values below beginning with string
    * string.format: the python string format operation
	* string.append: append the value to the parent value
	* string.prepend: prepend the value to the parent value
	* string.wrap: prepend and append the value to the parent value
	* string.enclose: prepend and append the parent value to the value
* math: a category of math mutations; must use one the values below beginning with math
	* math.add: add the parent value to this mutation's value
	* math.+: same as math.add
	* math.subtract: subtract this mutation's value from the parent value
		* math.subtract.reverse: subtract the parent value from this mutation's value
	* math.-: same as math.subtract
		* math.-.reverse: same as math.subtract.reverse
	* math.multiply: multiple the parent value to this mutation's value
	* math.*: same as math.multiply
	* math.divide: divide this mutation's value from the parent value
		* math.divide.reverse: divide the parent value from this mutation's value
	* math./: same as math.divide
		* math./.reverse: same as math.divide.reverse
	* math.mod: divide this mutation's value from the parent value and get the remainder
		* math.mod.reverse: divide the parent value from this mutation's value and get the remainder
	* math.%: same as math.mod
		* math.%.reverse: same as math.mod.reverse