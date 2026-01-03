# Pi‑Hole v4.3.2 base image
FROM pihole/pihole:4.3.2

# to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# install openssh-server, sqlite3 (DNS query database), using archives without applying full system upgrade
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list && \
    sed -i 's|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' /etc/apt/sources.list && \
    sed -i '/stretch-updates/d' /etc/apt/sources.list && \
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/90ignore-release-date && \
    apt-get update && \
    apt-get install -y openssh-server sqlite3 && \
    rm -rf /var/lib/apt/lists/*

# SSH confa: allows password authentication and enables root login
RUN echo "root:penguin101" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# DNS queries with the flag
RUN touch /etc/pihole/pihole-FTL.db && \
    sqlite3 /etc/pihole/pihole-FTL.db "CREATE TABLE IF NOT EXISTS queries (id INTEGER PRIMARY KEY, time INTEGER, type TEXT, domain TEXT, client TEXT, forward_dest TEXT, status INTEGER);" && \
    for i in $(seq 1 125); do \
         if [ "$i" -eq 69 ]; then \
             domain="DISA{I_managed_to_block_ads_but_not_You}.example.com"; \
         else \
             # Define an array of possible domains  
             domains=( "www.iltalehti.fi" "www.ylilauta.org" "www.tori.fi" "www.pi-hole.net" "www.wikipedia.org" ); \
             rnd=$(( RANDOM % ${#domains[@]} )); \
             domain=${domains[$rnd]}; \
         fi; \
         sqlite3 /etc/pihole/pihole-FTL.db "INSERT INTO queries (time, type, domain, client, forward_dest, status) VALUES (strftime('%s','now'), 'UDP', '$domain', '127.0.0.1', '8.8.8.8', 0);" ; \
    done

# ensure that SSH runtime directory exists
RUN mkdir -p /var/run/sshd

# create an s6 service directory for SSHD and copy the run script
RUN mkdir -p /etc/services.d/sshd
COPY sshd-run /etc/services.d/sshd/run
RUN chmod +x /etc/services.d/sshd/run

# expose port SSH port
EXPOSE 22