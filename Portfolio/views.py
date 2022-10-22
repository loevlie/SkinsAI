from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, CommentForm, UserForm,BlogPostForm,UpdateBlogPostForm
from django.views import generic
from .models import Post
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import GeeksForm
from torch import Tensor
import numpy as np
import torch
import torch.nn as nn
import os

import os
from glob import glob
#import seaborn as sns
from PIL import Image

read = lambda imname: np.asarray(Image.open(imname).convert("RGB").resize((28, 28), Image.ANTIALIAS))
device = 'cpu'
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3

## Image
def Upload_Your_Image(request):
    context = {}
    context['form'] = GeeksForm()
    if request.method == 'POST':
        form = GeeksForm(request.POST, request.FILES)
        if form.is_valid():
            user_im = form.cleaned_data['skin_image']
            img = read(user_im)
            img = img.reshape(1, 28, 28, 3)
            x = Tensor(img)
            class Net(nn.Module):   
                def __init__(self):
                    super(Net, self).__init__()

                    self.cnn_layers = nn.Sequential(
                        # Defining a 2D convolution layer
                        nn.Conv2d(3, 4, kernel_size=3, stride=1, padding=1),
                        nn.BatchNorm2d(4),
                        nn.ReLU(inplace=True),
                        nn.MaxPool2d(kernel_size=2, stride=2),
                        # Defining another 2D convolution layer
                        nn.Conv2d(4, 4, kernel_size=3, stride=1, padding=1),
                        nn.BatchNorm2d(4),
                        nn.ReLU(inplace=True),
                        nn.MaxPool2d(kernel_size=2, stride=2),
                    )

                    self.linear_layers = nn.Sequential(
                        nn.Linear(4 * 7 * 7, 2)
                    )

                # Defining the forward pass    
                def forward(self, x):
                    x = self.cnn_layers(x)
                    x = x.view(x.size(0), -1)
                    x = self.linear_layers(x)
                    return x
                
            model = Net()
            model.to(device)
            # print current directory
            #print(os.getcwd())
            model.load_state_dict(torch.load("Portfolio/skin_cancer_predictor.pt"))

            model.eval()

            m = nn.Softmax()

            model.eval()
            with torch.no_grad():
                # test_preds = next(iter(test_loader))
                test_pred = model(x.reshape(1,3,28,28))
                # y = test_preds[1][0]
                
                
                # plt.imshow(np.array(test_preds[0][0], dtype='uint8').reshape(28,28,3))
                print(np.argmax(m(test_pred)))
                prediction = np.argmax(m(test_pred))
                context['prediction'] = prediction
                if int(prediction) == 0:
                    prediction = 'beneign'
                    return render( request, "Portfolio/message_sent.html", context)
                else:
                    prediction = 'malignant'
                    return render( request, "Portfolio/about_me.html", context)
                

            
    else:
        form = GeeksForm()
        return render(request, "Portfolio/Upload_Your_Image.html", context)
            




def post_detail(request, slug):
    template_name = 'Portfolio/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None

    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


def successView(request):
    return HttpResponse('Success! Thank you for your message.')

# Create your views here.
def index(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message'] + '  Email: ' + from_email
            try:
                send_mail(subject, message, from_email, ['loevliedenny@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('Portfolio:success')
    return render(request, 'Portfolio/index.html', {'form': form})
    # return render(request,'Portfolio/index.html')

def timeline(request):
    return render(request, 'Portfolio/timeline.html')


def portfolio(request):
    return render(request, 'Portfolio/portfolio.html')


# class UpdatePostView(generic.UpdateView):
#     model = Post
#     template_name = 'Portfolio/update_post.html'
#     fields = ['title', 'slug','snippet', 'content','status']

def UpdatePostView(request,slug):
    blog_post = get_object_or_404(Post,slug=slug)
    if request.method == 'POST':
        user_profile = User.objects.get(username=request.user.username)
        post_form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if post_form.is_valid():
            form = post_form.save(commit=False)
            form.author = user_profile
            form = form.save()
            return render(request,'Portfolio/posted.html',{'action':'updating'})
        else:
            print(post_form.errors)
    else:
        if str(request.user.username) == str(blog_post.author):
            form = UpdateBlogPostForm(instance=request.user,initial = {"title":blog_post.title,"slug":blog_post.slug,"snippet":blog_post.snippet,"content":blog_post.content,"status":blog_post.status})
            return render(request,'Portfolio/update_post.html',{'form':form})
        else:
            return HttpResponse("<h1>Only the user who created the post may edit it</h1>")



class blog(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'Portfolio/blog.html'
    paginate_by = 3
    #return render(request, 'Portfolio/blog.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password) # Authenticating the user for us
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('Blog'))
            else:
                HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            return HttpResponse("Invalide Login")
    else:
        return render(request,'Portfolio/login.html',{})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Blog'))





def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save() # Saving directly to the DATABASE
            user.set_password(user.password) # Hashing the password
            user.save()

            # Set One to One relationship between

            # UserForm and UserProfileInfoForm
            # Can't commit yet because we still need to manipulate

            registered = True
            login(request,user)
    else:
        user_form = UserForm()
        privacy_policy=True
    return render(request,'Portfolio/registration.html',
                          {'user_form':user_form,
                           'registered':registered,})


def AddPostView(request):
    if request.method == 'POST':
        user_profile = User.objects.get(username=request.user.username)
        #model = Post.objects.get(author=user.request.user)
        post_form = BlogPostForm(data=request.POST)
        if post_form.is_valid():
            form = post_form.save(commit=False)
            form.author = user_profile
            form = form.save()
            return render(request,'Portfolio/posted.html',{'action':'making'})
        else:
            return HttpResponse('Something did not work the slug may already exist!')
    else:
        form = BlogPostForm(instance=request.user)
    return render(request,'Portfolio/add_post.html',{'form':form})


def about_me(request):
    return render(request, 'Portfolio/about_me.html')

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message'] + '  Email: ' + from_email
            try:
                send_mail(subject, message, from_email, ['loevliedenny@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, 'Portfolio/message_sent.html')
    return render(request, 'Portfolio/contact.html', {'form': form})