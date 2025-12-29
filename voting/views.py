from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Voter

# ---------------- HOME ----------------
def home(request):
    return render(request, 'voting/home.html')


# ---------------- REGISTER ----------------
def register(request):
    # ✅ CLEAR OLD MESSAGES
    list(messages.get_messages(request))

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

    return render(request, 'voting/register.html')


# ---------------- LOGIN ----------------
def login_view(request):
    # ✅ CLEAR OLD MESSAGES
    list(messages.get_messages(request))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'voting/login.html')


# ---------------- DASHBOARD ----------------
@login_required
def dashboard(request):
    voters = Voter.objects.all()
    return render(request, 'voting/dashboard.html', {'voters': voters})


# ---------------- ADD VOTER ----------------
@login_required
def add_voter(request):
    # ✅ CLEAR OLD MESSAGES FIRST
    list(messages.get_messages(request))

    if request.method == 'POST':
        voter_id = request.POST['voter_id']
        name = request.POST['name']
        age = int(request.POST['age'])

        if age < 18:
            messages.error(request, 'You are not eligible to vote')
            return redirect('add_voter')

        if Voter.objects.filter(voter_id=voter_id).exists():
            messages.error(request, 'Voter ID already exists')
            return redirect('add_voter')

        Voter.objects.create(
            voter_id=voter_id,
            name=name,
            age=age
        )

        messages.success(request, 'Voter added successfully')
        return redirect('dashboard')

    return render(request, 'voting/add_voter.html')



# ---------------- EDIT VOTER ----------------
@login_required
def edit_voter(request, id):
    voter = get_object_or_404(Voter, id=id)

    if request.method == 'POST':
        voter.name = request.POST['name']
        voter.age = int(request.POST['age'])
        voter.save()
        messages.success(request, 'Voter updated successfully!')
        return redirect('dashboard')

    return render(request, 'voting/edit_voter.html', {'voter': voter})


# ---------------- DELETE VOTER ----------------
@login_required
def delete_voter(request, id):
    voter = get_object_or_404(Voter, id=id)
    voter.delete()
    messages.success(request, 'Voter deleted successfully!')
    return redirect('dashboard')


# ---------------- VOTE ----------------
@login_required
def vote(request, voter_id):
    voter = get_object_or_404(Voter, id=voter_id)

    if request.method == 'POST':
        party = request.POST['party']
        voter.voted_party = party
        voter.has_voted = True
        voter.save()
        messages.success(request, f"{voter.name} voted to {voter.voted_party}")
        return redirect('dashboard')

    return render(request, 'voting/vote.html', {'voter': voter})
