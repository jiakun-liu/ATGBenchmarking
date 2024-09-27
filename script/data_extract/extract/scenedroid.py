from data_extract.extract.extract_base import ExtractorBase


class SceneDroidExtractor(ExtractorBase):

    def __init__(self, apk_path: str):
        super().__init__("scenedroid", apk_path, "scenedroid.log")

    def process_file(self, file_path: dict):
        file_path = set(file_path.values()).pop()
        result_strings = set()
        with open(file_path, "r") as f:
            lines = f.readlines()
            src, tgt = "", ""
            raw_record = False
            for line in lines:
                if "[NEW Trans] :" in line:
                    raw_transition = line.strip().replace("[NEW Trans] :", "").strip()
                    src, tgt = raw_transition.split("->")
                    result_strings.add(f"{src} -> {tgt}")
                if "A Different Act Name: " in line:
                    src, tgt = "", ""
                    raw_record = True
                if raw_record and "[screen.act] :" in line:
                    src = line.strip().replace("[screen.act] :", "").strip()
                if raw_record and "[NEW ACT] :" in line:
                    tgt = line.strip().replace("[NEW ACT] :", "").strip()
                    result_strings.add(f"{src} -> {tgt}")
                    raw_record = False
                    src, tgt = "", ""
        return result_strings
