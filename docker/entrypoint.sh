#!/bin/bash
set -eo pipefail

# Wordpress
if [ ! -d "/var/www/wordpress" ]; then
  wget https://wordpress.org/latest.tar.gz && tar xzvf latest.tar.gz -C /var/www/ && rm latest.tar.gz
  cp -f /wp-config.php /var/www/wordpress/
fi

# MariaDB
DATADIR=/var/lib/mysql

if [ ! -d "$DATADIR/mysql" ]; then
	mysql_install_db --user=root --basedir=/usr -ldata=/var/lib/mysql
fi

/usr/bin/mysqld_safe --user=root --basedir=/usr &
/usr/libexec/mariadb-wait-ready $!
mysql -e "CREATE DATABASE IF NOT EXISTS wordpress;"

# PHP-FPM
php-fpm -D

# Nginx
exec "$@"
