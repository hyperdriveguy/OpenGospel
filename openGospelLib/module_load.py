import json
import os
import vars

loaded_modules = []
module_data = dict()

with os.scandir(vars.module_dir) as it:
    for entry in it:
        if entry.is_dir():
            json_prefix = vars.module_dir + '/' + entry.name + '/' + entry.name
            try:
                with open(json_prefix + '.json', 'r') as f:
                    module_data[entry.name] = json.load(f)
                loaded_modules.append(entry.name)
            except OSError:
                pass
