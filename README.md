# alpha-social
- This is a social media website which is accessible through the rest api 
- It is divided into multiple microservices 
- Profile service will have api to create account,changing details (like email,phonenumber,name etc.)  of user, uploading or deleting profile picture, etc.
- Profile service also serves as authentication server,on sending username and password it returns a jwt Auth token which can be saved as a cookie and sent with every other request
- Follow service has features like follow any user,approve follow requests,get user details etc.
- Posts service to post images,like,comment,delete post,get post and many other features
- Home and search gives a user's home page contents,trending public posts,latest public posts etc.

## Technologies used
- Flask api 
- MySQL database 
- Used docker to manage services 

# Future work
- Front end client
- Reverse proxy server
- Event driven services like notifications,emails,SMS etc.
- Messaging service 

# Documentation and LICENCE

[ API Documentation ](DOCUMENTATION.md)

## Any help is appreciated!