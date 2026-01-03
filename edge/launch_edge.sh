#!/bin/bash

# Edge profile dir
mkdir -p /root/.config/microsoft-edge/Default

# Edge launch
microsoft-edge --no-sandbox --user-data-dir=/root/.config/microsoft-edge &