#!/bin/bash

# get the screenshot of the emulator

AVD_SERIAL=$1 # e.g., emulator-5554
RESULT_DIR=$2

mkdir -p $RESULT_DIR/screenshots
OUTPUT_DIR=$RESULT_DIR/screenshots

function take_screenshot() {
    adb -s $AVD_SERIAL shell screencap -p /sdcard/screenshot.png
    adb -s $AVD_SERIAL pull /sdcard/screenshot.png "$OUTPUT_DIR"/new.png
}

function get_current_activity() {
#    adb -s $AVD_SERIAL shell dumpsys activity activities | grep mFocusedApp | perl -pe 's/.*mFocusedApp=ActivityRecord\{[^\s]+ [^\s]+ ([^\s]+\/[^\s]+)\}.*/$1/'
#    adb -s $AVD_SERIAL shell dumpsys activity activities | grep mResumedActivity | perl -pe 's/.*mResumedActivity: ActivityRecord\{[^\s]+ [^\s]+ ([^\s]+\/[^\s]+)\}.*/$1/'
    adb -s $AVD_SERIAL shell dumpsys activity activities | grep mResumedActivity | perl -pe 's/.*mResumedActivity: ActivityRecord\{[^\s]+ [^\s]+ ([^\s]+\/[^\s]+).*/$1/'
}

take_screenshot
cp $OUTPUT_DIR/new.png $OUTPUT_DIR/last.png

take_screenshot
cp $OUTPUT_DIR/new.png $OUTPUT_DIR/last.png

take_screenshot
cp $OUTPUT_DIR/new.png $OUTPUT_DIR/last.png

while true; do
    take_screenshot
    diff_output=$(compare -metric AE "$OUTPUT_DIR"/new.png "$OUTPUT_DIR"/last.png "$OUTPUT_DIR"/diff.png 2>&1)
    diff_value=$(echo $diff_output | awk '{printf("%d",$0)}')
    echo $diff_value
    if [ "$diff_value" -gt 1000 ]; then
        current_activity=$(get_current_activity)
        current_activity=$(echo $current_activity | tr -d '/')
        echo current_activity: $current_activity
        current_date_time="`date "+%Y-%m-%d-%H-%M-%S"`"
        echo current_date_time: $current_date_time
        cp $OUTPUT_DIR/new.png $OUTPUT_DIR/$current_activity-$current_date_time.png
        cp $OUTPUT_DIR/new.png $OUTPUT_DIR/last.png
    fi

done
