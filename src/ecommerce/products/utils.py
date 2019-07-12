import random
import string

from django.utils.text import slugify

def randomStringGenerator(size=15, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def uniqueSlugGenerator(instance, newSlug=None):
    if newSlug is not None:
        slug = newSlug
    else:
        slug = slugify(instance.title)

    instanceClass = instance.__class__
    qs_exists = instanceClass.objects.filter(slug=slug).exists()
    if qs_exists:
        newSlug = "{slug}-{randstr}".format(slug=slug, randstr=randomStringGenerator(size=5))
        return uniqueSlugGenerator(instance, newSlug=newSlug)
    return slug