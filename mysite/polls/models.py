from django.db import models

# Create your models here.

class Question(models.Model):
    Q_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("data published")

    def __str__(self):
        return self.Q_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    C_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.C_text
