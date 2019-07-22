from django.shortcuts import render,get_object_or_404,redirect  
from .models import Restaurant,Dish
from django.http import HttpResponse
from .forms import RestaurantForm,CompleteForm
from django.db import connection
from django.template import loader

def index(request):
    res_list = Restaurant.objects.order_by('res_ID')[:]
    context = {'res_list': res_list}
    return render(request, 'rating/index.html', context)


def detail(request, res_ID):
    res_list = Restaurant.objects.get(pk=res_ID)
    menu = Dish.objects.filter(restaurant_id=res_ID)
    context = {'res_list': res_list, 'menu':menu}
    return render(request, 'rating/detail.html', context)


def destroy(request, res_ID):  
    restaurant = Restaurant.objects.get(res_ID=res_ID)  
    restaurant.delete()  
    return redirect("/rating") 

def edit(request, res_ID):  
    restaurant = Restaurant.objects.get(res_ID=res_ID)  
    return render(request,'rating/edit.html', {'restaurant':restaurant})  

def update(request, res_ID):  
    restaurant = Restaurant.objects.get(pk=res_ID)
    form = RestaurantForm(request.POST, instance = restaurant)  
    if form.is_valid():  
        form.save()  
        return redirect("/rating")   
    return redirect("/rating") 

def insert(request):  
    return render(request,'rating/insert.html') 

def res(request):   

    if request.method == "POST":  
        form = CompleteForm(request.POST)  
       
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/rating')  
            except:  
                pass  
    else:  
        form = CompleteForm()  
    return render(request,'/rating/insert.html',{'form':form})  

def convert(stri):
    if not stri: stri = None
    return stri


def price_re(request):
    price = convert(request.POST.get('price'))
    print(dish_type)
    with connection.cursor() as cursor:
        cursor.execute('''SELECT DISTINCT R1.Name, M1.Name, M1.price
            FROM rating_Restaurant R1, rating_Dish M1
            WHERE M1.price< %s AND R1.res_ID=M1.restaurant_id AND M1.restaurant_id IN
            (SELECT R.res_ID
            FROM rating_Dish M JOIN rating_Restaurant R
            ON R.res_ID=M.restaurant_id AND M.price< %s
            GROUP BY R.res_ID)
            ORDER BY M1.price
            LIMIT 10
            ''',[price])
        dish_list = cursor.fetchall()
    print("recommend: ", dish_list[0][0])
    # dish = [i[0] for i in dish]
    # dish_list = Dish.objects.filter(pk__in=restaurant)
    template = loader.get_template('rating/result.html')
    context = {'dish_list': dish_list}
    return HttpResponse(template.render(context, request))

def recommend(request):
    dish_type = convert(request.POST.get('dish_type'))
    print(dish_type)
    with connection.cursor() as cursor:
        cursor.execute('''SELECT DISTINCT R1.Name, M1.Name, M1.price
            FROM rating_Restaurant R1, rating_Dish M1
            WHERE M1.dish_type like "sal%" AND R1.res_ID=M1.restaurant_id AND M1.restaurant_id IN
            (SELECT R.res_ID
            FROM rating_Dish M JOIN rating_Restaurant R
            ON R.res_ID=M.restaurant_id AND M.dish_type like "sal%"
            GROUP BY R.res_ID)
            ORDER BY M1.price
            LIMIT 10''') #,
            # [dish_type])
        dish_list = cursor.fetchall()
    print("recommend: ", dish_list[0][0])
    # dish = [i[0] for i in dish]
    # dish_list = Dish.objects.filter(pk__in=restaurant)
    template = loader.get_template('rating/result.html')
    context = {'dish_list': dish_list}
    return HttpResponse(template.render(context, request))

def search(request):
    r_name = convert(request.POST.get('name'))
    cuision_type = convert(request.POST.get('cuision_type'))
    address = convert(request.POST.get('address'))

    with connection.cursor() as cursor:
        cursor.execute('''SELECT r.res_ID FROM rating_Restaurant r
                          WHERE r.name = IFNULL(%s,r.name) AND r.Cuisine_Type = IFNULL(%s,r.Cuisine_Type) AND r.address = IFNULL(%s, r.address)''',
                       [r_name,cuision_type,address])
        restaurant = cursor.fetchall()

    res_list = restaurant
    template = loader.get_template('rating/result.html')
    context = {'res_list': res_list}
    return HttpResponse(template.render(context, request))


def searchResult(request, res_list):
    context = {'res_list': res_list}
    return render(request, 'rating/result.html', context)