FROM androidsdk/android-28
LABEL authors="jiakun"

# Install dependencies
RUN DEBIAN_FRONTEND=noninteractive \
    && apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libreadline-dev \
    zlib1g-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install rbenv and ruby-build to manage Ruby versions
RUN DEBIAN_FRONTEND=noninteractive \
    && git clone https://github.com/rbenv/rbenv.git ~/.rbenv \
    && echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc \
    && echo 'eval "$(rbenv init -)"' >> ~/.bashrc \
    && git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build

# Install Ruby 2.1 using rbenv
RUN ~/.rbenv/bin/rbenv install 2.1.0 \
    && ~/.rbenv/bin/rbenv global 2.1.0

# Set PATH for rbenv
ENV PATH /root/.rbenv/shims:/root/.rbenv/bin:$PATH

RUN DEBIAN_FRONTEND=noninteractive \
    && gem install nokogiri -v 1.9.0 \
    && sdkmanager "system-images;android-28;google_apis;x86" \
    && avdmanager create avd --force --name api_28 --package 'system-images;android-28;google_apis;x86' --sdcard 1024M --device '9' \
    && apt-get update \
    && apt-get -yq install python-pip locales \
    && pip install uiautomator==0.3.6 \
    && locale-gen en_US en_US.UTF-8 \
    && dpkg-reconfigure locales \

