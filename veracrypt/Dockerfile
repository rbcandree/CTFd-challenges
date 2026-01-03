FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    xfce4 xfce4-terminal xfce4-panel xfce4-session xfce4-settings xfdesktop4 \
    xfce4-goodies thunar thunar-volman gvfs gvfs-backends udisks2 \
    adwaita-icon-theme tango-icon-theme gnome-icon-theme hicolor-icon-theme \
    xorg dbus-x11 x11-xserver-utils \
    x11vnc xvfb \
    python3 python3-pip wget curl unzip \
    hashcat ocl-icd-libopencl1 pocl-opencl-icd \
    git p7zip-full psmisc sudo nano mlocate vim less procps ca-certificates \
    net-tools iproute2 socat dialog sleuthkit \
    software-properties-common lsb-release gnupg \
 && add-apt-repository -y ppa:mozillateam/ppa \
 && printf 'Package: firefox*\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 501\n' > /etc/apt/preferences.d/mozillateam-ppa \
 && apt-get update \
 && apt-get install -y firefox \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# noVNC from source
RUN git clone https://github.com/novnc/noVNC.git /opt/novnc \
 && ln -s /opt/novnc/vnc_lite.html /opt/novnc/index.html

# Install VeraCrypt CLI
RUN wget -O /tmp/veracrypt.deb https://launchpad.net/veracrypt/trunk/1.26.24/+download/veracrypt-1.26.24-Ubuntu-22.04-amd64.deb \
 && apt-get update && apt-get install -y ./tmp/veracrypt.deb \
 && rm -f /tmp/veracrypt.deb

# Users: ctfuser (1000)
RUN useradd -m -u 1000 -s /bin/bash ctfuser \  
 && echo "ctfuser:ctfpass" | chpasswd \  
 && usermod -aG sudo ctfuser

# Volume, directories
RUN mkdir -p /home/ctfuser/Desktop /opt/volumes /usr/lib/firefox/browser/features/.support/.private \
 && chown -R ctfuser:ctfuser /home/ctfuser \
 && chown -R root:root /opt/volumes /usr/lib/firefox/browser/features/.support \
 && chmod 755 /opt/volumes \
 && chmod -R 700 /usr/lib/firefox/browser/features/.support

WORKDIR /home/ctfuser

# Desktop shortcut
RUN echo '[Desktop Entry]\n\
Name=Terminal\n\
Comment=Launch terminal\n\
Exec=xfce4-terminal\n\
Icon=utilities-terminal\n\
Terminal=false\n\
Type=Application\n\
Categories=Utility;System;\n' \
 > /home/ctfuser/Desktop/terminal.desktop \
 && chmod +x /home/ctfuser/Desktop/terminal.desktop \
 && chown ctfuser:ctfuser /home/ctfuser/Desktop/terminal.desktop

# Helpers
COPY secret.vc /opt/volumes/secret.vc
COPY minirockyou.txt /home/ctfuser/minirockyou.txt
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh
COPY container.raw /usr/lib/firefox/browser/features/.support/.private/container.raw
RUN chown root:root /usr/lib/firefox/browser/features/.support/.private/container.raw \
 && chmod 600 /usr/lib/firefox/browser/features/.support/.private/container.raw

# Trick script behavior:
#  - If called with: --filesystem=none --password="password1" --mount /opt/volumes/secret.vc /home/ctfuser/container.raw
#    -> copies the hidden container.raw to <dst>, chowns to ctfuser, prints success.
#  - If called with wrong password -> prints "Error: fusermount: mount failed: Operation not permitted"
#  - If called with --help/-h -> prints usage
#  - Otherwise -> prints generic invalid arguments error
RUN mv /usr/bin/veracrypt /usr/bin/veracrypt.real || true \
 && { \
    echo '#!/bin/bash'; \
    echo 'echo "V3raCrypt 1.26.24 - Command-Line Interface"'; \
    echo ''; \
    echo 'if [[ "$1" == "--help" || "$1" == "-h" ]]; then'; \
    echo '  echo "Usage: veracrypt [OPTIONS] <volume_path> [mount_point]"'; \
    echo '  echo "  --mount <volume> <mount_point>   Mounts the specified volume"'; \
    echo '  echo "  --filesystem=none               Do not mount a filesystem"'; \
    echo '  echo "  --text                         Use text user interface"'; \
    echo '  echo "  --non-interactive              Do not prompt for user input"'; \
    echo '  exit 0'; \
    echo 'fi'; \
    echo ''; \
    echo 'if [[ "$*" == *"--mount"* ]]; then'; \
    echo '  SRC=""; DST=""; PASS="";'; \
    echo '  for arg in "$@"; do'; \
    echo '    case "$arg" in'; \
    echo '      /opt/volumes/*) SRC="$arg" ;;'; \
    echo '      /home/ctfuser/*) DST="$arg" ;;'; \
    echo '      --password=*) PASS="${arg#--password=}" ;;'; \
    echo '    esac'; \
    echo '  done'; \
    echo '  if [[ "$SRC" == "/opt/volumes/secret.vc" && "$DST" == "/home/ctfuser/container.raw" ]]; then'; \
    echo '    if [[ "$PASS" == "password1" ]]; then'; \
    echo '      echo "Verifying..."; sleep 1'; \
    echo '      echo "Decrypting volume..."; sleep 2'; \
    echo '      cp /usr/lib/firefox/browser/features/.support/.private/container.raw "$DST"'; \
    echo '      chown ctfuser:ctfuser "$DST"'; \
    echo '      echo "Volume $SRC has been successfully decrypted to $DST"'; \
    echo '      exit 0'; \
    echo '    else'; \
    echo '      echo "Error: fusermount: mount failed: Operation not permitted"'; \
    echo '      exit 1'; \
    echo '    fi'; \
    echo '  else'; \
    echo '    echo "Error: fusermount: mount failed: Operation not permitted"'; \
    echo '    exit 1'; \
    echo '  fi'; \
    echo 'fi'; \
    echo ''; \
    echo 'echo "Error: Invalid arguments. Use --help for usage information."'; \
    echo 'exit 1'; \
 } > /usr/bin/veracrypt \
 && chmod +x /usr/bin/veracrypt


# Refresh the database for latest files
RUN updatedb

EXPOSE 6080

CMD ["/usr/local/bin/start.sh"]
