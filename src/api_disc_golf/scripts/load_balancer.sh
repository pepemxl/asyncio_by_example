#!/bin/bash


# Guarda la configuración en /etc/nginx/conf.d/load_balancer.conf.
# Reinicia Ngix
sudo systemctl restart nginx
#  test
# curl http://api-discgolf.com
