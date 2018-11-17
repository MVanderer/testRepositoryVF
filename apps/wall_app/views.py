from django.shortcuts import render, redirect
from .models import *
import bcrypt

# Views the landing page. If logged in - takeds user to dash.
def index(request):
    if 'errors' not in request.session:
        request.session['errors']={}
    if 'current_user' not in request.session:
        return render(request,"index.html")
    else:
        return redirect('/wall')

#The dash. To be filled with whatever content necessary
def wall(request):
    if 'current_user' not in request.session:
        return redirect('/')
    context = {
        'username':
            User.objects.get(email=request.session['current_user']).first_name,
        'messages': Message.objects.all()
    }
    return render(request,'wall.html',context)

#New user handling. First user created becomes admin
def sign_up(request):
    request.session.clear()
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        if len(errors):
            request.session['errors']=errors
            return redirect('/')
        else:
            #encoding password
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
            #checking if creating the first user
            if len(User.objects.all()) == 0:
                access_level = 9
            else:
                access_level = 1
            #Userbuilder and login wrapped together
            User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=hashed_pw, access_level=access_level)
            request.session['current_user']=request.POST['email']
    return redirect('/wall')

#Login view hands password confirmation to the models
def log_in(request):
    request.session.clear()
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            request.session['errors']=errors
            return redirect('/')
        else:
            request.session['current_user']=request.POST['email']
    return redirect('/wall')

#pretty self-explanatory
def log_off(request):
    request.session.clear()
    return redirect('/')

def post_message(request):
    if request.method=='POST':
        if len(request.POST['message'])>0:
            Message.objects.create(message=request.POST['message'],author=User.objects.get(email=request.session['current_user']))
    return redirect('/wall')

def post_comment(request, id):
    if request.method=='POST':
        if len(request.POST['comment'])>0:
            Comment.objects.create(comment=request.POST['comment'],author=User.objects.get(email=request.session['current_user']),message=Message.objects.get(id=id))
    return redirect('/wall')

def message_delete(request,id):
    message = Message.objects.get(id=id)
    message.delete()
    return redirect('/wall')

def comment_delete(request, id):
    Comment.objects.get(id=id).delete()
    return redirect('/wall')