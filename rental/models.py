from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Car(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):

        if self.start_date and self.end_date and self.start_date <= self.end_date:
            days = (self.end_date - self.start_date).days + 1
            self.total_price = days * self.car.price_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.car.name}"



@receiver(post_save, sender=Booking)
def mark_car_unavailable(sender, instance, **kwargs):
    car = instance.car
    car.is_available = False
    car.save()

@receiver(post_delete, sender=Booking)
def mark_car_available(sender, instance, **kwargs):
    car = instance.car
    car.is_available = True
    car.save()

