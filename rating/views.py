from django.shortcuts import render,get_object_or_404,redirect  
from .models import Restaurant,Dish
from user.models import Reviews,Information
from django.http import HttpResponse
from .forms import RestaurantForm,CompleteForm
from django.db import connection
from django.template import loader
from django.contrib import messages
import operator


def homepage(request):
    return render(request=request,template_name="home.html")

def index(request):
    res_list = Restaurant.objects.order_by('res_ID')[:]
    context = {'res_list': res_list}
    return render(request, 'index.html', context)

def detail(request, res_ID):
    current_user = request.user
    res_list = Restaurant.objects.get(pk=res_ID)
    with connection.cursor() as cursor:
        cursor.execute('''SELECT * FROM rating_restaurant_visit_by
                          WHERE user_id = %s AND restaurant_id = %s''',
                          [current_user.id, res_ID])
        visit = cursor.fetchall()
    flag = 0
    if visit: flag = 1 
    with connection.cursor() as cursor:
        cursor.execute('''SELECT d.name,r.rating,r.comment 
                          FROM user_reviews r JOIN rating_dish d
                          ON r.name_id=d.dish_id
                          WHERE r.rate_on_id = %s
                          LIMIT 8''',[res_ID])
        review = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute('''SELECT avg(rating) FROM user_reviews
                          WHERE rate_on_id = %s''',[res_ID])
        rate = cursor.fetchall()[0][0]
    menu = Dish.objects.filter(restaurant_id=res_ID)
    context = {'res_list': res_list, 'menu':menu, 'review':review, 'flag':flag, 'rate':rate}
    return render(request, 'detail.html', context)

def destroy(request, res_ID):  
    restaurant = Restaurant.objects.get(res_ID=res_ID)  
    restaurant.delete()  
    return redirect("/index") 

def edit(request, res_ID):  
    restaurant = Restaurant.objects.get(res_ID=res_ID)  
    return render(request,'edit.html', {'restaurant':restaurant})  

def update(request, res_ID):  
    restaurant = Restaurant.objects.get(pk=res_ID)
    form = RestaurantForm(request.POST, instance = restaurant)  
    if form.is_valid():  
        form.save()  
        return redirect("/index")   
    return redirect("/index") 

def insert(request):  
    return render(request,'insert.html') 

def res(request):   

    if request.method == "POST":  
        form = CompleteForm(request.POST)  
       
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/index')  
            except:  
                pass  
    else:  
        form = CompleteForm()  
    return render(request,'insert.html',{'form':form})  

def convert(stri):
    if not stri: stri = None
    return stri

def recommend(request):
    dish_type = convert(request.POST.get('dish_type'))

    with connection.cursor() as cursor:

        cursor.execute('''SELECT DISTINCT R1.res_ID
            FROM rating_Restaurant R1, rating_Dish M1
            WHERE M1.dish_type = %s AND R1.res_ID=M1.restaurant_id AND M1.restaurant_id IN
            (SELECT DISTINCT R.res_ID
            FROM rating_Dish M JOIN rating_Restaurant R
            ON R.res_ID=M.restaurant_id AND M.dish_type = %s
            GROUP BY R.res_ID)
            LIMIT 10''',[dish_type,dish_type])
        res = cursor.fetchall()

    res = [x[0] for x in res]
    res_list = Restaurant.objects.filter(res_ID__in=res)
    template = loader.get_template('result.html')
    context = {'res_list': res_list}
    return HttpResponse(template.render(context, request))

def search(request):
    r_name = convert(request.POST.get('name'))
    cuision_type = convert(request.POST.get('cuision_type'))
    address = convert(request.POST.get('address'))

    with connection.cursor() as cursor:
        cursor.execute('''SELECT r.res_ID FROM rating_Restaurant r
                          WHERE r.name = IFNULL(%s,r.name) AND r.Cuisine_Type = IFNULL(%s,r.Cuisine_Type) 
                          AND r.address = IFNULL(%s, r.address)''',
                       [r_name,cuision_type,address])
        res = cursor.fetchall()
 
    res = [x[0] for x in res]
    res_list = Restaurant.objects.filter(res_ID__in=res)
    template = loader.get_template('result.html')
    context = {'res_list': res_list}
    return HttpResponse(template.render(context, request))

def advanceSearch(request):
    return render(request=request, template_name="advanceSearch.html")


def get_ranking_parameter(W1,W2,W3,W4):
    print(W1,W2,W3,W4)
    avg_rating = dict()
    number_of_visit = dict()
    hours = dict()
    price = dict()
    name = dict()
    with connection.cursor() as cursor:
        cursor.execute('''SELECT number_of_visit, res_ID from rating_restaurant''')
        visit = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute('''SELECT Hours_End - Hours_Start, res_ID from rating_restaurant''')
        T = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute('''SELECT avg(rating),rate_on_id FROM user_reviews group by rate_on_id''')
        R = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute('''SELECT Price_Range, res_ID from rating_restaurant''')
        P = cursor.fetchall()
    
    with connection.cursor() as cursor:
        cursor.execute('''SELECT name, res_ID from rating_restaurant''')
        N = cursor.fetchall()

    for ele in visit:
        number_of_visit[ele[1]] = ele[0]

    for ele in R:
        avg_rating[ele[1]] = float(ele[0])

    for ele in T:
        hours[ele[1]] = ele[0]

    for ele in P:
        price[ele[1]] = ele[0]

    for ele in N:
        name[ele[1]] = ele[0]


    score = dict()

    Rmax = max(avg_rating.values())
    Rmin = min(avg_rating.values())
    Tmax = max(hours.values())
    Tmin = min(hours.values())
    Cmax = max(number_of_visit.values())
    Cmin = min(number_of_visit.values())
    Pmax = max(price.values())
    Pmin = min(price.values())

    for key in price:
        score[key] =  int(100*(W3*(avg_rating[key]-Rmin)/(Rmax-Rmin) + W1*(price[key]-Pmin)/(Pmax-Pmin) \
        + W2*(number_of_visit[key]-Cmin)/(Cmax-Cmin) + W4*(hours[key]-Tmin)/(Tmax - Tmin)))

    score = sorted(score.items(), key=operator.itemgetter(1),reverse=True)
    
    return score,name


def ranking(request):

    W1, W2, W3, W4 = 0.4, 0.2, 0.3, 0.1
    score, name = get_ranking_parameter(W1,W2,W3,W4)

    template = loader.get_template('rank_result.html')
    context = {'name': name, 'score':score}
    return HttpResponse(template.render(context, request))


def person_rank(request):
    if request.method == "POST":               
        W1 = float(request.POST.get('G1'))
        W2 = float(request.POST.get('G2'))
        W3 = float(request.POST.get('G3'))
        W4 = float(request.POST.get('G3'))
        sum_w = W1+W2+W3+W4

        score, name = get_ranking_parameter(W1/sum_w,W2/sum_w,W3/sum_w,W4/sum_w)

        template = loader.get_template('rank_result.html')
        context = {'name': name, 'score':score}
        return render(request,"person_rank.html",context)


    current_user = request.user
    information = Information.objects.get(user_id=current_user.id) 

    #number of visit in price in 3 level/total visit
    #number of visit in long hour/total visit
    #number of visit in high rating/total visit
    #number of visit in res with more visitors/total visit


    with connection.cursor() as cursor:
        cursor.execute('''SELECT avg(u.rating) FROM user_reviews u JOIN rating_restaurant r
            ON r.res_ID=u.rate_on_id where r.res_ID in 
            (SELECT DISTINCT rate_on_id FROM user_reviews 
            where rate_by_id = %s)''', [current_user.id])

        user_rating = cursor.fetchall()[0][0]

    with connection.cursor() as cursor:
        cursor.execute('''SELECT avg(Hours_End - Hours_Start), 
            avg(Price_Range),avg(number_of_visit)
            FROM rating_restaurant where res_ID in 
            (SELECT DISTINCT rate_on_id FROM user_reviews 
            where rate_by_id = %s)''', [current_user.id])

        user_average = cursor.fetchall()
    
    W1, W2, W3, W4 = 0.4, 0.2, 0.3, 0.1
    user_hour = user_average[0][0]
    user_visit = user_average[0][2]
    user_price = user_average[0][1]
    if user_rating and user_hour and user_visit and user_price:

        with connection.cursor() as cursor:
            cursor.execute('''SELECT avg(rating) FROM user_reviews''')
            rating = cursor.fetchall()[0][0]

        with connection.cursor() as cursor:
            cursor.execute('''SELECT avg(Hours_End - Hours_Start), 
                avg(Price_Range),avg(number_of_visit) FROM rating_restaurant''')
            overall = cursor.fetchall()

        c1 = float((user_price-overall[0][1])/overall[0][1])
        c2 = float((user_visit-overall[0][2])/overall[0][2])
        c3 = float((user_rating - rating)/rating)
        c4 = float((user_hour - overall[0][0])/overall[0][0])
        W1 = W1 +W1*c1
        W2 = W2 +W2*c2
        W3 = W3 +W3*c3
        W4 = W4 +W4*c4

    # W1 = information.Price
    # W2 = information.Visit
    # W3 = information.Rating
    # W4 = information.Duration

    sum_w = W1+W2+W3+W4

    score, name = get_ranking_parameter(W1/sum_w,W2/sum_w,W3/sum_w,W4/sum_w)

    context = {'name': name, 'score':score, 'W1':W1, 'W2':W2, 'W3':W3, 'W4':W4}

    return render(request,"person_rank.html",context)

