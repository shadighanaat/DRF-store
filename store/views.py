from django.shortcuts import render
from .models import Product, Customer, OrderItem, Order, Category, Customer, Comment
from django.db.models import Count, Avg, F, Func, Value


def Showdata(request):
    cat = Category.objects.create(title='headphon', description= 'this is headphone')
    p1 = Product()
    p1.name = 'p1'
    p1.category = cat
    p1.slug = 'p-1'
    p1.description = 'p1 descriptions'
    p1.unit_price = 1000
    p1.inventory = 1
    p1.save()
    # new_comment = Comment()
    # new_comment.name = 'SHADI'
    # new_comment.body = 'SALAM'
    # new_comment.product = product
    # new_comment.save()
   
    return render(request, 'hello.html')

