from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from datetime import datetime
from abc_app.models import abc_model
from django.contrib.auth import authenticate
from django.http import JsonResponse
import pyotp,time
from django.http import HttpResponse
import smtplib
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required



# Create your views here.
def home(request):
    return render(request,'home.html')
def index(request):

    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        user_id = request.POST.get('username')
        pass1 = request.POST.get('exampleInputPassword1')
        pass2 = request.POST.get('exampleInputPassword2')
        age = request.POST.get('age')
        email_id = request.POST.get('email')
        description = request.POST.get('description')


        print(user_id,pass1,pass2,age)
        check_param = User.objects.filter(username__iexact=user_id).exists()
        if (pass1 != pass2):
            sms = "password Doesn't match";
            print(sms);
            messages.error(request,sms)
            return redirect(index);
        if (check_param):
            messages.error(request,"username already exist")
            return redirect(index);

        if(pass1 == pass2):
            usr_prop = User.objects.create_user(first_name=f_name,last_name=l_name,username=user_id,email=email_id,password=pass1,is_staff=True,date_joined=datetime.now())
            print(usr_prop.password)
            mod_obj = abc_model.objects.create(user=usr_prop,age=age,description=description)
            messages.success(request,"Object:"+str(mod_obj)+'\n'+"user_id:"+str(mod_obj.user.username));
            # +'\n'+"email:"+mod_obj.user.email+'\n'+"password:"+mod_obj.user.password+'\n'+"doj:"+mod_obj.user.date_joined+'\n'+"description:"+mod_obj.description)
            return redirect(login);



    return render(request,'index.html');


def login(request):
        message_html = ''
        if request.method == 'POST':

            username = request.POST.get('user_id')
            password = request.POST.get('password_check')

            auth_user_object = authenticate(username=username,password=password)
            print(auth_user_object)

            if auth_user_object is not None:
                messages.success(request,"Successfully authenticated");
                abc_model_current_user = abc_model.objects.get(user=auth_user_object)
                print(str(abc_model_current_user.user.username)+'\n'+abc_model_current_user.description)
                email_cons = abc_model_current_user.user.email;

                print("!!!!!!!"+ email_cons)
                auth_login(request, auth_user_object);
                return redirect(otp);

            else:
                message_html = "Incorrect username or bad password";


        return render(request,'login.html',{'status': message_html})


def type_view(request):



        return render(request,'type.html')

def ajax_check(request):
        print("ajaxx  ")
        username = request.GET.get('username', None);
        print(username)
        check_param = User.objects.filter(username__iexact=username).exists()
        check = False;
        if check_param :
            check = True;

        data = {
            'is_taken': check,
            }
        return JsonResponse(data)

@login_required(login_url='login')
def otp(request):


    status_text = "OTP sent to your Registered Email!!"
    totp = pyotp.TOTP('base32secret3232',interval=60)
    email_check =  request.user.email

    a = User.objects.get(email=email_check)
    b = abc_model.objects.get(user = a)
    request.session['model_unique_id'] = b.id;

    print(email_check)

    if request.method == 'GET':

        otp_to_send = totp.now()
        print(otp_to_send+'\n')

        status = send_mail(email_check,otp_to_send)


    if request.method == 'POST':
        otp_val_input = request.POST.get('otp_val')
        print(otp_val_input)
        print(totp.verify(otp_val_input))
        if totp.verify(otp_val_input):
            messages.success(request,"Entered correct value")
            return redirect(display_data)
        else:
            messages.error(request,"Incorrect click < -- resend again -- >")



    return render(request,'otp.html',{'status':status_text})


def send_mail(email_cons,pin):

    print(email_cons)
    to = email_cons
    gmail_user = 'your_email_id@gamail.com'
    gmail_pwd = '********'
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: \n' + "The OTP is ";
    print(header)
    msg = header + '\n OTP to login is \n\n' + pin;
    #smtpserver.sendmail(gmail_user, to, msg)
    print("success")
    smtpserver.close()
    return True

@login_required(login_url='login')
def display_data(request):

    model_obj_id = request.session.get('model_unique_id',None)
    model_obj = abc_model.objects.get(id=model_obj_id)
    print("Session :: " + model_obj.user.username)
    user_obj_fields_val = User.objects.filter(id=model_obj.user_id).values()[0]
    print(user_obj_fields_val)
    model_obj_fields_val = abc_model.objects.filter(id=model_obj_id).values()[0]
    print("Model filed \n", model_obj_fields_val )

    return render(request,'display_data.html',{'data_user':user_obj_fields_val,'data_model':model_obj_fields_val,'model_obj_html':model_obj})


@login_required(login_url='login')
def logout_view(request):
    request.session.flush()
    logout(request)
    return render(request,'login.html')
