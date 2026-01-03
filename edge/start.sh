#!/bin/bash

# virtual display
Xvfb :1 -screen 0 1280x800x24 &
sleep 2

# D-Bus daemon
dbus-daemon --system --fork

fluxbox &

# x11vnc server
x11vnc -display :1 -nopw -forever -shared -rfbport 5900 &

# noVNC
cd /opt/novnc
./utils/novnc_proxy --vnc localhost:5900 --listen 8080 &

service apache2 start
sleep 2

#microsoft-edge --no-sandbox --user-data-dir=/root/.config/microsoft-edge &
microsoft-edge --no-sandbox --user-data-dir=/root/.config/microsoft-edge http://localhost/vuln.html &

# keeps the container running
tail -f /dev/null