import uuid

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from pinkle.utils.utility_func import wsi_confidence

# Create your models here.

# https://github.com/EatEmAll/django-djeddit/blob/d5b988cc94d185320c933f77494f0b1f4680b178/djeddit/models.py#L22


class IntegerRangeField(models.SmallIntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.SmallIntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {"min_value": self.min_value, "max_value": self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Post(models.Model):
    alphanumeric = RegexValidator(r"^[0-9a-zA-Z ]*$", "Only alphanumeric characters are allowed.")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        verbose_name=_("Post title"), help_text=_("Required"), max_length=225, validators=[alphanumeric]
    )
    body = models.TextField(verbose_name=_("Post body"), help_text=_("Required"), max_length=50)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    zip_code = models.CharField(_("zip code"), max_length=5, null=True, blank=True)
    # parent = models.ForeignKey(
    #     "self", null=True, blank=True, related_name="comments", db_index=True, on_delete=models.CASCADE
    # )
    truncated_body = models.CharField(verbose_name=_("Truncated body text"), help_text=_("Required"), max_length=50)
    grade = models.CharField(
        null=True,
        blank=True,
        verbose_name=_("Grade focus of post"),
        help_text=_("Required, 2 to 3 letter grade"),
        max_length=3,
    )

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    up_votes = models.IntegerField(_("Up votes"), default=0)
    down_votes = models.IntegerField(_("Down votes"), default=0)
    score = models.IntegerField(_("Vote score"), default=0)

    @staticmethod
    def _voteSetterWrapper(attr):
        def voteSetter(self, value):
            setattr(self, attr, max(0, value))
            self.wsi = wsi_confidence(self.up_votes, self.down_votes)

        return voteSetter

    @property
    def score(self):
        return self.up_votes - self.down_votes

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        Post.upvotes = property(lambda self: self.up_votes, Post._voteSetterWrapper("up_votes"))
        Post.downvotes = property(lambda self: self.down_votes, Post._voteSetterWrapper("down_votes"))

    def getComments(self, excluded=()):
        """:param excluded: exclude all posts with these uids and their descendants"""
        comments = Post.objects.filter(parent=self.id).exclude(id__in=excluded)
        for reply in comments:
            comments |= reply.getComments(excluded=excluded)
        return comments

    def _addToIncludedComments(self, post):
        if not hasattr(self, "included_comments"):
            self.included_comments = [post]
        else:
            self.included_comments.append(post)

    def getCommentList(self):
        comments = []
        for p in self.included_comments:
            comments.append(p)
            if p.included_comments:
                comments += p.getCommentList()
        return comments

    def save(self, *args, **kwargs):
        if not self.truncated_body:
            self.truncated_body = self.body[:50]
        super(Post, self).save(*args, **kwargs)


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name="+")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="+")
    value = IntegerRangeField(default=0, min_value=-1, max_value=1)
