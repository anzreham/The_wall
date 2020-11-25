from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import User, Message, Comment
import bcrypt
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request,'index.html')
def success(request):
        # login status check
    try:
        if request.session["login_user"]["status"]:
            this_user = User.objects.get(id=request.session["login_user"]["login_id"])
            allmessages = Message.objects.all().order_by("-created_at") 
            context = {
                "first_name" : this_user.firstname,
                "last_name" : this_user.lastname,
                "objs"        : allmessages,
            }
            return render(request, "success.html", context)
        
        else:
            messages.error(request, "Login error")
            return redirect("/")

        return render(request,'success.html',context )
    except:
         return redirect("/")
 
@csrf_exempt  
def emailvalidate(request):
    is_taken =User.objects.filter(email=request.POST['email']).exists()
    data = {'is_taken': is_taken}
    return JsonResponse(data)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        email =  request.POST['email']
        errors = User.objects.basic_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST["pass"]
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            User.objects.create(firstname = request.POST['firstname'], lastname =request.POST['lastname'], email = email,
            birthday=request.POST['birthday'] , password  = pw_hash)
            request.session["login_user"] = { "status": True, "login_id": User.objects.get(email=request.POST["email"]).id }
            print(" added to database")
            return redirect("/success")

def log(request):
    
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:

        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        request.session["login_user"] = { "status" : True, "login_id" : User.objects.get(email=request.POST["email"]).id }
        return redirect("/success")

def logout(request):
    del request.session["login_user"]
    return redirect("/")
def addmessage(request):
    this_user = User.objects.get(id=request.session["login_user"]["login_id"])
    Message.objects.create(message = request.POST['message'], user = this_user)
    return redirect (success)
def addcomment(request, id):
    this_user = User.objects.get(id=request.session["login_user"]["login_id"])
    this_message = Message.objects.get(id = int (id))

    Comment.objects.create(comment = request.POST['comment'], userc=this_user, messagec= this_message  )
    return redirect (success)
        # if len(User.objects.filter(email=request.POST["email"])) < 1:
        #     print("Email is not in database")
        #     return redirect("/")

        # else:
        #     print( bcrypt.checkpw(request.POST["pass"].encode(), User.objects.get(email=request.POST["email"]).password.encode()))
        #     # check user password matched with database using bcrypt library
        #     if not bcrypt.checkpw(request.POST["pass"].encode(), User.objects.get(email=request.POST["email"]).password.encode()):
        #         print("Wrong password, please check your password again")
        #         return redirect("/")

        #     else:
        #         print("Successfully, logged in!")
        #         return redirect("/success")




  
