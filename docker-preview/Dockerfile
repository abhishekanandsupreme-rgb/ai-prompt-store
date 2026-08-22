FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY docker-preview/nginx.conf /etc/nginx/conf.d/default.conf

# Copy website static assets
COPY website/ /usr/share/nginx/html/

EXPOSE 80
