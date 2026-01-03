from flask import Flask, request, render_template
import subprocess
import time
import os
import re

app = Flask(__name__)

FLAG_PATH = "/tmp/flag_triggered"
PCAP_FILE = "/tmp/network_out.pcap"

@app.route('/', methods=['GET', 'POST'])
def index():
    url = None
    flag = None

    if os.path.exists(FLAG_PATH):
        os.remove(FLAG_PATH)
    if os.path.exists(PCAP_FILE):
        os.remove(PCAP_FILE)

    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            print(f"[*] Launching Chrome with URL: {url}")

            tcpdump_proc = subprocess.Popen([
                'tcpdump', '-i', 'any', 'tcp', '-nn', '-w', PCAP_FILE
            ])

            subprocess.Popen([
                'google-chrome-stable',
                '--no-sandbox',
                '--disable-gpu',
                '--headless',
                '--disable-software-rasterizer',
                '--user-data-dir=/tmp/chrome-profile',
                url
            ])
            time.sleep(10)

            tcpdump_proc.terminate()
            tcpdump_proc.wait()

            try:
                output = subprocess.check_output([
                    'tcpdump', '-nn', '-r', PCAP_FILE
                ]).decode()

                for line in output.splitlines():
                    # example: IP 172.17.0.2.49234 > 192.168.1.100.4444: Flags [S], ...
                    if re.search(r'IP\s+\d{1,3}(\.\d{1,3}){3}\.\d+ > (?!127\.0\.0\.1)(\d{1,3}\.){3}\d+\.\d+', line):
                        print("[+] Outbound TCP connection detected!")
                        with open(FLAG_PATH, 'w') as f:
                            f.write("Check your msfconsole or send meta- greetings again")
                        flag = "Check your msfconsole or send meta- greetings again"
                        break

            except subprocess.CalledProcessError as e:
                print("[-] Error analyzing pcap file:", e)

    return render_template('index.html', url=url, flag=flag)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)