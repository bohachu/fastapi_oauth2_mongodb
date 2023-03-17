sudo docker run -it --rm --name certbot \
-v "$(pwd)/letsencrypt:/etc/letsencrypt" \
-p 80:80 -p 443:443 \
certbot/certbot \
certonly --standalone --agree-tos --no-eff-email --email cbh@cameo.tw -d roy-dist.g.cameo.tw --renew-by-default
