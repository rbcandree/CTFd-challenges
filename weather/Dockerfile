# Lets use the nginx:alpine image
FROM nginx:1.28.0-alpine

# Copy our custom index.html and the JSON file into the container’s Nginx root directory
COPY index.html /usr/share/nginx/html/index.html
COPY weather_data.json /usr/share/nginx/html/weather_data.json