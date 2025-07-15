from django import forms
from .models import Page, Section, Image, Video, FAQ, Banner, Testimonial, MetaTag
from ckeditor.widgets import CKEditorWidget

class PageForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = Page
        fields = [
            'title',
            'template',
            'content',
            'is_published',
            'publish_date',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-2 px-3 border'
            }),
            'template': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-2 px-3 border',
                'placeholder': 'e.g., default.html or landing.html'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-indigo-600 border-gray-300 rounded'
            }),
            'publish_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-2 px-3 border'
            }),
        }

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['page', 'title', 'content', 'order', 'section_type', 'is_active']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['section', 'image', 'caption', 'order']


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['section', 'video_url', 'caption']


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['section', 'question', 'answer']


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title', 'subtitle', 'image', 'link', 'is_active', 'display_order']


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'message', 'image']


class MetaTagForm(forms.ModelForm):
    class Meta:
        model = MetaTag
        fields = ['page', 'meta_title', 'meta_description', 'meta_keywords']
