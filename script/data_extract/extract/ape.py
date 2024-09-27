from data_extract.extract.extract_base import ExtractorBase


class ApeExtractor(ExtractorBase):

    def __init__(self, apk_path: str):
        super().__init__("ape", apk_path, "ape.log")

    def process_file(self, file_path: dict):
        file_path = set(file_path.values()).pop()
        transition_strings = set()
        with open(file_path, "r") as f:
            lines = f.readlines()
            begin = False
            src, tgt = None, None
            line_counter = 0
            for line in lines:
                line_counter += 1
                if line.strip().startswith("[APE] === Adding edge..."):
                    line_counter = 0
                    begin = True
                    continue
                if begin == True and line.strip().startswith("[APE]     Source: "):
                    if line_counter < 10 and src is None and tgt is None:
                        src = line.split("]")[3].strip().split("@")[0]
                    else:
                        print(f"Error in source {src} {tgt}")
                    continue
                if begin == True and line.strip().startswith("[APE]     Target: "):
                    if line_counter < 10 and src is not None and tgt is None:
                        tgt = line.split("]")[3].strip().split("@")[0]
                        transition_strings.add(f"{src} -> {tgt}")
                        line_counter = 0
                        begin = False
                        src, tgt = None, None
                    else:
                        print(f"Error in target {src} {tgt} {line_counter}")
                    continue
        return transition_strings
