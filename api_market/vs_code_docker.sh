sudo docker run -it -p 0.0.0.0:8080:8080 \
  -v "${PWD}:/home/coder/project" \
  -e "PASSWORD=0000" \
  codercom/code-server