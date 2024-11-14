from typing import Optional

from django.db import models
from django_extensions.db.fields import AutoSlugField
from .utils import custom_slugify
from django.utils.translation import gettext_lazy as _


class TeamMember(models.Model):
    """Модель участника команды с информацией о ФИО, должности и других данных."""

    name: str = models.CharField(max_length=100, verbose_name='ФИО')
    position: str = models.CharField(max_length=200, verbose_name='Должность')
    bio: str = models.TextField(blank=True, null=True, verbose_name='О себе')
    photo: Optional[models.ImageField] = models.ImageField(upload_to='team_photos/', blank=True, null=True,
                                                           verbose_name='Фотография')
    social_link: str = models.URLField(blank=True, null=True, verbose_name='Ссылка на соцсеть')
    slug: str = AutoSlugField(populate_from='name', slugify_function=custom_slugify, verbose_name='Slug')

    class Meta:
        verbose_name: str = 'Участник организации'
        verbose_name_plural: str = 'Участники организации'

    def save(self, *args, **kwargs) -> None:
        """Сохраняет объект TeamMember и обновляет slug, если имя изменилось."""
        if self.pk:  # Проверяем, является ли это обновлением существующего объекта
            original = TeamMember.objects.get(pk=self.pk)
            if original.name != self.name:
                self.slug = custom_slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Возвращает строковое представление участника команды."""
        return self.name


class Review(models.Model):
    """
    Модель для хранения отзывов клиентов.

    Атрибуты:
        client_name (str): Имя клиента, оставившего отзыв.
        rating (int): Оценка клиента по пятибалльной шкале.
        review_text (str): Текст отзыва, предоставленный клиентом.
        created_at (Optional[datetime]): Дата и время публикации отзыва.
        is_published (bool): Флаг, указывающий, опубликован ли отзыв.
    """

    client_name: str = models.CharField(
        max_length=100,
        verbose_name=_("Имя клиента"),
        help_text=_("Введите имя клиента, оставившего отзыв.")
    )
    rating: int = models.PositiveSmallIntegerField(
        verbose_name=_("Оценка"),
        choices=[(i, i) for i in range(1, 6)],
        default=5,
        help_text=_("Выберите оценку от 1 до 5.")
    )
    review_text: str = models.TextField(
        verbose_name=_("Текст отзыва"),
        help_text=_("Введите текст отзыва.")
    )
    created_at: Optional[models.DateTimeField] = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата публикации"),
        help_text=_("Дата и время публикации отзыва. Устанавливается автоматически при создании записи.")
    )
    is_published: bool = models.BooleanField(
        default=True,
        verbose_name=_("Опубликован"),
        help_text=_("Опубликован ли отзыв на сайте.")
    )

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")
        ordering = ['-created_at']

    def __str__(self) -> str:
        """
        Возвращает строковое представление отзыва, включающее имя клиента и его оценку.

        Returns:
            str: Строка формата "<Имя клиента> - <Оценка>★"
        """
        return f"{self.client_name} - {self.rating}★"

    def short_review(self) -> str:
        """
        Возвращает сокращенную версию текста отзыва, обрезанную до 75 символов.

        Returns:
            str: Сокращенный текст отзыва, заканчивающийся на '...' если длина превышает 75 символов.
        """
        return f"{self.review_text[:75]}..." if len(self.review_text) > 75 else self.review_text
