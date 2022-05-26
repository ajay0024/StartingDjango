from django import forms
from .models import Category, Page


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.max_name_length, help_text="Please enter Category Name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ("name",)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.max_title_length, help_text="Please enter title of the page")
    url = forms.URLField(max_length=200, help_text="Please eneter url of the page")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ("category",)
    def clean(self):
        cleaned_data=self.cleaned_data
        url=cleaned_data.get("url")
        if url and not url.startswith("http://"):
            url="http://"+url
            cleaned_data["url"]=url
            return cleaned_data
