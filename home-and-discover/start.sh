sudo docker build -t home:latest .
sudo docker run -v /home/adithya/Posts:/mnt/Posts --network="host" home:latest