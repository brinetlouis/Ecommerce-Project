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
def check_stock(c):
    stock=True
    for i in c:
        if i.product.stock < i.quantity:
            stock=False
            break
    return stock


from django.contrib import messages
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
            stock=check_stock(c)
            if stock:
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
                    response_payment=client.order.create(dict(amount=total*100,currency='INR'))

                    order_id=response_payment['id']
                    order.order_id=order_id
                    order.amount=total
                    order.is_ordered=False
                    order.save()
                    return render(request, 'payment.html', {"payment": response_payment, 'name': u.username})
                elif order.payment_method == 'COD':
                    order.is_ordered = True
                    order.amount = total
                    order.save()
                    items = Order_items.objects.filter(order=order)
                    for i in items:
                        i.product.stock -= i.quantity
                        i.product.save()
                    c = Cart.objects.filter(user=u)
                    c.delete()
                    return redirect('shop:categories')
                else:
                    pass

            else:
                messages.error(request,'Currently items not available')
                return  render(request,'payment.html')

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from shop.models import User
from cart.models import Order
from django.contrib.auth import login
@method_decorator(csrf_exempt,name='dispatch')
class SuccessView(View):
    def post(self,request,i):
        c=User.objects.get(username=i)
        login(request,c)
        response=request.POST
        print(response)
        o=Order.objects.get(order_id=response['razorpay_order_id'])
        o.is_ordered=True
        o.save()

        items=Order_items.objects.filter(order=o)
        for i in items:
            i.product.stock-=i.quantity
            i.product.save()

        c=Cart.objects.filter(user=c)
        c.delete()

        return render(request,'success.html')




class MyOrdersView(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        return render(request,'myorders.html',{'orders':o})
