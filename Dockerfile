# Use the official Nginx image
FROM nginx:alpine

# Copy the default Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy static files to serve
COPY static/ /usr/share/nginx/html/static/
