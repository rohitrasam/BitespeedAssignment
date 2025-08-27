from rest_framework import serializers
from .models import Contact


class IncomingDetailsSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=True)
    phoneNumber = serializers.CharField(
        max_length=20,
        allow_blank=True,
    )


class ContactDetailsSerializer(serializers.ModelSerializer):
    primaryContactId = serializers.IntegerField(source="id")
    emails = serializers.SerializerMethodField()
    phoneNumbers = serializers.SerializerMethodField()
    secondaryContactIds = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ["primaryContactId", "emails", "phoneNumbers", "secondaryContactIds"]


    def get_emails(self, obj: Contact):
        return Contact.objects.filter(linkedId=obj.id).values_list("email")

    def get_phoneNumbers(self, obj: Contact):
        return Contact.objects.filter(linkedId=obj.id).values_list("phoneNumber")

    def get_secondaryContactIds(self, obj: Contact):
        return Contact.objects.filter(linkedId=obj.id).values_list("linkedId")