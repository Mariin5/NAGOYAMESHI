from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

import uuid

from django.core.validators import RegexValidator

#ここ( https://github.com/django/django/blob/main/django/contrib/auth/models.py )のAbstractUserから流用
class CustomUser(AbstractBaseUser, PermissionsMixin):

    username_validator  = UnicodeUsernameValidator()

    # 主キーはUUID(16進数のコード)とする。
    id          = models.UUIDField( default=uuid.uuid4, primary_key=True, editable=False )
    username    = models.CharField(
                    _('username'),
                    max_length=150,
                    unique=True,
                    help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                    validators=[username_validator],
                    error_messages={
                        'unique': _("A user with that username already exists."),
                    },
                )

    # _() は verbose_nameの多言語仕様
    last_name   = models.CharField(_('last name'), max_length=150, blank=True)
    first_name  = models.CharField(_('first name'), max_length=150, blank=True)

    last_name_kana   = models.CharField(verbose_name="姓(カナ)", max_length=150, blank=True)
    first_name_kana  = models.CharField(verbose_name="名(カナ)", max_length=150, blank=True)


    # メールアドレスは入力必須でユニークとする。ログインに使用するため。多重登録を防ぐ。
    email       = models.EmailField(_('email address'), unique=True)

    # 
    tel_regex       = RegexValidator(regex=r'^\d{10,11}$')
    tel             = models.CharField(verbose_name="電話番号", max_length=11, validators=[tel_regex], blank=True, null=True)

    gender_choice = [
        ("男性","男性"),
        ("女性","女性"),
        ("その他","その他"),
    ]
    gender          = models.CharField(verbose_name="性別", max_length=3, choices=gender_choice, null=True, blank=True)
    birthday        = models.DateField(verbose_name="生年月日", null=True, blank=True)


    is_staff    = models.BooleanField(
                    _('staff status'),
                    default=False,
                    help_text=_('Designates whether the user can log into this admin site.'),
                )

    is_active   = models.BooleanField(
                    _('active'),
                    default=True,
                    help_text=_(
                        'Designates whether this user should be treated as active. '
                        'Unselect this instead of deleting accounts.'
                    ),
                )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects     = UserManager()

    EMAIL_FIELD = 'email'

    # メールアドレスを使ってログインさせる。(管理ユーザーも)
    #USERNAME_FIELD = 'username'
    USERNAME_FIELD = 'email'

    # createsuperuserをするとき、入力をするフィールド
    REQUIRED_FIELDS = [ "username" ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        #abstract = True #←このabstractをコメントアウトする。これがコメントアウトされていないとDjangoのデフォルトのユーザーモデルが読み込まれる。

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

