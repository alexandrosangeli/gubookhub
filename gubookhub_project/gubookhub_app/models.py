from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    url = models.URLField(max_length=256, blank=True)
    favorite_count = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(Profile)

    def __str__(self):
        # User favorited: Book
        return self.book + ' favorited by: ' + self.user.name 
    

class Course(models.Model):
    title = models.CharField(max_length=128, unique=True)
    level = models.IntegerField()
    subject = models.ForeignKey(Subject)

    def __str__(self):
        return self.title

class Subject(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    level = models.IntegerField()
    subject = models.CharField(max_length=128, blank=False) # Considering making it a foreign key later on

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone