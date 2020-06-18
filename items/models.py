from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator 
# Create your models here.

class Item(models.Model):
    item_rating = models.DecimalField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],max_digits=2,decimal_places=1)
    item_price = models.DecimalField(decimal_places=1, max_digits=5)
    item_name = models.CharField(max_length=50)



class Rating(models.Model):
    r_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    r_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    r_user = models.ForeignKey(User, on_delete=models.CASCADE)


# =====================================================================================

def calculate_rating(li):
    no_per_score = {}
    for i in li:
        if i.r_rating in no_per_score.keys():
            no_per_score[i.r_rating] += 1
        else:
            no_per_score[i.r_rating] = 1
    rating = 0
    print(no_per_score)
    for i in no_per_score:
        rating += i*no_per_score[i]
    rating /= len(li)
    return rating
    
    


def find_rating(sender, instance, created, **kwargs):
    if created:
        item = instance.r_item
        li = item.rating_set.all()
        rating = calculate_rating(li)
        item.item_rating = rating
        item.save()


post_save.connect(find_rating, sender=Rating)