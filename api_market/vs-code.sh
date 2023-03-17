docker run -it -p 0.0.0.0:8080:8080 \
  -v "${PWD}/vscode-data:/home/coder/project" \
  codercom/code-server