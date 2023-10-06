#!/usr/bin/env bash
# A Bash script that sets up your web servers for the deployment of web_static.

sudo apt-get update

sudo apt-get -y install nginx

sudo mkdir -p /data/web_static/releases/test/

sudo mkdir -p /data/web_static/shared/

sudo touch /data/web_static/releases/test/index.html

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -hR ubuntu:ubuntu /data/

sudo sed -i "s#^\s*location /hbnb_static/.*#&\n\talias /data/web_static/current/;#" /etc/nginx/sites-available/default

sudo service nginx restart

exit 0

