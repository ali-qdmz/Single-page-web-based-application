from django.shortcuts import render
from django.shortcuts import HttpResponse
import simplejson
import sqlite3
from django.views.decorators.csrf import csrf_exempt
from persiantools.jdatetime import JalaliDate
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.models import Custom_Auth
from django.utils.crypto import get_random_string
import json
import random
import time
from django.core.mail import BadHeaderError, send_mail
from untitled1.settings import EMAIL_HOST_USER


@csrf_exempt
def stocks(request):
    err = False
    try:
        user = Custom_Auth.objects.get(token=request.headers['Authorization'].split(" ")[1])
    except:
        err = True

    if (not err) and (user.token != ''):
        data = {}
        conn = sqlite3.connect('db.sqlite5')
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables_temp = c.fetchall()
        tables = []
        for item in tables_temp:
            tables.append(item[0])
        data['stocks'] = tables
        json_stuff = simplejson.dumps(data)
        return HttpResponse(json_stuff, content_type="application/json")
    else:
        return HttpResponse("Token expired")


@csrf_exempt
def filters(request):
    err = False
    try:
        user = Custom_Auth.objects.get(token=request.headers['Authorization'].split(" ")[1])
    except:
        err = True

    if (not err) and (user.token != ''):
        data = {}
        conn = sqlite3.connect('db.sqlite4')
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables_temp = c.fetchall()
        tables = []
        for item in tables_temp:
            tables.append(item[0])
        data['filters'] = tables
        json_stuff = simplejson.dumps(data)
        return HttpResponse(json_stuff, content_type="application/json")
    else:
        return HttpResponse("Token expired")


@csrf_exempt
def search_Filters(request):
    err = False
    try:
        user = Custom_Auth.objects.get(token=request.headers['Authorization'].split(" ")[1])
    except:
        err = True

    if (not err) and (user.token != ''):
        table_name = request.GET['search_item']
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        if start_date != '':
            start_date = JalaliDate(int(start_date.split("/")[0]), int(start_date.split("/")[1]),\
                                    int(start_date.split("/")[2])).to_gregorian().strftime("%Y-%m-%d")
        else:
            start_date = '2020-06-02'
        if end_date != '':
            end_date = JalaliDate(int(end_date.split("/")[0]), int(end_date.split("/")[1]),\
                                    int(end_date.split("/")[2])).to_gregorian().strftime("%Y-%m-%d")
        else:
            end_date = datetime.datetime.now().strftime("%Y-%m-%d")

        data = {}
        conn = sqlite3.connect('db.sqlite4')
        c = conn.cursor()
        c.execute("SELECT * FROM `{}` WHERE `تاریخ میلادی` BETWEEN '{}' AND '{}'".format(table_name,start_date,end_date))
        names = list(map(lambda x: x[0], c.description))
        tables = c.fetchall()
        data['search_result'] = tables
        data['columns'] = names
        json_stuff = simplejson.dumps(data)
        return HttpResponse(json_stuff, content_type="application/json")
    else:
        return HttpResponse("Token expired")


@csrf_exempt
def search_Stocks(request):
    err = False
    try:
        user = Custom_Auth.objects.get(token=request.headers['Authorization'].split(" ")[1])
    except:
        err = True

    if (not err) and (user.token != ''):
        table_name = request.GET['search_item']
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        if start_date != '':
            start_date = JalaliDate(int(start_date.split("/")[0]), int(start_date.split("/")[1]),\
                                    int(start_date.split("/")[2])).to_gregorian().strftime("%Y-%m-%d")
        else:
            start_date = '2020-06-02'
        if end_date != '':
            end_date = JalaliDate(int(end_date.split("/")[0]), int(end_date.split("/")[1]),\
                                    int(end_date.split("/")[2])).to_gregorian().strftime("%Y-%m-%d")
        else:
            end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        data = {}
        conn = sqlite3.connect('db.sqlite5')
        c = conn.cursor()
        c.execute("SELECT * FROM `{}` WHERE `تاریخ میلادی` BETWEEN '{}' AND '{}'".format(table_name,start_date,end_date))
        names = list(map(lambda x: x[0], c.description))
        tables = c.fetchall()
        data['search_result'] = tables
        data['columns'] = names
        json_stuff = simplejson.dumps(data)
        return HttpResponse(json_stuff, content_type="application/json")
    else:
        return HttpResponse("Token expired")


@csrf_exempt
def ali(request):
    return render(request,"index_app.html")


@csrf_exempt
def logout(request):
    user = Custom_Auth.objects.get(token=request.headers['Authorization'].split(" ")[1])
    user.token = ''
    user.save()
    return HttpResponse('logedout')


def send_email(code,email):
    try:
        send_mail('کد تایید ثبت نام سایت',str(code), EMAIL_HOST_USER, [str(email)], fail_silently=False)
    except:
        return HttpResponse('Invalid header found.')
    return HttpResponse('thanks')


@csrf_exempt
def signUp(request):
    data = {}
    code = ''
    username = request.GET['username']
    password = request.GET['password']
    email = request.GET['email']

    for i in range(5):
        random_number = random.randint(0,9)
        code += str(random_number)
    unique_id = get_random_string(length=32)
    try:
        user = Custom_Auth.objects.get(email=email)

        if user.email_confirmed == True:
            return HttpResponse("User exists")
        else:
            user.delete()

    except:
        pass
    user = Custom_Auth(username=username, password=password, email=email, token='', temp_token=unique_id)

    data_temp = json.loads(user.temporary_code)
    data_temp.clear()
    data_temp.extend([str(code),time.time()])
    user.temporary_code = json.dumps(data_temp)
    send_email(code=code,email=email)
    user.save()
    data['auth_token'] = unique_id
    json_stuff = simplejson.dumps(data)
    return HttpResponse(json_stuff, content_type="application/json")






@csrf_exempt
def email_Confirim(request):
    temp_token = str(request.headers['Authorization'].split(" ")[1])
    temp_token = temp_token.replace('"',"'")
    user = Custom_Auth.objects.get(temp_token=temp_token.replace("'",''))
    if request.GET['verification_code'] == str(json.loads(user.temporary_code)[0]):
        user.email_confirmed = True
        user.signup_date = str(datetime.datetime.now())
        user.save()
        return HttpResponse("Mail confirmation sucsess")
    else:
        user.email_confirmed = False
        user.save()
        return HttpResponse("Mail confirmation failed")






@csrf_exempt
def signIn(request):
    print("this is sign in")
    data = {}
    try:
        username = Custom_Auth.objects.get(email=request.GET['email'])
    except:
        return HttpResponse("Invalid credentials")
    if username.password == request.GET['password'] and username.email_confirmed == True:
        unique_id = get_random_string(length=32)
        data['auth_token'] = unique_id
        username.token = unique_id
        username.last_login = str(datetime.datetime.now())
        username.save()
        json_stuff = simplejson.dumps(data)
        return HttpResponse(json_stuff, content_type="application/json")
    else:
        return HttpResponse("Invalid credentials")


@csrf_exempt
def add_to_favorites_filters(request):
    err = False
    try:
        user = Custom_Auth.objects.get(token=request.headers['Authorization'].split(" ")[1])
    except:
        err = True

    if (not err) and (user.token != ''):
        item = request.GET['favorite_item']
        data = json.loads(user.favorite_filters)
        data.append(item)
        data = list(set(data))
        user.favorite_filters = json.dumps(data)
        user.save()
        return HttpResponse("done")
    else:
        return HttpResponse("Token expired")

@csrf_exempt
def show_favorites_filters(request):
    err = False
    try:
        user = Custom_Auth.objects.get(token=request.headers['Authorization'].split(" ")[1])
    except:
        err = True

    if (not err) and (user.token != ''):
        data = {}
        data['search_result'] = json.loads(user.favorite_filters)
        json_stuff = simplejson.dumps(data)
        return HttpResponse(json_stuff, content_type="application/json")
    else:
        return HttpResponse("Token expired")


def remove_favorites_filters(request):
    err = False
    try:
        user = Custom_Auth.objects.get(token=request.headers['Authorization'].split(" ")[1])
    except:
        err = True

    if (not err) and (user.token != ''):
        item = request.GET['favorite_item']
        data = json.loads(user.favorite_filters)
        data.remove(item)
        data = list(set(data))
        user.favorite_filters = json.dumps(data)
        user.save()
        return HttpResponse("done")
    else:
        return HttpResponse("Token expired")






@csrf_exempt
def add_to_favorites_stocks(request):
    err = False
    try:
        user = Custom_Auth.objects.get(token=request.headers['Authorization'].split(" ")[1])
    except:
        err = True

    if (not err) and (user.token != ''):
        item = request.GET['favorite_item']
        data = json.loads(user.favorite_stocks)
        data.append(item)
        data = list(set(data))
        user.favorite_stocks = json.dumps(data)
        user.save()
        return HttpResponse("done")
    else:
        return HttpResponse("Token expired")

@csrf_exempt
def show_favorites_stocks(request):
    err = False
    try:
        user = Custom_Auth.objects.get(token=request.headers['Authorization'].split(" ")[1])
    except:
        err = True

    if (not err) and (user.token != ''):
        data = {}
        data['search_result'] = json.loads(user.favorite_stocks)
        json_stuff = simplejson.dumps(data)
        return HttpResponse(json_stuff, content_type="application/json")
    else:
        return HttpResponse("Token expired")

@csrf_exempt
def remove_favorites_stocks(request):
    err = False
    try:
        user = Custom_Auth.objects.get(token=request.headers['Authorization'].split(" ")[1])
    except:
        err = True

    if (not err) and (user.token != ''):
        item = request.GET['favorite_item']
        data = json.loads(user.favorite_stocks)
        data.remove(item)
        data = list(set(data))
        user.favorite_stocks = json.dumps(data)
        user.save()
        return HttpResponse("done")
    else:
        return HttpResponse("Token expired")