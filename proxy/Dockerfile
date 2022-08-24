FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="togrulir"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./default-ssl.conf.tpl /etc/nginx/default-ssl.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./options-ssl-nginx.conf /etc/nginx/options-ssl-nginx.conf
COPY ./run.sh /run.sh

ENV LISTEN_PORT=80
ENV LISTEN_PORT_SECURE=443
ENV APP_HOST=app
ENV APP_PORT=9000

USER root

RUN mkdir -p /vol/static/ && \
    chmod 755 /vol/static && \
    touch /etc/certbot/conf.d/default.conf && \
    chown certbot:certbot /etc/certbot/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static
VOLUME /vol/www

USER nginx

CMD ["/run.sh"]
