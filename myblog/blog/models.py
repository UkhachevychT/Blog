from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

import itertools

class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    img = models.ImageField(null=True, blank=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    slug = models.SlugField(unique=True, editable=False)

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