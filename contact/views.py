from django.shortcuts import render
from django.db.models import Q
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import IncomingDetailsSerializer, ContactDetailsSerializer
from .models import Contact
# Create your views here.


class AddContactAPIView(CreateAPIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        serialized_data: IncomingDetailsSerializer = IncomingDetailsSerializer(
            data=request.data
        )
        if serialized_data.is_valid(raise_exception=True):
            contact = Contact.objects.filter(
                email=serialized_data.data["email"],
                phoneNumber=serialized_data.data["phoneNumber"],
            )
            print(contact)
            if contact.exists():
                return Response({"contact": ContactDetailsSerializer(contact).data})

            contact = Contact.objects.filter(
                Q(email=serialized_data.validated_data["email"])
                | Q(phoneNumber=serialized_data.validated_data["phoneNumber"])
            )
            if not contact.exists():
                if (
                    not serialized_data.data["email"] or 
                    not serialized_data.data["phoneNumber"]
                ):
                    return Response(
                        {
                            "contact": ContactDetailsSerializer(
                                contact.filter(
                                    linkPrecedence=Contact.Precedence.PRIMARY
                                )
                            ).data
                        }
                    )

                contact = Contact.objects.create(
                    **serialized_data.validated_data,
                    linkPrecedence=Contact.Precedence.PRIMARY,
                )
                
                res_data: ContactDetailsSerializer = ContactDetailsSerializer(contact)
                return Response({"contact": res_data.data})

            secondary_contact = Contact.objects.create(
                **serialized_data.validated_data,
                linkedId=contact,
                linkPrecedence=Contact.Precedence.SECONDARY,
            )
            res_data: ContactDetailsSerializer = ContactDetailsSerializer(contact)
            return Response({"contact": res_data.data})

        return Response({"message": "Validation errors"})
