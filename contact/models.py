from django.db import models

# Create your models here.


class Contact(models.Model):
    class Precedence(models.TextChoices):
        PRIMARY = "primary"
        SECONDARY = "secondary"

    phone_number = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=100, null=True)
    linked_id = models.ForeignKey("self", null=True)
    link_precedence = models.CharField(
        max_length=20, choices=Precedence.choices, default=Precedence.PRIMARY
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updateded_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.email=}, {self.phone_number=}"
