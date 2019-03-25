from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


_custom_perm =  (
            ('can_view', _('Permesso in lettura')),
            ('can_view_his_own', _('Permesso in lettura esclusivamente '
                                   'dei propri inserimenti')),
            ('can_change', _('Permesso in modifica')),
            ('can_change_his_own', _('Permesso in modifica esclusivamente '
                                     'dei propri inserimenti')),
            ('can_delete', _('Permesso in cancellazione')),
            ('can_delete_his_own', _('Permesso in cancellazione '
                                     'esclusivamente dei propri inserimenti')),
                )

class User(AbstractUser):
    GENDER= (
                ( 'male', _('Maschio')),
                ( 'female', _('Femmina')),
                ( 'other', _('Altro')),
            )

    # for NameID extreme lenghtness
    USERNAME_FIELD = 'username'
    username = models.CharField(_('Username'), max_length=64,
                                  blank=False, null=False, unique=True)
    is_active = models.BooleanField(_('attivo'), default=True)
    email = models.EmailField(_('email address'), blank=True, null=True)
    matricola = models.CharField(_('Matricola'), max_length=254,
                                 blank=True, null=True,
                                 help_text="come rappresentata su CSA")
    first_name = models.CharField(_('Nome'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('Cognome'), max_length=30,
                                 blank=True, null=True)
    codice_fiscale = models.CharField(_('Codice Fiscale'), max_length=16,
                                      blank=True, null=True)
    gender    = models.CharField(_('Genere'), choices=GENDER,
                                 max_length=12, blank=True, null=True)
    location = models.CharField(_('Luogo di nascita'), max_length=30,
                                blank=True, null=True)
    birth_date = models.DateField(_('Data di nascita'), null=True, blank=True)

    class Meta:
        ordering = ['username']
        verbose_name_plural = _("Accounts")
        permissions = _custom_perm

    def __str__(self):
        return '{} - {} {}'.format(self.matricola,
                                   self.first_name, self.last_name)
