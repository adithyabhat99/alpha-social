install docker-(docker official way)
https://askubuntu.com/questions/938700/how-do-i-install-docker-on-ubuntu-16-04-lts

Cheatsheet-

to remove untagged images-
sudo docker images -q --filter "dangling=true" | sudo xargs docker rmi -f

to stop an image-
sudo docker stop imageid

to stop all images-
sudo docker stop $(sudo docker ps -aq)

to delete an image-
sudo docker rmi imageid -f

to list running containers-
sudo docker container ls

to list all containers-
sudo docker container ls -a

to find ip address of a container-
sudo docker inspect containerid | grep IP



nginx-
docker pull nginx
https://blog.docker.com/2015/04/tips-for-deploying-nginx-official-image-with-docker/

flask-
sudo docker build -t profile:latest .
sudo docker run -v /home/adithya/Users:/mnt/Users --network="host"  profile:latest

mysql-
sudo docker pull mysql/mysql-server:5.6

Users database-

sudo docker run --detach --name=usersmysql -p 52000:3306
--env="MYSQL_ROOT_PASSWORD=123654654" mysql/mysql-server:5.6

sudo docker exec -it usersmysql mysql -uroot -p

Posts database-

sudo docker run --detach --name=postsmysql -p 52100:3306  --env="MYSQL_ROOT_PASSWORD=123654654" mysql/mysql-server:5.6

sudo docker exec -it postsmysql mysql -uroot -p

For both databases-
create user 'root'@'172.17.0.1' identified by '123654654';
GRANT ALL PRIVILEGES ON * . * TO 'root'@'172.17.0.1';


/* Future work
There is an authentification microservice which will return a token on correct username and password

There will be a post microservice which will work on users posting images or videos

There will be a profile service which will handle users following and create or delete account etc.

There will be a home page service which will precompute the home page for every user
and return whenever asked

There will also be a push service which sends sms/emails etc.

There will be a front and server as a microservice, this will be done at the end 

Activity database
Discover service
Messaging service
*/