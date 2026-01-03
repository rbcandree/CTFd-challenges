FROM nginx:1.28.0-alpine

# index.html and files into the container's Nginx root directory
COPY index.html /usr/share/nginx/html/index.html
COPY telegraph.jpg /usr/share/nginx/html/telegraph.jpg
COPY codebook-edelcrantz-1795-scan.png /usr/share/nginx/html/codebook-edelcrantz-1795-scan.png
COPY Edelcrantz-Chifferbok-1808.pdf /usr/share/nginx/html/Edelcrantz-Chifferbok-1808.pdf

EXPOSE 80