Django App Practice


Backend Creation

1. Started off with command: django-admin startproject backend
    - seems like this will be a seperate django section for the backend exclusively
2. Next, changed dir into backend folder, then created a new api 'app' with command: python manage.py startapp api     
    - this will be section for api related stuff exclusively
    - what will backend folder be used for?
        - The backend folder is like a central hub for the backend. Mainly for settings, urls, and the manage.py file which is
          an entry point to execute commands.
3. Went into backend folder, then settings.py file. Made the following changes:
    a. import os
       from datetime import timedelta
    b. from dotenv import load_dotenv
        - Apparently this is for credential in db
    c. load_dotenv()
        - Calling the function that was imported
    d. Inside the 'ALLOWED_HOSTS' list, put '*'
        - This will allow any different host to host the app
    e. Pasted the following code:
        `REST_FRAMEWORK = {
            "DEFAULT_AUTHENTICATION_CLASSES": (
                "rest_framework_simplejwt.authentication.JWTAuthentication",
            ),
            "DEFAULT_PERMISSION_CLASSES": [
                "rest_framework.permissions.IsAuthenticated",
            ],
            }
            
            SIMPLE_JWT = {
                "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
                "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
            }`
        - Specifying default authentication and permission classes. Will need these when working with JWT tokens. What does this mean?
            - JWT = JSON Web Tokens
            - When a user logs in, they receive an access token AND a refresh token
                - **Access token** is short lived - used for secure communication with the api
                - **Refresh token** is used to refresh the active token without logging in again
4. Went into 'INSTALLED APPS' list and added the following:
    a. api
        - because this is the app we just started
    b. rest_framework
        - will be used for the frontend
    c. corsheaders
        - What is this used for? Something to do with the frontend..
            - CORS = Cross-Origin Resource Sharing
            - This is a security feature that is enforced by browsers
            - It determines whether resources (like API data) can be accessed by a frontend app, hosted on a different domain than the backend
                - Generally the front and backends are on different domains because the front end is react - the backend is django 
                  i.e. they can scale/develop independently
            - Without cors, the browser couldn't fetch data from the backend
5. Went into 'MIDDLEWARE' list and added:
    a. corsheaders.middleware.CorsMiddleware
        - What is middleware?
            - Processes requests and responses before or after they reach the view
            - For example, security checks, authenticating data, modifying data ect.
            - Similar to the models page but models is more for DB stuff whereas middleware handles requests and responses
                - For example, during login, it might check whether user is already logged in i.e. is the request valid
6. Added to the bottom of settings file:
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWS_CREDENTIALS = True
    - Can change this later to make things more secure. Good for now for development.
    - How to make it more secure later?
    
Dealing with JWT Tokens
Interaction between the front end and backend
Front end stores access and refresh token - using them for each backend call
If access token expires - the refresh token will submit a request to get a new access token

Granting an Access token
First need a User
Before a User - Since we are using the User module in Django - We need a serializer in order to exchange Python data and JSON
1. Created the following file in the api app folder: serializers.py
    
    from django.contrib.auth.models import User
    from rest_framework import serializers


    class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ["id", "username", "password"]
        extra_kqargs = {"password": {"write_only": True}}

    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)
        
        return user

    - Using djangos user functionality and rest serializer functionality
2. In views, started views.py adjustments in order to create a user - because still needed a path to create a user

    from django.shortcuts import render
    from django.contrib.auth.models import User
    from rest_framework import generics
    from .serializers import UserSerializer
    from rest_framework.permissions import IsAuthenticated, AllowAny
    
    
    class CreateUserView(generics.CreateAPIView):
    
        queryset = User.objects.all()
        serializer_class = User
        permission_classes = [AllowAny]

3. Configured urls.py in backend dir
    
    from django.contrib import admin
    from django.urls import path, include
    from api.views import CreateUserView
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/user/register/', CreateUserView.as_view(), name="register"),
        path('api/token/', TokenObtainPairView.as_view(), name="get_token"),
        path('api/token/refresh/', TokenRefreshView.as_view(), name="refresh"),
        path('api-auth/', include("rest_framework.urls"))
    ]
   
4. Made migrations in DB with following code:
    a. python manage.py makemigrations
    b. python manage.py migrate
5. Run server
    a. python manage.py runserver
    


