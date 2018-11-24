# docker build -t eb:docker -f Dockerfile .
FROM        jeonyh0924/eb-docker:base

# settings 모듈에 대한 환경변수 설정
ENV         DJANGO_SETTINGS_MODULE  config.settings.production

# 전체 코드를 복사
COPY        ./  /srv/project/
WORKDIR     /srv/project/

# 프로세스를 실행할 명령
WORKDIR     /srv/project/app

# Nginx
# 기존에 존재하던 Nginx 설정파일들 삭제
RUN         rm -rf  /etc/nginx/sites-available/* && \
            rm -rf  /etc/nginx/sites-enabled/* && \
            cp -f   /srv/project/.config/app.nginx \
                    /etc/nginx/sites-available/ && \
            ln -sf  /etc/nginx/sites-available/app.nginx \
                    /etc/nginx/sites-enabled/app.nginx

RUN         cp -f   /srv/project/.config/supervisord.conf \
                    /etc/supervisor/conf.d/

# 80번 포트 개방
EXPOSE      80

# Command로 supervisor실행
CMD         supervisord -n