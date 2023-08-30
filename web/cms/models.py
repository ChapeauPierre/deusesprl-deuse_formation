from django.db import models
from django.utils.translation import gettext_lazy as _


# Custom our HTML content
# Use it with custom_content template tag
class CustomHTMLContent(models.Model):
    token = models.CharField(
        primary_key=True,
        verbose_name=_("Token d'identification"),
        max_length=50,
        unique=True,
        help_text=_("Format: Page HTML - Bloc"))

    content = models.TextField(
        verbose_name=_('Contenu'),
        null=True,
        blank=True,
        help_text="Il y a la possibilité de rajouter du contenu HTML, il est fortement déconseillé de rajouter du css dans ce HTML. Uniquement de balises du type < p >, < b >, < br />, < u >, ... sont autorisées"
    )

    class Meta:
        verbose_name = _('Contenu HTML')
        verbose_name_plural = _('Contenus HTML')
        permissions = [
            ('edit', 'Can edit content'),
        ]

    def __str__(self):
        return self.token
