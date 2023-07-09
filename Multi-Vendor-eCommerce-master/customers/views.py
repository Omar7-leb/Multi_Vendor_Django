from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib import messages
from django.contrib.auth import (
    authenticate, login, update_session_auth_hash, views as auth_views,
)
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, force_text
from order.models import OrderItem, Order

from .decorators import customer_required
from .forms import CustomerSignUpForm, CustomerUpdateForm
from .utils import service
from django.http import HttpResponse
from .tokens import account_activation_token
from .models import User


@customer_required
def customerWishlistAndFollowedStore(request):
    ''' customer wishlist and followed store.'''
    return render(request, 'customer/wishlist_and_followed_store.html')


@customer_required
def CustomerProfile(request):
    ''' customer profile '''
    orders = Order.objects.filter(customer=request.user.customer)
    # orders = OrderItem.objects.filter(customer=request.user.customer)

    context = {
        'customer': request.user.customer,
        'orders': orders,
    }

    return render(request, 'customer/customer_profile.html', context)


@customer_required
def CustomerProfileUpdate(request):
    ''' Update customer profile '''
    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, request.FILES, instance=request.user.customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('customer_profile')
    else:
        form = CustomerUpdateForm(instance=request.user.customer)
        context = {
            'form': form,
        }
        return render(request, 'customer/customer_profile_edit.html', context)



# def CustomerSignUpView(request):
#     ''' Sign up view for new customer account.'''
#     if request.method == 'POST':
#         form = CustomerSignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Thanks for registering. You are now logged in.')
#             user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
#             login(request, user)
#             #service.send_welcome_mail(request, request.user.customer.email)
#             return redirect('/')
#         else:
#             messages.error(request, 'Invalid form.')
#
#     else:
#         form = CustomerSignUpForm()
#     return render(request, 'customer/sign_up.html', {'form': form})

def CustomerSignUpView(request):
    ''' Sign up view for new customer account.'''
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Thanks for registering. You are now logged in.')

            current_site = get_current_site(request)
            mail_subject = 'Activate your  account.'
            message = render_to_string('customer/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = 'html'
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
             return render(request, 'customer/sign_up.html', {'form': form})
            # login(request, user)
            #service.send_welcome_mail(request, request.user.customer.email)

    form = CustomerSignUpForm()
    return render(request, 'customer/sign_up.html', {"form":form})



def activate(request, uidb64, token):
    print(uidb64)
    print(token)
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    print(user)
    print(account_activation_token.check_token(user,token))

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

@customer_required
def change_password_view(request):
    '''A form for allowing customer to change with old password '''
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password Change Successfully!")
            return redirect('/')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "customer/password_change.html", {"form": form})


class SignInView(auth_views.LoginView):
    ''' Sign in for customer '''
    form_class = AuthenticationForm
    template_name = 'customer/sign_in.html'
