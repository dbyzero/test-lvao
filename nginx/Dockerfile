FROM nginx

ARG APP_DOMAIN_NAME
ARG API_DOMAIN_NAME

RUN mkdir -p /var/www/acme-challenge

COPY ./server.conf /etc/nginx/conf.d/default.conf

RUN sed -e "s/{{APP_DOMAIN_NAME}}/$APP_DOMAIN_NAME/g" /etc/nginx/conf.d/default.conf > /etc/nginx/conf.d/default.conf.tmp && mv /etc/nginx/conf.d/default.conf.tmp /etc/nginx/conf.d/default.conf
RUN sed -e "s/{{API_DOMAIN_NAME}}/$API_DOMAIN_NAME/g" /etc/nginx/conf.d/default.conf > /etc/nginx/conf.d/default.conf.tmp && mv /etc/nginx/conf.d/default.conf.tmp /etc/nginx/conf.d/default.conf

