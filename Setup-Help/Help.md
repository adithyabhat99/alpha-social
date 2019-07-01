## install docker-(docker official way)
https://askubuntu.com/questions/938700/how-do-i-install-docker-on-ubuntu-16-04-lts


## nginx(make sure that you don't get error in any step)
``` sudo service apache stop ``` <br />
``` sudo systemctl stop apache ``` (if the above command worked,then no need to execute this command) <br />
``` sudo apt update && sudo apt install nginx ``` <br />
``` cd ~/alpha-social/Setup-Help/nginx ``` <br />
``` sudo mv default /etc/nginx/sites-available/ ``` <br />
``` sudo rm /etc/nginx/sites-enabled/default ``` <br />
``` sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/ ``` <br />
``` sudo systemctl reload nginx.service ``` <br />

## flask

Go to each directory(home-and-discover,post,follow,profile-and-auth) and then -

``` chmod +x start.sh ``` <br />
``` ./start.sh ```


## mysql

``` sudo docker pull mysql/mysql-server:5.6 ```

## Users database

``` 
sudo docker run --detach --name=usersmysql -p 52000:3306 --env="MYSQL_ROOT_PASSWORD=123654654" mysql/mysql-server:5.6 
```
(If the container already exists,then ``` sudo docker start <container-id> ``` )

### To enter into interactive database session
```
sudo docker exec -it usersmysql mysql -uroot -p
```

## Posts database

``` 
sudo docker run --detach --name=postsmysql -p 52100:3306  --env="MYSQL_ROOT_PASSWORD=123654654" mysql/mysql-server:5.6
```
(If the container already exists,then ``` sudo docker start <container-id> ``` )


### To enter into interactive database session

``` sudo docker exec -it postsmysql mysql -uroot -p ```

## In both the databases

``` create user 'root'@'172.17.0.1' identified by 'your_password'; ```

``` GRANT ALL PRIVILEGES ON * . * TO 'root'@'172.17.0.1'; ```



## Docker Cheatsheet-

### To stop a container

``` sudo docker stop <container-id> ```

### To stop all containers

``` sudo docker stop $(sudo docker ps -aq) ```

### To delete an image

``` sudo docker rmi <image-id> -f ```

### To list running containers

``` sudo docker container ls ```
or
``` sudo docker ps ```

### To list all containers

``` sudo docker container ls -a ```


## Cleaning data

### To remove untagged docker images

``` sudo docker images -q --filter "dangling=true" | sudo xargs docker rmi -f ```

### Removing untagged image

**Before running this make sure that both _usermysql_ and _postsmysql_ docker containers are running**

``` sudo docker ps --filter status=dead --filter status=exited -aq   | sudo xargs docker rm -v ```
