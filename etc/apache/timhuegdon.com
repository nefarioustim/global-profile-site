<VirtualHost *:80>

    ServerName dev.timhuegdon.com
    
    LogLevel debug

    DocumentRoot /var/www/timhuegdon.com/wsgi-scripts

#    Alias /robots.txt /var/www/timhuegdon.com/static/robots.txt
#    Alias /favicon.ico /var/www/timhuegdon.com/static/favicon.ico
    Alias /static /var/www/timhuegdon.com/static

    WSGIScriptAlias / /var/www/timhuegdon.com/wsgi-scripts/application.py

    <Directory /var/www/timhuegdon.com/wsgi-scripts>
        Order allow,deny
        Allow from all
    </Directory>

    ErrorLog "/var/www/timhuegdon.com/var/log/apache/error"
    CustomLog "/var/www/timhuegdon.com/var/log/apache/access" common
</VirtualHost>