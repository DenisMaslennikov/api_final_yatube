from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    image = models.ImageField(upload_to="posts/", null=True, blank=True)
    group = models.ForeignKey(
        to="Group",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Группа",
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )


class Follow(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="followers",
    )
    following = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Подписан на",
        related_name="followings",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "following"), name="unique following"
            ),
        ]


class Group(models.Model):
    title = models.CharField(verbose_name="Название группы", max_length=200)
    slug = models.SlugField(verbose_name="Слаг", max_length=50)
    description = models.TextField(verbose_name="Описание")
