from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNum

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=50)
    content = RichTextUploadingField()
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(Blog)
            readn = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readn.read_num
        except exceptions.ObjectDoesNotExist as e:
            print(e)
            return 0

    def __str__(self):
        return "<blog {0}>".format(self.title)

    class Meta:
        ordering = ['-create_time']






