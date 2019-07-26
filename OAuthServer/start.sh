sudo docker build -t auth:latest .
sudo docker run -v /home/adithya/Users:/mnt/Users --network="host" auth:latest