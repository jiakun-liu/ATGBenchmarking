FROM androidsdk/android-28
LABEL authors="jiakun"

RUN DEBIAN_FRONTEND=noninteractive \
    && sdkmanager "system-images;android-28;google_apis;x86" \
    && avdmanager create avd --force --name api_28 --package 'system-images;android-28;google_apis;x86' --sdcard 1024M --device '9' \
    && apt-get update \
    && apt-get -yq install lsof python3-pip locales \
    && pip3 install protobuf==3.6.1 pillow==8.3.2 \
    && pip3 install tensorflow==1.12 androguard==3.3.5 matplotlib scipy pyflann-py3 --upgrade-strategy only-if-needed \
    && wget https://github.com/the-themis-benchmarks/droidbot/archive/refs/heads/themis-branch.zip \
    && unzip themis-branch.zip \
    && cd  droidbot-themis-branch \
    && pip3 install -e . --upgrade-strategy only-if-needed \
    && locale-gen en_US en_US.UTF-8 \
    && dpkg-reconfigure locales