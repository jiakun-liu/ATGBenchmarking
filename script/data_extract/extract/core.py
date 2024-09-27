class Callback(object):
    def __init__(self, callback_type: str, callback: str):
        self.callback_type = callback_type
        self.callback = callback

    def __str__(self):
        return f"${self.callback_type}$ {self.callback}"


class Transition(object):
    def __init__(self, src: str, dst: str, src_type: str = None, dst_type: str = None):
        self.src = src
        self.dst = dst
        self.callbacks = []
        self.src_type = src_type
        self.dst_type = dst_type

    def add_callback(self, callback_type: str, callback_str: str):
        callback_obj = Callback(callback_type, callback_str)
        self.callbacks.append(callback_obj)

    # def __str__(self):
    #     return f"${self.src_type}$ {self.src} -> ${self.dst_type}$ {self.dst} ([{',|| '.join([str(callback) for callback in self.callbacks])}])"

    def __str__(self):
        return f"{self.src} -> {self.dst}"


def get_atg_from_logcat(file_path: str):
    # try:
    result_strings = set()
    last_activity = ""
    current_activity = ""
    with open(file_path, "r") as logcatfile:
        lines = logcatfile.readlines()
        for line in lines:
            if "ActivityManager" in line:
                if "Displayed" in line:
                    current_activity = line.split(" Displayed ")[-1].strip().split(": ")[0].replace("/", "")
                    if last_activity != "":
                        result_strings.add(f"{last_activity} -> {current_activity}")
                    last_activity = current_activity
                if "Force-killing" in line or "Force finishing" in line:
                    last_activity = ""
    results = []
    for result_string in result_strings:
        src, dst = result_string.split(" -> ")
        transition = Transition(src, dst, "activity", "activity")
        results.append(transition)
    return file_path, results
    # except Exception as e:
    #     print(f"Error in {file_path}")
    #     return file_path, []
