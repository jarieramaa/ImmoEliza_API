
from distutils.command.build_scripts import first_line_re
import json

def generate_info(f_meta: json) -> str:
    """
    Generate information about the features based on feature_meta_data.json.
    When generating this info from the actual meta data, it's always up to date.
    :f_meta: dictionary with feature meta data
    :return: string with information about the features"""
    keys= f_meta.keys()
    result = "{"
    first_line = True
    for name in keys:
        mandatory = f_meta[name]["mandatory"]
        if first_line:
            result += f"\"{name}\" : "
            first_line = False
        else:
            result += f",\n\"{name}\" : "
        if not mandatory:
            result += "Optional"
        if f_meta.get(name).get("options") is not None:
            options = f_meta[name]["options"]
            if len(options) < 50:
                counter = 0
                result += "["
                for i, option in enumerate(options):
                    result += f"\"{option}\""
                    print(i, len(options))
                    if i < len(options) - 1:
                        result += " | "
                    counter += 1
                    if counter >= 6:
                        result += "\n\t\t\t"
                        counter = 0
                result += "]"
            else:
                result += "int" #zip-code
        else:
            if mandatory :
                result += f_meta[name]["type"]
            else:
                result += "("+f_meta[name]["type"]+")"
    result += " \n}"
    print(result)
    return result
