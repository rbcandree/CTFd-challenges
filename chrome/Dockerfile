# Chrome 89.0.4389.114 (vulnerable to CVE-2021-21220)
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# basic and Chrome dependencies
RUN apt-get update && apt-get install -y \
    wget curl python3 python3-pip \
    libnss3 libxss1 libgtk-3-0 libasound2 libatk-bridge2.0-0 fonts-liberation \
    libappindicator3-1 xdg-utils libgbm1 libstdc++6 libssl1.1 libreadline8 \
    libncurses6 zlib1g iputils-ping iproute2 tcpdump net-tools \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install flask

# install Chrome
RUN wget -O /tmp/chrome.deb https://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/google-chrome-stable_89.0.4389.114-1_amd64.deb \
    && dpkg -i /tmp/chrome.deb || true \
    && apt-get -f install -y \
    && rm /tmp/chrome.deb \
    && rm -f /etc/apt/sources.list.d/google-chrome.list \
    && rm -f /etc/cron.daily/google-chrome

RUN echo "DISA{No_time_for_Firefox}" > /root/file.txt

COPY app/ /opt/app/
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/start.sh"]