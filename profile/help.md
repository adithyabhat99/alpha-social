
Sample sql insert query for create user-

insert into users.user(userid,username,firstname,lastname,password,email,phoneno,token,phonetoken,public,datecreated,dateupdated,profilepic,bio) 
values('uuid','username','first','last','pw','mail','phone','tok','phonet','1','2019-06-20 10:30:12','2019-06-20 10:30:12','null','hi');    

Test createuser(You can also use postman)-

curl -H "Content-Type: pplication/json" -POST -d '{"username":"adi","password":"123","firstname":"a","lastname":"b","email":"di"}' http://localhost:7700/api/v1.0/createuser

To test login use postman basic auth
The login token returned by server will be like this-
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiI3NTRkNDRlMy0xYTM1LTRmNzktOTA0NS1kZTY2M2NiOGYyM2QiLCJ1c2VybmFtZSI6ImFkaSIsImV4cCI6MTU2MTcwNzg2MH0.lgM17S_KoPzxlmNu82zCbNRuNdCnaR32YL7f_GvfsGA"
}