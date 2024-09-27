#!/bin/bash

APK_FILE=$1 # e.g., xx.apk
OUTPUT_DIR=$2
AVD_SERIAL=$3 # e.g., emulator-5554
AVD_NAME=$4 # e.g., base
TOOL_NAME=$5 # e.g., ape

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

current_date_time="`date "+%Y-%m-%d-%H-%M-%S"`"
apk_file_name=`basename $APK_FILE`
result_dir=$OUTPUT_DIR/$apk_file_name.$TOOL_NAME.result.$AVD_SERIAL.$AVD_NAME\#$current_date_time
mkdir -p $result_dir

echo $result_dir