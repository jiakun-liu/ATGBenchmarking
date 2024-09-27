from data_extract.extract.extract_base import ExtractorBase


class QTestExtractor(ExtractorBase):

    def __init__(self, apk_path: str):
        super().__init__("qtest", apk_path, "q-testing.log")

    def process_file(self, file_path: dict):
        file_path = set(file_path.values()).pop()
        transition_strings = set()
        with open(file_path, "r") as f:
            lines = f.readlines()
            last_activity = None
            for line in lines:
                if "the chosen action is restarting app" in line:
                    last_activity = None
                if "the jumped state is " in line:
                    current_activity = line.split("the jumped state is ")[-1].strip()
                    if last_activity is not None:
                        transition_strings.add(f"{last_activity} -> {current_activity}")
                    last_activity = current_activity
        return transition_strings
