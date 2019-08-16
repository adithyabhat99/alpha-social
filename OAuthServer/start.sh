sudo docker build -t auth:latest .
sudo docker run --network="host" auth:latest