from django.forms import ModelForm, ImageField, CharField, FileInput,TextInput
from .models import Tag, Quote, Author, Picture
from django import forms


class TagForm(ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        model = Tag
        fields = ['name', 'tags']


class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']




class PictureForm(ModelForm):
    description = CharField(max_length=200, widget=TextInput(attrs={"class":"form-control"}))
    path = ImageField(widget=FileInput(attrs={"class":"form-control"}))

    class Meta:
        model = Picture
        fields = ['description', 'path']



