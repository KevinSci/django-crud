from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True) # En blanco si no se pasa nada
    created = models.DateTimeField(auto_now_add=True) # Fecha y hora por defecto si no le pasamos nada
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False) # por defecto ninguna es importante
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - ' + self.user.username
    
    