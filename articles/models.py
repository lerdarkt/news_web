from django.db import models
from django.core.exceptions import ValidationError


class Tag(models.Model):
    """Модель тега (раздела)"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название раздела"
    )
    
    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Article(models.Model):
    """Модель статьи"""
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок"
    )
    text = models.TextField(
        verbose_name="Текст статьи"
    )
    image = models.ImageField(
        upload_to='articles/',
        blank=True,
        null=True,
        verbose_name="Изображение"
    )
    published_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    tags = models.ManyToManyField(
        Tag,
        through='Scope',
        through_fields=('article', 'tag'),
        verbose_name="Разделы",
        related_name='articles'
    )
    
    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title


class Scope(models.Model):
    """Промежуточная модель для связи Article и Tag"""
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='scopes'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='scopes'
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name="Основной раздел"
    )
    
    class Meta:
        verbose_name = "Раздел статьи"
        verbose_name_plural = "Разделы статьи"
        unique_together = ['article', 'tag']  # Один тег не может быть дважды у статьи
        ordering = ['-is_main', 'tag__name']  # Сначала основные, потом по алфавиту
    
    def __str__(self):
        return f"{self.article.title} - {self.tag.name} ({'основной' if self.is_main else 'дополнительный'})"
