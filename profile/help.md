
Sample sql insert query for create user-

insert into users.user(userid,username,firstname,lastname,password,email,phoneno,token,phonetoken,public,datecreated,dateupdated,profilepic,bio) 
values('uuid','username','first','last','pw','mail','phone','tok','phonet','1','2019-06-20 10:30:12','2019-06-20 10:30:12','null','hi');    

Test createuser(You can also use postman)-
adi123-
curl -H "Content-Type:application/json" -POST -d '{"username":"adi123","password":"123","firstname":"a","lastname":"b","email":"adithyabhat@gmail.com"}' http://localhost:7700/api/v1.0/createaccount

userid-d091f992-503d-4644-b559-f7370deff964

login token-
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiJkMDkxZjk5Mi01MDNkLTQ2NDQtYjU1OS1mNzM3MGRlZmY5NjQiLCJ1c2VybmFtZSI6ImFkaTEyMyIsImV4cCI6MTU2MjE1MjAyNX0.jsTCfA74c04meB0l1wDajIzQPP4c-guCL1GrOOpMpRk"
}

adithya-

curl -H "Content-Type:application/json" -POST -d '{"username":"adithya","password":"123","firstname":"a","lastname":"b","email":"adithyabhatoct@gmail.com"}' http://localhost:7700/api/v1.0/createaccount

userid-3da180c6-71ee-4f14-88f5-1019bd8e55f6

login token-
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiIzZGExODBjNi03MWVlLTRmMTQtODhmNS0xMDE5YmQ4ZTU1ZjYiLCJ1c2VybmFtZSI6ImFkaXRoeWEiLCJleHAiOjE1NjIxNTIwMDB9.dCoauzWvFN1G8n4LNRbLdhKZszbW2paocYaM0hU0nNE"
}

adi-
curl -H "Content-Type:application/json" -POST -d '{"username":"adi","password":"123","firstname":"a","lastname":"b","email":"adithyabhat99@gmail.com"}' http://localhost:7700/api/v1.0/createaccount

userid-d8e16d42-090f-4bbc-93ff-d76ab23a3a2d

login token-
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiJkOGUxNmQ0Mi0wOTBmLTRiYmMtOTNmZi1kNzZhYjIzYTNhMmQiLCJ1c2VybmFtZSI6ImFkaSIsImV4cCI6MTU2MjE1MTk1M30.edezb2yFBCnUcr4x4GVcU8lhN0aezlCiFy4TPNMWBZw"
}


To test login use postman basic auth
The login token returned by server will be like this-


To test all api endpoints, use postman


adithya follows adi123