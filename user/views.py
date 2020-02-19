from django.shortcuts import render,redirect
from django.contrib import messages
from django.db import connection
from .forms import NewUserForm,InformationForm, ReviewForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import Friendship,Information,Reviews


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password")
                
    form = UserCreationForm
    return render(request,"register.html", {"form":form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.info(request, "You are now logged in as username")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, "login.html", {"form":form})


@login_required
def information(request):
    current_user = request.user
    information = Information.objects.get(user_id=current_user.id)  

    if request.method == 'POST':
        form = InformationForm(request.POST,request.FILES,instance=request.user.information)
        form.save()
        if form.is_valid():
            form.save()
            messages.success(request,'successfuly Updated!')
            return redirect("/profile")
    else:
        form = InformationForm(instance=request.user.information)
        # form = InformationForm()
    context = {'form':form, 'information':information}
    return render(request,'information.html',context)

@login_required
def review(request,dish_id,res_ID):
    if request.method == 'POST':
        current_user = request.user
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        with connection.cursor() as cursor:
            cursor.execute('''INSERT INTO user_reviews(comment,rating,name_id, rate_by_id, rate_on_id) 
                              VALUES(%s, %s, %s, %s, %s)''',
                              [comment,rating,dish_id,current_user.id,res_ID])

        url = "/detail/" + str(res_ID)
        return redirect(url) 

    context = {'dish_id': dish_id, 'res_ID':res_ID}
    return render(request, 'review.html', context)

@login_required
def visit(request, res_ID):  
    current_user = request.user
    with connection.cursor() as cursor:
        cursor.execute('''INSERT INTO rating_restaurant_visit_by(restaurant_id, user_id) VALUES(%s, %s);''',
                       [res_ID,current_user.id])

        cursor.execute('''UPDATE rating_restaurant SET number_of_visit = 1+ number_of_visit WHERE res_ID = %s;''',[res_ID])
    url = "/detail/" + str(res_ID)
    return redirect(url) 

@login_required
def profile(request):
    current_user = request.user
    profile = Information.objects.get(user_id=current_user.id)
    with connection.cursor() as cursor:
        cursor.execute('''SELECT res.name, d.name,r.rating,r.comment,r.id
                          FROM (user_reviews r JOIN rating_dish d
                          ON r.name_id=d.dish_id) 
                          JOIN rating_restaurant res ON res.res_ID = r.rate_on_id
                          WHERE r.rate_by_id = %s''',[current_user.id])
        review = cursor.fetchall()


    with connection.cursor() as cursor:
        cursor.execute('''SELECT distinct username FROM auth_user WHERE id in
             (SELECT friend_id FROM user_friendship WHERE creator_id = %s)''', 
                    [current_user.id])
        friends = cursor.fetchall()

    context = {'profile': profile, 'friends':friends, 'review':review}
    return render(request, 'profile.html', context)

@login_required
def log_out(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")


@login_required
def edit_review(request,review_id): 
    if request.method == "POST":   
        review = Reviews.objects.get(pk=review_id)
        form = ReviewForm(request.POST, instance = review)  
        if form.is_valid():  
            form.save()  
            return redirect("/profile") 

    review = Reviews.objects.get(pk=review_id)
    return render(request,'edit_review.html', {'review':review}) 

@login_required
def recommend_friend(request):
    current_user = request.user

    with connection.cursor() as cursor:
        cursor.execute('''SELECT distinct V2.user_id
                    From rating_restaurant_visit_by V1 join rating_restaurant_visit_by V2
                    On V1.restaurant_id=V2.restaurant_id and V1.user_id
                    =%s and V2.user_id<> V1.user_id and V2.user_id not in 
                    (SELECT friend_id FROM user_friendship WHERE creator_id = %s)
                    union
                    select distinct U2.user_id
                    From user_information U1 join user_information U2
                    On U1.Favorite_Cuision = U2.Favorite_Cuision 
                    and U1.user_id<>U2.user_id and U1.user_id=%s and U1.user_id not in
                    (SELECT friend_id FROM user_friendship WHERE creator_id = %s)''', 
                    [current_user.id,current_user.id,current_user.id,current_user.id])
        user = cursor.fetchall()

    for u in user:
        print(u[0],current_user.id)
        with connection.cursor() as cursor:
            cursor.execute('''INSERT INTO user_friendship(creator_id,friend_id)
                VALUES(%s, %s)''', [current_user.id,u[0]])

    return redirect("/profile") 
