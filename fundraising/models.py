from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

class FundraisingPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fundraising_posts')
    image = models.ImageField(upload_to='fundraising_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def progress_percentage(self):
        if self.target_amount > 0:
            return (self.current_amount / self.target_amount) * 100
        return 0

class Transaction(models.Model):
    post = models.ForeignKey(FundraisingPost, on_delete=models.CASCADE, related_name='transactions')
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.donor.username} donated ${self.amount} to {self.post.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the post's current amount
        self.post.current_amount += self.amount
        self.post.save()
