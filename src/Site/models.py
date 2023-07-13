from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
import os

class Profile(AbstractUser):
    avatar = models.ImageField("Фотография", default="img/noImage.jpg",upload_to="img/")
    debt = models.FloatField("Задолжность", default=0)

    def save(self, *args, **kwargs):
        # Если пароль есть и он не является хэшем
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Forum(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название темы')
    Description = models.CharField(max_length=500, verbose_name='Описание темы')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Автор')
    voting = models.OneToOneField('VotingOption', on_delete=models.CASCADE, verbose_name='Голосование', null=True, blank=True,  related_name='forum_voting')
    titleVoting = models.CharField(max_length=200, verbose_name='Название голосования')
    def __str__(self):
        return self.title


class VotingOption(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, verbose_name='Форум', related_name='voting_options')
    # voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='options', verbose_name='Голосование')
    option_text = models.CharField(max_length=200, verbose_name='Текст варианта голосования')
    voters = models.ManyToManyField(Profile, blank=True, related_name='voted_options', verbose_name='Проголосовавшие')
    def __str__(self):
        return self.option_text


class Comment(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='comments', verbose_name='Форум')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments', verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст комментария')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата комментария')

    def __str__(self):
        return f'Комментарий №{self.id}'

# class Voting(models.Model):
#     forum = models.ForeignKey('Forum', on_delete=models.CASCADE, verbose_name='Форум', related_name='voting_forum')
#     title = models.CharField(max_length=200, verbose_name='Название голосования')

#     def __str__(self):
#         return self.title
class News(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField("Название", max_length=150)
    date = models.DateField("Дата")
    announcement = models.BooleanField("Анонсировать", default=False)
    content = models.TextField("Содержимое")
    image = models.ImageField("Фотография", default="img/noImage.jpg",upload_to="img/")


class Docs(models.Model):
    CATEGORY_CHOICES = [
        ('ustavnye', 'Уставные документы'),
        ('protokoly', 'Протоколы собраний'),
        ('zayavleniya', 'Заявления и бланки'),
    ]

    id = models.BigAutoField(primary_key=True)
    title = models.CharField("Название документа", max_length=100)
    date = models.DateField("Дата")
    file = models.FileField("Файл", upload_to="file/")
    size = models.CharField("Размер файла", max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def size(self):
        filepath = self.file.path
        return get_file_size(filepath)

    def size_formatted(self):
        size_in_kb = self.size() / 1024
        return "{:.1f} кб".format(size_in_kb)
    size_formatted.short_description = "File Size"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # При сохранении модели обновляем размер файла
        self.size()

    def delete(self, *args, **kwargs):
        # При удалении модели также удаляем файл и обновляем размер
        filepath = self.file.path
        if os.path.exists(filepath):
            os.remove(filepath)
        super().delete(*args, **kwargs)

def get_file_size(filepath):
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        return size
    return 0