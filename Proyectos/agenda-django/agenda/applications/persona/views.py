from django.shortcuts import render

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
)

from .models import Person, Reunion
from .serializers import (
    PersonSerializer,
    PersonaSerializer, 
    PersonaSerializer2,
    ReunionSerializer,
    PersonaSerializer3,
    ReunionSerializer2,
    ReunionSerializerLink,
)

class PersonListApiView(ListAPIView):

    serializer_class = PersonSerializer

    def get_queryset(self):
        return Person.objects.all()


class PersonSearchApiView(ListAPIView):

    serializer_class = PersonSerializer

    def get_queryset(self):
        kword = self.kwargs['kword']
        return Person.objects.filter(
            full_name__icontains=kword
        )


class PersonCreateView(CreateAPIView):

    serializer_class = PersonSerializer


class PersonDetailView(RetrieveAPIView):

    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class PersonDeleteView(DestroyAPIView):

    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class PersonUpdateView(UpdateAPIView):

    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class PersonRetrieveUpdateView(RetrieveUpdateAPIView):

    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class PersonaApiLista(ListAPIView):
    """
        Vista para interactuar con serializadores
    """
    
    # serializer_class = PersonaSerializer
    # serializer_class = PersonaSerializer2
    serializer_class = PersonaSerializer3

    def get_queryset(self):
        return Person.objects.all()


class ReunionApiLista(ListAPIView):

    # serializer_class = ReunionSerializer
    serializer_class = ReunionSerializer2

    def get_queryset(self):
        return Reunion.objects.all()


class ReunionApiListaLink(ListAPIView):

    serializer_class = ReunionSerializerLink

    def get_queryset(self):
        return Reunion.objects.all()
