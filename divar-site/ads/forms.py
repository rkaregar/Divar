from django import forms
from django.shortcuts import get_object_or_404
from ads.models import Advertisement, Category, Images
from django.forms import inlineformset_factory


class AdvertisementCreationForm(forms.ModelForm):
    # category1 = forms.CharField(max_length=12)
    # category2 = forms.CharField(max_length=12)
    # category3 = forms.CharField(max_length=12)

    class Meta:
        model = Advertisement
        # fields = ('title', 'price', 'description', 'city', 'is_urgent', 'category1', 'category2', 'category3')
        fields = ('title', 'price', 'description', 'city', 'is_urgent')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_price(self):
        if self.cleaned_data['price'] == -1:
            return 'On Agreement'
        else:
            return str(self.cleaned_data['price'])

    def save(self, commit=True):
        # if self.cleaned_data['category3'] != '':
        #     category = get_object_or_404(Category, level=3, title=self.cleaned_data['category3'])
        # elif self.cleaned_data['category2'] != '':
        #     category = get_object_or_404(Category, level=2, title=self.cleaned_data['category2'])
        # else:
        #     category = get_object_or_404(Category, level=1, title=self.cleaned_data['category1'])

        if commit:
            self.instance = Advertisement.objects.create(title=self.cleaned_data['title'],
                                                         price=self.cleaned_data['price'],
                                                         is_urgent=self.cleaned_data['is_urgent'],
                                                         description=self.cleaned_data['description'],
                                                         city=self.cleaned_data['city'],
                                                         # category=category,
                                                         user=self.user)

        return self.instance


class ImagesCreationForm(forms.ModelForm):

    class Meta:
        model = Images
        exclude = ()


ImagesFormset = inlineformset_factory(parent_model=Advertisement, model=Images, fields=('image',),
                                      form=ImagesCreationForm, extra=3)
