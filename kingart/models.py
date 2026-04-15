from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="media/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    def preview(self):
        return(self.content[:70]) + "..."
    