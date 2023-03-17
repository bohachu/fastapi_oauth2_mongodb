sudo docker run --rm -p 443:443 \
    -v $(pwd)/html:/usr/share/nginx/html \
    -v $(pwd)/letsencrypt:/etc/letsencrypt \
    -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf \
    --name nginx \
    nginx
