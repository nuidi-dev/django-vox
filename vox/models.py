from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.template.defaultfilters import slugify

class LikeManager(models.Manager):
    def get_queryset(self):
        return super(LikeManager, self).get_queryset().annotate(likes_num=Count('likes'))

class LikeModel(models.Model):
    liked = models.BooleanField(default=0)
    likes = models.ManyToManyField(User, \
    related_name="%(app_label)s_%(class)s_related", \
    related_query_name="%(app_label)s_%(class)ss", \
    blank=True)

    objects = models.Manager()
    objects_likes = LikeManager()

    class Meta:
        abstract = True

    def has_user_liked(self, user_id):
        user_like = self.likes.filter(id=user_id)
        if user_like.exists():
            return user_like
        else:
            return None

    def is_owner(self, user_id):
        if self.author.id == user_id:
            return True
        return False

    def like(self, user_id):
        if self.has_user_liked(user_id):
            self.likes.remove(user_id)
            return False
        else:
            self.likes.add(user_id)
            return True

class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            c=0
            slug = slugify(self.name)
            while True:
                try:
                    if (c==0): Category.objects.get(slug=slug)
                    else: Category.objects.get(slug="{}-{}".format(slug,c))
                    c+=1
                except Category.DoesNotExist:
                    if (c==0): self.slug = slug
                    else: self.slug = "{}-{}".format(slug, c)
                    break

        super(Category, self).save(*args, **kwargs)

class Topic(LikeModel):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    text = models.TextField()
    author = models.ForeignKey(User, related_name='author')
    created = models.DateTimeField(auto_now_add=True)
    last_post = models.OneToOneField('Post', related_name='last_in_topic', blank=True, null=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            c=0
            slug = slugify(self.title)
            while True:
                try:
                    if (c==0): Topic.objects.get(slug=slug)
                    else: Topic.objects.get(slug="{}-{}".format(slug,c))
                    c+=1
                except Topic.DoesNotExist:
                    if (c==0): self.slug = slug
                    else: self.slug = "{}-{}".format(slug, c)
                    break

        super(Topic, self).save(*args, **kwargs)

class Post(LikeModel):
    topic = models.ForeignKey(Topic)
    text = models.TextField()
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        self.topic.last_post = self
        self.topic.save()
