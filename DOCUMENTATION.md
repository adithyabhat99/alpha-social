## All urls start with /api/v1.0/

**For testing, recommended to use _postman_**

### /a/createaccount

- POST method
- 'username','password','email' or 'phoneno','firstname','lastname' should be compulsorily sent
- 'bio','public' are optional(By default 'public'=0, i.e account is private)
- All the details in JSON format
- Header: Content-Type:application/json
- Example
```
{
    "username":"adithya",
    "password":"123",
    "firstname":"a",
    "lastname":"b",
    "email":"adithyabhatoct@gmail.com"
}
```

### /a/login

- POST method
- Authorization form-username and email
- A 'x-access-token' will be sent,for all other features,this token is compulsory in header

## All the following requests must have 'x-access-token' and corresponding auth token in header

### /h/gethome

- GET method to get list of home page posts for the user
- Send 'num' as argument,by default it is 0
- num=0 for first 20 posts num=1 for 20-40 and so on..
- Example
```
http://url/api/v1.0/h/gethome?num=0
```

### /h/discover/latest

- GET method to get list of latest public posts for the day
- Send 'num' as argument,by default it is 0
- num=0 for first 20 posts num=1 for 20-40 and so on..
- Example
```
http://url/api/v1.0/h/discover/latest?num=0
```

### /h/discover/trending

- GET method to get list of trending public posts by likes for the day
- Send 'num' as argument,by default it is 0
- num=0 for first 20 posts num=1 for 20-40 and so on..
- Example
```
http://url/api/v1.0/h/discover/trending?num=0
```

### /f/suggestions/users

- GET method to get follow suggestions
- Send 'num' as argument,by default it is 0
- num=0 for first 20 users num=1 for 20-40 and so on..
- Example
```
http://url/api/v1.0/f/suggestions/users?num=0
```

### /a/search

- GET method to search a user by username or name
- Either 'firstname' and 'lastname' must be sent as argument
- Send 'num' as argument,by default it is 0
- num=0 for first 20 users num=1 for 20-40 and so on..
- to search based on username,there is already a method called "/getuserid" (here username is unique,so multiple people with same username is not possible)

### /a/getuserid

- GET method
- Send 'username' as argument
- Example
```
http://url/api/v1.0/a/getuserid?username=adithya
```

### /a/update/profilepic

- PUT method
- "file" and attach corresponding file as form data

### /a/update/username

- PUT method
- Header: Content-Type:application/json
- "new_username" should be sent as raw json

### /a/update/email

- PUT method
- Header: Content-Type:application/json
- "new_email" should be sent as raw json

### /a/update/phoneno

- PUT method
- Header: Content-Type:application/json
- "new_phoneno" should be sent as raw json

### /a/update/name

- PUT method
- Header: Content-Type:application/json
- "new_firstname" and "new_lastname" should be sent as raw json

### /a/update/bio

- PUT method
- Header: Content-Type:application/json
- "new_bio" should be sent as raw json

### /a/getmydetails

- GET method to get details of the user

### /a/getmyprofilepic

- GET method to get profile picture of the user

### /a/deleteprofilepic

- DELETE method to delete profile picture of the user

### /a/getdetails

- GET method
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/a/getdetails?userid2=absd-sdsd-sdds-werr
```

### /a/getprofilepic

- GET method
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/a/getprofilepic?userid2=absd-sdsd-sdds-werr
```

### /a/getusername

- GET method
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/a/getusername?userid2=absd-sdsd-sdds-werr
```

### /f/follow/user

- PUT method
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/f/follow/user?userid2=absd-sdsd-sdds-werr
```

### /f/getrequestlist

- GET method to get follow request list
- Example
```
http://url/api/v1.0/f/getrequestlist
```

### /f/approve

- PUT method to approve follow request
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/f/approve?userid2=absd-sdsd-sdds-werr
```

### /f/getfollowerslist

- GET method to get followers list
- Send 'num' as argument,by default it is 0
- num=0 for first 20 followers num=1 for 20-40 and so on..
- Example
```
http://url/api/v1.0/f/getfollowerslist?num=0
```

### /f/getfollowinglist

- GET method to get following list
- 'num' not required as following list will be usually small
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/f/getfollowinglist
```

### /f/unfollow

- DELETE method to unfollow user
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/f/unfollow?userid2=absd-sdsd-sdds-werr
```

### /f/disapprove

- DELETE method to disapprove follow request
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/f/disapprove?userid2=absd-sdsd-sdds-werr
```

### /f/removefollower

- DELETE method to remove follower
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/f/removefollower?userid2=absd-sdsd-sdds-werr
```

### /f/muteuser

- PUT method to mute user
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/f/muteuser?userid2=absd-sdsd-sdds-werr
```

### /f/reportuser

- POST method to report a user
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/f/reportuser?userid2=absd-sdsd-sdds-werr
```

### /p/post

- POST method to post image
- Header: Content-Type:mutipart/form-data
- "file" in form-attach image in PNG/JPG format
- Example
- "details" in form
```
{
    "location":"puttur",
    "caption":"hey!",
    "public":"0"
}
```

### /p/delete/post

- DELETE method to delete post
- Send 'postid' as argument
- Example
```
http://url/api/v1.0/p/delete/post?postid=absd-sdsd-sdds-werr
```

### /p/update/post

- PUT method to post image
- Header: Content-Type:mutipart/form-data
- "file" in form-attach image in PNG/JPG format
- Example
- "details" in form
```
{
    "location":"puttur",
    "caption":"hey!",
    "public":"0"
}
```

## To view a post,like,comment etc. the requesting user must be following the other user 

### /p/like/post

- PUT method to like a post
- Send 'postid' as argument
- Example
```
http://url/api/v1.0/p/like/post?postid=absd-sdsd-sdds-werr
```

### /p/comment/post

- POST method to comment on a post
- Send 'postid' as argument
- Header:Content-Type:application/json
- Send {"comment":"your message"} as raw json
- Example
```
http://url/api/v1.0/p/comment/post?postid=absd-sdsd-sdds-werr
```

### /p/delete/like

- DELETE method to delete a like
- Send 'postsid' as argument
- Example
```
http://url/api/v1.0/p/delete/like?postid=absd-sdsd-sdds-werr
```

### /p/delete/comment

- DELETE method to delete a comment
- Send 'commentid' as argument
- Example
```
http://url/api/v1.0/p/delete/comment?commentid=absd-sdsd-sdds-werr
```

### /p/getpostsfor/user

- GET method to get list of posts for a user
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/p/getpostsfor/user?userid=absd-sdsd-sdds-werr
```

### /p/getpost

- GET method to get a post(image file)
- Send 'postid' as argument
- Example
```
http://url/api/v1.0/p/getpost?postid=absd-sdsd-sdds-werr
```

### /p/getcommentslist

- GET method to get list of comments for a post
- Send 'postid' as argument
- Send 'num' as argument,by default it is 0
- num=0 for first 20 comments num=1 for 20-40 and so on..
- Example
```
http://url/api/v1.0/p/getcommentslist?postid=absd-sdsd-sdds-werr&num=0
```

### /p/getlikeslist

- GET method to get list of likes for a post
- Send 'postid' as argument
- Send 'num' as argument,by default it is 0
- num=0 for first 20 likes num=1 for 20-40 and so on..
- Example
```
http://url/api/v1.0/p/getlikeslist?postid=absd-sdsd-sdds-werr&num=0
```

### /a/deletemyaccount

- DELETE request to delete account
- All details and posts of the user will be deleted

## Following DOES NOT REQUIRE auth token in header

### /f/followsornot

- GET method to verify whether a user follows other user or not
- 'userid1' and 'userid2' must be sent as arguments
- Example
```
http://url/f/followsornot?userid1=qwer-rewq-tyui-iuyt&userid2=zxcv-vcxz-mnbv-vbnm
```