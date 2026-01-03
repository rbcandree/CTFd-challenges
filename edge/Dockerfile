# Base image
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:1

# dependencies
RUN apt-get update && apt-get install -y \
    wget curl gnupg2 software-properties-common \
    x11vnc xvfb fluxbox xterm dbus dbus-x11 \
    python3 python3-pip git net-tools apache2 \   
    && rm -rf /var/lib/apt/lists/*

# noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/novnc \
    && ln -s /opt/novnc/vnc.html /opt/novnc/index.html

# Microsoft Edge 95.0.1020.40
RUN wget -O /tmp/microsoft-edge-stable_95.0.1020.40-1_amd64.deb \
    https://packages.microsoft.com/repos/edge/pool/main/m/microsoft-edge-stable/microsoft-edge-stable_95.0.1020.40-1_amd64.deb \
    && apt-get update \
    && apt-get install -y /tmp/microsoft-edge-stable_95.0.1020.40-1_amd64.deb \
    && rm /tmp/microsoft-edge-stable_95.0.1020.40-1_amd64.deb

# prevents Edge from updating
RUN rm -f /etc/apt/sources.list.d/microsoft-edge-stable.list || true && \
    apt-get remove -y unattended-upgrades || true && \
    rm -f /opt/microsoft/msedge/msedge-updater || true && \
    chmod -x /opt/microsoft/msedge/msedge-updater || true

#COPY flag-extension/ /root/flag-extension/
COPY start.sh /usr/local/bin/start.sh
COPY launch_edge.sh /usr/local/bin/launch_edge.sh
COPY edge-wrapper.sh /usr/local/bin/edge-wrapper.sh

RUN chmod +x /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/launch_edge.sh
RUN chmod +x /usr/local/bin/edge-wrapper.sh

# custom Fluxbox menu
COPY fluxbox_menu /root/.fluxbox/menu
RUN echo 'session.menuFile: /root/.fluxbox/menu' >> /root/.fluxbox/init

COPY vuln_page.html /var/www/html/index.html
RUN ln -sf /var/www/html/index.html /var/www/html/vuln.html

EXPOSE 80 8080 5900

ENTRYPOINT ["/usr/local/bin/start.sh"]