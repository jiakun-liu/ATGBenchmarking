from data_extract.extract.extract_base import ExtractorBase


class StoatExtractor(ExtractorBase):

    def __init__(self, apk_path: str):
        super().__init__("stoat", apk_path, "allstates.txt", "app.gv")

    def parse_allstates(self, allstates_path: str):
        state_activity_dict = {}
        current_state = None
        with open(allstates_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line == "":
                    continue
                if "-----------" in line:
                    current_state = None
                    continue
                if current_state is None and line.startswith("the state file name:"):
                    current_state = line.split("/")[-1].replace(".xml", "")
                    continue
                if current_state is not None:
                    activity = line
                    state_activity_dict[current_state] = activity
                    current_state = None
        return state_activity_dict

    def parse_app_gv(self, app_gv_path: str, state_activity_dict: dict):
        transition_strings = set()
        with open(app_gv_path, "r") as f:
            lines = f.readlines()
            if len(lines) == 0:
                for activity in state_activity_dict.values():
                    transition_strings.add(f"Start -> {activity}")
            for line in lines:
                line = line.strip()
                if "[" in line:
                    content = line.split("[")[0].strip()
                    splits = content.split("->")
                    src = splits[0].strip()
                    dst = splits[1].strip()
                    if src in state_activity_dict.keys() and dst in state_activity_dict.keys():
                        src = state_activity_dict[src]
                        dst = state_activity_dict[dst]
                        transition_strings.add(f"{src} -> {dst}")
        return transition_strings

    def process_file(self, file_path: dict):
        allstates_path = file_path.get("allstates.txt")
        app_gv_path = file_path.get("app.gv")
        state_activity_dict = self.parse_allstates(allstates_path)
        transition_strings = self.parse_app_gv(app_gv_path, state_activity_dict)
        return transition_strings
