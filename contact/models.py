from django.db import models

# Create your models here.


class Contact(models.Model):
    class Precedence(models.TextChoices):
        PRIMARY = "primary"
        SECONDARY = "secondary"

    phoneNumber = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=100, null=True)
    linkedId = models.ForeignKey("self", null=True, on_delete=models.DO_NOTHING)
    linkPrecedence = models.CharField(
        max_length=20, choices=Precedence.choices, default=Precedence.PRIMARY
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatededAt = models.DateTimeField(auto_now_add=True)
    deletedAt = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.email=}, {self.phoneNumber=}"
