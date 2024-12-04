import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from forum.models import Thread
# Create your models here.


class Question(models.Model):
    
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)  # Relación con Thread
    pollEndDate = models.DateTimeField()  # Duracion de la votación
    
    class Meta:
        permissions = [
            ('can_publish', 'Can publish questions'),
        ]

    def __str__(self):
        return self.question_text
    @property
    def is_active(self):
        return timezone.now() < self.pollEndDate
  
   
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que votó
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Pregunta votada
    timestamp = models.DateTimeField(auto_now_add=True)  # Registro del tiempo del voto

    class Meta:
        unique_together = ('user', 'question')  # Evitar que un usuario vote más de una vez por pregunta

    def __str__(self):
        return f"{self.user} voted on {self.question}"
    
