FROM centos:7

RUN rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
    rpm -ivh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm && \
    rpm --import https://yum.mariadb.org/RPM-GPG-KEY-MariaDB && \
    yum -y install yum-plugin-protectbase.noarch \
        nginx \
        expect \
        wget \
        php70w \
        php70w-opcache \
        php70w-cli \
        php70w-intl \
        php70w-mbstring \
        php70w-mcrypt \
        php70w-mysqlnd \
        php70w-xml \
        php70w-fpm \
        mariadb-server \
        mariadb-client

RUN rm -rf /etc/nginx/nginx.conf /etc/php-fpm.d/www.conf

COPY entrypoint.sh /
COPY wp-config.php /
COPY nginx.conf /etc/nginx/nginx.conf
COPY wordpress.lan.conf /etc/nginx/conf.d/wordpress.lan.conf
COPY php-fpm.www.conf /etc/php-fpm.d/php-fpm.www.conf

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 80 3306

CMD ["nginx", "-g", "daemon off;"]
