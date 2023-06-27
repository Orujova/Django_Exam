from django.shortcuts import render, redirect,get_object_or_404
from .models import Blog
from .forms import BlogForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home_page(request):
  blogs = Blog.objects.all()

  context = {
    "blogs":blogs,
  }
  return render(request,"index.html",context)


def blog_detail_view(request,id):
   blog = get_object_or_404(Blog, id=id)
   
   
   context = {
      'blog': blog,
    }
    
  
   return render(request, "detail.html",context)


@login_required
def create_view(request):
    form = BlogForm()

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('Blog:home')  
    
    context={
      "form":form
    }

    return render(request, 'create.html', context)
  
def update_view(request,id):
  # blog = Blog.objects.get( id=id) 
  blog = get_object_or_404(Blog,id=id)
  form = BlogForm(instance=blog)
  if request.method == 'POST':
    form = BlogForm(request.POST,instance=blog)
    
    if form.is_valid():
      form.save()
      
      return redirect ("Blog:home")
  
  context={
      "form":form
    }
  return render(request, "update.html",context)



def delete_view(request, id):
    blog = get_object_or_404(Blog, id=id)

    if request.method == 'POST':
        blog.delete()
        return redirect("Blog:home")
        
    context = {
        "blog": blog
    }
    return render(request, "delete.html", context)
  
  
@login_required
def like_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)
    return redirect('Blog:home')  
