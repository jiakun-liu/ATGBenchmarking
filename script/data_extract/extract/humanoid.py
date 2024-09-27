import json

from data_extract.extract.extract_base import ExtractorBase


class HumanoidExtractor(ExtractorBase):
    def __init__(self, apk_path: str):
        super().__init__("humanoid", apk_path, "utg.js")

    def process_file(self, file_path: dict):
        file_path = set(file_path.values()).pop()
        transition_strings = set()
        json_string = ""
        with open(file_path, "r") as f:
            lines = f.readlines()
            for line in lines[1:]:
                json_string += line
        json_obj = json.loads(json_string)
        node_dict = {}
        for node in json_obj["nodes"]:
            node_id = node["id"]
            package_name, activity_name = node["package"], node["activity"]
            full_activity_name = f"{package_name}{activity_name}"
            node_dict[node_id] = full_activity_name
        for edge in json_obj["edges"]:
            src = node_dict[edge["from"]]
            dst = node_dict[edge["to"]]
            transition_strings.add(f"{src} -> {dst}")
        return transition_strings
