curl -fsSL https://code-server.dev/install.sh | sh
export PASSWORD=0000
export PORT=8080
export BIND_ADDRESS=0.0.0.0
code-server --bind-addr $BIND_ADDRESS:$PORT --user-data-dir /home
