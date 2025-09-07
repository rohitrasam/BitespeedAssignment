from rest_framework import serializers
from .models import Contact


class IncomingDetailsSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=True, allow_blank=True)
    phoneNumber = serializers.CharField(
        allow_null=True,
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
        emails = set(Contact.objects.filter(linkedId=obj.id).values_list("email", flat=True))
        emails.add(obj.email)
        return emails

    def get_phoneNumbers(self, obj: Contact):
        phoneNumbers = set(Contact.objects.filter(linkedId=obj.id).values_list("phoneNumber", flat=True))
        phoneNumbers.add(obj.phoneNumber)
        return phoneNumbers

    def get_secondaryContactIds(self, obj: Contact):
        return set(Contact.objects.filter(linkedId=obj.id).values_list("id", flat=True))