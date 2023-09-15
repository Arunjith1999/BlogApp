from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import random, re
from .serializer import *
from rest_framework import status
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, authenticate
import jwt
# Create your views here.

@api_view(['POST'])
def loginuser(request):                             # login user 
    try:                                            # try except is used to handle excepted errors
        email = request.data['email']
        password = request.data['password']
    except:
        return Response({'status':'incorrect'})
    
    try:

        user = Customuser.objects.get(email = email) # check if the user exists
        if check_password(password, user.password):  # checking the plain text password with hashed password
            name = user.username
            payload = {                              # setting payload for jwt token
                        'email' : user.email,
                        'password' : user.password,
            }
            user_id = user.id 
            message = f'Hey {name} Welcome to AuthorArena'
            jwt_token = jwt.encode(payload, 'secret', algorithm= 'HS256')  # creating jwt token on successfull login
            return Response ({'status':'true', 'jwt_token':jwt_token, 'user_id':user_id,'message':message}) # returning status of the response with jwt token
        else:
            return Response({'status':'incorrect password'}) # returning response if the user is invalid
    except Customuser.DoesNotExist:
        return Response({'status':'Incorrect '})

@api_view(['POST'])
def signup_user(request):  # signup for users
    try:
        username = request.data['username']
        email  = request.data['email']
        raw_password = request.data['password']
        error_message = ''
        if not is_valid_email(email):      # check if the user entered a valid email using is_valid_mail function
            error_message += 'Not a valid email '
            return Response({'error':error_message}) # if the email is invalid return response

        email_exist = Customuser.objects.filter(email = email).exists() # check if the email already exists , emails must be unique
        if email_exist:
            error_message += 'Email already taken '
            return Response({'error':error_message})
        username_exist = Customuser.objects.filter(username = username).exists() # checks if username is unique 
        if username_exist:
            error_message += 'Username already taken'
            return Response({'error': error_message})
        else:
            hashed_password = make_password(raw_password) # hashing the password before storing in database

            user = Customuser.objects.create(username = username, # creating a user 
                                       email = email,
                                       password = hashed_password)
            
            user.save()                                             # saving user on databse
            return Response({'status':'Success'}, status=status.HTTP_201_CREATED) # returning with Response 201
        
    except Exception as e:
        print(e)
        return Response({'error': 'An Error Occured'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def suggest_password(request):                       # suggesting password for users
    try:
        uppercase_letters =   'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        lowercase_letters =    uppercase_letters.lower()
        digits            =    '0123456789'
        symbols           =    '[]{}()$?#<>'

        upper, lower, nums, syms = True, True, True, True
        
        all = ''

        if upper:
            all += uppercase_letters
        
        if lower:
            all += lowercase_letters

        if nums:
            all += digits

        if syms:
            all += symbols

        length = 8
        amount = 1

        for x in range(amount):
            password = ''.join(random.sample(all, length)) #creating a random password for users

        return Response({'password': password})
    
    except Exception as e:
      
      return Response({'status': 'An error Occured'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def user_home(request):
    pass

def is_valid_email(email):                     # regex to check if the email is a valid one
    pattern = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern,email)is not None


@api_view(['POST'])
def create_blog(request, id):                           # creating a  new blog
    try:                                                # try except to handle possible errors
        title = request.data['title']
        content = request.data['content']
        user_id = id

        blog = Blog.objects.create(title = title,       # creating a new Blog 
                                   content = content,
                                   user_id = user_id)
        blog.save()                                     #save the blog
        return Response({'status':'Success'}, status= status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response({'status':'internal error Occured'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def view_blogs(request):
    blogs = Blog.objects.all().order_by('-created_at')
    serializer = BlogSerializer(blogs, many=True)                            # Serialize the blogs to convert to JSON format
    return Response(serializer.data)                                         # passing the data to frontend

@api_view(['POST'])                                                          #post comments for blogs
def post_comments(request, id, user_id):
   
    try:                                                                     #try-except to handle possible errors
        content = request.data['comment']
        comment = Comment.objects.create(content = content,                  #creating a new comment
                                         user_id = user_id,
                                         blog_id = id)
        comment.save()                                                       #saving the comments in database
        return Response({'status':'Success'}, status= status.HTTP_201_CREATED)
    except Exception as e:
         return Response({'status':'internal error Occured'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_comment(request, id):                                               #viewing the comments on Blogs
    try:        
        blog = Blog.objects.get(id = id)                                    
        comments = Comment.objects.filter(blog = blog)
        serializer = CommentSerializer(comments, many =True)                #serilaizing the data to JSON formats
        return Response(serializer.data)                                    #returning to frontend
    except Comment.DoesNotExist:
        return Response({'status':'no comments'})
    
@api_view(['GET'])                                                          #view users blogs
def my_blogs(request, id):
    try:
        user = Customuser.objects.get(id = id)
        blog = Blog.objects.filter(user = user)                             #filtering the blogs of user
        count = blog.count()                                                #counting the  number of blogs
        serializer = BlogSerializer(blog, many = True)                      #converting to JSON format
        data = {
            'count': count,                                                 #dict 'data' to pass values to frontend
            'blogs': serializer.data,
        }
        return Response(data)
    except Blog.DoesNotExist:
        return Response({'status':'no blogs'})
  
@api_view(['PATCH'])                                                        #editing the blog
def edit_blog(request, id):
    try:
        blog = Blog.objects.get(id = id)
        title = request.data['title']
        content = request.data['content']                      
        blog.title = title                                                   #assigning new value to old value
        blog.content = content 
        blog.save()                                                          #saving the blog with updations in database
        return Response({'status':'Success'})

    except Blog.DoesNotExist:
        return Response({'error'}, 'Blog does not exist')
    
@api_view(['DELETE']) 
def delete_blog(request, id):                                                #deleting the blog
    try: 
        blog = Blog.objects.get(id = id)                                     # get the particular Blog for deleting
        blog.delete()                                                        #deleted
        return Response({'status':'Success'})
    except Blog.DoesNotExist:
        return Response({'status':'Blog does not exist'})

@api_view(['GET'])                           
def get_user(request, id):                                                   # get the userDetails
    try:
        user = Customuser.objects.get(id = id)
        serializer = UserSerializer(user, many = False)                      #serialaize the data to JSON format
        return Response(serializer.data)
    except Customuser.DoesNotExist:
        return Response({'status':'user does not exist'})


