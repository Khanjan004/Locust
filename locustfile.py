# import time
import json
import logging
from json import JSONDecodeError
from locust import HttpUser, task, between

class AuthenticateUser(HttpUser):
    timer = between(1, 5)

    @task
    def login_task(self):
        with self.client.post("login/", json={"username":"testuser", "email":"test@test.com", "password":"testuser"}) as response:
            print("222222222222222222222222222222222222222222222222222222222222")
            # print(response.status_code)
            content = json.loads(response.content)
            # print(content)
            if response.status_code == 200 and content['access_token'] != None and content['refresh_token'] != None:
                print("------------------------------------------- LOGIN SUCCESSFUL ---------------------------------------------")
                response.success()
            else:
                response.failure("Error")
    
    @task
    def logout_task(self):
        with self.client.post("logout/") as response:
            print("333333333333333333333333333333333333333333333333333333333333")
            # print(response.status_code)
            content = json.loads(response.content)
            # print(content)
            if response.status_code == 200 and content['detail'] == "Successfully logged out.":
                print("------------------------------------------ LOGOUT SUCCESSFUL ---------------------------------------------")
                response.success()
            else:
                response.failure("Error")
    
    @task
    def user_details_task(self):
        with self.client.post("login/", json={"username":"testuser", "email":"test@test.com", "password":"testuser"}) as resp:
            print("444444444444444444444444444444444444444444444444444444444444")
            # print(resp.status_code)
            if resp.status_code == 200:
                with self.client.get("user", json={"username": "testuser"}) as response:
                    # print(response.status_code)
                    content = json.loads(response.content)
                    # print(content)
                    if response.status_code == 200 and content['pk'] != None and content['first_name'] == None and content['last_name'] == None:
                        print("------------------------------------------ USER DETAILS SUCCESSFUL ---------------------------------------------")
                        response.success()
                    else:
                        response.failure("Error")
    # , **{'HTTP_AUTHORIZATION': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # @task
    # def register_task(self):
    #     self.client.get("/register")

    # @task
    # def home_task(self):
    #     self.client.get("/")

    def on_start(self):
        with self.client.post("registration/", data={"username":"testuser", "email":"test@gmail.com", "password1":"testuser", "password2":"testuser"}, catch_response=True) as response:
            print("111111111111111111111111111111111111111111111111111111111111")
            print(response.status_code)
            content = json.loads(response.content)
            print(content)
            
            if response.status_code == 201 and content['access_token'] != None and content['refresh_token'] != None:
                print("------------------------------------------ REGISTRATION SUCCESSFUL ---------------------------------------------")
                response.success()
            else:
                response.failure("Error")
