import json

from lib.agent import AgentEncoder

ERROR = "Error:"


def err_return(s):
    return {ERROR: s}


def json_converter(obj):
    print("Converting model to json")
    obj_json = obj.to_json()
    json_str = json.dumps(obj_json, cls=AgentEncoder, indent=4)
    json_obj = json.loads(json_str)
    return json_obj
