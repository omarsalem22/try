


from django.db import models
from django.shortcuts import get_object_or_404 
from django.urls import reverse 
from django.contrib.auth.models import User
from PIL import Image




class Catecory(models.Model):
    name=models.CharField(max_length=100 ,unique=True )
    user = models.ManyToManyField(User, related_name='categories')
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    pic=models.ImageField(upload_to='books/images/owner/',null=True)
    
    def __str__ (self) :
        return   self.name    
    def get_img_cat(self):
        return f"/media/{self.pic}"  
    def get_show_url(self):
        return reverse("detailes",args=[self.id])  
    def save(self):
        super().save()  
        img=Image.open(self.pic.path)
        if img.height >300 or img.width > 300:
            outputsize=(200,200)
            img.thumbnail(outputsize)
            img.save(self.pic.path)
              



class book(models.Model):
    tittle=models.CharField(max_length=100)
    image=models.ImageField(upload_to='books/images/book/',null=True)
    content=models.CharField(max_length=100)

  
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    caticory=models.ForeignKey(Catecory, on_delete=models.CASCADE, related_name="cats",null=True)
    like=models.ManyToManyField(User,related_name='likebook')
    dislike=models.ManyToManyField(User,related_name='dislikebook')


    def total_likes(self):
        return self.like.count()
  

    
    from django.urls import reverse


    def __str__ (self) :
        return  f" {self.tittle } " 
    def get_img_url(self):
        return f"/media/{self.image}"  
    def get_show_url(self):
        return reverse("detailes",args=[self.id])    
    def get_edit_url(self):
        return reverse("editbook",args=[self.id])   
    def get_delete_url(self)   :
        return reverse ("delbook",args=[self.id]) 
    def createbookurl(self):
     
        return reverse("createbook")    
class user(models.Model):

    username=models.CharField(max_length=100)
    @classmethod
    def showuser(cls,id):
        return get_object_or_404(cls ,pk=id)
    @classmethod
    def geturls(cls):
        return reverse("users")   
    def get_delete_url(self):
        return reverse("deleteuser",args=[self.id])     
    def get_user_url(self):
        return reverse("details",args=[self.id])     
    def get_show_url(self):
        return reverse("detailesuser")    
class Comment(models.Model):
    book=models.ForeignKey('book', on_delete=models.CASCADE, related_name="commentpost")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.TextField()
    data_added=models.DateTimeField(auto_now_add=True)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name='+')
    reply=models.TextField(null=True)

    class Meta:
        ordering=['data_added']
    def  __str__(self) :


        return 'Comment {} by {}'.format(self.body, self.user)
   
   

class ForbiddenWords(models.Model):
    forbidden_word = models.CharField(max_length=100)

    def __str__(self):
        return self.forbidden_word


class Profile(models.Model):
    user= models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    is_locked= models.BooleanField(default=False)
    id_user = models.IntegerField()

    def __str__(self):
        return self.user.username        





   
