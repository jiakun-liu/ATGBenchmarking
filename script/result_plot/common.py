from core.apk_util import *


def get_real_transitions():
    real_transitions_file_path = "summary/data_analysis/first_round_no_internet/gt_transitions_bigger1.txt"
    real_transitions = {}
    apk_name = ""
    package_name = ""
    temp_transitions = []
    with open(real_transitions_file_path) as f:
        lines = f.readlines()
        for line in lines:
            if "APK: " in line:
                if apk_name != "":
                    real_transitions[apk_name] = temp_transitions
                temp_transitions = []
                apk_name = line.split("APK: ")[-1].strip()
                version_code = apk_name.split("_")[-1].split(".apk")[0]
                package_name = apk_name.split("/")[-1].replace(f"_{version_code}.apk", "")
                if "/Users/jiakun/Projects/TestingModelAnalysis" in apk_name:
                    apk_name = apk_name.replace("/Users/jiakun/Projects/TestingModelAnalysis", "/mnt/hdd1/jkliu/Projects/ATGEmpirical")
                continue
            if apk_name != "" and "->" in line:
                src, tgt = line.strip().split(" -> ")
                if "Start" in src:
                    continue
                src, tgt = transform_activtiy_name(src, package_name), transform_activtiy_name(tgt, package_name)
                transition = f"{src} -> {tgt}"
                temp_transitions.append(transition)
    return real_transitions


from core.file_paths import *


def get_tool_result(apk_path: str, declared_activities: list):
    print(f"extracting summaries for {apk_path}")
    version_code = apk_path.split("_")[-1].split(".apk")[0]
    package_name = apk_path.split("/")[-1].replace(f"_{version_code}.apk", "")
    tool_transitions = {}
    summary_dir = get_summary_dir(apk_path)
    if not os.path.exists(summary_dir):
        print(f"{summary_dir} does not exist")
        return
    for tool in tools:
        transitions = []
        tool_file = f"{tool}.txt"
        tool_dir = os.path.join(summary_dir, tool_file)
        if not os.path.exists(tool_dir):
            continue
        with open(tool_dir, "r") as f:
            for line in f.readlines():
                src, tgt = line.strip().split(" -> ")
                src, tgt = transform_activtiy_name(src, package_name), transform_activtiy_name(tgt, package_name)
                if (src in declared_activities) and (tgt in declared_activities):
                    transition = f"{src} -> {tgt}"
                    transitions.append(transition)
        tool_transitions[tool] = transitions
    return apk_path, tool_transitions
