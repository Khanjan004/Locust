# import time
import json
import random
from faker import Faker
from locust import events
from locust import HttpUser, task, between, constant, SequentialTaskSet

global users
users = []

global usernames
usernames = set()


class AuthenticateUser(SequentialTaskSet):

    @task
    def login_task(self):
        global user_name
        user_name = random.choice(users)
        # print(f"User Name - Login:- {user_name}")
        with self.client.post("login/", json={"username":f"{user_name}", "email":f"{user_name}@test.com", "password":f"{user_name}"}) as response:
            # print("111111111111111111111111111111111111111111111111111111111111")
            # print(response.status_code)
            content = json.loads(response.content)
            # print(content)
            if response.status_code == 200 and content['access_token'] != None and content['refresh_token'] != None:
                print("------------------------------------------- LOGIN SUCCESSFUL ---------------------------------------------")
                response.success()
            else:
                print("------------------------------------------- LOGIN UNSUCCESSFUL ---------------------------------------------")
                print(response.status_code)
                print(response.text)
                response.failure("Error")
    
    @task
    def user_details_task(self):
        with self.client.get("user", json={"username": f"{user_name}"}) as response:
            # print("222222222222222222222222222222222222222222222222222222222222")
            # print(response.status_code)
            content = json.loads(response.content)
            # print(content)
            if response.status_code == 200 and content['pk'] != None and len(content['first_name']) == 0 and len(content['last_name']) == 0:
                print("------------------------------------------ USER DETAILS SUCCESSFUL ---------------------------------------------")
                response.success()
            else:
                print("------------------------------------------ USER DETAILS UNSUCCESSFUL ---------------------------------------------")
                print(response.status_code)
                print(response.text)
                response.failure("Error")
    
    @task
    def logout_task(self):
        with self.client.post("logout/") as response:
            # print(response.status_code)
            content = json.loads(response.content)
            # print(content)
            if response.status_code == 200 and content['detail'] == "Successfully logged out.":
                print("------------------------------------------ LOGOUT SUCCESSFUL ---------------------------------------------")
                response.success()
            else:
                print("------------------------------------------ LOGOUT UNSUCCESSFUL ---------------------------------------------")
                response.failure("Error")
    
    def on_start(self):
        name = random.choice(tuple(usernames))
        # print(f"Name:- {name}")
        usernames.remove(name)
        with self.client.post("registration/", data={"username":f"{name}", "email":f"{name}@gmail.com", "password1":f"{name}", "password2":f"{name}"}, catch_response=True) as response:
            # print("000000000000000000000000000000000000000000000000000000000000")
            # print(response.status_code)
            content = json.loads(response.content)
            # print(content)
            if response.status_code == 201 and content['access_token'] != None and content['refresh_token'] != None:
                print("------------------------------------------ REGISTRATION SUCCESSFUL ---------------------------------------------")
                users.append(name)
                response.success()
            else:
                print("------------------------------------------ REGISTRATION UNSUCCESSFUL ---------------------------------------------")
                print(response.status_code)
                print(response.text)
                response.failure("Error")
    
    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        fake = Faker()
        while len(usernames) < 100:
            first_name = fake.first_name()
            while len(first_name) <= 6:
                first_name = fake.first_name()
            usernames.add(first_name)
        print("A new test is starting")


class MyLoadTest(HttpUser):
    tasks = [AuthenticateUser]
    wait_time = between(1, 3)
    



# class AuthenticateUser(HttpUser):
#     # timer = between(1, 5)

#     @task
#     def login_task(self):
#         with self.client.post("login/", json={"username":"testuser", "email":"test@test.com", "password":"testuser"}) as response:
#             print("222222222222222222222222222222222222222222222222222222222222")
#             # print(response.status_code)
#             content = json.loads(response.content)
#             # print(content)
#             if response.status_code == 200 and content['access_token'] != None and content['refresh_token'] != None:
#                 print("------------------------------------------- LOGIN SUCCESSFUL ---------------------------------------------")
#                 response.success()
#             else:
#                 response.failure("Error")
    
#     @task
#     def logout_task(self):
#         with self.client.post("logout/") as response:
#             print("333333333333333333333333333333333333333333333333333333333333")
#             # print(response.status_code)
#             content = json.loads(response.content)
#             # print(content)
#             if response.status_code == 200 and content['detail'] == "Successfully logged out.":
#                 print("------------------------------------------ LOGOUT SUCCESSFUL ---------------------------------------------")
#                 response.success()
#             else:
#                 response.failure("Error")
    
#     @task
#     def user_details_task(self):
#         with self.client.post("login/", json={"username":"testuser", "email":"test@test.com", "password":"testuser"}) as resp:
#             print("444444444444444444444444444444444444444444444444444444444444")
#             # print(resp.status_code)
#             if resp.status_code == 200:
#                 with self.client.get("user", json={"username": "testuser"}) as response:
#                     # print(response.status_code)
#                     content = json.loads(response.content)
#                     # print(content)
#                     if response.status_code == 200 and content['pk'] != None and content['first_name'] == None and content['last_name'] == None:
#                         print("------------------------------------------ USER DETAILS SUCCESSFUL ---------------------------------------------")
#                         response.success()
#                     else:
#                         response.failure("Error")
#     # , **{'HTTP_AUTHORIZATION': f'Bearer {token}', 'Content-Type': 'application/json'}
    
#     # @task
#     # def register_task(self):
#     #     self.client.get("/register")

#     # @task
#     # def home_task(self):
#     #     self.client.get("/")

#     def on_start(self):
#         with self.client.post("registration/", data={"username":"testuser", "email":"test@gmail.com", "password1":"testuser", "password2":"testuser"}, catch_response=True) as response:
#             print("111111111111111111111111111111111111111111111111111111111111")
#             print(response.status_code)
#             content = json.loads(response.content)
#             print(content)
            
#             if response.status_code == 201 and content['access_token'] != None and content['refresh_token'] != None:
#                 print("------------------------------------------ REGISTRATION SUCCESSFUL ---------------------------------------------")
#                 response.success()
#             else:
#                 response.failure("Error")
