# Lets use the nginx:alpine image
FROM nginx:1.28.0-alpine

# index.html and images into the container’s Nginx root directory
COPY index.html /usr/share/nginx/html/index.html
COPY semaphore1.jpg /usr/share/nginx/html/semaphore1.jpg
COPY semaphore2.jpg /usr/share/nginx/html/semaphore2.jpg

EXPOSE 80