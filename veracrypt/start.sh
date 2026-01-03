#!/bin/bash
set -e
export DISPLAY=:1

# Start Xvfb virtual display
Xvfb :1 -screen 0 1280x720x16 >/var/log/xvfb.log 2>&1 &
sleep 1

# Start XFCE desktop as ctfuser
su -c "startxfce4 >/home/ctfuser/xfce.log 2>&1 &" -s /bin/bash ctfuser

# Start x11vnc (VNC server)
x11vnc -display :1 -nopw -forever -shared -rfbport 5901 -localhost >/var/log/x11vnc.log 2>&1 &

# Start noVNC proxy (web browser access)
 /opt/novnc/utils/novnc_proxy --vnc localhost:5901 --listen 6080 >/var/log/novnc.log 2>&1 &

# Help note
cat > /home/ctfuser/note.txt <<'EOF'
...You have found a crumpled piece of paper near the crypt:
"
- ctfuser:ctfpass
- Tools preinstalled: hashcat, locate, nano, python3, veracrypt, sleuthkit, wget

- Step 1. Generate a hash:
  sudo dd if=<container.vc> of=/home/ctfuser/<container.vc>.hash bs=512 count=1

- Step 2. Decrypt <container.vc>:
  sudo veracrypt --text --non-interactive --filesystem=none --password="<yourpassword>" --pim=0 --protect-hidden=no --mount <container.vc> /home/ctfuser/container.raw

- Step 3. Analyze the decrypted container.raw image:
  fls /home/ctfuser/container.raw

- Step 4. Extract:
  icat /home/ctfuser/container.raw <inode_number> > /home/ctfuser/bingo.txt
  *Replace <inode_number> with the actual number you discovered at Step 3

"
EOF
chown ctfuser:ctfuser /home/ctfuser/note.txt

# Keep container alive
tail -f /dev/null
