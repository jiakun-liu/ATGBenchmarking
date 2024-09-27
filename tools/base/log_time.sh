#!/bin/bash

result_dir=$1
tool_name=$2
AVD_SERIAL=$3


adb -s $AVD_SERIAL shell date "+%Y-%m-%d-%H:%M:%S" >> ${result_dir}/${tool_name}_testing_time_on_emulator.txt