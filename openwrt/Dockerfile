# OpenWRT v24.10.1 base image.
FROM openwrt/rootfs:x86-64-v24.10.1

ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /var/lock && \
    opkg update && \
    opkg install luci luci-app-commands && \
    rm -rf /var/lib/opkg && \
    echo "Keep searching. Have you checked my images?" > /root/file.txt

# Custom Commands to /etc/config/luci
RUN printf "config command\n\toption command 'id'\n\toption param '0'\n\nconfig command\n\toption command 'pwd'\n\toption param '0'\n\nconfig command\n\toption command 'ls -la'\n\toption param '1'\n\nconfig command\n\toption command 'find'\n\toption param '1'\n\nconfig command\n\toption command 'cat'\n\toption param '1'\n" >> /etc/config/luci

COPY logo.png /www/luci-static/bootstrap/logo_48.png

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# port 80 for CuLI web interface
EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]