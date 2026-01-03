#!/bin/bash

# starts virtual display
Xvfb :1 -screen 0 1280x800x24 &
export DISPLAY=:1
sleep 2

# starts Fluxbox window manager
fluxbox &

# launches Firefox in GUI mode (sandbox disabled)
firefox --no-remote --profile /root/.mozilla/firefox/pinkman &

# starts x11vnc server (no password for simplicity)
x11vnc -display :1 -nopw -forever -shared -rfbport 5900 &

# starts noVNC websocket proxy on port 8080
cd /opt/novnc
./utils/novnc_proxy --vnc localhost:5900 --listen 8080 &

# keeps container running
tail -f /dev/null