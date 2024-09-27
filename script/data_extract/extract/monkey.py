from data_extract.extract.extract_base import ExtractorBase


class MonkeyExtractor(ExtractorBase):
    def __init__(self, apk_path: str):
        super().__init__("monkey", apk_path, "monkey.log")

    def process_file(self, file_path: dict):
        file_path = set(file_path.values()).pop()
        transition_strings = set()
        with open(file_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if ":Switch:" in line:
                    last_activity = None
                if "// Allowing start of Intent {" in line:
                    splits = line.split(" ")
                    for s in splits:
                        if "cmp=" in s:
                            current_activity = s.replace("cmp=", "").replace("/", "").replace("}", "").strip()
                            if last_activity is not None:
                                transition_strings.add(f"{last_activity} -> {current_activity}")
                            last_activity = current_activity
        return transition_strings
