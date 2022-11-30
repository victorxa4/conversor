from django.db import models
from django.contrib import admin

accepted_formats = [
    ('PNG', 'PNG'),
    ('JPEG', 'JPEG'),
    ('PPM', 'PPM'),
    ('GIF', 'GIF'),
    ('TIFF', 'TIFF'),
    ('BMP', 'BMP'),
    ('WEBP', 'WEBP')
]

class Conversion(models.Model):
    image_format = models.CharField(max_length=100)
    target_format = models.CharField(max_length=100)
    image = models.ImageField(upload_to='convertImages')

    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.image_format} to {self.target_format}'

class ConversionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Conversion, ConversionAdmin)