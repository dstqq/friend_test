from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from .models import CustomUser, Friend_Request, Friend
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'something went wrong')
    context = {}
    return render(request, 'registration/login_in_da_house.html', context)



def signupPage(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False )
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'users/registration.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('home')


def userProfile(request, pk):
    user = CustomUser.objects.get(id=pk)
    requests = []
    if user != request.user:
        try:
            are_friends = Friend.objects.get(
                to_user=user, from_user=request.user)
        except:
            are_friends = None

        if are_friends is not None:
            status = "friends"
        else:
            try:
                friend_request_to_me = Friend_Request.objects.get(
                    from_user=user, to_user=request.user)
            except:
                friend_request_to_me = None

            if friend_request_to_me is not None:
                status = "request_to_me"
                requests.append(friend_request_to_me)
            else:
                try:
                    friend_request_from_me = Friend_Request.objects.get(
                        from_user=request.user, to_user=user)
                except:
                    friend_request_from_me = None

                if friend_request_from_me is not None:
                    status = "request_from_me"
                else:
                    status = None
    else:
        status = "own_profile"
    context = {'user_profile': user, 'status': status}
    if requests != []:
        context['friend_request'] = requests[0]
    return render(request, 'users/profile.html', context)



def check_telegram_auth(user):
    if user.telegram_confirm_code == user.connect_telegram_form:
        user.is_connect_to_telegram = True
        user.telegram_confirm_code = 0
        user.save()


@login_required
def updadeProfile(request):
    user = request.user
    form = CustomUserChangeForm(instance=user)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            if user.is_connect_to_telegram is False:
                check_telegram_auth(user)
            return redirect('profile', pk=user.id)

    return render(request, 'users/update_profile.html', {'form': form})


@login_required
def send_friend_request(request, userID):
    from_user = request.user
    to_user = CustomUser.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(
        from_user=from_user, to_user=to_user)
    if created:
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponse('nope')


@login_required
def friendsPage(request):
    friends = Friend.objects.all().filter(from_user=request.user)
    context = {'friends': friends}
    return render(request, 'users/friends.html', context)


@login_required
def accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.accept()
        messages.success(request, 'new friend')
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponse('not oke')


@login_required
def reject_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    friend_request.reject()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
def friend_requests(request):
    requests = Friend_Request.objects.all().filter(
        to_user=request.user, rejected=None)
    context = {'requests': requests}
    return render(request, 'users/friend_requests.html', context)


@login_required
def cancel_my_friend_request(request, userID):
    try:
        to_user = CustomUser.objects.get(id=userID)
        friend_request = Friend_Request.objects.get(
            from_user=request.user, to_user=to_user)
        friend_request.cancel()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    except:
        return False
    

@login_required
def delete_from_friends(request, userID):
    friend = CustomUser.objects.get(id=userID)
    try:
        friendship_to_user = Friend.objects.get(from_user=request.user, to_user=friend)
        friendship_to_user.delete()
        friendship_from_user = Friend.objects.get(from_user=friend, to_user=request.user)
        friendship_from_user.delete()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    except:
        return HttpResponse('something went wrong')
