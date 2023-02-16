

from django.contrib import messages


from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import render ,redirect,get_object_or_404
from django.urls import reverse 

from products.forms import *
from django.http import HttpResponse ,HttpResponseRedirect
from django.views.generic.edit import CreateView ,UpdateView 
from products.models import *
from django.views.generic import ListView ,DetailView ,DeleteView ,View 
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin ,LoginRequiredMixin
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User,Group
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from better_profanity import profanity














def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if request.POST['username'] == '' or request.POST['email'] == '' or request.POST['password'] == '' or \
                request.POST['password2'] == '':
            messages.info(request, 'Requierd Fields')
            return redirect('reges')
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('reges')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('reges')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('login')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('reges')


     
    else:
        return render(request, 'registration/registration2.html')

def islocked(user):
    return Profile.objects.get(user=user).is_locked


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_staff:
                auth.login(request, user)
                return redirect('indexpage')
            elif islocked(user):
                messages.info(request, "This Account is blocked  ")
                return redirect('login')
            else:
                auth.login(request, user)
                return redirect("indexpage")
        else:
            messages.info(request, 'Invalid ')
            return redirect('login')

    else:
        return render(request, 'registration/login2.html')

def subscribe(request, cat_id):
    user = request.user
    category = Catecory.objects.get(id=cat_id)
    category.user.add(user)
    # ----sending email to the user----
    # try:
    #     send_mail("subscribed to a category",
    #                subscribed to category  + category.name,
    #               settings.EMAIL_HOST_USER,
    #               [request.user.email],
    #               fail_silently=False)
    # except Exception as ex:
    #     raise ValidationError("Couldn't send the message to the email ! " + str(ex))
    return redirect("indexpage")


# ---------------------------------categories unsubscribe-------------------------------
def unsubscribe(request, cat_id):
    user = request.user
    category = Catecory.objects.get(id=cat_id)
    category.user.remove(user)
    return redirect("indexpage")




class UserAccess(PermissionRequiredMixin) :
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('/index')
        return super(UserAccess,self).dispatch(request,*args,**kwargs)    
       
    

class Createbookview(CreateView):
    form_class=bookForm
    template_name= "books/createbook.html"
    success_url="/posts"  
    

class Updatabooksview(UserAccess,UpdateView):
    model= book
    form_class=bookForm
    raise_exception=False
    permission_required='books.change_books'
    permission_denied_message=""
    login_url= "/"
    redirect_field_name="next"
    success_url="/index"

    template_name= "books/createbook.html"
    success_url= "/index"

@login_required(login_url='login')

def  bookslistvieww(request): 

  booklist=book.objects.order_by('-created_at')
  p=Paginator(book.objects.all(),5)
  page= request.GET.get('page')
  
  posts=p.get_page(page)
  nums= "a" * posts.paginator.num_pages

  context={"booklist":booklist,'posts':posts,"nums":nums}
  return render   (request,"books/index.html",context)

class booksDetailview(DetailView):
    model=book
    template_name= "books/details.html"
    def get_context_data(self,*args,**kwargs):

        context=super().get_context_data(**kwargs)
        stuff=get_object_or_404(book ,id=self.kwargs['pk'])
        total_likes=stuff.total_likes()

        liked=False
        if stuff.like.filter(id=self.request.user.id).exists():
            liked=True


        context["total_likes"] = total_likes
        context["likedd"] =liked
        return context

    def get_context_data(self,*args,**kwargs):

        context=super().get_context_data(**kwargs)
        stuff=get_object_or_404(book ,id=self.kwargs['pk'])
        total_likes=stuff.total_likes()

        liked=False
        if stuff.like.filter(id=self.request.user.id).exists():
            liked=True


        context["total_likes"] = total_likes
        context["likedd"] =liked
        return context

class booksDeleteview(UserAccess,DeleteView):
    # Permission_required='book.delete_book'
    model=book
    template_name="books/delete.html"
    success_url="/index"   
    raise_exception=False
    permission_required='books.delete_books'

   
def showusername(request):
    User = get_user_model()
    displaynames=User.objects.all()
    context={"displayusers":displaynames}
    return render(request,'books/users.html',context)



def showusercomment(request):
    User = get_user_model()
    displaynames=User.objects.all()
    context={"displayusers":displaynames}
    return render(request,'books/users.html',context)    


class delete_user(SuccessMessageMixin,generic.DeleteView):
    model=User
    template_name='books/deleteuser.html'
    
    success_url=reverse_lazy('users')


class Createcommentview(CreateView):
    model =Comment
    form_class= commentform
    template_name= "books/add_comment.html"
    def form_valid(self, form) :
       form.instance.user = self.request.user 
       form.instance.book_id=self.kwargs['pk']
    
       return super().form_valid(form)
    success_url=reverse_lazy('indexpage')
class Comment_reply(CreateView):
    model =Comment
    form_class= replyform
    template_name= "books/reply.html"
    def form_valid(self, form) :
       form.instance.user = self.request.user 
       form.instance.book_id=self.kwargs['pk']
    
       return super().form_valid(form)
    success_url=reverse_lazy('indexpage')
 

class addlike(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post=book.objects.get(pk=pk)

        is_disliked=False

        for dislike in post.dislike.all():
            if dislike== request.user:
               post.dislike.add(request.user) 
               is_disliked=True
               break
        if is_disliked:
            post.dislike.remove(request.user)

        is_liked=False
        for like in post.like.all():
            if like== request.user:
                is_liked=True
                break
    
        if not is_liked:
            post.like.add(request.user) 
        if is_liked:
            post.like.remove(request.user)

        next= request.POST.get("next",'/')
        
        return HttpResponseRedirect(next)



class dislike(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post=book.objects.get(pk=pk)

        is_liked=False
        for like in post.like.all():
            if like== request.user:
                is_liked =True
                break
        if is_liked:
            post.like.remove(request.user)    

        is_disliked=False

        for dislike in post.dislike.all():
            if dislike== request.user:
               post.dislike.add(request.user) 
               is_disliked=True
               break

        if not is_disliked:
            post.dislike.add(request.user) 
        if is_disliked:
            post.dislike.remove(request.user) 
            
        next= request.POST.get("next",'/')
        
        return HttpResponseRedirect(next)

class Createcatview(CreateView):
    form_class=categoryform
    template_name= "books/createcat.html"
    success_url="/index"  
def search(request):
    
    if request.method=="POST":
        query=request.POST['query']
        items=book.objects.filter(Q(tittle__icontains=query) | Q(content__icontains=query))

        return render( request, 'books/search.html',{'query':query,'items':items})
    else  : 
        return render( request, 'books/search.html')
         
def CategoryView(request,cats):
    category_posts=book.objects.filter(caticory=cats)

    return render (request , 'books/catss.html', {'catss':cats,'category_posts':category_posts})

  
 

def  logout_user(request):
    logout(request)
    messages.success(request,'You were logged out')
    return redirect('login')

def showcategreis(request):
 
    displaycats=Catecory.objects.all()
    context={"displaycats":displaycats}
    return render(request,'books/cats2.html',context)

def adminpage(request):
 
   
    return render(request,'books/admin.html')
class catssDetailview(DetailView):
    model=Catecory
    template_name= "books/datails3.html"

class Updatcatsview(UpdateView):
    model= Catecory
    form_class=categoryform
    raise_exception=False
    

    template_name= "books/createcat.html"
    success_url= "/showcats"    
class CatDeleteview(DeleteView):
    
    model=Catecory
    template_name="books/deletecat.html"
    success_url="/showcats"   
 


def promoteUser(request, id):
    user = User.objects.get(id=id)
  
    if not islocked(user):
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return redirect('users')
    else:
        return redirect('users')
    
def lock_user(user):
    account = Profile.objects.get(user=user)
    account.is_locked = True
    account.save()



def lockUser(request, id):
    user = User.objects.get(id=id)
    lock_user(user)
    return redirect('users')



def unlock_user(user):
    account = Profile.objects.get(user=user)
    account.is_locked = False
    account.save()



def unlockUser(request, id):
    user = User.objects.get(id=id)
    unlock_user(user)
    return redirect('users')   

class baddwordview(CreateView):
    form_class=ForbiddenWordsForm
    template_name= "books/addbadword.html"
    success_url="/forbidd" 
def showForbidden(request):
    forbidden_words = ForbiddenWords.objects.all()
    context = {'forbidden_words': forbidden_words}
    return render(request, "books/showforb.html", context)     
    
class delete_bad(SuccessMessageMixin,generic.DeleteView):
    model=ForbiddenWords
    template_name='books/deletebad.html'
  
    success_url=reverse_lazy('forbiddenshow')
  

class Updatbaddsview(UpdateView):
    model= ForbiddenWords
    form_class=ForbiddenWordsForm
    raise_exception=False
    template_name= "books/addbadword.html"

    success_url="/forbidd"  
@login_required(login_url='login')

def  listall(request): 

  booklist=book.objects.order_by('created_at')

  context={"booklist":booklist}
  return render   (request,"books/posts.html",context)






       







      

    





  