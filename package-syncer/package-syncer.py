#!/usr/bin/env python3
import json


def update_version(filenames, package_name, package_version):
    for file in filenames:
        with open(file) as a_json_file:
            a_data = json.loads(a_json_file.read())
            if "dependencies" in a_data.keys():
                if package_name in a_data["dependencies"].keys():
                    a_data["dependencies"][package_name] = package_version
        with open(file, 'w+') as jsonfile:
            json.dump(a_data, jsonfile, indent=2)
            jsonfile.write("\n")


with open("settings.json") as json_file:
    data = json.loads(json_file.read())
    filename = data["source"]
    folders_to_change = data["update repos"]
    files_to_change = [sub + "package.json" for sub in folders_to_change]

with open(filename) as json_file:
    data = json.loads(json_file.read())
    version = data["version"]
    name = data["name"]
    print("updating to use %s version: %s" % (name,version))
update_version(filenames=files_to_change, package_name=name, package_version=version)

print("Versions updated, please update the following folders with NPM")
for folder in folders_to_change:
    print(folder)
