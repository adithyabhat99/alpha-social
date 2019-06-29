## All urls start with /api/v1.0/

**For testing, recommended to use _postman_**

### /createaccount

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

### /login

- POST method
- Authorization form-username and email
- A 'x-access-token' will be sent,for all other features,this token is compulsory in header

## All the following requests must have 'x-access-token' and corresponding auth token in header

### /update/profilepic

- POST method
- "file" and attach corresponding file as form data

### /update/username

- POST method
- Header: Content-Type:application/json
- "new_username" should be sent as raw json

### /update/email

- POST method
- Header: Content-Type:application/json
- "new_email" should be sent as raw json

### /update/phoneno

- POST method
- Header: Content-Type:application/json
- "new_phoneno" should be sent as raw json

### /update/name

- POST method
- Header: Content-Type:application/json
- "new_firstname" and "new_lastname" should be sent as raw json

### /update/bio

- POST method
- Header: Content-Type:application/json
- "new_bio" should be sent as raw json

### /getmydetails

- GET method to get details of the user

### /getmyprofilepic

- GET method to get profile picture of the user

### /deleteprofilepic

- DELETE method to delete profile picture of the user

### /getdetails

- GET method
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/getdetails?userid2=absd-sdsd-sdds-werr
```

### /getprofilepic

- GET method
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/getprofilepic?userid2=absd-sdsd-sdds-werr
```

### /getusername

- GET method
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/getusername?userid2=absd-sdsd-sdds-werr
```

### /getuserid

- GET method
- Send 'username' as argument
- Example
```
http://url/api/v1.0/getuserid?username=adithya
```

### /follow/user

- GET method
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/follow/user?userid2=absd-sdsd-sdds-werr
```

### /getrequestlist

- GET method to get follow request list
- Example
```
http://url/api/v1.0/getrequestlist
```

### /approve

- GET method to approve follow request
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/approve?userid2=absd-sdsd-sdds-werr
```

### /getfollowerslist

- GET method to get followers list
- Send 'num' as argument,by default it is 0
- num=0 for first 20 followers num=1 for 20-40 and so on..
- Example
```
http://url/api/v1.0/getfollowerslist?num=0
```

### /getfollowinglist

- GET method to get following list
- 'num' not required as following list will be usually small
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/getfollowinglist
```

### /unfollow

- GET method to unfollow user
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/unfollow?userid2=absd-sdsd-sdds-werr
```

### /disapprove

- GET method to disapprove follow request
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/disapprove?userid2=absd-sdsd-sdds-werr
```


### /removefollower

- GET method to remove follower
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/removefollower?userid2=absd-sdsd-sdds-werr
```

### /muteuser

- GET method to mute user
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/muteuser?userid2=absd-sdsd-sdds-werr
```

### /reportuser

- GET method to report a user
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/reportuser?userid2=absd-sdsd-sdds-werr
```

### /post

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

### /delete/post

- DELETE method to delete post
- Send 'postid' as argument
- Example
```
http://url/api/v1.0/delete/post?postid=absd-sdsd-sdds-werr
```

### /update/post

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

## To view a post,like,comment etc. the requesting user must be following the other user 

### /like/post

- GET method to like a post
- Send 'postid' as argument
- Example
```
http://url/api/v1.0/like/post?postid=absd-sdsd-sdds-werr
```

### /comment/post

- POST method to comment on a post
- Send 'postid' as argument
- Header:Content-Type:application/json
- Send {"comment":"your message"} as raw json
- Example
```
http://url/api/v1.0/comment/post?postid=absd-sdsd-sdds-werr
```

### /delete/like

- DELETE method to delete a like
- Send 'postsid' as argument
- Example
```
http://url/api/v1.0/delete/like?postid=absd-sdsd-sdds-werr
```

### /delete/comment

- DELETE method to delete a comment
- Send 'commentid' as argument
- Example
```
http://url/api/v1.0/delete/comment?commentid=absd-sdsd-sdds-werr
```

### /getpostsfor/user

- GET method to get list of posts for a user
- Send 'userid2' as argument
- Example
```
http://url/api/v1.0/getpostsfor/user?userid=absd-sdsd-sdds-werr
```

### /getpost

- GET method to get a post(image file)
- Send 'postid' as argument
- Example
```
http://url/api/v1.0/getpost?postid=absd-sdsd-sdds-werr
```

### /getcommentslist

- GET method to get list of comments for a post
- Send 'postid' as argument
- Send 'num' as argument,by default it is 0
- num=0 for first 20 comments num=1 for 20-40 and so on..
- Example
```
http://url/api/v1.0/getcommentslist?postid=absd-sdsd-sdds-werr&num=0
```

### /getlikeslist

- GET method to get list of likes for a post
- Send 'postid' as argument
- Send 'num' as argument,by default it is 0
- num=0 for first 20 likes num=1 for 20-40 and so on..
- Example
```
http://url/api/v1.0/getlikeslist?postid=absd-sdsd-sdds-werr&num=0
```

### /gethome

- GET method to get list of home page posts for the user
- Send 'num' as argument,by default it is 0
- num=0 for first 20 posts num=1 for 20-40 and so on..
- Example
```
http://url/api/v1.0/gethome?num=0
```

### /discover/latest

- GET method to get list of latest public posts for the day
- Send 'num' as argument,by default it is 0
- num=0 for first 20 posts num=1 for 20-40 and so on..
- Example
```
http://url/api/v1.0/discover/latest?num=0
```

### /discover/trending

- GET method to get list of trending public posts by likes for the day
- Send 'num' as argument,by default it is 0
- num=0 for first 20 posts num=1 for 20-40 and so on..
- Example
```
http://url/api/v1.0/discover/trending?num=0
```

### /search

- GET method to search a user by username or name
- Either 'firstname' and 'lastname' must be sent as argument
- Send 'num' as argument,by default it is 0
- num=0 for first 20 users num=1 for 20-40 and so on..
- to search based on username,there is already a method called "/getuserid" (here username is unique,so multiple people with same username is not possible)


## Following DOES NOT REQUIRE auth token in header

### /followsornot

- GET method to verify whether a user follows other user or not
- 'userid1' and 'userid2' must be sent as arguments
- Example
```
http://url/followsornot?userid1=qwer-rewq-tyui-iuyt&userid2=zxcv-vcxz-mnbv-vbnm
```