
"""amazon URL Configuration


The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from unicodedata import name
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings



from django.urls import path ,include

from products.views import *
from django.contrib.auth.decorators import login_required




urlpatterns = [



 
    path ('admin/' , admin.site.urls)    ,
    path("create",Createbookview.as_view(),name="createbook"),
    path("edit/<int:pk>",Updatabooksview.as_view(),name="editbook"),
    path("index",bookslistvieww,name="indexpage"),
    path("details<int:pk>",(booksDetailview.as_view()),name="detailes"),
      
    path("delete<int:pk>",login_required(booksDeleteview.as_view()),name="delbook"),
    path("regs",register,name='reges'),
    path("",login,name="login"),
    
    path('showuser',showusername,name="users"),
    path('deluser/<int:pk>/',delete_user.as_view(),name='dele'),
    path("details<int:pk>/addcomment" ,Createcommentview.as_view(),name="addcomment"),
    path('lock/<int:id>', lockUser, name="lock"),
    path('unlock/<id>', unlockUser, name="unlock"),

   
    path("createcat",Createcatview.as_view(),name="createcat"),
    path('search/', search, name='search_post'),
    path('category/<int:cats>/',CategoryView,name="category"),
    path ('logouuser',logout_user,name="logoutu"),
    path('showcats',showcategreis,name='showcats'),
    path('adminpage',adminpage,name="adminpage"),
    path('catdetaials<int:pk>',catssDetailview.as_view(),name="catdetailss"),
    path("edietcat/<int:pk>",Updatcatsview.as_view(),name="edietcat"),
    path("delcat<int:pk>",CatDeleteview.as_view(),name="delcat"),
    path('subscribe/<cat_id>', subscribe, name="subscribe"),
    path('unsubscribe/<cat_id>', unsubscribe, name="unsubscribe"),
     
    path("details<int:pk>/addlike",addlike.as_view(),name="like" ),
    path("details<int:pk>/dislike",dislike.as_view(),name="dislike" ),
    path("details<int:pk>/addreply",Comment_reply.as_view(),name="Comment_reply"),
    path('promote/<id>', promoteUser, name="promote"),
    path('addfobed', baddwordview.as_view(), name="addforb"),
    path('forbidd', showForbidden, name="forbiddenshow"),
    path('deletebad<int:pk>',delete_bad.as_view(),name='delete_bad'),
    path('edietbad<int:pk>',Updatbaddsview.as_view(),name='Updatcat'),
    path('posts', listall, name="posts"),

    


    

    


    

] + static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)






   
  
   

    

