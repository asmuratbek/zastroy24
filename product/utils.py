import os

import datetime
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from io import BytesIO

from django.core.files.base import ContentFile
from django.utils.text import slugify

from MyBrands import settings


def add_watermark(in_file, text, angle=0, opacity=0.5):
    file_name, ext = os.path.splitext(in_file.path)
    out_file = '%s.wt%s' % (file_name, ext)
    if os.path.isfile(out_file):
        return None
    text = text.upper()
    img = Image.open(in_file).convert('RGB')
    watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
    size = 10
    n_font = ImageFont.truetype(settings.WATERMARK_FONT, size)
    n_width, n_height = n_font.getsize(text)

    while n_width + n_height < watermark.size[0] * .3 or n_width + n_height < 80:
        size += 2
        n_font = ImageFont.truetype(settings.WATERMARK_FONT, size)
        n_width, n_height = n_font.getsize(text)

    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text(((watermark.size[0] - n_width) - n_height / 2,
               (watermark.size[1] - n_height) - n_height / 2),
              text, font=n_font, fill="#5e4d99")
    watermark = watermark.rotate(angle, Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    Image.composite(watermark, img, watermark).save(out_file, 'PNG')
    return out_file


def rename_file(image, filename=None):
    new_img_obj = Image.open(image)
    name, ext = os.path.splitext(image.name)
    if '/' in name:
        name = name.split('/')[len(name.split('/')) - 1]
    t_title = slugify(name) + '.png' if not filename else filename
    new_img_bytes = BytesIO()
    new_img_obj.save(new_img_bytes, format='PNG')

    image.delete(save=False)
    image.save(
        t_title,
        content=ContentFile(new_img_bytes.getvalue()),
        save=False
    )


def get_wt_image_url(image):
    f, e = os.path.splitext(image.path)
    wt_image = '%s.wt%s' % (f, e)
    if os.path.isfile(wt_image):
        b, s = os.path.splitext(image.url)
        return '%s.wt%s' % (b, s)
    return image.url


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                        secure=settings.SESSION_COOKIE_SECURE or None)
    return response

