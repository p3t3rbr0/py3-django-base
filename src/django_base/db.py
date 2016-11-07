from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile
from .settings import DEBUG, THUMBS_FORMAT, THUMBS_QUALITY

try:
    from PIL import Image
except Exception:  # Mac OSX
    import Image


def flat(*nums):
    'Build a tuple of ints from float or integer arguments. Useful because PIL crop and resize require integer points.'
    return tuple(int(round(n)) for n in nums)


class Size:
    def __init__(self, pair):
        self.width = float(pair[0])
        self.height = float(pair[1])

    @property
    def aspect_ratio(self):
        return self.width / self.height

    @property
    def size(self):
        return flat(self.width, self.height)


def cropped_thumbnail(img, size):
    '''
    Builds a thumbnail by cropping out a maximal region from the center of the original with
    the same aspect ratio as the target size, and then resizing. The result is a thumbnail which is
    always EXACTLY the requested size and with no aspect ratio distortion (although two edges, either
    top/bottom or left/right depending whether the image is too tall or too wide, may be trimmed off.)
    '''

    original = Size(img.size)
    target = Size(size)

    if target.aspect_ratio > original.aspect_ratio:
        # image is too tall: take some off the top and bottom
        scale_factor = target.width / original.width
        crop_size = Size((original.width, target.height / scale_factor))
        top_cut_line = (original.height - crop_size.height) / 2
        img = img.crop(flat(0, top_cut_line, crop_size.width, top_cut_line + crop_size.height))
    elif target.aspect_ratio < original.aspect_ratio:
        # image is too wide: take some off the sides
        scale_factor = target.height / original.height
        crop_size = Size((target.width/scale_factor, original.height))
        side_cut_line = (original.width - crop_size.width) / 2
        img = img.crop(flat(side_cut_line, 0,  side_cut_line + crop_size.width, crop_size.height))

    return img.resize(target.size, Image.ANTIALIAS)


class ImgThumbsFieldFile(ImageFieldFile):
    description = "Image with thumbs field file"

    def __init__(self, *args, **kwargs):
        super(ImageFieldFile, self).__init__(*args, **kwargs)

    def save(self, name, content, save=True):
        super(ImageFieldFile, self).save(name, content, save)
        if self.field.sizes:
            for size, opt in self.field.sizes.items():
                try:
                    self._generate_thumb(content, size, opt)
                except Exception:
                    if DEBUG:
                        import sys
                        print("Exception generating thumbnail")
                        print(sys.exc_info())

    # def delete(self, save=True):
    #     if self.name and self.field.sizes:
    #         for size in list(self.field.sizes.keys()):
    #             base, extension = self.name.rsplit('.', 1)
    #             thumb_name = self.THUMB_SUFFIX % (base, size[0], size[1], extension)
    #             try:
    #                 self.storage.delete(thumb_name)
    #             except:
    #                 if DEBUG:
    #                     import sys
    #                     print("Exception deleting thumbnails")
    #                     print(sys.exc_info())
    #     super(ImageFieldFile, self).delete(save)

    def _generate_thumb(self, image, size, opt):
        base, extension = self.name.rsplit('.', 1)  # Separate basename and extension
        s = tuple(map(lambda x: int(x), size.split('x')))

        im = Image.open(image).convert('RGB')
        im = cropped_thumbnail(im, s)  # im = prepare_image(im, s)

        if type(opt) is tuple and len(opt) and opt[0]:  # image.my_name.jpg
            thumb_name = self.storage.location+'/%s.%s.%s' % (base, opt[0], extension)
        else:  # image.512x512.jpg
            thumb_name = self.storage.location+'/%s.%sx%s.%s' % (base, s[0], s[1], extension)

        try:
            quality = opt[1]
        except Exception:
            quality = THUMBS_QUALITY

        im.save(thumb_name, THUMBS_FORMAT, quality=quality)

    def __getattr__(self, name):
        if name.startswith("url_"):
            img = name.replace("url_", "")
            base, ext = self.url.rsplit('.', 1)

            try:
                w, h = img.split('x')
                thumb = '%s.%sx%s.%s' % (base, w, h, ext)
            except Exception:
                thumb = '%s.%s.%s' % (base, img, ext)

            return thumb
        else:
            return super(ImgThumbsFieldFile, self).__getattr__(name)


class ImgThumbsField(ImageField):
    attr_class = ImgThumbsFieldFile

    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, sizes={}, **kwargs):
        self.name = name
        self.width_field = width_field
        self.height_field = height_field
        self.verbose_name = verbose_name
        self.sizes = sizes
        super(ImageField, self).__init__(verbose_name, name, **kwargs)
