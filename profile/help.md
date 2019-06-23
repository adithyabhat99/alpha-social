
Sample sql insert query for create user-

insert into users.user(userid,username,firstname,lastname,password,email,phoneno,token,phonetoken,public,datecreated,dateupdated,profilepic,bio) 
values('uuid','username','first','last','pw','mail','phone','tok','phonet','1','2019-06-20 10:30:12','2019-06-20 10:30:12','null','hi');    

Test createuser(You can also use postman)-
adi123-
curl -H "Content-Type:application/json" -POST -d '{"username":"adi123","password":"123","firstname":"a","lastname":"b","email":"adithyabhat@gmail.com"}' http://localhost:7700/api/v1.0/createaccount

userid-d091f992-503d-4644-b559-f7370deff964

login token-
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiJkMDkxZjk5Mi01MDNkLTQ2NDQtYjU1OS1mNzM3MGRlZmY5NjQiLCJ1c2VybmFtZSI6ImFkaTEyMyIsImV4cCI6MTU2MTkwNTE2N30.ZfWNa5nhv9A-_S42Pe9BiAVL3eYiGW5t4FuboLuy9YY"
}

adithya-3da180c6-71ee-4f14-88f5-1019bd8e55f6

curl -H "Content-Type:application/json" -POST -d '{"username":"adithya","password":"123","firstname":"a","lastname":"b","email":"adithyabhatoct@gmail.com"}' http://localhost:7700/api/v1.0/createaccount

userid-d8e16d42-090f-4bbc-93ff-d76ab23a3a2d

login token-
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiIzZGExODBjNi03MWVlLTRmMTQtODhmNS0xMDE5YmQ4ZTU1ZjYiLCJ1c2VybmFtZSI6ImFkaXRoeWEiLCJleHAiOjE1NjE5MDUyMTJ9.aZVgcQctJ9oN7-2_X5X23y7dCOfThnAYDqSSn5Xf1bw"
}

adi-
curl -H "Content-Type:application/json" -POST -d '{"username":"adi","password":"123","firstname":"a","lastname":"b","email":"adithyabhat99@gmail.com"}' http://localhost:7700/api/v1.0/createaccount

userid-3da180c6-71ee-4f14-88f5-1019bd8e55f6

login token-
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiJkOGUxNmQ0Mi0wOTBmLTRiYmMtOTNmZi1kNzZhYjIzYTNhMmQiLCJ1c2VybmFtZSI6ImFkaSIsImV4cCI6MTU2MTkwNTIzMn0.rqEQkpAgjJ5rlDVzixqX3D7dcfIY620yH42LQptb30E"
}


To test login use postman basic auth
The login token returned by server will be like this-


To test all api endpoints, use postman