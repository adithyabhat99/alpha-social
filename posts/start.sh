sudo docker build -t post:latest .
sudo docker run -v /home/adithya/Posts:/mnt/Posts --network="host" post:latest