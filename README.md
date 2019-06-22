# alpha-social
- This is a social media website which is accessible through the rest api 
- It is divided into multiple microservices 
- Profile service will have api to create account,changing details of user, uploading profile picture etc. This service is still in development 
- Profile service also serves as authentication server,on sending username and password it returns a jwt token which can be saved as a cookie and sent with every other request
- Follow service has features like follow any user,approve follow requests,get user details,and other internal apis
- Flask api 
- MySQL database 
- Used docker to manage services 

# Future work
- Posts service to post images 
- Home page service to fetch a user's custom home page contents 
- Front end client
- Reverse proxy server
- Discover service fetching trending public posts 
- Messaging service 

## Any help is appreciated!
