#!/bin/bash

APK_FILE=$1

app_package_name=`aapt dump badging $APK_FILE | grep package | awk '{print $2}' | sed s/name=//g | sed s/\'//g`
echo $app_package_name