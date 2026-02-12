from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile, PaymentTransaction, Watchlist, WatchHistory
from .forms import RegisterForm, EditProfileForm
import razorpay
from content.models import Content
from django.shortcuts import get_object_or_404


# ---------------- REGISTER ----------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            # ✅ Profile is created automatically by signals

            # ✅ Update extra fields safely
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.mobile = form.cleaned_data.get('mobile')
            profile.dob = form.cleaned_data.get('dob')
            profile.plan_confirmed = False
            profile.save()

            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('choose_plan')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            profile, _ = UserProfile.objects.get_or_create(user=user)
            if not profile.plan_confirmed:
                return redirect('choose_plan')
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ---------------- PROFILE ----------------
@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})


# ---------------- EDIT PROFILE ----------------
@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        messages.error(request, "Please fill all required details correctly.")
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'profile': profile, 'form': form})


# ---------------- CHOOSE PLAN ----------------
@login_required
def choose_plan_view(request):
    plan_order = ['free', 'basic', 'premium']
    plans = [{**settings.SUBSCRIPTION_PLANS[key], 'key': key} for key in plan_order]
    if request.method == 'POST':
        selected = request.POST.get('plan')
        if selected == 'free':
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.subscription = 'free'
            profile.subscription_status = 'free'
            profile.plan_confirmed = True
            profile.subscription_updated_at = timezone.now()
            profile.save()
            messages.success(request, "You're on the Free plan.")
            return redirect('home')
        messages.error(request, 'Invalid plan selection.')

    return render(request, 'users/choose_plan.html', {
        'plans': plans,
        'currency': settings.RAZORPAY_CURRENCY
    })


# ---------------- CHECKOUT ----------------
@login_required
def checkout_view(request):
    if request.method != 'POST':
        return redirect('choose_plan')

    plan = request.POST.get('plan')
    plans = settings.SUBSCRIPTION_PLANS
    if plan not in plans or plan == 'free':
        messages.error(request, 'Please choose a paid plan to continue.')
        return redirect('choose_plan')

    plan_data = plans[plan]
    amount_paise = int(plan_data['amount_inr'] * 100)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order = client.order.create({
        'amount': amount_paise,
        'currency': settings.RAZORPAY_CURRENCY,
        'payment_capture': 1
    })

    PaymentTransaction.objects.create(
        user=request.user,
        plan=plan,
        amount=amount_paise,
        currency=settings.RAZORPAY_CURRENCY,
        razorpay_order_id=order['id'],
        status='created'
    )

    return render(request, 'users/checkout.html', {
        'plan': plan,
        'plan_label': plan_data['label'],
        'amount_inr': plan_data['amount_inr'],
        'order_id': order['id'],
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'currency': settings.RAZORPAY_CURRENCY,
        'user': request.user,
    })


# ---------------- PAYMENT VERIFY ----------------
@login_required
def payment_verify_view(request):
    if request.method != 'POST':
        return redirect('choose_plan')

    payment_id = request.POST.get('razorpay_payment_id')
    order_id = request.POST.get('razorpay_order_id')
    signature = request.POST.get('razorpay_signature')
    plan = request.POST.get('plan')
    if plan not in settings.SUBSCRIPTION_PLANS or plan == 'free':
        messages.error(request, 'Invalid plan received.')
        return redirect('choose_plan')

    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
    except Exception:
        PaymentTransaction.objects.filter(
            user=request.user,
            razorpay_order_id=order_id
        ).update(status='failed', razorpay_payment_id=payment_id, razorpay_signature=signature)
        messages.error(request, 'Payment verification failed. Please try again.')
        return redirect('choose_plan')

    PaymentTransaction.objects.filter(
        user=request.user,
        razorpay_order_id=order_id
    ).update(status='paid', razorpay_payment_id=payment_id, razorpay_signature=signature)

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.subscription = plan
    profile.subscription_status = 'active'
    profile.plan_confirmed = True
    profile.last_payment_id = payment_id
    profile.last_order_id = order_id
    profile.subscription_updated_at = timezone.now()
    profile.save()

    messages.success(request, f'Payment successful! You are now on the {plan.title()} plan.')
    return redirect('home')


# ---------------- WATCHLIST ----------------
@login_required
def watchlist_view(request):
    items = Watchlist.objects.filter(user=request.user).select_related('content').order_by('-created_at')
    content_type = request.GET.get('type') or 'all'
    access_level = request.GET.get('access') or 'all'
    if content_type != 'all':
        items = items.filter(content__content_type=content_type)
    if access_level != 'all':
        items = items.filter(content__access_level=access_level)
    return render(request, 'users/watchlist.html', {
        'items': items,
        'content_type': content_type,
        'access_level': access_level
    })


@login_required
def watchlist_toggle_view(request, slug):
    if request.method != 'POST':
        return redirect('watchlist')
    content = get_object_or_404(Content, slug=slug)
    entry = Watchlist.objects.filter(user=request.user, content=content).first()
    if entry:
        entry.delete()
        messages.info(request, 'Removed from your watchlist.')
    else:
        Watchlist.objects.create(user=request.user, content=content)
        messages.success(request, 'Added to your watchlist.')
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'watchlist'
    return redirect(next_url)


# ---------------- WATCH HISTORY ----------------
@login_required
def history_view(request):
    history = WatchHistory.objects.filter(user=request.user).select_related('content').order_by('-last_watched_at')
    return render(request, 'users/history.html', {'history': history})


@login_required
def clear_history_view(request):
    if request.method == 'POST':
        WatchHistory.objects.filter(user=request.user).delete()
        messages.info(request, 'Watch history cleared.')
    return redirect('history')
