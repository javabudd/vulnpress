FROM centos:7

ENV container webserver

RUN rm -rf /etc/yum/pluginconf.d/fastestmirror.conf

COPY yum/plugins/fastestmirror.conf /etc/yum/pluginconf.d/
COPY scripts/disable-ipv6.sh /disable-ipv6.sh
COPY scripts/fix-slow-dns.sh /fix-slow-dns.sh

RUN groupadd -r mysql && useradd -r -g mysql mysql && \
    chmod +x /disable-ipv6.sh /fix-slow-dns.sh && \
    sh /disable-ipv6.sh && \
    sh /fix-slow-dns.sh && \
    rpm -ivh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm && \
    rpm --import https://yum.mariadb.org/RPM-GPG-KEY-MariaDB && \
    rpm -ivh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm && \
    yum clean all && \
    yum -y update && \
    yum -y install yum-plugin-protectbase.noarch \
        nginx \
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
        MariaDB-server \
        MariaDB-client && \
    rm -rf /etc/nginx/nginx.conf /etc/php-fpm.d/www.conf /var/lib/mysql /etc/my.cnf /etc/my.cnf.d/* && \
    mkdir /var/lib/mysql

COPY my.cnf /etc/my.cnf
COPY my.cnf.d /etc/my.cnf.d
COPY nginx.conf /etc/nginx/nginx.conf
COPY wordpress.lan.conf /etc/nginx/conf.d/wordpress.lan.conf
COPY php-fpm.www.conf /etc/php-fpm.d/php-fpm.www.conf
COPY scripts/entrypoint.sh /entrypoint.sh

RUN chmod 644 \
        /etc/my.cnf \
        /etc/my.cnf.d/* && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 80 3306

CMD ["nginx", "-g", "daemon off;"]