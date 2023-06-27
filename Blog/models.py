from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        


class Blog(AbstractModel):
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)

    def __str__(self):
        return self.name
      
      
def upload_image(instance, filename):
    name = instance.blog.name.lower().replace(' ', '-')
    return f"products/{name}/{filename}"
  

class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image)

    def __str__(self):
        return self.blog.name
