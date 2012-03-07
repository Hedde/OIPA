from sorl.thumbnail.main import DjangoThumbnail

def ImgPreview(get_field, size):
    def wrapper(admin, obj):
        field = get_field(obj)
        if field:
            try:
                url = DjangoThumbnail(field, size).absolute_url
            except:
                return u'Thumb error(check if file exist)'
            return u'<img src="%s">' % url
        return u''
    wrapper.allow_tags = True
    wrapper.__name__ = 'Preview'
    return wrapper
