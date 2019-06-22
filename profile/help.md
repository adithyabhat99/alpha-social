
Sample sql insert query for create user-

insert into users.user(userid,username,firstname,lastname,password,email,phoneno,token,phonetoken,public,datecreated,dateupdated,profilepic,bio) 
values('uuid','username','first','last','pw','mail','phone','tok','phonet','1','2019-06-20 10:30:12','2019-06-20 10:30:12','null','hi');    

Test createuser(You can also use postman)-
adi-
curl -H "Content-Type: pplication/json" -POST -d '{"username":"adi","password":"123","firstname":"a","lastname":"b","email":"adithyabhat99@gmail.com"}' http://localhost:7700/api/v1.0/createuser

adithya-
curl -H "Content-Type: pplication/json" -POST -d '{"username":"adithya","password":"123","firstname":"a","lastname":"b","email":"adithyabhatoct99@gmail.com"}' http://localhost:7700/api/v1.0/createuser

To test login use postman basic auth
The login token returned by server will be like this-
adi-
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiIyZTExODg0ZC0zOTRkLTRlYjgtODNkNy05YjQ2YjYxMDhkOTIiLCJ1c2VybmFtZSI6ImFkaSIsImV4cCI6MTU2MTc4Njc5N30.8lCN8BCVeNKkzcXGFCToy6fHMbhM7I--oH7gIzpsDXI"
}

adithya-
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiIzYWE1MmRlMS02ODI1LTQ0NDktODJhMy04MGE1MTZmOTIzMGEiLCJ1c2VybmFtZSI6ImFkaXRoeWEiLCJleHAiOjE1NjE3ODY3NjV9.D7SfC-V2EjN4dh2TQ70Hi6866XSxyyWEsx8zIuJhCO4"
}
adi123
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiIwZGI0M2ZhNC1iMDYzLTRkMjctODkzMC1hYzRkYjE0ZmU4OTIiLCJ1c2VybmFtZSI6ImFkaTEyMyIsImV4cCI6MTU2MTgxMzg0Nn0.ukthf0tiC2j_FjgfVrf1MHji0WWJ-NQ5B2UcepMELcY"
}

To test all api endpoints, use postman