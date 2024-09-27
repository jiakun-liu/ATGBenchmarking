from data_extract.extract.extract_base import ExtractorBase


class FastbotExtractor(ExtractorBase):
    def __init__(self, apk_path: str):
        super().__init__("fastbot", apk_path, "fastbot.log")

    def process_file(self, file_path: dict):
        file_path = set(file_path.values()).pop()
        transition_strings = set()
        with open(file_path, "r") as f:
            lines = f.readlines()
            last_activity = None
            for line in lines:
                line = line.strip()
                if last_activity is not None:
                    # if ("not testing app, need inject restart app" in line):
                    if ("not testing app, need inject restart app" in line) or ("Switch:" in line):
                        last_activity = None
                if "// current activity is " in line:
                    current_activity = line.split("// current activity is ")[1]
                    if last_activity is not None:
                        transition_strings.add(f"{last_activity} -> {current_activity}")
                    last_activity = current_activity
        return transition_strings
