mkdir ~/mongodb
docker run -d -p 27017:27017 --name mongodb -v ~/mongodb:/data/db mongo
