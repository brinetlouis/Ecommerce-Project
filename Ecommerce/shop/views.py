from django.shortcuts import render,redirect
from django.views import View
from shop.models import Category,Product
from shop.forms import SignupForm
from shop.forms import LoginForm
from shop.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from shop.forms import AddCategoryForm,AddProductForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class CategoryView(View):
    def get(self,request):
        c=Category.objects.all()
        return render(request,'categories.html',{'cate':c})


class ProductView(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        return render(request,'product.html',{"cate":c})



class DetailView(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        return render(request,'view_product.html',{"pro":p})


class SignupView(View):
    def get(self,request):
        form_instance=SignupForm()
        return render(request,'signup.html',{'form':form_instance})
    def post(self,request):
        form_instance=SignupForm(request.POST)
        if form_instance.is_valid():
            user=form_instance.save(commit=False)
            user.is_active=False
            user.save()
            user.generate_otp()
            send_mail(
                "Ecommerce  OTP",
                user.otp,
                "brinetlouis@gamil.com",
                [user.email],
                fail_silently=False,
            )
            return redirect("shop:otp")


class OtpView(View):
    def get(self,request):
        return render(request, 'otp.html', )
    def post(self,request):
        otp=request.POST['otp']
        try:
            u=User.objects.get(otp=otp)
            u.is_active=True
            u.is_verified=True
            u.save()
            return redirect('shop:categories')
        except:
            messages.error(request,"Invalid OTP")
            return redirect('shop:otp')



class LoginView(View):
    def get(self,request):
        form_instance=LoginForm()
        return render(request,'login.html',{'form':form_instance})
    def post(self,request):
        form_instance=LoginForm(request.POST)
        if form_instance.is_valid():
            name=form_instance.cleaned_data['username']
            pwd = form_instance.cleaned_data['password']
            user=authenticate(username=name,password=pwd)
            if user and user.is_superuser==True:
                login(request,user)
                return redirect('shop:categories')
            elif user and user.is_superuser==False:
                login(request, user)
                return redirect('shop:categories')

            else:
                print("invalid user credentials")
                return redirect('shop:signin')


class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('shop:categories')


class AddCategoryView(CreateView):
    form_class=AddCategoryForm
    template_name = 'add_category.html'
    model = Category
    success_url = reverse_lazy('shop:categories')


class AddProductView(View):
    def get(self,request):
        form_instance=AddProductForm()
        return render(request,'add_product.html',{'form':form_instance})
    def post(self,request):
        form_instance=AddProductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
