import argparse
import concurrent
from datetime import datetime

import pandas as pd

from core.apk_util import *
from core.file_paths import *


def extract_using_display(line, package_name):
    if "Displayed" not in line:
        return None, None
    current_activity = line.split("Displayed ")[-1].strip().split(": ")[0].replace("/", "")
    splits = line.split("Displayed ")[0].split(" ")
    time = f"2024-{splits[0]} {splits[1]}"
    time_stamp = datetime.fromisoformat(time)
    current_activity = transform_activtiy_name(current_activity, package_name)
    return current_activity, time_stamp


def extract_using_start(line, package_name):
    if " START " not in line:
        return None, None
    current_activity = None
    splits = line.split(" ")
    time = f"2024-{splits[0]} {splits[1]}"
    time_stamp = datetime.fromisoformat(time)
    for s in splits:
        if "cmp" in s:
            s = s.replace("cmp=", "").replace("{", "").replace("}", "")
            current_activity = s.replace("/", "")
            break
    current_activity = transform_activtiy_name(current_activity, package_name)
    return current_activity, time_stamp


def extract_transitions_from_logcat(logcat_file: str, transitions: list, declared_activities: list, package_name: str):
    activity_time = {}
    transition_time = {}
    if not os.path.exists(logcat_file):
        print(f"Logcat file {logcat_file} does not exist")
        return activity_time, transition_time
    last_activity = 'Start'
    first_time = None
    with open(logcat_file, "r") as logcatfile:
        lines = logcatfile.readlines()
        for line in lines:
            try:
                if "ActivityManager: " in line:
                    # current_activity, time_stamp = extract_using_display(line, package_name)
                    current_activity, time_stamp = extract_using_start(line, package_name)
                    if current_activity is None and time_stamp is None:
                        continue
                    if first_time is None:
                        first_time = time_stamp
                    time_interval = (time_stamp - first_time).total_seconds() / 60
                    is_valid_activity = False
                    for declared_activity in declared_activities:
                        if (declared_activity in current_activity) or (current_activity in declared_activity):
                            is_valid_activity = True
                            break
                    if not is_valid_activity:
                        continue
                    if current_activity not in activity_time:
                        activity_time[current_activity] = time_interval
                    if last_activity != 'Start':
                        for transition in transitions:
                            if transition in transition_time:
                                continue
                            src, tgt = transition.split(" -> ")
                            src, tgt = src.strip(), tgt.strip()
                            if ((src in last_activity) or (last_activity in src)) and (
                                    (tgt in current_activity) or (current_activity in tgt)):
                                transition_time[transition] = time_interval
                                print(f"Time to get {transition} is {time_interval}")
                    else:
                        transition_time['Start -> ' + current_activity] = time_interval
                    last_activity = current_activity
            except Exception as e:
                print(f"Error in line: {line}")
                print(f"Error: {e}")
                continue
    return activity_time, transition_time


def get_filtered_results(apk_path: str, declared_activities: list, package_name: str):
    raw_transitions = {}
    transition_results = {}
    activity_results = {}
    transition_times = {}
    activity_times = {}
    print(f"extracting summaries for {apk_path}")
    summary_dir = get_summary_dir(apk_path)
    if not os.path.exists(summary_dir):
        print(f"{summary_dir} does not exist")
        return transition_results
    for tool in tools:
        tool_transitions = []
        tool_file = f"{tool}.txt"
        print(f"tool_file: {tool_file}")
        tool_dir = os.path.join(summary_dir, tool_file)
        if not os.path.exists(tool_dir):
            continue
        _, _, logcat_file = get_path_of_result_file(tool, apk_path, "")
        with open(tool_dir, "r") as f:
            for line in f.readlines():
                print(f"line: {line}")
                src, tgt = line.strip().split(" -> ")
                src, tgt = src.strip(), tgt.strip()
                src, tgt = transform_activtiy_name(src, package_name), transform_activtiy_name(tgt, package_name)
                is_declared_src = False
                is_declared_tgt = False
                for activity in declared_activities:
                    if activity in src or src in activity:
                        is_declared_src = True
                    if activity in tgt or tgt in activity:
                        is_declared_tgt = True
                if is_declared_src and is_declared_tgt:
                    tool_transitions.append(line.strip())
        raw_transitions[tool] = tool_transitions
        if tool == 'stoat':
            transition_results[tool] = tool_transitions
            transition_times[tool] = None
            activity_times[tool] = None
            temp_activity_results = set()
            for transition in tool_transitions:
                src, tgt = transition.split("->")
                src, tgt = src.strip(), tgt.strip()
                src, tgt = transform_activtiy_name(src, package_name), transform_activtiy_name(tgt, package_name)
                if src != "Start":
                    temp_activity_results.add(src)
                if tgt != "Start":
                    temp_activity_results.add(tgt)
            activity_results[tool] = list(temp_activity_results)
            continue
        activity_time, transition_time = extract_transitions_from_logcat(logcat_file, tool_transitions, declared_activities, package_name)
        transition_results[tool] = list(transition_time.keys())
        transition_times[tool] = list(transition_time.values())
        activity_results[tool] = list(activity_time.keys())
        activity_times[tool] = list(activity_time.values())
    all_transitions = set()
    for tool in transition_results.keys():
        all_transitions.update(set(transition_results.get(tool)))
    transition_results["all"] = list(all_transitions)
    all_activities = set()
    for tool in activity_results.keys():
        all_activities.update(set(activity_results.get(tool)))
    activity_results["all"] = list(all_activities)
    print(f"extracted summaries for {apk_path}")
    print(raw_transitions)
    return raw_transitions, transition_results, transition_times, activity_results, activity_times


def get_diff_results(transition_results: dict):
    diff_dict = {}
    for tool in transition_results.keys():
        if tool == "all":
            diff_dict["all"] = list(set(transition_results["all"]))
            continue
        diff_dict[tool] = list(set(transition_results["all"]) - set(transition_results[tool]))
    return diff_dict


def get_transition_chains(transitions: list, exported_activities: list):
    transition_chains = []
    for activity in exported_activities:
        for transition in transitions:
            transition = transition.strip()
            src, tgt = transition.split(" -> ")
            src, tgt = src.strip(), tgt.strip()
            if src == activity:
                transition_chain = [transition]
                transition_chains.append(transition_chain)
    while True:
        transition_chain_sizes = len(transition_chains)
        for transition in transitions:
            transition = transition.strip()
            src, tgt = transition.split(" -> ")
            src, tgt = src.strip(), tgt.strip()
            for transition_chain in transition_chains:
                last_transition = transition_chain[-1].strip()
                _, last_tgt = last_transition.split(" -> ")
                last_tgt = last_tgt.strip()
                if last_tgt == src:
                    if transition not in transition_chain:
                        transition_chain.append(transition)
                        transition_chains.append(transition_chain)
        if len(transition_chains) == transition_chain_sizes:
            break
    deduplicated_transition_chains = set()
    transition_str_list_mapping = {}
    for transition_chain1 in transition_chains:
        for transition_chain2 in transition_chains:
            transition_chain1_str = str(transition_chain1)
            transition_chain2_str = str(transition_chain2)
            if transition_chain1_str in transition_chain2_str:
                transition_str_list_mapping[transition_chain2_str] = transition_chain2
                deduplicated_transition_chains.add(transition_chain2_str)
    deduplicated_transition_chains_list = []
    for transition_chain_str in deduplicated_transition_chains:
        deduplicated_transition_chains_list.append(transition_str_list_mapping[transition_chain_str])
    return deduplicated_transition_chains_list


def get_transition_size(transition_results: dict):
    transition_size = {}
    transition_size["all"] = 0
    for tool in transition_results.keys():
        number_of_valid_transitions = len(transition_results[tool])
        if number_of_valid_transitions != 0:
            transition_size[tool] = len(transition_results[tool])
    return transition_size


def get_covered_transitions(transition_size: dict):
    covered_transitions = {}
    for tool in transition_size.keys():
        if transition_size["all"] == 0:
            continue
        covered_transitions[tool] = transition_size[tool] / transition_size["all"]
    return covered_transitions


def get_missing_activities(activity_results: dict, declared_activities: list):
    missing_activities = {}
    missing_activities["declared"] = declared_activities
    declared_activities = set(declared_activities)
    for tool in activity_results.keys():
        visited_activities = set()
        activities = activity_results[tool]
        for activity in activities:
            visited_activities.add(activity)
        missing_activities[tool] = declared_activities - visited_activities
    return missing_activities


def get_failed_tools(transition_size: dict):
    failed_tools = []
    for tool in tools:
        if tool not in transition_size.keys():
            failed_tools.append(tool)
    return failed_tools


def update_intersections(transition_results: dict, transition_size: dict, covered_transitions: dict):
    for tool in transition_results.keys():
        if tool == "all":
            continue
        if transition_size["all"] == 0:
            continue
        for key2 in transition_results.keys():
            if key2 == "all":
                continue
            if tool == key2:
                continue
            intersection = set(transition_results[tool]) & set(transition_results[key2])
            transition_size[f"{tool} & {key2}"] = len(intersection)
            covered_transitions[f"{tool} & {key2}"] = len(intersection) / transition_size["all"]
    return transition_size


def save_transitions_results(all_transitions_results: dict, analysis_result_path: str):
    with open(analysis_result_path, "w") as f:
        for apk_path in all_transitions_results.keys():
            f.write(f"APK: {apk_path}\n")
            if "all" in all_transitions_results[apk_path].keys():
                all_result = all_transitions_results[apk_path]["all"]
                f.write(f"All results\n")
                for transition in all_result:
                    f.write(f"{transition}\n")
            for tool in all_transitions_results[apk_path].keys():
                f.write(f"Tool: {tool}\n")
                for transition in all_transitions_results[apk_path][tool]:
                    f.write(f"{transition}\n")


def save_to_csv(transition_size: dict, analysis_result_path: str):
    # convert dict to dataframe using pandas
    # save the dataframe to csv
    df = pd.DataFrame.from_dict(transition_size, orient='index')
    df.to_csv(analysis_result_path)


def single(apk_path: str):
    package_name, _, declared_activities, _ = parse_manifest_file(apk_path)
    print(f"declared_activities: {declared_activities}")
    try:
        raw_transitions, transition_results, transition_times, activity_results, activity_times = get_filtered_results(apk_path, declared_activities, package_name)
    except Exception as e:
        print(f"Error in {apk_path}")
        print(f"Error: {e}")
        return
    transition_chains_dict = {}
    # for tool in transition_results.keys():
    #     print(f"{tool}: {len(transition_results[tool])}")
    #     transitions = transition_results[tool]
    #     transition_chains = get_transition_chains(transitions, exported_activities)
    #     transition_chains_dict[tool] = transition_chains
    #     chain_lens = []
    #     for chain in transition_chains:
    #         chain_lens.append(len(chain))
    #     print(f"{tool}: {chain_lens}")
    diff_results = get_diff_results(transition_results)
    transition_size = get_transition_size(transition_results)
    covered_transitions = get_covered_transitions(transition_size)
    failed_tools = get_failed_tools(transition_size)
    missing_activities = get_missing_activities(activity_results, declared_activities)
    # return transition_results
    return apk_path, diff_results, transition_size, covered_transitions, failed_tools, missing_activities, transition_results, transition_chains_dict, transition_times, activity_times, raw_transitions


def multiple(apk_type, filter_internet, need_write: bool = True):
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = []
        for apk_path in get_apks_list(apk_type, filter_internet):
            futures.append(executor.submit(single, apk_path))
        all_raw_results = {}
        all_diff_results = {}
        all_transitions_size = {}
        all_covered_proportions = {}
        all_failed_tools = {}
        all_transition_chains = {}
        all_missing_activities = {}
        all_transition_results = {}
        all_transition_times = {}
        all_activity_times = {}
        for future in concurrent.futures.as_completed(futures):
            try:
                apk_path, diff_results, transition_size, covered_transitions, failed_tools, missing_activities, transition_results, transition_chains_dict, transition_times, activity_times, raw_transitions = future.result()
            except Exception as e:
                print(f"Error in {apk_path}")
                print(f"Error: {e}")
                continue
            all_diff_results[apk_path] = diff_results
            all_transitions_size[apk_path] = transition_size
            all_covered_proportions[apk_path] = covered_transitions
            all_failed_tools[apk_path] = failed_tools
            all_transition_chains[apk_path] = transition_chains_dict
            all_missing_activities[apk_path] = missing_activities
            # transition_results = single(apk_path)
            all_transition_results[apk_path] = transition_results
            all_transition_times[apk_path] = transition_times
            all_activity_times[apk_path] = activity_times
            all_raw_results[apk_path] = raw_transitions
        if not need_write:
            return all_diff_results, all_transitions_size, all_covered_proportions, all_failed_tools, all_missing_activities, all_transition_results
        analysis_result_dir = f"summary/data_analysis/{get_current_version()}"
        if not os.path.exists(analysis_result_dir):
            os.makedirs(analysis_result_dir, exist_ok=True)
        save_transitions_results(all_diff_results, f"{analysis_result_dir}/diff.txt")
        save_to_csv(all_transitions_size, f"{analysis_result_dir}/transition_size.csv")
        save_to_csv(all_covered_proportions, f"{analysis_result_dir}/covered_proportions.csv")
        save_to_csv(all_failed_tools, f"{analysis_result_dir}/failed_tools.csv")
        save_transitions_results(all_missing_activities, f"{analysis_result_dir}/missing_activities.txt")
        save_transitions_results(all_transition_results, f"{analysis_result_dir}/all_transitions.txt")
        save_transitions_results(all_raw_results, f"{analysis_result_dir}/all_raw_transitions.txt")
        result_transition_times = {}
        for tool in tools:
            result_transition_times[tool] = []
        for apk_path in all_transition_times.keys():
            tool_transition_times = all_transition_times.get(apk_path)
            for tool in tool_transition_times.keys():
                try:
                    result_transition_times[tool].extend(tool_transition_times[tool])
                except:
                    print(f"Error in {apk_path}")
                    print(f"tool: {tool}")
                    print(f"tool_transition_times: {tool_transition_times}")
                    pass
        result_activity_times = {}
        for tool in tools:
            result_activity_times[tool] = []
        for apk_path in all_activity_times.keys():
            tool_activity_times = all_activity_times.get(apk_path)
            for tool in tool_activity_times.keys():
                try:
                    result_activity_times[tool].extend(tool_activity_times[tool])
                except:
                    print(f"Error in {apk_path}")
                    print(f"tool: {tool}")
                    print(f"tool_activity_times: {tool_activity_times}")
                    pass
        save_to_csv(result_transition_times, f"{analysis_result_dir}/transition_times.csv")
        save_to_csv(result_activity_times, f"{analysis_result_dir}/activity_times.csv")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process to summarize the result of running tools.')
    parser.add_argument('--result_dir', type=str, help='Result directory', required=True)
    parser.add_argument('--apk_dir', type=str, help='Directory of APKs to test', default="all")
    parser.add_argument('--filter_internet', type=str, help='Whether exclude the apps with internet access', default="True")
    args = parser.parse_args()
    result_dir = args.result_dir
    apk_dir = args.apk_dir
    filter_internet = args.filter_internet
    set_current_version(result_dir)
    multiple(apk_dir, filter_internet)

    # print("begin")
    # result_dir = "second_round_no_internet"
    # set_current_version(result_dir)
    # print("***************Result dir: ", result_dir)
    # print(single("/mnt/hdd1/jkliu/Projects/ATGEmpirical/apks/androzoo/com.mlevap.datecalc_41.0.apk"))