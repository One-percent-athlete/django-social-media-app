from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile, Post, LikePost, Followers

@login_required(login_url='signin')
def home(request):
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user)
    posts = Post.objects.all()
    return render(request, 'home.html', {'user_profile': user_profile, 'posts':posts})
    
    
@login_required(login_url='signin')
def account_setting(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('profile_image') == None:
            image = user_profile.profile_img
        if request.FILES.get('profile_image') != None:
            image = request.FILES.get('profile_image')

        user_profile.profile_img = image
        bio = request.POST['bio']
        location = request.POST['location']
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        return redirect('account_setting')


    return render(request, 'account_setting.html', {'user_profile': user_profile})

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Is Already Registered..")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.warning(request, "Username Has Been Taken..")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                login_user = auth.authenticate(username=username, password=password1)
                auth.login(request, login_user)


                user_model = User.objects.get(username=username)
                user_profile = Profile.objects.create(user=user_model, userid=user_model.id)
                user_profile.save()
                return redirect('account_setting')
        else:
            messages.warning(request, "Password don't match..")
            return redirect('signup')
            
    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            messages.warning(request, "Invalid Account, Please Try Again..")
            return redirect("signin")
    else:
        return render(request, 'signin.html', {})
    

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def profile(request, user_name):
   user = User.objects.get(username=user_name)
   profile = Profile.objects.get(user=user)
   posts = Post.objects.filter(user=user_name)
   num_of_posts = len(posts)
   follower = request.user.username
   followed = user_name

   followers = len(Followers.objects.filter(user=user_name))
   followings = len(Followers.objects.filter(follower=user_name))


   if Followers.objects.filter(follower=follower, user=followed).first():
       button_text = 'Unfollow'
   else:
       button_text = 'Follow'
       

   return render(request, 'profile.html', {'user': user, 'profile': profile, 'posts': posts, "num_of_posts": num_of_posts, 'button_text': button_text, 'followers':followers, 'followings':followings})


@login_required(login_url='signin')
def create_post(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('file')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('home')
    else:
        return redirect('home')

        
@login_required(login_url='signin')
def like_post(request, post_id):
    username = request.user.username
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.num_of_likes += 1
        post.save()
        return redirect('home')
    else:
        like_filter.delete()
        post.num_of_likes -= 1
        post.save()
        return redirect('home')


@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        if Followers.objects.filter(follower=follower, user=user).first():
            follower = Followers.objects.get(follower=follower, user=user)
            follower.delete()
        else:
            follower = Followers.objects.create(follower=follower, user=user)
            follower.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('home')