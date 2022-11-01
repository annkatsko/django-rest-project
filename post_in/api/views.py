from notes.models import Note
from api.serializers import NoteSerializer
from rest_framework.viewsets import ModelViewSet


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer



