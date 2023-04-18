from django.db import models


class TgUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey("core.User", on_delete=models.CASCADE, null=True, blank=True, default=None)
    verification_code = models.CharField(max_length=100, null=True, blank=True, default=None)

    class Meta:
        verbose_name = "tg пользователь"
        verbose_name_plural = "tg пользователи"
