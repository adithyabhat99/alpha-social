# alpha-social
- This is a social media website which is accessible through the rest api 
- It is divided into multiple microservices 
- Profile service will have api to create account,changing details of user, uploading profile picture etc.
- Profile service also serves as authentication server,on sending username and password it returns a jwt token which can be saved as a cookie and sent with every other request
- Follow service has features like follow any user,approve follow requests,get user details,and other internal apis
- Posts service to post images,like,comment,delete post,get post and many other features
- Flask api 
- MySQL database 
- Used docker to manage services 

# Future work
- Home page service to fetch a user's custom home page contents 
- Front end client
- Reverse proxy server
- Event driven services like notifications,emails,SMS etc.
 (These will be secure internal APIs)
- Discover service fetching trending public posts 
- Messaging service 

## Any help is appreciated!
