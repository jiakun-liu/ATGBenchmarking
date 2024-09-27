#!/bin/bash

APK_FILE=$1
AVD_SERIAL=$2
result_dir=$3
LOGIN_SCRIPT=$4

sleep 20
## login if necessary
#if [[ $LOGIN_SCRIPT != "" ]]
#then
#    echo "** APP LOGIN (${AVD_SERIAL})"
#
#    # enable if use the login script
#    # adb -s $AVD_SERIAL install -g $APK_FILE &> $result_dir/install.log
#    # echo "** INSTALL APP (${AVD_SERIAL})"
#    # python3 $LOGIN_SCRIPT ${AVD_SERIAL} 2>&1 | tee $result_dir/login.log
#
#    # enable if use the snapshot (already login, do not need to install the app)
#    echo " *** Login SUCCESS ****" >> $result_dir/login.log
#
#else
#    # install the app
#    sleep 5 # wait for a few seconds before installation to avoid such error: "adb: connect error for write: closed"
#    adb -s $AVD_SERIAL install -g $APK_FILE &> $result_dir/install.log
#    echo "** INSTALL APP (${AVD_SERIAL})"
#fi

adb -s $AVD_SERIAL install -g $APK_FILE &> $result_dir/install.log
echo "** INSTALL APP (${AVD_SERIAL})"