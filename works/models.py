from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from uuid import uuid1
from core.models import SEO


class Album(SEO):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    desc = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Показывать на сайте')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата публикации')

    def get_picture_url(self, filename):
        ext = filename.split('.')[-1]
        filename = '{0}.{1}'.format(self.slug, ext)
        return 'images/albums/{0}'.format(filename)

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение')
    
    image_small = ImageSpecField(source='image',
                                     processors=[ResizeToFill(684, 384)],
                                     format='JPEG',
                                     options={'quality': 90})

    image_admin = ImageSpecField(source='image',
                                 processors=[ResizeToFill(150, 150)],
                                 format='JPEG',
                                 options={'quality': 90})
    
    def get_absolute_url(self):
        return reverse('album', args=[self.slug])

    def image_tag(self):
        try:
            image_link = self.image_admin.url
        except:
            image_link = ''
        return mark_safe('<a href="{0}"><img src="{0}" width="150px"></a>'.format(image_link))
    image_tag.short_description = 'Предпросмотр изоражения'
    image_tag.allow_tags = True

    def image_tag_mini(self):
        try:
            image_link = self.image_admin.url
        except:
            image_link = ''
            print(image_link)
        return mark_safe('<img src="{0}" width="53px">'.format(image_link))
    image_tag_mini.short_description = 'Предпросмотр'
    image_tag_mini.allow_tags = True

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
        ordering = ('created_date',)

    def __str__(self):
        return self.title


class ImageInAlbum(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name='Альбом', related_name='images')

    def get_picture_url(self, filename):
        ext = filename.split('.')[-1]
        filename = '{0}.{1}'.format(uuid1(), ext)
        return 'images/albums/{0}/{1}'.format(self.album.slug, filename)

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение')
    
    image_small = ImageSpecField(source='image',
                                     processors=[ResizeToFit(290)],
                                     format='JPEG',
                                     options={'quality': 90})

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return str(self.id)
