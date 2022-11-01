from django.db.models import EmailField, CharField, BooleanField, DateTimeField, Model, TextField, ForeignKey, SET_NULL
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.

class Note(Model):
    author = ForeignKey(User, null=True, blank=False, on_delete=SET_NULL)
    title = CharField(max_length=255)
    text = TextField(blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated']