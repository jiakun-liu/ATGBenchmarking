FROM androidsdk/android-28
LABEL authors="jiakun"

RUN sdkmanager "system-images;android-28;google_apis;x86" \
    && avdmanager create avd --force --name api_28 --package 'system-images;android-28;google_apis;x86' --sdcard 1024M --device '9' \
    && apt-get update \
    && apt-get -yq install locales imagemagick imagemagick-doc \
    && locale-gen en_US en_US.UTF-8 \
    && dpkg-reconfigure locales