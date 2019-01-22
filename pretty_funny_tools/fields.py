from django.db import models
from PIL import Image
import subprocess


class IntellegentImageField(models.ImageField):
    QUALITY = 80

    def pre_save(self, model_instance, add):
        file = super(IntellegentImageField, self).pre_save(model_instance=model_instance, add=add)

        im = Image.open(file.path)

        horisontal, vertical = False, False
        width = im.size[0]
        height = im.size[1]
        if width > height:
            horisontal = True
        else:
            vertical = True

        if horisontal:
            if width > 1300:
                basewidth = 1300
                wpercent = (basewidth / float(width))
                hsize = int((float(height) * float(wpercent)))
                out = im.resize((basewidth, hsize))
                out.save(file.path, quality=IntellegentImageField.QUALITY)
            else:
                im.save(file.path, quality=IntellegentImageField.QUALITY)
        if vertical:
            if height > 800:
                baseheight = 800
                hpercent = (baseheight / float(height))
                wsize = int(float(width) * float(hpercent))
                out = im.resize((wsize, baseheight))
                out.save(file.path, quality=IntellegentImageField.QUALITY)
            else:
                im.save(file.path, quality=IntellegentImageField.QUALITY)

        # optipng supports only some extensions
        if file.name.split('.')[-1] == 'png':
            try:
                subprocess.call(["optipng", file.path])
                print 'Warning: Package optipng is not installed!!!'
            except OSError:
                pass

        return file


from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ["^pretty_funny_tools\.fields\.IntellegentImageField"])
