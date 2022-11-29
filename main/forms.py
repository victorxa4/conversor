from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Conversion
from PIL import Image
from django.conf import settings
import os

accepted_formats = [
    ('PNG', 'PNG'),
    ('JPEG', 'JPEG'),
    ('PPM', 'PPM'),
    ('GIF', 'GIF'),
    ('TIFF', 'TIFF'),
    ('BMP', 'BMP')
]

class CreateUserProfileForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {'username': 'Username', 'email': 'Email'}

class EditUserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {'username': 'Username', 'email': 'Email'}

class ConvertImage(forms.Form):
    error_messages = {
        "same_formats": ("You can't convert a image formart to itself."),
    }

    image_format = forms.MultipleChoiceField(choices = accepted_formats)
    target_format = forms.MultipleChoiceField(choices = accepted_formats)
    image = forms.ImageField()

    # def clean_image_format(self):
    #     image_format = self.cleaned_data.get("image_format")
    #     target_format = self.cleaned_data.get("target_format")
    #     print(image_format)
    #     print(target_format)

    #     if image_format == target_format:
    #         raise ValidationError(
    #             self.error_messages["same_format"],
    #             code="same_format",
    #         )
    #     return image_format

    def clean(self):
        image_format = self.cleaned_data.get("image_format")[0]
        target_format = self.cleaned_data.get("target_format")[0]
        image = self.cleaned_data.get("image")

        if image_format == target_format:
            self.add_error("same_format", "You can't convert a image formart to itself.")
        else:
            return self.cleaned_data

    def save(self):
        image_format = self.cleaned_data.get("image_format")[0]
        target_format = self.cleaned_data.get("target_format")[0]
        image = self.cleaned_data.get("image")

        conversion = Conversion.objects.create(image_format=image_format, target_format=target_format, image=image)

        conversion.save()

        self.conversion = conversion

        # self.image_format= conversion.image_format
        # self.target_format = conversion.target_format
        # self.image = conversion.image
        
        return conversion

    def convert(self):
        if self.conversion.image:
            filename = self.conversion.image.name.split('.')[0]
            
            old_img = f'{settings.MEDIA_ROOT}\\{filename}.{self.conversion.image_format.lower()}'
            new_img = f'{settings.MEDIA_ROOT}\\{filename}.{self.conversion.target_format.lower()}'

            image = Image.open(old_img)

            rgb_image = image.convert("RGB")
            rgb_image.save(new_img)

            os.remove(old_img)

            self.conversion.image = f'{filename}.{self.conversion.target_format.lower()}'
            self.conversion.save()

            return self.conversion.image

    class Meta:
        model = Conversion
        fields = ['image_format', 'target_format', 'image']
        labels = {'image_format': 'Image Format', 'target_format': 'Target Format', 'image': 'Image'}