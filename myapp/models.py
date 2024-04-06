from django.db import models


class Registration(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    gender_choices={('Male','Male'),('Female','Female'),('Others','Others')}
    gender=models.CharField(max_length=100,choices=gender_choices,default='Male')
    date_of_birth=models.DateField()
    email=models.EmailField()
    phone_number=models.IntegerField()
    country=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    hobbies=models.CharField(max_length=100)
    upload_avatar=models.FileField(upload_to='Avatar')
    is_active=models.BooleanField(null=True,default=True)
