FROM androidsdk/android-28
LABEL authors="jiakun"

RUN wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool -O /usr/local/bin/apktool \
    && wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.7.0.jar -O /usr/local/bin/apktool.jar \
    && chmod +x /usr/local/bin/apktool \
    && chmod +x /usr/local/bin/apktool.jar

RUN DEBIAN_FRONTEND=noninteractive \
    && sdkmanager "system-images;android-28;google_apis;x86" \
    && avdmanager create avd --force --name api_28 --package 'system-images;android-28;google_apis;x86' --sdcard 1024M --device '9' \
    && apt-get update \
    && apt-get -yq install python3-pip locales \
    && locale-gen en_US en_US.UTF-8 \
    && dpkg-reconfigure locales \
    && pip3 install pillow==8.3.2 \
    && pip3 install treelib~=1.5.5 graphviz scikit-image uiautomator2 func_timeout packaging==21.3 setuptools urllib3 --upgrade-strategy only-if-needed \