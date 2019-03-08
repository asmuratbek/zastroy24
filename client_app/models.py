# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
from io import BytesIO

from MyBrands import settings
from product.utils import add_watermark, get_wt_image_url
from geoposition.fields import GeopositionField


class Subscribers(models.Model):
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписавшиеся на обновления'

    email = models.EmailField(verbose_name='Почта')
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.email)


class Feedback(models.Model):
    class Meta:
        verbose_name = 'писмо'
        verbose_name_plural = 'Обратная связь'

    is_read = models.BooleanField(default=False, verbose_name='Прочитано?')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия', null=True)
    email = models.CharField(max_length=255, verbose_name='Email')
    phone_number = models.CharField(max_length=255, verbose_name='Телефон')

    created_at = models.DateField(auto_now_add=True, verbose_name='Дата отправки', null=True)

    def __unicode__(self):
        return self.first_name + ' - ' + self.email


class AffiliateFeedback(models.Model):
    is_read = models.BooleanField(default=False, verbose_name='Прочитано?')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=255, verbose_name='Телефон')
    affiliate = models.ForeignKey('Contact', verbose_name='Филиал', blank=True)

    created_at = models.DateField(auto_now_add=True, verbose_name='Дата отправки', null=True)

    def __unicode__(self):
        return "%s %s -> %s" % (self.first_name, self.last_name, self.affiliate.email)


class AdminEmails(models.Model):
    class Meta:
        verbose_name_plural = 'Почта администраторов'
        verbose_name = 'почту'

    email = models.EmailField(verbose_name='Почта')
    is_active = models.BooleanField(default=True, verbose_name='Активный?')

    def __unicode__(self):
        return self.email


class SiteSettings(models.Model):
    class Meta:
        verbose_name_plural = 'Настройки сайта'
        verbose_name = 'настройку'

    phone = models.CharField(max_length=255, verbose_name='Телефон')
    weight = models.ForeignKey('product.AllProductProperties', verbose_name='Указатель веса', null=True)


    trust = RichTextUploadingField(verbose_name='Нам доверяют', null=True, blank=True)
    order = RichTextUploadingField(verbose_name='Просто заказать', null=True, blank=True)
    delivery = RichTextUploadingField(verbose_name='Доставка', null=True, blank=True)
    pay = RichTextUploadingField(verbose_name='Легко заплатить', null=True, blank=True)
    promotions = RichTextUploadingField(verbose_name='Скидки и акции', null=True, blank=True)

    def __unicode__(self):
        return 'Настройка сайтов'


class About(models.Model):
    class Meta:
        verbose_name_plural = 'О нас'
        verbose_name = 'О нас'

    body = RichTextUploadingField(verbose_name='О нас')
    about_in_numbers = models.ManyToManyField('AboutInNumbers', verbose_name='Мы в цифрах', blank=True)
    team = models.ManyToManyField('OurTeam', verbose_name='Наша команда', blank=True)

    def __unicode__(self):
        return 'Страница О Нас'


class AboutInNumbers(models.Model):
    class Meta:
        verbose_name_plural = 'Мы в цифрах'
        verbose_name = 'цифры'

    key = models.CharField(max_length=255, verbose_name='Название')
    number = models.CharField(max_length=255, verbose_name='Цифры')

    def __unicode__(self):
        return "%s - %s" % (self.key, self.number)


class OurTeam(models.Model):
    class Meta:
        verbose_name_plural = 'Наша команда'

    image = models.ImageField(upload_to='our_team/', verbose_name='Аватар')
    profession = models.CharField(max_length=255, verbose_name='Должность')
    full_name = models.CharField(max_length=255, verbose_name='Фамилия и имя')

    def __unicode__(self):
        return self.full_name


class Delivery(models.Model):
    class Meta:
        verbose_name_plural = 'Доставка'
        verbose_name = 'Доставка'


    key = models.CharField(max_length=255, verbose_name='Наименование')
    value = models.CharField(max_length=255, verbose_name='значение')

    def __unicode__(self):
        return "%s - %s" % (self.key, self.value)


class Datenschutz(models.Model):
    class Meta:
        verbose_name_plural = 'Политика конфиденциальности'

    body = RichTextUploadingField(verbose_name='Контент')

    def __unicode__(self):
        return 'Страница Политики Конфиденциальности'


class Slider(models.Model):
    class Meta:
        verbose_name_plural = 'Слайдер'
        verbose_name = 'слайд'

    image = models.ImageField(upload_to='slider/', verbose_name='Изображение')
    link = models.URLField(max_length=255, verbose_name='Ссылка', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активный?')

    title = models.CharField(max_length=255, verbose_name='Название ссылки', null=True, blank=True)
    short_description = models.CharField(max_length=255, verbose_name='Краткое описание', null=True, blank=True)
    is_sale = models.BooleanField(default=False, verbose_name='Акция?')

    def __unicode__(self):
        return get_wt_image_url(self.image)

    def save(self, *args, **kwargs):
        new_img_obj = Image.open(self.image)
        name = self.image.name
        if '/' in name:
            name = name.split('/')[len(name.split('/')) - 1]
        t_title = 'slide_' + name.split('.')[0] + '.png'
        new_img_bytes = BytesIO()
        new_img_obj.save(new_img_bytes, format='PNG')

        self.image.delete(save=False)
        self.image.save(
            t_title,
            content=ContentFile(new_img_bytes.getvalue()),
            save=False
        )
        super(Slider, self).save(*args, **kwargs)
        if self.image:
            try:
                add_watermark(self.image, settings.SITE_TITLE)
            except:
                pass


class SeoText(models.Model):
    class Meta:
        verbose_name = 'Текст на главной'
        verbose_name_plural = 'Текст на главной'

    title = models.CharField(max_length=255, verbose_name='Заголовок текста')
    text = RichTextUploadingField(verbose_name='Текст')

    def __unicode__(self):
        return self.title


class Contact(models.Model):
    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = ' Контакты'

    title = models.CharField(max_length=255,verbose_name='Заголовок')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    email = models.CharField(max_length=255, verbose_name='Email')
    phone = models.CharField(max_length=255, verbose_name='Телефон', null=True)
    location = GeopositionField(verbose_name='Местонахождение филиалла')

    def __unicode__(self):
        return self.title


class Reviews(models.Model):
    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    name = models.CharField(max_length=255, verbose_name='Имя')
    email = models.CharField(max_length=255, verbose_name='E-Mail')
    message = models.TextField(max_length=10000, verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания отзыва')
    is_active = models.BooleanField(default=False, verbose_name='Видимый отзыв')

    def __unicode__(self):
        return "%s, %s" % (self.name, self.email)


class Manufacturers(models.Model):
    class Meta:
        verbose_name = 'Производители'
        verbose_name_plural = 'Производители'

    content = RichTextUploadingField(verbose_name='Текст')

    def __unicode__(self):
        return 'Информация о производителях'

class TermsOfSaleOfGoods(models.Model):
    class Meta:
        verbose_name_plural = 'Условия продажи товаров'
        verbose_name = 'Условия продажи товаров'

    content = RichTextUploadingField(verbose_name='Текст')

    def __unicode__(self):
        return 'Условия продажи товаров'


class ReturnPolicy(models.Model):
    class Meta:
        verbose_name_plural = 'Условия возврата товаров'
        verbose_name = 'Условия возврата товаров'

    content = RichTextUploadingField(verbose_name='Текст')

    def __unicode__(self):
        return 'Условия возврата товаров'


class RepairTips (models.Model):
    class Meta:
        verbose_name_plural = 'Советы по ремонту'
        verbose_name = 'Советы по ремонту'

    content = RichTextUploadingField(verbose_name='Текст')

    def __unicode__(self):
        return 'Советы по ремонту'

