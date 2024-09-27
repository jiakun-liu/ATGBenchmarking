from core.file_paths import *
from data_extract.extract.core import Transition


class ExtractorBase:
    def __init__(self, tool_name: str, apk_path: str, *result_file_names: str):
        self.tool_name = tool_name
        self.result_file_names = result_file_names
        self.apk_path = apk_path

    def get_result_file_path(self):
        result_file_paths = {}
        for file_name in self.result_file_names:
            _, file_path, _ = get_path_of_result_file(self.tool_name, self.apk_path, file_name)
            result_file_paths[file_name] = file_path
        return result_file_paths

    def process_file(self, file_path: dict):
        raise NotImplementedError('extract method is not implemented')

    def extract(self):
        results = []
        file_paths = self.get_result_file_path()
        for file_path in file_paths.values():
            if not os.path.exists(file_path):
                print(f"{file_path} does not exist")
                return None
        transition_strings = self.process_file(file_paths)
        for transition_string in transition_strings:
            src, dst = transition_string.split(" -> ")
            if src == dst:
                continue
            transition = str(Transition(src, dst, "activity", "activity"))
            results.append(transition)
        return results
