from django.db import models
from django.utils import timezone
from users.models import User
from catalog.models import Substitute


class Comment(models.Model):
    content = models.TextField()
    date_added = models.DateTimeField(default=timezone.now, verbose_name="Date d'ajout")
    author = models.ForeignKey(User, related_name="comments_author", on_delete=models.CASCADE)
    substitute = models.ForeignKey(Substitute, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username
