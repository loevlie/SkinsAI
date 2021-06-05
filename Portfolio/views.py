from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, CommentForm
from django.views import generic
from .models import Post



class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3

# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'

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


class blog(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'Portfolio/blog.html'
    paginate_by = 3
    #return render(request, 'Portfolio/blog.html')




class AddPostView(generic.CreateView):
    model = Post
    template_name = 'Portfolio/add_post.html'
    fields = '__all__'