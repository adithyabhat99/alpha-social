sudo docker build -t profile:latest .
sudo docker run -v /home/adithya/Users:/mnt/Users --network="host" profile:latest