from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import FundraisingPost, Transaction
from .forms import FundraisingPostForm, DonationForm

def post_list(request):
    posts = FundraisingPost.objects.filter(is_active=True).order_by('-created_at')
    paginator = Paginator(posts, 9)  # Show 9 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'fundraising/post_list.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = FundraisingPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.save()
            messages.success(request, 'Your fundraising post has been created successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = FundraisingPostForm()
    return render(request, 'fundraising/create_post.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(FundraisingPost, pk=pk)
    transactions = post.transactions.all().order_by('-created_at')
    donation_form = DonationForm()
    return render(request, 'fundraising/post_detail.html', {
        'post': post,
        'transactions': transactions,
        'donation_form': donation_form
    })

@login_required
def make_donation(request, pk):
    post = get_object_or_404(FundraisingPost, pk=pk)
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.post = post
            transaction.donor = request.user
            transaction.save()
            messages.success(request, 'Thank you for your donation!')
            return redirect('post_detail', pk=post.pk)
    return redirect('post_detail', pk=pk)

@login_required
def my_posts(request):
    posts = FundraisingPost.objects.filter(creator=request.user).order_by('-created_at')
    return render(request, 'fundraising/my_posts.html', {'posts': posts})

@login_required
def my_donations(request):
    donations = Transaction.objects.filter(donor=request.user).order_by('-created_at')
    return render(request, 'fundraising/my_donations.html', {'donations': donations})
