from django import template
from apps.gallery.models import Image, Gallery


register = template.Library()


def show_gallery(gallery_id):
    try:
        gallery_obj = Gallery.objects.get(id=gallery_id)
        image_group = gallery_obj.slug
        images_list = Image.objects.filter(gallery=gallery_obj)
    except Exception:
        image_group = ''
        images_list = None
    return {'image_group': image_group, 'images_list': images_list}


register.inclusion_tag('gallery.html')(show_gallery)
