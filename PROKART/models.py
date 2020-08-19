from django.db import models
from django.utils import timezone


class Phones(models.Model):
    name = models.CharField(max_length=100)
    storage = models.IntegerField()
    ram = models.IntegerField()
    price = models.IntegerField()
    display = models.CharField(max_length=100)
    image = models.FilePathField(path='PROKART/static/img/')

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        super(Phones, self).save(**kwargs)
        ratingE = Ratings(phone=self, name='E')
        ratingVG = Ratings(phone=self, name='VG')
        ratingG = Ratings(phone=self, name='G')
        ratingP = Ratings(phone=self, name='P')
        ratingVP = Ratings(phone=self, name='VP')
        ratingE.save()
        ratingVG.save()
        ratingG.save()
        ratingP.save()
        ratingVP.save()


class Comments(models.Model):
    phones = models.ForeignKey(Phones, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_on = models.DateTimeField(default=timezone.now())


class Ratings(models.Model):
    rating_choice = (
        ('E', 'EXCELLENT'),
        ('VG', 'Very Good'),
        ('G', 'Good'),
        ('P', 'Poor'),
        ('VP', 'Very Poor')
    )
    phone = models.ForeignKey(Phones, on_delete=models.CASCADE)
    name = models.CharField(max_length=2, choices=rating_choice)
    vote = models.IntegerField(default=0)
    vote_percent = models.IntegerField(default=0)

    def __str__(self):
        return self.name



