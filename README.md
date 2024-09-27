# Replication Package for the paper "Activity Transition Graph Generation: How Far Are We?"

This repository contains the replication package for the paper "Activity Transition Graph Generation: How Far Are We?" submitted to the ACM Transactions on Software Engineering and Methodology (TOSEM) journal. The replication package contains the following files:

- `README.md`: this file.
- `tools/`: the implementation of the tools used in the study. We also provide the docker file to run the tools in `tools/{tool_name}/docker/Dockerfile`.
- `summary/data_analysis/final/gt_transitions_bigger1.txt` contains the ground truth transitions as well as the list of apps that are used in the study.
- `script/run_tools/run_batch.py` is the script to run the tools on the apps.
- `script/data_extract/extract_all.py` is the script to extract the transitions from the tools' output.
- `script/data_analysis/summarized.py` is the script to summarize the transitions.

Users should follow the instructions below to replicate the study.
- Users could use the scripts in `script/data` to download apps from F-Droid and AndroZoo (with their own API keys).
- Users should build the docker images for the tools in `tools/` one by one.
- Users should run the script `script/run_tools/run_batch.py` to run the tools on the apps.
- Users should run the script `script/data_extract/extract_all.py` to extract the transitions from the tools' output.
- Users should run the script `script/data_analysis/summarized.py` to summarize the transitions.

## Combining the results from different tools

Note that different tools have different output formats, so the extraction script is designed to handle the output of each tool. Please see the files in `script/data_extract/extract` to understand the extraction process for each tool.

Specifically, the extraction script reads the output files from each tool, which may include different formats and structures, and extracts the transitions in a unified format, i.e., `{Start Activity} -> {End Activity}`, to ensure that the transitions are consistently formatted across all tools.
The extracted transitions are then saved in a file that can be used for further analysis, e.g., we can combine the results from different tools to get a comprehensive view of the activity transitions.

For example, the log of FastBot2 records the visit to the activity. Therefore, we need to extract the visited activities and establish the transitions based on the order of visits. The extraction script processes the log files, identifies the start, end, and the restart of the app, and constructs the transitions accordingly.