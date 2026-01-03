# Mozilla Firefox 79.0 (vulnerable to CVE-2020-26950)
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV MOZ_DISABLE_CONTENT_SANDBOX=1

# basic and Firefox dependencies
RUN apt-get update && apt-get install -y \
  wget curl python3 python3-pip git \
  libnss3 libxss1 libgtk-3-0 libasound2 libatk-bridge2.0-0 fonts-liberation \
  libappindicator3-1 xdg-utils libgbm1 libstdc++6 libssl1.1 libreadline8 \
  libncurses6 zlib1g iputils-ping iproute2 tcpdump net-tools \
  fluxbox xvfb x11-utils x11vnc dbus-x11 \
  libdbus-glib-1-2 python3-websockify \
  && rm -rf /var/lib/apt/lists/*

# removes terminal shells from menu visibility
RUN apt-get purge -y xterm

RUN pip3 install flask

# installs Firefox
RUN wget -O /tmp/firefox.tar.bz2 "https://ftp.mozilla.org/pub/firefox/releases/79.0/linux-x86_64/en-US/firefox-79.0.tar.bz2" \
    && tar -xjf /tmp/firefox.tar.bz2 -C /opt/ \
    && ln -s /opt/firefox/firefox /usr/bin/firefox \
    && rm /tmp/firefox.tar.bz2

# disables Firefox auto-update via policies.json
RUN mkdir -p /opt/firefox/distribution
COPY policies.json /opt/firefox/distribution/policies.json

# fully locks update prefs
COPY mozilla.cfg /opt/firefox/mozilla.cfg
RUN echo '[XRE]\nEnableProfileMigrator=false\nEnableAppUpdate=false\n' > /opt/firefox/defaults/pref/override.ini \
    && echo 'pref("general.config.filename", "mozilla.cfg");' > /opt/firefox/defaults/pref/local-settings.js

# removes updater binary
RUN rm -f /opt/firefox/updater

# Firefox profile
RUN mkdir -p /root/.mozilla/firefox/pinkman
COPY logins.json /root/.mozilla/firefox/pinkman/logins.json
RUN chmod 600 /root/.mozilla/firefox/pinkman/logins.json

RUN echo "Have you checked my Firefox stored login credentials?" > /root/file1.txt
RUN echo "You are on the right way." > /root/.mozilla/file2.txt
RUN echo "Have you seen the Breaking Bad series? -> Firefox profile folder." > /root/.mozilla/firefox/file3.txt
RUN echo "Yes, in this folder." > /root/.mozilla/firefox/pinkman/file4.txt

# noVNC setup
RUN git clone https://github.com/novnc/noVNC.git /opt/novnc \
    && ln -s /opt/novnc/vnc.html /opt/novnc/index.html

COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# custom Fluxbox menu
COPY fluxbox_menu /root/.fluxbox/menu
RUN echo 'session.menuFile: /root/.fluxbox/menu' >> /root/.fluxbox/init

EXPOSE 8080 5900

ENTRYPOINT ["/usr/local/bin/start.sh"]