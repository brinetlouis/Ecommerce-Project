from django.db.transaction import commit
from django.shortcuts import render, redirect
from django.views import View
from shop.models import Product
from cart.models import Cart
import razorpay
from cart.models import Order_items


class AddtoCartView(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        try:
            c=Cart.objects.get(user=u,product=p)
            c.quantity+=1
            c.save()
        except:
            c=Cart.objects.create(user=u,product=p,quantity=1)
            c.save()
        return redirect('cart:cartview')


class CartView(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.quantity*i.product.price
        return render(request,'cart.html',{'cart':c,'total':total})


class MinusView(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        try:
            c=Cart.objects.get(user=u,product=p)
            if c.quantity >1:
                c.quantity-=1
                c.save()
            else:
                c.delete()

        except:
            pass
        return redirect('cart:cartview')


class RemoveView(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        try:
            c=Cart.objects.get(user=u,product=p)
            c.delete()

        except:
            pass
        return redirect('cart:cartview')

from cart.forms import OrderForm

class OrderView(View):
    def get(self,request):
        form_instance=OrderForm()
        u = request.user
        c = Cart.objects.filter(user=u)
        total = 0
        for i in c:
            total += i.quantity * i.product.price
        return render(request,'orderview.html',{'form':form_instance,'total':total})

    def post(self,request):
        form_instance=OrderForm(request.POST)
        if form_instance.is_valid():
            order=form_instance.save(commit=False)
            order.user=request.user
            order.save()
            c=Cart.objects.filter(user=request.user)
            for i in c:
                o=Order_items.objects.create(order=order,product=i.product,quantity=i.quantity)
                o.save()

            u = request.user
            c = Cart.objects.filter(user=u)
            total = 0
            for i in c:
                total += i.quantity * i.product.price
            if order.payment_method=="ONLINE":
                client=razorpay.Client(auth=('rzp_test_DhoX0AaVKOSz3n','WKbn9CA2nRasi4FiVJOT1Jnd'))
                response_payment=client.order.create(dict(amount=total,currency='INR'))

                order_id=response_payment['id']
                order.order_id=order_id
                order.is_ordered=False
                order.save()
            else:
                order.is_ordered=True
                order.save()
            return render(request,'payment.html')