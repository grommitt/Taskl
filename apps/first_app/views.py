from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import re
from django.db.models import Q, Count
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt


def index(request):
    context = {'all_memberships': Membership.objects.all()}
    return render(request, 'first_app/index.html', context)

def user_home(request):
    user = Membership.objects.get(id=request.session['user_id']) 
    friendslist = user.friends.all()
    context = {
        'user': user,
        'myFriends': user.friends.all(), 
        'notFriends': Membership.objects.exclude(id=request.session['user_id']),
        'my_tasklist': Task.objects.filter(claimed_by=user),
        'others_tasklist': Task.objects.exclude(claimed_by=user),
        
    }
    if len(friendslist)==0:
        messages.add_message(request, messages.ERROR, 'You do not have any friends added yet')
        
    return render(request, 'first_app/user_home.html', context)

def view_task(request, id):
    task = Task.objects.get(id=id)
    context = {
        'claimed_by': task.claimed_by.all(),
        'task': task
    }
    return render(request, 'first_app/viewTask.html', context)

def edit_task(request, id):
    user = Membership.objects.get(id=request.session['user_id'])
    task = Task.objects.get(id=id)
    context = {
        'editTask': task
    }
    if request.method == "POST":
        task_name=request.POST['name']
        task_desc=request.POST['description']
        if len(task_name)>3 and len(task_desc)>10:
            task.name=request.POST['name'] 
            task.description=request.POST['description'] 
            task.save()
        else:
           messages.add_message(request, messages.ERROR, 'Task name must be greater than 3 characters and description must be greater than 10 characters')
        return redirect('/user_home') 
    return render(request, 'first_app/editTask.html', context)

def remove_task(request, id):
    user = Membership.objects.get(id=request.session['user_id'])
    task = Task.objects.filter(id=id).delete()
    return redirect('/user_home')

def add_task(request, id):
    user = Membership.objects.get(id=request.session['user_id'])
    task = Task.objects.get(id=id) 
    task.claimed_by.add(user)
    task.save()
    return redirect('/user_home')  

def create_task(request):
    user = Membership.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        task_name=request.POST['name']
        task_desc=request.POST['description']
        if len(task_name)>3 and len(task_desc)>10:
            new_task = Task.objects.create(name=request.POST['name'], description=request.POST['description'], created_by=user)
           
            messages.success(request, 'You created a task!')
        else:
           messages.add_message(request, messages.ERROR, 'Task name must be greater than 3 characters and description must be greater than 10 characters')
           
        return redirect('/user_home')
    return render(request, 'first_app/createTask.html')


def view_profile(request, id):
    user = Membership.objects.get(id=request.session['user_id']) 
    friend = user.friends.get(id=id)
    context = {
        'friends': friend
    }
    return render(request, 'first_app/viewProfile.html', context)

def view_person(request, id):
    user = Membership.objects.get(id=request.session['user_id']) 
    person = Membership.objects.get(id=id)
    context = {
        'friends': person
    }
    return render(request, 'first_app/viewPerson.html', context)

def remove_friend(request, id):
    user = Membership.objects.get(id=request.session['user_id'])
    removed_friend = Membership.objects.get(id=id)
    user.friends.remove(removed_friend)
    user.save()
    return redirect('/user_home')    

def add_friend(request, id):
    user = Membership.objects.get(id=request.session['user_id'])
    new_friend = Membership.objects.get(id=id)
    user.friends.add(new_friend)
    user.save()
    return redirect('/user_home')

def logout(request):
    request.session.clear()
    return redirect('/')



def create(request):
    if request.method == "POST":
        context = {
            'name' : request.POST['name'], 
            'alias' : request.POST['alias'], 
            'email' : request.POST['email'], 
            'password' : request.POST['password'], 
            'password_confirm' : request.POST['password_confirm']
        }
        user = Membership.objects.validate_registration(context)
        
        if 'the_user' in user:
            request.session['alias'] = user['the_user'].alias
            request.session['user_id'] = user['the_user'].id
            return redirect('/user_home')
        
        if 'errors' in user:
            for key,value in user['errors'].items():
                messages.error(request, value)
            else:
                messages.success(request, "Welcome to the club!")
        return redirect('/')


def login(request):
    context = {
            'email' : request.POST['email'], 
            'password' : request.POST['password'], 
        }
    user = Membership.objects.login(context)
    if 'the_user' in user:
            request.session['alias'] = user['the_user'].alias
            request.session['user_id'] = user['the_user'].id
            return redirect('/user_home')
    if request.method == "POST":
        users_with_same_email = Membership.objects.filter(email = request.POST['email'])

        if len(users_with_same_email) > 0:
            print('user with the email exists! checking passswords now....')
            the_user = users_with_same_email.first()
            if bcrypt.checkpw(request.POST['password'].encode(), the_user.password.encode()):
                print('the passwords match! adding to session')
                request.session['user_id'] = the_user.id
                request.session['user_name'] = the_user.name
                messages.success(request, 'Welcome, {}!'.format(request.session['user_name']))
                return redirect('/user_home')
            else:
                print('passwords do not match')
                messages.error(request, "invalid info")
                return redirect('/')
        else:
            messages.error(request, "invalid info, no users with that email")
            return redirect('/')


