import os

from data_extract.extract import core


def parse_manual_log(dir_path: str):
    if not os.path.exists(dir_path):
        print(f"{dir_path} does not exist")
        return None
    if os.path.isfile(dir_path):
        print(f"{dir_path} is not a directory")
        return None
    results = set()
    for logfile in os.listdir(dir_path):
        file_path = os.path.join(dir_path, logfile)
        file_path, temp_result = core.get_atg_from_logcat(file_path)
        results.update(temp_result)
    return list(results)
