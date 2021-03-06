from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse

import itertools

class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    img = models.ImageField(null=True, blank=True, verbose_name='image')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    slug = models.SlugField(unique=True, editable=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        editable=False,
    )

    class Meta():
        ordering = ['-created']

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()

            self.slug = orig = slugify(self.title)

            for x in itertools.count(1):
                if not Post.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (orig, x)

        self.modified = timezone.now()
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        editable=False,
    )
    body = models.TextField()
    date = models.DateTimeField(editable=False)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        editable=False,
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = timezone.now()
        return super(Comment, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'slug': self.slug})

