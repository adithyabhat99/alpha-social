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


Cleaning data-

sudo apt-get clean

dpkg -l 'linux-*' | sed '/^ii/!d;/'"$(uname -r | sed "s/\(.*\)-\([^0-9]\+\)/\1/")"'/d;s/^[^ ]* [^ ]* \([^ ]*\).*/\1/;/[0-9]/!d' | xargs sudo apt-get -y purge
 
sudo docker ps --filter status=dead --filter status=exited -aq   | sudo xargs docker rm -v