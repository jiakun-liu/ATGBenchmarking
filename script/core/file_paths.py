import os
from concurrent.futures import ThreadPoolExecutor

root_dir = os.getcwd()

current_version = None


def set_current_version(version):
    global current_version
    current_version = version


def get_current_version():
    global current_version
    if current_version is None:
        exit("Current version is not set")
    return current_version


def get_result_version():
    return f"results/{get_current_version()}"


tools = ["ape", "fastbot", "humanoid", "monkey", "qtest", "scenedroid", "stoat"]


def get_apks_list(dir: str):
    files = []
    for apk_file in os.listdir(dir):
        if not apk_file.endswith(".apk"):
            continue
        apk = f"{dir}/{apk_file}"
        files.append(apk)
    files = list(set(files))
    return files


def get_result_dir(tool_name: str, apk_path: str):
    apk_name = apk_path.split("/")[-1]
    result_dir = f"{root_dir}/{get_result_version()}/{tool_name}/{apk_name}"
    print(f"result_dir: {result_dir}")
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    return result_dir


def get_summary_dir(apk_path: str):
    app_name = apk_path.split("/")[-1].split(".apk")[0]
    output_dir = f"{root_dir}/summary/{get_result_version()}/{app_name}"
    return output_dir


def get_log_file(tool_name: str, apk_path: str):
    apk_name = apk_path.split("/")[-1]
    log_dir = f"{root_dir}/{get_result_version()}/{tool_name}/execution_log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = f"{root_dir}/{get_result_version()}/{tool_name}/execution_log/{apk_name}.log"
    return log_file


def get_path_of_result_file(tool_name: str, apk_path: str, result_file_name: str):
    result_dir = get_result_dir(tool_name, apk_path)
    if not os.path.exists(result_dir):
        print(f"The {result_dir} for {apk_path} of {tool_name} does not exist")
        return "", "", ""
    result_file = ""
    logcat_file = ""
    for root, dirs, files in os.walk(result_dir):
        for file in files:
            if result_file_name == file:
                result_file = f"{root}/{file}"
            if "logcat" in file:
                logcat_file = f"{root}/{file}"
    return result_dir, result_file, logcat_file


def get_stoat_result_files(apk_path: str):
    resuld_dir = apk_path.replace(".apk", "-output")
    resuld_dir = f"{resuld_dir}/stoat_fsm_output"
    result_file = f"{resuld_dir}/explored_activity_list.txt"
    if not os.path.exists(result_file):
        print(f"{result_file} does not exist")
        result_file = ""
    if not os.path.exists(resuld_dir):
        print(f"{resuld_dir} does not exist")
        resuld_dir = ""
    return resuld_dir, result_file, ""
