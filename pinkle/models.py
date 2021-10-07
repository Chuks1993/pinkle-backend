import uuid

from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from pinkle.utils.utility_func import wsi_confidence

# Create your models here.

# https://github.com/EatEmAll/django-djeddit/blob/d5b988cc94d185320c933f77494f0b1f4680b178/djeddit/models.py#L22
# https://programmingwithmosh.com/backend/graphql/using-graphql-in-your-python-django-application/


# class SubGroup(models.Model):
#     name = models.CharField(max_length=20, null=False, blank=False)
#     slug = models.SlugField(unique=True)

#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super(SubGroup, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.name


# class Tag(models.Model):
#     name = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.name


class Post(models.Model):
    alphanumeric = RegexValidator(r"^[0-9a-zA-Z ]*$", "Only alphanumeric characters are allowed.")
    # subGroup = models.ForeignKey(SubGroup, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        verbose_name=_("Post title"), help_text=_("Required"), max_length=225, validators=[alphanumeric]
    )
    body = models.TextField(verbose_name=_("Post body"), help_text=_("Required"), max_length=50)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    zip_code = models.CharField(_("zip code"), max_length=5, null=True, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    # tags = models.ManyToManyField(Tag, blank=True)
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, default=None, related_name="users_favorited"
    )

    @property
    def truncated_body(self):
        return self.body[:100]

    @property
    def favorite_count(self):
        return self.favorites.count()

    @property
    def natural_created_at(self):
        return naturaltime(self.created_at)

    @property
    def post_comments(self):
        return list(Comment.objects.filter(post=self))

    @property
    def comment_count(self):
        print(list(Comment.objects.filter(post=self)))
        return 1

    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="users_liked")

    @property
    def natural_created_at(self):
        return naturaltime(self.created_at)

    @property
    def like_count(self):
        return self.likes.count()

    class Meta:
        ordering = ["created_at"]


# class Notification(models.Model):
#     reciever = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications", on_delete=models.CASCADE)
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_notifications", on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Sender: {self.sender} // Reciever: {self.reciever} // On post: {self.post}"

#     def date_sent(self):
#         return self.created_at.strftime("%B %d %Y")
