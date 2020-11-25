from django.db import models
import re
import bcrypt
from datetime import date
class logandregManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['firstname']) < 2:
            errors["firstname"] = "please fill the  firstname field at least 2 char"

        if len(postData['lastname']) < 2:
            errors["lastname"] = "please fill the network field at least 2 char"
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
       
        if User.objects.filter ( email = postData['email']):
             errors['email'] = "this email exist"
        if len(postData['lastname']) < 8:
            errors["pass"] = "please type valid characters number in the lastname fiald"

        if postData['pass'] != postData['passconf']:
            errors["pass1"] = "please type the confirmed password correctly"
            
        x = postData['birthday'].split('-')
        year_of_birth = int (x[0])

        if year_of_birth > 2019:
             errors["pass2"] = "the birthday must be in the past"
        else:
            current_year = date.today().year
            age = int(current_year) - year_of_birth
            if age < 13:
                errors["pass3"] = "under valid age"




        return errors



    def login_validator(self, postData):

        errors = {}
        if len(postData['email']) < 1:
            errors["logemail"] = "empty email field"

        user = User.objects.filter(email=postData['email']) # why are we using filter here instead of get?
        if user: # note that we take advantage of truthiness here: an empty list will return false
            # if not bcrypt.checkpw(postData['pass'].encode(), logged_user.password.encode()):
            if not bcrypt.checkpw( postData["pass"].encode(), User.objects.get(email=postData['email']).password.encode()):
                errors["logpass"] = "the password is wrong"
        else:
            errors["logemail2"] = "not registred"
            
        return errors

class User (models.Model):
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    birthday= models.DateField()
    password = models.CharField(max_length = 45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = logandregManager()

    # def __repr__(self):
    #     return f"<Dojo object: Name = {self.lastname}> , id: {self.id}" 

class Message (models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name= "users", on_delete = models.CASCADE)

    @property
    def getallcomments(self):
        return Comment.objects.filter(messagec = self )
 

class Comment (models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userc = models.ForeignKey(User, related_name= "usersC", on_delete = models.CASCADE)
    messagec = models.ForeignKey(Message, related_name= "messagesC", on_delete = models.CASCADE)


