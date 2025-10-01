# from django.db import models

# # Create your models here.
# from django.db import models
# import re
# import bcrypt

# # Create your models here.
# class usersManager(models.Manager):
#     def user_validator(self,postData):
#         errors={}
#         EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')

#         if not postData['first_name']:
#             errors['first_name_empty']='First Name is Empty'
#         else:
#             if len(postData['first_name'])<2:
#                 errors['first_name_len']='First Name must be more than 2 characters'

#         if not postData['last_name']:
#             errors['last_name_empty']='Last Name is Empty'
#         else:
#             if len(postData['last_name'])<2:
#                 errors['last_name_len']='Last Name must be more than 2 characters'

#         if not postData['email']:
#             errors['email_empty']='Email is Empty'
#         elif not EMAIL_REGEX.match(postData['email']):
#                 errors['email']='Invalid email address'
             
#         elif Users.objects.filter(email=postData['email']).exists():
#             errors['email_exist']="Email already registered"
        
#         if not postData['password'] or not postData['confirm_PW']:
#             errors['password_empty']='Paswsord is Empty'
#         else:
#             if len(postData['password'])<8:
#                 errors['password_len']='Password should be more than 8 characters'
#             else:
#                 if postData['password'] != postData['confirm_PW']:
#                     errors['password_confirm']='Password not match'
#         return errors

#     def login_validator(self,postData):
#         errors={}

#         if not postData['email']:
#             errors['email_empty']='Email is Empty'

#         if not postData['password']:
#             errors['password_empty']='Passord is Empty'

#         if not postData['user_email']:
#             errors['password_confirm']='Invalid Email or Password'

#         return errors

# class Users(models.Model):
   
#     first_name=models.CharField(max_length=45)
#     last_name=models.CharField(max_length=45)
#     email=models.EmailField(max_length=255 , unique=True)
#     password=models.CharField(max_length=255)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
#     objects=usersManager()
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"
    
    
# class Actors(models.Model):
#     name=models.CharField(max_length=45)
#     bio=models.TextField()
#     profile_img=models.ImageField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.name}"

# class Directors(models.Model):
#     name=models.CharField(max_length=45)
#     bio=models.TextField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.name}"



# class Movies(models.Model):
#     title=models.CharField(max_length=45)
#     description=models.TextField(max_length=400)
#     release_date=models.DateField()
#     trailer=models.URLField()
#     cover_img=models.ImageField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     actors=models.ManyToManyField(Actors,related_name='movies')
#     directors=models.ManyToManyField(Directors,related_name='movies')

#     def __str__(self):
#         return f'{self.title}'
    
# class Category(models.Model):
#     type=models.CharField(max_length=45)
#     movie=models.ForeignKey(Movies,related_name='categories',on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.type} {self.movie.title}"
    
# class Reviews(models.Model):
#     rating=models.IntegerField()
#     comment=models.TextField(max_length=400)
#     user=models.ForeignKey(Users,related_name='reviews',on_delete=models.CASCADE)
#     movie=models.ForeignKey(Movies,related_name='reviews',on_delete=models.CASCADE)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.first_name} on {self.movie.title}"



