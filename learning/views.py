from django.shortcuts import render, HttpResponse, redirect
from .models import Contact, Subject, Videos, VideoComment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .templatetags import extras

# Create your views here.
def index(request):
    return render(request, "index.html")

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        msg = request.POST['msg']
        # print(name, email, phone, msg)

        contact = Contact(name=name, email=email, phone=phone, msg=msg)
        contact.save()
        messages.success(request, 'Your message has been sent successfully.')
    return render(request, "contact.html")


def SignUp(request):
    if request.method == 'POST':
        # get the post parameters
        uname=request.POST['uname']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous inputs
        if len(uname) > 10:
            messages.error(request, 'Username must be under 10 characters')
            return redirect('index')
        if len(pass1) < 6:
            messages.error(request, 'Password is too short')
            return redirect('index')
        if len(pass1) > 13:
            messages.error(request, 'Password is too long')
            return redirect('index')
        if not uname.isalnum():
            messages.error(request, 'Username should only contain letters and numbers')
            return redirect('index')
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match')
            return redirect('index')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email you entered has already been taken. Please try another email.')
            return redirect('index')

        # Create the user
        try:
            myuser= User.objects.get(username=uname)
            messages.error(request, 'The username you entered has already been taken. Please try another username.')
            return redirect('index')
        
        except User.DoesNotExist:
            myuser = User.objects.create_user(uname, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, "Your account has been successfully created")
        return redirect('index')

    else:
        return HttpResponse('404 - Not Found')


def LogIn(request):
    if request.method == 'POST':
        luname=request.POST['luname']
        lpass=request.POST['lpass']
        user = authenticate(username=luname, password=lpass)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged In')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password, please try again!')
            return redirect('index')
    return HttpResponse('404 - Not Found')


def LogOut(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out')
    return redirect('index')


def about(request):
    return render(request, 'about.html')

def allsubject(request):
    subj = Subject.objects.all()
    context = {'subj': subj}
    return render(request, 'allsubject.html', context)

def pvideos(request, slug):
    vds = Videos.objects.filter(slug=slug).first()
    coursecontent = Videos.objects.filter(subject=vds.subject)
    comments = VideoComment.objects.filter(video=vds, parent=None)
    replies = VideoComment.objects.filter(video=vds).exclude(parent=None)
    replayDict = {}
    for replay in replies:
        if replay.parent.sno not in replayDict.keys():
            replayDict[replay.parent.sno] = [replay]
        else:
            replayDict[replay.parent.sno].append(replay)
    # print(replayDict)
    context = {'vds':vds, 'comments':comments, 'coursecontent':coursecontent, 'user':request.user, 'replayDict':replayDict}
    return render(request, 'pvideos.html', context)

def search(request):
    query = request.GET['query']
    if len(query) > 100:
        allvds = Videos.objects.none()
    else:
        allvdstitle = Videos.objects.filter(title__icontains=query)
        allvdscontent = Videos.objects.filter(cont__icontains=query)
        allvds = allvdstitle.union(allvdscontent)
        paginator = Paginator(allvds, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
    context = {'allvds':page_obj, 'query':query}
    return render(request, 'search.html', context)

    
def videoComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        videoSno = request.POST.get('videoSno')
        video = Videos.objects.get(sno=videoSno)
        rsno = request.POST.get('rsno')
        if rsno == "":
            comments= VideoComment(comment=comment, user=user, video=video)
            comments.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = VideoComment.objects.get(sno=rsno)
            comments = VideoComment(comment=comment, user=user, video=video, parent=parent)
            comments.save()
            messages.success(request, "Your replay has been posted successfully")
        
    return redirect(f"/videos/{video.slug}")