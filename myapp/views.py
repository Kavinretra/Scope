from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,TemplateView,ListView,UpdateView,DeleteView
from django.views import View
from django.core.mail import send_mail
from django.contrib import messages
import random
import string


class Home(TemplateView):
    template_name='home.html'

class Contact(View):
    def get(self,request):
        form=ContactForm()
        return render(request,'contact.html',{'form':form})
    
    def post(self,request):
        form=ContactForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            phone=form.cleaned_data['phone_number']
            
            try:
                send_mail('Contact details','Name:'+name+', Phone number:'+phone,'kavinretra91@gmail.com',['kavinretra91@gmail.com'])
                messages.success(request,"We will contact you soon..")
                return redirect('contact')
            except:
                messages.error(request,"Can't able to send email now!")
                return redirect('contact')

class About(TemplateView):
    template_name='about.html'

class RegistrationView(View):
    template_name='registration.html'
    model=Registration
    form=RegistrationForm
    def get(self,request):
        return render(request,self.template_name,{'form':self.form})
    def post(self,request):
        form=self.form(request.POST,request.FILES)
        if form.is_valid():
            email=form.cleaned_data['email']
            phone=form.cleaned_data['phone_number']
            if Registration.objects.filter(email=email).exists():
                messages.error(request,'Email already exists')
                return redirect('registration')
            elif Registration.objects.filter(phone_number=phone):
                messages.error(request,'Phone number already exists')
                return redirect('registration')
            else:
                form.save()
                messages.success(request,"Regsitration successfull.")
                return redirect('login')
        else:
            messages.error(request,'Please check the input fields')
            return redirect('registration')

        

class Login(View):
    template_name='login.html'
    model=User
    form=LoginForm
    def get(self,request):
        return render(request,self.template_name,{'form':self.form})
    def post(self,request):
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            try:
                user=User.objects.get(username=username)
                email=user.email
                try:
                    data=Registration.objects.get(email=email)
                except:
                    pass
                if user.check_password(password):
                    if user.is_superuser==True:
                        login(request,user)
                        return redirect('adminpage')
                    elif data.is_active==True:
                        login(request,user)
                        request.session['email']=email
                        return redirect('dashboard')
                    else:
                        messages.error(request,"Your account has been deactivated")
                        return redirect('login')
                else:
                    messages.error(request,'Wrong password!')
                    return redirect('login')
            except:
                messages.error(request,'Username not found!')
                return redirect('login')
        else:
            print(form.errors)
            
class RegisterNow(View):
    template_name='registernow.html'
    model=User
    form=RegisterNow
    def get(self,request):
        return render(request,'registernow.html',{'form':self.form})
    
    def post(self,request):
        form=self.form(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            try:
                data=Registration.objects.get(email=email)
            except:
                messages.error(request,"Register your details with email address")
                return redirect('registration')
            all_characters = string.ascii_letters + string.digits
            length = 6
            password = ''.join(random.choices(all_characters, k=length))
            print(password)
            try:
                send_mail("Temporary password for Scope India Login","Your temporary password is:"+password,"kavinretra91@gmail.com",[email])
            except:
                messages.error(request,"Can't able to send email")
                return redirect('registernow')
            user=User.objects.create(username=username,email=email)
            user.set_password(password)
            user.save()
            messages.error(request,'Your temporary password has been send to your mail.')
            return redirect('login')
        else:
            print(form.errors)
            messages.error(request,'Username or email already exists')
            return redirect('registernow')
        


def logoutpage(request):
    logout(request)
    return redirect('login')


class ForgetPassword(View):
    model=User
    form=ForgetPasswordForm
    def get(self,request):
        return render(request,'forget_password.html',{'form':self.form})
    def post(self,request):
        form=self.form(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            try:
                user=User.objects.get(email=email)
                all_characters = string.ascii_letters + string.digits
                length = 6
                password = ''.join(random.choices(all_characters, k=length))
                print(password)
                try:
                    send_mail("You have requested for a password reset.","Your new password is:"+password,"kavinretra91@gmail.com",[email])
                    messages.error(request,'Your new password has been send to your mail.')
                except:
                    pass
                user.set_password(password)
                user.save()
                return redirect('login')
            except:
                messages.error(request,"Email not registered!")
                return redirect('forget_password')
            
        else:
            print(form.errors)
            messages.error(request,'Username or email already exists')
            return redirect('registernow')

@login_required(login_url='login')
def dashboard(request):
    return render(request,'dashboard.html')


@login_required(login_url='login')
def profile(request):
    email=request.session['email']
    details=Registration.objects.get(email=email)
    return render(request,'profile.html',{'details':details})
    
class EditProfile(View):
    def get(self,request):
        email=request.session['email']
        form=RegistrationForm(instance=Registration.objects.get(email=email))
        return render(request,'editprofile.html',{'form':form})
    def post(self,request):
        email=request.session['email']
        form=RegistrationForm(request.POST,request.FILES,instance=Registration.objects.get(email=email))
        if form.is_valid():
            form.save()
            return redirect('profile')
        
def change_password(request):
    if request.method=='POST':
        form=ChangePasswordForm(request.POST)
        email=request.session['email']
        if form.is_valid():
            oldpassword=form.cleaned_data['old_password']
            newpassword=form.cleaned_data['new_password']
            user=User.objects.get(email=email)
            user.check_password(oldpassword)
            user.set_password(newpassword)
            user.save()
            messages.error(request,"Password changed successfully")
            return redirect('login')
    else:
        form=ChangePasswordForm()
        return render(request,'changepassword.html',{'form':form})
@login_required(login_url='login')
def adminpage(request):
        details=Registration.objects.all()
        return render(request,'list.html',{'details':details})
    
def adminedit(request,id):
    if request.method=='POST':
        form=RegistrationForm(request.POST,request.FILES,instance=Registration.objects.get(id=id))
        if form.is_valid():
            form.save()
            return redirect('adminpage')
    else:
        form=RegistrationForm(instance=Registration.objects.get(id=id))
        return render(request,'adminedit.html',{'form':form})
    
def deactivate(request,id):
    data=Registration.objects.get(id=id)
    email=data.email
    user=Registration.objects.get(email=email)
    user.is_active=False
    user.save()
    return redirect('adminpage')
    
def activate(request,id):
    data=Registration.objects.get(id=id)
    email=data.email
    user=Registration.objects.get(email=email)
    user.is_active=True
    user.save()
    return redirect('adminpage')

def displayall(request,id):
    details=Registration.objects.get(id=id)
    return render(request,'listall.html',{'i':details})
    
class AddDetails(View):
    template_name='adddetails.html'
    model=Registration
    form=RegistrationForm
    def get(self,request):
        return render(request,self.template_name,{'form':self.form})
    def post(self,request):
        form=self.form(request.POST,request.FILES)
        if form.is_valid():
            email=form.cleaned_data['email']
            phone=form.cleaned_data['phone_number']
            if Registration.objects.filter(email=email).exists():
                messages.error(request,'Email already exists')
                return redirect('addetails')
            elif Registration.objects.filter(phone_number=phone):
                messages.error(request,'Phone number already exists')
                return redirect('addetails')
            else:
                form.save()
                return redirect('adminpage')
        else:
            messages.error(request,'Please check the input fields')
            return redirect('addetails')