#!/bin/bash

APK_FILE=$1 # e.g., xx.apk
OUTPUT_DIR=$2
TEST_TIME=$3 # e.g., 10s, 10m, 10h

AVD_SERIAL=emulator-5554 # e.g., emulator-5554
AVD_NAME=api_28 # e.g., base
HEADLESS=-no-window # e.g., -no-window

TOOL_DIR=./Stoat/Stoat/bin
TOOL_NAME=stoat

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

current_dir=$(pwd)

app_package_name=$(../base/get_package_name.sh $APK_FILE)

result_dir=$(../base/create_result_dir.sh $APK_FILE $OUTPUT_DIR $AVD_SERIAL $AVD_NAME $TOOL_NAME)
echo "** CREATING RESULT DIR (${AVD_SERIAL}): " $result_dir

../base/run_emulator.sh $AVD_SERIAL $AVD_NAME $HEADLESS $result_dir $app_package_name

../base/install_app.sh $APK_FILE $AVD_SERIAL $result_dir

# run Stoat
echo "** RUN STOAT (${AVD_SERIAL})"
../base/log_time.sh $result_dir $TOOL_NAME $AVD_SERIAL
cd $TOOL_DIR
avd_port=${AVD_SERIAL:9:13}
base_num=3554
stoat_port="$(($avd_port-$base_num))"
ruby run_stoat_testing.rb --app_dir $result_dir --apk_path $APK_FILE --avd_port $avd_port --stoat_port $stoat_port --model_time 1h --mcmc_time 5h --project_type gradle 2>&1 | tee $result_dir/stoat.log
cd $current_dir
../base/log_time.sh $result_dir $TOOL_NAME $AVD_SERIAL

../base/stop_emulator.sh $AVD_SERIAL

echo "@@@@@@ Finish (${AVD_SERIAL}): " $app_package_name "@@@@@@@"