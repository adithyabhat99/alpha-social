# alpha-social
- This is a social media website which is accessible through the rest api 
- It is divided into multiple microservices 
- Profile service will have api to create account,changing details (like email,phonenumber,name etc.)  of user, uploading or deleting profile picture, etc.
- Profile service also serves as authentication server,on sending username and password it returns a JWT token which can be saved as a cookie and sent with every other request
- OAuth server can be used by third party websites to authenticate users using alpha social
- Follow service has features like follow any user,approve follow requests,get user details etc.
- Posts service to post images,like,comment,delete post,get post and many other features
- Home and search gives a user's home page contents,trending public posts,latest public posts etc.
- [Browser client](https://github.com/adithyabhat99/alpha-social-client) 

![Architecture](https://user-images.githubusercontent.com/30742449/60392061-ac607100-9b19-11e9-9fb6-02a6a43cfbae.jpg)


## Technologies used
- Python Flask
- AWS S3 for file storage
- MySQL database
- Docker for dependency management and virtualization

## Future work
- Notifications,emails,SMS etc.
- Messaging service 


# License

### [LICENSE](./LICENSE)
