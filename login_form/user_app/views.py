from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
import datetime
# Create your views here.
@csrf_exempt
def users(request):
    if request.method == "GET":
        user_pk = request.GET.get('pk')
        if user_pk:
            try:
                user = User.objects.get(pk=user_pk)
            except:
                return HttpResponse(json.dumps({"result":"User Not Found"}),content_type='application/json',status=400)
            result = {
                "username":user.username,
                "first_name":user.first_name,
                "last_name":user.last_name,
                "email":user.email,
                "is_superuser":user.is_superuser,
                "pk":user.pk
            }
            return HttpResponse(json.dumps({"result":result}),content_type='application/json',status=200)
        
        all_users = User.objects.all().order_by('pk')
        final_data = []
        for user in all_users:
            result = {
                "username":user.username,
                "first_name":user.first_name,
                "last_name":user.last_name,
                "email":user.email,
                "pk":user.pk,
                "is_superuser":user.is_superuser,
                "is_active":user.is_active,
            }
            final_data.append(result)

        return HttpResponse(json.dumps({"result":final_data}),content_type='application/json',status=200)
    
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        
        if not (username and email):
            return HttpResponse(\
            json.dumps({"result":"username and email are mandatory"}),content_type='application/json',status=400)
        
        if User.objects.filter(email=email).exists():
            return HttpResponse(\
            json.dumps({"result":"Email already exists"}),content_type='application/json',status=400)

        user,created = User.objects.get_or_create(username=username,
                                                email=email,
                                                first_name=first_name,
                                                last_name=last_name
                                                )
                                            
        if password:
            user.set_password(password)
            user.save()
        return HttpResponse(json.dumps({"result":"user added successfully"}),content_type='application/json',status=201)
    
    if request.method == "PUT":
        data = json.loads(request.body) # read body
        user_pk = data.get("pk")
        username = data.get("username")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        last_login = data.get("last_login")
        if last_login:
            last_login = datetime.strptime(last_login, '%Y-%m-%d')
        if not user_pk:
            return HttpResponse(\
            json.dumps({"result":"Please send 'pk' to update user"}),content_type='application/json',status=400)
        try:
            user = User.objects.get(pk=user_pk)
        except:
            return HttpResponse(\
            json.dumps({"result":"User Not Found"}),content_type='application/json',status=400)

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.last_login = last_login
        user.save()
        return HttpResponse(json.dumps({"result":"User updated Successfully"}),content_type='application/json',status=200)
    
    if request.method == "DELETE":

        user_pk = request.GET.get('pk')  #read params
        confirm = request.GET.get('confirm')
        if User.objects.filter(pk=user_pk,is_superuser=True).exists():
            return HttpResponse(json.dumps({"result":"Can't delete Superuser"}),content_type='application/json',status=400) 
        if User.objects.filter(pk=user_pk).exists():
            if confirm in [True,"true","True"]:
                User.objects.filter(pk=user_pk).delete()
                return HttpResponse(json.dumps({"result":"User Deleted Successfully"}),content_type='application/json',status=200) 
            return HttpResponse(json.dumps({"result":"User was not Deleted as you did not confirm"}),content_type='application/json',status=200) 
        return HttpResponse(json.dumps({"result":"User Not found"}),content_type='application/json',status=400) 
    
@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        try:
            user = User.objects.get(email=email)
        except:
            return HttpResponse(json.dumps({"result":"User not Found"}),content_type='application/json',status=400)     
        if user.check_password(password):
            user.last_login = datetime.now()
            user.save()
            return HttpResponse(json.dumps({"result":"Login Successfully"}),content_type='application/json',status=200) 
        return HttpResponse(json.dumps({"result":"Incorrect Password"}),content_type='application/json',status=200) 
