sudo docker build -t follow:latest .
sudo docker run -v /home/adithya/Users:/mnt/Users --network="host" follow:latest