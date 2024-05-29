from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from ecomapp.models import Products,Cart,Orders
import random
def index(request):
    # userid=request.user.id
    # print("authenthicated status",request.user.is_authenticated)
    a={}
    p=Products.objects.filter(is_active=True)
    a['products']=p
    return render(request,'index.html',a)
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def cart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    sum=0
    for i in c:
        sum=sum+(i.qty*i.pid.price)
    print("total price",sum)
    a={}
    a['products']=c
    a['items']=len(c)
    a['total']=sum
    return render(request,'cart.html',a)
def user_login(request):
    a={}
    print("method is",request.method)
    if request.method=='GET':
        return render(request,'login.html')
    else:
        u=request.POST['uname']
        p=request.POST['upass']
        if u=='' or p=='':
            a['err']="field is empty"
            return render(request,'login.html',a)
        else:
            b=authenticate(username=u,password=p)
            print("creditential ",b)
            if b is not None:
                login(request,b)
                return redirect('/')
            else:
                a['err']='invalid username and password'
                return render(request,'login.html',a)

def register(request):
    b={}
    print("request is",request.method)
    if request.method=='GET':
        return render(request,'register.html')
    else:
        u=request.POST['uname']
        e=request.POST['uemail']
        p=request.POST['upass']
        cp=request.POST['ucpass']
        print(u,e,p,cp)
        if u=='' or e==''or p=='' or cp=='':
            b['err']="please fill all the field"
            return render(request,'register.html',b)
        elif p!=cp:
            b['err']="password didnot match"
            return render(request,'register.html',b)

        else:
            try:
                a=User.objects.create(username=u,email=e,password=p)
                a.set_password(p)
                a.save()
                b['success']="user register successfully! please login"
                return render(request,'register.html',b)
            except Exception:
                b['err']="Already Exist"
                return render(request,'register.html',b)
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # Exclude URLs that should not require login
            excluded_urls = [reverse('login'), reverse('logout'), reverse('signup')]
            if request.path not in excluded_urls:
                # Redirect to the login page
                return redirect('login')
        
        return response


def user_logout(request):
    request.session.flush()
    logout(request)
    
    # Redirect to a specific page after logout, such as the homepage
    return redirect('/')

def cat_filter(request,a):
    q1=Q(is_active=True)
    q2=Q(cat=a)
    p=Products.objects.filter(q1 & q2)
    b={}
    b['products']=p
    return render(request,'index.html',b)
def sort(request,b):
    #print("type is",type(b))
    if b=='0':
        col='price'
    else:
        col='-price'
    p=Products.objects.filter(is_active=True).order_by(col)
    c={}
    c['products']=p
    return render(request,'index.html',c)
def range1(request):
    min=request.GET['min']
    max=request.GET['max']
    #1000 200000---select * from t where p gte 1000 and p lte 20000
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Products.objects.filter(q1 & q2 & q3)
    a={}
    a['products']=p
    return render(request,'index.html',a)

def productsdetails(request,pid):
    a={}
    a['products']=Products.objects.filter(id=pid)
    return render(request,'products_detail.html',a)
def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        q1=Q(uid=userid)
        q2=Q(pid=pid)
        c=Cart.objects.filter(q1 & q2)
        p=Products.objects.filter(id=pid)
        a={}
        a['products']=p
        if c:
            a['msg']='product already exist'
            return render(request,'products_detail.html',a)
        else:
            u=User.objects.filter(id=userid)
            # print("1234",u[0])
            # print('2344',p[0])
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            a['success']='product added successfully'
            return render(request,'products_detail.html',a)
    else:
        return redirect('/login')
    
def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')

def cartqty(request,a,pid):
    userid=request.user.id
    q1=Q(uid=userid)
    q2=Q(pid=pid)
    c=Cart.objects.filter(q1 & q2)
    #print(c)
    qty=c[0].qty
    # print(c[0])
    # print(qty)
    if a=='0':
        if qty>1:
            qty=qty-1
            c.update(qty=qty)
    else:
        qty=qty+1
        c.update(qty=qty)
    return redirect('/cart')

def placeorder(request):
    if request.user.is_authenticated:
        a={}
        c=Cart.objects.filter(uid=request.user.id)
        oid=random.randrange(1000,9999)
        sum=0
        for x in c:
            o=Orders.objects.create(order_id=oid,uid=x.uid,pid=x.pid,qty=x.qty)
            o.save()
            x.delete()
        j=Orders.objects.filter(uid=request.user.id)
        i=len(j)
        for y in j:
            sum=sum+(y.qty*y.pid.price)
        a['products']=j
        a['total']=sum
        a['items']=i
        return render(request,'place_order.html',a)
    else:
        return redirect('/login')

#    sum=0
#     for i in c:
#         sum=sum+(i.qty*i.pid.price)
#     print("total price",sum)
#     a={}
#     a['products']=c
#     a['items']=len(c)
#     a['total']=sum
#     return render(request,'cart.html',a)


    