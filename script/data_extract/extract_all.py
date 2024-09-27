import argparse
from os.path import isfile

from core.file_paths import *
from data_extract.extract.ape import ApeExtractor
from data_extract.extract.fastbot import FastbotExtractor
from data_extract.extract.humanoid import HumanoidExtractor
from data_extract.extract.monkey import MonkeyExtractor
from data_extract.extract.qtest import QTestExtractor
from data_extract.extract.scenedroid import SceneDroidExtractor
from data_extract.extract.stoat import StoatExtractor


def get_single_result(apk_path: str):
    results = {}
    try:
        print(f"apk_path: {apk_path}")
        # results["ape"] = ApeExtractor(apk_path).extract()
        results["fastbot"] = FastbotExtractor(apk_path).extract()
        # results["humanoid"] = HumanoidExtractor(apk_path).extract()
        # results["monkey"] = MonkeyExtractor(apk_path).extract()
        # results["qtest"] = QTestExtractor(apk_path).extract()
        # results["scenedroid"] = SceneDroidExtractor(apk_path).extract()
        # results["stoat"] = StoatExtractor(apk_path).extract()
        print(f"results: {results}")
    except Exception as e:
        print(e)
    return results, apk_path


def write_result(result_dict: dict, apk_path: str):
    output_dir = get_summary_dir(apk_path)
    valid_tools = set()
    for tool, result in result_dict.items():
        if result is not None and len(result) > 0:
            valid_tools.add(tool)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_file = f"{output_dir}/{tool}.txt"
            with open(output_file, "w") as f:
                for transition in result:
                    f.write(str(transition) + "\n")
    return apk_path, valid_tools


import concurrent.futures


def get_all_results(apk_dir: str, filter_internet: str):
    summary_dict = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as executor:
        futures = []
        for apk_path in get_apks_list(apk_dir, filter_internet):
            if apk_path.endswith(".apk") and isfile(apk_path):
                futures.append(executor.submit(get_single_result, apk_path))
        for future in concurrent.futures.as_completed(futures):
            result_dict, apk_path = future.result()
            apk_path, valid_tools = write_result(result_dict, apk_path)
            summary_dict[apk_path] = valid_tools
    return summary_dict


if __name__ == '__main__':

    # arg parsing
    parser = argparse.ArgumentParser(description='Process to summarize the result of running tools.')

    # Define the arguments
    parser.add_argument('--result_dir', type=str, help='Result directory', required=True)
    parser.add_argument('--apk_dir', type=str, help='Directory of APKs to test', default="all")
    parser.add_argument('--filter_internet', type=str, help='Whether exclude the apps with internet access', default="True")

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    result_dir = args.result_dir
    apk_dir = args.apk_dir
    filter_internet = args.filter_internet

    set_current_version(result_dir)

    summary_dict = get_all_results(apk_dir, filter_internet)
    # summary_dict = update_all_results("smag")
    print(summary_dict)
    print("Finish!!!!!!!!!!!!!!!!!!")

    # result_dir = "second_round_no_internet"
    # set_current_version(result_dir)
    # result, apk = get_single_result("/mnt/hdd1/jkliu/Projects/ATGEmpirical/apks/androzoo/rocks.poopjournal.vacationdays_9.apk")
    # for tool in result.keys():
    #     print(tool)
    #     transitions = result[tool]
    #     for transition in transitions:
    #         print(transition)
