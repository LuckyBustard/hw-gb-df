FROM nginx:alpine

RUN mkdir -p /var/www/site
WORKDIR /var/www/site
COPY ./main_site.conf /etc/nginx/sites-available/
COPY ./media /var/www/site/media
COPY ./static /var/www/site/static